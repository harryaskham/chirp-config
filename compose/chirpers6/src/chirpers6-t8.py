#!/usr/bin/env python3
"""chirpers6-t8 (All the Lights Left On, track 8, the closer). Composed by chirper-two: HYMNAL POST-ROCK INTO
POST-METAL.

"Sign-off". The night ends: the mast's broadcast signs off, the lights go out one by one and the dawn comes up over the
plain. A hymn, a march, real weight, and the album's last and largest peak, earned over the whole length.

THE HYMN (H): E4 F#4 G#4 B4 | A4 G#4 F#4 . | C#4 E4 F#4 G#4 | B4 . A4 G#4 . (half notes, a turn at the end).
THE MAST'S THEME (T, from track 1): F#4 E4 D4 A3 B3, here in C# minor / E: G#4 F#4 E4 B3 C#4.
 I   SIGN-OFF     the radio's closing announcement ("This is the night service, signing off. Thank you for leaving
                  the lights on.") over the hymn on a music box and celesta heard through the radio; then the carrier.
 II  FIRST BIRDS  synthesised dawn birds and wind; a solo cello sings the hymn slow; chirp's PHYSICAL drum layer under
                  brushes (taps and sweeps), a fretless underneath.
 III PROCESSION   a march in 3/4: felt mallets on the toms and kick, then sticks on a wired snare; strings and an
                  arpeggiating guitar in threes; The Mast's theme returns on the second guitar, in C# minor.
 IV  WEIGHT       post-metal in 7/8 (2+2+3): a low 8-string riff, the physical kit hit hard (plastic beater, rimshots),
                  the hymn in the bass, a strong sub; a breath of eight clean bars, then the weight again, heavier.
 V   SUNRISE      the album's final peak in E major: the hymn on a tape-echo lead and a choir, The Mast's theme against
                  it on a second guitar and glockenspiel, a sextuplet tremolo wall, strings, the kit with crashes.
 VI  LIGHTS OUT   one by one every part stops, every four bars; the radio returns ("Good morning.") and is switched off
                  with a click; birds.
One tempo (96 bpm); the movements change their bar: 4/4, 3/4, 7/8, 4/4.

Emits songs/chirpers6-t8.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T8_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers6-t8.yaml")
BPM = 96
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
LVL_GAIN = float(os.environ.get("LVL_GAIN", "1"))


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if e[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - e[0]) < 1e-3:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


# Round 2 (v2): H = SLOWER HARMONY: the sunrise and the lights-out change chord every four bars (not two), and the
# weight's crash marks eight-bar phrases (not four), so the movements breathe in long phrases; P = THE PEAK IS EARNED:
# a beat of silence before the sunrise's last stage, and that stage lifts a semitone to F major (the hymn, the theme,
# the chords and the choir all rise with it); W = THE WEIGHT IS HEAVIER: the 8-string riff doubled (a second
# player, panned), a kick on every group of the 2+2+3, and the fader no longer holds it back; S = THE RADIO IN THE
# PROCESSION: a field report through the radio, "Clear skies by morning. The roads are open."
# C = CONTINUOUS LINES: the melodic voices no longer switch on and off every few bars (which cut the movements into
# ten-second shards): the hymn runs whole and unbroken in the weight's bass, The Mast's theme repeats as a cantus
# under the procession and as a near-continuous counterline against the hymn at the sunrise, and the sunrise's tremolo
# wall drones on the key (E, then F) while the strings and the bass move under it.
R2 = set(filter(None, os.environ.get("T8_R2", "H,P,W,S,C").split(","))) - {"none"}
SPEECH_REPORT = [["k-l-ih1-r", "s-k-ay1-z", "b-ay1", "m-ao1-r", "n-ih0-ng"], ["dh-ah0", "r-ow1-d-z", "aa1-r", "ow1", "p-ah0-n"]]
# (movement, bars, beats per bar)
FORM = [("signoff", 16, 4.0), ("birds", 32, 4.0), ("procession", 64, 3.0), ("weight", 48, 3.5),
        ("sunrise", 64, 4.0), ("lightsout", 40, 4.0)]
HYMN = [(64, 2), (66, 2), (68, 2), (71, 2), (69, 2), (68, 2), (66, 4), (61, 2), (64, 2), (66, 2), (68, 2),
        (71, 3), (69, 1), (68, 4)]  # 32 beats
T_CSM = [(68, 2.0), (66, 1.0), (64, 1.0), (59, 2.0), (61, 4.0)]  # The Mast's theme in C# minor / E
# chords (bass root, voicing)
CSM = [(37, [56, 61, 64, 68]), (33, [57, 61, 64, 69]), (40, [56, 59, 64, 68]), (35, [54, 59, 63, 66])]  # C#m A E B
EMAJ = [(40, [56, 59, 64, 68]), (39, [54, 59, 63, 66]), (37, [56, 61, 64, 68]), (33, [57, 61, 64, 69])]  # E B/D# C#m A
RIFF = [(0.0, 0.45, 25), (0.5, 0.45, 25), (1.0, 0.45, 37), (1.5, 0.45, 25), (2.0, 0.45, 32), (2.5, 0.45, 25),
        (3.0, 0.45, 30)]  # 7/8 in eighths, 2+2+3, on C#1 (25) with octave and fifth stabs
SPEECH_OFF = [["dh-ih1-s", "ih1-z", "dh-ah0", "n-ay1-t", "s-er1", "v-ih0-s"], ["s-ay1", "n-ih0-ng", "ao1-f"],
              ["th-ae1-ng-k", "y-uw1", "f-ao1-r", "l-iy1", "v-ih0-ng", "dh-ah0", "l-ay1-t-s", "aa1-n"]]
SPEECH_MORNING = [["g-uh1-d", "m-ao1-r", "n-ih0-ng"]]


def build():
    rng = random.Random(8)
    brng = random.Random(88)  # the birds' own dice
    names = ["riff2", "musicbox", "celesta", "cello", "fretless", "sub", "kit", "cym", "strings", "g1", "g2", "riff", "lead",
             "choir", "glock", "radio", "static", "carrier", "birds", "wind", "click"]
    Tr = {k: Track(k) for k in names}
    bars, pos = [], 0.0
    for name, n, bl in FORM:
        for i in range(n):
            bars.append((pos, name, i, n, bl))
            pos += bl
    total = pos

    def line(track, start, notes, scale=1.0, up=0, vel=80, art=""):
        t = start
        for m, d in notes:
            track.add(t, d * scale * 0.97, nm(m + up), vel, art)
            t += d * scale
        return t

    def speak(track, start, lines, slow=1.0, base="A2"):
        t = start
        for ln in lines:
            for k, syl in enumerate(ln):
                last = k == len(ln) - 1
                f0 = "0>-30>-90" if last else ("0>15>0" if k == 0 else "0>-10")
                track.add(t, 0.9 * slow, base, 86 - (6 if syl.endswith("0") else 0), f"^ph={syl}^f0={f0}")
                t += 1.0 * slow
            t += 2.0 * slow
        return t

    for bi, (start, sec, i, n, bl) in enumerate(bars):
        # ---------------- I SIGN-OFF ----------------
        if sec == "signoff":
            if i == 0:
                line(Tr["musicbox"], start + 2.0, HYMN, 1.0, 12, 70)
                line(Tr["celesta"], start + 2.0, HYMN, 1.0, 0, 54)
                speak(Tr["radio"], start + 4.0, SPEECH_OFF)
            if i == 12:
                Tr["carrier"].add(start, 16.0, "B5", 60)  # the test tone after the sign-off
        # ---------------- II FIRST BIRDS ----------------
        elif sec == "birds":
            root, voic = CSM[(i // 2) % 4]
            if i in (4, 20):
                line(Tr["cello"], start, HYMN, 2.0 if i == 4 else 1.0, -12, 76)  # the hymn, slow then in time
            if i % 2 == 0 and i >= 8:
                Tr["fretless"].add(start, 7.8, nm(root), 76)
            if i >= 8:  # brushes on the physical kit
                Tr["kit"].add(start, 3.9, "bs", 60)
                Tr["kit"].add(start, 0.5, "k", 70)
                for b in (1.0, 3.0):
                    Tr["kit"].add(start + b + 0.03, 0.3, "bt", 66 + rng.randint(-4, 4))
                for b in (0.5, 1.5, 2.5, 3.5):
                    Tr["kit"].add(start + b + 0.04, 0.25, "bt", 40 + rng.randint(-4, 6))
            if i >= 16 and i % 2 == 0:
                Tr["strings"].add(start, 7.8, ",".join(nm(x) for x in voic), 44 + i)
        # ---------------- III PROCESSION (3/4) ----------------
        elif sec == "procession":
            root, voic = CSM[(i // 4) % 4]
            sticks = i >= 16
            # the march: kick on 1, snare on 3 (felt mallets, then sticks), toms rolling into each phrase
            Tr["kit"].add(start, 0.5, "k", 86 if sticks else 76)
            Tr["kit"].add(start + 2.0, 0.5, "s" if sticks else "ms", 84 if sticks else 70)
            if sticks:
                Tr["kit"].add(start + 2.5, 0.25, "s", 54)
                Tr["cym"].add(start, 1.0, "rd", 70)
                Tr["cym"].add(start + 1.0, 1.0, "rd", 56)
                Tr["cym"].add(start + 2.0, 1.0, "rd", 60)
            else:
                Tr["kit"].add(start + 1.0, 0.5, "mt2", 60)
            if i % 8 == 7:
                for k, piece in enumerate(("mt1", "mt1", "mt2", "mt2", "mt2", "k")):
                    Tr["kit"].add(start + 0.5 * k, 0.5, piece if not sticks else {"mt1": "t1", "mt2": "t2"}.get(piece, piece),
                                  70 + 4 * k)
            arp = sorted(voic)
            for k in range(6):  # the guitar in threes: eighths up and down the chord
                Tr["g1"].add(start + 0.5 * k, 0.9, nm(arp[[0, 1, 2, 3, 2, 1][k]]), 58 + (8 if k == 0 else 0))
            if i % 4 == 0:
                Tr["fretless"].add(start, 11.8, nm(root), 84)
                Tr["strings"].add(start, 11.8, ",".join(nm(x) for x in voic), 60 + i // 2)
            if "C" in R2:
                if i >= 16 and (i - 16) % 5 == 0 and i + 5 <= n:  # the theme as a cantus, back to back
                    line(Tr["g2"], start, T_CSM, 1.5, 12, 72)
            elif i in (16, 32, 48):  # The Mast's theme returns, changed: in C# minor, in threes
                line(Tr["g2"], start, T_CSM, 1.5, 12, 76)
            if i in (24, 40):
                line(Tr["cello"], start, HYMN, 1.5, -12, 80)
            if "S" in R2 and i == 34:
                speak(Tr["radio"], start, SPEECH_REPORT)
        # ---------------- IV WEIGHT (7/8) ----------------
        elif sec == "weight":
            breath = 32 <= i < 40
            heavy = i >= 40
            root_c = 25  # C#1
            if breath:  # eight clean bars: the riff on a clean guitar, the hymn on the celesta
                for b, ln, m in RIFF:
                    Tr["g1"].add(start + b, ln, nm(m + 24), 80)
                if i == 32:
                    line(Tr["celesta"], start, HYMN, 0.875, 0, 84)
                continue
            for b, ln, m in RIFF:
                for rt in (("riff", "riff2") if "W" in R2 else ("riff",)):
                    Tr[rt].add(start + b + (0.006 if rt == "riff2" else 0.0), ln,
                               nm(m + 12) if m == 25 else ",".join((nm(m + 12), nm(m + 19))),
                               104 if b in (0.0, 1.0, 2.0) else 88, "^pm" if m == 25 and b not in (0.0,) else "")
            Tr["sub"].add(start, bl - 0.1, nm(root_c + 12), 100)
            # the physical kit, hit hard: plastic beater, rimshots on the 2+2+3's accents
            Tr["kit"].add(start, 0.5, "kp", 110)
            Tr["kit"].add(start + 2.0, 0.5, "kp", 100)
            if "W" in R2:
                Tr["kit"].add(start + 1.0 - 0.004, 0.5, "kp", 96)  # a kick on every group of the 2+2+3
            Tr["kit"].add(start + 1.0, 0.5, "rs", 112 if heavy else 104)
            Tr["kit"].add(start + 3.0, 0.5, "rs", 108 if heavy else 98)
            phrase = 8 if "H" in R2 else 4
            Tr["cym"].add(start, 1.0, "c" if i % phrase == 0 else "rd", 96 if i % phrase == 0 else 80)
            if heavy:
                Tr["cym"].add(start + 2.0, 1.0, "x", 90)
            if "C" in R2:
                if i % 8 == 0:  # the hymn whole and unbroken in the bass (32 beats over eight 7/8 bars)
                    line(Tr["fretless"], start, HYMN, 0.875, -24, 100, "")
            elif i % 8 == 0:  # the hymn in the bass, two bars a phrase
                line(Tr["fretless"], start, HYMN[:7], 0.875, -24, 100, "")
            if i % 2 == 0:
                Tr["strings"].add(start, 6.8, "C#3,G#3,C#4", 84 if heavy else 72)
        # ---------------- V SUNRISE ----------------
        elif sec == "sunrise":
            root, voic = EMAJ[((i // (8 if "C" in R2 else 4)) if "H" in R2 else (i // 2)) % 4]
            stage = 0 if i < 16 else (1 if i < 48 else 2)
            lift = 1 if ("P" in R2 and stage == 2) else 0  # the last stage, a semitone higher: F major
            root, voic = root + lift, [x + lift for x in voic]
            v = (70, 96, 112)[stage]
            # the hymn on the lead and the choir; The Mast's theme against it
            if i % 8 == 0:
                line(Tr["lead"], start, HYMN, 1.0, (0 if stage < 2 else 12) + lift, v)
                if stage >= 1:
                    line(Tr["choir"], start, HYMN, 1.0, -12 + lift, 90)
            if "C" in R2:
                if i % 8 == 0 and stage >= 1:  # the theme three times through each eight bars: a counterline
                    for k in range(3):
                        line(Tr["g2"], start + 2.0 + 10.0 * k, T_CSM, 1.0, 12 + lift, v - 6)
                        line(Tr["glock"], start + 2.0 + 10.0 * k, T_CSM, 1.0, 24 + lift, 72)
            elif i % 8 == 4 and stage >= 1:
                line(Tr["g2"], start + 2.0, T_CSM, 1.0, 12 + lift, v - 6)
                line(Tr["glock"], start + 2.0, T_CSM, 1.0, 24 + lift, 76)
            top = sorted(voic)[-3:]
            if "C" in R2:  # the wall drones on the key (root, fifth, octave) while the strings and the bass move
                top = [64 + lift, 71 + lift, 76 + lift]
            if stage >= 1:  # the wall
                for s in range(24):
                    Tr["g1"].add(start + s / 6, 1 / 6 * 0.95, nm(top[(s // 3) % 3] + 12), v - 10 + (8 if s % 6 == 0 else 0))
            else:
                for k in range(8):
                    Tr["g1"].add(start + 0.5 * k, 0.9, nm(sorted(voic)[[0, 1, 2, 3, 2, 1, 2, 3][k]]), 64)
            if i % 2 == 0:
                Tr["strings"].add(start, 7.8, ",".join(nm(x) for x in voic), v - 6)
                Tr["fretless"].add(start, 7.8, nm(root), v - 4)
            Tr["sub"].add(start, 3.9, nm(root - 12 if root >= 36 else root), v - 6)
            # the kit
            Tr["kit"].add(start, 0.5, "kp", v)
            Tr["kit"].add(start + 2.5 if stage else start + 2.0, 0.5, "kp", v - 10)
            Tr["kit"].add(start + 1.0, 0.5, "s" if stage < 2 else "rs", v)
            Tr["kit"].add(start + 3.0, 0.5, "s" if stage < 2 else "rs", v)
            if stage >= 1:
                if not ("H" in R2 and i % (8 if "C" in R2 else 4) != 0 and stage < 2):
                    Tr["cym"].add(start, 1.0, "c" if i % 2 == 0 else "c2", v - 4)
                for b in range(8):
                    Tr["cym"].add(start + 0.5 * b, 0.5, "rd", v - 24 + (8 if b % 2 == 0 else 0))
            else:
                for b in range(4):
                    Tr["cym"].add(start + b, 1.0, "rd", 66)
            if i % 16 == 15:
                for k, piece in enumerate(("t1", "t1", "t2", "t2", "t2", "t2", "kp", "kp")):
                    Tr["kit"].add(start + 2.0 + 0.25 * k, 0.25, piece, v - 6 + 2 * k)
        # ---------------- VI LIGHTS OUT ----------------
        elif sec == "lightsout":
            root, voic = EMAJ[((i // 4) if "H" in R2 else (i // 2)) % 4]
            if "P" in R2:  # the lights go out in F, the key the sunrise reached
                root, voic = root + 1, [x + 1 for x in voic]
            # each part leaves in turn: kit (4), wall (8), strings (12), lead and choir (16), bass (20), guitar (24),
            # then the hymn alone on the celesta, the radio, the click, the birds
            if i < 4:
                Tr["kit"].add(start, 0.5, "kp", 96 - 6 * i)
                Tr["kit"].add(start + 1.0, 0.5, "s", 86 - 6 * i)
                Tr["kit"].add(start + 3.0, 0.5, "s", 86 - 6 * i)
                Tr["cym"].add(start, 1.0, "c", 90 - 6 * i)
            if i < 8:
                for s in range(24):
                    Tr["g1"].add(start + s / 6, 1 / 6 * 0.95, nm(sorted(voic)[-3:][(s // 3) % 3] + 12), 90 - 6 * i)
            if i < 12 and i % 2 == 0:
                Tr["strings"].add(start, 7.8, ",".join(nm(x) for x in voic), 84 - 4 * i)
            if i in (0, 8):
                line(Tr["lead"], start, HYMN, 1.0, 1 if "P" in R2 else 0, 92 - 3 * i)
            if i < 20 and i % 2 == 0:
                Tr["fretless"].add(start, 7.8, nm(root), 80 - 2 * i)
            if 8 <= i < 24:
                for k in range(8):
                    Tr["g2"].add(start + 0.5 * k, 0.9, nm(sorted(voic)[[0, 1, 2, 3, 2, 1, 2, 3][k]] + 12), 66 - i)
            if i == 24:
                line(Tr["celesta"], start, HYMN, 1.0, 13 if "P" in R2 else 12, 60)
            if i == 30:
                speak(Tr["radio"], start, SPEECH_MORNING)
            if i == 33:
                Tr["click"].add(start, 0.2, "C4", 110)  # the radio switched off
        # ---------------- the field: static on the radio, birds at dawn, wind ----------------
        if sec in ("signoff",) or (sec == "lightsout" and 28 <= i < 33):
            for _ in range(rng.randint(10, 16)):
                Tr["static"].add(start + rng.uniform(0, bl - 0.03), 0.04, "C5", rng.randint(24, 70))
        dawn = sec in ("birds",) or (sec == "lightsout" and i >= 24) or (sec == "procession" and i < 8)
        if dawn:
            for _ in range(brng.randint(2, 7)):
                Tr["birds"].add(start + brng.uniform(0, bl - 0.2), 0.12, nm(brng.choice([86, 88, 90, 91, 93, 95])),
                                brng.randint(40, 90))
        if i % 8 == 0 and sec in ("signoff", "birds", "lightsout"):
            Tr["wind"].add(start, 8.0 * bl, "C4", 66)
    if "P" in R2:  # a beat of silence before the last stage of the sunrise
        sun = next(bb for bb in bars if bb[1] == "sunrise")[0]
        edge = sun + 48 * 4.0
        for tr in Tr.values():
            tr.ev = [e for e in tr.ev if not (edge - 1.0 - 1e-6 <= e[0] < edge)]
            tr.ev = [(s, min(ln, edge - 1.0 - s) if s < edge - 1.0 < s + ln else ln, h, vel, art)
                     for s, ln, h, vel, art in tr.ev]
    sec = []
    for name, n, bl in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, Tr


def patches():
    def drum(pitch, layer, amp, gain="0dB", filters=("hp cutoff=40",)):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [layer], "filters": list(filters),
                                                                    "amp": amp}, "play": {"vel_sens": 0.7}}}
    brush = dict(type="drum", beater="brush", decay="0.3s", sharp=20, reso=1.4, cavity=0.3, reso_level=0.5,
                 shell=0.3, shell_hz=470, wires=0.45, gap=0.25, wire_tone="5k", strike=0.35, damp=0.35, slap=0.6,
                 stereo=0.35)
    snare = dict(type="drum", beater="stick", decay="0.35s", sharp=25, reso=1.4, cavity=0.3, reso_level=0.5,
                 shell=0.4, shell_hz=480, wires=0.7, gap=0.2, wire_tone="5k", strike=0.4, damp=0.3, slap=1.0,
                 stereo=0.3)
    tom = dict(type="drum", beater="felt", decay="0.7s", sharp=30, reso=1.0, cavity=0.2, tune_sounding=True,
               reso_level=0.5, air=0.4, strike=0.3, damp=0.3, slap=0.3, stereo=0.4)
    kick = dict(type="drum", beater="felt", decay="0.55s", sharp=35, reso=1.0, cavity=0.25, reso_level=0.6,
                air=0.45, strike=0.2, damp=0.35, slap=0.25, stereo=0.15)
    env = lambda d: {"a": "0.5ms", "d": d, "s": 0, "r": "60ms", "curve": 2}
    kit = {"about": "chirper-two's dawn kit for Sign-off: chirp's physical drum layer, one kit's whole arc: brushes, "
                    "felt mallets, sticks on a wired snare, rimshots, a felt kick and a plastic-beater kick.",
           "extends": "room-kit",
           "kit": {
               "k": drum("C#1", kick, env("650ms"), "9dB", ("hp cutoff=28",)),
               "kp": drum("C#1", dict(kick, beater="plastic", decay="0.5s", slap=0.8), env("600ms"), "9dB",
                          ("hp cutoff=30",)),
               "bt": drum("E3", brush, env("600ms"), "0dB", ("hp cutoff=200",)),
               "bs": drum("E3", dict(brush, sweep="1.2s"), {"a": "30ms", "d": "1.5s", "s": 0, "r": "100ms", "curve": 1},
                          "-4dB", ("hp cutoff=150",)),
               "ms": drum("D3", dict(brush, beater="felt", contact=1.4, wires=0.5, decay="0.28s", slap=0.5),
                          env("500ms"), "0dB", ("hp cutoff=90",)),
               "s": drum("D3", snare, env("500ms"), "0dB", ("hp cutoff=100",)),
               "rs": drum("D3", dict(snare, beater="rimshot", shell=0.8), env("550ms"), "1dB", ("hp cutoff=100",)),
               "mt1": drum("A2", tom, env("800ms")),
               "mt2": drum("E2", dict(tom, decay="0.8s"), env("900ms")),
               "t1": drum("A2", dict(tom, beater="stick", slap=0.8), env("800ms")),
               "t2": drum("E2", dict(tom, beater="stick", slap=0.8, decay="0.8s"), env("900ms")),
           }}
    return {
        "c2-dawn-kit": kit,
        "c2-static": {"about": "chirper-two: shortwave static, a 4 ms noise tick band-passed like a radio.",
                      "synth": {"layers": [{"type": "noise"}], "filters": ["hp cutoff=900", "lp cutoff=4500"],
                                "amp": {"a": "0.2ms", "d": "4ms", "s": 0, "r": "3ms"}}, "play": {"vel_sens": 1.0}},
        "c2-wind": {"about": "chirper-two: wind, pink noise through a band-pass swept by the track's LFOs.",
                    "synth": {"layers": [{"type": "noise", "color": "pink"}],
                              "filters": [{"kind": "bp", "q": 2.0,
                                           "cutoff": {"value": 500, "mod": [{"src": "lfo.w", "amount": 1.3},
                                                                            {"src": "lfo.g", "amount": 0.4}]}}],
                              "amp": {"a": "5s", "d": "1s", "s": 0.9, "r": "6s"}}},
        "c2-bird": {"about": "chirper-two: a dawn bird: a short sine whose pitch flicks up then falls (a syrinx "
                             "chirp), a little vibrato, a second partial.",
                    "synth": {"layers": [{"wave": "sine"}, {"wave": "sine", "ratio": 2.0, "level": "-12dB"}],
                              "pitch": {"value": 0, "mod": [{"src": "env.flick", "amount": 7},
                                                            {"src": "lfo.tr", "amount": 0.6}]},
                              "env": {"flick": {"a": "15ms", "d": "70ms", "s": 0}},
                              "lfo": {"tr": {"wave": "sine", "rate": "28hz"}},
                              "amp": {"a": "4ms", "d": "90ms", "s": 0, "r": "30ms"}}, "play": {"vel_sens": 1.0}},
        "c2-carrier": {"about": "chirper-two: a broadcast test tone after sign-off, a pure sine.",
                       "synth": {"layers": [{"wave": "sine"}], "amp": {"a": "50ms", "d": "0s", "s": 1, "r": "1s"}}},
        "c2-click": {"about": "chirper-two: a radio switched off: a click and a short thump.",
                     "synth": {"layers": [{"type": "noise"}, {"wave": "sine", "fixed": 90}],
                               "filters": ["lp cutoff=5000"], "amp": {"a": "0.1ms", "d": "25ms", "s": 0, "r": "10ms"}},
                     "play": {"vel_sens": 1.0}},
        "c2-musicbox": {"about": "chirper-two: a music box: a plucked steel comb, bright partials, quick decay.",
                        "synth": {"layers": [{"type": "additive", "partials": [[1, 1], [3.0, 0.3], [5.4, 0.12]]}],
                                  "amp": {"a": "1ms", "d": "1.2s", "s": 0, "r": "300ms", "curve": 2}}},
    }


def main():
    total, bars, sec, Tr = build()
    st = {n: s for n, s, k in sec}
    # the fader ride: quiet start, the procession sits back, the weight is heavy but not the peak, the sunrise climbs
    dyn = [["0b", 0.0], [f"{st['procession']}b", -5.0], [f"{st['weight'] - 0.01}b", -2.0],
           [f"{st['weight']}b", 1.0 if "W" in R2 else 0.0],
           [f"{st['sunrise'] - 0.01}b", 0.0], [f"{st['sunrise']}b", -6.0], [f"{st['sunrise'] + 64}b", -3.0],
           [f"{st['sunrise'] + 192}b", 0.0], [f"{st['lightsout']}b", 0.0], [f"{total}b", 0.0]]
    pump = {"type": "pump", "on": "kit.kp", "depth": "-5dB", "attack": "3ms", "release": "380ms", "curve": 0.8}
    radio_fx = ["hp cutoff=320", "lp cutoff=3200", {"type": "crush", "bits": 10, "rate": 11000, "mix": 0.35},
                "drive drive=0.3", "reverb kind=room decay=0.8s mix=0.15"]
    tracks = [
        {"name": "radio", "patch": "voice-speech", "gain": "-4dB", "pan": -0.1, "fx": radio_fx,
         "score": Tr["radio"].score(total)},
        {"name": "musicbox", "patch": "c2-musicbox", "gain": "-10dB", "pan": 0.15,
         "fx": ["hp cutoff=400", "lp cutoff=3500", {"type": "crush", "bits": 11, "rate": 16000, "mix": 0.3},
                "reverb kind=room decay=1s mix=0.2"], "score": Tr["musicbox"].score(total)},
        {"name": "celesta", "patch": "celesta", "gain": "-9dB", "fx": ["reverb kind=hall decay=4s mix=0.35"],
         "score": Tr["celesta"].score(total)},
        {"name": "cello", "patch": "cello", "gain": "-6dB", "pan": -0.15, "score": Tr["cello"].score(total)},
        {"name": "fretless", "patch": "fretless", "gain": "-4dB", "fx": [pump, "drive drive=0.25"],
         "score": Tr["fretless"].score(total)},
        {"name": "sub", "patch": "sub-sine", "gain": "-8dB",
         "fx": [pump, {"type": "phantom", "cutoff": "110hz", "harmonics": "-8dB", "odd": 0.4}],
         "score": Tr["sub"].score(total)},
        {"name": "kit", "patch": "c2-dawn-kit", "gain": "-3dB", "fx": ["reverb kind=room decay=1.2s mix=0.2"],
         "score": Tr["kit"].score(total)},
        {"name": "cymbals", "patch": "rock-kit", "gain": "-5dB", "fx": ["reverb kind=room decay=1.3s mix=0.2"],
         "score": Tr["cym"].score(total)},
        {"name": "strings", "patch": "strings", "gain": "-12dB", "fx": ["hp cutoff=110"], "score": Tr["strings"].score(total)},
        {"name": "g1", "patch": "clean-chorus", "gain": "-9dB", "pan": -0.35,
         "fx": ["reverb kind=hall decay=3.5s mix=0.3"], "score": Tr["g1"].score(total)},
        {"name": "g2", "patch": "clean-chorus", "gain": "-10dB", "pan": 0.35,
         "fx": [{"type": "delay", "time": "3/8", "feedback": 0.4, "mix": 0.3, "ping_pong": True, "tone": 3000},
                "reverb kind=hall decay=4s mix=0.35"], "score": Tr["g2"].score(total)},
        {"name": "riff", "patch": "m8", "gain": "-10dB", **({"pan": -0.3} if "W" in R2 else {}), "fx": ["lp cutoff=5000"],
         "score": Tr["riff"].score(total)},
        *([{"name": "riff2", "patch": "m8", "gain": "-11dB", "pan": 0.3, "fx": ["lp cutoff=4500"],
            "score": Tr["riff2"].score(total)}] if "W" in R2 else []),
        {"name": "lead", "patch": "lead-tape", "gain": "-12dB", "pan": 0.1, "score": Tr["lead"].score(total)},
        {"name": "choir", "patch": "choir", "gain": "-10dB", "fx": ["reverb kind=hall decay=4s mix=0.3"],
         "score": Tr["choir"].score(total)},
        {"name": "glock", "patch": "glock", "gain": "-16dB", "pan": -0.2, "fx": ["reverb kind=hall decay=3s mix=0.35"],
         "score": Tr["glock"].score(total)},
        {"name": "static", "patch": "c2-static", "gain": "-22dB", "fx": ["width width=1.4"], "score": Tr["static"].score(total)},
        {"name": "carrier", "patch": "c2-carrier", "gain": "-30dB", "fx": ["hp cutoff=200"], "score": Tr["carrier"].score(total)},
        {"name": "birds", "patch": "c2-bird", "gain": "-20dB", "fx": ["width width=1.6", "reverb kind=hall decay=2.5s mix=0.35"],
         "score": Tr["birds"].score(total)},
        {"name": "wind", "patch": "c2-wind", "gain": "-18dB", "fx": ["width width=1.6"],
         "lfo": {"w": "sine rate=7/1", "g": "sine rate=1/1 phase=0.3"}, "score": Tr["wind"].score(total)},
        {"name": "click", "patch": "c2-click", "gain": "-8dB", "score": Tr["click"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - All the Lights Left On, track 8 (the closer). Original composition by chirper-two, generated "
             "by compose/chirpers6/src/chirpers6-t8.py. Hymnal post-rock into post-metal at 96 bpm: the mast's "
             "broadcast signs off, the dawn comes up: Sign-off, First Birds, Procession (3/4), Weight (7/8), Sunrise "
             f"(the album's final peak, E major) and Lights Out. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "All the Lights Left On", "title": "Sign-off",
                               "track": 8, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "3s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "true_peak: true",
        "patches: " + json.dumps(patches()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=400 gain=-4dB q=0.6",
                                                               "highshelf cutoff=4500 gain=4dB"]},
                                        "glue threshold=-20dB ratio=1.8 attack=20ms release=200ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": f"{LVL_GAIN:g}dB",
                                                                  "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "100ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
