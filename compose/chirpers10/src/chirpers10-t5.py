#!/usr/bin/env python3
"""chirpers10-t5 "False Summit" (chirper-zero): a riff that climbs for four minutes and ends where it began.

Harry, 15 Nov: "true djent, but that leverages audio illusions throughout mainly risers/shpehers but in djent style,
really make it a clear illlusory song, all about the illusions".

A false summit is the top you can see from below that turns out not to be the top. This piece is built on the two
illusions of endless motion, and here the BAND plays them, not a pad behind the band:

  the stair (Shepard)  A line climbs the album's six notes (F, G flat, A flat, B, C, E flat) and goes on climbing, an
                       octave every bar, and is never any higher. It is played by FOUR guitars a side, the same line
                       an octave apart. Each guitar climbs through four octaves and its fader follows where it is:
                       silent at the bottom, full in the middle, silent again at the top, where it drops back to the
                       bottom unheard. So every bar is the same bar, and every bar starts higher than the last.
                       (Three were tried first: a guitar then falls from full to nothing inside one bar and can be
                       followed out; with four, two neighbours are always within 6 dB of each other.)
  the turn (Risset)    Three of those guitars a side chug one bar of the low F at three speeds, each twice the one
                       below, and all three speed up together: each doubles its speed over four bars while the
                       fastest fades out and the slowest fades in. The riff gets faster and faster and is never any
                       faster. The speed rises in a straight line, not a curve, which makes the arithmetic close: in
                       four bars the three play three, six and twelve bars of the riff, so every fourth bar line all
                       three and the kit are together again. The kit keeps four in a bar throughout.

Common Time (track 1) turns three cells under one pulse; Odd Sympathy slides a riff against itself; Plain Hunt rings a
row through every order; Running Total adds a riff up. This piece's long cycle is one that never completes.

  the foot      bars 0-8      the stair alone on a Shepard tone (the plain form of the illusion first); then the guitars.
  the stair     bars 8-32     the band: the low string chugs under the line (F, F, A flat, E flat), the kick on the
                              line's six notes.
  the turn      bars 32-48    the chug at three speeds, speeding up for ever; the kit and the bass hold the bar.
  the descent   bars 48-72    the stair the other way, and all of it: the whole riff a step lower every bar, on the
                              three guitars and two basses. A tuning that keeps dropping and is never lower.
  the pole      bars 72-84    a breath: one chord through a filter that climbs for ever, the line slowly over it, and
                              a bass that is only its overtones (the ear supplies the note).
  both          bars 84-100   pitch and speed rise together, as a tape speeding up does: each guitar climbs an octave
                              as it doubles its speed. A riser that never arrives swells over it, and stops dead.
  the summit    bars 101-105  one bar of nothing. Then the stair's first bars, exactly: the same notes, the same
                              tempo. After all that climbing the band is where it started. One chord.

v1 is the SKELETON (track 2's terms: mine, my title, the whole shape standing, bare).
"""
import json
import math
import os

OUT = os.environ.get("C10T5_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t5.yaml"))
BPM = 100
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# ---------------------------------------------------------------------------------------------------- the material
SCALE = (0, 1, 3, 6, 7, 10)             # the album's notes over the ground: F Gb Ab B C Eb
ACC = (0, 3, 6, 9, 12, 14)              # where the line's six notes fall in the bar (sixteenths): 3 3 3 3 2 2
PEDAL = (0, 0, 3, 10)                   # the low string under the stair, a bar each: F F Ab Eb
PAT = "occoccoc"                        # the turn's bar, in eighths (3 3 2): o = open and accented, c = a muted chug
VOICES = 4                              # the guitars a side that carry the stair, an octave apart
ROLES = 3                               # the speeds of the turn, an octave of speed apart (a fourth guitar rests each cycle)
FLOOR = -70.0
CYCLE = 4                               # bars in which the turn doubles its speed

# ---------------------------------------------------------------------------------------------------- the form (bars)
FOOT = 0
RISE = FOOT + 8
TIME = RISE + 24
FALL = TIME + 4 * CYCLE
POLE = FALL + 24
BOTH = POLE + 12
STOP = BOTH + 4 * CYCLE
HOME = STOP + 1
END = HOME + 4
NB = END + 3
assert (RISE - FOOT) % 4 == 0 and (TIME - RISE) % len(PEDAL) == 0 and (FALL - TIME) % CYCLE == 0 and (STOP - BOTH) % CYCLE == 0

# the guitars' register: four octaves from the low string up, so the bell is fullest two octaves over it (F3)
LINE_BASE = int(os.environ.get("C10T5_LINEBASE", str(F1)))
RIFF_BASE = F1
# each illusion's trim on the three guitars' faders, dB: the line ; the turn ; the descent ; both
TRIM = dict(zip(("line", "time", "fall", "both"), (float(x) for x in os.environ.get("C10T5_TRIM", "1;3;1.5;3").split(";"))))
# v2: THE ILLUSIONS HOLD, AND THE JOINS ARE RISERS (whole song).
# ONE CABINET A SIDE. chirp-eco's new `tools/endless.py` read v1: inside a bar the stair holds (no saw-tooth), but the
# eight guitars did not repeat every bar, they repeated every FOUR (+0.3 -0.8 -0.2 +0.7 dB by bar; 6 dB of movement
# at 60-120 Hz), and in the turn the third and fourth cycles were 1.6 to 2 dB over the first two. Each of the eight had
# its own speaker cone and its own place in the stereo, so WHICH speaker held WHICH octave came round every four bars:
# a cycle the ear could count. Now the four on a side share one cone and one place: a bar is the same bar.
# the pan of the four a side. "" = v1 (a cone and a pan each).
ONE = os.environ.get("C10T5_ONE", "0.7")
# THE JOINS ARE RISERS, ON THE GUITARS. Harry asked for "mainly risers/shpehers but in djent style". The song's
# sections now hand over on a RUN: the eight guitars pick a semitone to the sixteenth on the same bell, so the run
# climbs four thirds of an octave a bar and is never higher (falling, at the end of the descent). Two bars each: into
# the turn (bars 30-32, rising), out of the descent (70-72, falling), and out of the pole into both (82-84, rising,
# with the riser that never arrives). Under the two rising ones the snare doubles its speed into the bar line.
# bars of run at a join ; the eight guitars' trim in it, dB ; the snare's gain in its build, dB. "" = v1 (a tom fill).
RUNS = os.environ.get("C10T5_RUNS", "2;0;-3")
# THE KIT PLAYS ONE TOO. In the pole (the breath) the hat's quarters become a tick that speeds up for ever: the
# engine's own `risset` on a kit track (three copies an octave of speed apart, each doubling in four bars; it works
# there because a drum has no amp to flatten the copies' fades). The plain form of the turn, heard alone.
# the tick's gain ; its accent's and its other strokes' velocity ; bars to double its speed. "" = v1 (hat quarters).
TICK = os.environ.get("C10T5_TICK", "22dB;0.9;0.6;4")
# THE FIRST READ AGAINST THE RECORDS, BY PART (v1, `stembal --id`), and what it moved:
#   the stair was 3.7 dB over the eleven records at 250-500 Hz, and the Shepard tone held 57% of that band: it comes
#     down 2.5 dB under the band (and is as it was where it is alone); and 2.3 dB short at 60-120 Hz: the bass 1.5 dB up.
#   the turn was 2.9 dB short at 60-120 Hz and 2.8 over at 120-250: the bass held ONE LONG NOTE a bar there, and a long
#     note of this bass is all 120-250 Hz (alone: 60-120 Hz 7.3 dB under its total, 120-250 Hz 2.3 under; chugged it is
#     3.6 and 6.4). It now strikes every beat (in both, too): four in a bar with the kit, against the guitars' turn.
#   the descent was 2.4 dB over at 120-500 Hz, part of it the falling rumble: 2 dB off it.
# strokes of the bass to the bar in the turn and in both ("" = v1: one long note).
ANCHOR = os.environ.get("C10T5_ANCHOR", "4")
# v3: THE STAIR HAS A TUNE (whole song). The line was the scale, straight up: the plain form, and right for the first
# eight bars. But a scale is not a tune, and the band played it for twenty-two bars. From bar 16 the line is a FIGURE:
# up two steps of the scale, back one, up two, back one (F A-flat G-flat B A-flat C | B E-flat C F E-flat G-flat), six
# notes on the bar's 3 3 3 3 2 2 as before, each bar starting three steps above the last. So it is a two-bar tune that
# ends an octave above where it began and begins again there: it climbs an octave every two bars and is never higher.
# The same eight guitars on the same bell play it; the kit takes the backbeat where it comes in (it was at bar 20).
# the bar the figure starts ; its six notes, in steps of the scale over the bar's first ; steps a bar climbs. "" = v2.
FIGURE = os.environ.get("C10T5_FIGURE", "16;0,2,1,3,2,4;3")
# THE EIGHT GUITARS' OWN REGISTER. Read against the eleven records by part (v2), the stair stood 3.7 dB over them at
# 500 Hz-1 kHz and the eight guitars held 58% of that band (both: 2.8 over). One eq band on each of the eight.
# frequency : q : dB. "" = v2.
VEQ = os.environ.get("C10T5_VEQ", "700:1:-2.5")
# v4: THE LEAD COMES DOWN (section round, 0:57-1:12: the stair's last six bars before the run; the map called the
# stretch static, and from the band's entry at 0:19 to the turn at 1:16 nothing JOINED). A lead guitar comes in over
# the tune and does the one thing nothing else in this song does: it really moves. It comes DOWN the scale, a note to
# the half bar, two octaves in six bars (F5 to F3), and lands on the low F exactly where the guitars' run begins. In
# those six bars the tune under it climbs three octaves and is no higher; the lead falls two and is two octaves lower.
# So the one honest line in the song shows the stair up for what it is. It is the library's `lead-tape` (the
# sustaining 8-string into a dark tape echo and a wide hall), on no other track of the album.
# the patch ; its gain ; the bar it starts ; its top note (MIDI) ; the eight guitars under it, dB. "" = v3.
# (At the patch's first gain, -16 dB, it read 23 dB under the mix: not there. 14 dB went on at the bench.)
LEAD = os.environ.get("C10T5_LEAD", "lead-tape;-2dB;24;77;-1")
LANE = {v: [(0.0, FLOOR)] for v in range(VOICES)}       # each voice's fader, (beat, dB)
BLANE = {w: [(0.0, FLOOR)] for w in range(2)}           # the descent's two basses
KEY = [(0.0, 0)]                                        # the ground under the bass's eq, (beat, semitones over F)


def bell(x):
    """A voice's level (amplitude) at x in 0..1 of its way from the bottom to the top: nothing at either end. Three
    voices a third of the way apart always add up to the same power."""
    return 0.5 - 0.5 * math.cos(2 * math.pi * (x % 1.0))


def db(a):
    return max(FLOOR, 20 * math.log10(a)) if a > 0 else FLOOR


def step(lane, beat, level):
    """The fader jumps to `level` at `beat`."""
    t, last = lane[-1]
    level = round(level, 2)
    if level == last:
        return
    if beat - 0.01 > t:
        lane.append((round(beat - 0.01, 4), last))
    lane.append((round(beat, 4), level))


def ramp(lane, beat, level):
    """The fader moves in a straight line to `level` at `beat`."""
    if beat > lane[-1][0]:
        lane.append((round(beat, 4), round(level, 2)))


def addb(tr, beat, beats, pitch, vel, gain=None, **expr):
    n = {"at": round(beat, 4), "len": round(beats * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if gain is not None:
        n["gain"] = f"{gain:.1f}dB"
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def add(tr, s16, len16, pitch, vel, **expr):
    addb(tr, s16 / 4, len16 / 4, pitch, vel, **expr)


def vadd(v, beat, beats, pitch, vel, **expr):
    for side in "lr":
        addb(f"v{v}{side}", beat, beats, pitch, vel, **expr)


def drum(piece, s16, vel, gain=None):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym"}.get(piece, "toms")
    n = {"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece == "h" else 0.25, "pitch": piece, "vel": round(vel, 3)}
    if gain is not None:
        n["gain"] = f"{gain:.1f}dB"
    T.setdefault(tr, []).append(n)


def ground(beat, semis):
    if KEY[-1][1] != semis:
        KEY.append((beat, semis))


# ---------------------------------------------------------------------------------------------------- the illusions
def line(b0, b1, gtrs=True, synth=True, slow=1, rot=None):
    """THE STAIR. The six notes climbing, an octave a bar (`slow` 2: half an octave a bar), on the Shepard tone and on
    the three guitars a side. Guitar v is in octave (v + bar) mod 3 of its three, and its fader is the bell there."""
    n, rot = 0, b0 if rot is None else rot
    fig = [int(x) for x in FIGURE.split(";")[1].split(",")] if FIGURE and slow == 1 and gtrs and b0 == RISE else None
    for b in range(b0, b1):
        acc = ACC if slow == 1 else (0, 6, 12)
        for i, a in enumerate(acc):
            d = n                                  # the step of the scale: straight up
            if fig and b >= int(FIGURE.split(";")[0]):   # v3: the figure, from the octave the scale had reached
                bf = int(FIGURE.split(";")[0])
                d = 6 * (bf - b0) + int(FIGURE.split(";")[2]) * (b - bf) + fig[i]
            k, octave = d % 6, d // 6
            n16 = (acc[i + 1] if i + 1 < len(acc) else 16) - a
            t = b * 16 + a
            if synth:
                add("stair", t, n16, 65 + SCALE[k], 0.85 if k else 1.0)
            for v in range(VOICES if gtrs else 0):
                p = 12 * ((v + octave + rot) % VOICES) + SCALE[k]
                g = db(bell(p / (12 * VOICES))) + TRIM["line"]
                if g <= -45:
                    continue
                if LEAD and b0 == RISE and b >= int(LEAD.split(";")[2]):      # v4: the eight sit back a little under the lead
                    g += float(LEAD.split(";")[4])
                step(LANE[v], t / 4, g)
                vadd(v, t / 4, n16 / 4, LINE_BASE + p, 0.95)
            n += 1


def run(b0, b1, down=False, synth=True):
    """THE RISER, ON GUITARS. A semitone to the sixteenth on the eight guitars' bell (and on the Shepard tone)."""
    for n in range((b1 - b0) * 16):
        t, s = b0 * 16 + n, -n if down else n
        if synth:
            add("stair", t, 1, 65 + s % 12, 0.8)
        for v in range(VOICES):
            p = (s + 12 * v) % (12 * VOICES)
            g = db(bell(p / (12 * VOICES))) + float(RUNS.split(";")[1])
            if g <= -45:
                continue
            step(LANE[v], t / 4, g)
            vadd(v, t / 4, 0.25, LINE_BASE + p, 0.95)


def build(b0, b1):
    """The snare doubles its speed into the bar line (eighths, then sixteenths in the last bar), getting louder."""
    nb = b1 - b0
    for i, b in enumerate(range(b0, b1)):
        for p in range(0, 16, 2 if i < nb - 1 else 1):
            drum("s", b * 16 + p, 0.45 + 0.5 * (i * 16 + p) / (nb * 16), gain=float(RUNS.split(";")[2]))


def pedal(b0, b1, kick=True):
    """The low string under the stair: a chug on every sixteenth, open where the line's notes fall, the bass with it
    and the kick on the line's notes."""
    for b in range(b0, b1):
        root = PEDAL[(b - b0) % len(PEDAL)]
        ground(b * 4, root - 12 if root > 6 else root)
        for i in range(16):
            o = i in ACC
            for tr in ("gl", "gr"):
                add(tr, b * 16 + i, 1, F1 + root, 1.0 if o else 0.86, **({} if o else {"pm": 1}))
            add("bass", b * 16 + i, 1, F1 + (root - 12 if root > 6 else root), 0.95 if o else 0.82)
            if o and kick:
                drum("k", b * 16 + i, 0.95)


def descent(b0, b1, gend=None):
    """THE STAIR, DOWNWARDS, AND ALL OF IT. The whole riff (the stair's rhythm, chugged) a step of the scale lower
    every bar, on the three guitars a side over three octaves and on two basses over two."""
    for b in range(b0, b1):
        n = -(b - b0)
        lad = 12 * (n // 6) + SCALE[n % 6]
        ground(b * 4, lad % 12)
        for v in range(VOICES):
            p = (lad + 12 * v) % (12 * VOICES)
            g = db(bell(p / (12 * VOICES))) + TRIM["fall"]
            if g <= -45 or (gend is not None and b >= gend):       # from `gend` the guitars are on the run
                continue
            step(LANE[v], b * 4, g)
            for i in range(16):
                o = i in ACC
                vadd(v, b * 4 + i / 4, 0.25, RIFF_BASE + p, 1.0 if o else 0.86, **({} if o else {"pm": 1}))
        for w in range(2):
            p = (lad + 12 * w) % 24
            a = math.sin(math.pi * p / 24)
            if db(a) <= -45:
                continue
            step(BLANE[w], b * 4, db(a))
            for i in range(16):
                addb(f"bs{w}", b * 4 + i / 4, 0.25, RIFF_BASE + p, 0.95 if i in ACC else 0.82)
        for a in ACC:
            drum("k", b * 16 + a, 0.95)


def turn(b0, b1, pitched=False):
    """THE TURN. The bar `PAT` at three speeds an octave of speed apart, all three speeding up in a straight line so
    that each doubles in CYCLE bars: guitar v plays role (v + cycle) mod 3 (x0.5 -> x1, x1 -> x2, x2 -> x4) and its
    fader is the bell over the three. In a cycle the roles play 3, 6 and 12 bars of the riff, so every cycle starts
    with all three, and the kit, on the bar line. `pitched`: each guitar also climbs an octave of the scale as it
    doubles its speed (a tape speeding up); otherwise all three stay on the low F."""
    tc, L = CYCLE * 4.0, len(PAT) * 0.5
    which = "both" if pitched else "time"
    for c in range((b1 - b0) // CYCLE):
        c0 = b0 * 4 + c * tc
        for v in range(VOICES):
            j = (v + c) % VOICES
            if j >= ROLES:                       # this guitar rests this cycle: it has left at the top and comes back in at the bottom
                step(LANE[v], c0, FLOOR)
                continue
            scale = 2 ** (j - 1) * tc
            step(LANE[v], c0, db(bell(j / ROLES)) + TRIM[which])
            for s in range(1, 17):
                ramp(LANE[v], c0 + s / 16 * tc - (0.011 if s == 16 else 0), db(bell((j + s / 16) / ROLES)) + TRIM[which])
            pats = 1.5 * scale / L
            assert abs(pats - round(pats)) < 1e-9, "the cycle must hold whole bars of the riff at every speed"
            for m in range(int(round(pats))):
                for i, tok in enumerate(PAT):
                    q = m * L + i * 0.5
                    u = -1 + math.sqrt(1 + 2 * q / scale)
                    r = 2 ** (j - 1) * (1 + u)
                    g = db(bell((j + u) / ROLES))
                    if g <= -45:
                        continue
                    p = 12 * j + SCALE[min(5, int(6 * u))] if pitched else 0
                    vadd(v, c0 + u * tc, 0.5 / r, RIFF_BASE + p, 1.0 if tok == "o" else 0.86, **({} if tok == "o" else {"pm": 1}))
                    if tok == "o":
                        drum("k", (c0 + u * tc) * 4, 0.95, gain=g)


def anchor(b):
    """The bass under the turn: it keeps the bar while the guitars leave it."""
    if not ANCHOR:
        add("bass", b * 16, 14, F1, 0.95)
        return
    n = int(ANCHOR)
    for i in range(n):
        add("bass", b * 16 + i * 16 // n, 16 // n, F1, 0.95 if i == 0 else 0.85)


def beat(b0, b1, snare=(8,), cym="x", stepc=4, vel=0.5, crash=4):
    """The kit keeps four in a bar: the snare on the sixteenths `snare`, a cymbal every `stepc` sixteenths, a crash
    every `crash` bars."""
    for b in range(b0, b1):
        for p in snare:
            drum("s", b * 16 + p, 0.95)
        if cym:
            for p in range(0, 16, stepc):
                drum(cym, b * 16 + p, vel * (1.15 if p == 0 else 1.0 if p % 4 == 0 else 0.82))
        if crash and (b - b0) % crash == 0:
            drum("c", b * 16, 0.9 if b == b0 else 0.7)


def fill(b):
    """The last half bar before bar `b`."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, b * 16 - 8 + i, 0.6 + 0.045 * i)


def compose():
    # the foot: the stair alone on the Shepard tone; then the three guitars a side take it up
    line(FOOT, FOOT + 4, gtrs=False)
    line(FOOT + 4, RISE)
    beat(FOOT + 4, RISE, snare=(), cym="h", vel=0.45, crash=0)
    fill(RISE)
    # the stair: the band
    R = int(RUNS.split(";")[0]) if RUNS else 0
    line(RISE, TIME - R)
    pedal(RISE, TIME)
    back = int(FIGURE.split(";")[0]) if FIGURE else RISE + 12        # the backbeat comes in with the figure
    beat(RISE, back, snare=(8,), cym="x", stepc=4)
    beat(back, TIME - R, snare=(4, 12), cym="x", stepc=2)
    if R:                                # v2: the stair hands over on a run, the snare doubling under it
        run(TIME - R, TIME)
        beat(TIME - R, TIME, snare=(), cym="x", stepc=2, crash=0)
        build(TIME - R, TIME)
    else:
        fill(TIME)
    if LEAD:                             # v4: a lead comes down two octaves over the tune's last six bars, onto the run's first note
        lb, top = int(LEAD.split(";")[2]), int(LEAD.split(";")[3])
        halves = 2 * (TIME - R - lb)
        assert halves == 12, "two octaves of a six-note scale, a note to the half bar"
        for i in range(halves):
            add("lead", lb * 16 + 8 * i, 8, top + 12 * (-i // 6) + SCALE[-i % 6], 0.9)
        add("lead", (TIME - R) * 16, 4, top - 24, 0.95)
    # the turn: the chug at three speeds, speeding up for ever. The kit and the bass hold the bar
    turn(TIME, FALL)
    beat(TIME, FALL, snare=(8,), cym="x", stepc=4, crash=CYCLE)
    for b in range(TIME, FALL):
        ground(b * 4, 0)
        anchor(b)
    fill(FALL)
    # the descent
    descent(FALL, POLE, gend=POLE - R if R else None)
    if R:                                # v2: the guitars leave the descent on a falling run
        run(POLE - R, POLE, down=True, synth=False)
    beat(FALL, POLE, snare=(8,), cym="x", stepc=4, crash=6)
    T.setdefault("rumble", []).append({"at": FALL * 4, "len": (POLE - FALL) * 4 - 0.5, "pitch": "F2", "vel": 0.8})
    # the pole: one chord through a filter that climbs for ever; the line slowly; a bass that is only its overtones
    for b in range(POLE, BOTH, 2):
        root = PEDAL[((b - POLE) // 2) % len(PEDAL)]
        for tr in ("pl", "pr"):
            add(tr, b * 16, 31, ",".join(nm(F1 + root + i) for i in (0, 7, 12)), 0.9)
        add("ghost", b * 16, 31, F1 + (root - 12 if root > 6 else root), 0.85)
        drum("k", b * 16, 0.85)
    line(POLE, BOTH - R, gtrs=False, slow=2)
    if TICK:                             # v2: a tick that speeds up for ever (the track's `risset`; these three strokes are its pattern)
        for at, ln, v in ((0.0, 0.5, float(TICK.split(";")[1])), (0.5, 0.5, float(TICK.split(";")[2])), (1.0, 1.0, float(TICK.split(";")[2]))):
            T.setdefault("tick", []).append({"at": at, "len": ln, "pitch": "h", "vel": v})
    else:
        beat(POLE, BOTH, snare=(), cym="h", vel=0.42, crash=0)
    T.setdefault("riser", []).append({"at": (BOTH - 4) * 4, "len": 16.0, "pitch": "F4", "vel": 0.8, **({"gain": "-3.0dB"} if R else {})})
    if R:                                # v2: a rising run into both, the snare doubling under it (the riser 3 dB down under them)
        run(BOTH - R, BOTH)
        build(BOTH - R, BOTH)
    else:
        fill(BOTH)
    # both: pitch and speed rise together. A riser that never arrives swells over the second half, and stops dead
    turn(BOTH, STOP, pitched=True)
    beat(BOTH, STOP, snare=(4, 12), cym="x", stepc=2, crash=CYCLE)
    for b in range(BOTH, STOP):
        ground(b * 4, 0)
        anchor(b)
    T.setdefault("riser", []).append({"at": (STOP - 8) * 4, "len": 32.0, "pitch": "F4", "vel": 1.0})
    for b in range(STOP - 2, STOP):                      # the snare on every beat into the stop
        for q in (0, 8):
            drum("s", b * 16 + q, 0.85)
    # the summit: a bar of nothing; then the stair's first bars, exactly. One chord
    line(HOME, END, rot=RISE)
    pedal(HOME, END)
    beat(HOME, END, snare=(8,), cym="x", stepc=4)
    for tr in ("gl", "gr"):
        add(tr, END * 16, 40, ",".join(nm(F1 + i) for i in (0, 7, 12, 19)), 0.95)
    add("bass", END * 16, 40, F1, 0.95)
    ground(END * 4, 0)
    add("stair", END * 16, 40, 65, 0.9)
    drum("k", END * 16, 0.95)
    drum("c", END * 16, 0.95)
    # a voice that is not playing is down
    for lane in list(LANE.values()) + list(BLANE.values()):
        step(lane, END * 4, FLOOR)


def key_f(hz):
    """An eq frequency that follows the key: the lane `key` is the ground in semitones over F; the engine bends in octaves."""
    return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}


def pts(lane):
    return [[f"{t:g}b", v] for t, v in lane]


def song():
    compose()
    key_lane = [["0b", 0]]
    for (b, k), (_, prev) in zip(KEY[1:], KEY):
        key_lane += [[f"{b - 0.02:g}b", prev], [f"{b:g}b", k]]
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    heavy = os.environ.get("C10T5_HEAVY", "ct-twin fx.1.model='5150' fx.2.mic=0.5 fx.2.cone={}")     # the low string
    voice = os.environ.get("C10T5_VOICE", "ct-twin fx.1.model=mark fx.2.mic=0.45 fx.2.cone={}")      # the three that carry the illusions
    GH, GV = os.environ.get("C10T5_GHEAVY", "-1.7dB"), os.environ.get("C10T5_GVOICE", "0dB")
    # the Shepard tone: its gain under the band ; its hall send ; dB over that alone at the foot ; with the guitars
    # at the foot ; in the pole
    synth = os.environ.get("C10T5_STAIR", "-19.5dB;-10dB;7.5;5.5;5.5").split(";")
    syn_lane = [(0.0, float(synth[2]))]
    for bar, lvl in ((FOOT + 4, float(synth[3])), (RISE, 0.0), (POLE, float(synth[4])), (BOTH - (int(RUNS.split(";")[0]) if RUNS else 0), 0.0)):
        step(syn_lane, bar * 4, lvl)
    tracks = [
        {"name": "gl", "patch": heavy.format(30), "gain": GH, "pan": -1, "out": "gtrs"},
        {"name": "gr", "patch": heavy.format(31), "gain": GH, "pan": 1, "out": "gtrs"},
        *[{"name": f"v{v}{side}", "patch": voice.format(32 + i if ONE else 32 + 2 * v + i), "gain": {"value": GV, "mod": [{"src": "auto.bell", "amount": 1}]},
           "pan": (-1, 1)[i] * (float(ONE) if ONE else (0.9, 0.75, 0.6, 0.45)[v]), "out": "gtrs", "auto": {"bell": {"points": pts(LANE[v]), "curve": 0}},
           **({"fx": [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*VEQ.split(":"))]}]} if VEQ else {})}
          for v in range(VOICES) for i, side in enumerate("lr")],
        {"name": "pl", "patch": heavy.format(40), "gain": os.environ.get("C10T5_POLE", "-1dB"), "pan": -0.8, "out": "pole"},
        {"name": "pr", "patch": heavy.format(41), "gain": os.environ.get("C10T5_POLE", "-1dB"), "pan": 0.8, "out": "pole"},
        {"name": "stair", "patch": "fs-stair", "gain": {"value": synth[0], "mod": [{"src": "auto.lvl", "amount": 1}]}, "pan": 0, "sends": {"hall": synth[1]},
         "auto": {"lvl": {"points": pts(syn_lane), "curve": 0}}},
        *([{"name": "lead", "patch": LEAD.split(";")[0], "gain": LEAD.split(";")[1], "pan": 0.1}] if LEAD else []),
        {"name": "riser", "patch": "fx-riser-endless amp.a=16b", "gain": os.environ.get("C10T5_RISER", "-18dB"), "pan": 0},
        {"name": "rumble", "patch": "shepard-fall", "gain": os.environ.get("C10T5_RUMBLE", "-21dB"), "pan": 0},
        {"name": "ghost", "patch": "phantom-bass", "gain": os.environ.get("C10T5_GHOST", "-14dB"), "pan": 0},
        {"name": "bass", "patch": "ct-bass", "gain": os.environ.get("C10T5_BASS", "2dB"), "pan": 0, "out": "low"},
        *[{"name": f"bs{w}", "patch": "ct-bass", "gain": {"value": "0.5dB", "mod": [{"src": "auto.bell", "amount": 1}]}, "pan": 0, "out": "low",
           "auto": {"bell": {"points": pts(BLANE[w]), "curve": 0}}} for w in range(2)],
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        *([{"name": "tick", "patch": kit, "gain": TICK.split(";")[0], "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air, "at": f"{POLE * 4}b",
            "risset": {"cycle": f"{TICK.split(';')[3]}bar", "layers": 3, "length": f"{BOTH - POLE - (int(RUNS.split(';')[0]) if RUNS else 0)}bar"}}] if TICK else []),
    ]
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])
    return {
        "about": ("chirpers X (Common Time), track 5 by chirper-zero: False Summit. True djent built on the illusions of endless motion, "
                  "played by the band: a line that climbs an octave every bar and is never higher (three guitars a side an octave "
                  "apart, each fading in at the bottom and out at the top); a chug that speeds up for ever and is never faster (the "
                  "same three at three speeds); the two together; and at the end the first bars again, exactly. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {
            "ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
            # the Shepard tone, played as notes: octave-spaced partials under a fixed bell, so a climbing scale never gets higher
            "fs-stair": {"synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "520hz", "width": 1.1}},
                                              {"type": "shepard", "cents": 6, "level": "-5dB", "shepard": {"octaves": 8, "center": "520hz", "width": 1.1}}],
                                   "filters": [{"kind": "lp", "cutoff": "5k", "q": 0.6}],
                                   "amp": {"a": "6ms", "d": "500ms", "s": 0.55, "r": "150ms"}},
                         "play": {"gate": 1.0, "vel_sens": 0.3}, "gain": "-6dB"},
        },
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            # the pole: the endless filter sweep, one octave a bar
            "pole": {"fx": [{"type": "barberpole", "cycle": "1bar", "bands": 5, "spacing": 1, "low": "160hz", "q": 2.2, "spread": 0.4, "mix": float(os.environ.get("C10T5_POLEMIX", "0.85"))},
                            "reverb kind=hall decay=3s mix=0.25 predelay=20ms low_cut=150"]},
            "low": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                    {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]}],
                    "auto": {"key": {"points": key_lane, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T5_MASTER", "2.4dB")}]},
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
