#!/usr/bin/env python3
"""chirpers6-t3 (All the Lights Left On, track 3) - generator for songs/chirpers6-t3.yaml (chirper-zero).

INSTRUMENTAL POST-METAL / "night freight". 132 bpm, B minor in drop-tuned guitars (the heaviest movement down in A).
Freight by sea (v2: the trains are The Last Train's): a container port at night, where a gantry crane's chain clanking
through its sheave becomes the riff's odd meter - 7/8 (the crane) against 4/4 (the crescendo). Riff-led, heavy/light; the
only voice is the crane operator's intercom. Original; a style, not a version of any track.

Form (bars, meter; the code keeps v1's section names): I QUAYSIDE ("crossing") 32 x 7/8 (a buoy bell rocking on the swell,
waves, a ship's engine throbbing, the crane starting - its chain clanks in 7 - and the foghorn's two low tones) / II
JOINTS 40 x 7/8 (a clean 8-string arpeggio riff on the clank rhythm, fretless bass, rims and toms; a second guitar's
harmonics answer) / III CHUG 64 x 7/8 in four stages (the riff drop-tuned on doubled rigs; its grouping rotated 3+2+2;
the tremolo line on top; a stabbing peak over double kick, and a one-stab break) / IV STACKS ("yard") 32 x 4/4 (wind,
containers set down, air brakes, a reversing alarm far off, the operator: "seven, clear to lift"; a cello drone, an
ebow sings the line augmented) / V CLIMB 48 x 4/4 (toms to full kit, the clean riff stretched to 4/4, then tremolo
walls; the bass walks the riff inverted) / VI UNDERTOW ("derailed") 40 x 4/4 (half-time doom in A, china, sub, the
crane's 7 returning against the 4; then the doom thins to held chords and an ebow cry) / VII LAST SHIP ("lastcar")
32 x 7/8 (the clean riff alone with the buoy bell, the foghorn further out, "last one, lights stay on", waves).

Motifs (compose/chirpers6/motifs.md):
  THE JOINTS   the crane chain's clank - clank-clank ... clank-clank on a 14-sixteenth cycle - and the 2+2+3 riff on it.
  THE CHANGES  Bm(add9) | Gmaj7 | D(add9) | A(add9), two 7/8 bars (or one 4/4 bar pair) each.
  THE LINE     F#4 | D4 E4 | A4 | C#5 B4 - tremolo-picked in the chug, augmented on the ebow in the stacks.
Run: python3 compose/chirpers6/src/chirpers6-t3.py  (writes songs/chirpers6-t3.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C6T3_OUT") or os.path.join(ROOT, "songs", "chirpers6-t3.yaml")
BPM = 132
S = 0.25  # beats per sixteenth
MGAIN = float(os.environ.get("C6T3_MGAIN", "5"))
PORT = os.environ.get("C6T3_PORT", "1") == "1"  # the freight goes by sea (the trains are The Last Train's): a buoy bell, waves, a ship's engine throbbing, a gantry crane's chain clanking through its sheave on the 14-sixteenth cycle, a foghorn; the yard becomes the container stacks
DEV = os.environ.get("C6T3_DEV", "1") == "1"
VOX = os.environ.get("C6T3_VOX", "1") == "1"
LIFT = os.environ.get("C6T3_LIFT", "1") == "1"  # the climb's last 16 bars (the full kit) a whole tone up, in C# - so the undertow's fall to A is a major third down
FILLS = os.environ.get("C6T3_FILLS", "1") == "1"  # a drummer's vocabulary: tom fills on the last half-bar of every 8-bar phrase in the chug, the climb and the undertow; snare rolls into the chug and into the climb's full kit
SWELLS = os.environ.get("C6T3_SWELLS", "1") == "1"
HOIST = os.environ.get("C6T3_HOIST", "1") == "1"  # the operator's words move the crane: after "clear to lift" a hoist motor whines upward far across the stacks, after "lowering" it falls away and a container lands
WINDDOWN = os.environ.get("C6T3_WINDDOWN", "1") == "1"  # in the last ship the crane winds down: its chain's clank cycle stretches (14, 14, 16, 18, 20, 24, 28, 34, 42 sixteenths) and stops, under the clean riff
ANSWER = os.environ.get("C6T3_ANSWER", "1") == "1"
ENDFIX = os.environ.get("C6T3_ENDFIX", "1") == "1"  # no dead air into Sodium: the buoy bell rings to the last bar, the waves are held to the end, and the render tail is 1 s
PUMP = os.environ.get("C6T3_PUMP", "1") == "1"  # the low end breathes with the kick: the fuzz bass, the sub and both rigs pump (sidechain) from the room kit's kick
BASSLFO = os.environ.get("C6T3_BASSLFO", "1") == "1"  # the fuzz bass through a low-pass breathing on a 7-bar LFO (the crane's number), resonance up
TSTOP = os.environ.get("C6T3_TSTOP", "1") == "1"
LANDMARK = os.environ.get("C6T3_LANDMARK", "1") == "1"
TILT = os.environ.get("C6T3_TILT", "5,4")
SYNC = os.environ.get("C6T3_SYNC", "0") == "1"
DLY = os.environ.get("C6T3_DLY", "-8")  # a dotted-eighth delay bus (3/16, the post-rock echo whose repeats fall between the eighths): the clean riff, the harmonics, the tremolo lead and the ebow send to it at this level (dB)  # the kick finds the 16ths: in the chug's third stage (THE LINE over the riff) the kick plays 0, 3, 6, 8, 11 (with the rigs accenting the 3 and the 11), and the climb's full kit pushes on the 3 and the 11  # "low,high": the master's 150 Hz up and 3.5 kHz down (dB) - the body under the guitars, the fizz down; darker  # chirper-one's note (9.0): one changed bar a phrase - in the chug the fourth bar of every 8 is the crane's chain alone over the sub (the rigs, the fuzz and the kit drop out), and in the climb the fourth bar drops its back half  # the chug's last stab tape-stops: the crane brakes before the stacks  # a second ship answers the foghorn from further out (A and E, lower and quieter)  # reverse-cymbal swells drawn into the chug, the climb's full kit, the undertow and the last ship  # the crane operator on a handheld intercom in the stacks ("seven, clear to lift" - the 7 is the meter), and in the last ship's bars "last one, lights stay on"  # the movements develop instead of looping: the chug in four stages (the riff, its grouping rotated 3+2+2, the line over it, a stabbing peak and a break), a second clean guitar's harmonics answering in the joints, the doom thinning to held chords and an ebow cry

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
SEVEN, FOUR = 14, 16
FORM = [("crossing", 32, SEVEN), ("joints", 40, SEVEN), ("chug", 64, SEVEN), ("yard", 32, FOUR),
        ("climb", 48, FOUR), ("derailed", 40, FOUR), ("lastcar", 32, SEVEN)]
# (heavy root, clean voicing): B minor
CH = [(35, [47, 54, 61, 62, 66, 71]),   # Bm(add9): B2 F#3 C#4 D4 F#4 B4
      (31, [43, 50, 54, 57, 59, 62]),   # Gmaj7(9): G2 D3 F#3 A3 B3 D4
      (38, [50, 57, 62, 64, 66, 69]),   # D(add9): D3 A3 D4 E4 F#4 A4
      (33, [45, 52, 57, 59, 61, 64])]   # A(add9): A2 E3 A3 B3 C#4 E4
LINE = [[("F#4", 28)], [("D4", 14), ("E4", 14)], [("A4", 28)], [("C#5", 14), ("B4", 14)]]
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
        "A#": 10, "Bb": 10, "B": 11}
TRACKS = ("bell", "rumble", "clack", "horn", "wind", "clean", "fretless", "chugl", "chugr", "fuzz", "sub", "kit", "lead",
          "cello", "ebow", "yardmetal", "waves", "hiss", "beep", "harm", "vox", "swell", "horn2", "hoist", "lower", "clank2")


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def midi(n):
    return 12 * (int(n[-1]) + 1) + NOTE[n[:-1]]


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def grid(events, steps):
    ev = sorted(events)
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos or st >= steps:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else steps
        ln = max(1, min(ln, nxt - st, steps - st))
        out.append(R((st - pos) * S))
        note, _, art = head.partition("^")
        out.append(f"{note}/{ln * S:g}b@{int(vel)}" + (f"^{art}" if art else ""))
        pos = st + ln
    out.append(R((steps - pos) * S))
    return J(*out)


def layout():
    """[(section, bar-in-section, bar steps, absolute start step)] for every bar."""
    bars, t = [], 0
    for sec, nb, steps in FORM:
        for b in range(nb):
            bars.append((sec, b, steps, t))
            t += steps
    return bars, t


def sec_start(name):
    t = 0
    for sec, nb, steps in FORM:
        if sec == name:
            return t
        t += nb * steps
    raise KeyError(name)


def chord_of(sec, b, steps):
    """One chord per two bars (LIFT: the climb's last 16 bars a whole tone up)."""
    r, v = CH[(b // 2) % 4]
    if LIFT and sec == "climb" and b >= 32:
        return r + 2, [n + 2 for n in v]
    return r, v


def build():
    bars, total = layout()
    ev = {k: [] for k in TRACKS}  # absolute (step, head, len, vel)

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    # THE JOINTS: the wheels' clacks on a 14-step cycle, wherever the train is (independent of the bars)
    def clacks(a, b, v0, v1):
        n = b - a
        for t in range(a, b):
            ph = (t - a) % 14
            if ph in (0, 2, 8, 10):
                v = v0 + (v1 - v0) * (t - a) / max(1, n)
                add("clack", t, "C4" if ph in (0, 8) else "D4", 1, v * (1.0 if ph in (0, 8) else 0.8))

    s1 = sec_start("crossing")
    clacks(s1 + 12 * 14, sec_start("joints") + 16 * 14, 40, 112)  # approaching, passing, still rattling past
    s6 = sec_start("derailed")
    clacks(s6 + 16 * 16, sec_start("lastcar"), 70, 118)  # the train comes back: 7 against the 4
    s7 = sec_start("lastcar")
    if WINDDOWN and PORT:  # the crane winds down: each cycle longer, the pairs softer, then nothing
        t, k = s7, 0
        for cyc in (14, 14, 14, 14, 16, 16, 18, 18, 20, 22, 24, 28, 34, 42):
            v = 112 - 5 * k
            half = cyc * 8 // 14
            for off, acc in ((0, 1.0), (2, 0.8), (half, 1.0), (half + 2, 0.8)):
                add("clank2", t + off, "C4" if acc == 1.0 else "D4", 1, v * acc)
            t += cyc
            k += 1
    else:
        clacks(s7, s7 + 16 * 14, 70, 20)  # the last car receding

    for sec, b, steps, at in bars:
        r, v = chord_of(sec, b, steps)
        ln = steps * S

        def put(tr, head, vel, st=0, l=None):
            add(tr, at + st, head, steps - st if l is None else l, vel)

        # --- field sounds
        if not PORT and ((sec == "crossing" and b < 24) or (sec == "lastcar" and 4 <= b < 20)):
            for q in range(0, steps, 4):
                add("bell", at + q, "E5", 2, 72 if sec == "crossing" else 50)
        if sec == "crossing" and b == 8:
            add("rumble", at, "C3", 24 * 14, 100)  # the freight's rumble (PORT: the ship's engine), held
        if sec == "lastcar" and b == 0:
            add("rumble", at, "C3", 20 * 14, 70)
        if not PORT:
            if sec == "crossing" and b in (18, 20):
                put("horn", "F#4,A4,C#5", 96, 0, 14 + 7)  # the horn, three tones
            if sec == "crossing" and b == 22:
                put("horn", "F4,G#4,C5", 84, 0, 14 + 10)  # passing: the doppler drop
            if sec == "lastcar" and b == 6:
                put("horn", "E4,G4,B4", 54, 0, 21)  # far away now
        else:
            if sec == "crossing" and b in (14, 22):
                put("horn", "B1,F#2", 104, 0, 3 * 14)  # the foghorn: two low tones, long
            if sec == "lastcar" and b == 10:
                put("horn", "B1,F#2", 70, 0, 3 * 14)  # another ship, further out
            if ANSWER and ((sec == "crossing" and b == 18) or (sec == "lastcar" and b == 16)):
                put("horn2", "A1,E2", 72 if sec == "crossing" else 48, 0, 3 * 14)  # answered from further out
            if (sec == "crossing" and b == 0) or (sec == "lastcar" and b == 0):
                add("waves", at, "C3", (32 if sec == "crossing" else 32) * 14, 64 if sec == "crossing" else 52)
        if (sec == "crossing" and b == 0) or (sec == "yard" and b == 0) or (sec == "lastcar" and b == 12):
            nb = {"crossing": 32, "yard": 32, "lastcar": 20}[sec]
            add("wind", at, "C4", nb * steps, 70 if sec != "crossing" else 50)

        # --- the clean riff (THE JOINTS): 7 eighths, 2+2+3
        if sec in ("joints", "lastcar") or (sec == "crossing" and b >= 24) or (sec == "chug" and b < 8):
            idx = [0, 2, 3, 1, 4, 2, 5] if b % 2 == 0 else [0, 2, 3, 1, 4, 3, 2]
            for k, i in enumerate(idx):
                acc = k in (0, 2, 4)
                vel = (82 if acc else 66) - (20 if sec == "crossing" else 0) - (14 if (sec == "lastcar" and b >= 24) else 0)
                add("clean", at + 2 * k, nm(v[i]), 2, vel)
        if sec == "climb" and b < 16:  # stretched to 4/4: eight eighths
            idx = [0, 2, 3, 1, 4, 2, 5, 3]
            for k, i in enumerate(idx):
                add("clean", at + 2 * k, nm(v[i]), 2, 80 if k % 2 == 0 else 64)

        # --- bass
        if sec == "joints" or (sec == "lastcar" and 8 <= b < 24):
            for st, l in ((0, 4), (4, 4), (8, 6)):
                add("fretless", at + st, nm(r + 12), l, 88 if st == 0 else 74)
        if sec == "yard":
            if b % 2 == 0:
                put("cello", f"{nm(r + 12)},{nm(r + 19)}", 70, 0, 32)
        if sec == "chug" or (sec == "climb" and b >= 16):
            if steps == SEVEN:
                for st, l in ((0, 2), (2, 2), (4, 2), (6, 2), (8, 6)):
                    add("fuzz", at + st, nm(r + 12), l, 100 if st in (0, 8) else 82)
            else:  # the climb: the riff inverted - the bass walks down where the clean riff went up
                walk = [r + 12, r + 10, r + 7, r + 5]
                for k, n in enumerate(walk):
                    add("fuzz", at + 4 * k, nm(n), 4, 98 if k == 0 else 84)
        if sec in ("chug",) or (sec == "climb" and b >= 32):
            put("sub", nm(r), 90)
        if sec == "derailed":
            put("sub", nm(33 if (DEV and b >= 32) else DOOM[b % 4][0]), 96)

        # --- the heavy rigs
        if sec == "chug":
            pc = lambda n: f"{nm(n)},{nm(n + 7)},{nm(n + 12)}"  # noqa: E731
            stage = b // 16 if DEV else 0
            if stage == 1:  # the grouping rotated: 3+2+2 - the open chord first, the chugs after
                hits, ring = (6, 7, 8, 10, 11, 12), (0, 6)
            elif stage == 3:  # the peak: stabs on every group, ringing
                hits, ring = (), None
            else:
                hits, ring = (0, 1, 2, 4, 5, 6), (8, 6)
            if DEV and b == 63:  # the break before the yard: one stab, then nothing
                hits, ring = (), (0, 3)
            accents = (6, 10) if stage == 1 else (0, 4)
            if SYNC and stage == 2:
                hits = tuple(sorted(set(hits) | {3, 11})) if ring and ring[0] == 8 else hits
            for st in hits:
                add("chugl", at + st, nm(r) + "^pm", 1, 104 if st in accents else 92)
                add("chugr", at + st, nm(r) + "^pm", 1, 102 if st in accents else 90)
            if ring:
                add("chugl", at + ring[0], pc(r), ring[1], 118)
                add("chugr", at + ring[0], pc(r), ring[1], 116)
            if stage == 3 and b != 63:
                for st, l in ((0, 4), (4, 4), (8, 6)):
                    add("chugl", at + st, pc(r), l, 120)
                    add("chugr", at + st, pc(r), l, 118)
        if sec == "climb" and b >= 16:  # tremolo walls: power chords picked in 16ths
            pc = f"{nm(r)},{nm(r + 7)},{nm(r + 12)}"
            vel = 80 + (b - 16)
            add("chugl", at, pc + "^r=8", 8, vel)
            add("chugl", at + 8, pc + "^r=8", 8, vel)
            add("chugr", at, pc + "^r=8", 8, vel - 2)
            add("chugr", at + 8, pc + "^r=8", 8, vel - 2)
        if DEV and sec == "derailed" and b >= 32:  # the doom thins: one held chord every two bars, the ebow crying over it
            if b % 2 == 0:
                add("chugl", at, f"{nm(33)},{nm(40)},{nm(45)}", 32, 104 - 4 * (b - 32))
                add("chugr", at, f"{nm(33)},{nm(40)},{nm(45)}", 32, 102 - 4 * (b - 32))
            if b == 32:
                add("ebow", at, "A5", 48, 100)
                add("ebow", at + 48, "G5", 32, 90)
                add("ebow", at + 80, "E5", 48, 84)
        elif sec == "derailed":
            d = DOOM[b % 4]
            for st, n, l in d[1]:
                add("chugl", at + st, f"{nm(n)},{nm(n + 7)},{nm(n + 12)}", l, 120)
                add("chugr", at + st, f"{nm(n)},{nm(n + 7)},{nm(n + 12)}", l, 118)

        # --- THE LINE
        if sec == "chug" and b >= 32 and b % 2 == 0:
            cell = LINE[(b // 2) % 4]
            st = 0
            for n, l in cell:
                add("lead", at + st, f"{n}^r={l // 2}", l, 92)
                st += l
        if sec == "yard" and b >= 4 and b % 4 == 0:
            cell = LINE[(b // 4) % 4]
            st = 0
            for n, l in cell:
                add("ebow", at + st, n, l * 64 // 28, 84)
                st += l * 64 // 28
        if sec == "climb" and b >= 24 and b % 2 == 0:
            cell = LINE[(b // 2) % 4]
            st = 0
            for n, l in cell:
                add("ebow", at + st, nm(midi(n) + 12 + (2 if (LIFT and b >= 32) else 0)), l * 32 // 28, 96)
                st += l * 32 // 28

        # --- PORT: the buoy bell rocks on the swell (irregular), the stacks' sounds
        if PORT and ((sec == "crossing" and b < 28) or (sec == "lastcar" and b < (32 if ENDFIX else 24))):
            gaps = (9, 7, 11, 6, 10, 8, 12)
            t0 = at
            if b == 0 or (sec == "crossing" and b == 0):
                pass
            for k in range(0, steps):
                gt = at + k
                acc, n = 0, 0
                while acc < gt - (sec_start(sec)):
                    acc += gaps[n % len(gaps)]
                    n += 1
                if acc == gt - sec_start(sec):
                    add("bell", gt, "B4" if n % 3 else "A#4", 3, (66 if sec == "crossing" else 46) - 6 * (n % 2))
        if PORT and sec == "yard":
            if b % 7 == 3:
                for q in range(0, 16, 4):
                    add("beep", at + q, "C4", 2, 60)  # a straddle carrier reversing, far off
            if b % 3 == 1:
                add("hiss", at + 10, "C4", 6, 80)  # air brakes
            if b % 5 == 0:
                add("yardmetal", at + 2, "ft", 2, 84)  # a container set down
        # --- VOX: the crane operator's intercom (voice-speech, ARPAbet syllables, an eighth each; the last falls)
        if VOX:
            lines = {("yard", 6): ["s-eh1", "v-ah0-n", "k-l-ih1-r", "t-uw0", "l-ih1-f-t"],
                     ("yard", 13): ["l-ow1", "er0", "ih0-ng"],
                     ("yard", 20): ["hh-ow1-l-d"],
                     ("yard", 27): ["s-eh1", "v-ah0-n", "ao1-l", "k-l-ih1-r"],
                     ("lastcar", 14): ["l-ae1-s-t", "w-ah1-n"],
                     ("lastcar", 16): ["l-ay1-t-s", "s-t-ey1", "aa1-n"]}
            words = lines.get((sec, b))
            if words:
                for k, syl in enumerate(words):
                    last = k == len(words) - 1
                    add("vox", at + 2 + 2 * k, "A2^ph=" + syl + ("^f0=0>-60" if last else ""), 3 if last else 2, 84)
        # --- HOIST: the operator's words move the crane
        if HOIST and PORT and sec == "yard":
            if b in (7, 28):
                add("hoist", at, "C3", 16, 76)  # "clear to lift": the hoist whines upward
            if b == 14:
                add("lower", at, "C3", 16, 70)  # "lowering"
            if b == 15:
                add("yardmetal", at + 4, "ft", 2, 96)  # the container lands
                add("yardmetal", at + 5, "cbl", 2, 78)
        # --- DEV: a second clean guitar's natural harmonics answer the riff in the joints
        if DEV and sec == "joints" and b >= 24:
            for st_, i in ((6, 5), (12, 3)):
                add("harm", at + st_, nm(v[i] + 12) + "^nh=2", 2, 70)

        # --- distant metal in the yard (every 5 bars: the odd length keeps it from settling)
        if sec == "yard" and b % 5 == 2:
            add("yardmetal", at + 6, "cbl", 2, 70)
            add("yardmetal", at + 9, "t3", 2, 50)

        # --- drums
        kit = []
        if sec == "joints":
            kit += [(st, "rc", 70 if st in (0, 8) else 54) for st in (0, 2, 8, 10)]
            if b >= 16:
                kit += [(0, "ft", 84), (4, "t3", 72), (8, "ft", 90)]
            if b >= 32:
                kit += [(st, "hf", 50) for st in range(0, 14, 2)]
        elif sec == "chug":
            stage = b // 16 if DEV else 0
            if DEV and b == 63:
                kit += [(0, "k", 120), (0, "c", 124)]
            elif stage == 1:
                kit += [(0, "k", 118), (6, "s", 114), (8, "k", 104), (10, "k", 108), (12, "s", 116)]
                kit += [(st, "rd", 76 if st % 4 == 0 else 62) for st in range(0, 14, 2)]
            elif stage == 3:
                kit += [(st, "k", 108 if st % 2 else 118) for st in range(14)] + [(4, "s", 120), (8, "s", 120), (12, "s", 116)]
                kit += [(0, "c", 122)] if b % 4 == 0 else [(0, "x", 108)]
            elif SYNC and stage == 2:  # syncopated: the kick on the 16ths between the eighths
                kit += [(0, "k", 118), (3, "k", 108), (6, "k", 112), (8, "k", 114), (11, "k", 110), (4, "s", 112), (12, "s", 116)]
                kit += [(st, "rd", 76 if st % 4 == 0 else 62) for st in range(0, 14, 2)]
            else:
                kit += [(0, "k", 118), (2, "k", 104), (8, "k", 114), (4, "s", 112), (11, "s", 116)]
                kit += [(st, "rd", 76 if st % 4 == 0 else 62) for st in range(0, 14, 2)]
            if b % 8 == 0 and not (DEV and (stage == 3 or b == 63)):
                kit += [(0, "c", 118)]
        elif sec == "climb":
            if b < 16:
                kit += [(0, "ft", 70 + b), (8, "t3", 60 + b)]
            elif b < 32:
                kit += [(0, "k", 112), (8, "s", 112)] + [(st, "rd", 70) for st in range(0, 16, 2)]
                if b % 4 == 0:
                    kit += [(0, "c", 112)]
            else:
                kit += [(st, "k", 112) for st in range(0, 16, 2)] + [(4, "s", 118), (12, "s", 118)]
                if SYNC:
                    kit += [(3, "k", 104), (11, "k", 106)]
                kit += [(st, "rde", 90) for st in range(0, 16, 4)]
                if b % 2 == 0:
                    kit += [(0, "c", 122)]
        elif sec == "derailed" and DEV and b >= 32:
            if b % 2 == 0:
                kit += [(0, "k", 112), (0, "c", 110 - 3 * (b - 32))]
        elif sec == "derailed":
            kit += [(0, "k", 120), (6, "k", 108), (8, "s", 122), (4, "x", 100), (12, "x", 106)]
            if b % 4 == 0:
                kit += [(0, "c", 124)]
        nbars = dict((n, c) for n, c, _ in FORM)[sec]
        if FILLS and sec in ("chug", "climb", "derailed") and b % 8 == 7 and not (sec == "derailed" and DEV and b >= 32) and not (sec == "chug" and DEV and b == 63):
            toms = ["t1", "t1", "t2", "t2", "t3", "t3", "ft", "ft"][: steps - 8]
            kit = [k for k in kit if k[0] < 8] + [(8 + i, t, 92 + 4 * i) for i, t in enumerate(toms)]
        if FILLS and ((sec == "joints" and b == nbars - 1) or (sec == "climb" and b == 31)):
            kit = [k for k in kit if k[0] < steps // 2] + [(st, "s", 70 + 6 * (st - steps // 2)) for st in range(steps // 2, steps)]
        if SWELLS and ((sec == "joints" and b == nbars - 1) or (sec == "climb" and b == 31) or (sec == "climb" and b == nbars - 1)
                       or (sec == "derailed" and b == nbars - 1)):
            add("swell", at + steps - 8, "C4", 8, 96)
        for st, piece, vel in kit:
            add("kit", at + st, piece, 1, vel)

    if LANDMARK:  # one changed bar a phrase
        for sec, b, steps, at in bars:
            hole = None
            if sec == "chug" and b % 8 == 3 and (not DEV or b // 16 != 3):
                hole = (at, at + steps, ("chugl", "chugr", "fuzz", "kit", "lead"))
                for ph in (0, 2, 8, 10):
                    add("clack", at + ph, "C4" if ph in (0, 8) else "D4", 1, 118 if ph in (0, 8) else 100)
            elif sec == "climb" and b % 8 == 3:
                hole = (at + 8, at + steps, ("kit", "chugl", "chugr"))
            if hole:
                a, z, trs = hole
                for tr in trs:
                    ev[tr] = [e for e in ev[tr] if not (a <= e[0] < z)]
    # absolute events -> one continuous score per track (long holds simply run on)
    return {k: stream(ev[k], total) for k in TRACKS}


def stream(events, total):
    by = {}
    for st, head, ln, vel in events:  # simultaneous hits on one track (kit pieces) become one chord
        if st in by:
            h0, l0, v0 = by[st]
            n0, _, a0 = h0.partition("^")
            n1 = head.partition("^")[0]
            by[st] = (f"{n0},{n1}" + (f"^{a0}" if a0 else ""), min(l0, ln), max(v0, vel))
        else:
            by[st] = (head, ln, vel)
    ev = sorted((st, h, l, v) for st, (h, l, v) in by.items())
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else total
        hold = max(1, min(ln, max(nxt, st + 1) - st, total - st))
        out.append(R((st - pos) * S))
        note, _, art = head.partition("^")
        out.append(f"{note}/{hold * S:g}b@{int(vel)}" + (f"^{art}" if art else ""))
        pos = st + hold
    out.append(R((total - pos) * S))
    return J(*out)


DOOM = [(33, [(0, 33, 8), (8, 36, 4), (12, 34, 4)]),     # A, C, Bb
        (33, [(0, 33, 12), (12, 31, 4)]),                # A, G
        (36, [(0, 36, 8), (8, 34, 8)]),                  # C, Bb
        (31, [(0, 31, 6), (6, 33, 10)])]                 # G, A


def lane(points):
    _, total = layout()
    pts = [["0s", points[0][1]]]
    spb = 60 / BPM
    for step, val in points[1:]:
        t = step * S * spb
        pts.append([f"{t:.3f}s", val])
    pts.append([f"{total * S * spb + 10:.2f}s", pts[-1][1]])
    return {"points": pts}


def PUMPFX(d):
    return {"type": "pump", "on": "kit.k", "depth": f"{d}dB", "attack": "1ms", "release": "180ms", "curve": 0.8}


def tslane():
    """The chug's last stab winds down: the tape stops from its second eighth to the stacks' downbeat."""
    a, y = sec_start("yard") - 14 + 2, sec_start("yard")
    return lane([(0, 0), (a - 0.05, 0), (a, 1), (y - 0.05, 1), (y, 0)])


def song():
    T = build()
    sc = lambda n: T[n]  # noqa: E731
    st = {sec: sec_start(sec) for sec, _, _ in FORM}
    # the arc in dB on the master: quiet passages stay quiet
    dyn = lane([(0, -6), (st["joints"], -4), (st["chug"], 0), (st["yard"], -6), (st["climb"], -4),
                (st["climb"] + 32 * 16, 0), (st["derailed"], 1), (st["lastcar"], -5)])
    doc = {
        "about": "Chirpers - All the Lights Left On (Chirpers VI), track 3 by chirper-zero: INSTRUMENTAL POST-METAL, night freight. "
                 "Generated by compose/chirpers6/src/chirpers6-t3.py; see its docstring and compose/chirpers6/styles.md.",
        "tempo": BPM, "ceiling": "-1.2dB", "volume": "0dB", "true_peak": True, "tail": "1s" if ENDFIX else "2s",
        "patches": {
            **({"ship-engine": {"about": "night freight (the port): a ship's diesel - brown noise low-passed with a 46 Hz hum, throbbing (tremolo on the track)",
                               "synth": {"layers": [{"type": "noise", "color": "brown"}, "sine fixed=46 level=-8dB"], "filters": ["lp cutoff=130 q=0.8"],
                                         "amp": {"a": "6s", "s": 1, "r": "6s"}}},
                "crane-chain": {"about": "night freight (the port): a gantry crane's chain link over its sheave - a noise crack and two low metal partials",
                                "synth": {"layers": [{"type": "noise", "color": "white"}, "sine fixed=560 level=-5dB", "sine fixed=1040 level=-9dB"],
                                          "filters": ["bp cutoff=1200 q=0.7"], "amp": {"a": "0.5ms", "d": "90ms", "s": 0, "r": "50ms"}}},
                "air-hiss": {"about": "night freight (the port): air brakes releasing - white noise band-passed at 4 kHz, a second's decay",
                             "synth": {"layers": [{"type": "noise", "color": "white"}], "filters": ["bp cutoff=4000 q=0.6"],
                                       "amp": {"a": "5ms", "d": "900ms", "s": 0, "r": "200ms"}}},
                "reverse-beep": {"about": "night freight (the port): a straddle carrier's reversing alarm, far off",
                                 "synth": {"layers": ["sine fixed=1160"], "amp": {"a": "2ms", "s": 1, "r": "10ms"}}}} if PORT else {}),
            "rail-rumble": {"about": "night freight: the train's rumble - brown noise low-passed, swelling in and out over seconds",
                            "synth": {"layers": [{"type": "noise", "color": "brown"}], "filters": ["lp cutoff=160 q=0.8"],
                                      "amp": {"a": "6s", "s": 1, "r": "6s"}}},
            "wheel-clack": {"about": "night freight: a wheel over a rail joint - a noise crack and two metal partials, short",
                            "synth": {"layers": [{"type": "noise", "color": "white"}, "sine fixed=820 level=-6dB", "sine fixed=1370 level=-10dB"],
                                      "filters": ["bp cutoff=1600 q=0.7"], "amp": {"a": "0.5ms", "d": "70ms", "s": 0, "r": "40ms"}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=300 q=0.8 gain=-2dB", "highshelf cutoff=7000 gain=-1dB",
                                                   *([f"peak cutoff=150 q=0.7 gain={TILT.split(',')[0]}dB", f"peak cutoff=3500 q=0.7 gain=-{TILT.split(',')[1]}dB"] if TILT else [])]},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2, "attack": "15ms", "release": "200ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          *([{"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}, "time": "1.5b", "curve": 1.6}] if TSTOP else [])],
                   "auto": {"dyn": dyn, **({"ts": tslane()} if TSTOP else {})}},
        "buses": {
            "drums": {"fx": [{"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "5ms", "release": "90ms", "makeup": "1dB"}]},
            "hall": {"fx": ["reverb kind=hall decay=3.5s size=0.9 mix=1 predelay=30ms"]},
            "yard": {"fx": ["reverb kind=hall decay=6s size=1 mix=1 predelay=60ms", "lp cutoff=2500"]},
            **({"dly": {"fx": ["delay time=3/16 feedback=0.38 mix=1 tone=2800", "hp cutoff=250"], "sends": {"hall": "-8dB"}}} if DLY else {}),
        },
        "tracks": [
            {"name": "bell", "patch": "bell", "gain": "-20dB", "pan": 0.35, "sends": {"yard": "-6dB"}, "score": sc("bell")},
            {"name": "rumble", "patch": "ship-engine" if PORT else "rail-rumble", "gain": "-12dB",
             **({"fx": [{"type": "tremolo", "depth": 0.45, "rate": 2.7}]} if PORT else {}), "score": sc("rumble")},
            {"name": "clack", "patch": "crane-chain" if PORT else "wheel-clack", "gain": "-14dB", "pan": -0.2, "sends": {"yard": "-14dB"}, "score": sc("clack")},
            {"name": "horn", "patch": "brass-synth", "gain": "-12dB" if PORT else "-16dB", "fx": [{"type": "filter", "kind": "lp", "cutoff": 900 if PORT else 2200, "q": 0.7}],
             "sends": {"yard": "-4dB"}, "score": sc("horn")},
            *([{"name": "waves", "patch": "fx-ocean", "gain": "-16dB", "score": sc("waves")},
               {"name": "hiss", "patch": "air-hiss", "gain": "-22dB", "pan": 0.4, "sends": {"yard": "-6dB"}, "score": sc("hiss")},
               {"name": "beep", "patch": "reverse-beep", "gain": "-34dB", "pan": -0.5, "sends": {"yard": "0dB"}, "score": sc("beep")}] if PORT else []),
            *([{"name": "clank2", "patch": "crane-chain", "gain": "-4dB", "pan": -0.35, "sends": {"yard": "-8dB"}, "score": sc("clank2")}] if (WINDDOWN and PORT) else []),
            *([{"name": "horn2", "patch": "brass-synth", "gain": "-18dB", "pan": 0.5, "fx": [{"type": "filter", "kind": "lp", "cutoff": 700, "q": 0.7}],
                "sends": {"yard": "0dB"}, "score": sc("horn2")}] if ANSWER else []),
            *([{"name": "hoist", "patch": "fx-riser-pitch", "gain": "-2dB", "pan": 0.3,
                "fx": [{"type": "filter", "kind": "bp", "cutoff": 1000, "q": 0.7}], "sends": {"yard": "-4dB"}, "score": sc("hoist")},
               {"name": "lower", "patch": "fx-downlifter", "gain": "-2dB", "pan": 0.3,
                "fx": [{"type": "filter", "kind": "bp", "cutoff": 1000, "q": 0.7}], "sends": {"yard": "-4dB"}, "score": sc("lower")}] if HOIST else []),
            *([{"name": "swell", "patch": "fx-revcym", "gain": "-14dB", "sends": {"hall": "-8dB"}, "score": sc("swell")}] if SWELLS else []),
            *([{"name": "vox", "patch": "voice-speech", "gain": "-8dB", "pan": -0.3,
                "fx": [{"type": "filter", "kind": "hp", "cutoff": 400, "q": 0.7}, {"type": "filter", "kind": "lp", "cutoff": 3200, "q": 0.9},
                       {"type": "drive", "drive": 0.45, "mix": 1}], "sends": {"yard": "-10dB"}, "score": sc("vox")}] if VOX else []),
            *([{"name": "harm", "patch": "clean-chorus", "gain": "-12dB", "pan": 0.45, "sends": {"hall": "-6dB", **({"dly": f"{DLY}dB"} if DLY else {})}, "score": sc("harm")}] if DEV else []),
            {"name": "wind", "patch": "fx-wind", "gain": "-18dB", "score": sc("wind")},
            {"name": "clean", "patch": "clean-chorus", "gain": "-8dB", "pan": -0.15, "sends": {"hall": "-10dB", **({"dly": f"{DLY}dB"} if DLY else {})}, "score": sc("clean")},
            {"name": "fretless", "patch": "fretless-bass", "gain": "-6dB", "score": sc("fretless")},
            {"name": "chugl", "patch": "m8-rhythm-l", "gain": "-10dB", "pan": -0.7, **({"fx": [PUMPFX(-3)]} if PUMP else {}), "score": sc("chugl")},
            {"name": "chugr", "patch": "m8-rhythm-r", "gain": "-10dB", "pan": 0.7, **({"fx": [PUMPFX(-3)]} if PUMP else {}), "score": sc("chugr")},
            {"name": "fuzz", "patch": "bass-fuzz", "gain": "-8dB",
             **({"fx": ([PUMPFX(-5)] if PUMP else []) + ([{"type": "filter", "kind": "lp", "cutoff": {"value": 700, "mod": [{"src": "lfo.b", "amount": 1.0}]}, "q": 1.6}] if BASSLFO else [])}
                if (PUMP or BASSLFO) else {}),
             **({"lfo": {"b": "sine rate=7/1"}} if BASSLFO else {}), "score": sc("fuzz")},
            {"name": "sub", "patch": "sub-sine", "gain": "-10dB", **({"fx": [PUMPFX(-6)]} if PUMP else {}), "score": sc("sub")},
            {"name": "kit", "patch": "room-kit", "gain": "-2dB", "out": "drums", "score": sc("kit")},
            {"name": "lead", "patch": "m8-lead-guitar", "gain": "-14dB", "pan": 0.2, "sends": {"hall": "-8dB", **({"dly": f"{DLY}dB"} if DLY else {})}, "score": sc("lead")},
            {"name": "cello", "patch": "cellos", "gain": "-8dB", "sends": {"hall": "-6dB"}, "score": sc("cello")},
            {"name": "ebow", "patch": "ebow", "gain": "-10dB", "pan": 0.1, "sends": {"hall": "-8dB", **({"dly": f"{DLY}dB"} if DLY else {})}, "score": sc("ebow")},
            {"name": "yardmetal", "patch": "metal-kit", "gain": "-14dB", "pan": 0.5, "sends": {"yard": "0dB"}, "score": sc("yardmetal")},
        ],
    }
    return doc


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "volume", "true_peak", "tail", "patches", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
