#!/usr/bin/env python3
"""chirpers9-t6 (chirper-one): "Spring Tide" - track 6 of Accretion (chirpers9), tidal forces.

Closer in, the disk's matter is stretched and squeezed at once: the side nearer the centre pulls ahead, the far side
lags. This track is that, as counterpoint: E1 (t1's seed) runs in TWO layers that move in opposite directions in
time. The far side (a cello, low) starts augmented x3.2 - each of E1's notes a long bowed tone - and is squeezed a
little faster every sixteen bars; the near side (a marimba, high) starts squeezed x4 - E1 as a quarter-second trill,
just as t5 throws it across the seam - and is stretched a little slower every sixteen bars. They meet at the same
speed, in octaves, on one downbeat (bar 65): the crest, where the harmony opens into t4's four lights (E4), one
chord per E1 cycle. Then they cross and keep going - the near side slowing to a crawl, the far side racing into a
blur - and that tearing carries into t7, the storm.

E6 (this track's element, motifs.md): THE TIDE - two chords a semitone apart, D major 9 #11 and E-flat major 7 #11,
alternating in an 8-beat cycle whose split moves like a tide (4+4, 5+3, 6+2 ... 3+5, 2+6): augmentation against
diminution as harmony. A harmonium breathes it; a 303 plays E2 (t2's cell of seven) on its roots.
Also carried: E5 (t5's inner orbit, its 3-beat ostinato, received stretched x2 and squeezed back), E2 as the kit's
cell (kick, rim, snare in seven sixteenths, re-barred into eight - locked - at the crest).

Form (bars): in 16 (flat 120, the seam from t5) / pull 16 / tide 16 / squeeze 16 / crest 16 / cross 16 / surge 16 /
torn 16 / out 16 (flat 132, the seam into t7) = 144 bars; the tempo ramps 120 -> 132 between the seams.
Emits songs/chirpers9-t6.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, math, os, random, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers9-t6.yaml")
SEED = 20261106
HERE = os.path.dirname(os.path.abspath(__file__))

KEY = 38                                    # D2: D, with E5's G# (Lydian) - the hot inner disk
FORM = [('in', 16), ('pull', 16), ('tide', 16), ('squeeze', 16), ('crest', 16), ('cross', 16), ('surge', 16),
        ('torn', 16), ('out', 16)]
SEC = {}
_acc = 0
for _n, _k in FORM:
    SEC[_n] = _acc; _acc += _k
NBARS = _acc
CREST = SEC['crest']

# E1 (chirper-zero): D A C G E in 5/4 - (semitones above D, beats; None = rest)
E1 = [(0, 0.5), (7, 0.75), (10, 0.25), (5, 1.0), (2, 1.5), (None, 1.0)]
# (v5, Harry 6 Nov: 'tone is home') E1 in t6 is LYDIAN, the inner disk's heat: its C and G raised to C# and G# (D A C#
# G# E), so it sits inside the tide's chords and E5's G# instead of rubbing against them; E1's own C and G come back
# only in the out-seam, over B-flat, where they are consonant again (the seed cooling as it crosses into t7)
E1L = [(0, 0.5), (7, 0.75), (11, 0.25), (6, 1.0), (2, 1.5), (None, 1.0)]
# (v6) the album settled on D MIXOLYDIAN (E1's own scale: E5 v2, E3 v2, E4 v2, t5, t7): E1 is back in its own form
# everywhere in t6 - D A C G E, the hook plainly - and the Lydian spelling above is retired
E1L = E1
# E2 (t2): seven sixteenths, hits 0 2 3 5, pitches D A F C (here re-pitched on the tide's roots)
E2_STEPS = [0, 2, 3, 5]
E2_PITCH = {0: 0, 2: 7, 3: 4, 5: -2}          # (v6) D A F# C: the cell in D Mixolydian
E2_ON = {0: E2_PITCH, -2: {0: 0, 2: 7, 3: 4, 5: 2}, -4: {0: 0, 2: 7, 3: 4, 5: 2}}   # on C: C G E D; on Bb: Bb F D C
E2_ON[-7] = {0: 0, 2: 7, 3: 4, 5: 2}                      # (v21) on G: G D B A
# E5 (chirper-zero): A G# A . E . A G# A . D . - a 3-beat ostinato (sixteenths; None = rest), MIDI pitches
E5 = [69, 67, 69, None, 76, None, 69, 67, 69, None, 74, None]     # (v6) E5 v2: the G# became G (chirper-zero, 6 Nov)
# E4 (chirper-three): four lights, one chord per E1 cycle: D9, Bbmaj13#11, Am11, D9sus (MIDI voicings)
# (v5) re-harmonised into D Lydian, the same rhythm (one chord per E1 cycle): Dmaj9 | E/D | Bm9 | A(add9)
E4 = [[50, 54, 57, 60, 64], [48, 52, 55, 59, 62], [57, 60, 64, 67, 71, 74], [55, 59, 62, 64, 69]]   # (v6) E4 v2: D9 | Cmaj9 | Am11 | G6/9
# E6: the tide - X = Dmaj9#11, Y = Ebmaj7#11 (semitones above KEY + 12)
# (v5) E6 v2: the tide is now I and II of D Lydian - Dmaj9 and E over a D pedal (no semitone clash); in the out-seam
# Y becomes B-flat (D in common), the V of t7's E-flat, and the tide ebbs out onto it
TIDE_X = (0, [0, 4, 7, 14, 16])   # (v6) D(add9): D F# A E F#
TIDE_Y = (-2, [0, 4, 7, 14])      # (v6) E6 v3: C(add9) over the D pedal - I and bVII of D Mixolydian (C E G D)
TIDE_Z = (-4, [0, 4, 7, 14])
# (v21, whole song) THE TIDE LEARNS ITS THIRD CHORD: for three minutes the tide rocked between two chords, D and C.
# Now every fourth swing (the last two bars of each eight) it reaches G instead of C - G(add9) over its D, the IV of
# D Mixolydian: I - bVII, I - bVII, I - bVII, I - IV, the album's mode heard as a cadence, so the phrase has an end
# and the pull, the tide, the cross and the surge sound like verses of a song, not a loop (not in the in-seam, the
# squeeze's one-beat swings or the out-seam's ebb)
TIDE_W = (-7, [0, 4, 7, 14])      # G(add9): G B D A, its D the tide's own
W_SECS = ('pull', 'tide', 'cross', 'surge')
# (v5) THE LIFT: the crest goes up a whole tone, into E - the four lights, both E1 layers meeting, the hook, E5 and
# the 303 all lifted - the payoff as a key change; the tear's look back at the crest stays home in D
LIFT = {'crest': 2}
# X's share of each 8-beat cycle, per section (the tide moving)
# (v9, section w1: the in-seam was static) THE TIDE COMES IN: the head starts on D alone (8+0), the D9 world of t5's
# tail, and the C creeps in a beat at a time (7+1, 6+2, 5+3) to the even 4+4 by bar 16 - the tide visibly arriving
SPLIT = {'in': [8, 7, 7, 6, 6, 5, 5, 4], 'pull': [5, 5, 6, 6], 'tide': [6, 5, 4, 3, 2, 3, 4, 5], 'squeeze': [7, 1, 7, 1, 6, 2, 6, 2],
         'cross': [3, 3, 2, 2], 'surge': [5, 3, 5, 3], 'torn': [1, 1, 1, 1], 'out': [4, 3, 2, 1, 0, 0, 0, 0]}
# the two E1 layers' speed factors per section (1 = E1's own 5 beats)
FAR = {'pull': 3.2, 'tide': 2.4, 'squeeze': 1.6, 'crest': 1.0, 'cross': 0.8, 'surge': 0.5, 'torn': 0.2, 'out': 0.2}
NEAR = {'in': 0.25, 'pull': 0.4, 'tide': 0.6, 'squeeze': 0.8, 'crest': 1.0, 'cross': 1.6, 'surge': 2.0, 'torn': 3.2, 'out': 6.4}
# (v7, section w7: the surge was static, little new vs the cross) THE SURGE IS A MENSURATION CANON: the far side at
# x0.5, the hook at x1 and the near side at x2 - E1 at three speeds at once, the clean ratios of the squeeze and the
# stretch, all starting on bar 97's downbeat and coming back together every 10 beats (every 5 bars on a bar line)


def line(events, total):
    ev = sorted(events, key=lambda e: e[0])
    toks, t = [], 0.0
    for k, (at, p, d, v) in enumerate(ev):
        if at < t - 1e-6: continue
        if at > t + 1e-4: toks.append(f"R/{at - t:.4f}b")
        nxt = ev[k + 1][0] if k + 1 < len(ev) else total
        d = max(0.02, min(d, nxt - at))
        base, _, attr = p.partition('^')
        toks.append(f"{base}/{d:.4f}b@{max(1, min(127, int(v)))}" + (f"^{attr}" if attr else "")); t = at + d
    if total > t + 1e-4: toks.append(f"R/{total - t:.4f}b")
    return ' '.join(toks)


def m(n): return f"m{n:.3f}"


def sec_of(bar):
    for nm_, n_ in FORM:
        if SEC[nm_] <= bar < SEC[nm_] + n_:
            return nm_, bar - SEC[nm_]
    return FORM[-1][0], bar - SEC[FORM[-1][0]]


def build():
    rng = random.Random(SEED)
    total = NBARS * 4.0
    P = {k: [] for k in ('far', 'near', 'tide', 'acid', 'e5', 'kit', 'hats', 'lights', 'sub', 'farbass', 'e5b', 'hook', 'root')}

    # ---- E1 in two layers moving in opposite directions in time; each section restarts the cell on its downbeat ----
    def e1_layer(key, speeds, octave, vel0):
        for nm_, f in speeds.items():
            t0, t1 = SEC[nm_] * 4.0, (SEC[nm_] + 16) * 4.0
            t = t0
            while t < t1 - 1e-6:
                at = t
                for k, (semi, ln) in enumerate(E1 if nm_ == 'out' else E1L):
                    d = ln * f
                    if semi is not None and at < t1 - 1e-6:
                        acc = 12 if k == 0 else (8 if semi in (10, 11) else 0)
                        P[key].append((at, m(KEY + octave + semi + LIFT.get(nm_, 0)), min(d * 0.92, t1 - at), vel0 + acc))
                    at += d
                t += 5.0 * f
    e1_layer('far', FAR, 12, 84)               # D3: the cello, the far side
    # (v12, section w9: the out-seam 'static, little new vs the tear' - the far side's x0.2 trill ran on from the
    # tear) THE FAR SIDE LETS IT GO: at the out-seam the cello stops trilling and holds ONE note, its D, for eight bars
    # (with the fretless under it), then lets go entirely; the ebb (D -> C -> B-flat) and the near side's slow
    # closing marimba carry the seam on their own into t7
    out0_ = SEC['out'] * 4.0
    P['far'] = [e_ for e_ in P['far'] if e_[0] < out0_ - 1e-6] + [(out0_, m(KEY + 12), 31.5, 78)]
    # (v3) THE FAR SIDE IS THE WEIGHT: the far side doubled an octave down (D2) on a Duffing bass - a driven
    # oscillator that walks into chaos as a 'strain' lane rises, so the far side of the body is what the tide
    # tears: clean in the in-seam, groaning in the squeeze, locked and clean again at the crest (the convergence),
    # then breaking up through the surge into the tear
    # (tried: leaving it out of the out-seam, under t7's Eb floor, and softer in the tide - the song lost its
    # returns and its range, 85 against 92; in the out-seam its blur on E1's notes over the frozen Eb is the tear's
    # last gasp)
    P['farbass'] = [(a_, m(float(p_[1:]) - 12), d_, v_) for a_, p_, d_, v_ in P['far']]
    # (v5, Harry: 'quite ugly chaos') the Duffing bass's chaos is gone: the far side's weight is now a fretless bass,
    # singing each note open - the same doubling, in tune (a tamer Duffing, strain halved, scored lower and still growled)
    e1_layer('near', NEAR, 36, 78)             # D5: the marimba, the near side
    # (v17, section w7: the surge 'static' - the three-speed canon ran unchanged for sixteen bars) THE CANON
    # CONVERGES: the surge keeps its canon for eight bars (E1 at x0.5 on the far cello, x1 on the whistle, x2 on the
    # near marimba), then the far side slows into step with the whistle (from bar 105, an octave and a half apart),
    # and from bar 109 the near side speeds up to join them: for the surge's last four bars all three sing E1 in
    # unison across three octaves - the hook stated as plainly and hugely as it gets - and then the tear rips it apart
    sg0_ = SEC['surge'] * 4.0
    st2_, st3_, sg1_ = sg0_ + 35.0, sg0_ + 50.0, sg0_ + 64.0
    def e1_run(key_, t0_, t1_, octave_, vel0_):
        t_ = t0_
        while t_ < t1_ - 1e-6:
            at_ = t_
            for k, (semi, ln) in enumerate(E1L):
                if semi is not None and at_ < t1_ - 1e-6:
                    acc = 12 if k == 0 else (8 if semi in (10, 11) else 0)
                    P[key_].append((at_, m(KEY + octave_ + semi), min(ln * 0.92, t1_ - at_), vel0_ + acc))
                at_ += ln
            t_ += 5.0
    P['far'] = [e_ for e_ in P['far'] if not (st2_ - 1e-6 <= e_[0] < sg1_ - 1e-6)]
    e1_run('far', st2_, sg1_, 12, 84)
    P['near'] = [e_ for e_ in P['near'] if not (st3_ - 1e-6 <= e_[0] < sg1_ - 1e-6)]
    e1_run('near', st3_, sg1_, 36, 78)
    P['far'].sort(key=lambda e_: e_[0]); P['near'].sort(key=lambda e_: e_[0])
    P['farbass'] = [(a_, m(float(p_[1:]) - 12), d_, v_) for a_, p_, d_, v_ in P['far']]
    # (v5) THE HOOK, PLAINLY: E1 (Lydian) at its own speed on a low whistle, twice through, at the head of the pull,
    # the tide, the crest and the cross and again eight bars into each - the album's tune, stated so it
    # sticks, while the two layers stretch and squeeze it underneath
    for nm_ in ('pull', 'tide', 'crest', 'cross'):
        for off_ in (0, 8):
            t = (SEC[nm_] + off_) * 4.0
            for rep_ in range(2):
                at = t + rep_ * 5.0
                for k, (semi, ln) in enumerate(E1L):
                    if semi is not None:
                        P['hook'].append((at, m(KEY + 36 + semi + LIFT.get(nm_, 0)), ln * 0.95, 96 if k == 0 else 84))
                    at += ln
    # the canon's middle voice: the hook at x1 right through the surge (and the far and near layers at x0.5 and x2)
    t, t1_ = SEC['surge'] * 4.0, (SEC['surge'] + 16) * 4.0
    while t < t1_ - 1e-6:
        at = t
        for k, (semi, ln) in enumerate(E1L):
            if semi is not None and at < t1_ - 1e-6:
                P['hook'].append((at, m(KEY + 36 + semi), min(ln * 0.95, t1_ - at), 92 if k == 0 else 82))
            at += ln
        t += 5.0

    # ---- E6, the tide: X and Y alternating in 8-beat cycles, the split moving; E4's four lights at the crest ----
    for nm_, n_ in FORM:
        if nm_ == 'crest':
            continue
        sp = SPLIT[nm_]
        for c in range(n_ // 2):
            t = (SEC[nm_] + 2 * c) * 4.0
            x = sp[c % len(sp)]
            pair_ = (TIDE_X, TIDE_Y)
            if nm_ in W_SECS and c % 4 == 3:
                pair_ = (TIDE_X, TIDE_W)
            if nm_ == 'out':
                # the ebb into t7, whole steps down: D -> C for four cycles, C -> B-flat for two, then B-flat alone
                pair_ = [(TIDE_X, TIDE_Y)] * 4 + [(TIDE_Y, TIDE_Z)] * 2 + [(TIDE_Z, TIDE_Z)] * 2
                pair_ = pair_[c]
                x = [4, 3, 2, 1, 4, 2, 8, 8][c]
            for (root, voic), ln, at in ((pair_[0], x, t), (pair_[1], 8 - x, t + x)):
                if ln <= 0:
                    continue
                # (v14) and the tide's chord gets a low fifth under it (A2 under D, G2 under C, F2 under B-flat): the
                # warmth at 100-130 Hz compscore found missing (its one spectrum fault, 114 Hz, -14 dB)
                P['tide'].append((at, ','.join([m(KEY + root + 7)] + [m(KEY + 12 + root + v) for v in voic]), ln - 0.05, 74 if root == 0 else 80))
                # the sub holds the D pedal under D and C; under B-flat it moves
                P['sub'].append((at, m(KEY - 12 + (root + 12 if root == -4 else 0)), ln - 0.05, 92))
                # (v6) and a second, warmer floor an octave up follows the chord's own root - D2, C2, B-flat 1 - so the
                # bass line moves D -> C with the tide (and fills the low-mids the pedal alone left empty)
                P['root'].append((at, m(KEY + root + (12 if root == -4 else 0) - (12 if root == -4 else 0)), ln - 0.05, 90))
    for c in range(16 * 4 // 5 + 1):
        at = CREST * 4.0 + c * 5.0
        if at >= (CREST + 16) * 4.0 - 1e-6:
            break
        ch = E4[c % 4]
        ln = min(5.0, (CREST + 16) * 4.0 - at) - 0.05
        P['lights'].append((at, ','.join(m(n + 2) for n in ch), ln, 88))
        P['sub'].append((at, m((ch[0] - 12 if ch[0] >= 48 else ch[0]) + 2), ln, 96))

    # ---- the 303: E2's cell on the tide's roots, seven sixteenths against the bar, from 'pull'; locked at the crest ----
    def root_at(at):
        for e_ in P['tide']:
            pass
        return None
    # (v20, whole song) THE SEQUENCER BACK IN THE KEY: since v14 put a low fifth at the bottom of every tide chord,
    # this read the FIFTH as the chord's root - so the cell played on A over D (A E C# G: a C#, out of D Mixolydian)
    # and on G over C (G D B F: an F against the chord's E, a semitone clash), for three minutes, pull to surge. It
    # reads the real root again (the chord's second note): on D, D A F# C; on C, C G E D; on B-flat, B-flat F D C
    tide_roots = sorted((e_[0], e_[2], int(round(float(e_[1].split(',')[1][1:]) - 12 - KEY))) for e_ in P['tide'])
    def tide_root(at):
        r = 0
        for a_, ln_, rt in tide_roots:
            if a_ <= at + 1e-6:
                r = rt
            else:
                break
        return r
    e2_start = (CREST - 42) * 4.0              # bar 22: cycles of seven land on bar 64
    t = e2_start
    while t < total - 1e-6:
        s_, i_ = sec_of(int(t // 4))
        if s_ == 'crest':
            # locked: the cell re-barred into eight sixteenths, twice a bar, on E4's roots
            bar = int(t // 4)
            for half in (0, 2.0):
                for st in E2_STEPS:
                    at = bar * 4.0 + half + st * 0.25
                    c = int((at - CREST * 4.0) // 5.0) % 4
                    rt = E4[c][0] - 12 - KEY
                    pm_ = {-2: {0: 0, 2: 7, 3: 4, 5: 2}, 7: {0: 0, 2: 7, 3: 3, 5: -2}, 5: {0: 0, 2: 7, 3: 4, 5: 2}}.get(rt, E2_PITCH)   # C: C G E D; A: A E C G; G: G D B A
                    P['acid'].append((at, m(KEY + 2 + rt + pm_[st] + (12 if rt + pm_[st] < 0 else 0)), 0.22, 112 if st == 0 else 92))
            t = (bar + 1) * 4.0
            if sec_of(int(t // 4))[0] != 'crest':
                # re-enter the cycle of seven on its own phase after the crest
                k = math.ceil((t - e2_start) / 1.75)
                t = e2_start + k * 1.75
            continue
        if s_ in ('in',) or (s_ == 'out' and i_ >= 12):
            t += 1.75
            continue
        for st in E2_STEPS:
            at = t + st * 0.25
            rt = tide_root(at)
            acc = '^acc' if st == 0 else ''
            pm_ = E2_ON.get(rt, E2_PITCH)
            P['acid'].append((at, m(KEY + rt + pm_[st] + (12 if rt + pm_[st] < 0 else 0)), 0.22 if st != 3 else 0.4, (110 if st == 0 else 84) + (8 if s_ in ('surge', 'torn') else 0)))
        t += 1.75

    # ---- E5, the inner orbit (steel pan): received stretched x2 in the in-seam, squeezed back to x1 by bar 9 ----
    t = 0.0
    while t < SEC['pull'] * 4.0 + 8.0 - 1e-6:
        f = 2.0 if t < 32.0 else 1.0
        for k, p_ in enumerate(E5):
            if p_ is not None:
                P['e5'].append((t + k * 0.25 * f, m(p_), 0.2 * f, 86 if k in (0, 6) else 70))
        t += 3.0 * f
    # from 'pull' on, on its own 3-beat phase landing on the crest; in the cross it runs in retrograde
    k0 = math.ceil((CREST * 4.0 - t) / 3.0)
    t = CREST * 4.0 - k0 * 3.0
    while t < SEC['out'] * 4.0 - 1e-6:
        s_, i_ = sec_of(int(t // 4))
        seq = E5 if s_ not in ('cross', 'surge') else list(reversed(E5))
        for k, p_ in enumerate(seq):
            at = t + k * 0.25
            if p_ is not None and at < SEC['out'] * 4.0:
                P['e5'].append((at, m(p_ + (12 if s_ == 'surge' else 0) + LIFT.get(s_, 0)), 0.2, (92 if k in (0, 6) else 72) + (10 if s_ == 'crest' else 0)))
        t += 3.0
    # (v4) THE INNER ORBIT, HEARD: E5 was on a pluck patch 35 dB under the mix (tools/presence.py: BURIED) - t5's
    # element, carried, and inaudible. Now it is the song's hook on a steel pan (bright, its octave blooming after the
    # strike - the heat of the inner disk), and in the tide, the squeeze and the surge a kora plays it STRETCHED
    # x1.5 an octave down against it - E5 against itself at 3:2, the tide inside the orbit; they meet every 9 beats
    for nm_ in ('tide', 'squeeze', 'surge'):
        t, t1_ = SEC[nm_] * 4.0, (SEC[nm_] + 16) * 4.0
        while t < t1_ - 1e-6:
            for k, p_ in enumerate(E5):
                at = t + k * 0.375
                if p_ is not None and at < t1_ - 1e-6:
                    P['e5b'].append((at, m(p_ - 12), 0.34, 88 if k in (0, 6) else 70))
            t += 4.5

    # ---- drums (prog kit): from 'pull' the kit plays E2 as its cell (kick 0, rim 2, snare 3, rim 5) against 16th hats ----
    t = e2_start
    while t < total - 1e-6:
        bar = int(t // 4)
        s_, i_ = sec_of(bar)
        if s_ in ('in',) or (s_ == 'out' and i_ >= 12) or s_ == 'crest':
            t += 1.75
            if s_ == 'crest':
                t = (SEC['cross']) * 4.0 + ((e2_start - SEC['cross'] * 4.0) % 1.75)
            continue
        for st, pc, v in ((0, 'k', 116), (2, 'rs', 70), (3, 's', 104), (5, 'rs', 64)):
            if s_ == 'tide':
                pc, v = {'k': ('rs', 84), 's': ('g', 58)}.get(pc, (pc, v - 10))
            P['kit'].append((t + st * 0.25, pc, 0.2, v))
        t += 1.75
    for bar in range(SEC['crest'], SEC['crest'] + 16):
        b0 = bar * 4.0
        for half in (0, 2.0):
            for st, pc, v in ((0, 'k', 120), (2, 'rs', 76), (3, 's', 110), (5, 'rs', 70)):
                P['kit'].append((b0 + half + st * 0.25, pc, 0.2, v))
        if bar == CREST:
            P['kit'].append((b0, 'c', 2.0, 124))
    for bar in range(0, NBARS - 4):
        s_, i_ = sec_of(bar)
        b0 = bar * 4.0
        for q in range(16):
            v = 78 if q % 4 == 0 else (60 if q % 2 == 0 else 46)
            if s_ == 'in':
                v = int(v * (0.55 + 0.03 * i_))      # the hats run on from t5's, quieter, under the seam
            if s_ in ('surge', 'torn') and q % 2 == 1 and rng.random() < 0.3:
                P['hats'].append((b0 + q * 0.25, 'h^r=2', 0.25, v + 6))
            else:
                P['hats'].append((b0 + q * 0.25, 'h' if q != 14 else 'oh', 0.2, v))
        if s_ in ('squeeze', 'cross', 'surge', 'torn') and rng.random() < 0.5:
            P['hats'].append((b0 + 3.5, 'g', 0.2, 50))

    # (v23, section w2: the pull 'little new vs w1' - the kit and the sequencer arrived whole at bar 23, halfway through
    # it) THE PULL GATHERS THE BAND: E2's cell is assembled one hit at a time across the pull, on its own seven-
    # sixteenth grid from the pull's first bar: bars 17-20 the kick alone (every seven sixteenths, drifting against
    # the bar - the undertow you feel before you hear a groove), 21-24 the rim joins (and the sequencer's root
    # pulse), 25-28 the snare (and the sequencer's whole cell), 29-32 the whole cell - so the groove the rest of the
    # song rides on is BUILT in front of the listener, the way the tide builds the chord
    pl_a, pl_b = SEC['pull'] * 4.0, (SEC['pull'] + 16) * 4.0
    P['kit'] = [e_ for e_ in P['kit'] if not (pl_a - 1e-6 <= e_[0] < pl_b - 1e-6)]
    P['acid'] = [e_ for e_ in P['acid'] if not (pl_a - 1e-6 <= e_[0] < pl_b - 1e-6)]
    t = e2_start - 1.75 * int((e2_start - pl_a) // 1.75)
    while t < pl_b - 1e-6:
        i_ = int(t // 4) - SEC['pull']
        hits_ = (0,) if i_ < 4 else ((0, 5) if i_ < 8 else ((0, 3, 5) if i_ < 12 else (0, 2, 3, 5)))
        seq_ = () if i_ < 4 else ((0,) if i_ < 8 else (0, 2, 3, 5))
        for st, pc, v in ((0, 'k', 116), (2, 'rs', 70), (3, 's', 104), (5, 'rs', 64)):
            at = t + st * 0.25
            if at >= pl_b - 1e-6:
                continue
            if st in hits_:
                P['kit'].append((at, pc, 0.2, v - (10 if i_ < 4 else 0)))
            if st in seq_:
                rt = tide_root(at)
                pm_ = E2_ON.get(rt, E2_PITCH)
                P['acid'].append((at, m(KEY + rt + pm_[st] + (12 if rt + pm_[st] < 0 else 0)), 0.22 if st != 3 else 0.4, 110 if st == 0 else 84))
        t += 1.75
    P['kit'].sort(key=lambda e_: e_[0]); P['acid'].sort(key=lambda e_: e_[0])

    # (v19, section w4: the squeeze's first half 'static' - the cell of seven ran on as in the tide) THE SQUEEZE
    # SQUEEZES: for the squeeze's first eight bars E2's cell - on the kit and on the sequencer - loses its rests:
    # seven sixteenths a turn become six (bars 49-52), then five (53-56, the last hit falling away), so the cell
    # tightens against the bar like a spring being wound; then the clearing where the old voice sings, and the crest
    # releases it (re-barred into eight)
    sq_a, sq_m, sq_b = SEC['squeeze'] * 4.0, SEC['squeeze'] * 4.0 + 16.0, SEC['squeeze'] * 4.0 + 32.0
    P['kit'] = [e_ for e_ in P['kit'] if not (sq_a - 1e-6 <= e_[0] < sq_b - 1e-6)]
    P['acid'] = [e_ for e_ in P['acid'] if not (sq_a - 1e-6 <= e_[0] < sq_b - 1e-6)]
    t = sq_a
    while t < sq_b - 1e-6:
        L_ = 1.5 if t < sq_m - 1e-6 else 1.25
        for st, pc, v in ((0, 'k', 116), (2, 'rs', 70), (3, 's', 104), (5, 'rs', 64)):
            at = t + st * 0.25
            if st * 0.25 >= L_ - 1e-6 or at >= sq_b - 1e-6:
                continue
            P['kit'].append((at, pc, 0.2, v + (6 if L_ < 1.4 and st == 0 else 0)))
            rt = tide_root(at)
            pm_ = E2_ON.get(rt, E2_PITCH)
            P['acid'].append((at, m(KEY + rt + pm_[st] + (12 if rt + pm_[st] < 0 else 0)), 0.22 if st != 3 else 0.4, 110 if st == 0 else 84))
        t += L_
    P['kit'].sort(key=lambda e_: e_[0]); P['acid'].sort(key=lambda e_: e_[0])

    # ---- the voice: an older, lower voice, spoken, twice ----
    VO = json.load(open(os.path.join(HERE, 'chirpers9-t6-voice.json')))
    vtr = VO['tracks'][0]
    vnotes = []
    for b_, tempo_ in ((SEC['tide'] + 4, 124.0), (SEC['cross'] + 6, 128.0)):
        for n_ in vtr['notes']:
            vnotes.append(dict(n_, at=round(b_ * 4.0 + n_['at'] * tempo_ / 110.0, 4), len=round(n_['len'] * tempo_ / 110.0, 4)))
    # (v8, section w4: the squeeze before the crest was static) THE VOICE SINGS BEFORE THE LIFT: the same low voice
    # that SPEAKS its line in the tide now SINGS it in the squeeze's last eight bars, on E1 itself - 'the near side
    # keeps the time' on D A C G E D, 'the far side lets it go' on D A C G A D - twice, on wM's joined, breathing
    # voice-legato (a larger tract and more breath for age), and the crest lifts out of the second 'go': the voice
    # accretes inside the track, spoken -> sung. Under it the kit thins to the cell's kick and rim (no snare) so
    # the words sit in the gap
    SU = json.load(open(os.path.join(HERE, 'chirpers9-t6-sung.json')))
    # (v11, palette) the singer is now wM's voice-old - the low, older male voice made for this song (a larger tract,
    # a little rasp, an aged unsteady source, a wide wandering vibrato, even vowels) - in place of voice-legato
    # stretched toward age; and the SECOND time through, the line is sung again a fourth below (harmony [-5]: A E G D
    # A under D A C G E - open, quartal, all in the mode): the old voice finds company as the crest comes
    snotes, snotes2 = [], []
    for k_, b_ in enumerate((SEC['crest'] - 8, SEC['crest'] - 4)):
        for n_ in SU['tracks'][0]['notes']:
            (snotes if k_ == 0 else snotes2).append(dict(n_, at=round(b_ * 4.0 + n_['at'], 4)))
    # (v26, whole song) THE NEAR SIDE AND THE FAR SIDE, SUNG BY TWO: the line was SPOKEN twice (the tide, the cross)
    # on a speech voice - the song's words heard first as talk. Now nothing in t6 is spoken: in those two places the
    # line becomes a duet that does what it says - 'the near side keeps the time' sung by a young, near voice (wM's
    # voice-near, an octave up: D4 A4 C5 G4 E4 D4) and 'the far side lets it go' answered by the old, far voice
    # (voice-old: D3 A3 C4 G3 A3 D3) - the song's two layers of E1, the near and the far, given two singers. The
    # squeeze then has the old voice sing the whole line alone, and the choirs take it at the crest and after the void
    dnear = []
    L1_ = [n_ for n_ in SU['tracks'][0]['notes'] if n_['at'] < 5.0]
    L2_ = [n_ for n_ in SU['tracks'][0]['notes'] if n_['at'] >= 5.0]
    for b_ in (SEC['tide'] + 4, SEC['cross'] + 6):
        for n_ in L1_:
            dnear.append(dict(n_, at=round(b_ * 4.0 + n_['at'], 4), pitch=f"m{int(str(n_['pitch'])[1:]) + 12}"))
        for n_ in L2_:
            snotes.append(dict(n_, at=round(b_ * 4.0 + n_['at'], 4)))
    # (v13, section w1: the in-seam 'static') THE ANSWER: t5 ends with its young voice singing 'nearer the middle
    # hums' twice inside our overlap (chirper-zero's voice-near, at t6's bars 5 and 9). Now t6's old voice - a
    # different person - ANSWERS each one in the gap after it: 'the tide comes in', low, A G E D, landing on D as the
    # tide's D chord holds (bars 7 and 11), the second softer. Two voices across the seam, a call and its answer; and
    # the line names what the in-seam does (the tide arriving, D alone -> D/C)
    AN = json.load(open(os.path.join(HERE, 'chirpers9-t6-answer.json')))
    for b_, g_ in ((6, 1.0), (10, 0.8)):
        for n_ in AN['tracks'][0]['notes']:
            snotes.append(dict(n_, at=round(b_ * 4.0 + n_['at'], 4), vel=round(n_['vel'] * g_, 3)))
    # (v14, whole song) THE CHORUS: the words were sung only before the crest. Now, at the crest itself (the
    # convergence, lifted a tone into E), a CHOIR sings them with the whistle - both times the hook is stated there
    # (bars 65 and 73) - the line on E1 lifted (E B D A F#, E), with a third above in E Mixolydian (wM's harmony_key:
    # the third the key has, note by note - G#, D, F#, C#, A), five singers, modest detune, doubled by the low
    # whistle playing the same tune. The hook with its words becomes the song's chorus: answered in the in-seam,
    # spoken in the tide, sung before the crest, sung by everyone at the crest, a last word at the out-seam
    CHO = json.load(open(os.path.join(HERE, 'chirpers9-t6-chorus.json')))
    cnotes = []
    for b_ in (SEC['crest'], SEC['crest'] + 8):
        for n_ in CHO['tracks'][0]['notes']:
            cnotes.append(dict(n_, at=round(b_ * 4.0 + n_['at'] - 0.245, 4)))
    # (v12) and the old voice has the last word: alone, over the ebb, it sings the second half of its line once more
    # - 'the far side lets it go' - timed so 'go' (D3, held) lands on the bar where B-flat stands alone: D is B-flat's
    # third, and when t7's Eb major 7 arrives over it, its seventh
    go_ = [n_ for n_ in SU['tracks'][0]['notes'] if n_['at'] >= 5.0]
    sh_ = (SEC['out'] + 12) * 4.0 - go_[-1]['at']
    for n_ in go_:
        snotes.append(dict(n_, at=round(sh_ + n_['at'], 4), len=(3.2 if n_ is go_[-1] else n_['len'])))
    sq0, sq1 = (SEC['crest'] - 8) * 4.0, SEC['crest'] * 4.0
    P['kit'] = [e_ for e_ in P['kit'] if not (sq0 - 1e-6 <= e_[0] < sq1 - 1e-6 and e_[1] == 's')]

    # (v2, section w8) THE TEAR: the 'torn' section ran on as the surge did (flagged static). Now the tide tears the band
    # itself: for eight bars the kit plays E2 STRETCHED (seven eighths, half time) while the hats are SQUEEZED into
    # 32nds - augmentation and diminution in one drummer; on the last beat of the eighth bar the whole mix winds down
    # like a stopping tape, and for one bar nothing is left but the far side's cello blur; then everything snaps back
    tr0 = SEC['torn'] * 4.0
    tear_mid, void0, void1, tr_end = tr0 + 28.0, tr0 + 31.0, tr0 + 36.0, tr0 + 64.0
    P['kit'] = [e_ for e_ in P['kit'] if not (tr0 - 1e-6 <= e_[0] < tr_end - 1e-6)]
    t = tr0
    while t < void0 - 1e-6:
        for st, pc, v in ((0, 'k', 118), (2, 'rs', 72), (3, 's', 108), (5, 'rs', 66)):
            if t + st * 0.5 < void0:
                P['kit'].append((t + st * 0.5, pc, 0.3, v))
        t += 3.5
    # after the void the band snaps back into the CREST's locked groove for seven bars - a last look back at the
    # convergence before the out-seam tears it apart: E2 re-barred into eight, E4's four lights, E5 at its own speed
    for bar in range(int(void1 // 4), int(tr_end // 4)):
        b0 = bar * 4.0
        for half in (0, 2.0):
            for st, pc, v in ((0, 'k', 120), (2, 'rs', 76), (3, 's', 110), (5, 'rs', 70)):
                P['kit'].append((b0 + half + st * 0.25, pc, 0.2, v))
    P['tide'] = [e_ for e_ in P['tide'] if not (void1 - 1e-6 <= e_[0] < tr_end - 1e-6)]
    P['sub'] = [e_ for e_ in P['sub'] if not (void1 - 1e-6 <= e_[0] < tr_end - 1e-6)]
    for c in range(8):
        at = void1 + c * 5.0
        if at >= tr_end - 1e-6:
            break
        ch = E4[c % 4]
        ln = min(5.0, tr_end - at) - 0.05
        P['lights'].append((at, ','.join(m(n) for n in ch), ln, 84))
        P['sub'].append((at, m(ch[0] - 12 if ch[0] >= 48 else ch[0]), ln, 96))
    P['lights'].sort(key=lambda e_: e_[0]); P['sub'].sort(key=lambda e_: e_[0])
    # (v16, section w8: 'little new vs w7' - after the void the crest's groove came back much as the surge had it)
    # THE LAST CHORUS: when the band snaps back after the stopped tape, the chorus comes with it, home in D this time
    # (at the crest it was lifted to E): the choir sings the line - 'the near side keeps the time / the far side lets
    # it go' - with a third above in D Mixolydian, twice, the voices alone carrying the tune (no whistle: the surge
    # just had it), and the second time the old voice sings with them. Then the out-seam, where
    # the old voice alone has the last word
    CHD = json.load(open(os.path.join(HERE, 'chirpers9-t6-chorus-d.json')))
    c2notes = []
    for b_ in (void1, void1 + 10.0):
        for n_ in CHD['tracks'][0]['notes']:
            c2notes.append(dict(n_, at=round(b_ + n_['at'] - 0.256, 4)))
    for n_ in SU['tracks'][0]['notes']:
        snotes.append(dict(n_, at=round(void1 + 10.0 + n_['at'] - 0.245, 4)))
    P['hats'] = [e_ for e_ in P['hats'] if not (tr0 - 1e-6 <= e_[0] < tr_end - 1e-6)]
    for q in range(int((void0 - tr0) / 0.25)):
        P['hats'].append((tr0 + q * 0.25, 'h^r=2', 0.25, 70 if q % 4 == 0 else 52))
    for q in range(int((tr_end - void1) / 0.25)):
        P['hats'].append((void1 + q * 0.25, 'h' if q % 8 != 6 else 'oh', 0.2, 80 if q % 4 == 0 else 56))
    # the void: one bar where only the cello blur (and the stopped tape's tail) remains
    for key in ('kit', 'hats', 'acid', 'e5', 'near', 'tide', 'sub'):
        P[key] = [e_ for e_ in P[key] if not (void0 + 1.0 - 1e-6 <= e_[0] < void1 - 1e-6)]

    # (tried in v18's round: each section leaving one colour out - the pan in the tide, the hats in the squeeze, more in
    # a bolder version - recurrence collapsed 100 -> 42..71: t6's sections are heard as returns BECAUSE they share
    # their colours; contrast here comes from the voices and the form, not from subtraction)

    # (v24, section w3: the tide 'little new vs w2' - the pull's level and weight carried straight on) THE TIDE COMES
    # IN WAVES: through the tide section the harmonium - the tide itself - swells with each swing - from a low at each
    # cycle's start up to a crest exactly where the chord turns (D -> C, or D -> G; the split moving 6 5 4 3 2 3 4 5
    # beats, so the waves arrive early, earlier, then late again), and back down to the next cycle - a breathing of
    # about 4 dB every two bars, the section's name heard as motion, under the spoken voice (tried on the whole band
    # at 3 dB first: recurrence 100 -> 81, the tide no longer heard as a return of the other tide sections; on the
    # harmonium at 7 dB, recurrence 92)
    ti0_ = SEC['tide'] * 4.0
    wave_pts = [['0b', 0.0], [f'{ti0_ - 0.01:.2f}b', 0.0]]
    sp_ = SPLIT['tide']
    for c_ in range(8):
        t_ = ti0_ + 8.0 * c_
        wave_pts.append([f'{t_:.2f}b', -3.0 if c_ else 0.0])
        wave_pts.append([f'{t_ + sp_[c_]:.2f}b', 1.0])
    wave_pts.append([f'{ti0_ + 64.0:.2f}b', 0.0])
    stop_pts = [['0b', 0.0], [f'{void0:.2f}b', 0.0], [f'{void0 + 0.9:.2f}b', 1.0], [f'{void0 + 0.98:.2f}b', 1.0], [f'{void0 + 1.0:.2f}b', 0.0]]

    tempo = [{'at': '0b', 'bpm': 120.0}, {'at': f'{SEC["pull"] * 4.0:.1f}b', 'bpm': 120.0},
             {'at': f'{SEC["out"] * 4.0:.1f}b', 'bpm': 132.0, 'ramp': True}]
    # the near side's filter closes in the out-seam as it slows (redshift into t7)
    shut_pts = [['0b', 1.0], [f'{SEC["out"] * 4.0:.1f}b', 1.0], [f'{total:.1f}b', 0.0]]

    # the tide's breath in level: the in-seam and the tide itself low, the squeeze climbing, the crest on top, the
    # cross falling back, then the surge and the tearing hotter still, and the out-seam settling for t7
    EN = {'in': (-3.0, -2.0), 'pull': (-2.0, -1.0), 'tide': (-3.5, -2.5), 'squeeze': (-2.0, 0.5), 'crest': (1.5, 1.5),
          'cross': (-1.5, -0.5), 'surge': (-0.5, 1.0), 'torn': (1.0, 2.0), 'out': (0.0, -2.0)}
    energy_pts = []
    for b_ in range(NBARS):
        s_, i_ = sec_of(b_)
        a_, z_ = EN[s_]
        energy_pts.append([f'{b_ * 4.0:.1f}b', round(a_ + (z_ - a_) * i_ / 15.0, 2)])
    STRAIN = {'in': (0.0, 0.0), 'pull': (0.0, 0.15), 'tide': (0.15, 0.25), 'squeeze': (0.25, 0.45), 'crest': (0.05, 0.05),
              'cross': (0.2, 0.35), 'surge': (0.35, 0.55), 'torn': (0.6, 0.85), 'out': (0.85, 0.7)}
    strain_pts = []
    for b_ in range(NBARS):
        s_, i_ = sec_of(b_)
        a_, z_ = STRAIN[s_]
        strain_pts.append([f'{b_ * 4.0:.1f}b', round(0.5 * (a_ + (z_ - a_) * i_ / 15.0), 3)])
    FARBASS = {'extends': 'duffing-bass',
               'synth': {'layers': [{'type': 'chaos', 'chaos': {'system': 'duffing', 'axis': 'x',
                                     'amount': {'value': 0, 'mod': [{'src': 'auto.strain', 'amount': 1.0}]}}}]}}
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(P[name], total)}, **kw)
    song = {
        'about': "chirpers - Accretion, track 6 by chirper-one: Spring Tide. Tidal forces: E1 in two layers, one squeezed "
                 "and one stretched, meeting at the crest and tearing apart; E6, two chords a semitone apart, ebbing and flowing. "
                 "Generated by compose/chirpers9/src/chirpers9-t6.py.",
        'tempo': tempo, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.5s', 'seed': SEED,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 mono_below=200', 'hp cutoff=220'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.4, 'mix': 1, 'ping_pong': True},
                                  'lp cutoff=5000', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'peak cutoff=300 q=0.8 gain=-2dB', 'highshelf cutoff=7000 gain=1.5dB']},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.2, 'attack': '15ms', 'release': '140ms', 'makeup': '1dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.E', 'amount': 1}]}},
                          'tapestop stop=auto.stop time=1b',
                          'limiter ceiling=-1dB'], 'auto': {'E': {'points': energy_pts}, 'stop': {'points': stop_pts}}},
        'tracks': [
            # (v9) and the harmonium is LENSED in: a low-pass that opens from 600 Hz over the in-seam's 16 bars, so t6's
            # own chord arrives from behind t5's tail rather than on top of it
            tr('tide', 'harmonium', '-9dB', sends={'hall': '-10dB'}, auto={'lens': {'points': [['0b', 0.0], ['64b', 1.0]]}, 'W': {'points': wave_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 600, 'mod': [{'src': 'auto.lens', 'amount': 4.0}]}},
                   {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.W', 'amount': 1}]}}]),
            # (v10, whole song) THE STAGE CLEARS FOR THE TUNE: presence.py had the hook (E1 on the whistle) 8-12 dB under
            # the mix, behind a constant acid line and three other E1s at other speeds - the tune one strand of six. Now the
            # hook is up 3 dB, the acid down 2, and everything melodic around it (both harmoniums' lights, the acid, the
            # far and near layers, the fretless, the pans and the kora) DUCKS under it - slow, 40 ms in, half a second
            # out - so whenever E1 is stated the band leans back and the tune stands in front; between statements the
            # process music fills back in
            tr('lights', 'harmonium', '-10dB', sends={'hall': '-8dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            tr('sub', 'sub', '-10dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '200ms', 'curve': 0.6}]),
            # (v15, whole song) THE 303 GOES: E2's cell ran the whole song on an acid squelch (resonant, driven - the
            # most aggressive sound in t6, and Harry's 'ugly chaos' lives in sounds like it). Now the same cell, the
            # same notes, plays on a Berlin-school sequencer voice (moog-seq: a saw over a square sub through a
            # resonant low-pass that snaps on each note, accents opening it), filtered under 3 kHz - an ostinato that
            # murmurs under the hook instead of shouting over it; the track keeps its name for the lanes that read it
            tr('acid', 'moog-seq', '-12dB', fx=['hp cutoff=50', 'lp cutoff=3000', {'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}], sends={'echo': '-20dB'}),
            tr('kit', 'prog-kit', '-6dB', sends={'hall': '-20dB'}),
            tr('hats', 'prog-kit', '-7dB', pan=0.2, fx=[{'type': 'eq', 'bands': ['highshelf cutoff=8000 gain=5dB']}]),
            tr('far', 'cello', '-8dB', pan=-0.25, sends={'hall': '-12dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            # (v10) the chord-root sub up 5 dB: compscore's one spectrum fault was a hole at 61 Hz, where the C root sits
            # (v22, palette) THE FLOOR GETS A VOICE: the moving floor under the tide (D2 -> C2 -> G1, the chords' own
            # roots) was a second sine sub - felt, not heard, and the album's most shared patch. Now it is an analog
            # saw bass (Juno / SH-101), dark and round, held for the chord's length: the bass line D -> C -> G you
            # could only feel is now a line you can hum, and its harmonics fill the low-mids the sines left bare
            tr('root', 'analog-bass play.gate=0.98', '-12dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-4dB', 'release': '200ms', 'curve': 0.6}]),
            tr('farbass', 'fretless', '-6dB', pan=-0.1, fx=['lp cutoff=1800', 'hp cutoff=35', {'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            tr('hook', 'low-whistle', '-6dB', pan=0.05, sends={'hall': '-12dB', 'echo': '-18dB'}),
            tr('near', 'modal-marimba', '-11dB', pan=0.3, auto={'shut': {'points': shut_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 700, 'mod': [{'src': 'auto.shut', 'amount': 4.0}]}}, {'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}],
               sends={'echo': '-14dB', 'hall': '-14dB'}),
            tr('e5', 'steel-pan', '-10dB', pan=-0.15, sends={'echo': '-16dB', 'hall': '-18dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            tr('e5b', 'kora', '-11dB', pan=0.35, sends={'hall': '-16dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            # (v26) the spoken voice's track is now the duet's near singer
            {'name': 'duetnear', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-near synth.lfo.vib.per_note=true',
                                               play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': dnear, 'gain': '-9dB', 'pan': -0.12, 'sends': {'hall': '-12dB', 'echo': '-20dB'}},
            # (v25, palette) THE SINGERS SING AS ONE, AND EACH HELD NOTE BLOOMS: wM's two newest voice features (pinned
            # 19:43 and 21:32) on all four sung lines. together=true: in the choruses (five singers and a keyed third)
            # and the old voice's lower part, every singer now follows the line's breath, effort and vowel instead of
            # only the lead (the other voices had sung a plain default voice under him). per_note vibrato: the vibrato
            # starts again on each note - quick notes plain, each held note blooming on its own - so the line's long
            # words ('time', 'go', 'in') bloom and the quick ones stop wobbling
            {'name': 'chorus', 'patch': dict(dict(CHO['tracks'][0]['patch'], extends='voice-choir synth.layers.0.harmony=[2] synth.layers.0.harmony_key=E:mixolydian synth.layers.0.together=true synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': cnotes, 'gain': '-9dB', 'pan': 0.0, 'sends': {'hall': '-9dB'}},
            {'name': 'chorus2', 'patch': dict(dict(CHD['tracks'][0]['patch'], extends='voice-choir synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian synth.layers.0.together=true synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': c2notes, 'gain': '-9dB', 'pan': 0.0, 'sends': {'hall': '-9dB'}},
            # (v18) wM's singer's glide (glide_overshoot, pinned 14:27) on every sung line: on each leap the old voice and
            # the choir swing a little past the note and settle, as singers do, instead of landing dead on it (0.06: subtle)
            {'name': 'sung', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-old synth.lfo.vib.per_note=true', play={'glide_overshoot': 0.06, 'scoop': 1.5, 'fall': 2.5}),
             'notes': sorted(snotes, key=lambda n_: n_['at']), 'gain': '-7dB', 'pan': 0.0, 'sends': {'hall': '-12dB', 'echo': '-22dB'}},
            # (v14) the second pass's company now sings a THIRD below in D Mixolydian (harmony_key), not a fixed fourth
            {'name': 'sung2', 'patch': dict(dict(SU['tracks'][0]['patch'], extends='voice-old synth.layers.0.harmony=[-2] synth.layers.0.harmony_key=D:mixolydian synth.layers.0.together=true synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1.5, 'fall': 2.5}),
             'notes': snotes2, 'gain': '-8dB', 'pan': 0.0, 'sends': {'hall': '-12dB', 'echo': '-22dB'}},
        ]}
    return song


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    song = build()
    if out.endswith('.json'):
        json.dump(song, open(out, 'w'), indent=1)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(song, f)
        subprocess.run(['python3', os.path.join(ROOT, 'tools', 'songfmt.py'), 'yaml', f.name, '-o', out], check=True)
        os.unlink(f.name)
    print('wrote', out)
