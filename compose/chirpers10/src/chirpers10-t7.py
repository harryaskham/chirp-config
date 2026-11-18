#!/usr/bin/env python3
"""chirpers10-t7 "Extreme and Mean" (chirper-zero): one pattern of longs and shorts, the same at every size.

Euclid cuts a line "in extreme and mean ratio" when the whole is to the longer part as the longer is to the shorter.
A line cut so has no common measure: no unit, however small, goes a whole number of times into both parts. This piece
is that cut made in time, and it is the record's slow song (80 where the other six run 100 to 138).

There are two cells: a LONG of three sixteenths and a SHORT of two. And one rule, applied to every cell at once:

    a long becomes a long and a short;  a short becomes a long.

Start from one long and apply the rule over and over: L, LS, LSL, LSLLS, LSLLSLSL ... Each line is the line before
it followed by the line before that. The pattern never falls into a loop, yet every stretch of it comes back; and it
is the same at every size: group the cells as the rule made them and the groups are again longs and shorts in the
same order, 5 and 3 sixteenths, then 8 and 5, 13 and 8, 21 and 13 ... up to 233 and 144.

So the band plays ONE pattern at many sizes at once:

  cells of 3 and 2          the guitars' muted strokes (a long is two strokes and a rest, a short one stroke and a
                            rest), with the bass and the kick locked to them
  cells of 8 and 5          the string is let ring: an open low note
  cells of 13 and 8         a chord (on the long ones the root; on the short ones, from the third section, a tritone up)
  cells of 34 and 21        a crash
  cells of 55 and 34        the root: home on the long ones, a semitone up on the short ones
  cells of 233 and 144      THE SECTIONS OF THE SONG: the long ones heavy, the short ones quiet. Long, short, long,
                            long, short, long, short, long: the form is the riff, 78 times slower.

The whole song is the fourteenth line of the rule: 1597 sixteenths, and then one chord where the fifteenth would
begin. The kit keeps common time against all of it (the china in quarters, the snare on three) and starts its count
again at each section. A long section is fourteen bars and nine sixteenths; a short one is exactly nine bars.

In the quiet sections the rule is said another way, by the engine itself: a wire harp (Karplus-Strong, the first on
this record) is given no notes, only the rule as an L-system (the first on this record), written so that each short
cell is born one step up the scale from the long cell that made it. Its tune is therefore each phrase followed by
the phrase before it, one step higher. In the last section the harp plays over the band: the two sayings together.

v1 is the SKELETON (Harry, 17 Nov about 03:40: "open up 2 new song slots"; track 2's terms: mine, my title, a
skeleton first): the whole shape standing, bare.
"""
import bisect
import json
import os

OUT = os.environ.get("C10T7_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t7.yaml"))
BPM = 80
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}
GEN = 14                                  # the song is the rule's fourteenth line
TOP = 9                                   # the cells that are the song's sections
# the harp: gain ; hall send ; gain in the last section, over the band ("" = it does not play there)
HARP = os.environ.get("C10T7_HARP", "-14dB;-10dB;-12.5dB")
PAD = os.environ.get("C10T7_PAD", "7.5dB;-9dB")        # the clean guitar's chords in the quiet sections: gain ; hall send
# the bass in the quiet sections, dB after its bus (its compressor holds a long soft note at the level of a hard short
# one, so a lower velocity does not make it quieter; this does)
QBASS = os.environ.get("C10T7_QBASS", "-4.5")
# v2, THE SAME TUNE AT EVERY SIZE: the three quiet sections were the same nine bars three times. Now the second has two
# harps and the third three, and each added harp plays THE SAME TUNE ON LARGER CELLS (5 and 3 sixteenths; then 8 and 5),
# an octave lower each: a canon in which the voices' speeds stand as the long cell to the short. Every note of a slower
# harp falls with a note of the faster ones. The second voice's gain ; the third's. "" = v1.
CANON = os.environ.get("C10T7_CANON", "-16dB;-18dB")
# v3, THE TUNE AT THE LARGEST SIZE A BREATH CAN HOLD: cells of 21 and 13 sixteenths (3.9 and 2.4 seconds) had no voice of
# their own. In the four-guitar sections a brass section (horns and trombones on the engine's physical lips: the record's
# first `wind` source) plays the harp's tune on those cells, one long note to a cell: strings plucked for the small
# sizes, breath for the large one. patch ; gain ; velocity ; semitones over the harp's pool (an octave up: at the harp's
# own octave its notes sat at 250-500 Hz and read 7 dB over the records there) ; a dip at its lowest notes (Hz : q : dB).
# "" = v2.
BRASS = os.environ.get("C10T7_BRASS", "brass;-13dB;0.8;12;400:1:-3")
# v4: the last 89 sixteenths of the second two-guitar riff. A steel above the fretted guitars
# bends its way through 55, then 34: the short line is literally the head of the long one.
# Dry and close, not a third wall of rhythm guitar. Empty regenerates v3.
STEEL = os.environ.get("C10T7_STEEL", "-12dB")
# v5: the last riff sheds its smallest strokes before the whole band signs the final chord.
PEEL = os.environ.get("C10T7_PEEL", "1")
# v6: a shared pitch, a rubbed rim on a long cell and a felt stroke on a short.
# Middle quiet section only. Track trims in dB (rim; mallet); empty gives v5.
BOWL = os.environ.get("C10T7_BOWL", "-16;-13")
# v7: in the return to F, the wall pair plays the riff three sizes larger.
# Empty restores v6; the v6 BOWL-empty switch still restores v5.
BIG_STROKES = os.environ.get("C10T7_BIG_STROKES", "1" if BOWL else "")
# v8: the horn borrows five notes from the lowest harp before the last
# quiet section. Empty restores v7; older rollback switches keep working.
REVEAL = os.environ.get("C10T7_REVEAL", "1") if BIG_STROKES and CANON and BRASS else ""
# v9: after 55 sixteenths the first riff's short children go to a pitched log drum.
# Track gain; empty restores v8. Keep the older rollback switches intact.
CHILD = os.environ.get("C10T7_CHILD", "-5dB") if REVEAL else ""
# v10: the heavy middle anticipates the bowl's chords; the last one opens into F minor.
PIVOT = os.environ.get("C10T7_PIVOT", "1") if CHILD else ""  # empty restores v9
# v11: after the wall pair has played the riff three sizes larger, the foot plays it
# one size smaller (cells of 2 and 1); bass and inside guitars follow. Empty = v10.
SMALLER = os.environ.get("C10T7_SMALLER", "1") if PIVOT else ""
# v12: THE GROUND RISES UNDER THE HARP (section round, 4:42.8-4:49.1, in the window 4:24-4:48 the map calls static:
# nothing entered or left between the harp's entry at 4:16 and the peel). With 89 sixteenths to go the last section
# is three cells: 34, 21, 34. The last was already a semitone up (the rule for cells of 34) and the 21 is where the
# riff starts to fall away. In the first 34 the harp over the band plays only A flat, C and E flat, and the horn's
# two breaths there are A flat and C: an A flat major chord that the band, chugging F under it, never let be one.
# Now for that one cell the four guitars and the bass move up a minor third, to the middle sections' A flat, and
# the same notes are heard as what they spell. The harp's last note in the cell is F: it falls home a sixteenth
# before the band does, on the crash where the outer guitars begin to peel. So the last 89 are a lift (A flat),
# home thinning (F), the semitone (G flat), and the chord. Nothing but the root moves: every stroke, the kit, the
# harp and the horn are as they were.
# semitones the ground rises for that cell. "" = v11.
LIFT = os.environ.get("C10T7_LIFT", "3") if SMALLER and PEEL else ""


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


def word(n):
    """Line n of the rule: W1 = L, W2 = LS, Wn = W(n-1) W(n-2)."""
    a, b = "L", "LS"
    for _ in range(n - 2):
        a, b = b, b + a
    return a if n == 1 else b


SIZE = [(3, 2)]                           # SIZE[k] = (a long's sixteenths, a short's) at size k
for _k in range(GEN):
    SIZE.append((SIZE[-1][0] + SIZE[-1][1], SIZE[-1][0]))


def cells(k):
    """The song at size k: (start sixteenth, 'L' or 'S', length)."""
    out, t = [], 0
    for c in word(GEN - k):
        n = SIZE[k][c == "S"]
        out.append((t, c, n))
        t += n
    return out


LEV = [cells(k) for k in range(GEN)]
STARTS = [[c[0] for c in lv] for lv in LEV]
TOTAL = LEV[0][-1][0] + LEV[0][-1][2]
assert TOTAL == 1597 and all(lv[-1][0] + lv[-1][2] == TOTAL for lv in LEV) and SIZE[TOP] == (233, 144)
assert all(set(STARTS[k + 1]) <= set(STARTS[k]) for k in range(GEN - 1))     # every size's cells begin where smaller cells do
RANK = {}
for _k, _s in enumerate(STARTS):
    for _p in _s:
        RANK[_p] = _k                     # the largest size of cell that begins here


def at_size(k, p):
    """The size-k cell that sixteenth p lies in."""
    return LEV[k][bisect.bisect_right(STARTS[k], p) - 1]


LIFT_SPAN = (TOTAL - SIZE[7][0], TOTAL - SIZE[6][0])        # v12: from 89 to go until 55 to go
assert at_size(5, LIFT_SPAN[0]) == (LIFT_SPAN[0], "L", LIFT_SPAN[1] - LIFT_SPAN[0])      # one long cell of 34, crash to crash


SECS = LEV[TOP]                           # eight: L S L L S L S L
KEY = [0, 0, 0, 3, 3, 0, 0, 0]            # home, a minor third up for the middle pair, home (the rule's own grouping: 3 + 2 + 3)
WIDE = {3, 5, 7}                          # four guitars


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym", "rde": "cym"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 1.0 if piece == "rde" else 0.5 if piece == "h" else 0.25,
                                 "pitch": piece, "vel": round(vel, 3)})


ROOTS = []                                # (sixteenth, the bass's root in semitones over F1): the low bus's eq follows it


def heavy(i, s0, n):
    twins, walls = ("gl", "gr"), ("wl", "wr")
    # The first 55 sixteenths of this return stay in unison, as do the
    # 89 after the exchange. Both seams fall at the head of a size-3 cell.
    spread_at, together_at = s0 + SIZE[6][0], s0 + SIZE[8][0]
    for p, kind, ln in LEV[0]:
        if not s0 <= p < s0 + n:
            continue
        big = BIG_STROKES and i == 5 and spread_at <= p < together_at
        gtrs = twins + walls if i in WIDE and not big else twins
        r = RANK[p]
        root = KEY[i] + (1 if at_size(6, p)[1] == "S" else 0)
        if LIFT and LIFT_SPAN[0] <= p < LIFT_SPAN[1]:
            root += int(LIFT)
        if not ROOTS or ROOTS[-1][1] != root:
            ROOTS.append((p, root))
        if r >= 3:                        # a chord: the root on a long cell of 13, a tritone up on a short one of 8
            up = 6 if at_size(3, p)[1] == "S" and i >= 2 else 0
            for tr in gtrs:
                add(tr, p, ln, ",".join(nm(F1 + root + up + j) for j in (0, 7, 12)), 1.0)
            if big:
                # Magnify each one-sixteenth stroke by three substitutions:
                # L = hit(5), hit(3), rest(5); S = hit(5), rest(3).
                # The second attack turns the fifth upside down; it is not
                # a new chord. Let go before each next stroke.
                first, second = SIZE[1]
                base = F1 + root + up
                for tr in walls:
                    add(tr, p, first - 0.5, f"{nm(base)},{nm(base + 7)}", 0.97)
                    if at_size(3, p)[1] == "L":
                        add(tr, p + first, second - 0.5, f"{nm(base + 7)},{nm(base + 12)}", 0.92)
            add("bass", p, ln, F1 + root + up, 0.95)
            drum("k", p, 0.95)
            if r >= 5:
                drum("c", p, 0.9 if r >= 8 else 0.75)
        elif r == 2:                      # the string let ring
            for tr in gtrs:
                add(tr, p, 2, F1 + root, 1.0)
            add("bass", p, 2, F1 + root, 0.95)
            drum("k", p, 0.95)
            if ln == 3:
                for tr in gtrs:
                    add(tr, p + 2, 1, F1 + root, 0.85, pm=1)
                add("bass", p + 2, 1, F1 + root, 0.85)
                drum("k", p + 2, 0.85)
        else:                             # muted: a long is two strokes and a rest, a short one stroke and a rest
            for j in range(2 if ln == 3 else 1):
                v = (0.95 if r == 1 else 0.88) if j == 0 else 0.8
                for tr in gtrs:
                    add(tr, p + j, 1, F1 + root, v, pm=1)
                add("bass", p + j, 1, F1 + root, v)
                drum("k", p + j, v)
    # the kit keeps common time and starts its count again with the section
    kit_from = SIZE[8][0] if i == 0 else 0            # the first nine bars: no snare or china yet, a hat in quarters
    for q in range(0, n, 4):
        if q < kit_from:
            drum("h", s0 + q, 0.45)
        else:
            drum("x", s0 + q, 0.55 if q % 16 == 0 else 0.5)
    for q in range(8, n - 9, 16):
        if q >= kit_from:
            drum("s", s0 + q, 0.95)
    for j, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):      # the nine-sixteenth bar ends in a fill
        drum(pc, s0 + n - 8 + j, 0.6 + 0.045 * j)


def quiet(i, s0, n):
    key = KEY[i]
    for p, kind, ln in LEV[5]:            # cells of 34 and 21: the chord. F minor on the long ones, D flat on the short ones
        if not s0 <= p < s0 + n:
            continue
        ch, low = ((41, 48, 56), 0) if kind == "L" else ((37, 44, 53), 8)
        exposed = REVEAL and i == 6 and p == s0 + SIZE[6][0]
        if BOWL and i == 4:
            # Ab minor to E major: one bowl on Cb/B belongs to both. The clean
            # guitar leaves it out of its long chords and rests on the short
            # ones. Damp the rim before the mallet falls so the strokes speak.
            shared = 56 + key
            assert any((x + key - shared) % 12 == 0 for x in ch)
            if kind == "L":
                add("pad", p, ln - 1, ",".join(nm(x + key) for x in ch if (x + key - shared) % 12), 0.8)
                add("rim", p, ln - 2, shared, 0.82)
            else:
                add("mallet", p, ln - 1, shared, 0.85)
        elif not exposed:
            add("pad", p, ln - 1, ",".join(nm(x + key) for x in ch), 0.8)
        # In the exposed phrase the bass gives one low F, then leaves the
        # repeated Cs to the slow harp. The ride and foot keep their parts.
        add("bass", p, SIZE[2][0] - 1 if exposed else ln - 2, F1 + key + low, 0.3)
        ROOTS.append((p, key + low))
    for p, kind, ln in LEV[3]:
        if s0 <= p < s0 + n:
            drum("k", p, 0.3)
    for q in range(0, n, 4):
        drum("rde", s0 + q, 0.4)


def steel_answer():
    # Song arithmetic, not a separate clock: 233 = 144 + (55 + 34). Wait for the first
    # 144. The chords already mark the heads; the bar comes in *after* them. On the
    # second telling the extra high answer is missing, leaving the drum fill exposed.
    start = SECS[2][0] + SIZE[8][0]
    for length in SIZE[6]:
        for offset, duration, pitch, bend, velocity in (
            (3, 9, 65, 3, .82),          # F up to Ab
            (15, 5, 75, -3, .70),        # Eb down to C
            (21, 5, 68, -3, .80),        # Ab down to F; eight sixteenths of space
            (34 + 3, 12, 72, 3, .90),    # C up to Eb, only in the long telling
        ):
            if offset + duration <= length:
                add("bar", start + offset, duration, pitch, velocity)
                T["bar"][-1]["expr_path"] = {"bend": [0, 0, bend * .2, bend * .82, bend, bend, bend]}
        start += length
    assert start == SECS[3][0]


def peel_last_riff():
    # Count down *toward* the endpoint in the riff's own sizes. For 21 sixteenths
    # the outer pair rings the big cells above the inside chug; the inside pair
    # then inherits one held chord. First the feet, then the harp, horn and fill
    # have the figure to themselves. The final low F is composed as before.
    a, b, c, d = (TOTAL - SIZE[k][0] for k in (6, 5, 4, 3))  # 55, 34, 21, 13 to go
    for tr in ('wl', 'wr', 'gl', 'gr', 'bass', 'kick', 'cym'):
        kept = []
        for note in T[tr]:
            p = round(4 * note['at'])
            if a <= p < TOTAL:
                if tr in ('wl', 'wr', 'gl', 'gr'):
                    outside = tr in ('wl', 'wr')
                    if (outside and p >= b) or (not outside and p >= c):
                        continue
                    if outside or p >= b:
                        if p not in STARTS[3]:
                            continue
                        note = {**note, 'len': round((at_size(3, p)[2] - 1) / 4, 4)}
                elif p >= (c if tr == 'cym' else d):
                    continue
            kept.append(note)
        T[tr] = kept


def compose():
    if STEEL:
        steel_answer()
    for i, (s0, kind, n) in enumerate(SECS):
        (heavy if kind == "L" else quiet)(i, s0, n)
        if BRASS and i in WIDE:
            big = [c for c in LEV[4] if s0 <= c[0] < s0 + n]
            for (p, _, ln), step in zip(big, harp_tune(5)):
                if REVEAL and i == 5 and p >= s0 + n - SIZE[5][0]:
                    continue  # these last two breaths become the next harp's phrase below
                add("brass", p, ln - 1, POOL[step] + KEY[i] + int(BRASS.split(";")[3]), float(BRASS.split(";")[2]))
            if REVEAL and i == 5:
                q = SECS[i + 1][0]
                centre, width = q + SIZE[6][0], SIZE[5][0]
                low_cells = [cell for cell in LEV[2] if q <= cell[0] < q + SECS[i + 1][2]]
                steps = harp_tune(8 - 2)
                assert len(steps) == len(low_cells)
                for (p, _, ln), step in zip(low_cells, steps):
                    if centre <= p < centre + width:
                        here = q - width + p - centre
                        assert here in STARTS[2] and at_size(2, here)[2] == ln
                        add("brass", here, ln - 1, POOL[step] + KEY[i + 1] + 12, float(BRASS.split(";")[2]))
    if LIFT:
        # what the lift is for: there the harp and the horn already spell the major triad on the new ground,
        # and the harp's last note is the home the band falls back to
        s0 = SECS[7][0]
        here = [POOL[st] for (p, _, _), st in zip([c for c in LEV[0] if c[0] >= s0], harp_tune(9)) if LIFT_SPAN[0] <= p < LIFT_SPAN[1]]
        horn = [POOL[st] for (p, _, _), st in zip([c for c in LEV[4] if c[0] >= s0], harp_tune(5)) if LIFT_SPAN[0] <= p < LIFT_SPAN[1]]
        assert {(x - POOL[0] - int(LIFT)) % 12 for x in here[:-1] + horn} == {0, 4, 7} and (here[-1] - POOL[0]) % 12 == 0
    if PEEL:
        peel_last_riff()
    for tr in ("gl", "gr", "wl", "wr"):                   # where the fifteenth line would begin: one chord
        add(tr, TOTAL, 32, ",".join(nm(F1 + j) for j in (0, 7, 12, 19)), 0.95)
    add("bass", TOTAL, 32, F1, 0.95)
    drum("k", TOTAL, 0.95)
    drum("c", TOTAL, 0.95)
    ROOTS.append((TOTAL, 0))


RULES = {"A": "A", "p": "p", "q": "q[+Br]", "B": "A", "r": "pq"}      # Apq is a long, Br a short; the short is born a step up


def harp_gen(depth, n, pool):
    return {"type": "lsystem", "axiom": "Apq", "rules": RULES, "depth": depth, "n": n, "len": "/16", "notes": " ".join(nm(x) for x in pool)}


def harp_gen_at(k, n, pool):
    """The same L-system on the cells of size k (SIZE[k] sixteenths): a long is A and its rests, a short B and its rests."""
    ln, sn = SIZE[k]
    abc = "abcdefghijklmnopqrstuvwxyz"
    lr, sr = abc[:ln - 1], abc[ln - 1:ln - 1 + sn - 1]
    rules = {"A": "A", "B": "A"}
    for c in lr[:-1]:
        rules[c] = c
    rules[lr[-1]] = lr[-1] + "[+B" + sr + "]"                     # the short cell is born a step up, as at size 0
    for j, c in enumerate(sr):
        rules[c] = lr[j] if j < len(sr) - 1 else lr[len(sr) - 1:]     # a short's rests grow into a long's
    return {"type": "lsystem", "axiom": "A" + lr, "rules": rules, "depth": 8 - k, "n": n, "len": "/16", "notes": " ".join(nm(x) for x in pool)}


def harp_tune(depth):
    """What the engine's turtle will play (for the notes and the docs): the pool step of each cell."""
    s = "Apq"
    for _ in range(depth):
        s = "".join(RULES.get(c, c) for c in s)
    pos, stack, out = 0, [], []
    for c in s:
        if c == "+":
            pos += 1
        elif c == "[":
            stack.append(pos)
        elif c == "]":
            pos = stack.pop()
        elif c.isupper():
            out.append(pos)
    return out


POOL = [53, 56, 60, 63, 65, 68, 72, 75]   # F3 Ab3 C4 Eb4 F4 Ab4 C5 Eb5 (F minor seventh, broken): step 0 sounds once, step 1 at cells 1 2 3 5 8 13 21 34


def short_children():
    """The harp's tune, on only the cells born short. No new strike times."""
    s0 = SECS[0][0]
    long_span, short_span = SIZE[6]
    end = SIZE[8][0]
    band = [cell for cell in LEV[0] if s0 <= cell[0] < s0 + end]
    steps = harp_tune(8)
    assert len(steps) == len(band) and long_span + short_span + long_span == end
    low_hits, high_hits = set(), set()
    for (p, kind, ln), step in zip(band, steps):
        if p < s0 + long_span or kind != "S":
            continue
        # First tell it on Gb in the bass register. When the ground falls to
        # F, let the same contour speak an octave higher and finish its phrase.
        low = p < s0 + long_span + short_span
        root = KEY[0] + int(at_size(6, p)[1] == "S")
        add("log", p, ln - 1, POOL[step] + root - (24 if low else 12), .88)
        if low:
            T["log"][-1]["gain"] = "-2dB"       # match the five low strikes to the bass they take
            low_hits.add(p)
        else:
            high_hits.add(p)
    take = low_hits | high_hits
    T["bass"] = [n for n in T["bass"] if round(n["at"] * 4) not in take]
    # Low, the drum takes the foot's stroke too. High, the foot returns
    # under it while the right guitar leaves it the attack instead.
    T["kick"] = [n for n in T["kick"] if round(n["at"] * 4) not in low_hits]
    T["gr"] = [n for n in T["gr"] if round(n["at"] * 4) not in high_hits]


def one_size_smaller():
    """Run the rule backwards once: a long of three is a long of two and a short
    of one; a short of two is one long. So 'stroke stroke rest' becomes 'stroke
    rest stroke'. No cell head moves, and the wall pair keeps the riff's own size.
    """
    s0, _, n = SECS[5]
    start = s0 + SIZE[8][0]               # all four guitars are back on the small riff
    follow = start + SIZE[4][0]           # 21 later the players nearest the foot go with it
    stop = start + SIZE[6][0]             # 55: the horn's five notes get the old lock
    assert stop == s0 + n - SIZE[5][0] and follow in STARTS[4]

    def at(tr, p):
        found = [e for e in T[tr] if round(e["at"] * 4) == p]
        assert len(found) == 1, (tr, p, found)
        return found[0]

    for p, kind, _ in LEV[0]:
        if not start <= p < stop or kind != "L" or RANK[p] == 2:
            continue                      # a short is one stroke at either size; a ringing cell is 2 + 1 already
        for tr in ("kick",) + (("bass", "gl", "gr") if p >= follow else ()):
            head = at(tr, p)
            if RANK[p] < 3:               # the second muted stroke crosses into the rest
                at(tr, p + 1)["at"] = round((p + 2) / 4, 4)
            elif tr == "kick":           # under a chord the walls hold: two sixteenths, then one
                drum("k", p + 2, 0.85)
            else:
                head["len"] = round(2 / 4 * 0.98, 4)
                add(tr, p + 2, 1, head["pitch"].split(",")[0], 0.85, **({} if tr == "bass" else {"pm": 1}))


def two_common_tones():
    """Ab minor and E major share two notes. First move a finger, then move the ground."""
    s, quiet_in, back = (SECS[i][0] for i in (3, 4, 5))
    first, again = s + SIZE[7][0], s + SIZE[8][0]
    cells = [c for c in LEV[5] if first <= c[0] < quiet_in]
    assert "".join(kind for _, kind, _ in cells) == "LSLSL"  # question, then question with a return
    home = F1 + KEY[3]
    first_up, last_up = [p for p, kind, _ in cells if kind == "S"]

    def tick(n):
        return round(n["at"] * 4)

    def rest(tracks, start, end):
        for tr in tracks:
            T[tr] = [n for n in T[tr] if not start <= tick(n) < end]

    def ground(p):
        return home - 4 if p >= again and at_size(5, p)[1] == "S" else home

    # The left amp plays the quiet guitarist's Ab2/Eb3 and raises just the fifth.
    # The right picks B3 during each long and lets it ring across the short.
    rest(("wl", "wr"), first, quiet_in)
    for p, kind, ln in cells:
        short = kind == "S"
        add("wl", p, ln - .4, ",".join(nm(home + i) for i in (12, 19 + int(short))), .92)
        if not short:
            middle = p + SIZE[4][0]
            add("wr", p, middle - p - .25, home + 27, .92)
            following = SIZE[4][0] if p + ln < quiet_in else 0
            add("wr", middle, p + ln + following - middle - .25, home + 27, .90)

    # On the first E the bass holds Ab. Keep its octaves but not an Eb in the
    # inside guitar chord. The second E drops into root position with the chugs.
    for tr in ("bass", "gl", "gr"):
        for n in T[tr]:
            p = tick(n)
            if not first <= p < quiet_in:
                continue
            root = ground(p)
            intervals = (0,)
            if "," in n["pitch"]:
                intervals = (0, 12) if first_up <= p < again else (0, 7, 12)
            n["pitch"] = ",".join(nm(root + i) for i in intervals)
    ROOTS[:] = sorted([(p, r) for p, r in ROOTS if not first <= p < quiet_in]
                      + [(p, ground(p) - F1) for p, _, _ in cells])
    rest(("gl", "gr"), first_up + SIZE[3][0], again)  # eight sixteenths of space for the question
    T["brass"] = [n for n in T["brass"] if tick(n) != first_up and not quiet_in - SIZE[3][0] <= tick(n) < quiet_in]
    next(n for n in T["brass"] if tick(n) == last_up)["pitch"] = nm(home + 44)  # E5 on the answer

    # The mallet strikes B3 on the short cells. The clean guitarist answers the
    # first with E3; the second becomes a broken E chord on the way home to F.
    p, _, ln = next(c for c in LEV[5] if c[0] >= quiet_in and c[1] == "S")
    delay = SIZE[0][0]
    add("pad", p + delay, ln - delay - 1, home + 20, .78)
    final, kind, ln = at_size(5, back - 1)
    assert kind == "S" and final + ln == back
    wait, carry = SIZE[1][0], SIZE[3][0]
    add("pad", final + wait, ln - wait - .5, home + 20, .78)
    rest(("wl", "wr"), back, back + carry)
    # E/B moves to F/C. Ab3 is the common note this time, carried on one string
    # through the change. Only the left of the outside pair picks on the one.
    arrival = back - SIZE[2][0]
    assert arrival == final + carry
    add("wr", arrival, back + carry - 1 - arrival, home + 24, .88)
    add("wl", back, carry - .5, ",".join(nm(F1 + i) for i in (24, 31)), .96)


def song():
    compose()
    if PIVOT:
        two_common_tones()
    if CHILD:
        short_children()
    if SMALLER:
        one_size_smaller()
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    hg, hh, h8 = HARP.split(";")
    harps = [(i, s0, 8, 144, [x + KEY[i] + (12 if i == 6 else 0) for x in POOL], hg) for i, (s0, kind, n) in enumerate(SECS) if kind == "S"]
    if h8:
        harps.append((7, SECS[7][0], 9, 233, [x + 12 for x in POOL], h8))
    tracks = [
        {"name": "gl", "patch": main.format(50), "gain": "-0.7dB", "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(51), "gain": "-0.7dB", "pan": 1, "out": "gtrs", **mids},
        {"name": "wl", "patch": "ct-wall-stop-l", "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": "ct-wall-stop-r", "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        *[{"name": f"harp{i + 1}", "patch": "em-harp", "gain": g, "pan": 0.25, "at": f"{s0 / 4:g}b", "sends": {"hall": hh},
           "gen": [harp_gen(d, n, pool)]} for i, s0, d, n, pool, g in harps],
        *([{"name": f"harp{i + 1}{'bc'[k - 1]}", "patch": "em-harp", "gain": CANON.split(";")[k - 1], "pan": (-0.3, 0.0)[k - 1],
            "at": f"{SECS[i][0] / 4:g}b", "sends": {"hall": hh},
            "gen": [harp_gen_at(k, 144, [x + KEY[i] + (12 if i == 6 else 0) - 12 * k for x in POOL])]}
           for i, k in ((4, 1), (6, 1), (6, 2))] if CANON else []),
        *([{"name": "brass", "patch": BRASS.split(";")[0], "gain": BRASS.split(";")[1], "pan": 0,
            "fx": [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*BRASS.split(";")[4].split(":"))]}]}] if BRASS else []),
        {"name": "pad", "patch": "ct-glass", "gain": PAD.split(";")[0], "pan": -0.3, "sends": {"hall": PAD.split(";")[1]}},
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
    ]
    if PIVOT:
        # Bring the already vibrating Ab3 up AFTER the amp; no second pick when the band enters.
        t = next(t for t in tracks if t["name"] == "wr")
        back = SECS[5][0]
        at = back - SIZE[2][0]
        points = [(0, 0), (at - 2, 0), (at - 1, -14), (at, -14), (back - 1, -6), (back, 0)]
        t["gain"] = {"value": t["gain"], "mod": [{"src": "auto.carry", "amount": 1}]}
        t["auto"] = {"carry": {"points": [[f"{p / 4:g}b", v] for p, v in points], "curve": 0}}
    if STEEL:
        tracks.append({"name": "bar", "patch": "em-steel", "gain": STEEL, "pan": 0.12,
                       "fx": [{"type": "eq", "bands": ["hp cutoff=440 q=0.707", "peak cutoff=1650 q=0.8 gain=3.5dB"]}]})
    if BOWL:
        rim, mallet = BOWL.split(";")
        room = " fx.0.mix=0.1 fx.0.decay=1s"
        tracks.extend([
            {"name": "rim", "patch": "singing-bowl-rim synth.amp.r=200ms" + room, "gain": rim + "dB", "pan": 0},
            {"name": "mallet", "patch": "singing-bowl synth.amp.d=2.6s synth.amp.r=200ms" + room, "gain": mallet + "dB", "pan": 0},
        ])
    if REVEAL:
        # Keep the turtles running. Damp the faster strings to expose their
        # slow relative: 144 = 34 + 21 + 34 + 21 + 34 sixteenths.
        span = SECS[6][2]
        for name, margin in (("harp7", SIZE[5][0]), ("harp7b", SIZE[6][0])):
            t = next(tr for tr in tracks if tr["name"] == name)
            # Automation on these offset tracks counts from the harp's first
            # pluck, not from beat zero of the song.
            lo, hi = margin, span - margin
            pts = [["0b", 0], [f"{(lo - 2) / 4:.8g}b", 0], [f"{lo / 4:.8g}b", -60],
                   [f"{(hi - .25) / 4:.8g}b", -60], [f"{hi / 4:.8g}b", 0]]
            t["gain"] = {"value": t["gain"], "mod": [{"src": "auto.damp", "amount": 1}]}
            t["auto"] = {"damp": {"points": pts, "curve": 0}}
    if CHILD:
        tracks.append({"name": "log", "patch": "log-drum play.glide=0ms play.gate=1 synth.env.p.d=35ms synth.amp.r=45ms",
                       "gain": CHILD, "pan": .4, "out": "drums"})
    for t in tracks:
        if "gen" not in t:
            t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])

    def key_f(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", ROOTS[0][1]]], ROOTS[0][1]
    for p, r in ROOTS[1:]:
        if r != prev:
            pts += [[f"{p / 4 - 0.02:g}b", prev], [f"{p / 4:g}b", r]]
            prev = r
    qpts = [["0b", 0]]
    for s0, kind, n in SECS:
        if kind == "S":
            qpts += [[f"{s0 / 4 - 0.02:g}b", 0], [f"{s0 / 4:g}b", float(QBASS)], [f"{(s0 + n) / 4 - 0.02:g}b", float(QBASS)], [f"{(s0 + n) / 4:g}b", 0]]
    return {
        "about": ("chirpers X (Common Time), track 7 by chirper-zero: Extreme and Mean. Two cells, a long of three sixteenths and a short "
                  "of two, and one rule: a long becomes a long and a short, a short becomes a long. The pattern it makes never loops and "
                  "is the same at every size, so the band plays it at many sizes at once: muted strokes, open notes, chords, crashes, "
                  "the root, and the song's own sections (long ones heavy, short ones quiet). The kit keeps common time against it. In "
                  "the quiet sections a wire harp has no notes, only the rule (the engine's L-system). The slow song: 80. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{(TOTAL + 32) / 4:g}b", "event_stable": True,
        "patches": {
            **({"em-steel": {
                "extends": "pedal-steel synth.amp.a=75ms synth.amp.r=140ms fx.0.mix=0.08 fx.1.mix=0 fx.2.mix=0 play.glide=0ms",
                "about": "The moving bar against the two fretted guitars. Keep the pedal steel's vibrato, bend by hand within each note, and damp it before the band answers.",
                "synth": {"pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": 0.06}, {"src": "expr.bend", "amount": 1}]}},
            }} if STEEL else {}),
            "ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
            "em-harp": {"about": ("Extreme and Mean's wire harp (chirper-zero, 17 Nov): the library's ks-harp (Karplus-Strong, stretch 3) with a "
                                  "release long enough for a sixteenth-long pluck to ring on."),
                        "gain": "-5dB",
                        "synth": {"amp": {"a": "1ms", "d": 0, "s": 1, "r": "2.5s"},
                                  "layers": [{"type": "ks", "bright": 0.8, "decay": "5s", "ks": {"blend": 1, "stretch": 3}}]}},
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
            "low": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                    {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]},
                           {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.quiet", "amount": 1}]}}],
                    "auto": {"key": {"points": pts, "curve": 0}, "quiet": {"points": qpts, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T7_MASTER", "2.7dB")}]},
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
    if os.environ.get("C10T7_SHOW"):
        sec = 15 / BPM
        for i, (s0, kind, n) in enumerate(SECS):
            print(f"section {i + 1} {kind} {'heavy' if kind == 'L' else 'quiet'}  sixteenths {s0}-{s0 + n}  bars {s0 / 16 + 1:.2f}-{(s0 + n) / 16 + 1:.2f}  "
                  f"{int(s0 * sec) // 60}:{s0 * sec % 60:04.1f}-{int((s0 + n) * sec) // 60}:{(s0 + n) * sec % 60:04.1f}  key +{KEY[i]}")
        print("the first 34 cells:", "".join(c[1] for c in LEV[0][:34]))
        print("their sizes:       ", "".join(str(min(RANK[c[0]], 9)) for c in LEV[0][:34]))
        print("the harp's steps:  ", "".join(str(x) for x in harp_tune(8)))
    else:
        open(OUT, "w").write(dump(song()))
