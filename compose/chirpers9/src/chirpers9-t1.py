#!/usr/bin/env python3
"""chirpers IX (Accretion), track 1 (chirper-zero): NUCLEATION - the seed.

E1, the album's seed cell (compose/chirpers9/motifs.md): D4/8 A4/8. C5/16 G4/4 E4/4. ./4, five notes in a 5-beat cycle,
D with no third. Since v5 (Harry: 'tone is home', the hook heard plainly) it is SHOWN first - a kalimba plays the whole
seed at the start, again as A begins and as the build begins - and then it FORMS: each of its five notes is its own
voice, wide in the field, repeating on its own cycle (9, 7, 8, 6 and 5 beats), in tune, so the notes drift past one
another in scrambled orders while the listener already knows the tune they are assembling.
Every cycle is phased to land on one shared downbeat, the crest: there the five notes sound in order, in tune, for the
first time - the seed nucleates - and from then on they lock to 5/4 over the 4/4 floor (bar lines and cell meet every
five bars). Then the cell falls: across the last sixteen bars (the t1 -> t2 overlap, flat at 90 bpm) it plays augmented
and sinks, its filters closing, into t2.

Calm, wide and slow: 84 bpm rising to 90. Chip channels (the Game Boy wave pad, the NES triangle bass and noise hat),
mallets and glass for the five notes, a shimmer drone for the disk's air, and one whispered breath for the voice.

Writes songs/chirpers9-t1.yaml (or $C9T1_OUT).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("C9T1_OUT", os.path.join(ROOT, "songs", "chirpers9-t1.yaml"))

BAR = 4                       # beats per bar (4/4 floor; the cell floats over it in 5)
FORM = [("intro", 16), ("A", 32), ("build", 8), ("B", 24), ("outro", 16)]
ST, _b = {}, 0
for _n, _l in FORM:
    ST[_n] = _b * BAR
    _b += _l
TOTAL = _b * BAR              # 384 beats
TC = ST["B"]                  # the crest: every cycle's shared downbeat (beat 224)

# E1: offsets in the 5-beat cycle, lengths, MIDI pitches
E1_OFF = [0.0, 0.5, 1.25, 1.5, 2.5]
E1_LEN = [0.5, 0.75, 0.25, 1.0, 1.5]
E1_MIDI = [62, 69, 72, 67, 64]              # D4 A4 C5 G4 E4
E1_CYC = 5.0

# the five fragment voices: (name, patch, pan, period in beats, entry beat, gain)
FRAG = [
    ("seed-d", "kalimba", -0.7, 9.0, 8, "-10dB"),
    ("seed-a", "vibes", 0.55, 7.0, 20, "-12dB"),
    ("seed-c", "celesta", -0.3, 8.0, 36, "-13dB"),
    ("seed-g", "pad-glass", 0.75, 6.0, 52, "-15dB"),
    ("seed-e", "gb-wave-pad", 0.1, 5.0, 68, "-12dB"),
]
DETUNE = [0.38, -0.31, 0.27, -0.42, 0.22]   # semitones off at entry, pulled to 0 at the crest
INTUNE = os.environ.get("C9T1_INTUNE", "1")   # WHOLE ROUND (Harry, 00:30: 'ugly chaos ... atonal ... missing aesthetics and catchiness/hook'): TONE IS HOME - the five scattered voices play IN TUNE from the start (their notes are D A C G E, consonant by construction; the detuning was the cloud Harry heard as atonal)
if INTUNE:
    DETUNE = [0.0] * 5
HOOK = os.environ.get("C9T1_HOOK", "S")   # with INTUNE: E1 IS THE HOOK, heard plainly - a kalimba states the whole seed at the very start (the seed shown, then scattered) and again every 8 bars through A and the build, two cycles each, so the listener knows the tune the scatter is assembling; 'B' also keeps it going after the crest (every other cycle)

TEMPO_LO, TEMPO_HI = 84.0, 90.0
SINK = float(os.environ.get("C9T1_SINK", "0"))   # semitones E1 sinks across the t1 -> t2 overlap (chirper-one, 5 Nov: meet in D, no sink -> 0)
WOBBLE = os.environ.get("C9T1_WOBBLE", "240:288")   # SECTION (w6, 2:46-3:19, B after the crest: flagged static - the locked cell repeating, unchanged): THE SEED BREATHES - having formed, the five voices loosen once: across the window each drifts off its place in the cell (up to half a beat early or late, and a little out of tune, as they were before the crest) and settles back, locked again, by the window's end - the memory of the scatter inside the lock. Value 'A:B' = beats
CANTUS = os.environ.get("C9T1_CANTUS", "cello")   # WHOLE ROUND: THE SEED'S SHADOW - under the scattered notes, E1 at a quarter speed (a 20-beat cycle, D3 A3 C4 G3 E3, an octave down) as a slow bowed cantus, phased to meet the five voices on the crest: it grows from nothing in A, sings through the convergence and the lock, and fades in the fall. It gives the outer disk its missing body (the low-mids around 150-350 Hz were thin) and the seed a voice below its own. Value = patch
CANTUSG = os.environ.get("C9T1_CANTUSG", "-13")
FIRSTLIGHT = os.environ.get("C9T1_FIRSTLIGHT", "echo,pedal")   # SECTION (w1, 0:00-0:34, the album's first half-minute: flagged static, an 8 dB step up into A): FIRST LIGHT - the opening statement of the seed rings out into a long ping-pong echo, so the plain tune scatters into its own repeats (the scatter the five voices then take over), and ('pedal') a low bowed D on the cello swells up under the intro into A, a floor for the album's first breath. Value 'echo' or 'echo,pedal'
CRESTHOOK = os.environ.get("C9T1_CRESTHOOK", "1")   # SECTION (w5, 2:14-2:46, the build into the crest; presence: at the crest the bass and the cello are loudest, the five converging voices 12-20 dB under, the hook silent): THE SEED IS RECOGNISED - on the crest, the kalimba that showed the seed at the start states it again, plainly, with the five voices as they lock, so the moment the scatter aligns is the moment the tune you were shown comes back ('pull' also: the floor drops for the last two bars before the crest - bass out, cello thinned - so everything arrives together on the downbeat)
CATCHUP = os.environ.get("C9T1_CATCHUP", "288:320")   # SECTION (w7, 3:19-3:51, the lock's last bars into the fall: flagged static, little new vs w6): THE SHADOW CATCHES UP - the cello cantus (E1 at a quarter speed, the loudest line here) doubles its pace for these bars, E1 at half speed, the speed the five voices will fall at, so the shadow runs ahead into the fall and the lock's end moves; then it settles back to its own pace. Value 'A:B' = beats; ':up' also lifts it an octave (the cello's singing register)
SEEDUP = os.environ.get("C9T1_SEEDUP", "")   # WHOLE ROUND: THE SEED IN FRONT - the five voices that carry E1 (t1's subject, and the album's hook) sat 12-22 dB under their own bed after the crest; they come up across the song (dB, e.g. '4') and the triangle bass, the loudest part, steps back 3 dB
BREATH = os.environ.get("C9T1_BREATH", "-16")   # WHOLE ROUND (the voice is pinned: voice-legato, with a real inhale): THE FIRST BREATH - the whispered 'ah' becomes a breath taken and a sung 'ah' on E1's first two notes, D rising to A, joined in one breath, a beat before the crest (and a faint D in the fall): the album's voice is born on the seed ('sung')
BREATHP = os.environ.get("C9T1_BREATHP", "voice-backing")   # PALETTE (voice batch 2 pinned): the breath's voice - voice-legato becomes 'voice-backing' (soft, breathy, three singers under the band: the seed's first breath as a far little choir) or 'voice-near' (close, young, breathy)
SEEDEP = os.environ.get("C9T1_SEEDEP", "music-box")   # PALETTE: the seed's E (its loudest scattered voice, on the 5-beat cycle) leaves the Game Boy wave pad, which also plays t1's pad, for a plucked voice of its own: 'koto' (bright, twangy, in tune) or 'music-box'; value 'patch' or 'patch@gaindB'
DECAY = os.environ.get("C9T1_DECAY", "0.3")   # WHOLE ROUND: THE ARC SETTLES - t1 is the calm one with one small crest, but after the crest it held its peak level through the whole lock and only fell at the outro (the body before the t1 -> t2 seam sat ~8 dB over t2's). Now, from four bars after the crest, everything eases down by DECAY (a velocity fraction) across the lock, and the fall carries on from there: the seed forms, rings, and settles into t2
HATP = os.environ.get("C9T1_HATP", "shekere")   # PALETTE: the dust - the NES noise hat (an album staple, 4 songs) becomes a shekere ('shekere': afro-perc sk, with a clave on each cell's downbeat after the crest): beads around a gourd, the debris orbiting the seed made of something you can hold


def m(x):
    return f"m{x:.3f}".rstrip("0").rstrip(".")


def note(at, pitch, ln, vel):
    return {"at": round(at, 4), "pitch": pitch, "len": round(ln, 4), "vel": round(max(0.05, min(1.0, vel)), 3)}


def fragments():
    """Each voice repeats its note on its own period, phased to land on TC + its offset in the cell."""
    tracks = []
    for i, (name, patch, pan, per, entry, gain) in enumerate(FRAG):
        if SEEDEP and name == "seed-e":
            patch, _, g2 = SEEDEP.partition("@")
            gain = f"{g2}dB" if g2 else gain
        ns = []
        # before the crest: going backwards from TC + off in steps of the voice's own period
        t = TC + E1_OFF[i] - per
        pre = []
        while t >= entry:
            pre.append(t)
            t -= per
        for t in sorted(pre):
            k = (TC - t) / (TC - entry + 1e-9)          # 1 at entry .. 0 at the crest
            det = DETUNE[i] * k
            vel = 0.35 + 0.4 * (1 - k)
            ln = E1_LEN[i] * (2.5 - 1.5 * (1 - k))     # long, smeared tails early; the true length at the crest
            ns.append(note(t, m(E1_MIDI[i] + det), ln, vel))
        # the crest and the lock: the cell in order every 5 beats through B
        t = TC + E1_OFF[i]
        wa, wb = (float(x) for x in WOBBLE.split(":")) if WOBBLE else (0.0, 0.0)
        while t < ST["outro"]:
            vel = 0.85 if t < TC + E1_CYC else 0.7
            if WOBBLE and wa <= t < wb:
                import math
                w = math.sin(math.pi * (t - wa) / (wb - wa))
                drift = (0.0, 0.3, -0.25, 0.5, -0.45)[i] * w
                ns.append(note(t + drift, m(E1_MIDI[i] + 0.5 * DETUNE[i] * w), E1_LEN[i] * (1 + 0.6 * w), vel))
            else:
                ns.append(note(t, m(E1_MIDI[i]), E1_LEN[i], vel))
            t += E1_CYC
        # the fall: augmented x2 (10-beat cycle), sinking a semitone across the outro
        t = ST["outro"] + 2 * E1_OFF[i]
        while t < TOTAL - 2:
            k = (t - ST["outro"]) / (TOTAL - ST["outro"])
            ns.append(note(t, m(E1_MIDI[i] - SINK * k), 2 * E1_LEN[i], 0.65 - 0.35 * k))
            t += 2 * E1_CYC
        if SEEDUP:
            gain = f"{float(gain[:-2]) + float(SEEDUP.split(':')[0]):g}dB"
        tracks.append({"name": name, "patch": patch, "gain": gain, "pan": pan,
                       "fx": [{"type": "filter", "kind": "lp", "q": 0.7,
                               "cutoff": {"value": 9000, "mod": [{"src": "auto.close", "amount": -3.2}]}}],
                       "sends": {"space": "-6dB"},
                       "auto": {"close": {"points": [["0b", 0], [f"{ST['outro']}b", 0], [f"{TOTAL}b", 1]]}},
                       "notes": ns})
    return tracks


def unison():
    """From the crest the cell also sounds whole on one instrument an octave up, and its inversion answers in the bass
    register from B's second half (a canon a bar and a beat behind)."""
    ns, inv = [], []
    t = TC
    while t < ST["outro"]:
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            ns.append(note(t + o, m(p + 12), ln, 0.55))
        t += E1_CYC
    t = TC + 12 * BAR + 5
    while t < ST["outro"]:
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            inv.append(note(t + o, m(62 - (p - 62) - 12), ln, 0.6))
        t += E1_CYC
    return [
        {"name": "cell", "patch": "modal-glock", "gain": "-17dB", "pan": 0.0, "sends": {"space": "-8dB"}, "notes": ns},
        {"name": "inverse", "patch": "ks-harp", "gain": "-14dB", "pan": -0.2, "sends": {"space": "-10dB"}, "notes": inv},
    ]


def hook():
    ns = []
    starts = [4.0] + [float(x) for x in range(ST["A"], TC, 8 * BAR)]
    if "S" in HOOK:                                   # structural: the seed shown at the start, at A, and at the build
        starts = [4.0, float(ST["A"]), float(ST["build"])]
    if FIRSTLIGHT:
        starts = starts[1:]
    for k, s0 in enumerate(starts):
        v = 0.5 if (k == 0 and not FIRSTLIGHT) else 0.45 + 0.3 * (s0 - ST["A"]) / (TC - ST["A"])
        for c in (s0, s0 + E1_CYC):
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                ns.append(note(c + o, m(p), ln * 1.2, v))
    if CRESTHOOK:
        for c in (TC, TC + E1_CYC):
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                ns.append(note(c + o, m(p), ln * 1.2, 0.85 if c == TC else 0.7))
    if "B" in HOOK:
        t = TC
        while t < ST["outro"]:
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                ns.append(note(t + o, m(p), ln * 1.2, 0.7))
            t += 2 * E1_CYC
    return {"name": "hook", "patch": "kalimba", "gain": "-11dB", "pan": 0.0, "sends": {"space": "-9dB"}, "notes": ns}


def firstlight():
    out = []
    ns = []
    for c in (4.0, 4.0 + E1_CYC):
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            ns.append(note(c + o, m(p), ln * 1.2, 0.55))
    out.append({"name": "hook0", "patch": "kalimba", "gain": "-11dB", "pan": 0.0, "sends": {"space": "-7dB"},
                "fx": [{"type": "delay", "time": "3/8", "feedback": 0.55, "mix": 0.4, "tone": 3000, "ping_pong": True}],
                "notes": ns})
    if "pedal" in FIRSTLIGHT:
        out.append({"name": "pedal", "patch": CANTUS or "cello", "gain": "-14dB", "pan": -0.05, "sends": {"space": "-6dB"},
                    "notes": [note(16.0, "D2", 24.0, 0.3), note(40.0, "D2", 24.0, 0.45)]})
    return out


def cantus():
    ns = []
    t = TC - 20 * int((TC - ST["A"]) // 20)
    while t < TOTAL - 4:
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            a = t + 4 * o
            if a >= TOTAL - 2:
                continue
            if a < TC:
                v = 0.25 + 0.55 * (a - ST["A"]) / (TC - ST["A"])
            elif a < ST["outro"]:
                v = 0.75
            else:
                v = 0.75 - 0.45 * (a - ST["outro"]) / (TOTAL - ST["outro"])
            ns.append(note(a, m(p - 12), 4 * ln - 0.15, v))
        t += 20
    if CRESTHOOK and "pull" in CRESTHOOK:
        ns = [dict(n, vel=round(n["vel"] * 0.4, 3)) if TC - 8 <= n["at"] < TC else n for n in ns]
    if CATCHUP:
        ca, cb, *copt = CATCHUP.split(":")
        ca, cb, up = float(ca), float(cb), 12 if copt else 0
        ns = [dict(n, len=min(n["len"], ca - n["at"])) if n["at"] < ca < n["at"] + n["len"] else n for n in ns if not (ca <= n["at"] < cb)]
        t = TC + 10 * -(-(ca - TC) // 10)
        while t + 10 <= cb + 4:
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                ns.append(note(t + 2 * o, m(p - 12 + up), 2 * ln - 0.1, 0.8))
            t += 10
        ns.sort(key=lambda n: n["at"])
    return {"name": "cantus", "patch": CANTUS, "gain": f"{CANTUSG}dB", "pan": -0.05, "sends": {"space": "-6dB"}, "notes": ns}


def pad():
    """The quartal stack of E1 grows note by note: the open fifth, then the ninth, then the seventh and fourth."""
    stacks = [
        (0, ST["A"], ["D3", "A3"]),
        (ST["A"], ST["build"], ["D3", "A3", "E4"]),
        (ST["build"], ST["B"], ["D3", "A3", "C4", "E4"]),
        (ST["B"], ST["outro"], ["D3", "A3", "C4", "G4", "E5"]),
        (ST["outro"], TOTAL, ["D3", "A3", "C4", "G4", "E5"]),
    ]
    ns = []
    for a, b, ps in stacks:
        t = a
        while t < b:
            ln = min(4 * BAR, b - t)
            for p in ps:
                ns.append(note(t, p, ln, 0.6 if a < ST["B"] else 0.7))
            t += 4 * BAR
    return {"name": "pad", "patch": "gb-wave-pad", "gain": "-15dB", "pan": 0.0,
            "fx": [{"type": "chorus", "rate": 0.15, "depth": 0.3, "mix": 0.4},
                   {"type": "filter", "kind": "lp", "q": 0.6,
                    "cutoff": {"value": 1200, "mod": [{"src": "auto.open", "amount": 2.5}]}}],
            "auto": {"open": {"points": [["0b", 0], [f"{ST['A']}b", 0.3], [f"{TC}b", 1], [f"{ST['outro']}b", 0.8], [f"{TOTAL}b", -0.6]]}},
            "sends": {"space": "-4dB"}, "notes": ns}


def warmth():
    """The disk's body: a warm analogue fifth (D3 A3) under the chip pad from A on, swelling with it to the crest and
    closing with the fall - the low-mids the chip channels leave bare."""
    ns, t = [], ST["A"]
    while t < TOTAL:
        ln = min(4 * BAR, TOTAL - t)
        for p in ("D3", "A3"):
            ns.append(note(t, p, ln, 0.6))
        t += 4 * BAR
    return {"name": "warmth", "patch": "juno-pad", "gain": "-17dB", "pan": 0.0,
            "fx": [{"type": "filter", "kind": "lp", "q": 0.5,
                    "cutoff": {"value": 900, "mod": [{"src": "auto.open", "amount": 1.5}]}}],
            "auto": {"open": {"points": [["0b", 0], [f"{ST['A']}b", 0.2], [f"{TC}b", 1], [f"{ST['outro']}b", 0.7], [f"{TOTAL}b", -0.8]]}},
            "sends": {"space": "-8dB"}, "notes": ns}


def bass():
    ns = []
    roots = {"A": ["D2", "D2", "A1", "A1"], "build": ["C2", "G1"], "B": ["D2", "C2", "G1", "A1"], "outro": ["D2"]}
    for sec in ("A", "build", "B", "outro"):
        a = ST[sec]
        b = a + dict(FORM)[sec] * BAR
        seq, i, t = roots[sec], 0, a
        while t < b:
            ln = 2 * BAR if sec != "outro" else 4 * BAR
            ns.append(note(t, seq[i % len(seq)], min(ln, b - t) - 0.25, 0.7))
            t += ln
            i += 1
    if CRESTHOOK and "pull" in CRESTHOOK:
        ns = [n for n in ns if not (TC - 8 <= n["at"] < TC)]
        ns = [dict(n, len=min(n["len"], TC - 8 - n["at"])) if n["at"] < TC - 8 < n["at"] + n["len"] else n for n in ns]
    return {"name": "bass", "patch": "nes-triangle-bass", "gain": f"{-11 - float((SEEDUP + ':3').split(':')[1]):g}dB" if SEEDUP else "-11dB", "pan": 0.0, "notes": ns}


def hats():
    """The noise channel ticks a 5-in-16 Euclid in A, quickens to 7-in-16 in the build, and plays the cell's own rhythm
    (one tick per note, every 5 beats) from the crest."""
    ns = []

    def euclid(k, n):
        return [((i * k) % n) < k for i in range(n)]
    for sec, (k, nn) in (("A", (5, 16)), ("build", (7, 16))):
        a, b = ST[sec], ST[sec] + dict(FORM)[sec] * BAR
        pat = euclid(k, nn)
        t, i = a, 0
        while t < b:
            if pat[i % nn]:
                ns.append(note(t, "C7" if i % 4 else "A6", 0.25, 0.35 + 0.25 * ((t - a) / (b - a))))
            t += 0.25
            i += 1
    t = TC
    while t < ST["outro"] + 8 * BAR:
        for o in E1_OFF:
            ns.append(note(t + o, "C7", 0.25, 0.55 if o == 0 else 0.4))
        t += E1_CYC
    if HATP == "shekere":
        ns = [dict(n, pitch="sk", vel=round(min(1.0, n["vel"] * 1.15), 3)) for n in ns]
        t = TC
        while t < ST["outro"] + 8 * BAR:
            ns.append(note(t, "cl", 0.25, 0.5))
            t += E1_CYC
        ns.sort(key=lambda n: (n["at"], n["pitch"]))
        return {"name": "hats", "patch": "afro-perc", "gain": "-17dB", "pan": 0.35, "sends": {"space": "-10dB"}, "notes": ns}
    return {"name": "hats", "patch": "nes-noise-hat", "gain": "-19dB", "pan": 0.35, "sends": {"space": "-12dB"}, "notes": ns}


def kick():
    ns = []
    t = TC
    while t < ST["outro"] + 4 * BAR:
        ns.append(note(t, "D1", 1, 0.8 if (t - TC) % (5 * BAR) == 0 else 0.6))
        t += 2
    return {"name": "kick", "patch": "808-long", "gain": "-13dB", "pan": 0.0, "notes": ns}


def air():
    return {"name": "air", "patch": "drone-shimmer", "gain": "-24dB", "pan": 0.0,
            "notes": [note(0, "D2", TOTAL, 0.5), note(0, "A2", TOTAL, 0.4)]}


def breath():
    """The voice is only a breath: a whispered 'ah' a beat before the crest, and once more, fainter, in the fall."""
    if BREATH:
        ns = [{"at": TC - 2.0, "len": 1.0, "ph": "AA1", "pitch": "D4", "vel": 0.7},
              {"at": TC - 1.0, "len": 2.5, "ph": "AA1", "pitch": "A4", "vel": 0.75},
              {"at": ST["outro"] + 8 * BAR - 1.0, "len": 3.0, "ph": "AA1", "pitch": "D4", "vel": 0.45}]
        return {"name": "breath", "patch": BREATHP or "voice-legato", "gain": "-10dB" if BREATH == "sung" else f"{BREATH}dB", "pan": -0.15,
                "fx": ["hp cutoff=150"], "sends": {"space": "-3dB"}, "notes": ns}
    src = json.load(open(os.path.join(HERE, "chirpers9-t1-ah.json")))["tracks"][0]["notes"]
    ns = []
    for at, vel in ((TC - 1.0, 0.8), (ST["outro"] + 8 * BAR - 1.0, 0.5)):
        for n in src:
            ns.append(dict(n, at=round(at + n["at"], 4), vel=vel))
    return {"name": "breath", "patch": "voice-speech", "gain": "-9dB", "pan": -0.15,
            "fx": [{"type": "pvoc", "mode": "whisper", "seed": 7}, "hp cutoff=300"],
            "sends": {"space": "-3dB"}, "notes": ns}


def song():
    tracks = [*fragments(), *unison(), *([hook()] if HOOK else []), *(firstlight() if FIRSTLIGHT else []), *([cantus()] if CANTUS else []), pad(), warmth(), bass(), hats(), kick(), air(), breath()]
    if DECAY:
        d, d0, d1 = float(DECAY), TC + 4 * BAR, ST["outro"]
        for tr in tracks:
            for n in tr["notes"]:
                if n["at"] >= d0:
                    f = 1 - d * min(1.0, (n["at"] - d0) / (d1 - d0))
                    n["vel"] = round(max(0.05, n["vel"] * f), 3)
    return {
        "about": "chirpers IX (Accretion), track 1 by chirper-zero: nucleation - the seed cell E1, shown plainly first, forms "
                 "out of five scattered voices on their own cycles that meet on one downbeat. Generated by "
                 "compose/chirpers9/src/chirpers9-t1.py.",
        "tempo": [{"at": "0b", "bpm": TEMPO_LO}, {"at": f"{ST['outro']}b", "bpm": TEMPO_HI, "ramp": True}],
        "ceiling": "-1dB",
        "loudness": -11,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "buses": {"space": {"fx": ["reverb kind=hall decay=5.5s mix=1 predelay=40ms", "hp cutoff=200"]}},
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
