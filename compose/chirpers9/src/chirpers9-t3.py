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
# round 5 (section, w10 = bars 109-120, the crest cooling into the outfall; the mix-window out-seam had +32 dB at
# 10-15 kHz against t4's body): T3_R5=cool (default) - THE CREST COOLS TO ITS CORE. The top drops away layer by layer
# (hats to eighths at 109, quarters at 110, the octave lead out at 110, and in the last two bars before the crossfade
# the snare, hats, percussion, chip voices, arps and shards all gone) until only kick, undertow, floor, the clean E1
# lead and the robot's last line remain over the dust pad swelling in Dm(add9); and a glass line plays E1 in
# RETROGRADE, slowing - x2 (bars 109-110), then x4 an octave down (111-114) - a melody falling out of the lock.
# T3_R5=none reproduces v4.
R5 = os.environ.get("T3_R5", "cool") != "none"
# round 6 (Harry, 6 Nov 00:30: "ugly chaos ... atonal ... missing aesthetics and catchiness/hook ... play with time
# and texture"): T3_R6=tonal (default) - TONE IS HOME. E3 v2: the undertow on D | Bb | C (i - VI - VII), harmony
# Dm(add9) | Bbmaj7 | C(add9), no Neapolitan ground; the tracker arps walk those chords' own consonant intervals; the
# ring lead's modulator at 2:1 (harmonic sidebands, in tune) instead of 1.414; the alignment count climbs D Aeolian
# (E, not Eb); and THE HOOK - E1 stated plainly, upright and doubled, for two cycles at the top of the front (bar
# 17), the eyewall (41) and after the eye (67), so the storm's fragments are heard against the tune.
# T3_R6=none reproduces v5.
R6 = os.environ.get("T3_R6", "tonal") != "none"
# round 7 (section, w8 = bars 85-96, the lock arriving): T3_R7=sung (default) - THE HOOK IS SUNG. Harry: hooks want a
# voice that sings tunes cleanly. At the lock a legato singing voice (wM's voice-legato, unused on the album) sings
# "nothing here is late" ON E1 - five syllables, five notes, D A C G E in the seed's own rhythm - at bars 91 and 95,
# alone: the E1 lead steps out of those bars and answers in the bars after (call and response); the pvoc robot keeps
# only its later echoes (101, 109). T3_R7=none reproduces v6.
R7 = os.environ.get("T3_R7", "sung") != "none"
SUNG_BARS = (90, 94)
# round 9 (palette): T3_R9=tight (default) - A PLAYED KIT AND HANDS. (1) The 909 (an album staple: t2, t3, t5) gives way
# on every drum track to tight-kit - dry, close-miked, damped kick, tight snare, crisp rimshot and sidestick (the
# Smile / GoGo Penguin kit; no other Accretion track has it): the storm sounds played, not programmed (kh -> k, the
# clap -> sidestick). (2) A new part on congas (no other track has hand drums): E2's cell (hits 0 2 3 5 of seven:
# tumba / open / slap / muted, its D A F C as low-high-mid-low) cycling in sevens through the front (bars 25-40) and
# the eyewall's end (61-72), then at the lock it takes ONE MORE SIXTEENTH - the seven becomes eight - and sits on the
# bar through the crest. T3_R9=none reproduces v8.
R9 = os.environ.get("T3_R9", "tight") != "none"
# round 10 (WHOLE): T3_R10=accrete (default) - THE VOICE BECOMES THE SONG'S THREAD. With wM's voice-legato pinned
# (joined syllables, an inhale before each phrase, a wandering vibrato, smooth glides), t3's singer is a small near
# voice (tract 0.86, breath 0.35, ring 0.15, drier - t8's choir keeps the big dark one), and it carries E1 through
# the song instead of appearing once: (1) a distant wordless hum of E1 ("oo") in the front at bars 25 and 33 - the
# hook heard before it has words; (2) "nothing here is late" at the lock (91, 95), now legato; (3) the pvoc robot's
# echoes give way to the voice's ANSWER, "everything comes round" on E1 at bars 101 and 109 - the storm's arithmetic
# in five words. Whisper and the dry speech stay (not all singing). T3_R10=none reproduces v9.
R10 = os.environ.get("T3_R10", "accrete") != "none"
SUNG2_BARS, HUM_BARS = (100, 108), (24, 32)
# round 11 (section, w11 = bars 113-128, the overlap into t4 - flagged 'level jump'; the low-end handover agreed with
# chirper-three, 6 Nov 06:05): T3_R11=handover (default) - THE STORM HANDS OVER ITS RESIDUE. (1) The D1 thump stops
# at bar 112 (the floor steps down: the redshifting undertow is the soft floor left, and t4 puts a D2 sine under its
# lens that takes over); (2) a new warm mid pad - two triangles and an octave sine, slow in, a little chorus - holds
# Dm(add9) as D5 F5 A5 E6 (587-1319 Hz) from bar 113 to the end, swelling in: the 600-900 Hz warmth t4's cellos
# inherit, with the F that t4 lifts to F#; (3) the singer's last trace - the E1 hum ("oo") at HALF SPEED, far off,
# from bar 119: the tune handed to t4's handpan, which assembles E1 from its downbeat. T3_R11=none reproduces v10.
R11 = os.environ.get("T3_R11", "handover") != "none"
# round 12 (WHOLE): T3_R12=voices (default) - THE VOICE GATHERS COMPANY. wM's second voice batch is pinned (even
# vowels, singers: N, harmony): (1) t3's singer moves onto voice-near (wM's own close young voice: even vowels, so the
# 'ee' of 'everything' and the 'oo' of the hum no longer sink under the 'ah's) - the lead, the front hum and the last
# hum; (2) NEW: backing voices (voice-backing - three soft breathy singers on each line, even, little ring) sing the
# lock's harmony under the crest from bar 97 to 112 on 'ah', in two diatonic lines that follow Dm | Bb | C | Dm two
# beats a chord - F5 F5 E5 F5 over A4 Bb4 G4 A4 (sixths and a fifth) - 9-11 dB under the lead: the reward gets
# voices, and the crest gets the 600-900 Hz warmth t4's body has (the out-seam's worst band was 877 Hz, -17 dB);
# (3) the eye (bars 63-66) holds its breath on the same backing singers - an open D-A 'oo', four bars, very soft.
# T3_R12=none reproduces v11.
R12 = os.environ.get("T3_R12", "voices") != "none"
# round 13 (WHOLE): T3_R13=clean (default) - THE STORM IN TUNE, WITH ITS WEIGHT. Harry's "ugly chaos" in t3 lives in
# the storm's damage lanes: a 6-bit crush whose mix climbed to 0.6 on the bass and the arps through the eyewall,
# and a stutter firing on 42% of slices. Both eased (crush x0.4: at most 0.24 - grit you feel, not a broken radio;
# stutter x0.6) so the storm's complexity is its cycles and its tune, not its damage; and with the crush off the
# undertow, the bass and its floor come up 2 dB each (the album envelope had 44-97 Hz 8-12 dB light). T3_R13=none
# reproduces v12.
R13 = os.environ.get("T3_R13", "clean") != "none"
# round 14 (palette): T3_R14=boc (default; =air adds the shaker) - A WARM HIGH VOICE (AND, OPTIONALLY, SOME AIR). (1) The E1 line two octaves up (e1hi, the
# hook's top double from the crest on) was a ring-modulated pulse at -21 dB - presence -25 at the crest, unheard.
# It moves to boc-lead (a detuned saw + sine pair drifting in pitch, low-passed, chorused, tape-worn: the
# hauntological lead; no other Accretion track has it) at -12 dB: the seed's top line sung by a wobbly, nostalgic
# synth over the crest. (2) NEW PART - air: tight-kit's shaker in sixteenths through the front and the eyewall (bars
# 17-40 - the front; in the eyewall too it cost recurrence 2.4), accented on E2's seven-cycle (hits 0 2 3 5 of seven, like the congas below it). The
# storm's top end had been the crush's aliasing (v13 eased it; the front fell 14 dB under t2's body at 9 kHz) - now
# it is a played texture. (A tambourine on two and four over the crest brightened the out-seam body against t4:
# cut.) T3_R14=none reproduces v13.
# DEFAULT IS boc: the shaker (T3_R14=air) helped the in-seam flow +1.9 but cost recurrence 1.9 (s0) / 5.8 (s11) -
# the storm's sections stopped returning to each other - so it is kept only as an option.
R14 = os.environ.get("T3_R14", "boc") != "none"
# round 15 (WHOLE): T3_R15=open (default) - THE LOCK OPENS. The crest is the storm's reward, and it was static (the
# sections map: w9 'static, little new vs w8'): Dm | Bb | C | Dm, two beats a chord, for 24 bars. Now, for the eight
# bars of the answer (101-108, "everything comes round"), the lock's last two chords turn: Dm | Bb | F | C - i VI III
# VII, the relative major lifting under the singer, then C falling back to Dm as the crest cools (109). Shards, arps,
# the undertow and its floor move in place (same events, new pitches: C -> F is the riff up a fourth; Dm(add9) -> C
# (add9) note by note), and the backing singers follow (F5 F5 F5 E5 over A4 Bb4 A4 G4). E1 sits on it: its D A C
# over F, its G E over C. T3_R15=none reproduces v14.
R15 = os.environ.get("T3_R15", "open") != "none"
OPEN_BARS = (100, 108)
R14_AIR = os.environ.get("T3_R14", "boc") in ("air", "shaker")
R14_BOC = os.environ.get("T3_R14", "boc") in ("air", "boc")
# round 8 (section, w5 = bars 49-60, the eyewall's first half, flagged 'little new'): T3_R8=seven (default) - TIME,
# NOT NOISE. The storm's random Euclid drums give way for 12 bars to ONE groove in sevens: E2's cell (hits 0 2 3 5 of
# 7 sixteenths) as kick / hat / snare / hat, cycling across the bar line - a cross-rhythm you can follow - and over it
# the glass sings E1 STRETCHED x2 (D A C G E, ten beats a statement) three times: the hook as a long line above the
# storm. T3_R8=none reproduces v7.
R8 = os.environ.get("T3_R8", "seven") != "none"
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
if R6:                                    # E3 v2: D | Bb | C, consonant
    E3_RIFF = [("D2", 0.75), ("D2", 0.75), ("D3", 0.5), ("Bb1", 0.5), ("Bb1", 0.75), ("F2", 0.75), ("C2", 0.75),
               ("C2", 0.75), ("G2", 0.5), ("C3", 1.0)]
    E3 = [((50, 57, 64, 65), 2.0),        # Dm(add9):  D3 A3 E4 F4
          ((46, 53, 57, 62, 65), 2.0),    # Bbmaj7:    Bb2 F3 A3 D4 F4
          ((48, 55, 62, 64), 3.0)]        # C(add9):   C3 G3 D4 E4
# the lock under R6 resolves HOME every two bars (D minor, not C): harmony Dm | Bb | C | Dm (2+2+2+2) and the riff's
# held last beat becomes C -> D
LOCK_SEQ = [(0, 2.0), (1, 2.0), (2, 2.0), (0, 2.0)]


def lock_riff():
    if R6:
        return E3_RIFF[:-1] + [("C3", 0.5), ("D3", 1.5)]
    return E3_RIFF[:-1] + [(E3_RIFF[-1][0], E3_RIFF[-1][1] + 1.0)]
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
if R6:
    ARP_STEPS = {0: [0, 7, 14, 15, 19], 1: [0, 7, 11, 16, 19], 2: [0, 7, 14, 16, 19]}  # m(add9) | maj7 | add9


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
        for n, ln in (E3_RIFF if at < CREST * 4 else lock_riff()):
            if ln >= 0.75 and 64 <= at < 112 * 4 and not (EYE[0] * 4 <= at < EYE[1] * 4 or BREAK[0] * 4 <= at < BREAK[1] * 4):
                T["floor"].add(at, ln * 0.9, mtok(midi(n) - 12 if midi(n) >= 36 else midi(n)), 90)
            at += ln
    # the lock and after: re-barred 2+2+4, steady
    for bar in range(CREST, 112, 2):
        at = bar * 4.0
        for k, beats in (LOCK_SEQ if R6 else list(enumerate(E3_LOCKED))):
            ch = E3[k][0]
            T["shard"].add(at, 0.22, ",".join(mtok(m) for m in ch), 96)
            T["shard"].add(at + 0.75, 0.22, ",".join(mtok(m) for m in ch), 78)
            if beats > 2:
                T["shard"].add(at + 2.5, 0.22, ",".join(mtok(m) for m in ch), 84)
            T[f"arp{k}"].add(at, beats - 0.05, mtok(ch[0] + 12), 78)
            T["hold"].add(at, beats - 0.1, ",".join(mtok(m + 12) for m in ch[1:]), 70)
            T["sub"].add(at, beats - 0.1, mtok(ch[0] - 24), 70)
            at += beats
        at = bar * 4.0
        for j, (n, ln) in enumerate(lock_riff()):              # the riff, re-barred: its last C held a beat more
            ln2 = ln
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
        lock = lock_riff()                                                       # 8 beats
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
    for bar in (() if R10 else (100, 108) if R7 else (92, 100, 108)):
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
        steps = ["D5", "E5" if R6 else "Eb5", "F5", "G5", "A5", "Bb5", "C6"]  # (R4 count)
        for bar in range(72, 86):
            T["tick"].add(bar * 4.0, 0.9, mtok(midi(steps[(bar - 72) // 2])), 84 + 2 * (bar - 72) + (12 if bar in hits else 0))
    if R15:                                                 # the crest's answer: Dm | Bb | F | C
        lo, hi = OPEN_BARS[0] * 4.0, OPEN_BARS[1] * 4.0

        def dm_to_c(m):
            return m - 1 if m % 12 == 5 else m - 2           # F -> E; D, A, E -> C, G, D

        for k in ("shard", "arp0", "arp1", "arp2", "bass", "floor", "hold"):
            if k not in T:
                continue
            ev = []
            for e in T[k].ev:
                if lo <= e[0] < hi and isinstance(e[2], str) and e[2].startswith("m"):
                    pos = (e[0] - CREST * 4.0) % 8.0
                    f = (lambda m: m + 5) if 4.0 <= pos < 6.0 else dm_to_c if pos >= 6.0 else None
                    if f is not None:
                        e = (e[0], e[1], ",".join(mtok(f(int(float(h[1:])))) for h in e[2].split(",")), e[3], e[4])
                ev.append(e)
            T[k].ev = ev
    if R8:                                                  # w5: one groove in sevens + E1 stretched on the glass
        lo, hi = 48 * 4.0, 60 * 4.0
        # silence (velocity 1) rather than delete, so later events keep their per-event randomness; the new parts
        # live on their own tracks
        for k in ("kick", "snare", "hats"):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
        for k in ("kick7", "snare7", "hats7", "glass7"):
            T[k] = Track(k)
        for c in range(48 * 16, 60 * 16, 7):
            b = c / 4.0
            T["kick7"].add(b, 0.25, "k", 114)
            T["hats7"].add(b + 0.5, 0.1, "h", 74)
            T["snare7"].add(b + 0.75, 0.25, "D4", 104)
            T["hats7"].add(b + 1.25, 0.1, "h", 62)
        at = lo
        for _ in range(3):
            for n, ln in E1:
                T["glass7"].add(at, ln * 2 * 0.95, mtok(midi(n) + 12), 86)
                at += ln * 2
    if R7:                                                  # the voice sings E1 alone in its bars; the lead answers
        for bar in SUNG_BARS:
            T["e1"].ev = [e for e in T["e1"].ev if not (bar * 4.0 <= e[0] < bar * 4.0 + 4.0)]
            T["e1hi"].ev = [e for e in T["e1hi"].ev if not (bar * 4.0 <= e[0] < bar * 4.0 + 4.0)]
    if R6:                                                  # the hook, plainly: E1 upright, two cycles, doubled
        for bar in (16, 40, 66):
            a0 = bar * 4.0
            T["e1"].ev = [e for e in T["e1"].ev if not (a0 <= e[0] < a0 + 10.0)]
            at = a0
            for _ in range(2):
                for n, ln in E1:
                    T["e1"].add(at, ln * 0.92, mtok(midi(n) + 12), 102)
                    T["e1hi"].add(at, ln * 0.92, mtok(midi(n) + 24), 74)
                    at += ln
    if R5:
        a, b, c = 108 * 4.0, 110 * 4.0, 112 * 4.0
        T["hats"].ev = [e for e in T["hats"].ev if not (a <= e[0] < c)]
        for bar, step, v in ((108, 0.5, 66), (109, 1.0, 56)):
            for k in range(int(4 / step)):
                T["hats"].add(bar * 4.0 + k * step, 0.1, "h", v - 3 * k)
        T["e1hi"].ev = [e for e in T["e1hi"].ev if not (109 * 4.0 <= e[0] < c)]
        for k in ("snare", "perc", "e2", "chipsn", "chiphat", "arp0", "arp1", "arp2", "shard", "floor", "sub"):
            T[k].ev = [e for e in T[k].ev if not (b <= e[0] < c)]
        T["dust"].add(a, 16.0 - 0.2, ",".join(mtok(m) for m in E3[0][0]), 72)
        retro = list(reversed(E1))
        at = a
        for n, ln in retro:
            T["glass"].add(at, ln * 2 * 0.95, mtok(midi(n) + 12), 84)
            at += ln * 2
        for n, ln in retro:
            T["glass"].add(at, ln * 4 * 0.95, mtok(midi(n)), 76)
            at += ln * 4
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
    if R13:
        stut = [[p_, round(v * 0.6, 3)] for p_, v in stut]
        grit = [[p_, round(v * 0.4, 3)] for p_, v in grit]

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
                              "synth": {"layers": [{"name": "m", "wave": "sine", "ratio": 2.0 if R6 else 1.414, "audible": False},
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
    if R2 or R4 or R5 or R8:
        patches["a3-glass"] = {"about": "chirper-two: the crest's glass - a sine phase-modulated at 3.5:1, the index pinged "
                                        "on each attack and settling to a faint shimmer; an octave partial; no low end",
                               "synth": {"layers": [{"name": "g", "ratio": 3.5, "audible": False},
                                                    {"wave": "sine", "pm": [{"from": "g", "depth": {"value": 0.06, "mod": [
                                                        {"src": "env.ping", "amount": 0.45}]}}]},
                                                    {"wave": "sine", "ratio": 2, "level": "-14dB"}],
                                         "env": {"ping": {"a": "0.5ms", "d": "250ms", "s": 0.05, "r": "100ms"}},
                                         "filters": ["hp cutoff=300", "lp cutoff=8000 q=0.6"],
                                         "amp": {"a": "2ms", "d": "600ms", "s": 0.45, "r": "400ms"}}}
    if R2 or R5 or R8:
        tracks.append({"name": "glass", "patch": "a3-glass", "gain": "-8dB", "pan": 0.25,
                       "fx": ["delay time=3/8 mix=0.2 feedback=0.35"], "sends": {"space": "-6dB"},
                       "score": T["glass"].score()})
    if R4:
        tracks.append({"name": "speak", "patch": "voice-speech", "gain": "3dB", "pan": 0.0,
                       "fx": ["delay time=3/8 mix=0.12 feedback=0.25"], "sends": {"space": "-10dB"}, "notes": CLEAR})
        tracks.append({"name": "tick", "patch": "a3-glass", "gain": "-10dB", "pan": -0.2,
                       "fx": ["delay time=1/4 mix=0.2 feedback=0.4"], "sends": {"space": "-6dB"},
                       "score": T["tick"].score()})
    if R9:
        import re
        for tr in tracks:
            if tr.get("patch") == "909":
                tr["patch"] = "tight-kit"
                tr["score"] = re.sub(r"(?<![a-z])cp/", "ss/", re.sub(r"(?<![a-z])kh/", "k/", tr["score"]))
        hand = Track("hand")
        cell = ((0, "lo", 82), (2, "o", 70), (3, "sl", 88), (5, "mu", 62))
        for lo, hi, period in ((24, 40, 7), (60, 72, 7), (72, 112, 8)):
            for c in range(lo * 16, hi * 16, period):
                for pos, head, vel in cell:
                    if c + pos < hi * 16:
                        hand.add((c + pos) / 4.0, 0.25, head, vel - (6 if lo == 72 and hi == 112 and c >= 88 * 16 else 0))
        # the tight kick is damped (no boom): a tuned 808 thump on D1 under every kick gives the storm back its floor,
        # on the home note
        ksub = Track("ksub")
        for k in ("kick", "kick7"):
            for e in (T[k].ev if k in T else []):
                if e[3] > 1 and not (R11 and e[0] >= 112 * 4.0):
                    ksub.add(e[0], 0.3, "D1", e[3])
        tracks.append({"name": "ksub", "patch": "808-short", "gain": "-4dB", "score": ksub.score()})
        tracks.append({"name": "hand", "patch": "congas", "gain": "-7dB", "pan": 0.3, "sends": {"space": "-12dB"},
                       "score": hand.score()})
    if R8:
        spec = {tr["name"]: tr for tr in tracks}
        for new, old in (("kick7", "kick"), ("hats7", "hats"), ("snare7", "skin"), ("glass7", "glass")):
            if old in spec:
                tracks.append(dict(spec[old], name=new, score=T[new].score()))
    if R7:
        src = json.load(open(os.path.join(HERE, "t3", "sung.json")))["tracks"][0]
        # voice-legato (join/inhale/wander/glide_smooth) needs a newer engine than the groove pin: until it is pinned,
        # the built-in singing voice with a mono glide carries the line (same notes, same phonemes)
        patches["a3-sung"] = dict(src["patch"], extends="voice play.glide=90ms play.mono=true")
        if R10:
            patches["a3-sung"] = dict(src["patch"], extends="voice-legato synth.layers.0.tract=0.86 "
                                                            "synth.layers.0.breath=0.35 synth.layers.0.ring=0.15")
        if R12:
            patches["a3-sung"] = dict(src["patch"], extends="voice-near")

        def place(srcn, bars, scale=1.0):
            out = []
            for bar in bars:
                for n in srcn:
                    d = {"at": round(bar * 4.0 - 0.25 + n["at"], 4), "len": n["len"], "ph": n["ph"],
                         "pitch": n["pitch"], "vel": round(n["vel"] * scale, 3)}
                    if n.get("expr_path"):
                        d["expr_path"] = n["expr_path"]
                    out.append(d)
            return out
        notes = place(src["notes"], SUNG_BARS)
        if R10:
            notes += place(json.load(open(os.path.join(HERE, "t3", "sung2.json")))["tracks"][0]["notes"], SUNG2_BARS)
            tracks[:] = [tr for tr in tracks if tr["name"] != "robot"]
            hum = place(json.load(open(os.path.join(HERE, "t3", "hum.json")))["tracks"][0]["notes"], HUM_BARS, 0.85)
            tracks.append({"name": "hum", "patch": "a3-sung", "gain": "-8dB", "pan": -0.2,
                           "fx": ["delay time=3/8 mix=0.3 feedback=0.4"], "sends": {"space": "-1dB"}, "notes": hum})
        # the lock's groove was buried under the undertow (presence, bars 89-96: bass -0.2 dB vs the mix, the 909 snare
        # -26, hats -34, percussion -42): the bass steps back and the kit comes up, so the reward is a groove you hear
        for tr in tracks:
            g = {"bass": -3.5, "snare": 9.0, "hats": 8.0, "perc": 8.0}.get(tr["name"])
            if g is not None:
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + g:g}dB"
        tracks.append({"name": "sung", "patch": "a3-sung", "gain": "0dB", "pan": 0.0,
                       "fx": ["delay time=3/8 mix=0.14 feedback=0.25"], "sends": {"space": "-7dB"}, "notes": notes})
        if R10:
            tracks[-1].update({"fx": ["delay time=3/8 mix=0.1 feedback=0.2"], "sends": {"space": "-11dB"}})
    if R12:
        hi, lo = [], []
        for bar in range(96, 112, 2):
            opened = R15 and OPEN_BARS[0] <= bar < OPEN_BARS[1]
            for j, (h, l) in enumerate(((77, 69), (77, 70), (77, 69), (76, 67)) if opened else
                                       ((77, 69), (77, 70), (76, 67), (77, 69))):
                at = bar * 4.0 + j * 2.0
                ln = 1.75 if j == 3 else 2.0                      # touching inside the two bars, a breath at the end
                v = 0.62 + 0.04 * ((bar - 96) // 4)
                hi.append({"at": at, "len": ln, "ph": "AA1", "pitch": mtok(h), "vel": round(v, 3)})
                lo.append({"at": at, "len": ln, "ph": "AA1", "pitch": mtok(l), "vel": round(v - 0.04, 3)})
        for b0 in range(EYE[0], EYE[1], 2):                            # the eye: an open D-A 'oo', held
            hi.append({"at": b0 * 4.0, "len": 7.5, "ph": "UW1", "pitch": mtok(74), "vel": 0.45})
            lo.append({"at": b0 * 4.0, "len": 7.5, "ph": "UW1", "pitch": mtok(69), "vel": 0.42})
        # their breath was a 10-15 kHz hiss over the crest (+24..28 dB over t4's body): darkened to the vowel
        tracks.append({"name": "backhi", "patch": "voice-backing", "gain": "-11dB", "pan": 0.35, "fx": ["lp cutoff=4500"],
                       "sends": {"space": "-6dB"}, "notes": hi})
        tracks.append({"name": "backlo", "patch": "voice-backing", "gain": "-13dB", "pan": -0.35, "fx": ["lp cutoff=4500"],
                       "sends": {"space": "-6dB"}, "notes": lo})
    if R11:
        patches["a3-residue"] = {"about": "chirper-two: the storm's residue for t4 - two triangles a few cents apart and "
                                          "an octave sine, slow in, mids only (600-1300 Hz), a little chorus",
                                 "synth": {"layers": [{"wave": "triangle", "detune": -5}, {"wave": "triangle", "detune": 5},
                                                      {"wave": "sine", "ratio": 2, "level": "-14dB"}],
                                           "filters": ["hp cutoff=320", "lp cutoff=3200 q=0.4"],
                                           "amp": {"a": "4s", "d": "1s", "s": 0.9, "r": "4s"}}}
        res = Track("residue")
        res.add(112 * 4.0, 16 * 4.0 - 0.2, ",".join(mtok(m) for m in (74, 77, 81, 88)), 78)
        tracks.append({"name": "residue", "patch": "a3-residue", "gain": "-16dB", "pan": 0.0, "fx": ["chorus mix=0.3"],
                       "sends": {"space": "-6dB"}, "score": res.score()})
        if R10 and R7:
            hsrc = json.load(open(os.path.join(HERE, "t3", "hum.json")))["tracks"][0]["notes"]
            last = []
            for n in hsrc:
                d = {"at": round(118 * 4.0 - 0.5 + n["at"] * 2, 4), "len": round(n["len"] * 2, 4), "ph": n["ph"],
                     "pitch": n["pitch"], "vel": round(n["vel"] * 0.8, 3)}
                if n.get("expr_path"):
                    d["expr_path"] = n["expr_path"]
                last.append(d)
            tracks.append({"name": "humlast", "patch": "a3-sung", "gain": "-9dB", "pan": 0.2,
                           "fx": ["delay time=3/8 mix=0.35 feedback=0.45"], "sends": {"space": "0dB"}, "notes": last})
    if R14:
        for tr in tracks:
            if tr["name"] == "e1hi" and R14_BOC:
                tr["patch"], tr["gain"] = "boc-lead", "-6dB"
                tr.get("auto", {}).pop("ring", None)
        air = Track("air")
        for bar in (range(16, 40) if R14_AIR else ()):
            if EYE[0] <= bar < EYE[1]:
                continue
            for s in range(16):
                g = bar * 16 + s
                acc = (g % 7) in (0, 2, 3, 5)
                air.add(g / 4.0, 0.1, "shk", 72 if acc else 44)
        if R14_AIR:
            tracks.append({"name": "air", "patch": "tight-kit", "gain": "-5dB", "pan": 0.25, "sends": {"space": "-12dB"},
                       "score": air.score()})
    if R13:
        for tr in tracks:
            if tr["name"] in ("bass", "floor"):
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + 2.0:g}dB"
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
