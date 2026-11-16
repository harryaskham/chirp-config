#!/usr/bin/env python3
"""chirpers10-t4 "Running Total" (chirper-zero): one riff, said one note more each time.

A running total is the sum so far, carried forward: each line of the ledger is everything before it and one thing more.
This piece's riff is two bars of sixteenths, thirty-two places. It is never simply played. It is ADDED UP: first its
first place alone; then its first two; then its first three; each statement starting again from the top and going one
place further than the last, until the thirty-second statement is the whole riff.

Common Time (track 1) turns three cells of different lengths under one pulse; Odd Sympathy (track 2) slides one riff
against itself; Plain Hunt (track 3) rings one row through every order. This piece's long cycle is a SUM. The
statements are 1, 2, 3 ... 32 sixteenths long, so the n-th begins after 1 + 2 + ... + (n-1) sixteenths: the
triangular numbers. Against a kit that keeps four in a bar the riff's head therefore lands somewhere new every time
(on the bar line, a sixteenth late, three late, six late, ten late ...) and never twice running in the same place. And
the arithmetic closes: 1 + 2 + ... + 31 is 496 sixteenths, exactly 31 bars, and adding the 32nd makes 528, exactly 33.
So the first statement after the very first to begin ON a bar line is the first WHOLE one. It lines up after a long
wait, and what lines up is the riff complete: from there it is two bars long and sits in the bar as if it always had.

  the build       bars 0-33     statements 1 to 32 from the top (the first place, the first two, ...). The band grows
                                as the riff does: a marimba alone (an abacus: wooden beads), then one guitar with the
                                bass and kick, the second guitar, the snare, the doubles.
  the total       bars 33-49    the whole riff, eight times: on F, then on A flat.
  the back-build  bars 49-82    the same sum from the other end: its LAST place alone, its last two, its last three ...
                                so the ending is always there and the riff grows backwards to meet its head. On B. The
                                marimba counts the first sixteen alone; the bass and kick join; then the band.
  the total       bars 82-98    the whole riff on C, then home on F.
  the melt        bars 98-129   the sum undone: the riff loses its FIRST place each time (31 long, 30, ... 1), 496
                                sixteenths, exactly 31 bars, and the band thins with it; the marimba counts the last
                                eight down alone; then one chord.

The riff's notes are the album's: a low F, muted, and the hook notes A flat, B, G flat, C, E flat. The marimba (the
library's `modal-marimba`, a rosewood bar: wood, where Odd Sympathy has a music box and Plain Hunt has bells) plays
them two octaves up.

v1 is the SKELETON (Harry, 15 Nov about 02:42: "we can do fourth track same climber"; track 2's terms: mine, my title,
a skeleton first): the whole shape standing, bare.
"""
import json
import os

OUT = os.environ.get("C10T4_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t4.yaml"))
BPM = 116
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# ---------------------------------------------------------------------------------------------------- the riff
# thirty-two places (two bars of sixteenths). o = the open low string, accented (the riff's head and its half-way mark);
# c = a muted chug on the low string; a number = a hook note, that many semitones over the ground, unmuted;
# - = the note before goes on; r = a rest.
RIFF = ("o c c 3 - c 6 - c c r 1 c 7 - c "
        "o c 10 - c c 6 3 c r c 1 - c c 7").split()
N = len(RIFF)
assert N == 32
assert sum(range(1, N + 1)) % 16 == 0 and sum(range(1, N)) % 16 == 0      # the build ends on a bar line, and its last statement begins on one

# the form, in bars
BUILD, TOTAL1, BACK, TOTAL2, MELT = 0, 33, 49, 82, 98
END = MELT + sum(range(1, N)) // 16
NB = END + 2
assert TOTAL1 == sum(range(1, N + 1)) // 16 and BACK - TOTAL1 == 16 and TOTAL2 - BACK == 33 and MELT - TOTAL2 == 16
G_MAIN, G_DBL = ("gl", "gr"), ("gl2", "gr2")


# v2: THE TOTAL HAS A TUNE (section round, 1:25-1:41: the second half of the first total, which the section map
# called static: once the riff is whole it was played eight times and nothing else happened). The riff has nine notes
# that are not the low string: A flat, B, G flat, C, then E flat, B, A flat, G flat, C: the album's hook, the notes
# Common Time's riffs grow. In the riff they pass in a sixteenth or two. Now, when the total moves up to A flat, a LEAD
# GUITAR plays only those nine, each held until the next: the tune that was inside the riff all along, drawn out of it
# over the band, in the riff's own time (each lead note starts exactly where the riff strikes it).
# the patch ; its gain ; semitones over the riff ; its hall send. "" = v1.
TUNE = os.environ.get("C10T4_TUNE", "lead-monster;-13.5dB;36;-12dB")


# v3: THE SECOND COUNT IS SAID QUIETLY (whole song). The scorer's one weak term on this song said something true: its
# sections were all one loudness (a range of 1.7 dB) and one density. The riff is added up twice, and both times the
# band came in a third of the way through and stayed. Now the second sum, the one from the riff's END (bars 49-82, on
# B), is the song's quiet middle. The marimba counts the first eight statements alone, as it did; then a CLEAN GUITAR
# says them with it (the album's `ct-glass`: bridge and middle coils, a small miked amp), an octave over the riff, its
# low notes short and its hook notes ringing; at the seventeenth a second clean guitar on the other side (`ct-clean`:
# a neck coil, chorus); at the twenty-fifth the bass and the kick come back, on the riff's accents and hook notes
# only. The hat keeps time; no snare. The band waits for the LAST FOUR statements (the 29th, 2:33, on a crash): seven
# and a half bars of the riff nearly whole, into the total on C. So something joins at each stage, the low end is
# gone for forty seconds, and you hear the riff's ending said clean twenty-eight times before the band says it.
# (First with the bass and kick back at the seventeenth: by loudness the stretch was 2.5 dB under the band, but by
# plain level only 1.6: the low end had never left. The scorer said so, and it was right.)
# the clean guitar on the left ; on the right ; their gains ; semitones over the riff ; the statement the first
# joins ; the second ; the band ; their hall send ; the statement the bass and kick come back, softly. "" = v2.
CLEAN = os.environ.get("C10T4_CLEAN", "ct-glass;ct-clean;8dB;8dB;12;9;17;29;-9dB;25")
# THE BASS'S TONE FOLLOWS THE KEY (the fault found on Plain Hunt at its v11, owed here since): the bass's eq was cut
# to the low F, and off it the bass alone lost 3 to 5 dB from 120 Hz up on A flat and 8 to 10 on B and C (`keyshape`).
# The three bands fitted to the ground now follow it (a lane `key` on the bass's bus, semitones over F). "" = v2.
# (`all` makes the two fixed bands, 350 Hz and 1500 Hz, follow too. Tried at the bench and worse: on B and C the bass
# alone then read 8 dB down at 500 Hz-2 kHz where the three leave it 5 down.)
KEYEQ = os.environ.get("C10T4_KEYEQ", "1")


# v4: THE TUNE IS ADDED UP TOO (section round, 2:50-3:23: the second total, which the section map called static: the
# whole riff eight times, as the first total was, and without the first total's tune). The riff was a sum; now its
# tune is one. Over the second total the lead plays the riff's hook notes as the riff strikes them, but only the first
# TWO in the first statement, holding the second; the first three in the next; one more each statement. The total is
# eight statements and the tune has nine notes, so the tune is whole exactly once: in the last statement, at home on
# F, as the melt begins to take the riff apart. (The riff took thirty-two statements to be whole; its tune takes
# eight.) And the kit shapes the stretch: half time on C (the snare on three, the china on the beats) while the tune
# is short, the backbeat when the key comes home.
# hook notes in the first statement ; the kit on C (`half` = half time; anything else = the backbeat). "" = v3.
TUNE2 = os.environ.get("C10T4_TUNE2", "2;half") if TUNE else ""


def tune_sum(b0, roots, first):
    """The riff's hook notes over the statements from bar b0, one more each statement, each held until the next and
    the last to the statement's end."""
    hooks = [(i, int(k)) for i, k in enumerate(RIFF) if k not in "ocr-"]
    for r, root in enumerate(roots):
        m = min(len(hooks), first + r)
        for j in range(m):
            i, semi = hooks[j]
            add("lead", (b0 + 2 * r) * 16 + i, (hooks[j + 1][0] if j + 1 < m else N) - i, F1 + root + int(TUNE.split(";")[2]) + semi, 0.9)


# v7: THE TUNE MELTS TOO (section round, 3:18-3:51: the melt's first half minute, which the section map called static
# and "little new" against the total before it: the riff nearly whole, on the same ground, with the lead gone). The
# riff was added up and so was its tune; the riff is taken apart, and now so is the tune. Through the melt the lead
# goes on playing the riff's hook notes where the riff strikes them, and as the riff loses its front the tune loses
# its first note: nine notes for four statements, then eight (the A flat has gone), seven (the B), six, five. A
# thirty-two-place riff losing one chug is hard to hear; a nine-note tune losing its first note is not: the melt can
# now be followed by ear. The lead stops where the second pair of guitars does (the seventeenth statement from the
# end, 4:09) and the marimba, which comes in there with the riff's notes, carries what is left of the tune down to
# its last note.
# THE LEAD SINKS AS IT MELTS. At the total's level the lead read as it does in the total (-8.3 to -8.9 by presence)
# and lifted the melt 0.5 to 0.7 dB, level with the total it comes out of: but the melt is the band thinning, a step
# down (0.8 dB) from the riff whole. So the lead's fader goes down through the melt, to its last statement. (A fader after its amp: on a high-gain lead a note's velocity or gain changes the drive, not the
# level. Tried at -3 falling to -6: the lead read -12.5 to -14.3 by presence and was never near the front: too far
# down for a line the ear is meant to follow; and at -1.5 falling to -5: -11.2 at the start, where the ear has to
# learn the game. So it starts where the total left it and sinks from there.)
# the shortest statement the lead still plays ; its fader at the melt's start and at its own last statement, dB. "" = v6.
MELTUNE = os.environ.get("C10T4_MELTUNE", "17;0;-5") if TUNE else ""
MELT_END = [0.0]                         # the beat the lead's last melt statement ends


def tune_melt(t, a, vel):
    """The riff's hook notes in places a..N-1, from sixteenth t (place a), each held until the next and the last to
    the statement's end. A statement that begins inside a held hook note strikes it again, as the guitars do."""
    hooks = [(i, int(k)) for i, k in enumerate(RIFF) if k not in "ocr-"]
    if RIFF[a] == "-":
        j = a
        while RIFF[j] == "-":
            j -= 1
        hooks = [(a, int(RIFF[j]))] + [h for h in hooks if h[0] > a]
    else:
        hooks = [h for h in hooks if h[0] >= a]
    for j, (i, semi) in enumerate(hooks):
        nxt = hooks[j + 1][0] if j + 1 < len(hooks) else N
        add("lead", t + i - a, nxt - i, F1 + int(TUNE.split(";")[2]) + semi, vel)


# v5: THE CHINA COUNTS (whole song). The song's one idea is a sum: each statement starts again and goes one place
# further. But the kit only kept time: the china rode the beat through the build exactly as it does when the riff is
# whole, so nothing but the guitars' open note said where a statement began. Now, wherever the riff is being added up
# or taken apart (the build, the last statements of the second count, the melt), THE CHINA STRIKES WHERE EACH STATEMENT
# STARTS, with the kick and the open string, and a hat keeps the time in its place. The strokes come further and
# further apart as the statements grow (and closer as they melt): the kit plays the sum. When the riff is whole (the
# two totals) the china rides the bar as it did: so you can hear by the cymbal alone whether the riff is being counted
# or is complete.
# In the build it starts with the SEVENTEENTH statement (0:17), where the second guitar and the snare come in: one
# stage more. (Tried from the ninth, with the first guitar: the scorer then lost the seam at 0:18 on its two highest
# cuts, 5 sections to 4, because too much had already come in. It was right: the entry at 0:18 had nothing left.)
# the cymbal on each statement's head ; its velocity ; the hat's step in sixteenths where the china rode ; its
# velocity ; the statement of the build it starts at. "" = v4.
COUNT = os.environ.get("C10T4_COUNT", "x;0.9;2;0.5;17")
HEADS = []                            # (sixteenth, section) of each statement's start, where the band plays


# v6: THE RIFF WHOLE HAS ITS OWN RIG (palette round). All four guitars were the album's `ct-twin`, a staple of four
# of its five songs, and the same four played the riff being counted and the riff complete. Now, in the two totals
# (and on the last chord, which is the total), the SECOND pair is Common Time's WALL rig, in its form whose rests are
# rests (`ct-wall-stop-l` / `ct-wall-stop-r`: a darker, thicker amp into a captured cabinet), which no song but Common
# Time had used. (The plain `ct-wall` was benched first: its sympathetic strings keep the amp full through the riff's
# two rests, which read as loud as the chug before them; on the old pair and on this one a rest is 9 dB down.) Alone on the same notes and
# as loud as the pair it replaces it has 7 to 8 dB more from 120 Hz to 1 kHz and 13 dB less above 8 kHz: the first
# pair keeps the edge and the second becomes the body. So the guitars say what the china says: the riff being counted
# is tight; the riff whole is a wall.
# (Benched and not taken: the engine's 4x12 and 2x12 cabinets on the second pair: each lost 5 to 10 dB under 250 Hz
# and gained 2 at 500 Hz-1 kHz: thinner and honkier, the wrong way for an arrival.)
# the left patch ; the right ; their gain ; one eq band on them (hz:q:dB, or empty). "" = v5.
RIG2 = os.environ.get("C10T4_RIG2", "ct-wall-stop-l;ct-wall-stop-r;-3.5dB;380:1:-3")
G_TOT = ("gl", "gr", "wl", "wr") if RIG2 else ("gl", "gr", "gl2", "gr2")

# v8: THE KNOCK (palette round: the part the song lacked). The piece is a count, and in two of its three counts the
# count is the hardest thing in it to hear: in the back-build each statement starts on a different place of the riff
# (its last place, its last two ...), and in the melt likewise, so nothing says "again". Now something does: a
# WOODBLOCK knocks once where every statement starts, in the passages where the china does not (the china has the
# statements' heads once the band is in, since v5). It is the abacus's other voice: the marimba is the beads, the
# block is the bead hitting the frame. A new instrument, on no other song: `rt-block`, the song's own patch: the
# marimba's rosewood bar made short and hard (rung out in a tenth of a second, struck near its edge, with a click),
# two octaves over the marimba's low note and tuned to the key.
# And because the statements are 1, 2, 3 ... sixteenths long, the knocks are a figure of their own: at the start of
# each count they come one, two, three, four sixteenths apart and slow by arithmetic (a ball bouncing, backwards);
# and at the very end of the song, as the melt runs out (8, 7, 6 ... 1), they close up again and run into the last
# chord: the ball comes to rest.
# The knocks are soft where they are close together and full where they are a bar apart, as a ball's bounces are.
# (First bench: decay 0.1 s, gone in 40 ms, at -12 dB: a tick, 5 dB under the hat in the back-build. Then decay
# 0.3 s and -5 dB at one velocity: right in the back-build, but LOUDER THAN THE MARIMBA in the flurries at the
# start and the end. Hence the velocities.)
# the patch ; its gain ; semitones over the riff's low note ; velocity where the statements are sixteen places or
# longer ; hall send ; velocity at one place long. "" = v7.
KNOCK = os.environ.get("C10T4_KNOCK", "rt-block;-5dB;48;0.9;-14dB;0.4")
BLOCK = json.loads(os.environ.get("C10T4_BLOCK", json.dumps({
    "about": "Running Total's woodblock (chirper-zero, v8): the marimba's rosewood bar made short and hard, with a stick's click.",
    "play": {"vel_sens": 0.9},
    "synth": {"amp": {"a": "0.5ms", "d": "400ms", "s": 0, "r": "80ms"},
              "env": {"c": {"a": "0.2ms", "d": "4ms", "s": 0}},
              "layers": [{"type": "modal", "modes": "bar", "decay": "0.3s", "damp": 0.5, "strike": 0.6, "tilt": 0.0, "vary": 0.3,
                          "bright": {"value": 0.7, "mod": [{"src": "vel", "amount": 0.25}]}},
                         {"type": "noise", "level": {"value": "-60dB", "mod": [{"src": "env.c", "amount": 44}]}}]}})))
KNOCKS = []                           # (sixteenth, the key's root, the statement's length) of each statement's start, where the block knocks


def key_f(hz):
    return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}


def tune(b0, root, reps, vel=0.9):
    """The riff's hook notes alone, each held until the next, over `reps` statements of the whole riff from bar b0."""
    hooks = [(i, int(k)) for i, k in enumerate(RIFF) if k not in "ocr-"]
    for r in range(reps):
        for j, (i, semi) in enumerate(hooks):
            nxt = hooks[j + 1][0] if j + 1 < len(hooks) else N + (hooks[0][0] if r + 1 < reps else 0)
            add("lead", (b0 + 2 * r) * 16 + i, nxt - i, F1 + root + int(TUNE.split(";")[2]) + semi, vel)


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece == "h" else 0.25, "pitch": piece, "vel": round(vel, 3)})


def say(t, a, b, root, gtrs, kick=True, low=True, wood=False, soft=False, clean=()):
    """Places a..b-1 of the riff, from sixteenth t, on the guitars `gtrs`, the bass (`low`) and the kick; on the
    marimba too with `wood`. A statement that begins inside a held note strikes it again; one that ends inside it
    cuts it short."""
    i = a
    while i < b:
        kind = RIFF[i]
        if kind == "-":                       # begun inside a held note
            j = i
            while RIFF[j] == "-":
                j -= 1
            kind = RIFF[j]
        if kind == "r":
            i += 1
            continue
        n = 1
        while i + n < b and RIFF[i + n] == "-":
            n += 1
        at = t + (i - a)
        if wood:
            add("wood", at, 2, F1 + root + 24 + (0 if kind in "oc" else int(kind)), 0.95 if kind == "o" else 0.6 if kind == "c" else 0.85)
        up = int(CLEAN.split(";")[4]) if clean else 0
        if kind == "o":
            for tr in gtrs:
                add(tr, at, n, F1 + root, 1.0)
            for tr in clean:
                add(tr, at, 2, F1 + root + up, 0.9)
            if low:
                add("bass", at, 2 if soft else n, F1 + root, 0.8 if soft else 0.95)
            if kick and low:
                drum("k", at, 0.8 if soft else 0.95)
        elif kind == "c":
            for tr in gtrs:
                add(tr, at, n, F1 + root, 0.88, pm=1)
            for tr in clean:
                add(tr, at, 0.6, F1 + root + up, 0.55)
            if low and not soft:
                add("bass", at, n, F1 + root, 0.85)
            if kick and low and not soft:
                drum("k", at, 0.85)
        else:
            for tr in gtrs:
                add(tr, at, n, F1 + root + int(kind), 0.95)
            for tr in clean:
                add(tr, at, n + 1, F1 + root + up + int(kind), 0.85)
            if low:
                add("bass", at, n, F1 + root + int(kind), 0.75 if soft else 0.9)
        i += n


def beat(b0, b1, snare=(), cym=None, step=4, vel=0.5):
    """The kit keeps four in a bar: the snare on the sixteenths `snare`, a cymbal every `step` sixteenths."""
    for b in range(b0, b1):
        for p in snare:
            drum("s", b * 16 + p, 0.95)
        if cym:
            for p in range(0, 16, step):
                drum(cym, b * 16 + p, vel * (1.15 if p % 16 == 0 else 1.0 if p % 4 == 0 else 0.82))


def fill(b):
    """The last half bar before bar `b`."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, b * 16 - 8 + i, 0.6 + 0.045 * i)


def compose():
    # the build: statement k is the riff's first k places. The band grows as the riff does
    t = BUILD * 16
    for k in range(1, N + 1):
        gtrs = () if k < 9 else ("gl",) if k < 17 else G_MAIN if k < 25 else G_MAIN + G_DBL
        say(t, 0, k, 0, gtrs, low=k >= 9, wood=k < 17)       # the marimba counts the first eight alone, and hands over
        if COUNT and k >= int(COUNT.split(";")[4]):
            HEADS.append(t)
        elif KNOCK:
            KNOCKS.append((t, 0, k))
        t += k
    assert t == TOTAL1 * 16
    beat(0, 9, cym="h", vel=0.45)
    beat(9, 19, snare=(8,), cym="h", vel=0.5)
    if COUNT:                             # v5: the china is on the statements' heads; a hat keeps the time
        beat(19, 33, snare=(4, 12), cym="h", step=int(COUNT.split(";")[2]), vel=float(COUNT.split(";")[3]))
    else:
        for b in range(9, 19):
            drum("x", b * 16, 0.55)
        beat(19, 33, snare=(4, 12), cym="x", vel=0.5)
    drum("c", 31 * 16, 0.9)               # the first whole statement begins on a bar line
    fill(TOTAL1)
    # the total: the whole riff, eight times: on F, then on A flat
    for i in range(8):
        say((TOTAL1 + 2 * i) * 16, 0, N, 0 if i < 4 else 3, G_TOT)
        drum("c", (TOTAL1 + 2 * i) * 16, 0.9 if i in (0, 4) else 0.7)
    if TUNE:                              # v2: on A flat the lead draws the riff's hook out of it
        tune(TOTAL1 + 8, 3, 4)
    beat(TOTAL1, BACK, snare=(4, 12), cym="x", step=2, vel=0.5)
    fill(TOTAL1 + 8)
    fill(BACK)
    # the back-build: statement k is the riff's LAST k places. On B
    t = BACK * 16
    if CLEAN:                             # v3: the second count is said quietly; the band waits for the last four statements
        c1, c2, cb = (int(x) for x in CLEAN.split(";")[5:8])
    for k in range(1, N + 1):
        if CLEAN:
            band = k >= cb
            say(t, N - k, N, 6, G_MAIN + G_DBL if band else (), low=k >= int(CLEAN.split(";")[9]), soft=not band, wood=k < cb,
                clean=() if band or k < c1 else ("cl",) if k < c2 else ("cl", "cr"))
            if k == cb:
                for i, pc in enumerate(["t1", "t2", "ft", "s"]):
                    drum(pc, t - 4 + i, 0.6 + 0.08 * i)
                drum("c", t, 0.9)
            elif band:
                HEADS.append(t)
            elif KNOCK:
                KNOCKS.append((t, 6, k))
            t += k
            continue
        gtrs = () if k < 25 else G_MAIN + G_DBL
        say(t, N - k, N, 6, gtrs, low=k >= 17, wood=k < 29)   # the marimba alone; then with the bass and kick; then the band
        if k == 25:
            drum("c", t, 0.9)
        t += k
    assert t == TOTAL2 * 16
    beat(BACK, BACK + 9, cym="h", vel=0.45)
    if CLEAN:
        bb = BACK + (cb * (cb - 1) // 2) // 16          # the bar the band comes in
        beat(BACK + 9, bb, cym="h", step=2, vel=0.5)
        if COUNT:
            beat(bb, TOTAL2, snare=(4, 12), cym="h", step=int(COUNT.split(";")[2]), vel=float(COUNT.split(";")[3]))
        else:
            beat(bb, TOTAL2, snare=(4, 12), cym="x", vel=0.5)
    else:
        beat(BACK + 9, BACK + 19, snare=(8,), cym="h", step=2, vel=0.55)
        beat(BACK + 19, TOTAL2, snare=(4, 12), cym="x", vel=0.5)
    drum("c", (TOTAL2 - 2) * 16, 0.9)
    fill(TOTAL2)
    # the total again: on C, then home on F
    for i in range(8):
        say((TOTAL2 + 2 * i) * 16, 0, N, 7 if i < 4 else 0, G_TOT)
        drum("c", (TOTAL2 + 2 * i) * 16, 0.9 if i in (0, 4) else 0.7)
    if TUNE2:                             # v4: the tune is added up over the second total
        tune_sum(TOTAL2, [7 - 12] * 4 + [0] * 4, int(TUNE2.split(";")[0]))      # on C an octave under: the tune rises as it comes home
    if TUNE2 and TUNE2.split(";")[1] == "half":
        beat(TOTAL2, TOTAL2 + 8, snare=(8,), cym="x", step=4, vel=0.55)
        beat(TOTAL2 + 8, MELT, snare=(4, 12), cym="x", step=2, vel=0.5)
    else:
        beat(TOTAL2, MELT, snare=(4, 12), cym="x", step=2, vel=0.5)
    fill(TOTAL2 + 8)
    fill(MELT)
    # the melt: the riff loses its first place each time; the band thins with it
    t = MELT * 16
    for k in range(N - 1, 0, -1):
        gtrs = G_MAIN + G_DBL if k > 16 else G_MAIN if k > 8 else ()
        say(t, N - k, N, 0, gtrs, low=k > 8, wood=k <= 16)    # the marimba joins as the band thins, and counts the last eight down alone
        if MELTUNE and k >= int(MELTUNE.split(";")[0]):       # v7: the tune melts with the riff, on the lead
            tune_melt(t, N - k, 0.9)
            MELT_END[0] = (t + k) / 4
        if k > 8 and t > MELT * 16:
            HEADS.append(t)
        elif KNOCK and k <= 8:
            KNOCKS.append((t, 0, k))
        t += k
    assert t == END * 16
    drum("c", MELT * 16, 0.9)
    if COUNT:
        beat(MELT, MELT + 12, snare=(4, 12), cym="h", step=int(COUNT.split(";")[2]), vel=float(COUNT.split(";")[3]))
        crashes = {n["at"] for n in T["cym"] if n["pitch"] == "c"}
        for h in HEADS:                   # the china where each statement starts (a crash already there stands)
            if round(h / 4, 4) not in crashes:
                drum(COUNT.split(";")[0], h, float(COUNT.split(";")[1]))
    else:
        beat(MELT, MELT + 12, snare=(4, 12), cym="x", vel=0.5)
    beat(MELT + 12, MELT + 22, snare=(8,), cym="h", vel=0.5)
    beat(MELT + 22, END, cym="h", vel=0.42)
    for t, root, k in KNOCKS:             # v8: the block knocks where each statement starts
        v1, v0 = float(KNOCK.split(";")[3]), float(KNOCK.split(";")[5])
        add("knock", t, 1, F1 + root + int(KNOCK.split(";")[2]), round(v0 + (v1 - v0) * min(1.0, (k - 1) / 15), 3))
    # one chord: the total
    for tr in G_TOT:
        add(tr, END * 16, 32, ",".join(nm(F1 + i) for i in (0, 7, 12, 19)), 0.95)
    add("bass", END * 16, 32, F1, 0.95)
    drum("k", END * 16, 0.95)
    drum("c", END * 16, 0.95)


def song():
    compose()
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"            # a take a side
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"            # a second take a side through another amp, microphone and cone
    GM, GD = os.environ.get("C10T4_GMAIN", "-0.7dB"), os.environ.get("C10T4_GDBL", "-1.5dB")
    tracks = [
        {"name": "gl", "patch": main.format(20), "gain": GM, "pan": -1, "out": "gtrs"},
        {"name": "gr", "patch": main.format(21), "gain": GM, "pan": 1, "out": "gtrs"},
        {"name": "gl2", "patch": dbl.format(22), "gain": GD, "pan": -0.75, "out": "gtrs"},
        {"name": "gr2", "patch": dbl.format(23), "gain": GD, "pan": 0.75, "out": "gtrs"},
        *([{"name": tr, "patch": RIG2.split(";")[i], "gain": RIG2.split(";")[2], "pan": (-0.75, 0.75)[i], "out": "gtrs",
            **({"fx": [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*RIG2.split(";")[3].split(":"))]}]} if RIG2.split(";")[3] else {})}
           for i, tr in enumerate(("wl", "wr"))] if RIG2 else []),
        {"name": "wood", "patch": "modal-marimba", "gain": os.environ.get("C10T4_WOOD", "-14dB"), "pan": -0.15, "sends": {"hall": "-10dB"}},
        *([{"name": "knock", "patch": KNOCK.split(";")[0], "gain": KNOCK.split(";")[1], "pan": 0.2, "sends": {"hall": KNOCK.split(";")[4]}}] if KNOCK else []),
        *([{"name": "lead", "patch": TUNE.split(";")[0],
            "gain": {"value": TUNE.split(";")[1], "mod": [{"src": "auto.melt", "amount": 1}]} if MELTUNE else TUNE.split(";")[1],
            "pan": 0, "sends": {"hall": TUNE.split(";")[3]},
            **({"auto": {"melt": {"points": [["0b", 0], [f"{MELT * 4 - 0.5:g}b", 0], [f"{MELT * 4:g}b", float(MELTUNE.split(";")[1])],
                                             [f"{MELT_END[0]:g}b", float(MELTUNE.split(";")[2])]]}}} if MELTUNE else {})}] if TUNE else []),
        *([{"name": tr, "patch": CLEAN.split(";")[i], "gain": CLEAN.split(";")[2 + i], "pan": (-0.5, 0.5)[i], "sends": {"hall": CLEAN.split(";")[8]}}
           for i, tr in enumerate(("cl", "cr"))] if CLEAN else []),
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
    ]
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])
    return {
        "about": ("chirpers X (Common Time), track 4 by chirper-zero: Running Total. One riff, two bars of sixteenths, never simply played but "
                  "added up: its first place, its first two, its first three ... each statement from the top and one place longer, so "
                  "the riff's head lands somewhere new in the bar every time; the sum closes on a bar line exactly when the riff is "
                  "whole. Then the same sum from the other end, and at last undone. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    **({KNOCK.split(";")[0]: BLOCK} if KNOCK else {})},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            "low": ({"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                     {"kind": "peak", "cutoff": key_f(350) if KEYEQ == "all" else 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": key_f(1500) if KEYEQ == "all" else 1500, "q": 1.0, "gain": "4dB"}]},
                            {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                            {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]}],
                     "auto": {"key": {"points": [["0b", 0]] + [pt for (b, k), prev in zip(((TOTAL1 + 8, 3), (BACK, 6), (TOTAL2, 7), (TOTAL2 + 8, 0)), (0, 3, 6, 7))
                                                                for pt in ([f"{b * 4 - 0.02:g}b", prev], [f"{b * 4:g}b", k])], "curve": 0}}} if KEYEQ else
                    {"fx": [{"type": "eq", "bands": ["peak cutoff=44 q=1.5 gain=-7dB", "peak cutoff=90 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                            {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                            {"type": "eq", "bands": ["peak cutoff=170 q=1.2 gain=-3dB"]}]}),
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T4_MASTER", "2.7dB")}]},
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
