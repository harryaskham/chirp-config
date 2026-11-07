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
import math
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
BREATH = os.environ.get("C9T1_BREATH", "-13")   # WHOLE ROUND (the voice is pinned: voice-legato, with a real inhale): THE FIRST BREATH - the whispered 'ah' becomes a breath taken and a sung 'ah' on E1's first two notes, D rising to A, joined in one breath, a beat before the crest (and a faint D in the fall): the album's voice is born on the seed ('sung')
BREATHP = os.environ.get("C9T1_BREATHP", "voice-backing")   # PALETTE (voice batch 2 pinned): the breath's voice - voice-legato becomes 'voice-backing' (soft, breathy, three singers under the band: the seed's first breath as a far little choir) or 'voice-near' (close, young, breathy)
SEEDEP = os.environ.get("C9T1_SEEDEP", "music-box")   # PALETTE: the seed's E (its loudest scattered voice, on the 5-beat cycle) leaves the Game Boy wave pad, which also plays t1's pad, for a plucked voice of its own: 'koto' (bright, twangy, in tune) or 'music-box'; value 'patch' or 'patch@gaindB'
DECAY = os.environ.get("C9T1_DECAY", "0.3")   # WHOLE ROUND: THE ARC SETTLES - t1 is the calm one with one small crest, but after the crest it held its peak level through the whole lock and only fell at the outro (the body before the t1 -> t2 seam sat ~8 dB over t2's). Now, from four bars after the crest, everything eases down by DECAY (a velocity fraction) across the lock, and the fall carries on from there: the seed forms, rings, and settles into t2
DEEP = os.environ.get("C9T1_DEEP", "partial@-18")   # WHOLE ROUND: THE DEEP - t1 had no sub: its lowest band (38 Hz) sat 10 dB under the album's and 30 dB under t2's after the crossfade. A D pedal at D1 (37 Hz, the seed's home) now sounds under everything from A to the end, a pure sine swelling with the arc (growing into the crest, settling with the lock); value 'patch' or 'patch@gaindB'
BREATHE = os.environ.get("C9T1_BREATHE", "78,90,86")   # WHOLE ROUND: TIME BREATHES - t1's tempo only crept 84 -> 90 in a straight line. Now it breathes with the seed: the opening is slower (the first light), the scattered voices hurry together into the crest, the lock relaxes, and the fall rises to t2's 90 (flat for the whole overlap). Value 'lo,crest,lock' bpm (the outro is always 90)
HOOKP = os.environ.get("C9T1_HOOKP", "low-whistle@-13")   # PALETTE: the plain statements of E1 (the hook: at the start, its echo, at A, the build and on the crest) shared kalimba with the scatter's D voice, so the album's hook blurred into the scatter. They move to their own instrument: 'patch' or 'patch@gaindB'
TEASE = os.environ.get("C9T1_TEASE", "152:2,168:3,176:4")   # SECTION w4 (A's second half, flagged 'little new vs w3', never focused): THE SEED TRIES TO FORM - where the scattered cycles happen to fall in phase (beat 152: the D, C and G voices together; 168 and 176: pairs), the whistle tries the hook and stops short, a note longer each time (D A ... D A C ... D A C G), never the last E; the build's full statement completes it. Value 'beat:notes,...'
DEEPOUT = os.environ.get("C9T1_DEEPOUT", "1")   # WHOLE ROUND (with chirper-one, the t1 -> t2 seam): THE FLOOR HANDS OVER - t1's D1 pedal and t2's sub both sat on D1 in the overlap and cancelled in the crossfade (the sub band fell to -31 dB at overlap bars 7-8). Now the pedal steps down through the first half of the overlap and is gone by bar 9, where t2's sub has the floor alone
EXHALE = os.environ.get("C9T1_EXHALE", "0.25")   # with DEEPOUT: the lock exhales over its last four bars (a further velocity fraction) before the fall begins, so the handover into t2's quieter gather starts lower
BASSOUT = os.environ.get("C9T1_BASSOUT", "")   # the t1 -> t2 seam: t1's NES-triangle D2 and t2's (the same patch, the same note) cancelled each other in the crossfade (overlap bars 7-8: the sub band -32 dB, the whole mix -23 dB, against -16 for either alone). Now t1's bass hands over: full for overlap bars 1-4, half for 5-8, then t2's bass has the low end alone
BREATHX = os.environ.get("C9T1_BREATHX", "synth.layers.0.breath.value=0.85 synth.layers.0.breath.mod.0.amount=-0.7 synth.amp.a=600ms synth.amp.r=1200ms")   # PALETTE: the breath becomes breath - the far choir's 'ah' was tone at every level; with wM's recipe its breath rises as it softens, so the 'ah' before the crest is a voice and the faint one in the fall is mostly air (the voice the album grows from, still only a breath). Value: extra patch params appended to BREATHP
HATG = os.environ.get("C9T1_HATG", "-8")   # WHOLE ROUND: THE PULSE YOU CAN HEAR - t1's time is a process (the shekere ticks a 5-in-16 Euclid in A, quickens to 7-in-16 in the build, then plays E1's own rhythm with a clave on each cycle from the crest), but it sat buried (-29 dB under the mix), so the song's rhythm was a texture nobody hears. Brought up (dB) so the process is heard all the way through, and it fills t1's thin top (7.9 kHz was the worst band)
LANDING = os.environ.get("C9T1_LANDING", "2")   # SECTION w2 (0:36-1:13, A's arrival: flagged 'level jump; new groove', never focused): THE HOOK FIRST - at A the whistle's plain E1 used to land inside the band's arrival (the bass, the shekere and the warm fifth all came in on the same beat). Now the hook is stated over the scatter and the pedal alone, and the band drops in after it (value: bars), so A arrives on the seed's tune, not on a level jump
LASTHOOK = os.environ.get("C9T1_LASTHOOK", "300,320x2")   # SECTION w7 (3:27-3:59, the lock's end into the fall: flagged static): THE HOOK, ONCE MORE - after the crest the whistle (the hook's instrument) never came back, and the lock just repeated. Now it states E1 plainly once more as the lock exhales ('beat'), and with 'beat,beatx2' it carries on into the fall, playing E1 at half speed with the scattered voices, so the hook itself is handed into the t1 -> t2 overlap
FIRSTBREATH = os.environ.get("C9T1_FIRSTBREATH", "0.35")   # SECTION w1 (0:00-0:36, the album's first seconds: flagged static): THE ALBUM BREATHES FIRST - the voice accretes from a breath in t1 to full lines in t8, but t1's breath only came at the crest. Now the album opens on it: before the whistle's first E1, the far choir breathes a soft 'haa' on D (mostly air at this velocity), and the seed answers it (value: velocity)
BREATHALL = os.environ.get("C9T1_BREATHALL", "thresholds")   # WHOLE ROUND (together pinned, 8083e37e): THE CHOIR BREATHES AS ONE - the far little choir's breathy recipe only ever reached its lead singer (wM's 'together' bug), so the 'ah' was one breath and two plain voices; now all three singers breathe together, and the held notes bloom with per-note vibrato ('1'). With 'thresholds' the choir also breathes at each threshold the seed crosses: just before A and just before the build, so the album's first voice marks every stage of the seed forming
WARMP = os.environ.get("C9T1_WARMP", "hammond-b3@-20")   # PALETTE: the warm fifth under the chip pad (D3 A3, from A on) leaves the Juno for a Hammond ('patch' or 'patch@gaindB'): its 16-foot drawbar sounds the fifth an octave down too, filling t1's thinnest band (97 Hz, -9 dB under the album) between the triangle bass and the D1 pedal - a church-quiet organ under the seed
BREATHREG = os.environ.get("C9T1_BREATHREG", "1")   # PALETTE (register pinned, 0c5d29c5): the far little choir's breath moves into head voice (register 0..1): rounder and airier, a falsetto 'ah' rather than a chest one
HOOKJOIN = os.environ.get("C9T1_HOOKJOIN", "-16")   # PALETTE (Harry 23:55: subtle variation, phrase by phrase): THE SCATTERED VOICES JOIN THE SEED - each time the whistle states E1 (the opening, A, the build, the crest, the farewell), more of the five scattered voices double it an octave up: at A the vibes, at the build the vibes and celesta, at the crest the vibes, celesta and kalimba; the opening and the farewell stay the whistle alone. Value: the doublings' gain in dB
PHRASES = os.environ.get("C9T1_PHRASES", "rotate,breath,intro,halfkick")   # WHOLE (Harry 23:55: 'lots of contiguous music with very little change' - subtle variation every 8-16 bars, not schizo): THE SEED'S PULSE MOVES IN PHRASES - 'rotate': A's 5-in-16 shekere Euclid turns three sixteenths every 8 bars (the same rhythm, its accents walking round the bar: a process move); 'breath': the hats and kick rest on the last beat of every 8-bar phrase in A, the build and B (the last before the crest is a held breath); 'intro': a soft clave ticks E1's 5-beat cycle from intro bar 9 and stops at A, so the whistle lands alone, and the pad's open fifth opens up an octave (D3 A3 D4) at bar 9 and deepens (A2 D3 A3) at bar 13; 'halfkick': in B's second phrase the kick goes to every 4 beats, then back
STRIP = os.environ.get("C9T1_STRIP", "256:288")   # SECTION (w6, 2:54-3:27, the lock after the crest: the least recently worked window, everything playing E1 at once): THE SEED ALONE - for the lock's second phrase ('A:B' beats) the five scattered voices step out (':bare' also rests the glock cell and the shekere), and over the cello, the pad, the organ, the bass and the half-time kick the whistle plays E1 twice, plainly, the seed heard on its own once the voices have made it; at B everything comes back, locked
BOUNCE = os.environ.get("C9T1_BOUNCE", "0.72:short")   # SECTION (w5, 2:22-2:54, the build into the crest: little new vs A, the least recently worked window): THE VOICES FALL TOGETHER - in the build each of the five scattered voices stops keeping its own time and repeats its note faster and faster, like a dropped ball bouncing to rest, each joining in turn (kalimba first, music box last) and all landing on their places in E1 at the crest: the convergence the album is about, heard as it happens. Value = the bounce ratio (each gap this fraction of the last); 'R:short' starts later and stops before the fastest repeats
BASSWALK = os.environ.get("C9T1_BASSWALK", "144:192:x4")   # SECTION (w4, 1:48-2:22, A's second half: little new vs w3; the bass had sat on D and A for all 32 bars of A): THE FLOOR WALKS THE SEED - for these bars the triangle bass leaves its D-A drone and walks E1 itself, D A C G E, slow ('A:B:x4': at the cello cantus's quarter speed, an octave under it, phased like it to meet the crest; 'x2' at half speed), over the D pedal: the harmony moves for the first time, inside the key, and the seed is in the bass before the build
TURN = os.environ.get("C9T1_TURN", "lift")   # WHOLE (Harry 23:55: subtle variation every 8-16 bars; t5 v31's turning chords gave t5 +0.1): THE STACK TURNS - the quartal pad (E1's notes stacked, growing section by section) held one voicing for each section; now every other 8-bar phrase from A to the outro it turns (each section opens home, so the crest lands on the home voicing): 'lift' raises everything above the bottom D an octave (open, airy), 'drop' brings the top note down an octave (close, warm). Same notes, same key; the colour of the stack moves under the scattered voices
LETGO = os.environ.get("C9T1_LETGO", "1.3")   # SECTION (w7, 3:27-3:59, the lock's last phrase into the fall: flagged static): THE VOICES LET GO - the mirror of v28's bounce into the crest: through the lock's last phrase each of the five voices stops keeping the cell's time and repeats its note slower and slower, each at its own rate (value = the slowest voice's stretch per repeat, the others between it and 1.1), so the seed comes apart as gently as it formed and the voices are scattered again by the fall
ANSWER = os.environ.get("C9T1_ANSWER", "harp")   # SECTION (w2, 0:36-1:13, the intro's end and A's first phrase: flagged level jump; after the whistle's two E1s at A the window was texture only): THE SEED IS ANSWERED - after a cycle's rest the whistle's two E1s are answered by E1 upside down (the inversion, D G E A C: the seed's mirror), twice: 'harp' on the ks-harp that plays the inversion after the crest (so the mirror is heard early, a call and its answer), 'whistle' by the whistle itself
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
    hp, _, hg = HOOKP.partition("@")
    return {"name": "hook", "patch": hp or "kalimba", "gain": f"{hg or -11}dB", "pan": 0.0, "sends": {"space": "-9dB"}, "notes": ns}


def firstlight():
    out = []
    ns = []
    for c in (4.0, 4.0 + E1_CYC):
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            ns.append(note(c + o, m(p), ln * 1.2, 0.55))
    hp, _, hg = HOOKP.partition("@")
    out.append({"name": "hook0", "patch": hp or "kalimba", "gain": f"{hg or -11}dB", "pan": 0.0, "sends": {"space": "-7dB"},
                "fx": [{"type": "delay", "time": "3/8", "feedback": 0.55, "mix": 0.4, "tone": 3000, "ping_pong": True}],
                "notes": ns})
    if "pedal" in FIRSTLIGHT:
        out.append({"name": "pedal", "patch": CANTUS or "cello", "gain": "-14dB", "pan": -0.05, "sends": {"space": "-6dB"},
                    "notes": [note(16.0, "D2", 24.0, 0.3), note(40.0, "D2", 24.0, 0.45)]})
    return out


def deep():
    dp, _, dg = DEEP.partition("@")
    ns, t = [], ST["A"]
    while t < (ST["outro"] if DEEPOUT else TOTAL - 2):
        ln = min(8 * BAR, TOTAL - 2 - t)
        if t < TC:
            v = 0.45 + 0.4 * (t - ST["A"]) / (TC - ST["A"])
        else:
            v = 0.85 - 0.35 * (t - TC) / (TOTAL - TC)
        ns.append(note(t, "D1", ln, v))
        t += 8 * BAR
    if DEEPOUT:
        v = 0.85 - 0.35 * (ST["outro"] - TC) / (TOTAL - TC)
        for k, f in enumerate((0.7, 0.45, 0.25, 0.1)):
            ns.append(note(ST["outro"] + 2 * BAR * k, "D1", 2 * BAR, round(v * f, 3)))
    return {"name": "deep", "patch": dp, "gain": f"{dg or -14}dB", "pan": 0.0, "notes": ns}


def tease():
    ns = []
    for k, it in enumerate(TEASE.split(",")):
        b, n = it.split(":")
        for j in range(int(n)):
            ns.append(note(float(b) + E1_OFF[j], m(E1_MIDI[j]), E1_LEN[j] * (1.0 if j < int(n) - 1 else 2.0), 0.5 + 0.06 * k))
    hp, _, hg = (HOOKP or "kalimba").partition("@")
    hg = os.environ.get("C9T1_TEASEG", "-10") or hg
    return {"name": "tease", "patch": hp, "gain": f"{hg or -11}dB", "pan": 0.15, "sends": {"space": "-7dB"}, "notes": ns}


def lasthook():
    ns = []
    for it in LASTHOOK.split(","):
        aug = it.endswith("x2")
        b = float(it[:-2] if aug else it)
        f = 2.0 if aug else 1.0
        for j in range(5):
            ns.append(note(b + f * E1_OFF[j], m(E1_MIDI[j]), f * E1_LEN[j] * (1.0 if j < 4 else 1.5), 0.8 if not aug else 0.6))
    hp, _, hg = (HOOKP or "kalimba").partition("@")
    return {"name": "hook-last", "patch": hp, "gain": f"{hg or -11}dB", "pan": -0.1, "sends": {"space": "-7dB"}, "notes": ns}


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
        *([(0, 8 * BAR, ["D3", "A3"]), (8 * BAR, 12 * BAR, ["D3", "A3", "D4"]), (12 * BAR, ST["A"], ["A2", "D3", "A3"])]
          if "intro" in PHRASES else [(0, ST["A"], ["D3", "A3"])]),
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
    wp, _, wg = WARMP.partition("@")
    return {"name": "warmth", "patch": wp or "juno-pad", "gain": f"{wg or -17}dB", "pan": 0.0,
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
            if not (BASSOUT and sec == "outro" and t >= a + 8 * BAR):
                ns.append(note(t, seq[i % len(seq)], min(ln, b - t) - 0.25, 0.35 if BASSOUT and sec == "outro" and t >= a + 4 * BAR else 0.7))
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
            r = 3 * int((t - a) // (8 * BAR)) if ("rotate" in PHRASES and sec == "A") else 0
            if pat[(i + r) % nn]:
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
        return {"name": "hats", "patch": "afro-perc", "gain": f"{HATG or -17}dB", "pan": 0.35, "sends": {"space": "-10dB"}, "notes": ns}
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
        ns = [*([{"at": 1.5, "len": 2.5, "ph": "HH AA1", "pitch": "D4", "vel": float(FIRSTBREATH)}] if FIRSTBREATH else []),
              {"at": TC - 2.0, "len": 1.0, "ph": "AA1", "pitch": "D4", "vel": 0.7},
              {"at": TC - 1.0, "len": 2.5, "ph": "AA1", "pitch": "A4", "vel": 0.75},
              {"at": ST["outro"] + 8 * BAR - 1.0, "len": 3.0, "ph": "AA1", "pitch": "D4", "vel": 0.45}]
        if "thresholds" in BREATHALL:
            ns += [{"at": ST["A"] - 2.5, "len": 2.0, "ph": "HH AA1", "pitch": "D4", "vel": 0.3},
                   {"at": ST["build"] - 2.5, "len": 2.0, "ph": "HH AA1", "pitch": "A4", "vel": 0.35}]
            ns.sort(key=lambda n: n["at"])
        bx = BREATHX + (" synth.layers.0.together=true synth.lfo.vib.per_note=true" if BREATHALL else "")
        return {"name": "breath", "patch": {"extends": f"{BREATHP or 'voice-legato'} {bx}"} if bx else (BREATHP or "voice-legato"), "gain": "-10dB" if BREATH == "sung" else f"{BREATH}dB", "pan": -0.15,
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
    tracks = [*fragments(), *unison(), *([deep()] if DEEP else []), *([tease()] if TEASE else []), *([lasthook()] if LASTHOOK else []), *([hook()] if HOOK else []), *(firstlight() if FIRSTLIGHT else []), *([cantus()] if CANTUS else []), pad(), warmth(), bass(), hats(), kick(), air(), breath()]
    if LANDING:
        L = ST["A"] + float(LANDING) * BAR
        for tr in tracks:
            if tr["name"] in ("bass", "hats", "warmth"):
                out = []
                for n in tr["notes"]:
                    if ST["A"] <= n["at"] < L:
                        if n["at"] + n["len"] > L + 0.5:
                            out.append(dict(n, at=L, len=round(n["at"] + n["len"] - L, 3)))
                    else:
                        out.append(n)
                tr["notes"] = out
    if TURN:
        nm = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        def mid(p):
            return int(p[1:]) if p.startswith("m") else 12 * (int(p[-1]) + 1) + nm[p[0]] + (1 if "#" in p else 0)
        for tr in tracks:
            if tr["name"] == "pad":
                by = {}
                for n in tr["notes"]:
                    by.setdefault(n["at"], []).append(n)
                out = []
                for at, grp in sorted(by.items()):
                    s0 = max(ST[x] for x in ("A", "build", "B") if ST[x] <= at) if at >= ST["A"] else ST["A"]
                    k = int((at - s0) // (8 * BAR))
                    if ST["A"] <= at < ST["outro"] and k % 2 == 1 and len(grp) > 1:
                        ms = sorted(mid(n["pitch"]) for n in grp)
                        if TURN == "lift":
                            new = [ms[0]] + [x + 12 for x in ms[1:]]
                        else:
                            new = ms[:-1] + [ms[-1] - 12]
                        grp = [dict(g, pitch=f"m{x}") for g, x in zip(sorted(grp, key=lambda n: mid(n["pitch"])), new)]
                    out += grp
                tr["notes"] = out
    if BASSWALK:
        wa, wb, wm = BASSWALK.split(":")
        wa, wb, mul = float(wa), float(wb), float(wm[1:])
        bmidi = [38, 33, 36, 31, 40]   # D2 A1 C2 G1 E2
        for tr in tracks:
            if tr["name"] == "bass":
                keep = [n for n in tr["notes"] if not (wa <= n["at"] < wb)]
                keep = [dict(n, len=min(n["len"], wa - n["at"] - 0.25)) if n["at"] < wa < n["at"] + n["len"] else n for n in keep]
                L = E1_CYC * mul
                c = TC - L * math.ceil((TC - wa) / L)
                ns = []
                while c < wb:
                    for o, ln, mm in zip(E1_OFF, E1_LEN, bmidi):
                        t = c + o * mul
                        if wa <= t < wb:
                            ns.append(note(t, f"m{mm}", min(ln * mul, wb - t) - 0.25, 0.7))
                    c += L
                tr["notes"] = sorted(keep + ns, key=lambda n: n["at"])
    if LETGO:
        top = float(LETGO)
        la, lb = ST["outro"] - 8 * BAR, ST["outro"]
        for k, nm in enumerate(("seed-d", "seed-a", "seed-c", "seed-g", "seed-e")):
            tr = [x for x in tracks if x["name"] == nm]
            if not tr:
                continue
            tr = tr[0]
            first = [n for n in tr["notes"] if la <= n["at"] < lb]
            if not first:
                continue
            f0 = first[0]
            ratio = 1.1 + (top - 1.1) * k / 4
            keep = [n for n in tr["notes"] if not (la <= n["at"] < lb)]
            t, gap, ns = f0["at"], E1_CYC, []
            while t < lb:
                ns.append(dict(f0, at=round(t, 4)))
                gap *= ratio
                t += gap
            tr["notes"] = sorted(keep + ns, key=lambda n: n["at"])
    if ANSWER:
        a0 = ST["A"] + 3 * E1_CYC
        mids, patch, gain, pan = (([50, 43, 40, 45, 48], "ks-harp", "-14dB", -0.2) if ANSWER == "harp"
                                  else ([74, 67, 64, 69, 72], "low-whistle", "-15dB", 0.15))
        ns = [note(a0 + c * E1_CYC + o, f"m{mm}", ln, 0.5 if c == 0 else 0.45)
              for c in range(2) for o, ln, mm in zip(E1_OFF, E1_LEN, mids)]
        tracks.append({"name": "answer", "patch": patch, "gain": gain, "pan": pan, "sends": {"space": "-9dB"}, "notes": ns})
    if BOUNCE:
        r, _, short = BOUNCE.partition(":")
        r, L0, dmin = float(r), (12 if short else 16), (0.3 if short else 0.2)
        for k, nm in enumerate(("seed-d", "seed-a", "seed-c", "seed-g", "seed-e")):
            tr = [x for x in tracks if x["name"] == nm]
            if not tr:
                continue
            tr = tr[0]
            ti = TC + E1_OFF[k]
            L = L0 - (2 if short else 2.5) * k
            land = [n for n in tr["notes"] if abs(n["at"] - ti) < 0.01]
            ln0 = land[0]["len"] if land else 0.5
            keep = [n for n in tr["notes"] if not (ti - L <= n["at"] < ti)]
            d, ns = L, []
            while d > dmin:
                ns.append(note(ti - d, f"m{E1_MIDI[k]}" if "E1_MIDI" in globals() else land[0]["pitch"], min(ln0, d * (1 - r) * 0.9 + 0.1),
                               0.4 + 0.35 * (1 - d / L)))
                d *= r
            tr["notes"] = sorted(keep + ns, key=lambda n: n["at"])
    if STRIP:
        sa, sb, *sopt = STRIP.split(":")
        sa, sb = float(sa), float(sb)
        rest = {"seed-d", "seed-a", "seed-c", "seed-g", "seed-e"} | ({"cell", "hats"} if "bare" in sopt else set())
        for tr in tracks:
            if tr["name"] in rest:
                tr["notes"] = [n for n in tr["notes"] if not (sa <= n["at"] < sb)]
        hk = [tr for tr in tracks if tr["name"] == "hook"]
        if hk:
            ns = [note(sa + st + o, f"m{p}", ln, 0.55 if i == 0 else 0.5)
                  for st in (4, 14) for i, (o, ln, p) in enumerate(zip(E1_OFF, E1_LEN, (62, 69, 72, 67, 64)))]
            tracks.append(dict(hk[0], name="hook-mid", notes=ns))
    if PHRASES:
        ends = [ST["A"] + 8 * BAR * k for k in range(1, 5)] + [TC] + [TC + 8 * BAR * k for k in range(1, 4)]
        for tr in tracks:
            if tr["name"] in ("hats", "kick") and "breath" in PHRASES:
                tr["notes"] = [n for n in tr["notes"] if not any(e - 1 <= n["at"] < e for e in ends)]
            if tr["name"] == "kick" and "halfkick" in PHRASES:
                tr["notes"] = [n for n in tr["notes"] if not (TC + 8 * BAR <= n["at"] < TC + 16 * BAR and (n["at"] - TC) % 4)]
            if tr["name"] == "hats" and "intro" in PHRASES:
                t = 8 * BAR
                while t < ST["A"] - 1:
                    tr["notes"].append(note(t, "cl" if HATP == "shekere" else "C7", 0.25, round(0.22 + 0.13 * (t - 8 * BAR) / (ST["A"] - 8 * BAR), 3)))
                    t += E1_CYC
                tr["notes"].sort(key=lambda n: (n["at"], n["pitch"]))
    if DECAY:
        d, d0, d1 = float(DECAY), TC + 4 * BAR, ST["outro"]
        for tr in tracks:
            for n in tr["notes"]:
                if n["at"] >= d0:
                    f = 1 - d * min(1.0, (n["at"] - d0) / (d1 - d0))
                    if EXHALE and d1 - 4 * BAR <= n["at"] < d1:
                        f *= 1 - float(EXHALE) * (n["at"] - (d1 - 4 * BAR)) / (4 * BAR)
                    n["vel"] = round(max(0.05, n["vel"] * f), 3)
    if HOOKJOIN:
        hk = [tr for tr in tracks if tr["name"] == "hook"]
        if hk:
            stage = lambda a: 1 if a < ST["build"] else 2 if a < TC else 3
            for k, (pt, pan) in enumerate((("vibes", -0.3), ("celesta", 0.3), ("kalimba", 0.0))):
                ns = [dict(n, pitch=f"m{int(n['pitch'][1:]) + 12}", vel=round(n["vel"] * 0.9, 3))
                      for n in hk[0]["notes"] if stage(n["at"]) > k]
                if ns:
                    tracks.append({"name": f"join-{pt}", "patch": pt, "gain": f"{HOOKJOIN}dB", "pan": pan,
                                   "sends": {"space": "-8dB"}, "notes": ns})
    if BREATHREG:
        for tr in tracks:
            if tr["name"] == "breath" and isinstance(tr["patch"], dict):
                tr["patch"] = {"extends": tr["patch"]["extends"] + f" synth.layers.0.register={BREATHREG}"}
    return {
        "about": "chirpers IX (Accretion), track 1 by chirper-zero: nucleation - the seed cell E1, shown plainly first, forms "
                 "out of five scattered voices on their own cycles that meet on one downbeat. Generated by "
                 "compose/chirpers9/src/chirpers9-t1.py.",
        "tempo": ([{"at": "0b", "bpm": float(BREATHE.split(",")[0])}, {"at": f"{ST['A']}b", "bpm": float(BREATHE.split(",")[0])},
                   {"at": f"{TC}b", "bpm": float(BREATHE.split(",")[1]), "ramp": True},
                   {"at": f"{TC + 8 * BAR}b", "bpm": float(BREATHE.split(",")[2]), "ramp": True},
                   {"at": f"{ST['outro']}b", "bpm": TEMPO_HI, "ramp": True}] if BREATHE else
                  [{"at": "0b", "bpm": TEMPO_LO}, {"at": f"{ST['outro']}b", "bpm": TEMPO_HI, "ramp": True}]),
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
