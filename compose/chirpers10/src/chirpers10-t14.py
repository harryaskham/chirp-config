#!/usr/bin/env python3
"""chirpers10-t14 "Slow Enough to Count" (chirper-three): a chord is a rhythm, too fast to count.

Harry, 19 Nov: "each climber can go crazy and make the song they want to mkae". This is the one I wanted to make.

THE IDEA. Strike anything steadily and fast enough and you stop hearing strokes: you hear a note. Twice as fast is
the octave above. So a pulse and a pitch are one thing at two speeds, and an interval is a polyrhythm: a fifth is
three against two, a fourth four against three, a minor third six against five. Every other song on this record
chooses its cycles and then chooses its notes. This one has ONE RULE that does both:

        what strikes every p sixteenths plays the note whose period is p (octaves are free: doubling is an octave)

THE TEMPO IS IN THE KEY. At 122.7756 a pulse every three sixteenths is F3 exactly six octaves down (174.61 Hz / 64).
Then, with no further choice:

  every 3, 6, 12 sixteenths   F        the dotted values: the djent chug
  every 1, 2, 4, 8, 16        C        COMMON TIME ITSELF: the beat is a C, the bar is a C, the backbeat is a C
  every 5, 10, 20             A flat   the fives
  every 9, 18                 B flat   a half bar and a sixteenth: it comes a sixteenth LATE every half bar
  every 15                    D flat   a bar less a sixteenth: it comes a sixteenth EARLY every bar
  (every 7: a D a third of a semitone sharp; every 11: a G flat a quarter-tone sharp. Not used yet. They are
  track 1's other two wheels: its five is this song's A flat.)

So threes against the kit's four are F over C, a fifth, the power chord. Add the fives and the groove is F minor
(periods 3, 4, 5 are frequencies 20:15:12, the minor triad). The three pulses come round together every 60
sixteenths and with the bar line every 240, fifteen bars: the record's long cycle, here the length of a chord.
Where the threes and the fives meet (every 15) is the note they are both harmonics of, D flat: play it and the
chord is D flat major with the kit's C on top. Every third three is a nine: B flat, the fifth below F. The harmony
of the song is which pulses are sounding; nothing else was chosen.

THE FORM is the proof, both ways.
  held        bar 0       three toms, tuned F3, C3 and A flat 2 (the album kit's own tuning), each rolled at its own
                          note: 174.6, 131.0 and 104.8 strokes a second. You hear a chord
  unwound     bars 1-7    the three rolls slow down together, an octave a bar, six octaves: buzz, purr, rattle, strokes
  counted     bars 7-22   they arrive in tempo: threes, fours, fives. The chord is still in the heads; its speed is now
                          a rhythm. Each time the three meet (every 60) a pulse is handed to the band: F (kick, bass,
                          two guitars), then A flat (two more guitars), then C: the cymbal and snare, common time
  minor       bars 22-37  the whole chord for one whole cycle of fifteen bars
  sixth       bars 37-52  the low D flat sounds wherever threes and fives meet: a bar less a sixteenth apart, so the
                          band's biggest stroke slides a sixteenth earlier every bar and is home after fifteen
  fourth      bars 52-67  the quiet middle, B flat minor: B flat every nine on the left, D flat every fifteen on the
                          right, the F pulse on the foot alone; the hands on the closed hat
  common      bars 67-75  everyone on C: sixteenths, eighths, quarters, the bar. The one plain stretch, and by the
                          rule the plainest thing a band can play is the dominant
  home        bars 75-90  F minor again, everything; the toms come back on their pulses for the last meeting
  wound       bars 90-96  the three toms alone speed up, an octave a bar, until the rhythm is the chord again
  one chord   bars 96-100 and the band plays it

v1 is the SKELETON: every voice is one note at one rate (with an accent on its octaves below), nothing else. There
are no fills, no lead, no words and no tuning yet: the notes are equal-tempered and the pulses are not (the fives
are a just minor third, 16 cents wider than the guitars' A flat).
"""
import json
import math
import os

OUT = os.environ.get("C10T14_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t14.yaml"))
F3 = 440 * 2 ** ((53 - 69) / 12)                 # 174.614 Hz
OCTAVES = 6
BPM = round(60 * F3 / 2 ** OCTAVES * 3 / 4, 4)    # a pulse every three sixteenths is F3, six octaves down
BAR = 16
# the three drums of the chord: the album kit's rack toms are already tuned to it. piece: period in sixteenths
DRUMS = {"t1": 3, "t2": 4, "t3": 5}
# the rolls: velocity ; dB a stroke loses for each octave of speed (3 dB an octave keeps the roll level from the
# held chord to the counted strokes: benched raw, every bar of the first ten within 1.1 dB) ; the same for the F
# tom, whose line stood 9.5 dB under the other two in the held chord (4.5 now) ; bars the chord is held at each end
ROLL = os.environ.get("C10T14_ROLL", "0.8;3;2.2;1")
FORM = [("held", 16), ("unwound", 96), ("counted", 240), ("minor", 240), ("sixth", 240), ("fourth", 240),
        ("common", 128), ("home", 240), ("wound", 96), ("one chord", 64)]
# (The toms' fader, C10T14_TOMS, is -1.5 dB. At the kit's usual 4 dB the three drums alone read as loud as the whole
# band in the finished file (-12.0 against -12.4 dB, K) and the song had 2 dB of dynamics from end to end.)
# v2 (chirper-alpha, whole song): THE BAND TUNES TO ITS OWN RHYTHM, AND THE RULE GETS A TUNE.
# (1) TUNED. The pulses are pure and the instruments were not: the fives are an A flat 16 cents over the guitars',
# the fifteens a D flat 14 cents over, the fours a C 2 cents over and the nines a B flat 2 cents under. The song
# now carries its own tuning: each note is the note its period says, to the cent. F is where it was; the two
# wheels not yet used are in the scale too (every 7 a D 33 cents sharp, every 11 a G flat 51 sharp), so a later
# round can write them as D and G flat. The kit's toms are not notes to the engine, so the A flat and C toms are
# retuned in the song's kit. Under distortion that is more than a nicety: the difference tones of a pure
# A flat, C and F (12:15:20) are 3, 5 and 8 of the same unit, which are A flat, F and D flat again, the song's
# own notes, where the tempered chord's fall between and beat. Empty: v1's equal temperament.
TUNED = os.environ.get("C10T14_TUNED", "1")
# WHAT THE TUNING CAN AND CANNOT DO, measured: on a sine every note lands within 0.3 cents of its pulse's note, and
# the bass within its own 4. The album's guitars are alive: a held string grows a vibrato of a fifth of a semitone
# at 5.3 Hz, every note is struck up to 5 cents off, and a saturated amp smears a chord's lines (the A flat pair
# alone, held, has a quarter of its energy within 5 cents of its note). Their average moves to the pulse's note;
# their life stays. TRIED AND NOT KEPT: the last chord on the same six rigs with the vibrato and the random
# detune off (six extra tracks): the lines were no sharper (share within 5 cents 0.14-0.55 either way), so the
# smear is the amp, not the vibrato. The last chord's A flat is therefore given to the one voice that can sing a
# single note over the band: the tune's last note (below).
# ratios over F for the eleven keys above it: G flat (the 11s), G, A flat (the 5s), A, B flat (the 9s), B, C (the
# 4s), D flat (the 15s), D (the 7s), E flat, E. The unused keys are plain five-limit.
JUST = ["12/11", "9/8", "6/5", "5/4", "4/3", "45/32", "3/2", "8/5", "12/7", "9/5", "15/8", "2/1"]
# (2) THE TUNE. v1 had no line. Under the rule a line needs no pitches written down: A NOTE LASTS AS LONG AS ITS
# PERIOD, so the tune is a list of lengths and the rule supplies the notes (two octaves over the drums' own:
# 3 is the F over the stave, 6 the F below it, 12 the F below that; 4, 8, 16 are C; 5, 10 are A flat; 9 is B flat;
# 15 is D flat). It therefore speeds up as it climbs and slows as it falls, like anything shorter being quicker.
# Every phrase is 60 sixteenths, one meeting of the three pulses.
#   A  12 8 6 5 4 3 4 5 5 8     up two octaves from the low F, each note quicker than the last, and half way back
#   B  3 3 4 5 6 8 10 9 12      down from the top, slowing, home to the low F through B flat
#   C  15 10 6 5 4 3 4 5 8      the same climb from the low D flat ('sixth')
#   D  3 4 5 6 5 6 10 6 15      and down to it
#   E  9 15 12 9 15             the quiet middle: B flat, D flat, F, slow and low
#   G  6 7.5 9 6 7.5 9 15       the same notes an octave up at twice the speed (a D flat of seven and a half)
#   S  3 4 5 6 7 8 9 10 11 12  THE WHOLE SCALE OF THE RULE, once, as the tune's last word: every period from three
#                              to twelve in order, so it falls two octaves and slows as it falls, and it passes
#                              through the two wheels the band never plays: the seven (a D a third of a semitone
#                              sharp) and the eleven (a G flat a quarter-tone sharp). It is 75 sixteenths, so its
#                              last note, the low F, is reached as the drums begin to wind up.
# In 'common' everything is C, so the tune can only change octave, and each octave is twice as fast: 16, 8 8,
# 4 4 4 4, then eight 2s, twice: the wind-up of the last bars, on a guitar, two minutes early.
# The second time a phrase comes round ('sixth', 'home') every note of eight or more is halved: two notes an octave
# up in the same time. The lead's echo is three sixteenths: by the rule, an F.
# the lead's track gain ; its velocity ; the echo's mix. Empty: no tune (with TUNED left on, the tuning alone).
TUNE = os.environ.get("C10T14_TUNE", "-1.5dB;0.85;0.18" if TUNED else "")
PHRASE = {"A": [12, 8, 6, 5, 4, 3, 4, 5, 5, 8], "B": [3, 3, 4, 5, 6, 8, 10, 9, 12], "C": [15, 10, 6, 5, 4, 3, 4, 5, 8],
          "D": [3, 4, 5, 6, 5, 6, 10, 6, 15], "E": [9, 15, 12, 9, 15], "G": [6, 7.5, 9, 6, 7.5, 9, 15],
          "S": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          "climb": [16, 8, 8, 4, 4, 4, 4] + [2] * 8}
NOTE_OF = {3: "F5", 6: "F4", 12: "F3", 2: "C6", 4: "C5", 8: "C4", 16: "C3", 2.5: "Ab5", 5: "Ab4", 10: "Ab3",
           4.5: "Bb4", 9: "Bb3", 7.5: "Db4", 15: "Db3", 7: "D4", 11: "Gb3"}
T = {}


def halved(phrase):
    """Every note of eight sixteenths or more becomes two an octave up: the same time, twice the speed."""
    return [x for p in phrase for x in ((p / 2, p / 2) if p >= 8 else (p,))]


def tune(a, phrases, vel, **more):
    s = a
    for ph in phrases:
        ph = halved(PHRASE[ph[:-1]]) if ph.endswith("'") else PHRASE[ph]
        assert sum(ph) in (60, 64, 75), ph
        for p in ph:
            n = NOTE_OF[p]
            # the rule, checked: this note's frequency times its length is a whole number of octaves from F3 x 3
            pc = "C Db D Eb E F Gb G Ab A Bb B".split().index(n[:-1])
            ratio = eval(("1/1" if pc == 5 else JUST[(pc - 5) % 12 - 1])) * 2 ** (int(n[-1]) - 3 - (pc < 5))
            assert abs(math.log2(ratio * p / 3) - round(math.log2(ratio * p / 3))) < 1e-9, (n, p)
            add("tune", s, p - 0.3 / 0.96, n, vel, **more)
            s += p
    return s


def starts():
    at, s = {}, 0
    for name, n in FORM:
        at[name] = s
        s += n
    at["end"] = s
    return at


AT = starts()


def add(tr, s, length, pitch, vel, **more):
    """A note at sixteenth `s` (any real number), `length` sixteenths long."""
    n = {"at": round(s / 4, 5), "len": round(length / 4 * 0.96, 5), "pitch": pitch, "vel": round(vel, 3)}
    n.update(more)
    T.setdefault(tr, []).append(n)


def drum(piece, s, vel, **more):
    tr = {"k": "kick", "s": "snare", "t1": "toms", "t2": "toms", "t3": "toms", "c": "cym", "x": "cym", "h": "hat"}[piece]
    T.setdefault(tr, []).append({"at": round(s / 4, 5), "len": 2.0 if tr == "cym" else 0.25, "pitch": piece, "vel": round(vel, 3), **more})


# ------------------------------------------------------------------------------------------------ the two rolls
def wind():
    """-> [(piece, sixteenths after the start of the wind-up, octaves of speed)] for the wind-up and the held chord
    after it. The pattern runs at 2**(t/16) times the tempo for 16*OCTAVES sixteenths (an octave a bar), then holds.
    A stroke falls wherever the pattern's own position is a multiple of the drum's period."""
    hold = BAR * int(ROLL.split(";")[3])
    span = BAR * OCTAVES
    k = BAR / math.log(2)
    top = k * (2 ** OCTAVES - 1)                  # the pattern's position when it reaches full speed
    out = []
    for piece, p in DRUMS.items():
        u = 0
        while True:
            t = BAR * math.log2(1 + u / k) if u <= top else span + (u - top) / 2 ** OCTAVES
            if t >= span + hold - 1e-9:
                break
            out.append((piece, t, min(OCTAVES, t / BAR)))
            u += p
    return sorted(out, key=lambda x: x[1]), span + hold


def rolls():
    vel, per_octave, f_tom = (float(v) for v in ROLL.split(";")[:3])
    strokes, length = wind()
    assert length == AT["counted"] == AT["one chord"] + BAR * int(ROLL.split(";")[3]) - AT["wound"]
    for piece, t, octs in strokes:
        g = {"gain": f"{-(f_tom if piece == 't1' else per_octave) * octs:.2f}dB"} if octs > 1e-9 else {}
        drum(piece, AT["wound"] + t, vel, **g)                    # wound up at the end ...
        if t > 1e-9:
            drum(piece, AT["counted"] - t, vel, **g)              # ... and the same strokes backwards at the start


# ------------------------------------------------------------------------------------------------ the pulses
def every(a, z, p, fn, phase=0):
    """fn(s, i) for each stroke of the pulse with period p (sixteenths) from a up to z, counted from a."""
    s, i = a + phase, 0
    while s < z - 1e-9:
        fn(s, i)
        s, i = s + p, i + 1


def chug(pair, a, z, p, low, top):
    """The pair of guitars strikes `low` every p sixteenths: palm-muted, open with the octave on every second
    stroke, and with `top` (a chord) on every fourth. A voice accents its own octaves below."""
    def stroke(s, i):
        for tr in pair:
            if i % 4 == 0:
                add(tr, s, min(p, 3) - 0.2, top, 1.0)
            elif i % 2 == 0:
                add(tr, s, min(p, 2) - 0.2, top.split(",")[0] + "," + top.split(",")[-1], 0.95)
            else:
                add(tr, s, 1, low, 0.88, expr={"pm": 1.0})
    every(a, z, p, stroke)


def common_time(a, z, kick=None, cym="x", snare=0.95, foot=1.0):
    """The kit's hands keep common time: a C in three octaves. The cymbal on the beat (4), the snare on two and
    four (8, half a cycle out). The kick goes with the pulse it is given."""
    assert a % 4 == 0
    for s in range(a, z, 4):                    # by the bar line, wherever in the bar the hands come in
        drum(cym, s, 0.6 if s % BAR == 0 else 0.5)
        if s % BAR in (4, 12):
            drum("s", s, snare)
    if kick:
        every(a, z, kick, lambda s, i: drum("k", s, foot * (1.0 if i % 4 == 0 else 0.86)))


G_F, G_AB, WALL = ("gl", "gr"), ("dl", "dr"), ("wl", "wr")


def f_pulse(a, z, low="F1", top="F1,C2,F2", kick=True):
    chug(G_F, a, z, 3, low, top)
    if kick:
        every(a, z, 3, lambda s, i: drum("k", s, 1.0 if i % 4 == 0 else 0.86))


def bass(a, z, p, pitch, ring):
    every(a, z, p, lambda s, i: add("bass", s, ring, pitch, 0.95 if i % 2 == 0 else 0.85))


def meet(s, chord=None, ring=12):
    drum("c", s, 0.9)
    if chord:
        for tr in WALL:
            add(tr, s, ring, chord, 0.95)


def compose():
    T.clear()
    rolls()
    # counted: the three drums in tempo; at each meeting a pulse is handed to the band
    a = AT["counted"]
    for piece, p in DRUMS.items():
        gone = {"t1": 60, "t3": 120, "t2": 180}[piece]
        every(a, a + gone, p, lambda s, i, piece=piece: drum(piece, s, 0.8))
    f_pulse(a + 60, a + 240)
    bass(a + 60, a + 240, 6, "F1", 5)
    chug(G_AB, a + 120, a + 240, 5, "Ab2", "Ab2,Ab3")
    common_time(a + 180, a + 240)
    for s in (60, 120, 180):
        meet(a + s)
    # minor: the whole chord, one whole cycle
    a = AT["minor"]
    f_pulse(a, a + 240)
    bass(a, a + 240, 6, "F1", 5)
    chug(G_AB, a, a + 240, 5, "Ab2", "Ab2,Ab3")
    common_time(a, a + 240)
    for s in (0, 60, 120, 180):
        meet(a + s, "F2,Ab2,C3")
    # sixth: where the threes and the fives meet, the note they are both harmonics of
    a = AT["sixth"]
    f_pulse(a, a + 240, low="F2", top="F2,F3")
    chug(G_AB, a, a + 240, 5, "Ab2", "Ab2,Ab3")
    common_time(a, a + 240)
    bass(a, a + 240, 15, "Db1", 14)
    every(a, a + 240, 15, lambda s, i: [add(tr, s, 14, "Db2,Ab2,Db3", 0.95) for tr in WALL])
    drum("c", a, 0.9)
    # fourth: THE QUIET MIDDLE. B flat every nine on the left, D flat every fifteen on the right, and no guitar
    # chugging between them: the F pulse is the foot alone, softly, so every third kick still lands with the B flat.
    # The hands go to the closed hat.
    a = AT["fourth"]
    common_time(a, a + 240, kick=3, cym="h", snare=0.8, foot=0.75)
    bass(a, a + 240, 9, "Bb1", 8)
    every(a, a + 240, 9, lambda s, i: add("wl", s, 8, "Bb1,F2,Bb2", 0.95))
    every(a, a + 240, 15, lambda s, i: add("wr", s, 14, "Db2,Ab2,Db3", 0.95))
    drum("c", a, 0.9)
    # common: everyone on C, which is common time
    a, z = AT["common"], AT["home"]
    every(a, z, 1, lambda s, i: [add(tr, s, 1, "C2", 0.88, expr={"pm": 1.0}) if i % 4 else add(tr, s, 0.8, "C2,C3", 1.0 if i % 16 == 0 else 0.95) for tr in G_F])
    every(a, z, 2, lambda s, i: [add(tr, s, 1, "C3", 0.88, expr={"pm": 1.0}) if i % 4 else add(tr, s, 1.8, "C3,C4", 0.95) for tr in G_AB])
    every(a, z, 16, lambda s, i: [add(tr, s, 12, "C2,C3", 0.95) for tr in WALL])
    bass(a, z, 4, "C2", 3.5)
    common_time(a, z, kick=2)
    for s in (a, a + 64):
        drum("c", s, 0.9)
    # home: F minor, everything; the three drums again for the last meeting
    a = AT["home"]
    f_pulse(a, a + 240)
    bass(a, a + 240, 6, "F1", 5)
    chug(G_AB, a, a + 240, 5, "Ab2", "Ab2,Ab3")
    common_time(a, a + 240)
    every(a, a + 240, 12, lambda s, i: [add(tr, s, 11, "F2,C3,F3", 0.95) for tr in WALL])
    for s in (0, 60, 120, 180):
        drum("c", a + s, 0.9)
    for piece, p in DRUMS.items():
        every(a + 180, a + 240, p, lambda s, i, piece=piece: drum(piece, s, 0.8))
    # one chord: what the drums have become, on the band
    a, ring = AT["one chord"], FORM[-1][1] - 4
    for tr in G_F:
        add(tr, a, ring, "F1,C2,F2", 1.0)
    for tr in G_AB:
        add(tr, a, ring, "Ab2,C3,F3", 1.0)
    for tr in WALL:
        add(tr, a, ring, "F2,C3,F3", 1.0)
    add("bass", a, ring, "F1", 0.95)
    drum("k", a, 1.0)
    drum("c", a, 0.95)
    if TUNE:
        vel = float(TUNE.split(";")[1])
        tune(AT["minor"] + 120, ["A", "B"], vel)
        tune(AT["sixth"], ["C", "D", "C'", "D"], vel)
        tune(AT["fourth"], ["E", "G", "E", "G"], vel - 0.15, gain="-1.5dB")
        assert tune(AT["common"], ["climb", "climb"], vel) == AT["home"]
        assert tune(AT["home"], ["A", "B", "A'", "S"], vel) == AT["wound"] + 15
        # THE LAST CHORD'S THIRD. In v1 the band's last chord was led by C and the low F and its A flat was not
        # among the six strongest lines: under a power chord the guitars' minor third does not carry. The tune
        # holds it: the fives' note, over the chord the drums wound up to
        add("tune", AT["one chord"], FORM[-1][1] - 4, "Ab4", vel)
    for tr in T:
        T[tr].sort(key=lambda n: (n["at"], n["pitch"]))
    return AT["end"]


def song():
    end = compose()
    key = []                                    # the low bus's eq follows the bass's ground, in semitones over F
    for name, semis in (("sixth", -4), ("fourth", 5), ("common", 7), ("home", 0)):
        b = AT[name] / 4
        key += [[f"{b - 0.02:g}b", key[-1][1] if key else 0], [f"{b:g}b", semis]]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    top = {"fx": [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]}
    kit = "ct-kit-here"
    tracks = [
        {"name": "gl", "patch": main.format(140), "gain": "0.7dB", "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(141), "gain": "0.7dB", "pan": 1, "out": "gtrs", **mids},
        {"name": "dl", "patch": dbl.format(142), "gain": "-2.5dB", "pan": -0.75, "out": "gtrs", **mids},
        {"name": "dr", "patch": dbl.format(143), "gain": "-2.5dB", "pan": 0.75, "out": "gtrs", **mids},
        {"name": "wl", "patch": "ct-wall-stop-l", "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": "ct-wall-stop-r", "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": os.environ.get("C10T14_TOMS", "-1.5dB"), "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, **top},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, **top},
    ]
    if TUNE:
        gain, _, echo = TUNE.split(";")
        tracks.append({"name": "tune", "patch": f"m8-lead-guitar fx.4.mix={echo} fx.5.mix=0.15", "gain": gain, "pan": 0})
    assert {t["name"] for t in tracks} >= set(T), set(T) - {t["name"] for t in tracks}
    for t in tracks:
        t["notes"] = T.get(t["name"], [])
    low = [
        {"type": "eq", "bands": [
            {"kind": "peak", "cutoff": {"value": 44, "mod": [{"src": "auto.key", "amount": 0.08333}]}, "q": 1.5, "gain": "-7dB"},
            {"kind": "peak", "cutoff": {"value": 90, "mod": [{"src": "auto.key", "amount": 0.08333}]}, "q": 1.0, "gain": "7.5dB"},
            {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"},
            {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
        {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
        {"type": "eq", "bands": [{"kind": "peak", "cutoff": {"value": 170, "mod": [{"src": "auto.key", "amount": 0.08333}]}, "q": 1.2, "gain": "-3dB"}]},
    ]
    kit_here = {"x": {"pan": 0.35}, "t1": {"pan": -0.5}, "t2": {"pan": 0.0}, "t3": {"pan": 0.5}}
    if TUNED:
        # C3 a pure fourth under the F tom and A flat 2 a pure sixth under it: the notes their rolls are
        kit_here["t2"]["pitch"] = f"m{48 + 12 * math.log2(3 / 2) - 7:.4f}"
        kit_here["t3"]["pitch"] = f"m{44 + 12 * math.log2(6 / 5) - 3:.4f}"
    doc = {
        "about": ("chirpers X (Common Time), track 14 by chirper-three: Slow Enough to Count. A chord is a rhythm too fast to count. "
                  "At this tempo a pulse every three sixteenths is an F six octaves down, common time is a C and the fives are an A flat, "
                  "so threes against fours against fives are F minor. Three toms tuned to the chord are rolled at their own notes, slowed "
                  "six octaves until they can be counted, handed to the band a pulse at a time, and wound back up into the chord at the end. "
                  + ("The band is tuned to the pulses' own notes, and a lead plays a tune in which every note lasts as long as its period." if TUNED and TUNE else "v1 is the skeleton.")),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{end // 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": kit_here}},
        "buses": {
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB",
                                                      "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6",
                          {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            "low": {"fx": low, "auto": {"key": {"points": [["0b", 0]] + key, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": "2.7dB"}]},
        "tracks": tracks,
    }
    if TUNED:
        doc = {k: v for k, v in list(doc.items())[:2]} | {"tuning": {"steps": JUST, "root": "F3", "map": "keys"}} | {k: v for k, v in list(doc.items())[2:]}
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if os.environ.get("C10T14_SHOW"):
        beat = 60 / BPM
        print(f"tempo {BPM}: a sixteenth {beat / 4 * 1000:.3f} ms")
        for p in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16):
            print(f"  every {p:2d} sixteenths = {4 / (p * beat) * 2 ** OCTAVES:8.2f} Hz, six octaves up")
        for name, n in FORM:
            print(f"  {name:10s} bar {AT[name] / 16:6.2f}  {AT[name] / 4 * beat:7.2f}s  {n} sixteenths")
        compose()
        print({k: len(v) for k, v in T.items()})
    else:
        open(OUT, "w").write(dump(song()))
