#!/usr/bin/env python3
"""chirpers3-t6 (Tape Weather, track 6). Composed by chirper-two: WONKY BRUSH DRAG.

Bedroom-jazz lo-fi played by hand on a physical kit: no samples and no quantise.
- THE DRUMMER DRAGS: chirp's physical drum layer (bd-7d117e) with soft mallets and brushes. A felt kick pushed a
  little early, a mallet snare dragged late, brush taps drifting off the swung sixteenths (a seeded drunk walk, the
  same every render), brush sweeps under it all, mallet-tom fills at phrase ends.
- THE TAPE WARPS: the wurli goes through a slow chorus at full wet (wow), a fast shallow one (flutter), tape
  saturation, a worn top and a little bit-crush. The drop deepens the wow until the chords seasick.
- THE CHORDS SINK: Fmaj9 | Em7 | Ebmaj7#11 | Dm9, a semitone a bar; the switch-up sinks a fourth lower (Bbmaj9 |
  Am7 | Abmaj7#11 | G13sus) in half time.
- DUSTY VIBES: Odd Hours t8's vibraphone (borrowed) behind a lo-pass, a falling three-note sigh, late.
- Vinyl crackle (synthesised: sparse noise ticks) and hiss throughout.
Form: intro (radio-muffled keys) / A / switch-up (half time) / A2 / drop (the warp) / A3 / outro.

Emits songs/chirpers3-t6.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T6_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers3-t6.yaml")
BPM = 78
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel):
        self.ev.append((round(max(0.0, at), 4), max(0.05, round(ln, 4)), head, int(max(1, min(127, vel)))))

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
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


# chords: (bass root midi, voicing midis)
A_LOOP = [(41, [57, 60, 64, 67]),   # Fmaj9: F2 | A3 C4 E4 G4
          (40, [55, 59, 62, 66]),   # Em7(9): E2 | G3 B3 D4 F#4
          (39, [55, 58, 62, 69]),   # Ebmaj7#11: Eb2 | G3 Bb3 D4 A4
          (38, [53, 57, 60, 64])]   # Dm9: D2 | F3 A3 C4 E4
A_TURN = (45, [55, 61, 65, 68])     # A7b13 (the fourth bar of every other phrase leans home)
B_LOOP = [(34, [50, 53, 57, 60]),   # Bbmaj9: Bb1 | D3 F3 A3 C4
          (33, [48, 52, 55, 59]),   # Am7(9)
          (32, [48, 51, 55, 62]),   # Abmaj7#11
          (31, [53, 57, 60, 64])]   # G13sus: G1 | F3 A3 C4 E4

# Round 2 (v2): the DROP becomes an event. W = the wurli's tape warps until the chords seasick (the wow deepens and
# slows, the top wears away, the crush rises) and snaps back at A3; F = the whole mix sinks under a lo-pass through
# the drop (18 kHz down to ~1 kHz) and opens again; N = the NEEDLE LIFTS: the drop's last beat is silence but for a
# crackle burst, and A3 lands.
R2 = set(filter(None, os.environ.get("T6_R2", "W,F,N").split(","))) - {"none"}
# Round 3 (v3): T = the vibes' SIGH GROWS INTO A TUNE through A2 and A3, a four-bar phrase per chord loop: the sigh
# falling, its inversion rising, the sigh again from lower, and a held top note; M = the mix: the fretless darker
# (less mid), the brush taps brighter.
R3 = set(filter(None, os.environ.get("T6_R3", "T,M").split(","))) - {"none"}
# Round 4 (v4): R = TAPE WEATHER (the album's name, made literal): rain on the window, synthesised (soft noise
# droplets, band-passed, random), thick in the intro, the drop and the outro and a faint drizzle under the grooves,
# and distant thunder (a low noise swell) rolling through the drop.
R4 = set(filter(None, os.environ.get("T6_R4", "R").split(","))) - {"none"}
# Round 5 (v5): F = THE WEATHER COMES IN FIRST: the record starts from near-silence (a master fade over six beats)
# with only the rain and the record's surface; the radio-muffled keys enter in the intro's third bar, as if heard
# through the window.
R5 = set(filter(None, os.environ.get("T6_R5", "F").split(","))) - {"none"}
# Round 6 (v6): D = DUB THROWS in the switch-up, answering t5 Low Pressure (chirper-zero's dub next door): the
# mallet snare and the rim go to a dub send (a dotted-eighth ping-pong tape echo, a spring), and every other bar
# one vibes note is thrown into the echo.
R6 = set(filter(None, os.environ.get("T6_R6", "D").split(","))) - {"none"}
# Round 7 (v7): J = THE TAPE TRIPS once, answering t3 Late for the Grid (chirper-one's warped boom-bap, whose loop
# trips and catches itself): in A3 the eighth bar loses its fourth beat (everything drops out for it), and the next
# bar lands a beat early: one happy accident.
R7 = set(filter(None, os.environ.get("T6_R7", "J").split(","))) - {"none"}
# Round 8 (v8): H = THE HAND-OFF to t7 (After the Beat, Rain): the outro's last two bars leave the rain alone (the
# keys stop, the weather does not), so t6 ends in the same rain t7 begins in.
R8 = set(filter(None, os.environ.get("T6_R8", "H").split(","))) - {"none"}
# Round 9 (v9): T = the rain runs to the very end: a short tail (0.5 s, was 3 s of silence after the last drop), so
# t6 hands t7 a shower, not a silence.
R9 = set(filter(None, os.environ.get("T6_R9", "T").split(","))) - {"none"}
FORM = [("intro", 4), ("A", 16), ("switch", 8), ("A2", 16), ("drop", 4), ("A3", 12), ("outro", 4)]
LEVEL = {"intro": 58, "A": 72, "switch": 66, "A2": 78, "drop": 56, "A3": 80, "outro": 56}
DRUMS = {"A", "switch", "A2", "A3"}


def build():
    rng = random.Random(6)
    T = {k: Track(k) for k in ("keys", "kw", "bass", "sub", "vibes", "drums", "crackle", "hiss", "rain", "thunder",
                               "dub", "vdub")}
    rrng = random.Random(66)  # the weather's own dice (the music's stay as they were)
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 3.0 if (name == "A3" and i == 7 and "J" in R7) else 4.0
    total = pos
    drift = 0.0
    for start, sec, i, n in bars:
        v = LEVEL[sec]
        if sec == "switch":
            root, voic = B_LOOP[(i // 2) % 4]  # half time: a chord every two bars
        else:
            root, voic = A_LOOP[i % 4]
            if i % 8 == 7 and sec in ("A", "A2", "A3"):
                root, voic = A_TURN
        # ---- keys: the chord a hair late, strummed; a soft re-hit on the and of three ----
        drag = 0.05 if sec != "intro" else 0.0
        K = T["kw"] if sec == "drop" and "W" in R2 else T["keys"]  # the drop's chords on the warped tape
        if sec == "intro" and i < 2 and "F" in R5:
            K = Track("_")  # the window is shut for two bars: weather only
        if sec == "outro" and i >= 2 and "H" in R8:
            K = Track("_")  # the keys stop; the rain goes on into t7
        K.add(start + drag, 2.4 if sec != "switch" else 3.8, ",".join(nm(x) for x in voic), v - 6)
        if sec in ("A", "A2", "A3") and i % 2 == 1:
            T["keys"].add(start + 2.5 + drag, 1.3, ",".join(nm(x) for x in voic[1:]), v - 18)
        if sec in ("intro", "drop", "outro"):
            K.add(start + 2.0 + drag, 1.9, ",".join(nm(x) for x in voic[:3]), v - 14)
        # ---- bass: behind the beat ----
        if sec in DRUMS:
            late = 0.04
            T["sub"].add(start + late, 3.6 if sec == "switch" and i % 2 == 0 else 1.6, nm(root - 12), v - 4)
            if sec == "switch":
                if i % 2 == 0:
                    T["bass"].add(start + late, 3.6, nm(root), v - 2)
                else:
                    T["bass"].add(start + 2.5 + late, 1.2, nm(root + 7), v - 10)
            else:
                T["bass"].add(start + late, 1.4, nm(root), v - 2)
                T["bass"].add(start + 1.75 + late, 0.6, nm(root + 12 if i % 2 else root + 7), v - 12)
                T["bass"].add(start + 2.5 + late, 1.2, nm(root + 7), v - 8)
                if i % 4 == 3:
                    T["bass"].add(start + 3.5 + late, 0.45, nm(root + 1 if i % 8 == 7 else root - 1), v - 10)
        # ---- dusty vibes: a falling three-note sigh, late, every other bar of the A sections ----
        tune = "T" in R3 and sec in ("A2", "A3")
        if (sec in ("A2", "A3") and i % 2 == 0 and not tune) or (sec == "A" and i % 4 == 2) or tune:
            top = sorted(voic)[-1] + 12
            sigh = [top, top - 3 if (top - 3) % 12 in {x % 12 for x in voic} else top - 4, top - 5]
            ph = i % 4 if tune else 0
            if ph == 1:  # the sigh inverted: rising
                sigh = list(reversed(sigh))
            elif ph == 2:  # the sigh from lower
                sigh = [x - 5 for x in sigh]
            if ph == 3:  # the held top
                T["vibes"].add(start + 1.55 + rng.uniform(-0.02, 0.04), 2.2, nm(top + 2), v - 8)
            else:
                for k, (o, nn) in enumerate(zip((1.55, 1.95, 2.75), sigh)):
                    T["vibes"].add(start + o + rng.uniform(-0.02, 0.04), 0.9 if k == 2 else 0.4, nm(nn), v - 10 - 3 * k)
        # ---- the drummer ----
        d = T["drums"]
        if sec in DRUMS:
            drift = max(-0.03, min(0.03, drift + rng.uniform(-0.012, 0.012)))
            half = sec == "switch"
            kicks = [0.0, 2.5] if half else ([0.0, 1.625, 2.5] if i % 4 != 3 else [0.0, 1.625, 2.375, 2.75])
            for kb in kicks:
                d.add(start + kb - 0.035, 0.5, "k", v + (4 if kb == 0 else -6))
            for sb in ([2.0] if half else [1.0, 3.0]):
                (T["dub"] if half and "D" in R6 else d).add(start + sb + 0.09 + drift, 0.5, "ms", v - 2)
            for s16 in range(16 if not half else 0):  # brush taps on the swung sixteenths, drifting
                pos16 = s16 // 2 * 0.5 + (0.33 if s16 % 2 else 0.0)
                if s16 % 2 and rng.random() < (0.1 if sec == "A3" else 0.45):
                    continue
                vel = v - (14 if s16 % 4 == 0 else 22 if s16 % 2 == 0 else 30)
                d.add(start + pos16 + drift + rng.uniform(-0.02, 0.02), 0.2, "bt", vel)
            d.add(start, 1.9, "bs", v - 22)
            d.add(start + 2.0, 1.9, "bs", v - 24)
            if i % 4 == 3 and not half:  # a mallet-tom fill dragging into the next bar
                for k, (o, piece) in enumerate(((3.25, "mt1"), (3.5, "mt1"), (3.75, "mt2"))):
                    d.add(start + o + 0.03 * k, 0.3, piece, v - 6 - 2 * k)
            if half and i % 2 == 1:
                (T["dub"] if "D" in R6 else d).add(start + 3.5 + 0.05, 0.3, "rc", v - 10)
                if "D" in R6:  # a vibes throw into the echo
                    T["vdub"].add(start + 1.5 + 0.04, 0.4, nm(sorted(voic)[-1] + 14), v - 8)
        elif sec == "drop":
            d.add(start, 3.8, "bs", v - 18)
        if sec == "A3" and i == 7 and "J" in R7:  # the trip: the bar's fourth beat never happens
            for tr in T.values():
                tr.ev = [e for e in tr.ev if not (start + 3.0 - 1e-6 <= e[0] < start + 4.0)]
                tr.ev = [(s, min(ln, start + 3.0 - s) if s < start + 3.0 < s + ln else ln, h, vel) for s, ln, h, vel in tr.ev]
        # ---- the weather ----
        if "R" in R4:
            heavy = sec in ("intro", "drop", "outro")
            for _ in range(rrng.randint(34, 46) if heavy else rrng.randint(6, 10)):
                T["rain"].add(start + rrng.uniform(0, 3.97), 0.05, "C5", rrng.randint(20, 70 if heavy else 45))
            if sec == "drop" and i == 0:
                T["thunder"].add(start + 0.5, 7.0, "C2", 90)
        # ---- vinyl crackle and hiss ----
        for _ in range(rng.randint(5, 11)):
            T["crackle"].add(start + rng.uniform(0, 3.95), 0.06, "C5", rng.randint(30, 80))
    T["hiss"].add(0.0, total - 0.1, "C4", 60)
    if "N" in R2:  # the needle lifts on the drop's last beat
        dr = [bb for bb in bars if bb[1] == "drop"]
        lift0, lift1 = dr[-1][0] + 3.0, dr[-1][0] + 4.0
        for name, tr in T.items():
            if name == "hiss":
                continue
            tr.ev = [e for e in tr.ev if not (lift0 - 1e-6 <= e[0] < lift1)]
            tr.ev = [(s, min(ln, lift0 - s) if s < lift0 < s + ln else ln, h, vel) for s, ln, h, vel in tr.ev]
        for k in range(14):
            T["crackle"].add(lift0 + k * 0.05 + rng.uniform(0, 0.03), 0.05, "C5", 70 + rng.randint(0, 30))
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    def drum(pitch, layer, amp, gain="0dB", filters=("hp cutoff=40",)):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [layer], "filters": list(filters),
                                                                    "amp": amp}, "play": {"vel_sens": 0.7}}}
    brush = dict(type="drum", beater="brush", decay="0.3s", sharp=20, reso=1.4, cavity=0.3, reso_level=0.5,
                 shell=0.3, shell_hz=470, wires=0.45, gap=0.25, wire_tone="5k", strike=0.35, damp=0.35, slap=0.6,
                 stereo=0.35)
    kit = {"about": "chirper-two's lo-fi hand kit for Tape Weather t6: chirp's physical drum layer with soft mallets "
                    "and brushes (no samples): a felt kick, a mallet snare, brush taps and sweeps, mallet toms, a rim.",
           "extends": "room-kit",
           "kit": {
               "k": drum("D1", dict(type="drum", beater="felt", decay="0.55s", sharp=35, reso=1.0, cavity=0.25,
                                    reso_level=0.6, air=0.45, strike=0.2, damp=0.35, slap=0.25, stereo=0.15),
                         {"a": "0.5ms", "d": "650ms", "s": 0, "r": "50ms", "curve": 2}, "10dB", ("hp cutoff=28",)),
               "ms": drum("D3", dict(brush, beater="felt", contact=1.4, wires=0.5, decay="0.28s", slap=0.5),
                          {"a": "0.5ms", "d": "500ms", "s": 0, "r": "60ms", "curve": 2}, "-2dB", ("hp cutoff=90",)),
               "bt": drum("E3", brush, {"a": "0.5ms", "d": "600ms", "s": 0, "r": "60ms", "curve": 2},
                          "-2dB" if "M" not in R3 else "1dB", ("hp cutoff=%d" % (120 if "M" not in R3 else 400),)),
               "bs": drum("E3", dict(brush, sweep="0.9s"), {"a": "30ms", "d": "1.2s", "s": 0, "r": "100ms", "curve": 1},
                          "-5dB", ("hp cutoff=150",)),
               "mt1": drum("A2", dict(type="drum", beater="felt", decay="0.6s", sharp=30, reso=1.0, cavity=0.2,
                                      tune_sounding=True, reso_level=0.5, air=0.4, strike=0.3, damp=0.3, slap=0.3,
                                      stereo=0.4), {"a": "0.5ms", "d": "800ms", "s": 0, "r": "80ms", "curve": 2}),
               "mt2": drum("E2", dict(type="drum", beater="felt", decay="0.7s", sharp=30, reso=1.0, cavity=0.2,
                                      tune_sounding=True, reso_level=0.5, air=0.4, strike=0.3, damp=0.3, slap=0.3,
                                      stereo=0.4), {"a": "0.5ms", "d": "900ms", "s": 0, "r": "80ms", "curve": 2}),
               "rc": drum("E3", dict(brush, beater="stick", strike=0.95, damp=0.8, wires=0.2, slap=1.0),
                          {"a": "0.2ms", "d": "120ms", "s": 0, "r": "30ms"}, "-4dB", ("hp cutoff=300",)),
           }}
    vibes = {"about": "Odd Hours t8's vibraphone (chirper-two), borrowed: partials 1 / 4 / 10, a 5.2 Hz motor.",
             "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.16], [10.0, 0.025]],
                                   "level": {"value": "0dB", "mod": [{"src": "lfo.motor", "amount": 3}]}}],
                       "lfo": {"motor": {"wave": "sine", "rate": "5.2hz"}},
                       "filters": ["hp cutoff=150", "lp cutoff=7k"],
                       "amp": {"a": "2ms", "d": "3.2s", "s": 0, "r": "500ms", "curve": 2}},
             "play": {"vel_sens": 0.55}}
    crackle = {"about": "chirper-two's vinyl crackle: a 3 ms noise tick, high-passed.",
               "synth": {"layers": [{"name": "tick", "type": "noise"}], "filters": ["hp cutoff=1800", "lp cutoff=9k"],
                         "amp": {"a": "0.1ms", "d": "3ms", "s": 0, "r": "2ms"}}, "play": {"vel_sens": 1.0}}
    hiss = {"about": "chirper-two's tape hiss: a quiet band of noise.",
            "synth": {"layers": [{"name": "hiss", "type": "noise"}], "filters": ["hp cutoff=3000", "lp cutoff=10k"],
                      "amp": {"a": "2s", "d": "1s", "s": 1.0, "r": "3s"}}}
    sub = {"about": "chirper-two's sub: a sine an octave under the fretless's long notes.",
           "synth": {"layers": [{"name": "sub", "wave": "sine"}], "amp": {"a": "140ms", "d": "500ms", "s": 0.8, "r": "200ms"}}}
    out = {"c2-lofi-kit": kit, "c2-vibes": vibes, "c2-crackle": crackle, "c2-hiss": hiss, "c2-sub": sub}
    if "R" in R4:
        out["c2-rain"] = {"about": "chirper-two's rain: a droplet of band-passed noise (8 ms), scattered at random.",
                          "synth": {"layers": [{"name": "drop", "type": "noise"}],
                                    "filters": ["hp cutoff=900", "lp cutoff=5500"],
                                    "amp": {"a": "0.3ms", "d": "9ms", "s": 0, "r": "6ms", "curve": 2}},
                          "play": {"vel_sens": 1.0}}
        out["c2-thunder"] = {"about": "chirper-two's distant thunder: low noise swelling and rolling away.",
                             "synth": {"layers": [{"name": "roll", "type": "noise"}], "filters": ["lp cutoff=180"],
                                       "amp": {"a": "1.2s", "d": "4s", "s": 0.2, "r": "2.5s", "curve": 2}}}
    return out


def main():
    total, bars, sec, T = build()
    d0 = next(s for n, s, k in sec if n == "drop")
    a3 = next(s for n, s, k in sec if n == "A3")
    warp_pts = [["0b", 0.0], [f"{d0}b", 0.0], [f"{a3 - 0.5}b", 1.0], [f"{a3}b", 0.0]]
    wow = {"type": "chorus", "rate": 0.35, "depth": 0.55, "voices": 1, "mix": 1.0}
    wow_k = wow
    flutter = {"type": "chorus", "rate": 5.5, "depth": 0.08, "voices": 1, "mix": 0.5}
    tracks = [
        {"name": "keys", "patch": "wurli", "pan": -0.1, "gain": "-6dB",
         "fx": [wow_k, flutter, "tape drive=0.3 warmth=0.65",
                ({"type": "filter", "kind": "lp", "cutoff": {"value": 5000, "mod": [{"src": "auto.warp", "amount": -1.5}]}}
                 if "W" in R2 else "lp cutoff=5000"),
                ({"type": "crush", "bits": 12, "rate": 16000, "mix": {"value": 0.3, "mod": [{"src": "auto.warp", "amount": 0.5}]}}
                 if "W" in R2 else {"type": "crush", "bits": 12, "rate": 16000, "mix": 0.3}),
                "reverb kind=room decay=1.2s mix=0.18"], "score": T["keys"].score(total),
         **({"auto": {"warp": {"points": warp_pts}}} if "W" in R2 else {})},
        *([{"name": "keys-warped", "patch": "wurli", "pan": 0.05, "gain": "-5dB",
             "fx": [{"type": "chorus", "rate": 0.18, "depth": 0.95, "voices": 1, "mix": 1.0},
                    {"type": "chorus", "rate": 3.1, "depth": 0.2, "voices": 1, "mix": 0.6},
                    "tape drive=0.5 warmth=0.8", "lp cutoff=2200",
                    {"type": "crush", "bits": 10, "rate": 11000, "mix": 0.55},
                    "reverb kind=hall decay=2.5s mix=0.3"], "score": T["kw"].score(total)}] if "W" in R2 else []),
        {"name": "bass", "patch": "fretless", "gain": "1dB" if "M" not in R3 else "0dB",
         "fx": ["lp cutoff=%d" % (900 if "M" not in R3 else 600), "tape drive=0.2 warmth=0.5"],
         "score": T["bass"].score(total)},
        {"name": "sub", "patch": "c2-sub", "gain": "-5dB", "score": T["sub"].score(total)},
        {"name": "vibes", "patch": "c2-vibes", "pan": 0.3, "gain": "-6dB",
         "fx": [wow, "lp cutoff=2600", "reverb kind=hall decay=2.2s mix=0.3"], "score": T["vibes"].score(total)},
        {"name": "drums", "patch": "c2-lofi-kit", "gain": "0dB",
         "fx": ["tape drive=0.35 warmth=0.6", "lp cutoff=11000",
                {"type": "crush", "bits": 12, "rate": 18000, "mix": 0.25},
                "reverb kind=room decay=0.7s mix=0.12"], "score": T["drums"].score(total)},
        *([{"name": "dub", "patch": "c2-lofi-kit", "gain": "0dB",
             "fx": [{"type": "delay", "time": "3/16", "feedback": 0.55, "ping_pong": True, "tone": 2500, "mix": 0.5},
                    "reverb kind=spring decay=2.2s mix=0.35", "tape drive=0.35 warmth=0.6"],
             "score": T["dub"].score(total)},
            {"name": "vibes-dub", "patch": "c2-vibes", "pan": -0.2, "gain": "-7dB",
             "fx": [{"type": "delay", "time": "3/16", "feedback": 0.62, "ping_pong": True, "tone": 2200, "mix": 0.6},
                    "lp cutoff=3000", "reverb kind=spring decay=2.4s mix=0.3"], "score": T["vdub"].score(total)}]
          if "D" in R6 else []),
        {"name": "crackle", "patch": "c2-crackle", "pan": 0.05, "gain": "-20dB", "score": T["crackle"].score(total)},
        *([{"name": "rain", "patch": "c2-rain", "pan": -0.2, "gain": "-22dB",
             "fx": ["reverb kind=room decay=0.6s mix=0.25", "width width=1.6"], "score": T["rain"].score(total)},
           {"name": "thunder", "patch": "c2-thunder", "gain": "-8dB", "fx": ["reverb kind=hall decay=3s mix=0.4"],
            "score": T["thunder"].score(total)}] if "R" in R4 else []),
        {"name": "hiss", "patch": "c2-hiss", "gain": "-36dB", "score": T["hiss"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Tape Weather, track 6. Original composition by chirper-two, generated by "
             "compose/chirpers3/src/chirpers3-t6.py. Wonky brush drag: bedroom-jazz lo-fi on a physical soft-mallet "
             "and brush kit, unquantised (kick early, snare late, brushes drifting), tape-warped wurli chords sinking "
             f"a semitone a bar, a lazy fretless, dusty vibes, crackle and hiss. 78 bpm. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Tape Weather", "title": "Late on Purpose", "track": 6,
                               "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "%s"' % ("0.5s" if "T" in R9 else "3s"),
        'ceiling: "-0.5dB"',
        'volume: "3dB"',
        "patches: " + json.dumps(patches()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=30", "highshelf cutoff=8000 gain=0dB"]}]
                                 + ([{"type": "filter", "kind": "lp", "cutoff": {"value": 18000, "mod": [{"src": "auto.dive", "amount": -4.0}]}}]
                                    if "F" in R2 else [])
                                 + ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.fadein", "amount": 1}]}}]
                                    if "F" in R5 else [])
                                 + ["tape drive=0.2 warmth=0.5",
                                    "glue threshold=-20dB ratio=1.6 attack=20ms release=250ms makeup=1dB"],
                                 **({"auto": {**({"dive": {"points": [["0b", 0.0], [f"{d0}b", 0.0], [f"{a3 - 1}b", 1.0],
                                                                       [f"{a3}b", 0.0]]}} if "F" in R2 else {}),
                                              **({"fadein": {"points": [["0b", -30.0], ["6b", 0.0]]}} if "F" in R5 else {})}}
                                    if ("F" in R2 or "F" in R5) else {})}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
