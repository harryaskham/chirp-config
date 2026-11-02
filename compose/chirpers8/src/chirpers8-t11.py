#!/usr/bin/env python3
"""chirpers - A Light Left On (chirpers VIII), track 11 (chirper-three): BUTTERFLY HOUSE.

Deep, breathing electronic house whose every dial is steered by a STRANGE ATTRACTOR. The Lorenz system
(sigma 10, rho 28, beta 8/3) is integrated once per sixteenth from one fixed seed; its three coordinates drive the song:
  x  which LOBE the orbit is in -> which harmonic world (C# or F#), and the wavetable lead's POSITION;
  y  which partial the lead plays, and how often the TRANCE GATE opens on the pads;
  z  the vocal CHOPS (sampled, sliced) fire near the top of the attractor.
The orbit flips lobes at moments nobody can predict - the song changes key when the weather does. (The smallest change
in the seed and it is a different song: a butterfly in the machine.)

TUNING: the HARMONIC SERIES. Every pitch is a partial (8..16) of the lobe's fundamental - C#1 or F#1 - written as
fractional MIDI: the 7th, 11th and 13th partials are alien to twelve notes, and pure.

DYNAMICS SHOWCASE: a bass that PUMPS on the kick, pads TRANCE-GATED by a ghost track the attractor writes, OTT on the
drums, a TRANSIENT shaper on the kick, GLUE on the master; a wavetable lead with a PITCH harmonizer a pure fifth above.

FORM (168 bars, ~5:40; 120 bpm, a ritardando to 112 over the last 16 bars to hand the closer its tempo):
  intro 1-16  kick, gated pads   |  A 17-48 the lead   |  B 49-80 + chops, full   |  break 81-96 the attractor alone
  C 97-136 the peak  |  outro 137-168 thinning; the orbit is held in the F# lobe for the last 16 bars, into the closer
"""
import json
import math
import os
import random

OUT = os.environ.get("C8T11_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t11.yaml")
BAR = 4.0
SECTIONS = [("intro", 1, 16), ("A", 17, 48), ("B", 49, 80), ("break", 81, 96), ("C", 97, 136), ("outro", 137, 168)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR
FUND = {+1: 25, -1: 30}                     # C#1 (lobe x > 0), F#1 (lobe x < 0)
PARTIALS = [8, 9, 10, 11, 12, 13, 14, 15, 16]


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


def partial(n, lobe, octave=0):
    """The n-th partial of the lobe's fundamental, as fractional MIDI."""
    return FUND[lobe] + 12 * math.log2(n) + 12 * octave


def mm(p):
    return f"m{p:.3f}"


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((at, ln, head, int(max(1, min(127, vel)))))

    def score(self, total=TOTAL):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(ev):
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-5:
                toks.append(f"R/{s - pos:.5g}b")
            base, _, mods = head.partition("^")
            base, _, prob = base.partition("?")              # v9: generative tokens - (a|b|c) choices, ?p chance
            toks.append(f"{base}/{ln:.5g}b@{vel}" + (f"?{prob}" if prob else "") + (f"^{mods}" if mods else ""))
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks) if toks else f"R/{total:g}b"


P = {}


def part(n):
    return P.setdefault(n, Part())


# ---------------------------------------------------------------- the attractor
def lorenz(n, seed=(1.0, 1.0, 1.05), dt=0.0045, sub=4):
    x, y, z = seed
    out = []
    for _ in range(n):
        for _ in range(sub):                         # RK2 (midpoint), small steps
            dx, dy, dz = 10 * (y - x), x * (28 - z) - y, x * y - (8 / 3) * z
            xm, ym, zm = x + dx * dt / 2, y + dy * dt / 2, z + dz * dt / 2
            dx, dy, dz = 10 * (ym - xm), xm * (28 - zm) - ym, xm * ym - (8 / 3) * zm
            x, y, z = x + dx * dt, y + dy * dt, z + dz * dt
        out.append((x, y, z))
    return out


ORBIT = lorenz(BARS * 16)


def state(bar, s16=0):
    return ORBIT[(bar - 1) * 16 + s16]


def lobe_at(bar, s16=0):
    if bar >= BARS - 15:
        return -1                                   # the outro is held in the F# lobe: into the closer
    return 1 if state(bar, s16)[0] > 0 else -1


# ---------------------------------------------------------------- writing
# v10: THUNDER AT THE LOBE FLIPS - each time the attractor changes wing (the key change, C# <-> F#) the weather
# announces it: a crack (pink noise through a low-pass that opens and shuts) rolling into a sub rumble, into the hall;
# louder the higher the storm (z); distant and soft in the break; none in the intro and outro
THUNDER = {"synth": {"layers": [{"type": "noise", "color": "pink"}, {"wave": "sine", "level": "-8dB"}],
                     "filters": [{"kind": "lp", "q": 0.7,
                                  "cutoff": {"value": 160, "mod": [{"src": "env.crack", "amount": 4}]}}],
                     "env": {"crack": {"a": "2ms", "d": "600ms", "s": 0, "r": "200ms"}},
                     "amp": {"a": "30ms", "d": "3.5s", "s": 0, "r": "1s"}},
           "fx": [{"type": "tremolo", "rate": 3, "depth": 0.45}]}


def write_thunder():
    for bar in range(2, BARS + 1):
        if lobe_at(bar) == lobe_at(bar - 1):
            continue
        sec = sec_of(bar)
        if sec in ("A", "B", "C"):
            part("thunder").add(b0(bar), 8.0, "m28.000", 84 + int(state(bar)[2]))
        elif sec == "break":
            part("thunder").add(b0(bar), 8.0, "m28.000", 52)


# v11: THE WIND IN THE GAP - pink noise through a feedback COMB that whistles at its cutoff and harmonics, the
# cutoff steered by the attractor's own var.gust (x, +-0.7) over 1.2 octaves (~390-1250 Hz), long swells, slow gusts;
# strongest in the break, where the rain stops and only the wind is left; the intro and outro stay still
WIND = {"synth": {"layers": [{"type": "noise", "color": "pink"}],
                  "filters": [{"kind": "comb", "q": 12, "cutoff": {"value": 700, "mod": [{"src": "var.gust", "amount": 1.2}]}},
                              {"kind": "lp", "cutoff": 2500}],
                  "amp": {"a": "2s", "d": "0ms", "s": 1, "r": "3s"}},
        "fx": [{"type": "tremolo", "rate": 0.3, "depth": 0.55}]}
WIND_VEL = {"A": 58, "B": 76, "break": 100, "C": 84}


def write_wind():
    for name, a, z in SECTIONS:
        if name in WIND_VEL:
            part("wind").add(b0(a), b0(z + 1) - b0(a) - 0.1, "m60.000", WIND_VEL[name])


# v12: THE EYE OF THE STORM - at the peak's most extreme moment (bar 115, z ~40, right after the forecast's 'good
# visibility, falling slowly') the storm stops dead for two bars: only the wind still whistling in the gap and the
# opening's bell struck once on F#; then the storm crashes back with a thunderclap at 117
EYE = (115, 117)
EYE_KEEP = {"wind", "hum"}


def eye_clear():
    a, z = b0(EYE[0]), b0(EYE[1])
    for n, prt in P.items():
        if n in EYE_KEEP:
            continue
        ev = []
        for s, ln, head, vel in prt.ev:
            if a <= s < z and n in ("rainL", "rainR"):
                ev.append((s, ln, head, 1))            # silent, but each drop still takes its roll of the engine's
                continue                               # dice, so every later drop falls exactly as before
            if a <= s < z:
                continue
            if s < a < s + ln:
                ln = a - s - 0.02                      # nothing rings into the eye
            ev.append((s, ln, head, vel))
        prt.ev = ev
    part("thunder").add(z, 8.0, "m28.000", 124)       # the storm crashes back


# v13: THE ROOM BREATHES WITH THE STORM - the stereo width of the hall (where rain, wind, thunder, bell, singer and
# lead all send) and of the pad follows the attractor's z: calm, the room is close and narrow (0.6); in the storm the
# walls fall away (1.6). Drums, bass and voices stay centred; width keeps the bass mono below 120 Hz.
def width_lane():
    return [[f"{b0(bar):.2f}b", round(0.6 + 1.0 * min(1.0, max(0.0, (state(bar)[2] - 12) / 26)), 3)]
            for bar in range(1, BARS + 1)]


WIDTH_FX = {"type": "width", "width": {"value": 0, "mod": [{"src": "auto.wd", "amount": 1}]}}


RAIN_WEIGHT = {"intro": 0.35, "A": 0.7, "B": 0.9, "break": 0.15, "C": 1.0, "outro": 0.3}


def write_rain():
    """v9: IT RAINS INDOORS. Each sixteenth may hold a drop: a CHOICE among the lobe's high partials, falling with a
    CHANCE that follows the storm (the attractor's z) - re-rolled by the engine on every play, so no two plays of the
    album rain alike."""
    drops = random.Random(77)
    for bar in range(1, BARS + 1):
        w = RAIN_WEIGHT[sec_of(bar)]
        for s in range(16):
            x, y, z = state(bar, s)
            storm = min(1.0, max(0.0, (z - 18) / 24))
            p = round((0.08 + 0.42 * storm) * w, 2)
            if p < 0.03:
                continue
            lb = lobe_at(bar, s)
            head = "(" + "|".join(mm(partial(n, lb)) for n in (16, 18, 20, 21, 24, 27)) + f")?{p:.2f}"
            part("rainL" if s % 2 == 0 else "rainR").add(b0(bar) + s / 4, 0.24, head, 56 + drops.randint(0, 34))


def write_music():
    hand = random.Random(11)
    for bar in range(1, BARS + 1):
        sec = sec_of(bar)
        lb = lobe_at(bar)
        # PADS: a harmonic-seventh chord of the lobe (partials 8 10 12 14), held; gated by the ghost track below
        if (sec != "break" or bar >= 89) and bar <= BARS - 8:    # v3: the last eight bars are the hum and the light
            part("pad").add(b0(bar), BAR - 0.05, ",".join(mm(partial(n, lb, -1)) for n in (8, 10, 12, 14)),
                            62 if sec in ("intro", "outro") else 72)
        # THE TRANCE GATE: a muted ghost track, a sixteenth wherever the attractor's |y| is high enough
        for s in range(16):
            x, y, z = state(bar, s)
            if bar <= 8 or abs(y) > 6 + (6 if sec in ("intro", "outro") else 0) or s % 4 == 0:   # v7: open for 8 bars
                part("gtrig").add(b0(bar) + s / 4, 0.2, "rs", 110)
        # BASS: partial 2 (an octave above the fundamental), pumping eighths; the 3rd partial on the off-beat 'and'
        if sec not in ("intro", "break") and not (sec == "outro" and bar > 160):
            for e in range(8):
                n = 2 if e % 4 != 3 else 3
                part("bass").add(b0(bar) + e * 0.5, 0.45, mm(partial(n, lb, 0)), 100 if e % 2 == 0 else 84)
        # v4: THE HOOK, rearranged by the weather - in A, B and C every two-bar phrase plays the hook in one of four
        # forms (original, retrograde, inversion round the 12th partial, a partial up), chosen by y at its start
        if sec in ("A", "B", "C") and (bar - 17) % 2 == 0:
            x, y, z = state(bar)
            form = 0 if bar in (17, 19, 49, 97) + SUNG_AT else int(max(0, min(3, (y + 25) / 50 * 4)))   # each section states it plain
            for at, n, ln, v in hook_form(form):
                part("lead").add(b0(bar) + at, ln * 0.92, mm(partial(n, lb, 0)), v)
            continue_lead = False
        else:
            continue_lead = True
        # THE LEAD (now the break's and the outro's): a wavetable, a partial chosen by y each eighth
        if continue_lead and (sec == "break" or (sec == "outro" and bar < 153)):
            for e in range(8):
                x, y, z = state(bar, e * 2)
                x2, y2, z2 = state(bar, min(15, e * 2 + 1))
                if abs(y2 - y) > (1.2 if sec != "break" else 0.6):
                    k = int(round((y + 25) / 50 * (len(PARTIALS) - 1)))
                    n = PARTIALS[max(0, min(len(PARTIALS) - 1, k))]
                    part("lead").add(b0(bar) + e * 0.5, 0.42, mm(partial(n, lb, 0)), 76 + int(min(30, abs(y2 - y) * 4)))
        # v2: THE HANDOVER - the 16th partial of F# (F#5), the closer's first note, on a music box: the light already on
        if bar >= BARS - 11 and bar % 2 == 1:
            part("light").add(b0(bar), 1.5, mm(partial(16, -1, 0)), 66 + (bar - (BARS - 11)) * 2)
        # v2: THE FAN'S HUM begins here and carries across the gap into the closer (its F#2, the same sine)
        if bar == BARS - 11:
            part("hum").add(b0(bar), b0(BARS + 1) - b0(bar) - 0.05, mm(42), 60)
        # v2: a ride in the peak, for the top end
        if sec == "C":
            for e in range(8):
                part("ride").add(b0(bar) + e * 0.5, 0.4, "rd", 66 if e % 2 == 0 else 50)
        # CHOPS: the sampled voice, sliced, fires near the top of the attractor (z high)
        if sec in ("B", "C"):
            for s in range(0, 16, 2):
                x, y, z = state(bar, s)
                if z > 36:
                    part("chops").add(b0(bar) + s / 4, 0.25, f"m{60 + int(abs(x)) % 16}", 90)
        # DRUMS
        if sec != "break":
            for b in range(4):
                if not (sec == "outro" and bar > 156):           # v2: the kick leaves before the handover
                    part("kick").add(b0(bar) + b, 0.5, "k", 114 if b == 0 else 106)
                if (sec != "intro" or bar > 8) and bar <= BARS - 8:
                    part("hats").add(b0(bar) + b + 0.5, 0.25, "oh", 66 + hand.randint(-6, 6))
                    for s in (1, 3):
                        if hand.random() < 0.7:
                            part("hats").add(b0(bar) + b + s / 4, 0.1, "h", 48 + hand.randint(-8, 8))
            if sec in ("A", "B", "C"):
                for b in (1, 3):
                    part("clap").add(b0(bar) + b + 0.02, 0.5, "cp", 90 + hand.randint(-4, 4))


FORECAST = {   # v2: chirp tts --humanize 0.7, three lines of a forecast read by the machine to itself: (at, len, ph, pitch, vel, f0)
    1: [
        (0.0, 0.78, 'K L IH1', '142.85hz', 0.865, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
        (0.783, 0.48, 'R IH0 NG', '119.54hz', 0.799, [0.0, -3.0, -6.0, -9.0, -12.0, -16.0, -19.0, -22.0, -25.0, -28.0]),
        (1.251, 0.601, 'L EY1', '137.34hz', 0.743, [0.0, 11.0, 21.0, 29.0, 35.0, 35.0, 33.0, 33.0, 33.0, 27.0, 13.0, -7.0, -28.0]),
        (1.85, 0.37, 'T ER0', '114.00hz', 0.859, [0.0, -4.0, -8.0, -12.0, -16.0, -20.0, -24.0, -28.0]),
        (2.199, 0.37, 'IH0 N', '113.50hz', 0.88, [0.0, -4.0, -8.0, -12.0, -16.0, -20.0, -24.0, -28.0]),
        (2.553, 0.37, 'DH AH0', '110.92hz', 0.776, [0.0, -4.0, -8.0, -12.0, -16.0, -20.0, -24.0, -28.0]),
        (2.937, 0.601, 'S EH1', '124.45hz', 0.841, [0.0, 11.0, 21.0, 29.0, 35.0, 35.0, 33.0, 33.0, 33.0, 27.0, 13.0, -7.0, -28.0]),
        (3.537, 0.59, 'K AH0 N D', '106.17hz', 0.742, [0.0, -3.0, -5.0, -7.0, -12.0, -18.0, -20.0, -16.0, -13.0, -15.0, -24.0, -34.0]),
        (4.106, 1.131, 'R UW1 M', '104.90hz', 0.762, [0.0, 3.0, 6.0, 9.0, 11.0, 13.0, 14.0, 14.0, 15.0, 17.0, 15.0, 9.0, 1.0, -7.0, -10.0, -10.0, -11.0, -18.0, -31.0, -47.0, -62.0, -71.0, -75.0, -79.0]),
    ],
    2: [
        (0.0, 0.78, 'L AY1 T', '142.85hz', 0.865, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
        (0.783, 1.649, 'W IH1 N D Z', '122.16hz', 0.799, [0.0, 4.0, 8.0, 11.0, 15.0, 18.0, 22.0, 25.0, 27.0, 30.0, 33.0, 35.0, 35.0, 35.0, 35.0, 37.0, 41.0, 44.0, 44.0, 39.0, 32.0, 26.0, 25.0, 28.0, 32.0, 32.0, 26.0, 16.0, 6.0, -1.0, -2.0, -0.0, 1.0, -3.0, -11.0, -23.0]),
        (2.78, 0.601, 'T ER1', '143.42hz', 0.743, [0.0, 11.0, 21.0, 29.0, 35.0, 35.0, 33.0, 33.0, 33.0, 27.0, 13.0, -7.0, -28.0]),
        (3.379, 0.696, 'N IH0 NG', '91.14hz', 0.859, [0.0, -6.0, -13.0, -19.0, -26.0, -35.0, -43.0, -47.0, -48.0, -50.0, -59.0, -72.0, -84.0, -93.0, -95.0]),
    ],
    3: [
        (0.0, 0.78, 'G UH1 D', '142.85hz', 0.865, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
        (0.783, 0.509, 'V IH2', '125.01hz', 0.799, [0.0, 8.0, 14.0, 20.0, 23.0, 25.0, 23.0, 20.0, 14.0, 8.0, 0.0]),
        (1.279, 0.37, 'Z AH0', '115.82hz', 0.743, [0.0, -4.0, -8.0, -12.0, -16.0, -20.0, -24.0, -28.0]),
        (1.648, 0.601, 'B IH1', '126.67hz', 0.859, [0.0, 11.0, 21.0, 29.0, 35.0, 35.0, 33.0, 33.0, 33.0, 27.0, 13.0, -7.0, -28.0]),
        (2.228, 0.37, 'L IH0', '107.75hz', 0.88, [0.0, -4.0, -8.0, -12.0, -16.0, -20.0, -24.0, -28.0]),
        (2.582, 0.537, 'T IY0', '106.99hz', 0.776, [0.0, -3.0, -6.0, -8.0, -11.0, -14.0, -17.0, -20.0, -22.0, -25.0, -28.0]),
        (3.492, 0.601, 'F AA1', '141.72hz', 0.841, [0.0, 11.0, 21.0, 29.0, 35.0, 35.0, 33.0, 33.0, 33.0, 27.0, 13.0, -7.0, -28.0]),
        (4.092, 0.48, 'L IH0 NG', '116.62hz', 0.742, [0.0, -3.0, -6.0, -9.0, -12.0, -16.0, -19.0, -22.0, -25.0, -28.0]),
        (4.551, 0.78, 'S L OW1', '124.75hz', 0.762, [0.0, 8.0, 16.0, 23.0, 29.0, 33.0, 35.0, 37.0, 41.0, 43.0, 39.0, 28.0, 14.0, 2.0, -5.0, -10.0, -14.0]),
        (5.329, 0.537, 'L IY0', '92.71hz', 0.809, [0.0, -9.0, -18.0, -27.0, -36.0, -46.0, -55.0, -64.0, -73.0, -82.0, -91.0]),
    ],
}
VOICE_AT = [(81, 1), (85, 2), (89, 3), (101, 1), (113, 3), (125, 2)]   # (bar, line)


def voice_notes():
    out = []
    for bar, k in VOICE_AT:
        for a, ln, ph, pitch, v, f0 in FORECAST[k]:
            out.append({"at": round(b0(bar) + 0.5 + a, 4), "len": ln, "ph": ph, "pitch": pitch, "vel": v,
                        "expr_path": {"f0": f0}})
    return out


def radio_lanes():
    """v2: the radio's dial turned by the attractor's z (near the station mid-orbit, drifting off at the extremes,
    within +-0.25 so the words stay intelligible); a gate lane keeps the static to where the voice speaks."""
    dial = [[f"{b0(bar):.2f}b", round(max(-0.25, min(0.25, (state(bar)[2] - 24) / 80)), 3)] for bar in range(1, BARS + 1)]
    rg = [["0b", -80.0]]
    for bar, k in VOICE_AT:
        a, z = b0(bar), b0(bar + 2) + 1
        rg += [[f"{a - 0.05:.2f}b", -80.0], [f"{a:.2f}b", 0.0], [f"{z:.2f}b", 0.0], [f"{z + 0.5:.2f}b", -80.0]]
    return {"dial": {"points": dial}, "rg": {"points": rg}}


# v4: THE HOOK - two bars in harmonic-series partials, rising through the alien 11th and 13th and falling home
HOOK = [(0.0, 8, 1.0, 96), (1.0, 10, 0.5, 84), (1.5, 12, 0.5, 88), (2.0, 11, 1.0, 94), (3.0, 13, 0.5, 90),
        (3.5, 12, 0.5, 84), (4.0, 10, 1.5, 92), (5.5, 9, 0.5, 82), (6.0, 8, 2.0, 88)]


def hook_form(form):
    if form == 0:
        return HOOK
    if form == 1:                                  # retrograde: the same notes, backwards in time
        rev, t = [], 0.0
        for at, n, ln, v in reversed(HOOK):
            rev.append((t, n, ln, v))
            t += ln
        return rev
    if form == 2:                                  # inversion round the 12th partial
        return [(at, max(8, min(16, 24 - n)), ln, v) for at, n, ln, v in HOOK]
    return [(at, PARTIALS[min(len(PARTIALS) - 1, PARTIALS.index(n) + 1)], ln, v) for at, n, ln, v in HOOK]


SUNG = [   # v6: chirp tts --sing "it rained in the second room a-gain" --humanize 0.4: (ph, vel, f0), one per hook note
    ('IH1 T', 0.85, [-55.0, -28.0, -9.0, 2.0, 5.0, 5.0, 2.0, 2.0, 6.0, 13.0, 17.0, 13.0, -0.0, -14.0, -18.0, -7.0, 14.0, 30.0, 30.0, 15.0, -7.0, -22.0]),
    ('R EY1 N D', 0.841, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]),
    ('IH0 N', 0.791, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]),
    ('DH AH0', 0.795, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 1.0, 6.0, 14.0, 18.0, 12.0, -2.0, -17.0, -20.0, -7.0, 17.0, 33.0, 31.0, 13.0, -11.0, -26.0]),
    ('S EH1', 0.853, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]),
    ('K AH0 N D', 0.773, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]),
    ('R UW1 M', 0.849, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -5.0, 0.0, 7.0, 9.0, 2.0, -12.0, -23.0, -21.0, -6.0, 15.0, 25.0, 17.0, -4.0, -23.0, -29.0]),
    ('AH0', 0.801, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]),
    ('G EY1 N', 0.839, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -7.0, -4.0, 3.0, 9.0, 9.0, 0.0, -14.0, -24.0, -24.0, -10.0, 10.0, 22.0, 21.0, 6.0, -14.0, -28.0, -28.0, -13.0, 7.0, 21.0, 22.0, 9.0, -11.0, -27.0, -29.0, -17.0, 3.0, 19.0, 23.0, 12.0, -8.0, -27.0, -36.0, -32.0, -22.0, -15.0, -22.0]),
]
SUNG_PATCH = {"extends": "voice-speech", "synth": {"pitch": {"mod": [{"amount": 0.01, "src": "expr.f0"}], "value": 0}}}
SUNG_AT = (105, 121)


def sung_notes():
    """v6: in the peak the hook is SUNG - each syllable on the hook's own partial, in whichever lobe the weather is in."""
    out = []
    for bar in SUNG_AT:
        lb = lobe_at(bar)
        for (at, n, ln, v), (ph, vel, f0) in zip(HOOK, SUNG):
            out.append({"at": round(b0(bar) + at, 4), "len": round(ln * 0.95, 3), "ph": ph,
                        "pitch": mm(partial(n, lb, 0)), "vel": vel, "expr_path": {"f0": f0}})
    return out


# v8: chirper-one's FM bell from t10 (borrowed, credited): t10 ends tolling D, then a Picardy D-F#-A; t11 begins with the
# SAME bell tolling only the F# - the common tone - every two bars, fading, while the F# harmonic-seventh pad grows from it
BELL = {"synth": {"layers": [{"name": "m", "ratio": 3.5, "audible": False},
                             {"wave": "sine", "pm": [{"from": "m", "depth": {"value": 0.3, "mod": [{"src": "env.bright", "amount": 2.6}]}}]}],
                  "env": {"bright": {"a": "1ms", "d": "450ms", "s": 0, "r": "200ms"}},
                  "amp": {"a": "2ms", "d": "1.1s", "s": 0.25, "r": "300ms"}}}


def toll_notes():
    out = []
    out.append({"at": b0(EYE[0]), "len": 7.5, "pitch": "m66", "vel": 0.72})   # v12: one toll in the eye
    for i, bar in enumerate((1, 3, 5, 7)):
        for pc in (("m62", "m66") if i == 0 else ("m66",)):      # first toll keeps t10's D with the F#; then the D drops away
            out.append({"at": b0(bar), "len": 7.5, "pitch": pc, "vel": round((92 - i * 9) / 127, 3)})
    return out


def wt_lane():
    """The wavetable position from x, once a bar: 0 (lobe F#, x -20) to 1 (lobe C#, x +20)."""
    return [[f"{b0(bar):.2f}b", round(max(0.0, min(1.0, (state(bar)[0] + 20) / 40)), 3)] for bar in range(1, BARS + 1)]


def tempo_map():
    """v5: THE TEMPO FOLLOWS THE WEATHER - from bar 17 to 136 a point every four bars at 120 + (z - 24)/5 bpm (clamped to
    +-3), ramped between: the groove leans forward and back as the storm passes; back to 120 before the ritardando."""
    pts = [{"at": "0b", "bpm": 120}, {"at": f"{b0(17):.0f}b", "bpm": 120}]
    for bar in range(21, 137, 4):
        z = state(bar)[2]
        pts.append({"at": f"{b0(bar):.0f}b", "bpm": round(120 + max(-3.0, min(3.0, (z - 24) / 5)), 2), "ramp": True})
    pts += [{"at": f"{b0(141):.0f}b", "bpm": 120, "ramp": True}, {"at": f"{b0(BARS - 15):.0f}b", "bpm": 120},
            {"at": f"{b0(BARS + 1):.0f}b", "bpm": 112, "ramp": True}]
    return pts


def lanes():
    level = {"intro": -6, "A": -3, "B": -1, "break": -5, "C": 0, "outro": -6}
    pts = []
    for name, a, z in SECTIONS:
        if pts:
            pts.append([f"{b0(a) - 0.25:.2f}b", pts[-1][1]])
        pts.append([f"{b0(a):.2f}b", float(level[name])])
    return pts


def main():
    write_music()
    write_rain()
    write_thunder()
    write_wind()
    eye_clear()
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    # v6: the wavetable scans VOWELS (u o a e i), not a resonant sweep: the weather speaks, no squelch
    lead_patch = {"extends": "juno-pad", "synth": {"layers": [
        {"type": "wavetable", "table": "vowel", "position": {"value": 0, "mod": [{"src": "auto.wt", "amount": 1}]}}],
        "amp": {"a": "4ms", "d": "180ms", "s": 0.55, "r": "120ms"}}}
    flips = sum(1 for i in range(1, len(ORBIT)) if (ORBIT[i][0] > 0) != (ORBIT[i - 1][0] > 0))
    song = {
        "about": "chirpers - A Light Left On (chirpers VIII), track 11 by chirper-three: butterfly house. The Lorenz "
                 "attractor steers every dial - the key (its two lobes), a wavetable lead, a trance gate, sampled chops - "
                 "in the harmonic series over C# and F#; a dynamics showcase (pump, gate, ott, transient, glue). "
                 "Generated by compose/chirpers8/src/chirpers8-t11.py.",
        "tempo": tempo_map(),
        # v5: A SECOND WEATHER - the engine's own Lorenz system (a var) pans the chops and the lead
        "vars": {"gust": {"system": {"type": "lorenz", "axis": "x", "n": 1400, "range": [-0.7, 0.7]}, "every": "1/2"}},
        "tail": "0.5s",
        "loudness": -11,
        "volume": "0dB",
        "tracks": [
            tr("lead", lead_patch, gain="-10dB", pan=0.15, sends={"hall": "-10dB", "dly": "-12dB"},
               auto={"wt": {"points": wt_lane()}},
               fx=[{"type": "pitch", "semitones": 7.02, "mix": 0.3}, {"type": "filter", "kind": "lp", "cutoff": 6000},
                   {"type": "pan", "pan": {"value": 0, "mod": [{"src": "var.gust", "amount": -0.6}]}}]),
            {"name": "singer", "patch": SUNG_PATCH, "gain": "-10dB", "pan": 0.05, "sends": {"hall": "-6dB", "dly": "-12dB"},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": 160}], "notes": sung_notes()},   # v6: the sung hook
            {"name": "toll", "patch": BELL, "gain": "-12dB", "pan": -0.15, "sends": {"hall": "-8dB", "dly": "-12dB"},
             "notes": toll_notes()},                                                       # v8: the bell carries over
            tr("wind", WIND, gain="-14dB", pan=0.25, sends={"hall": "-8dB"}),           # v11: the wind in the gap
            tr("thunder", THUNDER, gain="-6dB", pan=-0.1, sends={"hall": "-4dB"}),          # v10: thunder at the flips
            tr("rainL", "celesta", gain="-8dB", pan=-0.6, sends={"hall": "-8dB"}),       # v9: rain indoors
            tr("rainR", "celesta", gain="-8dB", pan=0.6, sends={"hall": "-8dB"}),
            tr("pad", "juno-pad", gain="-11dB", pan=-0.15, sends={"hall": "-8dB"},
               fx=["gate key=gtrig threshold=-40dB attack=1ms release=40ms", "ott depth=0.3", WIDTH_FX],
               auto={"wd": {"points": width_lane()}}),                                      # v13
            tr("gtrig", "machine-kit", gain="-80dB"),
            tr("bass", "808", gain="-11dB", fx=[{"type": "pump", "on": "kick", "depth": "-9dB", "release": "1/6",
                                                "curve": 0.6}]),
            tr("chops", "chopper", gain="-12dB", sends={"dly": "-8dB"},
               fx=[{"type": "pan", "pan": {"value": 0, "mod": [{"src": "var.gust", "amount": 1}]}}]),
            tr("kick", "machine-kit", gain="-11dB", fx=["transient attack=6 sustain=-4"]),
            tr("light", "music-box", gain="-8dB", sends={"hall": "-6dB"}),            # v2: the handover
            tr("hum", "partial", gain="-16dB"),          # v2: t12's hum, begun early (v3: +6 dB, meeting it)
            tr("ride", "machine-kit", gain="-10dB", pan=-0.3, sends={"room": "-12dB"}),
            {"name": "voice", "patch": "voice-speech", "gain": "-10dB", "pan": 0.1, "sends": {"dly": "-10dB"},
             "auto": radio_lanes(), "notes": voice_notes(),
             "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial", "amount": 1}]}, "fade": 0.3,
                     "drift": 0.04, "hiss": "-32dB", "whistle": "-34dB", "seed": 5},
                    {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.rg", "amount": 1}]}}]},
            tr("hats", "machine-kit play.humanize.drunk=4ms", gain="0dB", pan=0.2, fx=["ott depth=0.35"]),
            tr("clap", "machine-kit play.humanize.nudge.cp=8ms", gain="-5dB", sends={"room": "-8dB"}),
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=1.0s mix=1 predelay=10ms", "hp cutoff=250"]},
                  "hall": {"fx": ["reverb kind=hall decay=2.8s mix=1 predelay=25ms", "hp cutoff=250", WIDTH_FX],
                           "auto": {"wd": {"points": width_lane()}}},                     # v13: the room breathes
                  "dly": {"fx": ["delay time=3/16 mix=1 feedback=0.4", "hp cutoff=400", "lp cutoff=4000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=280 q=0.9 gain=-4dB",
                                                    "highshelf cutoff=5000 gain=5dB"]},     # v2: the album's envelope
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          "glue makeup=2dB",
                          {"type": "compressor", "threshold": "-12dB", "ratio": 8, "attack": "0.3ms",
                           "release": "60ms", "makeup": "0dB"}],
                   "auto": {"dyn": {"points": lanes()}}},
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print("wrote", OUT, "bars", BARS, "lobe flips", flips,
          "lobes by section", {n: sum(lobe_at(b) for b in range(a, z + 1)) for n, a, z in SECTIONS})


if __name__ == "__main__":
    main()
