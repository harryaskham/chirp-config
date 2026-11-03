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


# v16: A THUNDER SHEET - before recordings, theatres made thunder INDOORS by shaking a big metal sheet; every thunder
# now has one: a modal PLATE (the album's last unused physical family) struck near its edge, so its dense upper modes
# ring, with a large bloom - and SHAKEN, a roll of ~7 strikes over a beat and a half, decaying, at a slightly
# different low pitch each time: the storm in this song is stage weather, made indoors
SHEET = {"synth": {"layers": [{"type": "modal", "modes": "plate", "decay": "4s", "damp": 0.03, "bloom": 0.8,
                               "strike": 0.8}],
                   "amp": {"a": "1ms", "d": "4s", "s": 0, "r": "2s", "curve": 3}}}
SHEET_ROLL = (0.0, 0.11, 0.24, 0.4, 0.6, 0.86, 1.2)


def sheet_roll(bar, vel, name="sheet"):
    rng = random.Random(1000 + bar)
    nt = f"m{rng.choice((37, 38, 39, 40))}"
    for k, at in enumerate(SHEET_ROLL):
        part(name).add(b0(bar) + at + rng.uniform(-0.02, 0.02), 1.5, nt, max(30, int(vel * (1 - 0.11 * k)) + rng.randint(-5, 5)))


def write_thunder():
    for bar in range(2, BARS + 1):
        if lobe_at(bar) == lobe_at(bar - 1):
            continue
        sec = sec_of(bar)
        if sec in ("A", "B", "C"):
            part("thunder").add(b0(bar), 8.0, "m28.000", 84 + int(state(bar)[2]))
            sheet_roll(bar, 70 + int(state(bar)[2]))                                  # v16: the sheet
        elif sec == "break":
            part("thunder").add(b0(bar), 8.0, "m28.000", 52)
            sheet_roll(bar, 50)


# v11: THE WIND IN THE GAP - pink noise through a feedback COMB that whistles at its cutoff and harmonics, the
# cutoff steered by the attractor's own var.gust (x, +-0.7) over 1.2 octaves (~390-1250 Hz), long swells, slow gusts;
# strongest in the break, where the rain stops and only the wind is left; the intro and outro stay still
WIND = {"synth": {"layers": [{"type": "noise", "color": "pink"}],
                  "filters": [{"kind": "comb", "q": 12, "cutoff": {"value": 700, "mod": [{"src": "var.gust", "amount": 1.2}]}},
                              {"kind": "lp", "cutoff": 2500}],
                  "amp": {"a": "2s", "d": "0ms", "s": 1, "r": "3s"}},
        "fx": [{"type": "tremolo", "rate": 0.3, "depth": 0.55}]}
WIND_VEL = {"A": 58, "B": 76, "break": 100, "C": 84}


# v29 (ROUND TYPE: whole; gendyn pinned 6014b933): THE AEOLIAN HARP. Wind across a string makes it sound its HARMONIC
# PARTIALS - the series this whole song is built from - and the harder the wind, the higher the partial. Through the
# break and C (81-136), where the wind is strongest, strings the weather plays by itself: a GENDYN voice (Xenakis's
# stochastic synthesis - a living tone that never quite repeats), one new string a bar, each ringing three bars (or to
# the next lobe flip), three at once panned left/centre/right; the attractor's HEIGHT (z) at that bar picks which
# partial (8-16) of the lobe's fundamental sounds, an octave up; and the Lorenz var.gust modulates the gendyn's amp and
# time, so the tone wavers as the wind gusts. Two systems coupled: the Lorenz weather plays Xenakis's strings.
AEOLIAN = (81, 136)
AEOL_PATCH = {"synth": {"layers": [{"type": "gendyn", "gendyn": {
    "points": 10, "amp": {"value": 0.04, "mod": [{"src": "var.gust", "amount": 0.04}]},
    "time": {"value": 0.01, "mod": [{"src": "var.gust", "amount": 0.008}]}, "spread": 0.05}}],
    "amp": "1.2s 1 1 2.5s", "filters": [{"kind": "lp", "cutoff": 2600, "q": 0.6}, {"kind": "lp", "cutoff": 2600, "q": 0.5}]}}


def aeolian():
    for bar in range(AEOLIAN[0], AEOLIAN[1] + 1):
        z = state(bar)[2]
        n = PARTIALS[max(0, min(8, round((z - 10) / 30 * 8)))]
        lb = lobe_at(bar)
        ring = 1
        while ring < 3 and bar + ring <= AEOLIAN[1] + 2 and lobe_at(bar + ring) == lb:
            ring += 1
        part(f"aeolian{bar % 3}").add(b0(bar), b0(bar + ring) - b0(bar) - 0.1, mm(partial(n, lb, 1)),
                                      92 if sec_of(bar) == "break" else 72)


# v30 (ROUND TYPE: section, w3 1:03-1:35 = A's second half, flagged static / little new vs w2; terrain pinned
# 758ba1dc): FROST ON THE GLASS. A slow descant - one long note every two bars, climbing the lobe's partials 8 -> 16 an
# octave up, as frost spreads up a window - on WAVE TERRAIN synthesis (an orbit circling a surface of hills, its heights
# the wave): a lane widens the orbit across the sixteen bars, so the tone OPENS from hollow (odd harmonics only, like
# a clarinet) to glassy and bright - reshaped, not filtered - and the Lorenz var.gust pushes the orbit off centre, so
# even harmonics join when the wind blows; ratio 1.003 lets it drift. Slow and sparse on purpose: busy mid-register
# lines here merged A's second half into B (v28's first placement).
FROST = (33, 48)
FROST_PARTIALS = (8, 9, 10, 11, 12, 13, 14, 16)
FROST_PATCH = {"synth": {"layers": [{"type": "terrain", "terrain": {
    "surface": "sines", "ratio": 1.003, "k": 1.2,
    "rx": {"value": 0.3, "mod": [{"src": "auto.fr", "amount": 0.6}]},     # rx 1.3 put a 6-7 kHz harmonic on top
    "ry": {"value": 0.3, "mod": [{"src": "auto.fr", "amount": 0.5}]},
    "cx": {"value": 0.0, "mod": [{"src": "var.gust", "amount": 0.4}]}}}],
    "amp": "700ms 1 0.9 1.8s"}}


def frost():
    for i, n in enumerate(FROST_PARTIALS):
        bar = FROST[0] + 2 * i
        lb = lobe_at(bar)
        ring = 1
        while ring < 2 and lobe_at(bar + ring) == lb:
            ring += 1
        part("frost").add(b0(bar), b0(bar + ring) - b0(bar) - 0.1, mm(partial(n, lb, 1)), 80)


def write_wind():
    for name, a, z in SECTIONS:
        if name in WIND_VEL:
            part("wind").add(b0(a), b0(z + 1) - b0(a) - 0.1, "m60.000", WIND_VEL[name])


# v12: THE EYE OF THE STORM - at the peak's most extreme moment (bar 115, z ~40, right after the forecast's 'good
# visibility, falling slowly') the storm stops dead for two bars: only the wind still whistling in the gap and the
# opening's bell struck once on F#; then the storm crashes back with a thunderclap at 117
EYE = (115, 117)
EYE_KEEP = {"wind", "hum", "aeolian0", "aeolian1", "aeolian2"}     # v29: the harp keeps singing in the eye


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
            line = BASS_LINE[(bar - 17) % 2] if sec in ("A", "B", "C") else None
            for e in range(8):
                n = line[e] if line else (2 if e % 4 != 3 else 3)
                part("bass").add(b0(bar) + e * 0.5, 0.45, mm(partial(n, lb, 0)), 100 if e % 2 == 0 else 84)
        # v4: THE HOOK, rearranged by the weather - in A, B and C every two-bar phrase plays the hook in one of four
        # forms (original, retrograde, inversion round the 12th partial, a partial up), chosen by y at its start
        if sec in ("A", "B", "C") and (bar - 17) % 2 == 0 and hook_on(bar):
            x, y, z = state(bar)
            form = 0 if bar in (17, 19, 49, 97) + SUNG_AT else int(max(0, min(3, (y + 25) / 50 * 4)))   # each section states it plain
            for at, n, ln, v in hook_form(form):
                part("lead").add(b0(bar) + at, ln * 0.92, mm(partial(n, lb, 0)), v)
            continue_lead = False
        else:
            continue_lead = True
        # THE LEAD (now the break's and the outro's): a wavetable, a partial chosen by y each eighth
        weather = sec in ("A", "B", "C") and not hook_on(bar)                   # v17: the lead improvises
        if continue_lead and (sec == "break" or (sec == "outro" and bar < 153) or weather):
            for e in range(8):
                x, y, z = state(bar, e * 2)
                x2, y2, z2 = state(bar, min(15, e * 2 + 1))
                if abs(y2 - y) > (0.6 if sec == "break" else 0.9 if weather else 1.2):
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
                    part("clap").add(b0(bar) + b + 0.02, 0.5, "sl", 90 + hand.randint(-4, 4))   # v26: a brush slap


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


# v17: FEWER RETURNS (Harry on t1: 'fewer returns', 'a tune good to hear'): the hook played every two bars through A, B
# and C - 52 statements back to back; now each section alternates 8 bars of hook with 8 bars of WEATHER, where the
# lead stops quoting and improvises on the partials as the attractor's y moves (as it does in the break); the hook
# keeps each section's plain first statement and both sung bars (the voice carries it there)
# v18: A BASS THAT SINGS ('a tune good to hear', Harry on t1): through A, B and C the bass pumped partial 2 with a 3
# on every fourth eighth - rhythm without a line. Now a two-bar line climbs and falls through the low harmonic series
# in just intonation - 2, 5/2 (the pure major third), 3, 7/2 (the septimal seventh, a blue, subtly-off lean), 4 -
# rising as the hook rises and falling home with it; the outro keeps the plain pulse as the weather calms
BASS_LINE = ([2, 2, 2.5, 3, 2, 2.5, 3, 3.5],
             [4, 3.5, 3, 2.5, 3, 2.5, 2, 2])


# v20 (SECTION round, w3 1:03-1:35, bars 33-48 - 'static, little new vs w2'): SOMEONE IN ANOTHER ROOM WHISTLES THE
# TUNE - in w3's weather bars (41-48), where the lead stops quoting, a low whistle (breathy fipple, unused on the
# album) answers with the hook twice (41, 45), soft, far right, in the room, a hair behind the beat - someone in the
# next room who caught the tune; on the partials of whichever lobe the weather is in. Its own track, listed last.
WHISTLE_AT = (41, 45, 153)                  # v22: and once more in the outro, softer, farther, as the light goes

# v21 (SECTION round, w5 2:08-2:40, bars 65-80, the second half of B - 'static, little new vs w4'; Harry: do more
# each round): THREE CHANGES IN THE WINDOW. (1) THE HOOK IN HARMONY (65-72): for the first time the hook gets a second
# voice - every note a pure 5/4 major third above (partial n x 5/4), following whichever form the lead plays - on the
# physical modal-vibes. (2) A COUNTER-LINE IN THE WEATHER (73-80): where the lead improvises, a physical modal-marimba
# rolls the weather lobe's harmonic chord (partials 8, 10, 12 and the septimal 14) in soft rising and falling
# eighths - the rain on the roof turning into notes. (3) A BREATH BEFORE THE BREAK: the drums drop for the last two
# beats of bar 80 (silenced at velocity 1, held notes cut - every track keeps its note count), so the break arrives
# from a held breath. New parts on new tracks, listed last.
HARM = (65, 72)
# v22 (ROUND TYPE: whole; Harry 'do more each round'): THE HARMONY GROWS THROUGH THE PEAK - the 5/4 voice now carries
# through every hook phrase of C as well (97-136, under both sung statements too), and in C's last hook group
# (129-136) a THIRD voice joins on chirper-two's physical modal-glock (a bell's minor-third tierce would fight the
# triad), a pure 3/2 fifth above: the hook ends the
# climax as a just major triad. And the whistle from A comes back once in the outro (153), softer and farther off.
HARM_BARS = list(range(65, 73)) + list(range(97, 137))
FIFTH = (129, 136)
RAINMAR = (73, 80)
ROLL = (8, 10, 12, 14, 12, 10, 8, 10)


def hook_harmony():
    out = []
    for bar in HARM_BARS:
        if (bar - 17) % 2 or not hook_on(bar):
            continue
        x, y, z = state(bar)
        form = 0 if bar in (17, 19, 49, 97) + SUNG_AT else int(max(0, min(3, (y + 25) / 50 * 4)))
        lb = lobe_at(bar)
        for at, n, ln, v in hook_form(form):
            out.append({"at": round(b0(bar) + at, 4), "len": round(ln * 0.92, 3),
                        "pitch": mm(partial(n * 1.25, lb, 0)), "vel": round(0.7 * v / 96, 3)})
    return out


def hook_fifth():
    out = []
    for bar in range(FIFTH[0], FIFTH[1] + 1):
        if (bar - 17) % 2 or not hook_on(bar):
            continue
        x, y, z = state(bar)
        form = 0 if bar in (17, 19, 49, 97) + SUNG_AT else int(max(0, min(3, (y + 25) / 50 * 4)))
        lb = lobe_at(bar)
        for at, n, ln, v in hook_form(form):
            out.append({"at": round(b0(bar) + at, 4), "len": round(ln * 0.92, 3),
                        "pitch": mm(partial(n * 1.5, lb, 0)), "vel": round(0.62 * v / 96, 3)})
    return out


# v23 (ROUND TYPE: section, w8 3:44-4:16, bars 113-128; Harry 'do more each round'): THREE CHANGES around the eye.
# (1) SUN THROUGH THE EYE (115-117): in the clearing a harp climbs the harmonic series slowly - partials 8 to 16 of
# the song's own fundamental - light through the cloud. (2) THE BACK WALL (118-128): behind a real eye the winds are
# strongest; thunder drums on the harmonic series (a pitched modal-tom, eighths on the lobe's 2nd and 3rd partials,
# growing 60 -> 100) and a kick pushed before each bar bring the storm back harder than it left. (3) THE WIND TURNS
# ROUND: behind the eye the hook's harmony voice (vibes) crosses to the other side of the stereo field (pan lane).
SUNBEAM = (115, 8, 16, 1.25)
BACKWALL = (118, 128)


def sunbeam():
    bar, lo, hi, step = SUNBEAM
    lb = lobe_at(bar)
    return [{"at": round(b0(bar) + i * step, 4), "len": 4.0, "pitch": mm(partial(n, lb, 0)),
             "vel": round(0.5 + 0.03 * i, 3)} for i, n in enumerate(range(lo, hi + 1))]


def backwall():
    toms, push = [], []
    a, z = BACKWALL
    for bar in range(a, z + 1):
        lb = lobe_at(bar)
        g = (bar - a) / (z - a)
        for e in range(8):
            toms.append({"at": round(b0(bar) + e * 0.5, 4), "len": 0.45, "pitch": mm(partial(2 if e % 2 == 0 else 3, lb, 0)),
                         "vel": round((0.47 + 0.32 * g) * (1.0 if e % 4 == 0 else 0.82), 3)})
        if bar < z:
            push.append({"at": round(b0(bar) + 3.75, 4), "len": 0.25, "pitch": "k", "vel": 0.72})
    return toms, push


# v24 (ROUND TYPE: section, w9 4:16-4:48 - flagged 'little new vs w8' - its second half, bars 137-144, the storm
# passing into the outro): (1) DRIPS FROM THE GUTTERS - single high partials of the harmonic series on a MUSIC BOX,
# timed by the attractor itself (a sixteenth drips when |13.7y + 3.1z| mod 1 falls under a density that thins across
# the eight bars), irregular and deterministic; the closer's first sound is a music-box note. (2) THE LAST THUNDER,
# FAR OFF - one thunder-sheet roll at 140, soft, low-passed and drowned in hall: the storm a long way away.
DRIPS = (137, 144)
FAR_THUNDER = 140


def drips():
    out = []
    a, z = DRIPS
    for bar in range(a, z + 1):
        lb = lobe_at(bar)
        dens = 0.3 * (1 - 0.6 * (bar - a) / (z - a))
        for s in range(16):
            x, y, zz = state(bar, s)
            h = abs(13.7 * y + 3.1 * zz) % 1
            if h < dens:
                n = (8, 9, 10, 12, 14, 16)[int(abs(zz)) % 6]
                out.append({"at": round(b0(bar) + s / 4, 4), "len": 1.5, "pitch": mm(partial(n, lb, 1)),
                            "vel": round(0.45 + 0.25 * (h / max(dens, 1e-9)), 3)})
    return out


def rain_marimba():
    out = []
    for bar in range(RAINMAR[0], RAINMAR[1] + 1):
        lb = lobe_at(bar)
        for e, n in enumerate(ROLL):
            out.append({"at": round(b0(bar) + e * 0.5, 4), "len": 0.45, "pitch": mm(partial(n, lb, 0)),
                        "vel": 0.62 if e % 4 == 0 else 0.48})
    return out


def breath():
    a, z = b0(80) + 2, b0(81)
    for name in ("kick", "hats", "clap"):
        ev = []
        for s, ln, head, vel in P[name].ev:
            if a <= s < z:
                ev.append((s, ln, head, 1))
            elif s < a < s + ln:
                ev.append((s, a - s - 0.02, head, vel))
            else:
                ev.append((s, ln, head, vel))
        P[name].ev = ev


def whistle_notes():
    out = []
    for bar in WHISTLE_AT:
        lb = lobe_at(bar)
        far = bar > 100                                  # v22: the goodbye is farther off and a little later
        for at, n, ln, v in HOOK:
            out.append({"at": round(b0(bar) + at + (0.1 if far else 0.06), 4), "len": round(ln * 0.9, 3),
                        "pitch": mm(partial(n, lb, 0)), "vel": round((0.42 if far else 0.62) * v / 96, 3)})
    return out


def hook_on(bar):
    a = next(a for name, a, z in SECTIONS if a <= bar <= z)
    return ((bar - a) // 8) % 2 == 0 or any(s <= bar < s + 2 for s in SUNG_AT)


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
# v26 (ROUND TYPE: palette; Harry 'do more each round'): BRUSHES AND A PLAYER'S BASS. The album's staples under the
# whole song change: the hats, the backbeat and the ride move from machine-kit (7 songs) to BRUSHES - taps, slaps and
# swishes, the sound of rain on a window, indoors - while the machine kick keeps the four-on-the-floor heart (a machine
# pulse under human brushes). An UPRIGHT BASS for the 808 was tried and refused: its pizzicato decays where the 808
# sustained, the sections' low-end signature blurred and seed 0's structure term fell 99 -> 88 (one section swallowed
# its neighbour, length cv 0.72 -> 1.1), with or without the brushes. Gain-matched by solo against the old
# patches (bars 25-28): brush hats came in +9.9 dB (-10 dB), the slap +7.2 dB and brighter (3.6 kHz centroid against
# the clap's 1.9; -7 dB and a 6 kHz low-pass - the cajon's lesson).
# v25 (ROUND TYPE: whole; Harry 'a tune good to hear', 'oblique words', 'do more each round'): THE HOOK GETS AN ANSWER.
# The peak sang one line twice; now the second statement (121) answers 'it rained in the second room again' with
# 'warm in the glass, and the weather stayed' - stresses on the hook's long notes (WARM, GLASS, WEATH-, STAYED): the
# glass is the window, the screen, and the closer's 'warm glass' at once; the weather stayed in - the title, answered.
# ('wires' was tried first: the voice splits it in two and the stresses slip.) The radio at 145 keeps the first line.
# And event_stable is on from here.
SUNG_B = [   # chirp tts --sing "C#5/4 D#5/8 F5/8 E5/4 G5/8 F5/8 D#5/4. C#5/8 C#5/2" "warm in the glass and the weather stayed" --humanize 0.4
    ('W AO1 R M', 0.85, [-55.0, -28.0, -9.0, 2.0, 5.0, 5.0, 2.0, 2.0, 6.0, 13.0, 17.0, 13.0, 1.0, -13.0, -18.0, -8.0, 13.0, 30.0, 31.0, 16.0, -6.0, -21.0, -21.0, -5.0]),
    ('IH0 N', 0.771, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -6.0, -5.0, 2.0, 10.0, 9.0, -3.0]),
    ('DH AH0', 0.791, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -5.0, 1.0, 7.0, 8.0, -1.0]),
    ('G L AE1 S', 0.865, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 1.0, 6.0, 14.0, 18.0, 13.0, -1.0, -16.0, -21.0, -8.0, 15.0, 32.0, 32.0, 14.0, -10.0, -25.0, -23.0, -4.0]),
    ('AH0 N D', 0.783, [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 1.0, 2.0, 9.0, 16.0, 16.0, 5.0]),
    ('DH AH0', 0.773, [-3.0, -3.0, -3.0, -3.0, -3.0, -4.0, -7.0, -7.0, -1.0, 8.0, 12.0, 4.0]),
    ('W EH1', 0.849, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -5.0, -1.0, 6.0, 9.0, 4.0, -8.0, -21.0, -23.0, -11.0, 9.0, 23.0, 21.0, 4.0, -17.0, -29.0, -24.0, -6.0, 15.0, 24.0, 17.0, -2.0, -22.0, -30.0, -20.0, 0.0, 19.0, 24.0, 13.0, -8.0]),
    ('DH ER0', 0.801, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -4.0, -3.0, 3.0, 10.0, 11.0, 2.0]),
    ('S T EY1 D', 0.839, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0, -7.0, -4.0, 2.0, 9.0, 9.0, 0.0, -13.0, -24.0, -24.0, -11.0, 9.0, 22.0, 21.0, 6.0, -14.0, -28.0, -28.0, -14.0, 6.0, 21.0, 22.0, 10.0, -10.0, -26.0, -29.0, -18.0, 2.0, 19.0, 23.0, 13.0, -6.0, -24.0, -30.0, -21.0, -3.0, 12.0, 15.0, 1.0, -26.0, -54.0, -75.0]),
]


def answer_harmony():
    """v25: the answer sung as a duet - a second voice a pure 5/4 third above (the vibes' line), quieter, opposite."""
    bar = SUNG_AT[1]
    lb = lobe_at(bar)
    return [{"at": round(b0(bar) + at + 0.02, 4), "len": round(ln * 0.95, 3), "ph": ph,
             "pitch": mm(partial(n * 1.25, lb, 0)), "vel": round(vel * 0.85, 3), "expr_path": {"f0": f0}}
            for (at, n, ln, v), (ph, vel, f0) in zip(HOOK, SUNG_B)]


def sung_notes():
    """v6: in the peak the hook is SUNG - each syllable on the hook's own partial, in whichever lobe the weather is in."""
    out = []
    for k, bar in enumerate(SUNG_AT):
        lb = lobe_at(bar)
        for (at, n, ln, v), (ph, vel, f0) in zip(HOOK, SUNG if k == 0 else SUNG_B):
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


# v14: THE WEATHER SINGS ONCE MORE FROM THE RADIO - in the outro, as the weather clears into the closer, the hook comes
# home one last time, SUNG THROUGH THE FORECAST'S RADIO: on the station as it begins, the dial drifting off (0 -> 0.3)
# as the phrase goes on, the voice receding into static; a gate lane keeps the radio silent outside the phrase
RADIO_SUNG_AT = 145


def radio_sung_notes():
    lb = lobe_at(RADIO_SUNG_AT)
    return [{"at": round(b0(RADIO_SUNG_AT) + at, 4), "len": round(ln * 0.95, 3), "ph": ph, "pitch": mm(partial(n, lb, 0)),
             "vel": round(vel * 0.9, 3), "expr_path": {"f0": f0}} for (at, n, ln, v), (ph, vel, f0) in zip(HOOK, SUNG)]


# v27 (ROUND TYPE: whole; the intro flagged static since the map began): THE RADIO IS SWITCHED ON AT THE START. In the
# intro someone indoors turns the dial looking for the forecast: from bar 3 the radio's static wanders between
# stations (the tune lane sweeping), the dial LOCKS as the hook arrives sung at bar 5, holds through the phrase, drifts
# off and closes before the band (bar 9). The radio at 145 becomes a return - the same station found again near the
# end - so the radio frames the song. Sung once (Harry: fewer returns).
RADIO_INTRO = (3, 5, 9)


def radio_intro_notes():
    a, sung, z = RADIO_INTRO
    lb = lobe_at(sung)
    return [{"at": round(b0(sung) + at, 4), "len": round(ln * 0.95, 3), "ph": ph, "pitch": mm(partial(n, lb, 0)),
             "vel": round(vel * 0.85, 3), "expr_path": {"f0": f0}} for (at, n, ln, v), (ph, vel, f0) in zip(HOOK, SUNG)]


def radio_intro_lanes():
    a, sung, z = (b0(x) for x in RADIO_INTRO)
    dial = [[0.0, 0.6], [a, 0.6], [a + 2, 0.35], [a + 4, 0.55], [a + 6, 0.3], [sung - 1.5, 0.15], [sung + 0.5, 0.0],
            [sung + 8, 0.0], [z - 1, 0.35]]
    gain = [[0.0, -80.0], [a - 0.05, -80.0], [a + 1, -6.0], [sung - 1, 0.0], [z - 1.5, 0.0], [z - 0.25, -80.0]]
    return {"dial3": {"points": [[f"{x:.2f}b", y] for x, y in dial]},
            "rg3": {"points": [[f"{x:.2f}b", y] for x, y in gain]}}


# v28 (ROUND TYPE: whole; wM's systems pinned ade7b930; section A flagged static, w2-w3): A SECOND WEATHER. The song
# runs on the Lorenz attractor, which SWIRLS; the Henon map JUMPS. (1) Through A's first hook group (17-24) a KALIMBA plays a
# line driven by the engine's henon gen - leaping where the lead glides, a second weather system crossing the first -
# on the tones the song's two harmonic-series lobes share (C#, F#, G# in octaves: partials 8/12/16 of C#, 6/8/9/16 of
# F#), so it sits consonant whichever lobe the weather is in. (2) A random WALK (the engine's walk system, a step
# every 4 beats) moves the pad's PAN through the whole song (vars on pans - chirper-two's lesson): the pad wanders.
HENON = (17, 24)          # 33-48 merged A's second half into B for the structure term (88.4, length cv 1.1)
HENON_POOL = (61.0, 66.0, 68.02, 73.0, 78.0, 80.02)


def radio_sung_lanes():
    a, z = b0(RADIO_SUNG_AT), b0(RADIO_SUNG_AT + 2) + 1
    return {"dial2": {"points": [["0b", 0.0], [f"{a:.2f}b", 0.0], [f"{z:.2f}b", 0.3]]},
            "rg2": {"points": [["0b", -80.0], [f"{a - 0.05:.2f}b", -80.0], [f"{a:.2f}b", 0.0], [f"{z:.2f}b", 0.0],
                               [f"{z + 0.5:.2f}b", -80.0]]}}


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
    sheet_roll(FAR_THUNDER, 70, "farsheet")              # v24: the last thunder, far off
    write_wind()
    aeolian()                                     # v29: the Aeolian harp
    frost()                                       # v30: frost on the glass
    eye_clear()
    breath()                                                     # v21: the drums breathe in before the break
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
        "vars": {"gust": {"system": {"type": "lorenz", "axis": "x", "n": 1400, "range": [-0.7, 0.7]}, "every": "1/2"},
                 "drift": {"system": {"type": "walk", "width": 16, "step": 1, "n": 180, "range": [-0.45, 0.45]},
                           "every": "4b"}},                                     # v28: the pad wanders through the house
        "tail": "0.5s",
        "loudness": -11,
        "event_stable": True,                     # v25: each note's draws from its track, beat and pitch (wM f5283535)
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
            tr("aeolian0", AEOL_PATCH, gain="-17dB", pan=-0.5, sends={"hall": "-6dB"}),     # v29
            tr("aeolian1", AEOL_PATCH, gain="-17dB", pan=0.05, sends={"hall": "-6dB"}),     # v29
            tr("aeolian2", AEOL_PATCH, gain="-17dB", pan=0.5, sends={"hall": "-6dB"}),     # v29
            tr("thunder", THUNDER, gain="-6dB", pan=-0.1, sends={"hall": "-4dB"}),          # v10: thunder at the flips
            tr("sheet", SHEET, gain="-10dB", pan=0.15, sends={"hall": "-6dB"}),            # v16: the thunder sheet
            tr("rainL", "celesta", gain="-8dB", pan=-0.6, sends={"hall": "-8dB"}),       # v9: rain indoors
            tr("rainR", "celesta", gain="-8dB", pan=0.6, sends={"hall": "-8dB"}),
            tr("pad", "juno-pad", gain="-11dB", pan={"value": -0.15, "mod": [{"src": "var.drift", "amount": 1}]},
               sends={"hall": "-8dB"},
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
            tr("ride", "brush-kit", gain="-10dB", pan=-0.3, sends={"room": "-12dB"}),
            {"name": "voice", "patch": "voice-speech", "gain": "-10dB", "pan": 0.1, "sends": {"dly": "-10dB"},
             "auto": radio_lanes(), "notes": voice_notes(),
             "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial", "amount": 1}]}, "fade": 0.3,
                     "drift": 0.04, "hiss": "-32dB", "whistle": "-34dB", "seed": 5},
                    {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.rg", "amount": 1}]}}]},
            {"name": "radiosinger", "patch": SUNG_PATCH, "gain": "-9dB", "pan": -0.1,
             "sends": {"dly": "-10dB", "hall": "-10dB"}, "auto": radio_sung_lanes(), "notes": radio_sung_notes(),
             "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial2", "amount": 1}]}, "fade": 0.3,
                     "drift": 0.04, "hiss": "-32dB", "whistle": "-34dB", "seed": 6},
                    {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.rg2", "amount": 1}]}}]},   # v14
            tr("hats", "brush-kit play.humanize.drunk=4ms", gain="-10dB", pan=0.2, fx=["ott depth=0.35"]),
            tr("clap", "brush-kit play.humanize.nudge.sl=8ms", gain="-12dB",
               fx=[{"type": "filter", "kind": "lp", "cutoff": 6000}], sends={"room": "-8dB"}),
            {"name": "whistle", "patch": "low-whistle", "gain": "-6dB", "pan": 0.6,
             "sends": {"room": "-4dB", "hall": "-10dB"}, "notes": whistle_notes()},   # v20: LAST (keeps every rng)
            {"name": "hookharm", "patch": "modal-vibes", "gain": "-9dB",
             "pan": {"value": -0.35, "mod": [{"src": "auto.wt", "amount": 1}]},          # v23: the wind turns round
             "auto": {"wt": {"points": [["0b", 0.0], [f"{b0(BACKWALL[0]):g}b", 0.0], [f"{b0(BACKWALL[0]) + 1:g}b", 0.7]]}},
             "sends": {"hall": "-8dB"}, "notes": hook_harmony()},                   # v21: the hook in harmony
            {"name": "rainmar", "patch": "modal-marimba", "gain": "-12dB", "pan": -0.55,
             "sends": {"room": "-8dB"}, "notes": rain_marimba()},                   # v21: rain into notes
            {"name": "hookfifth", "patch": "modal-glock", "gain": "-12dB", "pan": 0.4,
             "sends": {"hall": "-8dB"}, "notes": hook_fifth()},                     # v22: the triad at the peak
            {"name": "sunbeam", "patch": "harp", "gain": "-8dB", "pan": 0.3,
             "sends": {"hall": "-6dB"}, "notes": sunbeam()},                        # v23: sun through the eye
            {"name": "backwall", "patch": "modal-tom", "gain": "-12dB", "pan": -0.1,
             "sends": {"room": "-10dB"}, "notes": backwall()[0]},                   # v23: the back wall
            {"name": "kickpush", "patch": "machine-kit", "gain": "-13dB", "notes": backwall()[1]},   # v23
            {"name": "singerharm", "patch": SUNG_PATCH, "gain": "-10dB", "pan": 0.3,
             "sends": {"hall": "-6dB", "dly": "-12dB"}, "notes": answer_harmony()},     # v25: the answer as a duet
            {"name": "radiointro", "patch": SUNG_PATCH, "gain": "-11dB", "pan": 0.15,
             "sends": {"hall": "-12dB"}, "auto": radio_intro_lanes(), "notes": radio_intro_notes(),
             "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial3", "amount": 1}]}, "fade": 0.3,
                     "drift": 0.05, "hiss": "-18dB", "whistle": "-24dB", "seed": 9},
                    {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.rg3", "amount": 1}]}}]},   # v27
            {"name": "henon", "patch": "kalimba", "gain": "-14dB", "pan": 0.4, "sends": {"room": "-8dB"},
             "at": f"{b0(HENON[0]):g}b",
             "gen": {"type": "henon", "n": 8 * (HENON[1] - HENON[0] + 1), "len": "/8", "rest": 0.3,
                     "notes": " ".join(mm(p) for p in HENON_POOL)}},                        # v28: a second weather
            {"name": "drips", "patch": "music-box", "gain": "-11dB", "pan": 0.45,
             "sends": {"room": "-8dB", "hall": "-12dB"}, "notes": drips()},          # v24: after the storm
            tr("farsheet", SHEET, gain="-10dB", pan=-0.4, sends={"hall": "-2dB"},
               fx=[{"type": "filter", "kind": "lp", "cutoff": 900}]),               # v24: the last thunder, far off
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
    # v30: new tracks go LAST - a track inserted mid-list re-seeds every later track's noise and stochastic layers
    song["tracks"].append(tr("frost", FROST_PATCH, gain="-14dB", pan=0.3, sends={"hall": "-8dB"},
                             auto={"fr": {"points": [[f"{b0(FROST[0]):g}b", 0.0], [f"{b0(FROST[1] + 1):g}b", 1.0]]}}))
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print("wrote", OUT, "bars", BARS, "lobe flips", flips,
          "lobes by section", {n: sum(lobe_at(b) for b in range(a, z + 1)) for n, a, z in SECTIONS})


if __name__ == "__main__":
    main()
