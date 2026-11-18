#!/usr/bin/env python3
"""chirpers10-t8 "Common Measure" (chirper-zero): two riffs of different lengths, argued down to what they share.

Euclid finds the greatest common measure of two lengths by taking the less from the greater, again and again: what is
left over is set against the shorter one, and what that leaves against the leftover, until something goes in exactly.
That last length measures both. This piece is the algorithm played by two guitars, and it is the record's fast song
(160 where the other seven run 80 to 138).

The left guitar has a riff of 52 sixteenths (A); the right has one of 32 (B, two bars). Played together they meet
again only after 26 bars. Then, each section, the longer riff is cut down to WHAT WAS LEFT OVER: its own tail.

  the two given     bars 0-8      B alone on the right: the short riff, twice bare and twice with the band
  52 against 32     bars 8-34     A on the left, B on the right: one whole cycle, 26 bars
  20 against 32     bars 34-54    the left keeps only A's last 20 sixteenths (52 - 32): they meet every 10 bars
  20 against 12     bars 54-69    the right keeps only B's last 12 (32 - 20): every 3 bars and three quarters
  8 against 12      bars 69-81    the left keeps its last 8 (20 - 12): every bar and a half
  8 against 4       bars 81-89    the right keeps its last 4 (12 - 8): every half bar. Four goes into eight: it is found
  the measure       bars 89-105   both guitars, and two more, on the four sixteenths both riffs END with: one beat. The
                                  beat is the common measure; the cell climbs the record's hook notes as chords
  measured          bars 105-126  now the two riffs can be said together: all four guitars play A four times, then B
                                  four times, in unison, the kit's four in a bar under them (A is thirteen beats, B eight)
  one chord         bar 126

The bass and the kick go with the SHORTER riff of each pair (the one doing the measuring), so the rhythm section's
cycle shrinks section by section: two bars, a bar and a quarter, three beats, half a bar, a beat. WHAT IS LEFT OVER
IS HEARD ALONE: at the end of each pair the band stops and the longer riff plays its tail by itself (20 sixteenths,
then 12, 8, 4: the breaks shrink too), and that tail is the next section's riff. The kit keeps common time
throughout, its feel changing with each cut, and crashes wherever the two riffs meet, so the crashes come closer and
closer: 39 seconds apart, then 15, 5.6, 2.25, and at last the china on every beat. THE ARGUMENT NARROWS: each riff is
two takes a side until 8 against 12, where it is one; at 8 against 4 the bass and the kick drop out (the kick comes
back half way) and the snare counts every beat, louder and louder; two beats of nothing; then the measure, with every
guitar there is.

Track 7 (Extreme and Mean) is the cut that has no common measure, slow, never looping. This is its pair: the two
lengths here do have one, and the song is the finding of it. 52 and 32 are four times 13 and 8, so the algorithm takes
as long as it can (every quotient is one) and ends on four sixteenths: the beat of common time, where the record began.

v1 is the SKELETON (Harry, 17 Nov about 03:40: "open up 2 new song slots"; track 2's terms: mine, my title, a
skeleton first): the whole shape standing, bare.
"""
import json
import os

OUT = os.environ.get("C10T8_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t8.yaml"))
BPM = 160
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}
# v2, THE TWO BELLS: each riff has a bell that rings where the riff begins again, the left riff's low and on the left, the
# right riff's a fourth higher and on the right. As the riffs are cut down the bells come faster and closer, and at the
# measure they ring together on every beat. gain, dB ; velocity ; velocity in the measure ; the low bell's dB over the
# high one's (it reads 2.4 dB quieter at the same gain). "" = v1 (no bells).
BELLS = os.environ.get("C10T8_BELLS", "-12;0.9;0.95;1.5")
# v3, WHAT WAS CUT AWAY COMES BACK: the long riff's head (the hook coming down: E flat, C, B, A flat, G flat, F) was the
# first thing the algorithm cut off, at 0:51. At the measure a lead guitar plays it again, each note held for two
# bars over the cell that measures it, against the chords climbing the same notes the other way. Then the F again and
# the F above. patch ; gain ; hall send ; semitones over the low F. "" = v2 (no lead).
HEAD = os.environ.get("C10T8_HEAD", "lead-monster;-12dB;-12dB;36")
# v4: in the one-guitar-per-side pair, the right riff's three rising notes are
# stretched to the distance between joint landings, then gathered back to tempo.
# Empty switches the section off, giving v3 exactly. This part is dry: let the
# bare last tail belong to the guitars.
BREATH = os.environ.get("C10T8_BREATH", "shaper-reed;-13dB")
# v5: the bass takes the measuring riff; the guitars answer with what's left.
BASS_BREAK = os.environ.get("C10T8_BASS_BREAK", "1")
# v6: the kit learns B's surviving tail in the measured coda. Empty = v5.
STICKS = os.environ.get("C10T8_STICKS", "1")


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# o an open low root, c a muted stroke, r a rest, - a held place, a number a hook note (semitones over the root)
A = ("10 - - 7 - - 6 - 3 - - 1 - - o - "          # the hook coming down in threes and twos
     "c c r c c r c r o c c r 7 - 6 - "
     "o c c 3 - c o c c 10 - c "                   # (its last 20 begin here)
     "6 - c c o - c c").split()                    # (its last 8)
B = ("o r c c r c c r o r c c r 1 - r "
     "o c c r "
     "3 - - 6 - - 7 - "                            # (its last 12 begin here)
     "o - c c").split()                            # (its last 4: the measure)
assert len(A) == 52 and len(B) == 32 and A[-4:] == B[-4:]
G = B[-4:]

# the algorithm: (left riff, right riff); the shorter of each pair carries the bass and the kick
PAIRS = []
_l, _r = A, B
while len(_l) != len(_r):
    PAIRS.append((_l, _r))
    if len(_l) > len(_r):
        _l = _l[-(len(_l) - len(_r)):] if len(_l) - len(_r) > 0 else _l
    else:
        _r = _r[-(len(_r) - len(_l)):]
assert [(len(a), len(b)) for a, b in PAIRS] == [(52, 32), (20, 32), (20, 12), (8, 12), (8, 4)] and _l[-4:] == G and _r == G
REPS = [1, 2, 4, 8, 16]                   # how many times each pair runs its whole cycle
INTRO = 8 * 16
HOOK = [0, 3, 6, 1, 7, 10, 0, 0]          # the measure's roots, two bars each: the record's hook notes in their order


def lcm(a, b):
    x, y = a, b
    while y:
        x, y = y, x % y
    return a * b // x


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece == "h" else 0.25,
                                 "pitch": piece, "vel": round(vel, 3)})


def say(riff, t, gtrs, low=False, root=0, chord=False, stop=None, bass=True):
    """One statement of a riff from sixteenth t (cut at `stop`), on the guitars `gtrs`; with the kick, and the bass
    unless `bass` is off, if `low`."""
    for i, k in enumerate(riff):
        if k in "r-" or (stop is not None and t + i >= stop):
            continue
        n = 1
        while i + n < len(riff) and riff[i + n] == "-":
            n += 1
        at = t + i
        if k == "c":
            for tr in gtrs:
                add(tr, at, 1, F1 + root, 0.88, pm=1)
            if low:
                if bass:
                    add("bass", at, 1, F1 + root, 0.88)
                drum("k", at, 0.88)
        else:
            semi = 0 if k == "o" else int(k)
            pitch = ",".join(nm(F1 + root + j) for j in (0, 7, 12)) if chord and k == "o" else F1 + root + semi
            for tr in gtrs:
                add(tr, at, n, pitch, 1.0 if k == "o" else 0.95)
            if low:
                if bass:
                    add("bass", at, n, F1 + root + semi, 0.95)
                drum("k", at, 0.95)


def beat(s0, s1, cym="h", step=2, vel=0.5, snare=(4, 12)):
    for q in range(s0, s1, step):
        drum(cym, q, vel + (0.05 if (q - s0) % 16 == 0 else 0))
    for q in range(s0, s1, 16):
        for b in snare:
            if q + b < s1:
                drum("s", q + b, 0.95)


def fill(s):
    """The last half bar before sixteenth s."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, s - 8 + i, 0.6 + 0.045 * i)


ALL = ("gl", "gr", "dl", "dr", "wl", "wr")
def bell(side, s16, root=0, vel=None):
    if BELLS:
        add("bell-" + side, s16, 1, F1 + root + (55 if side == "l" else 60), float(BELLS.split(";")[1]) if vel is None else vel)


MARKS = [("the two given", 0)]            # (name, first sixteenth)
ROOTS = [(0, 0)]


def bass_break(start, stop, short, long, short_side, long_side):
    """The shorter riff is already in the bass and foot. Give it the stage.

    Leave the longer guitar only the remainder at the end of each cycle, in
    its original place. Its last exposed tail, beyond stop, is untouched.
    """
    def keep(track, p):
        if not start <= p < stop:
            return True
        return track in long_side and (p - start) % len(long) >= len(short)

    for tr in short_side + long_side:
        T[tr] = [n for n in T[tr] if keep(tr, round(n['at'] * 4))]
    pop_tail(start, stop, short)


def pop_tail(start, stop, riff):
    # Thumb the low F; take only the changing, pitched notes up one string octave.
    # Same attacks and rests, so the kick and the picking hand keep their pattern.
    for note in T['bass']:
        p = round(note['at'] * 4)
        if start <= p < stop:
            token = riff[(p - start) % len(riff)]
            if token.isdigit():
                note['pitch'] = nm(F1 + 12 + int(token))


def measured_drums(start, stop):
    """Four statements of B: keep time, play its tail, anticipate it, land it."""
    tail = PAIRS[2][1]  # the twelve B still had after 32 minus 20
    assert B[-len(tail):] == tail and tail[-len(G):] == G
    notes = [i for i, token in enumerate(tail) if token.isdigit()]
    shells = ("ft", "t2", "t1")
    assert len(notes) == len(shells)
    first_b = stop - 4 * len(B)
    beat(start, first_b, cym="x", step=4, vel=.5)
    # Quote the kit's first two bars: only the hat counts quarters. B is
    # now in all the guitars instead of one, so the opening returns changed.
    beat(first_b, first_b + len(B), cym="h", step=4, vel=.45, snare=())
    T["kick"] = [n for n in T["kick"] if not first_b <= round(n["at"] * 4) < first_b + len(B)]
    T["cym"] = [n for n in T["cym"] if not (n["pitch"] == "c" and round(n["at"] * 4) == first_b)]
    for rep in (1, 2, 3):
        base = first_b + rep * len(B)
        tail_at = base + len(B) - len(tail)
        lead = len(tail) - len(G) if rep == 2 else 0
        phrase = tail_at - lead
        # No continuous backbeat under the shell phrase. In the third B, a
        # short closed hat in the head leaves air around the coming bass solo.
        beat(base, phrase, cym="h" if rep == 2 else "x", step=4, vel=.5)
        velocities = {1: (.78, .85, .92), 2: (.66, .74, .83), 3: (.87, .93, .99)}[rep]
        for i, piece, v in zip(notes, shells, velocities):
            drum(piece, phrase + i, v)
        common = base + len(B) - len(G)
        if rep == 2:
            # After the drummer's early answer, leave the three popped notes
            # to the bassist. Foot comes back for the shared one-beat cell.
            if BASS_BREAK:
                T["kick"] = [n for n in T["kick"] if not tail_at <= round(n["at"] * 4) < common]
        elif rep == 1:
            drum("s", common, .92)
        else:
            # Replace the stock eight-stroke fill with the actual o - c c.
            drum("ft", common, .92)
            drum("s", common, .92)
            for i, token in enumerate(G):
                if token == "c":
                    drum("s", common + i, .70 if i == len(G) - 2 else .89)


def compose():
    # the two given: B alone on the right, twice bare (a hat in quarters) and twice with the band
    for i in range(4):
        say(B, i * 32, ("gr", "dr") if i >= 2 else ("gr",), low=i >= 2)
        bell("r", i * 32)
    beat(0, 64, cym="h", step=4, vel=0.45, snare=())
    beat(64, INTRO)
    t = INTRO
    for (left, right), reps in zip(PAIRS, REPS):
        a, b = len(left), len(right)
        cyc = lcm(a, b)
        n = cyc * reps
        MARKS.append((f"{a} against {b}", t))
        k = PAIRS.index((left, right))
        last = k == len(PAIRS) - 1
        # WHAT IS LEFT OVER IS HEARD ALONE: for the last |a - b| sixteenths of a pair the longer riff plays its tail by
        # itself (that tail is the next section's riff). The last pair leaves nothing over: two beats of silence instead
        stop = t + n - (8 if last else abs(a - b))
        # THE ARGUMENT NARROWS: the last two pairs are one guitar a side, and the last has no bass; the measure gets everything
        gl, gr = (("gl", "dl"), ("gr", "dr")) if k < 3 else (("gl",), ("gr",))
        kick_from = t + n // 2 if last else t          # the last pair: the guitars alone for its first half, then the kick

        def grow(q, t=t, stop=stop):                   # in the last pair the bells grow with the snare (0.5 to 0.9)
            return 0.5 + 0.4 * (q - t) / (stop - t)
        for i in range(n // a):
            say(left, t + i * a, gl, low=a < b and t + i * a >= kick_from, stop=stop if last or a < b else None, bass=not last)
            if not (last or a < b) or t + i * a < stop:
                bell("l", t + i * a, vel=grow(t + i * a) if last else None)
        for i in range(n // b):
            # In v4 the right guitarist lets the reed take the three pitched
            # attacks. His four-place tail and bell still give the riff its
            # full twelve places. First one of every two statements answers,
            # then he waits; at landing six the pitches meet in octaves.
            leave_head = BREATH and k == 3 and i*b < 5*cyc and (i % 2 == 0 or i*b >= 3*cyc)
            played = ["r" if token.isdigit() else token for token in right] if leave_head else right
            say(played, t + i * b, gr, low=b < a and t + i * b >= kick_from, stop=stop if last or b < a else None, bass=not last)
            if not (last or b < a) or t + i * b < stop:
                bell("r", t + i * b, vel=grow(t + i * b) if last else None)
        if BASS_BREAK and k in (1, 2):
            # On the second half of each pair the measuring hand switches side:
            # A's twenty places against B's twelve-place answer, then the reverse
            # subtraction with twelve in the bass and eight in the answer.
            args = (left, right, gl, gr) if a < b else (right, left, gr, gl)
            bass_break(t + n // 2, stop, *args)
        if k == 0:
            fill(t)
        drum("c", t, 0.9)
        for i in range(1, reps):                       # a crash wherever the two riffs meet again
            if cyc >= 24:
                drum("c", t + i * cyc, 0.75 if cyc >= 60 else 0.65)
        # the kit keeps common time, and its feel changes with each cut
        if k == 0:
            beat(t, stop)                                              # a hat in eighths, the snare on two and four
        elif k == 1:
            beat(t, stop, cym="x", step=4)                             # the china in quarters
        elif k == 2:
            beat(t, stop, cym="x", step=4, snare=(8,))                 # half time: the snare on three
        elif k == 3:
            beat(t, stop)                                              # the hat again, the backbeat back
            if BREATH:
                # Right begins Ab-- B-- C-. Give each note first a whole
                # landing (24 sixteenths), then three times and twice its
                # written length, then let the reed meet the actual guitar.
                heads = [(i, int(token)) for i, token in enumerate(right) if token.isdigit()]
                assert [i for i, _ in heads] == [0, 3, 6]
                for j, (_, pitch) in enumerate(heads):
                    add("breath", t + j * cyc, cyc - 2, F1 + 36 + pitch, 0.79 + 0.035 * j)
                for h, stretch in ((3, 3), (4, 2), (5, 1)):
                    for j, (i, pitch) in enumerate(heads):
                        # The two quicker answers overblow an octave; come
                        # back down when both play the three pitches together.
                        add("breath", t + h * cyc + i * stretch, (3 if j < 2 else 2) * stretch - 0.3,
                            F1 + (48 if stretch > 1 else 36) + pitch, 0.86 + 0.035 * j)
                # Answer down on F, then let the last two meetings and the
                # right riff's exposed tail go by without the reed.
                add("breath", t + 5 * cyc + 8, cyc - 10, F1 + 36, 0.84)
        else:
            beat(t, stop, snare=())                                    # the snare on every beat, growing
            beats = list(range(t, stop, 4))
            for j, q in enumerate(beats):
                drum("s", q, 0.45 + 0.55 * j / (len(beats) - 1))
        t += n
    # the measure: every guitar on the four sixteenths both riffs end with; the cell climbs the hook notes as chords
    MARKS.append(("the measure", t))
    drum("c", t, 0.95)
    for j, root in enumerate(HOOK):
        ROOTS.append((t + j * 32, root))
        for i in range(8):
            say(G, t + j * 32 + i * 4, ALL, low=True, root=root, chord=True)
            for side in "lr":
                bell(side, t + j * 32 + i * 4, root, float(BELLS.split(";")[2]) if BELLS else 0)
        if j:
            drum("c", t + j * 32, 0.7)
        if HEAD:
            head = [int(k) if k.isdigit() else 0 for k in A[:16] if k not in "-rc"] + [0, 12]
            add("lead", t + j * 32, 32, F1 + int(HEAD.split(";")[3]) + head[j], 0.9)
    beat(t, t + 256, cym="x", step=4, vel=0.5)
    t += 256
    # measured: the two riffs said together, in unison, the beat under them
    MARKS.append(("measured", t))
    fill(t)
    drum("c", t, 0.95)
    s = t
    for j, riff in enumerate((A, A, A, A, B, B, B, B)):
        # Once on each complete riff, hand its tail back to the bass soloist.
        # The last B reunites everybody; the low F at the end is unchanged.
        recall = A[-20:] if j == 3 else B[-12:] if j == 6 else []
        if BASS_BREAK and recall:
            split = len(riff) - len(recall)
            say(riff[:split], s, ALL, low=True)
            say(recall, s + split, (), low=True)
            pop_tail(s + split, s + len(riff), recall)
        else:
            say(riff, s, ALL, low=True)
        bell("l", s)
        bell("r", s)
        if s > t:
            drum("c", s, 0.7)
        s += len(riff)
    if STICKS:
        measured_drums(t, s)
    else:
        beat(t, s, cym="x", step=4, vel=0.5)
        fill(s)
    MARKS.append(("one chord", s))
    for tr in ALL:
        add(tr, s, 32, ",".join(nm(F1 + j) for j in (0, 7, 12, 19)), 0.95)
    add("bass", s, 32, F1, 0.95)
    drum("k", s, 0.95)
    drum("c", s, 0.95)
    bell("l", s)
    bell("r", s)
    ROOTS.append((t, 0))
    return s + 32


def song():
    total = compose()
    assert total % 16 == 0 and all(m[1] % 16 == 0 for m in MARKS)
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"            # each riff is two takes: a second through another amp, microphone and cone
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    tracks = [
        {"name": "gl", "patch": main.format(60), "gain": os.environ.get("C10T8_MAIN", "0.7dB"), "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(61), "gain": os.environ.get("C10T8_MAIN", "0.7dB"), "pan": 1, "out": "gtrs", **mids},
        {"name": "dl", "patch": dbl.format(62), "gain": os.environ.get("C10T8_DBL", "-2.5dB"), "pan": -0.75, "out": "gtrs", **mids},
        {"name": "dr", "patch": dbl.format(63), "gain": os.environ.get("C10T8_DBL", "-2.5dB"), "pan": 0.75, "out": "gtrs", **mids},
        {"name": "wl", "patch": "ct-wall-stop-l", "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": "ct-wall-stop-r", "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        *([{"name": "bell-" + side, "patch": "cm-bell", "gain": f"{float(BELLS.split(';')[0]) + (float(BELLS.split(';')[3]) if side == 'l' else 0):g}dB", "pan": pan}
           for side, pan in (("l", -0.6), ("r", 0.6))] if BELLS else []),
        *([{"name": "lead", "patch": HEAD.split(";")[0], "gain": HEAD.split(";")[1], "pan": 0, "sends": {"hall": HEAD.split(";")[2]}}] if HEAD else []),
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
    ]
    if BREATH:
        timbre, gain = BREATH.split(";")
        tracks.append({"name": "breath", "patch": timbre, "gain": gain, "pan": 0.12})
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])

    def key_f(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", 0]], 0
    for p, r in ROOTS[1:]:
        if r != prev:
            pts += [[f"{p / 4 - 0.02:g}b", prev], [f"{p / 4:g}b", r]]
            prev = r
    return {
        "about": ("chirpers X (Common Time), track 8 by chirper-zero: Common Measure. Two riffs of different lengths, 52 sixteenths on the "
                  "left guitar and 32 on the right, and Euclid's way of finding what measures both: take the less from the greater. "
                  "Each section the longer riff is cut down to what was left over, its own tail: 52 against 32, 20 against 32, 20 "
                  "against 12, 8 against 12, 8 against 4. Four goes into eight: the measure is one beat, the four sixteenths both "
                  "riffs end with, and then the two riffs are played whole, together. The fast song: 160. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{total // 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    **({"cm-bell": {
                        "about": ("Common Measure's bell (chirper-zero, 17 Nov): the library's agogo bell (afro-perc's `ah`: three partials at 1, "
                                  "2.4 and 3.9 and a 4 ms click) as a patch that takes a pitch, so the two bells can sit on the song's fifth "
                                  "and root and follow the chords."),
                        "synth": {"amp": {"a": "0.2ms", "curve": 3, "d": "240ms", "r": "30ms", "s": 0},
                                  "env": {"h": {"a": "0.2ms", "d": "4ms", "s": 0}},
                                  "layers": [{"type": "additive", "damp": 0.3, "partials": [[1, 1], [2.4, 0.4], [3.9, 0.15]]},
                                             {"type": "noise", "level": {"value": "-60dB", "mod": [{"src": "env.h", "amount": 40}]}}]}}} if BELLS else {})},
        "buses": {
            **({"hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]}} if HEAD else {}),
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
                           {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]}],
                    "auto": {"key": {"points": pts, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T8_MASTER", "2.7dB")}]},
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
    if os.environ.get("C10T8_SHOW"):
        end = compose()
        sec = 15 / BPM
        for (name, s0), (_, s1) in zip(MARKS, MARKS[1:] + [("", end)]):
            print(f"{name:16s} bars {s0 // 16 + 1:3d}-{s1 // 16 + 1:3d}  {int(s0 * sec) // 60}:{s0 * sec % 60:04.1f}-{int(s1 * sec) // 60}:{s1 * sec % 60:04.1f}")
    else:
        open(OUT, "w").write(dump(song()))
