#!/usr/bin/env python3
"""chirpers10-t16 "Close Enough" (chirper-two): two reeds a hair apart, and a band that plays the difference.

Tune one string to another and you do not listen to the notes: you listen to the wobble between them, and you turn
the peg until it slows, and stops. Two notes a hair apart make a third thing that is not a note at all but a pulse,
as many times a second as the hair is wide in cycles. And every overtone of the pair is twice, three times, four
times as far apart as the notes themselves: so the second harmonic pulses twice for each pulse of the first, the
third three times, the fourth four. One mistuned unison is a polyrhythm, 1 : 2 : 3 : 4, with nobody playing it.

This piece is that, taken as the whole rhythm section. Two harmoniums hold one note. The second is sharp of the
first by a width chosen in cycles a second, so that the wobble of the pair is IN TEMPO: at 66 to the minute a hair
of 1.1 Hz (eleven cents at F3) pulses once a beat. Then, with no further choice, the band plays what the pair is
already doing:

  the kick      the pulse of the notes themselves       (the first harmonic's beats; the bass holds a note to each)
  the guitars   twice as fast: the second harmonic's    (the low note open with the kick, muted between)
  the toms      three times: the third's
  the hat       four times: the fourth's
  the snare     is not in the rule: two and four of every bar. The drummer's left hand keeps common time

So the METRE IS A TUNING. Widen the hair by a quarter and the whole band is in five against the snare's four; by
three quarters, in seven; narrow it and they are in three; halve it and they play half as often. Nothing is
counted: the form below is a list of widths. And the song ends the way tuning ends: the hair is halved, and halved
again, the strokes come further and further apart (each rings until the next), and when the two reeds are one note
the band has one chord left.

  in tune      the pair on one note: still
  a hair       a quarter of a pulse to the beat: one kick to the bar, four taps of the hat
  wider        half a pulse to the beat
  square       ONE pulse to the beat: common time, from a tuning. The band comes in
  five         a hair and a quarter: five against four
  seven        a hair and three quarters: seven against four
  three        three quarters of a hair: three against four, the slow one, on the lowest ground
  square       one again, as long as the first time
  close enough a half, a quarter, an eighth, and in tune: the last chord

Inside each kick, then, there is one cell: two against three against four (guitar, toms, hat). It is the same cell at
every width; only how many of them fit the snare's bar changes.

v1 is the SKELETON: the whole shape standing, bare (Harry, 19 Nov: "each climber can go crazy and make the song they
want to mkae"). The pair's pitches are written in hertz, so that the hair is a number of cycles and not of cents.

The first thing built for this slot was a Collatz song (halve the even, treble the odd and add one, as lengths and as
harmonics of F). chirper-one recorded So Far on the same rule in track seventeen while it was on the bench, so this
is the other song.
"""
import json
import os
from collections import defaultdict
from fractions import Fraction as Fr

OUT = os.environ.get("C10T16_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../songs/chirpers10-t16.yaml"))
BPM = 66
HAIR = BPM / 60.0                            # Hz: the width that pulses once a beat
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# THE FORM: name ; the hair's width, in pulses to the beat ; bars ; the ground (semitones over F) ; who plays
#   k = the kick (the notes' own pulse), g = guitars and bass (twice), t = toms (three times), h = hat (four times),
#   s = the snare on three, c = an open chord on each bar line
FORM = [
    ("in tune", Fr(0), 2, 0, ""),
    ("a hair", Fr(1, 4), 4, 0, "kh"),
    ("wider", Fr(1, 2), 4, 0, "khts"),
    ("square", Fr(1), 8, 0, "kgthsc"),
    ("five", Fr(5, 4), 8, 3, "kgthsc"),
    ("seven", Fr(7, 4), 8, 6, "kgthsc"),
    ("three", Fr(3, 4), 8, -2, "kgthsc"),
    ("square again", Fr(1), 8, 0, "kgthsc"),
    ("a half", Fr(1, 2), 2, 0, "kgths"),
    ("a quarter", Fr(1, 4), 2, 0, "kgh"),
    ("an eighth", Fr(1, 8), 2, 0, "kg"),
    ("close enough", Fr(0), 2, 0, "c"),
]
REED = 53                                    # the pair's note on F: F3
# v2, palette: THE PULSES ARE NAMED. The pair's overtones pulse two, three and four times to its one, and the kit
# says so in strokes that have no pitch. A handpan (no other song on the record has one; its note fields are tuned
# fundamental, octave and twelfth, the first three of the pair's own series) strikes each overtone AS A NOTE every
# time that overtone swells: the reed's own F once to the pulse, the octave twice, the twelfth (C) three times, the
# double octave four times. All four swell together on the pulse, so the pulse is a chord; between pulses it is
# two against three against four: high F, C, the two Fs, C, high F. The cell is a tune, and it is the tune the
# two reeds are already singing. Its notes are written in hertz, at whole multiples of the still reed.
# It frames the song, and it SAYS, THEN LISTENS. As the hair opens (0:07.3) it names the overtones in order, a bar
# each: one and two; then three; then four; and leaves the fourth bar to the pair alone. When the hair is twice as
# wide (0:21.8) it says the whole cell on the first pulse of each bar and leaves the second to the pair, until the
# band takes the cell over at 0:36.4. As the hair closes it comes back where the toms have gone (3:09.1) and
# leaves as it came, the fours first, then the threes; the last pulse (3:16.4, two bars long) has only one and
# two; then one chord, in tune.
# Empty restores v1.  The song's own handpan ; the track gain as the hair opens ; as it closes (the band is in;
# leave this field empty and it does not come back at the end: re-fit the target) ; the loudness target (every bar
# without it keeps v1's mastering gain).
# (The library handpan beats with itself: a split partner 3 cents up on the fundamental, the octave 2 cents sharp,
# the twelfth 3 flat; and its shell answers at 92 Hz, a semitone over F. In this song the only wobble may be the
# hair: the partner is silenced, the partials are exact, the shell is on F2.)
PAN = os.environ.get("C10T16_PAN", "handpan synth.layers.0.partials.1.1=0 synth.layers.1.cents=0 synth.layers.2.cents=0 synth.layers.3.fixed=87.307;-17dB;-11dB;-9.981")
NAMED = {"a hair": ((1, 2), (1, 2, 3), (1, 2, 3, 4), ()), "wider": ((1, 2, 3, 4), ()) * 4,
         "a quarter": ((1, 2, 3, 4), (1, 2, 3)), "an eighth": ((1, 2),)}
TOUCH = {1: 0.8, 2: 0.68, 3: 0.6, 4: 0.54}
STILL = "harmonium fx.0.depth=0 synth.layers.1.cents=0"       # see the tracks


def build():
    ev = defaultdict(list)
    marks = []

    def put(tr, at, pitch, dur, vel, mute=False):
        e = {"at": round(float(at), 5), "len": round(float(dur), 5), "pitch": pitch, "vel": vel}
        if mute:
            e["expr"] = {"pm": 1}
        ev[tr].append(e)

    def kit(tr, at, piece, vel):
        put(tr, at, piece, 0.95 if piece in ("c", "x") else 0.29, vel)

    b = 0                                    # in beats
    for name, r, bars, ground, who in FORM:
        marks.append((name, b, r, bars))
        f = hz(REED + ground)
        # how often the pair is struck again: a bar (two when the pulse is that slow; once when there is no pulse at all)
        span = 4 * bars if not r else 8 if r == Fr(1, 8) else 4
        for a in range(b, b + 4 * bars, span):
            put("reed", a, f"{f:.3f}hz", span - 0.04, 0.8)
            put("hair", a, f"{f + float(r) * HAIR:.3f}hz", span - 0.04, 0.8)
            n = r * span                     # pulses of the notes themselves in this span
            if "c" in who and a % 4 == 0:    # the open chord on the bar line
                root = 29 + ground
                for tr in ("left", "right"):
                    put(tr, a, f"{nm(root)},{nm(root + 7)},{nm(root + 12)}", (1 / (2 * float(r)) - 0.08) if r and "g" in who else 7.6, 0.96)
                if not r:
                    put("bass", a, nm(root), 7.6, 0.95)
                kit("brass", a, "c" if a == b or (a - b) % 16 == 0 else "x", 0.86 if a == b else 0.72)
            if not r:
                continue
            for layer, mult in (("k", 1), ("g", 2), ("t", 3), ("h", 4)):
                if layer not in who:
                    continue
                count = n * mult
                assert count.denominator == 1, (name, layer, count)
                for j in range(int(count)):
                    at = a + Fr(span * j, int(count))
                    if layer == "k":
                        kit("foot", at, "k", 0.98 if j == 0 else 0.88)
                        if "g" in who:        # the bass is the notes' own pulse too: it holds from one kick to the next
                            put("bass", at, nm(29 + ground), Fr(span, int(count)) - Fr(1, 10), 0.95 if j == 0 else 0.9)
                    elif layer == "g":
                        if j == 0 and "c" in who and a % 4 == 0:
                            continue          # the chord is there
                        gap = Fr(span, int(count))
                        for tr in ("left", "right"):
                            if j % 2 == 0:    # with the kick: the low string and its fifth, open, cut before the muted stroke
                                put(tr, at, f"{nm(29 + ground)},{nm(36 + ground)}", gap - Fr(1, 12), 0.92)
                            else:
                                put(tr, at, nm(29 + ground), min(Fr(3, 10), gap * Fr(3, 5)), 0.82, mute=True)
                    elif layer == "t":
                        kit("skins", at, ("ft", "t2", "t1")[j % 3], 0.8 if j % 3 == 0 else 0.62)
                    else:
                        kit("hat", at, "h", 0.62 if j % 4 == 0 else 0.42)
            if "s" in who:
                for bar in range(a, a + span, 4):
                    kit("snare", bar + 1, "s", 0.9)
                    kit("snare", bar + 3, "s", 0.95)
        if PAN and name in NAMED and (b < 40 or PAN.split(";")[2]):
            pulse = 1 / r                    # beats
            assert len(NAMED[name]) == r * 4 * bars, name
            for i, which in enumerate(NAMED[name]):
                tr = "pan" if b < 40 else "pan-out"
                for k in which:              # overtone k, k times to the pulse
                    for j in range(k):
                        put(tr, b + i * pulse + Fr(j, k) * pulse, f"{k * f:.3f}hz", min(2, float(pulse) / 2),
                            round(TOUCH[k] + (0.2 if name == "an eighth" else 0), 2))   # three strokes in two bars: firmer
        if PAN and PAN.split(";")[2] and name == "close enough":   # in tune: all four at once
            for k in (1, 2, 3, 4):
                put("pan-out", b, f"{k * f:.3f}hz", 6, round(1.06 - 0.06 * k, 2))
        b += 4 * bars
    end = b
    # the bass bus's eq follows the ground, as the album's does (its notch and lift sit on the note's first two harmonics)
    key, at, last = [["0b", 0]], 0, 0
    for name, r, bars, ground, who in FORM:
        if ground != last:
            key += [[f"{at - 0.02:g}b", last], [f"{at}b", ground]]
            last = ground
        at += 4 * bars
    keyed = lambda hz_: {"value": hz_, "mod": [{"src": "auto.key", "amount": 0.08333}]}

    def track(name, patch, gain, pan=0, out=None, fx=None, sends=None):
        tr = dict(name=name, patch=patch, gain=gain, pan=pan, notes=sorted(ev[name], key=lambda e: (e["at"], str(e["pitch"]))))
        if out:
            tr["out"] = out
        if sends:
            tr["sends"] = sends
        if fx:
            tr["fx"] = fx
        return tr

    # THE BAND IS THE ALBUM'S (Common Time's kit staging, bass bus and guitar bus, as In the Time Of carries them).
    # What is this song's own is the pair: two harmoniums, close together in the middle so that they beat in the
    # air of one place and not between two ears.
    palm = " synth.layers.0.mute=expr.pm*0.56 synth.layers.0.mute_width=0.10"
    mid = [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    tracks = [
        # (their body cut 6 dB at 300 Hz: against the eleven records the band with the pair read 3 to 4 dB over at 120-500 Hz,
        # and of 250-500 Hz the pair was the largest part)
        # ONE STILL REED EACH. The library harmonium beats with itself (a second reed 7 cents sharp: 0.7 times a second
        # at F3, twice that an octave up) and its bellows tremble at 1.3 Hz: three slow pulses that are not in tempo,
        # under the one that is. Here the second reed is in unison and the bellows are steady, so the only wobble in
        # the song is the hair.
        track("reed", STILL, "-9.5dB", -0.12, fx=[{"type": "eq", "bands": ["peak cutoff=300 q=0.8 gain=-6dB"]}]),
        track("hair", STILL, "-9.5dB", 0.12, fx=[{"type": "eq", "bands": ["peak cutoff=300 q=0.8 gain=-6dB"]}]),
        track("left", "ct-twin fx.2.cone=37" + palm, "0.5dB", -0.92, "strings", mid),
        track("right", "ct-twin fx.2.cone=41" + palm, "0.5dB", 0.92, "strings", mid),
        # the bass holds its notes here (on the other songs it chugs): half of 120-250 Hz was its overtones
        track("bass", "ct-bass", "0.5dB", 0, "low", [{"type": "eq", "bands": ["peak cutoff=180 q=1 gain=-3dB"]}]),
        track("foot", "ct-kit", "3.5dB", 0, "drums", [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]),
        track("snare", "ct-kit", "3.5dB", 0, "drums", [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}], {"oh": "-1.5dB"}),
        track("skins", "ct-kit", "-3dB", 0, "drums"),      # at 1.5 dB they were half of everything from 60 to 500 Hz
        track("hat", "ct-kit", "16dB", -0.3, "drums", air, {"oh": "4.5dB"}),
        track("brass", "ct-kit", "-2.5dB", 0.2, "drums", air, {"oh": "4.5dB"}),
    ]
    if PAN:
        patch, opens, closes, _ = PAN.split(";")
        tracks += [track("pan", patch, opens, 0.0)] + ([track("pan-out", patch, closes, 0.0)] if closes else [])
    buses = {
        "strings": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
        "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                         {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                         "clip drive=0dB ceiling=-13dB",
                         {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB",
                                                  "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
        "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6",
                      {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
        "low": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": keyed(44), "q": 1.5, "gain": "-7dB"},
                                                {"kind": "peak", "cutoff": keyed(90), "q": 1.0, "gain": "7.5dB"},
                                                {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"},
                                                {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                       {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                       {"type": "eq", "bands": [{"kind": "peak", "cutoff": keyed(170), "q": 1.2, "gain": "-3dB"}]}],
                "auto": {"key": {"points": key, "curve": 0}}},
    }
    doc = dict(
        about=("Close Enough: chirpers, Common Time, track sixteen (chirper-two). Two harmoniums hold one note a hair apart; "
               "the hair is as wide in cycles as the tempo is in beats, so the pair pulses in time, and each overtone pulses twice, "
               "three times, four times as fast. The band plays those pulses. The metre is a tuning; the snare keeps four."),
        tempo=BPM, seed=1, length=f"{end:g}b", tail="5s", ceiling="-1dB", loudness=float(PAN.split(";")[3]) if PAN else -10, event_stable=True,
        buses=buses, master={"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}]}, tracks=tracks)
    return doc, marks, end


def dump(doc):
    return "\n".join("tracks:\n" + "\n".join("  - " + json.dumps(tr) for tr in v) if k == "tracks" else k + ": " + json.dumps(v)
                     for k, v in doc.items()) + "\n"


if __name__ == "__main__":
    doc, marks, end = build()
    if os.environ.get("C10T16_SHOW"):
        sec = lambda t: f"{int(t * 60 / BPM // 60)}:{t * 60 / BPM % 60:04.1f}"
        for name, b, r, bars in marks:
            print(f"{name:14s} bar {b // 4 + 1:3d}  {sec(b)}  the hair {float(r) * HAIR:5.3f} Hz ({r} of a pulse to the beat), {bars} bars: "
                  f"to the bar, kick {r * 4}, guitars {r * 8}, toms {r * 12}, hat {r * 16}")
        print(f"end {sec(end)}  ({end // 4} bars)")
    else:
        with open(OUT, "w") as f:
            f.write(dump(doc))
