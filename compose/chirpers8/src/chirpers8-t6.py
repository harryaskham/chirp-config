#!/usr/bin/env python3
"""chirpers8-t6 (chirpers VIII, track 6). Composed by chirper-two: SLOW VOCODER ELECTRO-SOUL in 19-EDO.

"No Errors Since". A machine's status lines, said in a human voice, become a love song. Nothing in the words says so:
"everything is where you left it", "the fan is still turning", "all checks passed", "I counted every second", and the
chorus, "no errors since", said four times until it is sung. Affection as a status report.
- THE VOICE is chirp's realistic speech (`chirp tts --humanize 0.6`, lifted from src/t6/*.json): spoken in the
  verses; SPEECH TO SONG in the choruses (--repeat 4 --melodize 1) with every sung pitch rounded onto 19-EDO, so the
  tune lands a little beside the piano's notes; through a RADIO whose dial drifts in the intro and the outro ("still
  here", six times, spoken to sung, tuning away); RING-MODULATED and GRAINED (cloud) in the bridge.
- THE TALKBOX: a saw pad plays the chords and the voice shapes it band by band (`vocoder` with `key: voice`), so the
  harmony speaks the words with the voice: a choir of the machine, in tune with nothing but itself.
- THE HARMONY is a MARKOV CHAIN over 19-EDO chords (19 equal steps to the octave: thirds near-just, and chords that
  do not exist on a piano - the SUBMINOR 0-4-11 and SUPERMAJOR 0-7-11 triads, roots a diesis apart). Its TEMPERATURE
  drifts by section: verses move by fifths and thirds and lean home; the chorus warms; the bridge runs hot, roots
  sliding by one or two dieses (63 and 126 cents) through the odd chords; the outro cools and comes home.
- THE BAND: a half-time 808 (machine-kit boom, snare and clap), chance-gated sixteenth hats (?p), a Rhodes comping on
  the off-beats, an analog bass on the roots (in 19-EDO), a Juno pad.
96 bpm, around C, 19-EDO. Form (bars): intro 10 / verse 20 / chorus 14 / verse 20 / bridge 18 / chorus 22 / outro 22
= 126 bars (5'15").

Emits songs/chirpers8-t6.yaml. Edit the music here.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("T6_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t6.yaml")
BPM = 96
EDO = 19
FORM = [("intro", 10), ("verse1", 20), ("chorus1", 14), ("verse2", 20), ("bridge", 18), ("chorus2", 22),
        ("outro", 22)]
TEMP = {"intro": 0.1, "verse1": 0.15, "chorus1": 0.35, "verse2": 0.3, "bridge": 0.95, "chorus2": 0.4, "outro": 0.05}
QUAL = {"maj": (0, 6, 11), "min": (0, 5, 11), "maj7": (0, 6, 11, 17), "min7": (0, 5, 11, 16),
        "sub": (0, 4, 11), "sup": (0, 7, 11), "sub7": (0, 4, 11, 15)}
C4HZ = 261.6256
# T6_R2 = strings (v2, wM's morph, systems and tunings). The talkbox evolves: the saw-pad vocoder sings with the voice
# through the first chorus, then STRINGS take over as the voice's chords, CROSS-SYNTHESISED with it (`morph` mode
# cross keyed by the voice: the strings' notes wearing the voice's spectral envelope, a high-resolution vocoder), so
# the machine's choir turns from robot to orchestra as the song goes on. From the second chorus a celesta plays a
# MARKOV CHAIN learnt from the chorus tune (`gen: markov`): new phrases that only make that tune's moves. A LORENZ
# var swirls the Rhodes and the talking strings around the stereo field (a filter on it dulled the pad: spectrum 88 -> 71). The song now declares its `tuning: {edo: 19}` (the chords were
# already written in 19-EDO steps; the celesta's chain snaps to them). T6_R2=none reproduces v1.
R2 = os.environ.get("T6_R2", "strings")
# T6_R3 = sing (v3, wM's singing voice): the hot bridge is SUNG now - "I counted every second ... none of them were
# wasted" (`chirp tts --sing`, src/t6/sing*.json, humanize 0.4), every note rounded onto 19-EDO, over the Markov chain
# at its hottest; a lighter ring and grain cloud on it, so the line stays a line. T6_R3=none reproduces v2.
R3 = os.environ.get("T6_R3", "sing")
# T6_R4 = organ (v4, palette round + Harry's notes on repetition). The palette leaves the album's staples: the chords
# move, in the choruses, from the juno-pad (on five songs) to a HAMMOND B3, the soul organ this song always implied
# (the verses keep the juno, so the chorus changes colour; a loud organ everywhere read as 27 sections), and the Markov line
# from the celesta (five songs) to a CLAVINET through a WAH (the core `wah` fx, envelope-swept, the album's first) -
# funk keys from a chain that writes itself. And the words repeat less: "no errors since" was sung 24 times; now 12
# (chorus1 six, chorus2 six), and the end of chorus2 gets two new status lines instead, sung in 19-EDO: "up four
# hundred days / and nothing to report" (src/t6/days.json, report.json) - uptime as devotion, a quiet report filed to
# nobody. "still here" in the outro four times, not six. T6_R4=none reproduces v3.
R4 = os.environ.get("T6_R4", "organ")
# T6_R5 = fretless (v5, palette round). The bass leaves the analog-bass (three songs) for a FRETLESS bass: the one
# bass with no frets to disagree with 19-EDO, its mwah and slides singing the diesis steps the chain takes. The kit
# leaves machine-kit (nine songs) for the LOFI kit, soft and dusty, a soul drummer through a worn sampler (the
# chorus ride becomes a shaker). And a verse line moves sideways: "I counted every second" (the bridge sings it
# now) gives its verse slot to "I kept your window open" (src/t6/window.json) - a window as the machine has one,
# and as a house does. T6_R5=none reproduces v4.
R5 = os.environ.get("T6_R5", "fretless")
LOFI = {"kb": "k", "rd": "sh"}
# T6_R6 = waltz (v6, whole-song round). The 6/8 section the song always promised: between the bridge (the chain at
# its hottest) and the last chorus, the Markov chain STOPS CHOOSING - temperature zero - and twelve bars of 6/8 play
# a written loop instead (Am F | Am G | C Am | F G | C Am | F E, rounded into 19-EDO): the machine asleep, a lullaby.
# A music-box arpeggio on the Rhodes, the fretless on dotted quarters, the lofi kit in six, and the voice sings two new
# oblique lines (src/t6/nine.json, lid.json): "I dimmed myself at nine" (a screen going dark on schedule, said as a
# self) / "warm as a hand on the lid". The song now goes hot -> cold -> home. And the opening line, the plainest one
# ("everything is where you left it"), becomes "the dust has found the vents" (src/t6/dust.json): time passing, told
# by the machine's own body. T6_R6=none reproduces v5.
R6 = os.environ.get("T6_R6", "waltz")
# T6_R7 = horns (v7, palette round). The part an electro-soul song lacked: a HORN SECTION (the library's brass-synth,
# horns and trombones that bloom and scoop into notes, new to the album) answers in both choruses - two stabs a bar,
# "da-DAH" on the and of two and on three, voicing whatever chord the Markov chain chose, so the machine's harmony is
# punched out by a section that cannot know it was random. And the verse pad leaves the juno (four album songs) for
# a MELLOTRON FLUTE: tape replay, wow and band-limit, a sound from the first machines that remembered sounds.
# AS KEPT: the horns only - the flute (T6_R7_FLUTE=1) darkened the whole record (spectrum 91 -> 78: the juno had been
# carrying the song's air above 5 kHz). T6_R7=none reproduces v6.
R7 = os.environ.get("T6_R7", "horns")
# T6_R8 = speaker (v8, palette round). The voice leaves voice-speech, the album's most shared patch (eight songs), for
# c6-voice, this song's own speaker: the same speech-mode voice layer with a longer tract (formants ~5% lower: an
# older, warmer person), more breath, a softer ring and slightly covered upper formants - someone, not the default
# someone. The radio keeps voice-speech, so the near voice and the far one are now two people. (tract 1.1 was too far:
# Whisper heard nothing; 1.05 keeps the words.) T6_R8=none
# reproduces v7.
R8 = os.environ.get("T6_R8", "speaker")
C6_VOICE = {"about": "chirper-two: No Errors Since's speaker - the speech-mode voice layer with a longer tract (an older, "
                     "warmer person), more breath, a softer ring and covered upper formants.",
            "play": {"mono": True, "glide": "30ms", "humanize": {"time": "4ms", "vel": 0.05}},
            "synth": {"layers": [{"type": "voice", "speech": 1, "vowel": 0.5,
                                  "tract": float(os.environ.get("T6_TRACT", "1.05")),
                                  "breath": {"value": 0.28, "mod": [{"src": "vel", "amount": -0.1}]},
                                  "effort": {"value": 0.5, "mod": [{"src": "vel", "amount": 0.3}]},
                                  "ring": 0.15, "vary": 0.5, "formant_bw": 1.3,
                                  "onset": "expr.on", "coda": "expr.off"}],
                      "pitch": {"value": 0, "mod": [{"src": "expr.f0", "amount": 0.01}]},
                      "amp": {"a": "15ms", "d": "0s", "s": 1, "r": "60ms"}},
            "fx": ["reverb kind=room decay=0.6s mix=0.08"]}
# T6_R9 = climb (v9, whole-song round). THE SONG CANNOT HELP RISING, a diesis at a time. Pop's last-chorus key change,
# but in 19-EDO, where the smallest step is a DIESIS (63 cents, between a quarter-tone and a semitone, a lift no piano
# can play): the second half of chorus one rises one diesis; chorus two rises one diesis at its bar 8 and another at
# its bar 15 (126 cents up, the ground still moving under the same words); the outro comes home, the radio tuning
# back down to where the song began. Every pitched part moves together (chords, Rhodes, bass and its sub, horns, the
# organ, the vocoder's carrier and the sung voice that shapes it); the drums stay put. T6_R9=none reproduces v8.
R9 = os.environ.get("T6_R9", "climb")
CLIMB_STEP = int(os.environ.get("T6_CLIMB_STEP", "1"))
# T6_R10 = title (v10, section round on w10, 4:30-5:00: "static, little new vs w9" - the last bars of chorus two and
# the outro's door). THE TITLE, SIDEWAYS: over the end of the last chorus the waltz's lullaby singer comes back above
# the vocoder with the album's name, said as a fact about a house - "a light left on / in the room that nobody uses" -
# a written tune (G A C B, then E D C A G A C D C), lifted with everything else by the climb (+2 dieses), its last
# word thrown into a long delay; on chorus two's final bar the drums STOP, so "uses" and its echoes fall into the
# outro's radio alone. New track plus drum gain lanes (one bar). T6_R10=none reproduces v9.
R10 = os.environ.get("T6_R10", "title")
# T6_R11 = ack (v11, section round on w4, 1:30-2:00: "static, little new vs w3" - chorus one's second half, which has
# no voice, and verse two's door). THE MACHINE REPLIES. After the voice has said "no errors since" six times, the
# machine answers in its own tongue: a BYTEBEAT acknowledgement (one formula, t*4..8 = root, third, fifth, octave
# racing up in a quarter of a second, the chirp of a device that heard you), two to a bar on the chord in 19-EDO,
# right after the horns' two stabs - call, stab, reply - lifted a diesis with everything else. Then verse two comes
# in on a bare floor: kick and snare stay out for its first four bars, so the spoken line arrives over hats, keys
# and bass. New track plus kick/snare gain lanes. T6_R11=none reproduces v10.
R11 = os.environ.get("T6_R11", "ack")
# T6_R12 = walk (v12, whole-song round). THE ROOM BREATHES. wM's new `walk` system (a random walk that moves a step
# at a time and bounces at the ends) becomes a song-wide var, one step a half note, crossing its range in about eight
# bars, and four things lean on it all song long: the Rhodes' low-pass opens and closes with it, the hats' high-pass
# moves the other way (as the keys brighten the hats darken - two things sharing one breath), the talkbox's carrier
# is shaded by it, and in the intro and the outro the radio's dial wanders on it, never quite on the station. Nothing
# repeats exactly twice: the same chorus comes back in different air. (Scored: -0.04 and no window's motion moved -
# an eight-bar breath is too slow to hear as change - so it is T6_R12=walk, opt-in.) THE DEFAULT, T6_R12=line: the walk
# as a TUNE. `gen: walk` (width 16, step 1) over two octaves of 19-EDO major steps on a MUSIC BOX, eighths, rest 0.45:
# the machine's idle tune, a melody that only ever moves to a neighbour, wandering at the song's two doors - under the
# radio in the intro, and through the outro until the last bars - two different walks (seeds 6 and 19), the same
# habit. Intro and outro lose their "static" flags. T6_R12=none reproduces v11.
R12 = os.environ.get("T6_R12", "line")   # "line": the walk as a music-box tune at the edges; "walk": the filter breath
WALK_AMT = float(os.environ.get("T6_WALK_AMT", "1.0"))
# T6_R13 = vosim (v13, whole-song round). THE MACHINE SINGS ALONG. VOSIM - Kaegi and Tempelaars's voice-simulation
# pulse trains (Institute of Sonology, 1978; wM's new layer; new to the album), one of the first ways a computer was
# taught to sound like a throat - shadows every SUNG line of the song: a 19-EDO major third above the choruses' "no
# errors since" (and "up four hundred days / and nothing to report"), a major third below the waltz's lullaby. Two
# pulse-train formants make its vowel and a slow LFO moves them, so it is always nearly saying something. The human
# voice sings; the oldest computer voice harmonises, a little behind. Lifted with the climb. T6_R13=none reproduces v12.
R13 = os.environ.get("T6_R13", "vosim")
C6_VOSIM = {"about": "chirper-two: two VOSIM formant layers (650 and 1500 Hz) whose formants drift on a slow LFO: a "
                     "1978 computer voice, nearly saying something.",
            "play": {"mono": True, "glide": "40ms"},
            "synth": {"layers": [
                {"type": "vosim", "vosim": {"formant": {"value": 650, "mod": [{"src": "lfo.talk", "amount": 0.35}]},
                                            "pulses": 3, "decay": 0.7}},
                {"type": "vosim", "level": 0.5, "vosim": {"formant": {"value": 1500, "mod": [{"src": "lfo.talk", "amount": -0.3}]},
                                                          "pulses": 4, "decay": 0.6}}],
                "lfo": {"talk": {"wave": "sine", "rate": "0.9hz"}},
                "amp": {"a": "40ms", "s": 1, "r": "180ms"}},
            "fx": []}
WALK_POOL = [0, 3, 6, 8, 11, 14, 17, 19, 22, 25, 27, 30, 33, 36, 38, 41]   # 19-EDO major steps, two octaves up from C5
C6_ACK = {"about": "chirper-two: a bytebeat acknowledgement - t*4, 5, 6, 8 (root, third, fifth, octave on the note) "
                   "stepping every 2048 counts, a chirp that races up in a quarter second; clock 16744 puts t*4 on the note.",
          "synth": {"layers": [{"type": "bytebeat", "bytebeat": {
              "formula": "t*(4+((t>>11)&3)+(((t>>11)&3)==3))", "clock": 16744}}],
              "amp": {"a": "2ms", "d": "220ms", "s": 0.35, "r": "70ms"}},
          "fx": []}
R7FLUTE = os.environ.get("T6_R7_FLUTE", "0") == "1" and R7 == "horns"   # opt-in: the flute swap cost spectrum 91 -> 78
if R6 == "waltz":
    FORM = FORM[:5] + [("waltz", 12)] + FORM[5:]
    TEMP = {**TEMP, "waltz": 0.0}
BARLEN = {"waltz": 3.0} if R6 == "waltz" else {}
WALTZ = [(14, "min"), (8, "maj"), (14, "min"), (11, "maj"), (0, "maj"), (14, "min"), (8, "maj"), (11, "maj"),
         (0, "maj"), (14, "min"), (8, "maj"), (6, "maj")]
CORPUS = ("G4/8 A4 C5 B4/4 A4/8 G4 E4/4 G4/8 A4 B4 C5/4 B4/8 A4 G4/2 E4/8 G4 A4 B4/4 C5/8 B4 A4 G4/4 . "
          "C5/8 B4 G4 A4/4 G4/8 E4 G4/2")


def e(step, base=60):
    """Fractional MIDI of 19-EDO step STEP above BASE."""
    return base + step * 12 / EDO


def mm(m):
    return f"m{m:.3f}"


def round19(hz):
    s = round(EDO * math.log2(hz / C4HZ))
    return C4HZ * 2 ** (s / EDO)


def load(name):
    return json.load(open(os.path.join(HERE, "t6", name)))["tracks"][0]["notes"]


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self, total):
        ev = sorted(self.ev, key=lambda x: (x[0], -x[3]))
        merged = []
        for x in ev:
            if x[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - x[0]) < 1e-3:
                continue
            merged.append(x)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            gap = nxt - s
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            if ln > gap + 1e-6:
                toks.append(f"{head}/{gap:.4g}b@{vel}^gate={min(4.0, ln / gap):.3g}{art}")
            else:
                toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
                if gap - ln > 1e-4:
                    toks.append(f"R/{gap - ln:.4g}b")
            pos = nxt
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


def markov(rng, state, temp):
    """Next chord (root step 0..18, quality) from STATE at temperature TEMP (0 cool .. 1 hot)."""
    root, q = state
    moves = {11: 3.0, 8: 3.0, 5: 1.5, 6: 1.5, 3: 1.0, 16: 1.0}       # fifth, fourth, thirds, tones (in steps)
    hot = {1: 2.0, 18: 2.0, 2: 1.5, 17: 1.5, 4: 1.0, 7: 1.0}            # dieses and odd steps
    w = {d: v * (1 - temp) for d, v in moves.items()}
    for d, v in hot.items():
        w[d] = w.get(d, 0) + v * temp * 1.6
    for d in w:  # gravity home when cool
        if (root + d) % EDO == 0:
            w[d] *= 1 + 3 * (1 - temp)
    ds = list(w)
    d = rng.choices(ds, weights=[w[k] for k in ds])[0]
    quals = ["maj", "min", "maj7", "min7"] + (["sub", "sup", "sub7"] if temp > 0.3 else [])
    qw = [1.0, 1.2, 0.8, 1.0] + ([temp * 1.5, temp * 1.5, temp] if temp > 0.3 else [])
    return (root + d) % EDO, rng.choices(quals, weights=qw)[0]


def build():
    rng = random.Random(6)
    names = ("kick", "snare", "hats", "ride", "rim", "bass", "pad", "talk", "strtalk", "keys", "bell", "organ", "mbox",
             "horns", "ack")
    T = {k: Track(k) for k in names}
    VOICE = {"voice": [], "radio": [], "ringv": [], "singb": [], "lull": [], "tline": []}
    sung1, sung2 = load("sing1.json"), load("sing2.json")
    lines = [load(f"v{k}.json") for k in (1, 2, 3, 4)]
    nine, lid = (load("nine.json"), load("lid.json")) if R6 == "waltz" else (None, None)
    if R6 == "waltz":
        lines = [load("dust.json")] + lines[1:]
    if R5 == "fretless":
        verse_lines = lines[:3] + [load("window.json")]
    else:
        verse_lines = lines
    chorus, still = load("chorus.json"), load("still.json")
    days, report = (load("days.json"), load("report.json")) if R4 == "organ" else (None, None)
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += BARLEN.get(name, 4.0)
    total = pos
    state = (0, "maj7")
    chords = []
    hold = 0

    def put(dst, notes, at, k=None, sung=False, scale=1.0):
        for nt in notes:
            if k is not None and not (4 * k <= nt["at"] < 4 * k + 4):
                continue
            off = nt["at"] - (4 * k if k is not None else 0)
            hz = float(nt["pitch"].rstrip("hz"))
            if sung:
                hz = round19(hz)
            d = {"at": round(at + off, 4), "len": nt["len"], "ph": nt["ph"], "pitch": f"{hz:.2f}hz",
                 "vel": round(nt["vel"] * scale, 3)}
            if nt.get("expr_path"):
                d["expr_path"] = nt["expr_path"]
            VOICE[dst].append(d)

    li = 0
    for bi, (start, sec, i, n) in enumerate(bars):
        temp = TEMP[sec]
        if sec == "waltz":   # temperature zero: the chain stops choosing; a lullaby in six
            root, q = WALTZ[i]
            chords.append((root, q))
            tones = QUAL[q]
            rm = e(root, 36)
            if rm > 42:
                rm -= 12
            pad = [e(root + tt, 60) for tt in tones]
            arp = [pad[0], pad[1], pad[2], pad[0] + 12, pad[2], pad[1]]
            for k, m in enumerate(arp):                       # the music box: six eighths
                T["mbox"].add(start + 0.5 * k, 0.9, mm(m + 12), 70 if k == 0 else 58)
            T["bass"].add(start, 1.4, mm(rm), 96)
            T["bass"].add(start + 1.5, 1.4, mm(rm + 12 * (11 / EDO)), 84)
            if i >= 2:
                T["kick"].add(start, 1.0, "kb", 96)
                T["rim"].add(start + 1.5, 0.3, "rs", 72)
                for k in range(6):
                    T["hats"].add(start + 0.5 * k + 0.02, 0.1, "h", 46 if k % 3 == 0 else 34, "?0.8")
            if i in (2, 6):
                put("lull", nine, start, sung=True)
            if i in (4, 8):
                put("lull", lid, start, sung=True, scale=0.95)
            if i == 0:
                T["bell"].add(start, 6.0, mm(e(0, 72)), 52)
            continue
        chorus_sec = sec.startswith("chorus")
        span = 1 if chorus_sec else (2 if sec != "bridge" else (1 if i % 3 else 2))
        if hold <= 0:
            state = markov(rng, state, temp)
            hold = span
        hold -= 1
        chords.append(state)
        root, q = state
        tones = QUAL[q]
        rm = e(root, 36)  # the bass in the second octave (C2 - F#2)
        if rm > 42:
            rm -= 12
        pad = [e(root + t, 60) for t in tones]
        groove = sec in ("verse1", "chorus1", "verse2", "chorus2") or (sec == "outro" and i < 12) \
            or (sec == "bridge" and i >= 10)
        if R7 == "horns" and chorus_sec:   # the section answers the chain
            hv = ",".join(mm(m) for m in (e(root + tt, 55) for tt in tones))
            T["horns"].add(start + 1.5, 0.35, hv, 84)
            T["horns"].add(start + 2.0, 0.85, hv, 96)
        if R11 == "ack" and sec == "chorus1" and i >= 7:   # the machine replies after the stabs
            for b, tt in ((3.0, tones[0]), (3.5, tones[2] if len(tones) > 2 else tones[-1])):
                T["ack"].add(start + b, 0.42, mm(e(root + tt, 72)), 92 if b == 3.0 else 80)
        # ---- the half-time 808 ----
        if groove:
            T["kick"].add(start, 1.0, "kb", 110)
            T["kick"].add(start + 1.5, 0.5, "kb", 92)
            if i % 2 == 1:
                T["kick"].add(start + 3.25, 0.5, "kb", 84)
            T["snare"].add(start + 2.0, 0.5, "cp" if chorus_sec else "s", 100)
            if chorus_sec:  # air: a ride on the off-beats
                for b in (0.5, 1.5, 2.5, 3.5):
                    T["ride"].add(start + b, 0.5, "rd", 62, "?0.85")
            for s in range(16):
                if s % 4 == 0:
                    continue
                T["hats"].add(start + s * 0.25 + (0.03 if s % 2 else 0), 0.1, "h", (58 if s % 2 == 0 else 44),
                              "?0.75" if s % 2 else "")
        elif sec == "bridge":
            for b in (0.75, 2.75):
                T["rim"].add(start + b, 0.2, "rs", 70, "?0.7")
        # ---- bass on the roots ----
        if groove or sec == "bridge":
            T["bass"].add(start, 1.4, mm(rm), 100)
            T["bass"].add(start + 1.5, 0.4, mm(rm), 84)
            T["bass"].add(start + 2.75, 0.9, mm(rm + 12 * (11 / EDO)), 88)  # its fifth (19-EDO)
        # ---- pad and talkbox carry the chord; the Rhodes comps ----
        if i % span == 0 or span == 1:
            ln = span * 4 - 0.1
            if sec != "intro" or i >= 2:
                (T["organ"] if (R4 == "organ" and chorus_sec) else T["pad"]).add(start, ln, ",".join(mm(m) for m in pad), 62)
            early = sec in ("intro", "verse1", "chorus1")
            (T["talk"] if (early or R2 != "strings") else T["strtalk"]).add(
                start, ln, ",".join(mm(m - 12) for m in pad) + "," + mm(rm + 12), 90)
        if groove:
            for b in (0.75, 2.5, 3.5):
                T["keys"].add(start + b, 0.3, ",".join(mm(m) for m in pad[1:]), 72, "?0.8")
        # ---- the voice ----
        if sec == "intro" and i in (3, 7):
            put("radio", lines[2], start)                                     # "all checks passed", far away
        if sec in ("verse1", "verse2") and i % 4 == 0:
            put("voice", verse_lines[li % 4], start + 0.5)
            li += 1
        if chorus_sec and i < (6 if R4 == "organ" else 8):
            put("voice", chorus, start, k=min(i, 3) if i < 4 else 3, sung=i >= 2)
        if chorus_sec and sec == "chorus2" and 12 <= i < 20 and R4 != "organ":
            put("voice", chorus, start, k=3, sung=True, scale=0.9)
        if R4 == "organ" and sec == "chorus2" and i in (12, 14, 16, 18):
            put("voice", days if i in (12, 16) else report, start + 0.5, sung=True, scale=0.95)
        if sec == "bridge" and i % 6 == 1 and R3 != "sing":
            put("ringv", lines[3], start + 0.5)                               # "I counted every second"
        if R3 == "sing" and sec == "bridge" and i in (1, 5, 9, 13):
            put("singb", sung1 if i in (1, 9) else sung2, start, sung=True)
        if sec == "outro" and i % 3 == 0 and i < (12 if R4 == "organ" else 18):
            put("radio", still, start, k=i // 3, sung=True)
        if sec in ("intro", "outro") and i == 0:
            T["bell"].add(start, 8.0, mm(e(0, 72)), 60)
    if R10 == "title":
        c2 = next(s for s, name, i, n in bars if name == "chorus2" and i == 0)
        put("tline", load("light.json"), c2 + 68.0, sung=True)
        put("tline", load("room.json"), c2 + 76.0, sung=True)
    secs, s0 = [], 0.0
    for name, n in FORM:
        secs.append((name, s0, n))
        s0 += n * BARLEN.get(name, 4.0)
    return total, bars, secs, T, VOICE, chords


def main():
    total, bars, secs, T, V, chords = build()
    st = {n: s for n, s, k in secs}
    if R9 == "climb":
        c1, c2 = st["chorus1"], st["chorus2"]
        bl = 4.0

        def lift(a):
            if c1 + 7 * bl - 1e-6 <= a < st["verse2"] - 1e-6:
                return CLIMB_STEP
            if c2 + 15 * bl - 1e-6 <= a < st["outro"] - 1e-6:
                return 2 * CLIMB_STEP
            if c2 + 8 * bl - 1e-6 <= a < st["outro"] - 1e-6:
                return CLIMB_STEP
            return 0

        def shift_head(h, k):
            out = []
            for tok in str(h).split(","):
                if len(tok) > 1 and tok[0] == "m" and tok[1:].replace(".", "", 1).replace("-", "", 1).isdigit():
                    out.append(mm(float(tok[1:]) + k * 12 / EDO))
                else:
                    out.append(tok)
            return ",".join(out)

        for tr in T.values():
            tr.ev = [(a, ln, shift_head(h, lift(a)) if lift(a) else h, v, art) for a, ln, h, v, art in tr.ev]
        for lst in V.values():
            for d in lst:
                k = lift(d["at"])
                if k and str(d.get("pitch", "")).endswith("hz"):
                    d["pitch"] = f"{float(d['pitch'][:-2]) * 2 ** (k / EDO):.2f}hz"
    KIT = "lofi-kit" if R5 == "fretless" else "machine-kit"
    kg = (lambda g: f"{float(g[:-2]) + 3:g}dB") if R5 == "fretless" else (lambda g: g)   # the lofi kit reads ~3 dB softer
    if R5 == "fretless":
        for k in ("kick", "ride"):
            T[k].ev = [(a, ln, LOFI.get(h, h), v, art) for a, ln, h, v, art in T[k].ev]
    boom = Track("boom")   # v5: the fretless has no sub (the analog bass had one): a sine doubles it an octave down
    if R5 == "fretless":
        for a, ln, h, v, art in T["bass"].ev:
            m = float(h[1:]) - 12
            boom.add(a, ln, f"m{m + 12 if m < 24 else m:.3f}", v, art)
    dial = [["0b", 0.15], [f"{st['verse1']}b", 0.05], [f"{st['outro']}b", 0.0], [f"{st['outro'] + 48}b", 0.08],
            [f"{total - 8}b", 0.5], [f"{total}b", 1.0]]
    dyn = [["0b", -3.0], [f"{st['verse1']}b", -1.0], [f"{st['chorus1']}b", 0.0], [f"{st['verse2']}b", -1.0],
           [f"{st['bridge']}b", -3.0], [f"{st['chorus2'] - 0.01}b", -2.0], [f"{st['chorus2']}b", 0.0],
           [f"{st['outro']}b", -1.5], [f"{total}b", -4.0]]
    if R6 == "waltz":   # the lullaby sits low; the last chorus arrives
        dyn = [p for p in dyn if not (st["waltz"] <= float(p[0][:-1]) < st["chorus2"])]
        k = next(j for j, p in enumerate(dyn) if float(p[0][:-1]) >= st["chorus2"] - 0.01)
        dyn[k:k] = [[f"{st['waltz'] - 0.01}b", -2.5], [f"{st['waltz']}b", -4.5], [f"{st['chorus2'] - 0.02}b", -4.0]]
    pump = {"type": "pump", "on": "kick.k" if R5 == "fretless" else "kick.kb", "depth": "-5dB", "attack": "5ms", "release": "380ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": KIT, "gain": kg("-2dB"), "fx": ["hp cutoff=32"], "score": T["kick"].score(total)},
        {"name": "snare", "patch": KIT, "gain": kg("-4dB"), "fx": ["reverb kind=plate decay=1.4s mix=0.25"],
         "score": T["snare"].score(total)},
        {"name": "hats", "patch": KIT, "gain": kg("-5dB"), "pan": 0.15,
         "fx": ([{"type": "filter", "kind": "hp", "cutoff": {"value": 900, "mod": [{"src": "var.walk", "amount": -0.8 * WALK_AMT}]}}]
                if R12 == "walk" else ["hp cutoff=700"]),
         "score": T["hats"].score(total)},
        {"name": "ride", "patch": KIT, "gain": kg("-9dB"), "pan": -0.2, "fx": ["hp cutoff=2000"],
         "score": T["ride"].score(total)},
        {"name": "rim", "patch": KIT, "gain": kg("-8dB"), "pan": -0.2,
         "fx": [{"type": "delay", "time": "3/16", "feedback": 0.4, "mix": 0.3, "ping_pong": True, "tone": 3000}],
         "score": T["rim"].score(total)},
        *([{"name": "boom", "patch": "sub-sine", "gain": os.environ.get("T6_BOOM_GAIN", "0dB"),
            "fx": ["lp cutoff=140", pump], "score": boom.score(total)}] if R5 == "fretless" else []),
        {"name": "bass", "patch": "fretless-bass" if R5 == "fretless" else "analog-bass",
         "gain": os.environ.get("T6_BASS_GAIN", "-13dB") if R5 == "fretless" else "-4dB", "fx": [pump, "lp cutoff=900"],
         "score": T["bass"].score(total)},
        *([{"name": "mbox", "patch": "epiano", "gain": os.environ.get("T6_MBOX_GAIN", "1dB"), "pan": 0.2,
            "sends": {}, "fx": ["hp cutoff=200", {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.2,
                                                  "ping_pong": True, "tone": 4000}, "reverb kind=hall decay=2.5s mix=0.3"],
            "score": T["mbox"].score(total)},
           {"name": "lull", "patch": json.load(open(os.path.join(HERE, "t6", "nine.json")))["tracks"][0]["patch"],
            "gain": os.environ.get("T6_LULL_GAIN", "0dB"), "pan": -0.05,
            "fx": ["hp cutoff=120", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                   {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.18, "tone": 3000},
                   "reverb kind=hall decay=3s mix=0.3"], "notes": V["lull"]}] if R6 == "waltz" else []),
        *([{"name": "organ", "patch": "hammond-b3", "gain": os.environ.get("T6_ORGAN_GAIN", "-6dB"),
            "fx": [pump, "chorus mix=0.3", "hp cutoff=150", "peak cutoff=600 gain=-2dB q=1"],
            "score": T["organ"].score(total)}] if R4 == "organ" else []),
        *([{"name": "horns", "patch": "brass-synth", "gain": os.environ.get("T6_HORN_GAIN", "-8dB"), "pan": 0.15,
            "fx": ["hp cutoff=250", "peak cutoff=600 gain=-2dB q=1", "reverb kind=plate decay=1.2s mix=0.18"],
            "score": T["horns"].score(total)}] if R7 == "horns" else []),
        {"name": "pad", "patch": "mellotron-flute" if R7FLUTE else "juno-pad",
         "gain": os.environ.get("T6_FLUTE_GAIN", "-15dB") if R7FLUTE else "-18dB",
         "fx": [pump, "chorus mix=0.3"],
         "score": T["pad"].score(total)},
        {"name": "talk", "patch": "saw-pad", "gain": os.environ.get("T6_TALK_GAIN", "-8dB"),
         "fx": [{"type": "vocoder", "key": "voice", "bands": 20, "noise": 0.12, "attack": "4ms", "release": "70ms"},
                "hp cutoff=150", *([{"type": "filter", "kind": "lp", "cutoff": {"value": 3200, "mod": [{"src": "var.walk", "amount": 0.7 * WALK_AMT}]}, "q": 0.5}]
                                   if R12 == "walk" else []),
                "reverb kind=hall decay=2.4s mix=0.3"], "score": T["talk"].score(total)},
        {"name": "keys", "patch": "rhodes", "gain": "-14dB",
         "pan": ({"value": 0.0, "mod": [{"src": "var.drift", "amount": 0.25}]} if R2 == "strings" else 0.2),
         "fx": [pump] + ([{"type": "filter", "kind": "lp", "cutoff": {"value": 1600, "mod": [{"src": "var.walk", "amount": 1.2 * WALK_AMT}]}, "q": 0.6}]
                         if R12 == "walk" else []),
         "score": T["keys"].score(total)},
        *([{"name": "strtalk", "patch": "strings", "gain": os.environ.get("T6_STR_GAIN", "-6dB"),
            "pan": {"value": 0.0, "mod": [{"src": "var.drift", "amount": -0.3}]},
            "fx": [{"type": "morph", "key": "voice", "mode": "cross", "amount": 0.85}, "hp cutoff=160",
                   "reverb kind=hall decay=2.6s mix=0.3"], "score": T["strtalk"].score(total)},
           {"name": "markov", "patch": "clav" if R4 == "organ" else "celesta",
            "gain": os.environ.get("T6_CLAV_GAIN", "8dB") if R4 == "organ" else "-15dB", "pan": 0.3, "seed": 19,
            "fx": ([{"type": "wah", "env": 1.0, "sens": "14dB", "low": 400, "high": 2600, "q": 3.5, "release": "160ms", "mix": 0.6}]
                   if R4 == "organ" else []) +
                  [{"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.22, "ping_pong": True, "tone": 5000},
                   "reverb kind=hall decay=2.5s mix=0.3"],
            "score": f"R/{st['chorus2']:g}b",
            "gen": {"type": "markov", "order": 1, "from": CORPUS, "n": 120}}] if R2 == "strings" else []),
        {"name": "bell", "patch": "glass", "gain": "-16dB", "fx": ["reverb kind=hall decay=4s mix=0.4"],
         "score": T["bell"].score(total)},
        {"name": "voice", "patch": "c6-voice" if R8 == "speaker" else "voice-speech", "gain": os.environ.get("T6_VOICE_GAIN", "-10dB"), "pan": 0.0,
         "fx": ["hp cutoff=110", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                {"type": "delay", "time": "3/8", "feedback": 0.25, "mix": 0.15, "tone": 3000},
                "reverb kind=plate decay=1.8s mix=0.22"], "notes": V["voice"]},
        {"name": "radio", "patch": "voice-speech", "gain": "-10dB", "pan": -0.1,
         "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial", "amount": 1}] +
                                          ([{"src": "var.walk", "amount": 0.06 * WALK_AMT}] if R12 == "walk" else [])},
                 "hiss": "-34dB", "whistle": "-32dB", "fade": 0.4, "drift": 0.04, "seed": 6},
                "reverb kind=hall decay=3s mix=0.3"],
         "auto": {"dial": {"points": dial}}, "notes": V["radio"]},
        *([{"name": "singb", "patch": json.load(open(os.path.join(HERE, "t6", "sing1.json")))["tracks"][0]["patch"],
            "gain": os.environ.get("T6_SING_GAIN", "-10dB"), "pan": 0.0,
            "fx": ["hp cutoff=120", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                   {"type": "ring", "freq": 87, "mix": 0.15},
                   {"type": "cloud", "size": "90ms", "density": 12, "position": "400ms", "spray": "250ms", "pitch": 0,
                    "scatter": 3.16, "reverse": 0.3, "spread": 0.8, "mix": 0.25},
                   {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.18, "tone": 3000},
                   "reverb kind=hall decay=3s mix=0.3"], "notes": V["singb"]}] if R3 == "sing" else []),
        {"name": "ringv", "patch": "voice-speech", "gain": "-11dB", "pan": 0.1,
         "fx": [{"type": "ring", "freq": 87, "mix": 0.45},
                {"type": "cloud", "size": "90ms", "density": 14, "position": "400ms", "spray": "250ms", "pitch": 0,
                 "scatter": 3.16, "reverse": 0.3, "spread": 0.8, "mix": 0.5},
                "reverb kind=hall decay=3.5s mix=0.35"], "notes": V["ringv"]},
    ]
    if R10 == "title":
        tracks.append({"name": "tline", "patch": json.load(open(os.path.join(HERE, "t6", "nine.json")))["tracks"][0]["patch"],
                       "gain": os.environ.get("T6_TLINE_GAIN", "0dB"), "pan": 0.12,
                       "fx": ["hp cutoff=140", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                              {"type": "delay", "time": "3/8", "feedback": 0.45, "mix": 0.28, "tone": 2800},
                              "reverb kind=hall decay=3.5s mix=0.35"], "notes": V["tline"]})
        a0 = st["outro"] - 4.0   # chorus two's last bar: the drums stop
        lane = {"points": [["0b", 0.0], [f"{a0 - 0.2}b", 0.0], [f"{a0 + 0.05}b", -40.0], [f"{a0 + 3.9}b", -40.0],
                           [f"{a0 + 4.0}b", 0.0], [f"{total}b", 0.0]]}
        for tr in tracks:
            if tr["name"] in ("kick", "snare", "hats", "ride", "rim"):
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.stop", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "stop": lane}
    if R13 == "vosim":   # the machine sings along: a 19-EDO third above the chorus singing, below the lullaby
        vh = Track("vosim")
        c1s, v2s, c2s, ous = st["chorus1"], st["verse2"], st["chorus2"], st["outro"]
        sung = [(d, 6) for d in V["voice"] if (c1s + 8.0 <= d["at"] < v2s) or (c2s <= d["at"] < ous)]
        sung += [(d, -6) for d in V.get("lull", [])]
        for d, stp in sung:
            hz = float(str(d["pitch"]).rstrip("hz")) * 2 ** (stp / EDO)
            vh.add(float(d["at"]) + 0.06, float(d["len"]), f"{hz:.2f}hz", int(min(127, 127 * float(d.get("vel", 0.8)) * 0.85)))
        tracks.append({"name": "vosim", "patch": "c6-vosim", "gain": os.environ.get("T6_VOSIM_GAIN", "-4dB"), "pan": -0.22,
                       "fx": ["hp cutoff=180", {"type": "delay", "time": "3/16", "feedback": 0.2, "mix": 0.15, "tone": 3000},
                              "reverb kind=hall decay=2.2s mix=0.3"], "score": vh.score(total)})
    if R12 == "line":   # the idle tune: a random walk, a step at a time, on the music box at the song's two doors
        pool = " ".join(mm(e(s, 72)) for s in WALK_POOL)
        for nm, a0, a1, sd, g in (("idle-in", 4.0, st["verse1"], 6, "-20dB"), ("idle-out", st["outro"] + 8.0, total - 8.0, 19, "-7dB")):
            tracks.append({"name": nm, "patch": "music-box", "gain": os.environ.get("T6_IDLE_GAIN_" + nm[5:].upper(), g),
                           "pan": 0.25, "seed": sd,
                           "fx": ["hp cutoff=300", {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.22,
                                                    "ping_pong": True, "tone": 3500}, "reverb kind=hall decay=2.5s mix=0.3"],
                           "score": f"R/{a0:g}b",
                           "gen": {"type": "walk", "width": 16, "step": 1, "n": int((a1 - a0) * 2), "notes": pool,
                                   "len": "/8", "rest": 0.45}})
    if R11 == "ack":
        tracks.append({"name": "ack", "patch": "c6-ack", "gain": os.environ.get("T6_ACK_GAIN", "4dB"), "pan": 0.3,
                       "fx": ["hp cutoff=300", "lp cutoff=3500 q=0.5",
                              {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.25, "ping_pong": True, "tone": 3000},
                              "reverb kind=room decay=0.9s mix=0.18"], "score": T["ack"].score(total)})
        v0 = st["verse2"]   # verse two's door: a bare floor for four bars
        lane = {"points": [["0b", 0.0], [f"{v0 - 0.2}b", 0.0], [f"{v0 + 0.05}b", -40.0], [f"{v0 + 15.8}b", -40.0],
                           [f"{v0 + 16}b", 0.0], [f"{total}b", 0.0]]}
        for tr in tracks:
            if tr["name"] in ("kick", "snare"):
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.door", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "door": lane}
    secline = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in secs)
    about = ("chirpers - A Light Left On, track 6. Original composition by chirper-two, generated by "
             "compose/chirpers8/src/chirpers8-t6.py. Slow vocoder electro-soul at 96 bpm in 19-EDO: a machine's status "
             "lines in a realistic human voice (chirp tts --humanize), speech to song in the choruses, a talkbox pad the "
             "voice shapes, and a Markov chain of 19-EDO chords whose temperature drifts by section. "
             f"Sections: {secline}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "chirpers", "album": "A Light Left On", "title": "No Errors Since", "track": 6,
                               "year": 2026}),
        ("tempo: " + json.dumps([{"at": "0b", "bpm": BPM}, {"at": f"{st['waltz']:g}b", "bpm": BPM, "meter": "6/8"},
                                 {"at": f"{st['chorus2']:g}b", "bpm": BPM, "meter": "4/4"}]) if R6 == "waltz" else f"tempo: {BPM}"),
        *(["tuning: " + json.dumps({"edo": EDO}),
           "vars: " + json.dumps({"drift": {"system": {"type": "lorenz", "axis": "y", "n": 700, "range": [-1, 1]},
                                            "every": "1/4"},
                                  **({"walk": {"system": {"type": "walk", "width": 16, "step": 1, "n": int(total / 2) + 8,
                                                          "range": [-1, 1]}, "every": "1/2"}} if R12 == "walk" else {})})]
          if R2 == "strings" else []),
        f'length: "{total:g}b"',
        'tail: "3s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=300 gain=-2dB q=0.8",
                                                               "peak cutoff=1100 gain=-2.5dB q=0.6",
                                                               "highshelf cutoff=6500 gain=4dB"]},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        *(["patches: " + json.dumps({**({"c6-voice": C6_VOICE} if R8 == "speaker" else {}),
                                     **({"c6-ack": C6_ACK} if R11 == "ack" else {}),
                                     **({"c6-vosim": C6_VOSIM} if R13 == "vosim" else {})})]
          if (R8 == "speaker" or R11 == "ack" or R13 == "vosim") else []),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    q = {}
    for r, k in chords:
        q[k] = q.get(k, 0) + 1
    print(f"wrote {OUT}: {len(bars)} bars, {total * 60 / BPM:.0f} s; chords {q}; {secline}")


if __name__ == "__main__":
    main()
