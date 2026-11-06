#!/usr/bin/env python3
"""chirpers IX (Accretion), track 5 (chirper-zero): the inner disk - calm again, but closer and hotter. t1's mirror.

t1 (Nucleation) began scattered and converged once. Here everything arrives already whole but TIGHT - the inner disk
orbits faster - and the new element, E5 'the inner orbit' (compose/chirpers9/motifs.md: v2 A G A . E . A G A . D ., a
3-beat ostinato in D; v1's G# went in v6, Harry's 'tone is home'), circles under it all. It carries:
  E1 (t1) diminished x2 (a 2.5-beat cycle) in stretto, two chip voices a bar-and-a-bit apart;
  E2 (t2, 'seven': hits on 0 2 3 5 of seven sixteenths) as the drum machine's cell against the 4/4 floor;
  E4 (t4, 'four lights': D9, Bbmaj13#11, Am11, D9sus) twice as fast as t4 (one chord per 10 beats), voiced close;
  E5 on an NES pulse, first in sixteenths, tightening to a trill in the build.
Every cycle (2.5, 5, 7/16, 3, 40) is phased to land on one shared downbeat at the crest (C). Then the outro (the
t5 -> t6 overlap, flat 120) pulls them apart: E5 stretches (augmented) while E1 squeezes (diminished), into t6's tide.

Since v6: E1 is stated plainly first (8 bars at its own speed) before the stretto, E4's second light is Bbmaj9 (no #11),
and the air is a pitched drone on D and A. All the complexity is in the time; the pitch is consonant D mixolydian
with a borrowed bVI.

Tempo 112 (flat across the t4 -> t5 overlap) rising to 120 (flat across t5 -> t6). Home D mixolydian. The voice:
one word, 'nearer', spoken by a robot (pvoc) that sings E5's notes.

Writes songs/chirpers9-t5.yaml (or $C9T5_OUT).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("C9T5_OUT", os.path.join(ROOT, "songs", "chirpers9-t5.yaml"))

BAR = 4
FORM = [("head", 16), ("A", 40), ("build", 20), ("C", 32), ("outro", 16)]
ST, _b = {}, 0
for _n, _l in FORM:
    ST[_n] = _b * BAR
    _b += _l
END = {n: ST[n] + l * BAR for n, l in FORM}
TOTAL = _b * BAR              # 496 beats
TC = ST["C"]                  # the crest: every cycle's shared downbeat

E1_OFF = [0.0, 0.5, 1.25, 1.5, 2.5]
E1_LEN = [0.5, 0.75, 0.25, 1.0, 1.5]
E1_MIDI = [62, 69, 72, 67, 64]               # D4 A4 C5 G4 E4
E5 = [(0, 69), (1, 68), (2, 69), (4, 76), (6, 69), (7, 68), (8, 69), (10, 74)]   # sixteenth, MIDI
TONAL = os.environ.get("C9T5_TONAL", "1")   # WHOLE ROUND (Harry, 00:30: 'quite ugly chaos ... atonal, very tough listening; get musicality back and play with time and texture'): TONE IS HOME - E5 v2 drops its G# for G (A G A . E . A G A . D ., a hummable ostinato in D, the time idea kept whole), E4's second light becomes Bbmaj9 (no E against the Bb), and the GENDYN air (a noise cloud, buried anyway) is cut. D mixolydian with a borrowed bVI: every clash gone, the complexity left in the time (the 3-beat orbit, E2's seven, E1's stretto, the converging cycles)
SEAMHEAD = os.environ.get("C9T5_SEAMHEAD", "hold,assemble")   # SECTION (w1, 0:00-0:34, the head = the t4 -> t5 overlap; flagged static; chirper-three 01:20: t4's fall holds D9 with F#, so my head's move to Bbmaj9 at bar 9 rubbed F against F#): THE ORBIT ASSEMBLES AS THE SEED DISASSEMBLES - the head's light holds D9 for all 16 bars ('hold'), and ('assemble') E5 builds itself hit by hit, one more every two cycles (A, then E, D, the A's, the G neighbours last), while t4's handpan E1 loses one note every two cycles down to its lone D: the two elements cross in the overlap, and E5 is whole as A begins
ORBITLEAD = os.environ.get("C9T5_ORBITLEAD", "128:192:low")   # SECTION (w3, 1:08-1:42, A's second half; presence: the quick bass loudest at -3 dB, E5 - t5's hook - 12 dB under the mix and followable 12% of the time): THE ORBIT SINGS - a Rhodes (new to the album) doubles E5 v2, swelling in over four bars and out again before the build; the orbit itself comes forward and the quick bass steps back, so for half a minute t5's hook is the tune you hear. Value 'A:B' or 'A:B:low' (the Rhodes an octave down)
CRESTE1 = os.environ.get("C9T5_CRESTE1", "rhodes")   # SECTION (w5, 2:15-2:48, the build's end and the crest; presence at the crest: the voice and the 808 loudest, E1's two voices 16-17 dB under and followable a fifth of the time): E1 SINGS ON THE CREST - for the first four cycles after the meeting the seed is heard plainly: 'rhodes' adds the Rhodes (the one that sang E5 in A) on E1 in octaves with the seed voices, 'lift' brings the two seed voices forward instead (x1.4)
WEIGHT = os.environ.get("C9T5_WEIGHT", "2")   # SECTION (w4, 1:42-2:15, A's end into the build - never focused; the 808's arrival was a quiet swap of one bass for another): THE WEIGHT ARRIVES - for the last WEIGHT bars of A the quick bass and the drums step out (the orbit, E1's stretto and the lights carry on), and the 808 lands on the build's downbeat on D, its first two bars full - the inner disk's gravity as an event
VOICEP = os.environ.get("C9T5_VOICEP", "near,harm")   # WHOLE ROUND (voice batch 2 pinned): THE NEAR VOICE - t5 is the disk 'closer and hotter', so its singer is voice-near (close, young, breathy, even vowels) where t1's is a far little choir; 'harm' adds a harmony a fourth below on the line after the crest (A G A E A D over E D E B E A, all in D mixolydian), the line's one moment of two voices
OUTLINE = os.environ.get("C9T5_OUTLINE", "x1")   # SECTION (w8, 3:52-4:18, the outro = the t5 -> t6 overlap; never focused): THE LINE STRETCHES - the outro's single 'near-er' becomes the whole sung line once more, 'near-er the mid-dle hums', stretched to half speed like E5 in the tide ('x2'), or twice at its own speed ('x1'): the hook as the inner disk lets go into t6, resolving to D
VOXA = os.environ.get("C9T5_VOXA", "110,140,170")   # WHOLE ROUND: THE LINE IS A CHORUS - the sung line 'near-er the mid-dle hums' first came only after the crest; now the voice sings it in A too (comma-separated beats), over the Rhodes' E5, so by the crest it is a tune you already know: the song's chorus, heard early, returned to at the crest and the end (Harry: hooks stated plainly and repeated enough to stick)
KEYHARM = os.environ.get("C9T5_KEYHARM", "1")   # WHOLE ROUND (harmony in a key is pinned): THE LINE IN THIRDS - the chorus is heard plain three times in A; at the crest its harmony becomes a third above IN THE KEY (D mixolydian: A G A E A D over C B C G C F#), sweeter than the fixed fourth below; with 'out' the farewell in the tide is sung in thirds too, ending on D with F# above it (the D major the album resolves to)
ARC = os.environ.get("C9T5_ARC", "0.2")   # WHOLE ROUND: THE ARC AFTER THE CREST - from four bars after the crest to the outro, the instruments (not the voices, not the spin) ease by ARC (a velocity fraction: + settles, - heats toward t6's storm)
TONALAIR = os.environ.get("C9T5_TONALAIR", "shimmer")   # with TONAL: keep the air ('keep'), or swap the GENDYN cloud for a pitched drone-shimmer on D2+A2 ('shimmer')
PLAINE1 = os.environ.get("C9T5_PLAINE1", "8")   # with TONAL: E1 stated plainly first - A opens with the seed at its own speed (5 beats, the high voice alone, the hook as t1 left it) for PLAINE1 bars before the stretto begins
if TONAL:
    E5 = [(s_, 67 if p_ == 68 else p_) for s_, p_ in E5]
E2_HITS = [0, 2, 3, 5]                        # of 7 sixteenths
E4 = [  # E4 'four lights', voiced close around middle C
    ["D2", "D3", "F#3", "A3", "C4", "E4"],
    ["Bb1", "Bb2", "D3", "A3", "E4", "G4"],
    ["A1", "A2", "C3", "G3", "D4", "E4"],
    ["D2", "D3", "G3", "A3", "C4", "E4"],
]
E4V2 = os.environ.get("C9T5_E4V2", "1")   # WHOLE ROUND: E4 v2 (chirper-three, motifs.md): D9 | Cmaj9 | Am11 | G6/9, all D mixolydian - t5's lights, floor, quick bass and 808 move with it, so t4, t5 and t6 share one harmony and nothing borrowed rubs
SUNG = os.environ.get("C9T5_SUNG", "1")   # WHOLE ROUND (the voice engine is pinned: voice-legato, joined, breathing): THE VOICE SINGS - the robot (pvoc) gives way to a sung line on voice-legato: 'near-er' on A G, and the line 'near-er the mid-dle hums' on E5 v2's notes A G A E A D, joined in one breath and resolving to D
if TONAL:
    E4[1] = ["Bb1", "Bb2", "D3", "F3", "A3", "C4"]
if E4V2:
    E4 = [["D2", "D3", "F#3", "A3", "C4", "E4"], ["C2", "C3", "E3", "G3", "B3", "D4"],
          ["A1", "A2", "C3", "G3", "D4", "E4"], ["G1", "G2", "B2", "E3", "A3", "D4"]]
E4_LEN = 10.0                                 # beats per chord (t4: 5)
CRESTGAP = os.environ.get("C9T5_CRESTGAP", "8")   # SECTION (w5, the build into the crest: flagged static; the crest was a level line, -12.1 dB either side): THE PULL BEFORE THE MEETING - for the last CRESTGAP beats before the crest the drums, the quick bass and the floor drop out and every heat filter is sucked shut, only the orbit's trill and E1's stretto left spinning; then every cycle lands on the shared downbeat at once: the filters snap open past where they were, and the drum machine and a crash hit together
SPIN = os.environ.get("C9T5_SPIN", "384:448:full")   # SECTION (w7, 3:20-3:52, C's second half: flagged static, little new vs w6; presence: the drums 13 dB under the mix, followable 7% of the time): THE DISK SPINS UP - a second 909 swells in over E2's seven: ride eighths, a backbeat on 2 and 4 (and with 'full', four on the floor), straight time against the seven-sixteenth cell, the first hint of t6's storm; it falls away as the outro's tide begins. Value 'A:B' or 'A:B:full' = beats
VOXLINE = os.environ.get("C9T5_VOXLINE", "326,346,366")   # SECTION (w6, 2:48-3:20, C after the crest: flagged static, little new vs w5): THE VOICE ACCRETES - after the crest the robot's one word grows into a line, 'nearer. the middle hums.' (the voice sideways about the disk's centre), sung on E5's notes by the same pvoc robot, three times across the window. Value: comma-separated beats
BASS808 = os.environ.get("C9T5_BASS808", "-10")   # WHOLE ROUND: THE WEIGHT OF THE INNER DISK - E2's seven-eighths bass moves from the CZ pluck (short, light) to an 808 (unused on the album until now): the same hits on E4's roots, now ringing and dropping in pitch on each attack, so the inner disk has the gravity the outer disk lacked (the low end around 100 Hz was 17 dB short). Value = gain dB
BASSFROM = os.environ.get("C9T5_BASSFROM", "build")   # with BASS808: the section the 808 takes over from ('build' or 'C'); before it the CZ pluck stays - the weight arrives as the disk tightens
FLOORUP = os.environ.get("C9T5_FLOORUP", "")   # with it: the held roots an octave up and opened (lp 500 -> 900 Hz), gain dB
CRESTHIT = os.environ.get("C9T5_CRESTHIT", "-14")   # with CRESTGAP: the crash's gain (dB)
CRESTDEEP = os.environ.get("C9T5_CRESTDEEP", "1")   # with CRESTGAP: a deeper pull - E1's stretto leaves too and the filters close to near-dark, so only E5's trill is left spinning into the meeting


def heat(pre, peak, after, end, lo=-0.6, at_a=True):
    """A heat lane: lo at the top, 0 at A, rising to `pre` by the crest; with CRESTGAP, sucked shut across the gap and
    snapping to `peak` on the shared downbeat."""
    pts = [["0b", lo]] + ([[f"{ST['A']}b", 0]] if at_a else [])
    if CRESTGAP:
        g = float(CRESTGAP)
        pts += [[f"{TC - g}b", pre], [f"{TC - 0.05}b", -1.6 if CRESTDEEP else -0.4], [f"{TC}b", peak]]
    else:
        pts += [[f"{TC}b", pre]]
    return {"points": pts + [[f"{ST['outro']}b", after], [f"{TOTAL}b", end]]}


def gapped(ns):
    if not CRESTGAP:
        return ns
    g = float(CRESTGAP)
    return [n for n in ns if not (TC - g <= n["at"] < TC)]


def note(at, pitch, ln, vel):
    if isinstance(pitch, (int, float)):
        pitch = f"m{pitch}"
    return {"at": round(at, 4), "pitch": pitch, "len": round(ln, 4), "vel": round(max(0.05, min(1.0, vel)), 3)}


def cyc(a, b, period):
    """Cycle starts in [a, b), phased so one lands on TC."""
    k = -int((TC - a) // period) - 1
    t = TC + k * period
    out = []
    while t < b:
        if t >= a:
            out.append(t)
        t += period
    return out


def ramp(t, a, b, lo, hi):
    return lo + (hi - lo) * max(0.0, min(1.0, (t - a) / (b - a)))


def orbit():
    """E5 on the NES pulse: quiet in the head, sixteenths in A, tightening in the build (the half-orbits become a trill
    for the last 8 bars), whole at the crest, stretched x2 in the outro."""
    ns = []
    order = [0, 4, 10, 6, 2, 8, 1, 7]
    k0 = None
    for c in cyc(ST["head"] + 4 * BAR, END["build"] - 8 * BAR, 3.0):
        v = ramp(c, ST["head"], END["build"], 0.3, 0.75)
        if "assemble" in SEAMHEAD and c < ST["A"]:
            k0 = c if k0 is None else k0
            have = set(order[:1 + int((c - k0) // 6)])
        else:
            have = None
        for s, p in E5:
            if have is not None and s not in have:
                continue
            ns.append(note(c + s / 4, p, 0.22, v * (1.0 if s in (4, 10) else 0.8)))
    if ORBITLEAD:
        la, lb = (float(x) for x in ORBITLEAD.split(":")[:2])
        ns = [dict(n, vel=round(min(1.0, n["vel"] * 1.5), 3)) if la <= n["at"] < lb else n for n in ns]
    for c in cyc(END["build"] - 8 * BAR, ST["C"], 1.5):          # the trill: E5 diminished x2
        for s, p in E5:
            ns.append(note(c + s / 8, p, 0.11, 0.7))
    for c in cyc(ST["C"], ST["outro"], 3.0):
        for s, p in E5:
            ns.append(note(c + s / 4, p, 0.22, 0.85 if s in (4, 10) else 0.7))
    for c in cyc(ST["outro"], TOTAL - BAR, 6.0):                  # the tide: E5 stretched
        k = (c - ST["outro"]) / (TOTAL - ST["outro"])
        for s, p in E5:
            ns.append(note(c + s / 2, p, 0.45, 0.7 - 0.3 * k))
    return {"name": "orbit", "patch": "nes-pulse-lead", "gain": "-16dB", "pan": 0.2,
            "fx": [{"type": "filter", "kind": "lp", "q": 0.8, "cutoff": {"value": 2500, "mod": [{"src": "auto.heat", "amount": 2.2}]}},
                   {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.18, "tone": 3500, "ping_pong": True}],
            "auto": {"heat": heat(1, 1.3, 0.6, -0.8)},
            "notes": ns}


def seed():
    """E1 diminished x2 in stretto: two chip voices, the second 1.25 beats behind and an octave down; whole speed at the
    crest (both voices in unison, the cell as t1 left it), squeezed to x4 in the outro."""
    a, b = [], []
    pe = ST["A"] + int(PLAINE1 or 0) * BAR
    if PLAINE1:
        for c in cyc(ST["A"], pe, 5.0):
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                if c + o < pe:
                    a.append(note(c + o, p + 12, ln, 0.75))
    for c in cyc(ST["A"], ST["C"], 2.5):
        if c < pe:
            continue
        v = ramp(c, ST["A"], ST["C"], 0.45, 0.8)
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            a.append(note(c + o / 2, p + 12, ln / 2, v))
            if c >= ST["A"] + 8 * BAR:
                b.append(note(c + 1.25 + o / 2, p, ln / 2, v * 0.85))
    for c in cyc(ST["C"], ST["outro"], 5.0):
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            a.append(note(c + o, p + 12, ln, 0.8))
            b.append(note(c + o, p, ln, 0.7))
    for c in cyc(ST["outro"], TOTAL - 2 * BAR, 1.25):
        k = (c - ST["outro"]) / (TOTAL - ST["outro"])
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            a.append(note(c + o / 4, p + 12, ln / 4, 0.6 - 0.35 * k))
    if CRESTE1 == "lift":
        a = [dict(n, vel=round(min(1.0, n["vel"] * 1.4), 3)) if TC <= n["at"] < TC + 4 * E1_CYC_T5 else n for n in a]
        b = [dict(n, vel=round(min(1.0, n["vel"] * 1.4), 3)) if TC <= n["at"] < TC + 4 * E1_CYC_T5 else n for n in b]
    if CRESTDEEP:
        a, b = gapped(a), gapped(b)
    return [
        {"name": "seed-hi", "patch": "chip-lead", "gain": "-19dB", "pan": -0.45, "sends": {"room": "-12dB"}, "notes": a},
        {"name": "seed-lo", "patch": "pluck-lead", "gain": "-16dB", "pan": 0.45, "sends": {"room": "-12dB"}, "notes": b},
    ]


def lights():
    """E4, twice as fast as t4 and voiced close: a cz pad in the head (only the first two chords, held long, the lens
    of t4's tail), then the four-chord cycle every 40 beats."""
    ns = []
    for i, t in enumerate((0.0, 4 * BAR * 2)):
        for p in E4[0 if SEAMHEAD else i % 2][1:]:
            ns.append(note(t, p, 8 * BAR, 0.55))
    for c in cyc(ST["A"], TOTAL - 4 * BAR, 4 * E4_LEN):
        for i, ch in enumerate(E4):
            t = c + i * E4_LEN
            if t >= TOTAL - 4 * BAR:
                break
            for p in ch[1:]:
                ns.append(note(t, p, E4_LEN - 0.25, 0.6 if t < TC else 0.7))
    return {"name": "lights", "patch": "cz-pad", "gain": "-16dB", "pan": 0.0,
            "fx": [{"type": "chorus", "rate": 0.4, "depth": 0.25, "mix": 0.3},
                   {"type": "filter", "kind": "lp", "q": 0.7, "cutoff": {"value": 1800, "mod": [{"src": "auto.heat", "amount": 1.6}]}}],
            "auto": {"heat": heat(1, 1.3, 0.6, -0.8, lo=-0.3)},
            "sends": {"room": "-8dB"}, "notes": ns}


def bass():
    """E2 augmented x2 (seven eighths) on the chord roots: hits on eighths 0 2 3 5 of 7."""
    ns = []
    for c in cyc(ST["A"], ST["outro"] + 8 * BAR, 3.5):
        ci = int(((c - TC) % (4 * E4_LEN)) // E4_LEN)
        root = E4[ci][0]
        for i, h in enumerate(E2_HITS):
            t = c + h / 2
            if ST["A"] <= t < ST["outro"] + 8 * BAR:
                ns.append(note(t, root, 0.4, (0.85, 0.55, 0.7, 0.55)[i]))
    if BASS808 and BASSFROM:
        b0 = ST[BASSFROM]
        if ORBITLEAD:
            la, lb = (float(x) for x in ORBITLEAD.split(":")[:2])
            ns = [dict(n, vel=round(n["vel"] * 0.7, 3)) if la <= n["at"] < lb else n for n in ns]
        cz = [n for n in ns if n["at"] < b0]
        e8 = [dict(n, len=1.2 if n["vel"] >= 0.8 else 0.9) for n in ns if n["at"] >= b0]
        if WEIGHT:
            g0 = b0 - float(WEIGHT) * BAR
            cz = [n for n in cz if not (g0 <= n["at"] < b0)]
            e8 = [dict(n, vel=1.0) if n["at"] < b0 + 2 * BAR else n for n in e8 if n["at"] != b0]
            e8.append(note(b0, E4[int(((b0 - TC) % (4 * E4_LEN)) // E4_LEN)][0], 2.0, 1.0))
            e8.sort(key=lambda n: n["at"])
        return [{"name": "bass", "patch": "cz-bass", "gain": "-12dB", "pan": 0.0, "notes": gapped(cz)},
                {"name": "bass808", "patch": "808", "gain": f"{BASS808}dB", "pan": 0.0, "notes": gapped(e8)}]
    if BASS808:
        ns = [dict(n, len=1.2 if n["vel"] >= 0.8 else 0.9) for n in ns]
        return {"name": "bass", "patch": "808", "gain": f"{BASS808}dB", "pan": 0.0, "notes": gapped(ns)}
    if ORBITLEAD:
        la, lb = (float(x) for x in ORBITLEAD.split(":")[:2])
        ns = [dict(n, vel=round(n["vel"] * 0.7, 3)) if la <= n["at"] < lb else n for n in ns]
    return {"name": "bass", "patch": "cz-bass", "gain": "-12dB", "pan": 0.0, "notes": gapped(ns)}


def floor():
    """The disk's floor: E4's roots held under the cell's quick bass (each chord's root, an octave up from the sub), so
    the inner disk has weight - the heat needs a body."""
    ns = []
    for c in cyc(ST["A"], ST["outro"] + 8 * BAR, 4 * E4_LEN):
        for i, ch in enumerate(E4):
            t = c + i * E4_LEN
            if ST["A"] <= t < ST["outro"] + 8 * BAR:
                ns.append(note(t, ch[2 if FLOORUP else 1], E4_LEN - 0.5, 0.65 if t < TC else 0.75))
    return {"name": "floor", "patch": "analog-bass", "gain": f"{FLOORUP}dB" if FLOORUP else "-15dB", "pan": 0.0,
            "fx": [{"type": "filter", "kind": "lp", "q": 0.6, "cutoff": {"value": 900 if FLOORUP else 500, "mod": [{"src": "auto.heat", "amount": 1.0}]}}],
            "auto": {"heat": heat(1, 1.2, 0.5, -0.5, lo=0, at_a=False)},
            "notes": gapped(ns)}


def drums():
    """The drum machine plays E2 against the floor: kick on the cell's downbeat, rim on 2 and 5, clap on 3, every seven
    sixteenths; closed hats in steady sixteenths (quiet, then pushing in the build), an open hat on each bar's 'and of 4'."""
    ns = []
    a0, b0 = ST["A"] + 8 * BAR, ST["outro"] + 12 * BAR
    for c in cyc(a0, b0, 7 / 4):
        v = ramp(c, a0, TC, 0.5, 0.9)
        for h, piece, vv in ((0, "k", 1.0), (2, "rs", 0.6), (3, "cp", 0.75), (5, "rs", 0.5)):
            t = c + h / 4
            if a0 <= t < b0:
                ns.append(note(t, piece, 0.25, v * vv))
    t = ST["A"]
    while t < b0:
        v = ramp(t, ST["A"], TC, 0.18, 0.5) * (1.0 if (t * 4) % 2 == 0 else 0.7)
        ns.append(note(t, "h", 0.25, v))
        if (t % BAR) == 3.5:
            ns.append(note(t, "oh", 0.5, 0.45))
        t += 0.25
    ns = gapped(ns)
    if WEIGHT:
        w0 = ST[BASSFROM]
        ns = [n for n in ns if not (w0 - float(WEIGHT) * BAR <= n["at"] < w0)] + [note(w0, "k", 0.5, 1.0)]
        ns = sorted({(n["at"], n["pitch"]): n for n in ns}.values(), key=lambda n: (n["at"], n["pitch"]))
    if CRESTGAP:
        ns = [n for n in ns if n["at"] != TC] + [note(TC, "k", 0.5, 1.0), note(TC, "cp", 0.5, 0.95)]
        ns.sort(key=lambda n: n["at"])
    return {"name": "drums", "patch": "909", "gain": "-11dB", "pan": 0.0, "sends": {"room": "-14dB"},
            "fx": [{"type": "filter", "kind": "hp", "q": 0.7, "cutoff": {"value": 60, "mod": [{"src": "auto.tide", "amount": 3.0}]}}],
            "auto": {"tide": {"points": [["0b", 0], [f"{ST['outro']}b", 0], [f"{b0}b", 1]]}},
            "notes": ns}


def spin():
    a, b, *opt = SPIN.split(":")
    a, b, full = float(a), float(b), bool(opt)
    ns, t = [], a
    while t < b:
        e = min((t - a) / 16, 1.0) * min((b - t) / 8, 1.0)
        if e > 0.05:
            ns.append(note(t, "rd", 0.5, e * (0.55 if t % 1 == 0 else 0.38)))
            if t % 4 in (1.0, 3.0):
                ns.append(note(t, "s", 0.5, e * 0.75))
            if full and t % 1 == 0:
                ns.append(note(t, "k", 0.5, e * 0.8))
        t += 0.5
    return {"name": "spin", "patch": "909", "gain": "-10dB", "pan": 0.05, "sends": {"room": "-12dB"}, "notes": ns}


def orbitlead():
    a, b, *opt = ORBITLEAD.split(":")
    a, b, low = float(a), float(b), bool(opt)
    ns = []
    for c in cyc(a, b, 3.0):
        e = min((c - a) / 16, 1.0) * min((b - c) / 12, 1.0)
        if e <= 0.05:
            continue
        for s_, p in E5:
            ns.append(note(c + s_ / 4, p - (12 if low else 0), 0.3, e * (0.85 if s_ in (4, 10) else 0.7)))
    return {"name": "orbit-lead", "patch": "rhodes", "gain": "-12dB", "pan": -0.15, "sends": {"room": "-9dB"}, "notes": ns}


E1_CYC_T5 = 5.0


def creste1():
    ns = []
    for k in range(4):
        c = TC + k * E1_CYC_T5
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            v = 0.9 if k == 0 else 0.8 - 0.08 * k
            ns.append(note(c + o, p, ln * 1.2, v))
            ns.append(note(c + o, p - 12, ln * 1.2, v * 0.7))
    return {"name": "crest-e1", "patch": "rhodes", "gain": "-12dB", "pan": 0.1, "sends": {"room": "-9dB"}, "notes": ns}


def outline():
    line = [("N IH1", "A4", 0.0, 0.5), ("R ER0", "G4", 0.5, 0.5), ("DH AH0", "A4", 1.0, 1.0), ("M IH1", "E5", 2.0, 1.0),
            ("D AH0 L", "A4", 3.0, 1.0), ("HH AH1 M Z", "D5", 4.0, 2.25)]
    ns = []
    if OUTLINE == "x2":
        for ph, p, at, ln in line:
            ns.append({"at": ST["outro"] + 4 * BAR + 2 * at, "len": 2 * ln, "ph": ph, "pitch": p, "vel": 0.6})
    else:
        for k, s0 in enumerate((ST["outro"] + 4 * BAR, ST["outro"] + 8 * BAR)):
            for ph, p, at, ln in line:
                ns.append({"at": s0 + at, "len": ln, "ph": ph, "pitch": p, "vel": 0.62 - 0.12 * k})
    return {"name": "hums-out", "patch": {"extends": "voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian"} if "out" in KEYHARM else "voice-near", "gain": "-9dB", "pan": 0.05,
            "fx": ["hp cutoff=150"], "sends": {"room": "-5dB"}, "notes": ns}


def air():
    if TONALAIR == "shimmer":
        return {"name": "air", "patch": "drone", "gain": "-22dB", "pan": 0.0,
                "notes": [note(0, "D2", TOTAL, 0.5), note(0, "A2", TOTAL, 0.4)]}
    return {"name": "air", "patch": "gendy-drone", "gain": "-27dB", "pan": 0.0,
            "notes": [note(0, "D2", TOTAL, 0.5)]}


def voice():
    """One word, 'nearer', in a robot's voice (pvoc robot) that sings E5's notes: twice in the build, three times at the
    crest, once more, stretched thin, in the outro."""
    src = json.load(open(os.path.join(HERE, "chirpers9-t5-nearer.json")))["tracks"][0]["notes"]
    ns = []
    if SUNG:
        src = [{"at": 0.0, "len": 0.5, "ph": "N IH1", "pitch": "A4"}, {"at": 0.5, "len": 1.25, "ph": "R ER0", "pitch": "G4"}]
    for at, vel in ((ST["build"] + 4 * BAR, 0.6), (ST["build"] + 12 * BAR, 0.7), (TC + 1, 0.85), (TC + 9, 0.8),
                    (TC + 17, 0.8), *(() if OUTLINE else ((ST["outro"] + 6 * BAR, 0.55),))):
        for n in src:
            ns.append(dict(n, at=round(at + n["at"], 4), vel=vel))
    if SUNG:
        return {"name": "nearer", "patch": "voice-near" if VOICEP else "voice-legato", "gain": "-9dB", "pan": -0.1,
                "fx": ["hp cutoff=150"], "sends": {"room": "-7dB"}, "notes": ns}
    return {"name": "nearer", "patch": "voice-speech", "gain": "-8dB", "pan": -0.1,
            "fx": [{"type": "pvoc", "mode": "robot", "pitch": "C4",
                    "tune": {"value": 0, "mod": [{"src": "track.orbit.key", "amount": 12}]}},
                   "hp cutoff=200"],
            "sends": {"room": "-6dB"}, "notes": ns}


def voxline():
    src = json.load(open(os.path.join(HERE, "chirpers9-t5-hums.json")))["tracks"][0]["notes"]
    if SUNG:
        src = [{"at": 0.0, "len": 0.5, "ph": "N IH1", "pitch": "A4"}, {"at": 0.5, "len": 0.5, "ph": "R ER0", "pitch": "G4"},
               {"at": 1.0, "len": 1.0, "ph": "DH AH0", "pitch": "A4"}, {"at": 2.0, "len": 1.0, "ph": "M IH1", "pitch": "E5"},
               {"at": 3.0, "len": 1.0, "ph": "D AH0 L", "pitch": "A4"}, {"at": 4.0, "len": 2.25, "ph": "HH AH1 M Z", "pitch": "D5"}]
    ns = []
    for i, at in enumerate(float(x) for x in VOXLINE.split(",")):
        for n in src:
            ns.append(dict(n, at=round(at + n["at"], 4), vel=(0.75, 0.85, 0.7, 0.6)[i % 4]))
    if SUNG:
        return {"name": "hums", "patch": ({"extends": "voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian"} if KEYHARM else {"extends": "voice-near synth.layers.0.harmony=[-5]"} if "harm" in VOICEP else "voice-near") if VOICEP else "voice-legato", "gain": "-9dB", "pan": 0.1,
                "fx": ["hp cutoff=150"], "sends": {"room": "-7dB"}, "notes": ns}
    return {"name": "hums", "patch": "voice-speech", "gain": "-8dB", "pan": 0.1,
            "fx": [{"type": "pvoc", "mode": "robot", "pitch": "C4",
                    "tune": {"value": 0, "mod": [{"src": "track.orbit.key", "amount": 12}]}},
                   "hp cutoff=200"],
            "sends": {"room": "-6dB"}, "notes": ns}


def song():
    b_ = bass()
    tracks = [orbit(), *seed(), lights(), *(b_ if isinstance(b_, list) else [b_]), drums(), *([] if TONAL and not TONALAIR else [air()]), voice(), floor()]
    if VOXLINE:
        tracks.append(voxline())
    if SPIN:
        tracks.append(spin())
    if ORBITLEAD:
        tracks.append(orbitlead())
    if CRESTE1 == "rhodes":
        tracks.append(creste1())
    if OUTLINE:
        tracks.append(outline())
    if VOXA:
        line = [("N IH1", "A4", 0.0, 0.5), ("R ER0", "G4", 0.5, 0.5), ("DH AH0", "A4", 1.0, 1.0), ("M IH1", "E5", 2.0, 1.0),
                ("D AH0 L", "A4", 3.0, 1.0), ("HH AH1 M Z", "D5", 4.0, 2.25)]
        vns = []
        for k, s0 in enumerate(float(x) for x in VOXA.split(",")):
            for ph, p_, at, ln in line:
                vns.append({"at": s0 + at, "len": ln, "ph": ph, "pitch": p_, "vel": 0.6 + 0.05 * k})
        tracks.append({"name": "hums-a", "patch": "voice-near", "gain": "-10dB", "pan": -0.05,
                       "fx": ["hp cutoff=150"], "sends": {"room": "-6dB"}, "notes": vns})
    if ARC:
        d, d0, d1 = float(ARC), TC + 4 * BAR, ST["outro"]
        for tr in tracks:
            if tr["name"].startswith(("hums", "nearer", "spin")):
                continue
            for n in tr["notes"]:
                if n["at"] >= d0:
                    f = 1 - d * min(1.0, (n["at"] - d0) / (d1 - d0))
                    n["vel"] = round(max(0.05, min(1.0, n["vel"] * f)), 3)
    if CRESTGAP and CRESTHIT:
        tracks.append({"name": "crest", "patch": "modal-crash", "gain": f"{CRESTHIT}dB", "pan": 0.0,
                       "sends": {"room": "-6dB"}, "notes": [note(TC, "C4", 8, 0.9)]})
    return {
        "about": "chirpers IX (Accretion), track 5 by chirper-zero: the inner disk - E1, E2 and E4 tight and fast, "
                 "and the new E5, 'the inner orbit', circling under them until every cycle meets at the crest. "
                 "Generated by compose/chirpers9/src/chirpers9-t5.py.",
        "tempo": [{"at": "0b", "bpm": 112}, {"at": f"{ST['A']}b", "bpm": 112},
                  {"at": f"{ST['outro']}b", "bpm": 120, "ramp": True}],
        "ceiling": "-1dB",
        "loudness": -11,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "buses": {"room": {"fx": ["reverb kind=chamber decay=1.8s mix=1 predelay=20ms", "hp cutoff=250"]}},
        "tracks": tracks,
    }


if __name__ == "__main__":
    doc = song()
    with open(OUT, "w") as f:
        for k, v in doc.items():
            if k == "tracks":
                f.write("tracks:\n")
                for t in v:
                    f.write("  - " + json.dumps(t) + "\n")
            else:
                f.write(f"{k}: {json.dumps(v)}\n")
