#!/usr/bin/env python3
"""chirpers10-t3 "Plain Hunt" (chirper-zero): one row of six notes, rung in every order.

English church bells cannot play tunes: a bell swings full circle and can only be made to strike a little sooner or a
little later. So ringers ring CHANGES: the bells strike once each, in a row, and from one row to the next a bell may
only swap places with its neighbour. A method is a rule for the swaps that visits every possible order exactly once and
comes back to where it started ("rounds", the bells running down the scale). On five bells that is 120 rows, an EXTENT,
and until the last row nothing is ever heard twice.

Common Time (track 1) turns three cells of different lengths under one pulse; Odd Sympathy (track 2) slides one riff
against itself. This piece's long cycle is an ORDER: the riff is a row of six sixteenths, five notes that change places
by the ringers' rule and a low F that always comes last ("the tenor behind"), and it is rung through two extents, 240
rows, no two alike within either, each ending where it began. Six sixteenths against four beats also turn: the row and
the bar line meet every third bar.

  the row     bells 1 2 3 4 5 (6) = Eb C B Ab Gb (F): the album's hook notes, running down. Rounds is that scale.
  the hunt    bell 1 (the treble, the highest note) "plain hunts": its place in the row walks 1 2 3 4 5 5 4 3 2 1 and
              round again, all piece long. It is played open and loud, the kick goes with it, and a church bell doubles
              it: an accent that slides later and later through the riff, then earlier and earlier.
  the methods Plain Bob Doubles (called plain plain plain bob, three times) and Grandsire Doubles (plain bob plain bob
              plain single, twice): each is checked below to be a true extent.

v1 is the SKELETON (Harry, 14 Nov: "answered clips. unlock a third track slot!"; track 2's terms): the whole shape
standing, bare.
"""
import json
import os

OUT = os.environ.get("C10T3_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t3.yaml"))
BPM = 96
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# ---------------------------------------------------------------------------------------------------- the ringing
ROUNDS = (1, 2, 3, 4, 5)
PITCH = {1: 10, 2: 7, 3: 6, 4: 3, 5: 1, 6: 0}        # semitones above the ground: Eb C B Ab Gb, and the tenor F


def change(row, places):
    """One change: the bells in `places` (1-indexed) stay where they are; every other pair of neighbours swaps."""
    r, i = list(row), 0
    while i < len(r):
        if i + 1 in places:
            i += 1
        else:
            r[i], r[i + 1] = r[i + 1], r[i]
            i += 2
    return tuple(r)


def notation(s):
    return [set(int(c) for c in x) for x in s.split(".")]


PLAIN_BOB = {"p": notation("5.1.5.1.5.1.5.1.5.125"), "b": notation("5.1.5.1.5.1.5.1.5.145")}
GRANDSIRE = {"p": notation("3.1.5.1.5.1.5.1.5.1"), "b": notation("3.1.5.1.5.1.5.1.3.1"), "s": notation("3.1.5.1.5.1.5.1.3.123")}


def ring(method, calls):
    """The rows a touch produces, one lead (ten rows) to each call, starting from rounds (which is not itself rung)."""
    rows, r = [], ROUNDS
    for c in calls:
        for places in method[c]:
            r = change(r, places)
            rows.append(r)
    assert len(rows) == 120 and len(set(rows)) == 120 and rows[-1] == ROUNDS, "not a true extent"
    return rows


EXTENT_1 = ring(PLAIN_BOB, "pppb" * 3)
EXTENT_2 = ring(GRANDSIRE, "pbpbps" * 2)

# ---------------------------------------------------------------------------------------------------- the form (bars)
INTRO, BAND, PART1, MIDDLE, PART2, LAND, END, NB = 0, 4, 10, 55, 63, 108, 117, 120
KEYS_1 = (0, 3, 6)        # the ground of each third of the first extent: F, Ab, B
KEYS_2 = (0, 3, 7)        # and of the second: F, Ab, C (so the landing on F is a fall of a fifth)
G4 = ("gl", "gr", "gl2", "gr2")
BELL_LAND = float(os.environ.get("C10T3_BELLLAND", "-5"))
KICK_ALL = float(os.environ.get("C10T3_KICKALL", "-3"))
CYM_BUSY = float(os.environ.get("C10T3_CYMBUSY", "-3"))
# v2: THE TOWER GETS ITS VOICES AND A GONG (palette round). Where the bells ring alone (the opening, the middle, the
# end) they rang over a bowed drone and a synth pad: `contrabass-tight` and `juno-pad`, which all three songs of the
# album use. Both leave this song. Under the bells there is now a CHANT: two low men's voices a fifth apart (F and C),
# the library's `fof-chant` (Rodet's CHANT bass, one grain per formant per period, no filters, the mouth moving slowly
# between "o" and "u"), which no other track on the album uses and whose source (`fof`) the album had not used. And a
# GONG (`modal-gong`, a tam-tam on the modal layer) is struck twice: when the first extent comes round (2:17) and on
# the last chord (4:52).
# The CHANT voice has no weight of its own (its sound is its mouth's resonance, 250-500 Hz; nothing under 120 Hz), so
# a floor goes under it where the bowed bass was: a BASS TAGELHARPA (`tagelharpa-bass`, a bowed horsehair lyre, coarse
# and beating), on the low F. It too is new to the album.
# the chant's patch ; its gain ; its hall send ; the gong's patch ; its gain ; its note ; the floor's patch ; its gain.
# "" = v1 (the drone and the pad).
TOWER = os.environ.get("C10T3_TOWER", "fof-chant;-15.5dB;-6dB;modal-gong;-13dB;F1;tagelharpa-bass;-21dB")
# v3: THE SECOND EXTENT STARTS ON THE BASS, AND THE BASS HAS TEETH (palette round). Until now nothing but the drums'
# pattern told the second extent from the first. Now its bass is two basses: the album's `ct-bass`, which keeps the
# weight, and over it the library's `bass-fuzz` (a bass string through a FOLDING fuzz; here the fold is the engine's
# `wavefold`, which the album had not used), high-passed so that only its teeth are added: 1-4 kHz, where ct-bass
# has little. No other track on the album uses it. And the extent opens on it: for its first eight rows (three bars,
# until the row and the bar line meet again) the guitars rest and the bass, the kick, the snare and the bell carry
# the row; then the four guitars come in on the crash.
# the patch string ; its gain ; its high-pass, Hz ; rows the guitars rest at the start ; its gain in those rows, dB over. "" = v2.
FUZZ = os.environ.get("C10T3_FUZZ", "bass-fuzz fx.0.shape=wavefold;4dB;180;8;4")


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "g": "snare", "h": "hat", "c": "cym", "x": "cym", "rb": "ride", "rd": "ride"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece in ("h", "rb", "rd") else 0.25, "pitch": piece, "vel": round(vel, 3)})


def row_notes(row, s16, root, kicks="hunt", bell=True, gtrs=True, teeth=False):
    """One row on the band, six sixteenths from `s16`: the five bells in the row's order, then the tenor. Every note a
    muted chug but the treble, which is open and loud; the kick goes with the treble and the tenor (`all`: with every
    note); a church bell doubles the treble three octaves up."""
    for i, b in enumerate(tuple(row) + (6,)):
        t = s16 + i
        for tr in (G4 if gtrs else ()):
            if b == 1:
                add(tr, t, 1, F1 + root + PITCH[b], 1.0)
            else:
                add(tr, t, 1, F1 + root + PITCH[b], 0.95 if b == 6 else 0.85, pm=1)
        for tr in (("bass", "fuzz") if teeth else ("bass",)):
            add(tr, t, 1, F1 + root + PITCH[b], 0.95 if b in (1, 6) else 0.85)
        if kicks == "all" or b in (1, 6):
            drum("k", t, 0.95 if b in (1, 6) else 0.62)
        if bell and b == 1:
            T.setdefault("bell", []).append({"at": round(t / 4, 4), "len": 1.5, "pitch": nm(F1 + root + PITCH[1] + 36), "vel": 0.6})


def slow_rounds(b0, rows, root=0, vel=0.8):
    """The bells alone, ringing rounds: a row every three beats (eighth notes), the tenor a little harder."""
    for r in range(rows):
        for i in range(6):
            T.setdefault("bell", []).append({"at": b0 * 4 + (r * 6 + i) * 0.5, "len": 3.0, "pitch": nm(F1 + root + PITCH[i + 1] + 36), "vel": round(min(1.0, vel * (1.12 if i == 5 else 1.0)), 3)})


def chant(at, beats):
    """Two low voices a fifth apart, held."""
    for p, v in (("F2", 0.6), ("C3", 0.5)):
        T.setdefault("chant", []).append({"at": at, "len": beats, "pitch": p, "vel": v})
    T.setdefault("drone", []).append({"at": at, "len": beats, "pitch": "F1", "vel": 0.5})


def gong(at, vel):
    T.setdefault("gong", []).append({"at": at, "len": 12.0, "pitch": TOWER.split(";")[5], "vel": vel})


def beat(b0, b1, kind):
    """The kit over a stretch (the kick is written with the rows). a: half time, the snare on three, china on the
    quarters. b: the backbeat, the hat in eighths. c: the backbeat, china in eighths."""
    for b in range(b0, b1):
        for p in ((8,) if kind == "a" else (4, 12)):
            drum("s", b * 16 + p, 0.95)
        if kind == "b":
            for p in range(0, 16, 2):
                drum("h", b * 16 + p, 0.62 if p % 4 == 0 else 0.48)
        else:
            for p in range(0, 16, 4 if kind == "a" else 2):
                drum("x", b * 16 + p, (0.6 if p == 0 else 0.5) if kind == "a" else (0.52 if p % 4 == 0 else 0.42))
        if (b - b0) % 3 == 0:                # where the row and the bar line meet
            drum("c", b * 16, 0.9 if b == b0 else 0.7)


def fill(b):
    """The last half bar before bar `b`."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, b * 16 - 8 + i, 0.6 + 0.045 * i)


def hit(b, beats, root=0):
    """One chord from the whole band, left to ring."""
    for tr in G4:
        add(tr, b * 16, beats * 4, ",".join(nm(F1 + root + i) for i in (0, 7, 12, 19)), 0.95)
    add("bass", b * 16, beats * 4, F1 + root, 0.95)
    drum("k", b * 16, 0.95)
    drum("c", b * 16, 0.95)


def compose():
    # the bells alone: rounds, slowly, five times; a drone under them. No band.
    slow_rounds(INTRO, 5)
    if TOWER:
        chant(0, 15.5)
    else:
        T.setdefault("home", []).append({"at": 0, "len": 15.5, "pitch": "F1", "vel": 0.5})
    # the band takes the row up at twice the speed: rounds, sixteen times, the row turning against the bar
    for r in range(16):
        row_notes(ROUNDS, BAND * 16 + r * 6, 0)
    beat(BAND, PART1, "a")
    fill(PART1)
    # the first extent: Plain Bob Doubles. Forty rows (fifteen bars) on F, forty on Ab, forty on B
    for k, row in enumerate(EXTENT_1):
        row_notes(row, PART1 * 16 + k * 6, KEYS_1[k // 40], kicks="all" if k >= 80 else "hunt")
    for i, kind in enumerate("abc"):
        beat(PART1 + 15 * i, PART1 + 15 * (i + 1), kind)
        fill(PART1 + 15 * (i + 1))
    # it has come round. One chord, and the bells alone again: rounds, slowly, over a drone and a pad
    hit(MIDDLE, 6)
    slow_rounds(MIDDLE + 1, 9)
    if TOWER:
        gong(MIDDLE * 4, 0.9)
        chant(MIDDLE * 4 + 2, 29.5)
    else:
        T.setdefault("home", []).append({"at": MIDDLE * 4, "len": 31.5, "pitch": "F1", "vel": 0.5})
        for p in ("F2", "C3"):
            T.setdefault("air", []).append({"at": (MIDDLE + 1) * 4, "len": 27.5, "pitch": p, "vel": 0.45})
    fill(PART2)
    # the second extent: Grandsire Doubles, on F, Ab and C
    for k, row in enumerate(EXTENT_2):
        row_notes(row, PART2 * 16 + k * 6, KEYS_2[k // 40], kicks="all" if k >= 80 else "hunt",
                  gtrs=not FUZZ or k >= int(FUZZ.split(";")[3]), teeth=bool(FUZZ))
    for i, kind in enumerate("bac"):
        beat(PART2 + 15 * i, PART2 + 15 * (i + 1), kind)
        fill(PART2 + 15 * (i + 1))
    # the landing: rounds on F, twenty-four times, and the bells ring rounds over the band at half its speed
    for r in range(24):
        row_notes(ROUNDS, LAND * 16 + r * 6, 0, bell=False)
    beat(LAND, END, "c")
    slow_rounds(LAND, 12, vel=0.9)
    # the end: one chord, and the tenor tolls
    hit(END, 10)
    if TOWER:
        gong(END * 4, 1.0)
        chant(END * 4 + 2, 9.5)
    for i, v in enumerate((0.9, 0.7, 0.5)):
        T.setdefault("bell", []).append({"at": (END + i) * 4, "len": 4.0, "pitch": nm(F1 + 36), "vel": v})


def song():
    compose()
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    dtop = ["lp cutoff=14250 q=0.8"]
    main = "ct-twin fx.1.model='5150' fx.2.mic=0.5 fx.2.cone={}"            # the takes it had: a 5150
    dbl = "ct-twin fx.1.model='nolly' fx.2.mic=0.35 fx.2.cone={}"           # a second take a side through another amp, microphone and cone
    GM, GD = os.environ.get("C10T3_GMAIN", "-0.7dB"), os.environ.get("C10T3_GDBL", "-1.5dB")        # each pair as loud as the other, alone; the four as loud as Odd Sympathy's two
    tracks = [
        {"name": "gl", "patch": main.format(10), "gain": GM, "pan": -1, "out": "gtrs"},
        {"name": "gr", "patch": main.format(11), "gain": GM, "pan": 1, "out": "gtrs"},
        {"name": "gl2", "patch": dbl.format(16), "gain": GD, "pan": -0.75, "out": "gtrs"},
        {"name": "gr2", "patch": dbl.format(17), "gain": GD, "pan": 0.75, "out": "gtrs"},
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        # the kick's fader: down where it plays every sixteenth (the last third of each extent)
        *([{"name": "fuzz", "patch": FUZZ.split(";")[0], "gain": {"value": FUZZ.split(";")[1], "mod": [{"src": "auto.open", "amount": 1}]}, "pan": 0,
            "fx": [{"type": "eq", "bands": [f"hp cutoff={FUZZ.split(';')[2]}"]}],
            "auto": {"open": {"points": [["0b", float(FUZZ.split(";")[4])], [f"{PART2 * 4 + int(FUZZ.split(';')[3]) * 1.5 - 0.5:g}b", float(FUZZ.split(";")[4])],
                                         [f"{PART2 * 4 + int(FUZZ.split(';')[3]) * 1.5:g}b", 0]], "curve": 0}}}] if FUZZ else []),
        {"name": "kick", "patch": kit, "gain": {"value": "2dB", "mod": [{"src": "auto.all", "amount": 1}]}, "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}],
         "auto": {"all": {"points": [["0b", 0]] + [pt for b0 in (PART1 + 30, PART2 + 30) for pt in ([f"{b0 * 4 - 0.5}b", 0], [f"{b0 * 4}b", KICK_ALL], [f"{(b0 + 15) * 4 - 0.5}b", KICK_ALL], [f"{(b0 + 15) * 4}b", 0])], "curve": 0}}},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        # the cymbals' fader: down where the china plays eighths (the last third of each extent, and the landing)
        {"name": "cym", "patch": kit, "gain": {"value": "-4.5dB", "mod": [{"src": "auto.busy", "amount": 1}]}, "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air,
         "auto": {"busy": {"points": [["0b", 0]] + [pt for b0, b1 in ((PART1 + 30, PART1 + 45), (PART2 + 30, END)) for pt in ([f"{b0 * 4 - 0.5}b", 0], [f"{b0 * 4}b", CYM_BUSY], [f"{b1 * 4 - 0.5}b", CYM_BUSY], [f"{b1 * 4}b", 0])], "curve": 0}}},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        # the bells' fader: down in the landing, where twelve slow rows of six ring into one another over the full band
        {"name": "bell", "patch": "modal-bell", "gain": {"value": os.environ.get("C10T3_BELL", "-18dB"), "mod": [{"src": "auto.lvl", "amount": 1}]}, "pan": 0.1, "sends": {"hall": "-8dB"},
         "auto": {"lvl": {"points": [["0b", 0], [f"{LAND * 4 - 1}b", 0], [f"{LAND * 4}b", BELL_LAND], [f"{END * 4 - 1}b", BELL_LAND], [f"{END * 4}b", 0]], "curve": 0}}},
        *([{"name": "chant", "patch": TOWER.split(";")[0], "gain": TOWER.split(";")[1], "pan": -0.1, "sends": {"hall": TOWER.split(";")[2]}},
           {"name": "gong", "patch": TOWER.split(";")[3], "gain": TOWER.split(";")[4], "pan": 0.2, "sends": {"hall": "-8dB"}},
           {"name": "drone", "patch": TOWER.split(";")[6], "gain": TOWER.split(";")[7], "pan": 0.2, "sends": {"hall": "-12dB"}}] if TOWER else
          [{"name": "home", "patch": "contrabass-tight", "gain": "-9dB", "pan": 0.3, "sends": {"hall": "-12dB"}},
           {"name": "air", "patch": "juno-pad", "gain": "-13dB", "pan": 0.15, "sends": {"hall": "-8dB"}}]),
    ]
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])
    return {
        "about": ("chirpers X (Common Time), track 3 by chirper-zero: \"Plain Hunt\". One row of six sixteenths (Eb C B Ab Gb and a low F "
                  "that always comes last) rung in every order by the bell-ringers' rule that a note may only swap places with its "
                  "neighbour: two extents, 240 rows, none repeated within either, each coming back to the scale it began on. The "
                  "highest note walks through the row and back all piece long, with the kick and a church bell on it. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}}},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB"] + dtop}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": dtop}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            "low": {"fx": [{"type": "eq", "bands": ["peak cutoff=44 q=1.5 gain=-7dB", "peak cutoff=90 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": ["peak cutoff=170 q=1.2 gain=-3dB"]}]},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T3_MASTER", "3.1dB")}]},
        "tracks": tracks,
    }


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
    open(OUT, "w").write(dump(song()))
