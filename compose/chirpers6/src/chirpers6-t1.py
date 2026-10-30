#!/usr/bin/env python3
"""chirpers6-t1 (All the Lights Left On, track 1, the opener). Composed by chirper-two: CRESCENDO POST-ROCK.

"The Mast". The album's door at night: a radio voice from the mast's night service, a five-note theme that is never
played the same way twice, and one long earned climb from wind and static to a wall of guitars, and back to a piano
left on.

THE THEME (T): F#4 E4 D4 A3 B3, falling and lifting. It is transformed in every movement:
 I   CARRIER    one clean guitar, slow, deep in delay, over wind and radio static; the night service announces itself.
 II  BRUSHES    the brush kit, a fretless bass, an arpeggiating guitar; a second guitar answers with T in eighths,
                warm in D (Dmaj9 A6 Bm9 Gmaj7#11).
 III SNOWFALL   the drums leave; a celesta plays T at half speed over a cello; the radio again with new words; the wind
                rises.
 IV  CLIMB      T in triplets (a 12/8 feel inside 4/4); tremolo guitars whose drive opens bar by bar; toms under
                mallets, then sticks, then the full kit; a string section swelling; a violin counter-melody.
 V   THE LIGHTS the peak, a tone higher (in E, the key lifting on its first downbeat): a crash-ride wash, a driven guitar wall and an 8-string power chord under it, T in long
                values on a tape-echo lead with a glockenspiel above, a strong sub pumped by the kick.
 VI  STILL ON   a sudden quiet: a piano, the static, the radio voice slowed and lowered; T's first three notes, and no
                ending.
Speech: chirp's voice engine speaking ARPAbet phonemes, one syllable a beat, through a radio's band-pass, crush and
static. Field textures: wind (noise through a band-pass swept by a 7-bar LFO), shortwave static and a tuning whistle.

Emits songs/chirpers6-t1.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T1_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers6-t1.yaml")
BPM = 140
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
LVL_GAIN = float(os.environ.get("LVL_GAIN", "0"))


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


# movements, in bars of 4/4 at 140 bpm
FORM = [("carrier", 48), ("brushes", 64), ("snowfall", 32), ("climb", 64), ("climb-e", 24), ("lights", 56),
        ("still", 40)]
T = [(66, 2.0), (64, 1.0), (62, 1.0), (57, 2.0), (59, 4.0)]  # the theme: F#4 E4 D4 A3 B3 (beats)
# chords: (bass root, voicing)
BRUSH = [(38, [50, 57, 61, 64, 66]), (33, [52, 57, 61, 66]), (35, [50, 54, 57, 61]), (31, [50, 54, 59, 61])]
BRUSH_B = [(35, [50, 54, 57, 61, 64]), (31, [50, 54, 59, 62]), (30, [50, 54, 57, 62]), (28, [50, 55, 59, 62, 66])]
CLIMB_B = [(31, [50, 55, 59, 62]), (38, [50, 54, 57, 62]), (33, [52, 57, 61, 64]), (35, [50, 54, 59, 62])]
VIOLIN = [(78, 4.0), (76, 2.0), (74, 2.0), (73, 4.0), (71, 4.0), (69, 4.0), (71, 4.0), (74, 8.0)]  # F#5 E5 D5 C#5 B4 A4 B4 D5
SNOW = [(31, [55, 59, 62, 66]), (28, [55, 59, 62, 66, 67]), (35, [50, 54, 57, 61]), (33, [54, 57, 61, 64])]
CLIMB = [(35, [50, 54, 59, 62]), (31, [50, 55, 59, 62]), (38, [50, 54, 57, 62]), (33, [52, 57, 61, 64])]
CLIMB_E = [(37, [52, 56, 61, 64]), (33, [52, 57, 61, 64]), (40, [52, 56, 59, 64]), (35, [51, 54, 59, 63])]
LIGHTS = [(40, [52, 56, 59, 64]), (35, [51, 54, 59, 63]), (37, [52, 56, 61, 64]), (33, [52, 57, 61, 64])]
STILL = [(38, [50, 57, 61, 64, 66]), (31, [50, 54, 59, 62])]
# the radio: (bar offset, [(syllable phonemes, f0 path)]) - one syllable a beat
SPEECH_1 = [["dh-ih1-s", "ih1-z", "dh-ah0", "n-ay1-t", "s-er1", "v-ih0-s"],
            ["ao1-l", "dh-ah0", "l-ay1-t-s", "aa1-r", "l-eh1-f-t", "aa1-n"],
            ["k-iy1-p", "y-ao1-r", "r-ey1", "d-iy0", "ow0", "aa1-n"]]
SPEECH_2 = [["s-n-ow1", "aa1-n", "dh-ah0", "l-ay1-n"], ["w-iy1", "aa1-r", "s-t-ih1-l", "hh-iy1-r"]]
SPEECH_3 = [["ao1-l", "dh-ah0", "l-ay1-t-s", "aa1-r", "l-eh1-f-t", "aa1-n"]]


def build():
    rng = random.Random(1)
    wrng = random.Random(11)
    names = ["g1", "g2", "lead", "wall", "bass", "sub", "brush", "kit", "strings", "violin", "cello", "celesta",
             "glock", "piano", "radio", "radio2", "static", "whistle", "wind"]
    Tr = {k: Track(k) for k in names}
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos

    def theme(track, start, scale=1.0, up=0, vel=80, art=""):
        t = start
        for m, d in T:
            track.add(t, d * scale * 0.98, nm(m + up), vel, art)
            t += d * scale

    def speak(track, start, lines, slow=1.0, base="A2"):
        t = start
        for line in lines:
            for k, syl in enumerate(line):
                last = k == len(line) - 1
                f0 = "0>-30>-90" if last else ("0>15>0" if k == 0 else "0>-10")
                track.add(t, 0.9 * slow, base, 86 - (6 if syl.endswith("0") else 0), f"^ph={syl}^f0={f0}")
                t += 1.0 * slow
            t += 2.0 * slow  # a breath between lines
        return t

    for bi, (start, sec, i, n) in enumerate(bars):
        # ---------------- I CARRIER ----------------
        if sec == "carrier":
            if i >= 8 and i % 8 == 0:
                theme(Tr["g1"], start, 1.0, 0, 62 + i // 2)
            if i == 4:
                speak(Tr["radio"], start, SPEECH_1)
            if i in (2, 30):
                Tr["whistle"].add(start, 6.0, "C5", 70)
        # ---------------- II BRUSHES ----------------
        elif sec == "brushes":
            phase = 0 if i < 24 else (1 if i < 48 else 2)  # the arpeggio / the answer, on new chords / the thinning
            root, voic = (BRUSH if phase != 1 else BRUSH_B)[(i // 2) % 4]
            if i % 2 == 0:
                Tr["bass"].add(start, 3.8, nm(root), 84)
                Tr["bass"].add(start + 4.0, 3.8, nm(root + (7 if i % 4 == 0 else 0)), 76)
            arp = sorted(voic)
            for k in (range(8) if phase < 2 else range(0, 8, 2)):  # an arpeggio in eighths (quarters as it thins)
                idx = [0, 1, 2, 3, 2, 1, 2, 3][k] % len(arp)
                Tr["g1"].add(start + 0.5 * k, 0.9, nm(arp[idx]), 58 + (8 if k == 0 else 0) + rng.randint(-4, 4))
            if phase == 1 and i % 8 == 4:  # the second guitar answers with T in eighths
                t0 = start + 1.0
                for k, (m, d) in enumerate(T):
                    Tr["g2"].add(t0 + 0.5 * k, 0.5 if k < 4 else 2.0, nm(m + 12), 72)
            if i >= 4 and phase < 2:  # brushes, half time
                Tr["brush"].add(start, 0.5, "k", 84)
                Tr["brush"].add(start + 2.0, 0.5, "sl", 80)
                Tr["brush"].add(start, 3.9, "sw", 56)
                for b in (0.5, 1.5, 2.5, 3.5):
                    Tr["brush"].add(start + b + 0.02, 0.3, "s", 44 + rng.randint(-4, 6))
                for b in (0.0, 1.0, 2.0, 3.0):
                    Tr["brush"].add(start + b, 0.5, "rd", 58 + (8 if b == 0 else 0))
            if phase == 2:  # the thinning: one sweep a bar, the ride's bell
                Tr["brush"].add(start, 3.9, "sp", 50)
                if i % 2 == 0:
                    Tr["brush"].add(start + 3.0, 0.5, "rb", 50)
            if i == 52:
                speak(Tr["radio"], start, [SPEECH_1[1]])  # the lights, once more, as the band thins
        # ---------------- III SNOWFALL ----------------
        elif sec == "snowfall":
            root, voic = SNOW[(i // 4) % 4]
            if i % 4 == 0:
                Tr["cello"].add(start, 15.8, nm(root + 12 if root < 36 else root), 70)
                Tr["strings"].add(start, 15.8, ",".join(nm(x) for x in voic[1:]), 40)
            if i in (0, 16):
                theme(Tr["celesta"], start + 2.0, 2.0, 12, 70)  # T at half speed, up an octave
            if i == 6:
                speak(Tr["radio"], start, SPEECH_2)
            if i == 24:
                Tr["whistle"].add(start, 8.0, "C5", 76)
        # ---------------- IV CLIMB ----------------
        elif sec in ("climb", "climb-e"):
            e = sec == "climb-e"
            ci = i if not e else i + 64
            cphase = 3 if e else (0 if i < 24 else (1 if i < 48 else 2))
            # the climb stays in D to its last bar: the key lifts a tone ON the peak's first downbeat, with the lead's
            # feedback swell on B (the dominant of E) holding the door open
            root, voic = (CLIMB if e else (CLIMB_B if cphase == 1 else CLIMB))[(i // 2) % 4]
            up = 0
            prog = ci / 88.0  # 0 -> 1 over the climb
            if cphase == 1 and i % 16 == 0:  # a violin counter-melody, the theme's shape inverted and stretched
                t0 = start
                for m, d in VIOLIN:
                    Tr["violin"].add(t0, d * 0.98, nm(m), 70 + int(20 * prog))
                    t0 += d
            # the bass drives eighths; the sub on the roots
            for k in range(8):
                Tr["bass"].add(start + 0.5 * k, 0.45, nm(root), 70 + int(30 * prog) - (8 if k % 2 else 0))
            if ci >= 48:
                Tr["sub"].add(start, 3.9, nm(root - 12 if root >= 36 else root), 80 + int(20 * prog))
            # tremolo guitars on the top two chord tones, sixteenths, louder as it climbs
            top = sorted(voic)[-2:]
            for s in range(16):
                m = top[(s // 4) % 2] + 12
                Tr["g1"].add(start + 0.25 * s, 0.24, nm(m), 50 + int(50 * prog) + (6 if s % 4 == 0 else 0))
            # T in triplets on the second guitar: each beat three notes of the theme's cycle
            if ci >= 8:
                seq = [m for m, d in T]
                for b in range(4):
                    for k in range(3):
                        m = seq[(b * 3 + k) % 5] + up
                        Tr["g2"].add(start + b + k / 3, 1 / 3, nm(m + 12), 58 + int(36 * prog))
            # strings swell each two bars
            if i % 2 == 0:
                Tr["strings"].add(start, 7.8, ",".join(nm(x) for x in voic), 46 + int(50 * prog))
            # drums: toms under mallets, then sticks, then the full kit (12/8 feel)
            if ci < 24:
                for b in range(4):
                    Tr["kit"].add(start + b, 0.5, "ft", 40 + ci + (8 if b == 0 else 0))
                    Tr["kit"].add(start + b + 2 / 3, 0.3, "t1", 30 + ci)
            elif ci < 48:
                Tr["kit"].add(start, 0.5, "k", 80)
                Tr["kit"].add(start + 2.0, 0.5, "k", 72)
                for b in range(4):
                    for k in range(3):
                        Tr["kit"].add(start + b + k / 3, 0.2, "g" if k else "rd", 40 + (ci - 24) * 2 + (10 if k == 0 else 0))
            else:
                Tr["kit"].add(start, 0.5, "k", 100)
                Tr["kit"].add(start + 2.0 + 2 / 3, 0.5, "k", 88)
                Tr["kit"].add(start + 2.0, 0.5, "s", 96 + int(20 * prog))
                for b in range(4):
                    for k in range(3):
                        Tr["kit"].add(start + b + k / 3, 0.3, "rd", 60 + (14 if k == 0 else 0) + rng.randint(-4, 4))
                if i % 4 == 0:
                    Tr["kit"].add(start, 1.0, "c", 100)
            if e and i >= n - 4:  # the last four bars: a snare roll rising into the light
                k, step = 0, 0.25 if i < n - 2 else 1 / 6
                while k * step < 4.0 - 1e-6:
                    Tr["kit"].add(start + k * step, step, "s", 70 + int(50 * ((i - (n - 4)) * 4 + k * step) / 16))
                    k += 1
            if e and i >= n - 8:  # the lead's feedback swell on B
                if i == n - 8:
                    Tr["lead"].add(start, 31.8, "B4", 70)
        # ---------------- V THE LIGHTS ----------------
        elif sec == "lights":
            root, voic = LIGHTS[(i // 2) % 4]
            for k in range(8):
                Tr["bass"].add(start + 0.5 * k, 0.45, nm(root), 104 - (8 if k % 2 else 0))
            Tr["sub"].add(start, 3.9, nm(root - 12 if root >= 36 else root), 104)
            top = sorted(voic)[-3:]
            for s in range(16):  # the wall: tremolo on three chord tones
                Tr["g1"].add(start + 0.25 * s, 0.24, nm(top[(s // 2) % 3] + 12), 100 + (8 if s % 4 == 0 else 0))
            if i % 2 == 0:
                Tr["wall"].add(start, 7.8, ",".join(nm(x) for x in (root, root + 7, root + 12)), 96)
                Tr["strings"].add(start, 7.8, ",".join(nm(x) for x in voic), 100)
            if i % 12 == 0 and i <= 36:  # T in long values on the lead, a glockenspiel above
                theme(Tr["lead"], start, 2.0, 2, 104)
                theme(Tr["glock"], start, 2.0, 26, 84)
            if i == 24:
                Tr["violin"].add(start, 31.8, "E6", 80)
            Tr["kit"].add(start, 0.5, "k", 112)
            Tr["kit"].add(start + 1.5, 0.5, "k", 96)
            Tr["kit"].add(start + 2.0, 0.5, "k", 106)
            for b in (1.0, 3.0):
                Tr["kit"].add(start + b, 0.5, "s", 116)
            Tr["kit"].add(start, 1.0, "c" if i % 2 == 0 else "c2", 108)
            for b in range(8):
                Tr["kit"].add(start + 0.5 * b, 0.5, "rd", 84 + (10 if b % 2 == 0 else 0))
            if i % 8 == 7:
                for k, piece in enumerate(("t1", "t1", "t2", "t2", "t3", "t3", "ft", "ft")):
                    Tr["kit"].add(start + 2.0 + 0.25 * k, 0.25, piece, 96 + 2 * k)
            if i >= n - 2:  # the last two bars hang on the crash
                Tr["kit"].ev = [ev for ev in Tr["kit"].ev if not (ev[0] >= start and ev[2] not in ("c", "c2"))]
        # ---------------- VI STILL ON ----------------
        elif sec == "still":
            root, voic = STILL[(i // 4) % 2]
            if i % 4 == 0 and i < 32:
                Tr["piano"].add(start, 15.5, ",".join(nm(x) for x in [root] + voic), 58)
            if i in (8, 24):
                t0 = start + 4.0
                for m, d in T[:3]:  # T's first three notes, and no ending
                    Tr["piano"].add(t0, d * 1.5, nm(m + 12), 64)
                    t0 += d * 1.5
            if i == 12:
                speak(Tr["radio2"], start, SPEECH_3, slow=1.6, base="F2")
            if i == 34:
                Tr["whistle"].add(start, 8.0, "C5", 60)
        # ---------------- the field: static and wind, thinning as the band plays ----------------
        quiet = sec in ("carrier", "snowfall", "still")
        for _ in range(wrng.randint(10, 18) if quiet else wrng.randint(0, 2)):
            Tr["static"].add(start + wrng.uniform(0, 3.97), 0.04, "C5", wrng.randint(24, 70))
        if i % 8 == 0 and (quiet or sec == "brushes"):
            Tr["wind"].add(start, 32.0, "C4", 86 if sec == "snowfall" else 70)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, Tr


def patches():
    return {
        "c2-static": {"about": "chirper-two: shortwave static, a 4 ms noise tick band-passed like a radio.",
                      "synth": {"layers": [{"type": "noise"}], "filters": ["hp cutoff=900", "lp cutoff=4500"],
                                "amp": {"a": "0.2ms", "d": "4ms", "s": 0, "r": "3ms"}}, "play": {"vel_sens": 1.0}},
        "c2-wind": {"about": "chirper-two: wind, noise through a band-pass swept by the track's 7-bar LFO `w`.",
                    "synth": {"layers": [{"type": "noise", "color": "pink"}],
                              "filters": [{"kind": "bp", "q": 2.0,
                                           "cutoff": {"value": 500, "mod": [{"src": "lfo.w", "amount": 1.3},
                                                                            {"src": "lfo.g", "amount": 0.4}]}}],
                              "amp": {"a": "5s", "d": "1s", "s": 0.9, "r": "6s"}}},
        "c2-whistle": {"about": "chirper-two: a shortwave heterodyne whistle gliding as the dial turns.",
                       "synth": {"layers": [{"wave": "sine"}],
                                 "pitch": {"value": 0, "mod": [{"src": "env.dial", "amount": 14}]},
                                 "env": {"dial": {"a": "3s", "d": "3s", "s": 0.2}},
                                 "amp": {"a": "800ms", "d": "2s", "s": 0.5, "r": "1.5s"}}},
    }


def main():
    total, bars, sec, Tr = build()
    st = {n: s for n, s, k in sec}
    climb0 = st["climb"]
    dist = [["0b", 0.0], [f"{climb0}b", 0.0], [f"{st['lights']}b", 1.0], [f"{st['still']}b", 1.0],
            [f"{st['still'] + 0.01}b", 0.0], [f"{total}b", 0.0]]
    # the fader ride: the brushes sit back, the climb climbs, the lights are the loudest place
    dyn = [["0b", 0.0], [f"{st['brushes']}b", -6.0], [f"{st['snowfall'] - 0.01}b", -6.0], [f"{st['snowfall']}b", 0.0],
           [f"{st['climb']}b", -9.0], [f"{st['lights'] - 0.01}b", -1.0], [f"{st['lights']}b", 0.0],
           [f"{st['still']}b", 0.0], [f"{total}b", 0.0]]
    pump = {"type": "pump", "on": "kit.k", "depth": "-6dB", "attack": "3ms", "release": "280ms", "curve": 0.8}
    radio_fx = ["hp cutoff=320", "lp cutoff=3200", {"type": "crush", "bits": 10, "rate": 11000, "mix": 0.35},
                "drive drive=0.3", "reverb kind=room decay=0.8s mix=0.15"]
    tracks = [
        {"name": "g1", "patch": "clean-chorus", "gain": "-8dB", "pan": -0.35,
         "fx": [{"type": "drive", "drive": {"value": 0.05, "mod": [{"src": "auto.dist", "amount": 0.7}]}},
                "lp cutoff=6000", "reverb kind=hall decay=3.5s mix=0.3"],
         "auto": {"dist": {"points": dist}}, "score": Tr["g1"].score(total)},
        {"name": "g2", "patch": "clean-chorus", "gain": "-10dB", "pan": 0.35,
         "fx": [{"type": "delay", "time": "3/8", "feedback": 0.45, "mix": 0.35, "ping_pong": True, "tone": 3000},
                "reverb kind=hall decay=4s mix=0.35"], "score": Tr["g2"].score(total)},
        {"name": "lead", "patch": "lead-tape", "gain": "-12dB", "pan": 0.1, "score": Tr["lead"].score(total)},
        {"name": "wall", "patch": "m8", "gain": "-16dB", "fx": ["lp cutoff=4000", "reverb kind=hall decay=2.5s mix=0.2"],
         "score": Tr["wall"].score(total)},
        {"name": "bass", "patch": "fretless", "gain": "-4dB", "fx": [pump, "drive drive=0.25"],
         "score": Tr["bass"].score(total)},
        {"name": "sub", "patch": "sub-sine", "gain": "-8dB",
         "fx": [pump, {"type": "phantom", "cutoff": "110hz", "harmonics": "-8dB", "odd": 0.4}],
         "score": Tr["sub"].score(total)},
        {"name": "brush", "patch": "brush-kit", "gain": "-4dB", "fx": ["reverb kind=room decay=1.0s mix=0.18"],
         "score": Tr["brush"].score(total)},
        {"name": "kit", "patch": "rock-kit-dark", "gain": "-4dB", "fx": ["reverb kind=room decay=1.3s mix=0.18"],
         "score": Tr["kit"].score(total)},
        {"name": "strings", "patch": "strings", "gain": "-12dB", "fx": ["hp cutoff=120"], "score": Tr["strings"].score(total)},
        {"name": "violin", "patch": "violin", "gain": "-16dB", "pan": 0.2, "score": Tr["violin"].score(total)},
        {"name": "cello", "patch": "cello", "gain": "-8dB", "pan": -0.15, "score": Tr["cello"].score(total)},
        {"name": "celesta", "patch": "celesta", "gain": "-8dB", "pan": 0.2,
         "fx": ["reverb kind=hall decay=4s mix=0.4"], "score": Tr["celesta"].score(total)},
        {"name": "glock", "patch": "glock", "gain": "-16dB", "pan": -0.2,
         "fx": ["reverb kind=hall decay=3s mix=0.35"], "score": Tr["glock"].score(total)},
        {"name": "piano", "patch": "piano", "gain": "-6dB", "fx": ["reverb kind=hall decay=3.5s mix=0.3"],
         "score": Tr["piano"].score(total)},
        {"name": "radio", "patch": "voice-speech", "gain": "-4dB", "pan": -0.1, "fx": radio_fx,
         "score": Tr["radio"].score(total)},
        {"name": "radio-late", "patch": "voice-speech", "gain": "-5dB", "pan": 0.1,
         "fx": [{"type": "pitch", "semitones": -3, "formant": -3}] + radio_fx + ["reverb kind=hall decay=3s mix=0.3"],
         "score": Tr["radio2"].score(total)},
        {"name": "static", "patch": "c2-static", "gain": "-22dB", "pan": -0.1, "fx": ["width width=1.4"],
         "score": Tr["static"].score(total)},
        {"name": "whistle", "patch": "c2-whistle", "gain": "-30dB", "pan": 0.3, "fx": ["reverb kind=room decay=1s mix=0.3"],
         "score": Tr["whistle"].score(total)},
        {"name": "wind", "patch": "c2-wind", "gain": "-16dB", "fx": ["width width=1.6"],
         "lfo": {"w": "sine rate=7/1", "g": "sine rate=1/1 phase=0.3"}, "score": Tr["wind"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - All the Lights Left On, track 1 (the opener). Original composition by chirper-two, generated by "
             "compose/chirpers6/src/chirpers6-t1.py. Crescendo post-rock at 140 bpm (half time first): a radio voice "
             "from a mast's night service and a five-note theme transformed through six movements: Carrier, Brushes, "
             f"Snowfall, Climb, The Lights and Still On. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "All the Lights Left On", "title": "The Mast",
                               "track": 1, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "3s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "true_peak: true",
        "patches: " + json.dumps(patches()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "highshelf cutoff=7000 gain=-1dB"]},
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
