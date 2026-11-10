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
E2_ON[-5] = {0: 0, 2: 7, 3: 3, 5: -2}                     # (v27) on A: A E C G
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
TIDE_V = (-5, [0, 3, 7, 10])     # (v27) Am7: A C E G
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


# (v60) the tempo map as (bar, bpm, ramp-from-the-previous-point)
TEMPO_PTS = [(0, 120.0, False), (SEC['pull'], 120.0, False), (SEC['squeeze'], 123.0, True), (SEC['crest'], 127.0, True),
             (SEC['cross'], 127.0, False), (SEC['surge'], 124.0, True), (SEC['torn'], 131.0, True), (SEC['out'], 132.0, True)]


def tempo_at(bar):
    for (b0, v0, _), (b1, v1, r1) in zip(TEMPO_PTS, TEMPO_PTS[1:]):
        if b0 <= bar < b1:
            return v0 + (v1 - v0) * (bar - b0) / (b1 - b0) if r1 else v0
    return TEMPO_PTS[-1][1]


def swung(score, at0, at1, amt):
    # (v57, from t2's v44) put a 16th shuffle on a score between two beats: split the rest that crosses each boundary
    # and put the engine's swing16= directive there
    out, t, done_ = [], 0.0, set()
    for tk in score.split(' '):
        base, _, rest_ = tk.partition('/')
        dur = float(rest_.split('b')[0])
        for mark, tok in ((at0, f"swing16={amt}"), (at1, "swing16=0.5")):
            if mark in done_:
                continue
            if t < mark - 1e-6 < t + dur - 1e-6 and base == 'R':
                out.append(f"R/{mark - t:.4f}b"); out.append(tok); dur -= mark - t; t = mark; tk = f"R/{dur:.4f}b"; done_.add(mark)
            elif t >= mark - 1e-6:
                out.append(tok); done_.add(mark)
        out.append(tk); t += dur
    return ' '.join(out)


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
            # (v28, whole song) THE TIDE TURNS OVER IN EVERY SECTION: Harry, 6 Nov 23:55 - 'very little change ... add
            # subtle variation'; v27 found that what moves the ear (and flatness.py) over 30 s is the HARMONY, not the
            # surface. So each vamping section now has a second chord pair for one of its halves, every chord in D
            # Mixolydian or borrowed from its minor: the tide's second half swings Am7 -> G (v -> IV); the squeeze's
            # first half and the cross's second half swing B-flat -> C - E3 itself, t3's D | B-flat | C, carried here
            # (B-flat held, C a beat in the squeeze: the pressure before the sung clearing on D); the tear's D -> B-flat
            # (the darkest colour, before the out-seam's ebb onto B-flat); the first halves (and the duet) stay on E6's
            # D and C. (Am7/G there first: too close to D/C - the ear and flatness.py barely moved)
            if nm_ == 'tide' and c >= 4:
                pair_ = (TIDE_V, TIDE_W)
            if (nm_ == 'squeeze' and c < 4) or (nm_ == 'cross' and c >= 4):
                pair_ = (TIDE_Z, TIDE_Y)
            if nm_ == 'torn':
                pair_ = (TIDE_X, TIDE_Z)
            if nm_ == 'surge' and c in (2, 3):
                # (v63, section w7: 3:06-3:36, the surge - eco: the 48 s still run, 2:48-3:36, back since v58; each
                # 8-bar half of the surge sounded the same twice over, D and C under it all) THE SURGE CLIMBS IN FOUR-
                # BAR STEPS: the harmony now turns every four bars - D/C for the low gear's first four, the cross's
                # B-flat/C for its second (the water still drawn back), D/C again as the high gear lands, and G/A minor
                # 7 (the pull's far shore) for the last four under the choir's 'near and far as one', the line's own
                # notes; then the tear's D/B-flat. Every chord in D Mixolydian or borrowed from its minor
                pair_ = (TIDE_Z, TIDE_Y)
            if nm_ == 'surge' and c in (6, 7):
                pair_ = (TIDE_W, TIDE_V)
            if nm_ == 'pull' and c >= 4:
                # (v27) the pull's second half turns the tide over: G(add9) and Am7 (IV and v of D Mixolydian, every
                # note in the mode) instead of D and C - the same swing, the split still moving, on the far shore -
                # and the tide section comes home to D. The harmony's first real move, eight bars in
                pair_ = (TIDE_W, TIDE_V)
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
    for b_, tempo_ in ((SEC['tide'] + 4, tempo_at(SEC['tide'] + 4)), (SEC['cross'] + 6, tempo_at(SEC['cross'] + 6))):
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
    # (v37, section w3: the tide 'little new vs w2' - the tide section sounded like the pull again) THE TIDE SINGS
    # HIGH: after the duet, over the tide's second half (bars 41-47, Am7 and G swinging), the young near voice floats a
    # wordless 'ooh' far above everything in FALSETTO (wM's register=1: head voice, rounder, softer) - E5 held, then
    # stepping down D C B A to G, one long note a bar, like a wave coming in high and drawing back - a descant the pull
    # never had, quiet, in the hall
    DS = json.load(open(os.path.join(HERE, 'chirpers9-t6-descant.json')))
    dsnotes = [dict(n_, at=round((SEC['tide'] + 8) * 4.0 + n_['at'] - 0.25, 4)) for n_ in DS['tracks'][0]['notes']]
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
    # (v38, section w9: the out-seam 'static') THE OLD MAN'S LAST WORD, AND THE FAR SIDE LETS GO: his last line is
    # now sung by an OLDER voice - wM's age (0.8): the folds leaking air, a slow tremor shaking the held 'go' - the
    # same man, the tide gone out of him; and as 'go' lands on the B-flat bar, the far side's trombone, silent since
    # its held D, comes back once, softly, and SLIDES down D -> C -> B-flat - the ebb, and the words, played by the
    # far side itself - holding B-flat (t7's V, under its Bbsus4 -> Bb7) to the end of the seam
    lastnotes = []
    for n_ in go_:
        lastnotes.append(dict(n_, at=round(sh_ + n_['at'], 4), len=(3.2 if n_ is go_[-1] else n_['len'])))
    lw_ = (SEC['out'] + 12) * 4.0
    P['far'] = [e_ for e_ in P['far'] if e_[0] < lw_ - 1e-6]
    P['far'] += [(lw_ + 0.5, m(KEY + 12), 0.9, 60), (lw_ + 1.5, m(KEY + 10), 0.9, 58), (lw_ + 2.5, m(KEY + 8), 5.0, 56)]
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
    # (v32, section w7: the surge 'static' - the canon converges into a three-octave unison, but only instruments
    # carried it, the melody line unchanged for thirty seconds) THE CHOIR SINGS THE MEETING: where the far side joins
    # the whistle (bar 108) the choir enters, softly, on E1 itself - 'near and far as one' - and as the near side
    # joins too, for the surge's last four bars it sings with everything, an octave under itself: 'near and far as
    # one, near and far as one, all of it at once' - the story of the song (the near side and the far side, crossing)
    # sung at the one moment they are the same - and then the tear rips it apart
    SG = json.load(open(os.path.join(HERE, 'chirpers9-t6-surge.json')))
    sgn_ = SG['tracks'][0]['notes']
    sgnotes = []
    _sg0 = SEC['surge'] * 4.0
    for n_ in sgn_[:5]:
        sgnotes.append(dict(n_, at=round(_sg0 + 45.0 + n_['at'] - 0.245, 4), vel=round(n_['vel'] * 0.6, 3)))
    for n_ in sgn_:
        sgnotes.append(dict(n_, at=round(_sg0 + 50.0 + n_['at'] - 0.245, 4)))
    c2notes = []
    for b_ in (void1, void1 + 10.0):
        for n_ in CHD['tracks'][0]['notes']:
            c2notes.append(dict(n_, at=round(b_ + n_['at'] - 0.256, 4)))
    for n_ in SU['tracks'][0]['notes']:
        snotes.append(dict(n_, at=round(void1 + 10.0 + n_['at'] - 0.245, 4)))
    # (v33, section w8: the tear 'static' - sixteen bars of the stretched kit and the 32nd hats with nothing sung over
    # them, between the surge's unison and the last chorus) THE TEAR, SUNG: the duet comes back and is torn apart the
    # way the tide tears the disk - the near voice sings 'the near side keeps the time' FASTER each time (x0.75 twice,
    # then x0.6 three times, racing ahead, an octave up), while the old voice sings 'the far side lets it go' SLOWER
    # (x1.5, then x2.2, dragging behind, low) - the same words pulled out of step, the song's whole idea in two
    # voices - until the stopped tape and the void, and then the last chorus sings it together
    for st_, f_ in ((tr0 + 2.0, 0.75), (tr0 + 6.0, 0.75), (tr0 + 10.0, 0.6), (tr0 + 13.25, 0.6), (tr0 + 16.5, 0.6)):
        for n_ in L1_:
            dnear.append(dict(n_, at=round(st_ + n_['at'] * f_, 4), len=round(n_['len'] * f_, 4),
                              pitch=f"m{int(str(n_['pitch'])[1:]) + 12}", vel=round(n_['vel'] * 0.92, 3)))
    for st_, f_ in ((tr0 + 2.5, 1.5), (tr0 + 12.0, 2.2)):
        for n_ in L2_:
            snotes.append(dict(n_, at=round(st_ + (n_['at'] - 5.0) * f_, 4), len=round(n_['len'] * f_, 4)))
    P['hats'] = [e_ for e_ in P['hats'] if not (tr0 - 1e-6 <= e_[0] < tr_end - 1e-6)]
    for q in range(int((void0 - tr0) / 0.25)):
        P['hats'].append((tr0 + q * 0.25, 'h^r=2', 0.25, 70 if q % 4 == 0 else 52))
    for q in range(int((tr_end - void1) / 0.25)):
        P['hats'].append((void1 + q * 0.25, 'h' if q % 8 != 6 else 'oh', 0.2, 80 if q % 4 == 0 else 56))
    # (v35, section w8: eco's as-heard reading - 3:09-4:05 still one flat run; sung lines over a dense, steady floor
    # don't register, a change in the floor does) THE FLOOR TEARS AWAY: as the duet is torn furthest apart (bars
    # 117-120, the near voice racing, the old one dragging) the floor goes - the analog bass, the fretless and the sequencer; only the sine sub's pedal is left under it
    # (with the sub gone too, and for all eight bars, the low end emptied for 15 s: spectrum 83 -> 78; eight bars
    # without the sub, 81) - and the torn voices, the stretched
    # kit, the 32nd hats, the harmonium and the far side's brass blur hang over almost nothing; the stopped tape
    # and the void follow, and the floor comes back with the band and the last chorus (bar 122): the drop and the
    # return the tear was always about
    fd0_ = tr0 + 16.0
    for key_ in ('root', 'farbass', 'acid'):
        P[key_] = [e_ for e_ in P[key_] if not (fd0_ - 1e-6 <= e_[0] < void1 - 1e-6)]
        P[key_] = [(e_[0], e_[1], min(e_[2], fd0_ - e_[0]), *e_[3:]) if e_[0] < fd0_ < e_[0] + e_[2] else e_ for e_ in P[key_]]
    # the void: one bar where only the cello blur (and the stopped tape's tail) remains
    for key in ('kit', 'hats', 'acid', 'e5', 'near', 'tide', 'sub'):
        P[key] = [e_ for e_ in P[key] if not (void0 + 1.0 - 1e-6 <= e_[0] < void1 - 1e-6)]
    # (v45, section w8: the tear still read 'static' - the surge's whole band ran on under the torn duet, the
    # harmonium the loudest bed) THE TEAR CLEARS THE ROOM: on the tear's downbeat the steel pan, the marimba, the
    # sequencer and the whistle are ripped out with it - what is left is the tide's harmonium, the two voices being
    # pulled apart (the near one racing up, the old one slowing), the stretched drummer and its 32nd hats, the
    # trombone (the far side) and the floor; four bars on the floor tears away too, then the tape stops, and only
    # then does the whole band snap back for the last chorus. Fullest (the surge) -> bare -> barer -> nothing ->
    # everything. (The tide out too scored 97.59/96.82: seed 11 split into 17 sections)
    for key in ('e5', 'near', 'acid', 'hook', 'e5b'):
        P[key] = [e_ for e_ in P[key] if not (tr0 + 0.5 - 1e-6 <= e_[0] < void1 - 1e-6)]
        P[key] = [(e_[0], e_[1], min(e_[2], tr0 + 0.5 - e_[0]), *e_[3:]) if e_[0] < tr0 + 0.5 < e_[0] + e_[2] else e_ for e_ in P[key]]
    # (v49, section w8: still 'static' - after the stopped tape the whole band snapped straight back with the last
    # chorus, so the window ran full from the tear's end to the seam) THE LAST CHORUS STARTS ALONE: after the tape
    # stops, the band does NOT come back at once - the choir (with its basses) sings the first line of the last
    # chorus, 'the near side keeps the time / the far side lets it go', over nothing but the harmonium's lights and
    # the sub, home in D; then on the second statement the band crashes back in, the crest's locked groove, and runs
    # into the seam. The song's chorus heard bare once, at the moment everything has been torn away
    ac0_, ac1_ = void1, void1 + 10.0
    for key in ('kit', 'hats', 'acid', 'root', 'farbass', 'near', 'e5', 'e5b', 'hook', 'far'):
        P[key] = [e_ for e_ in P[key] if not (ac0_ - 1e-6 <= e_[0] < ac1_ - 1e-6)]
    P['kit'].append((ac1_ - 1.0, 's', 0.25, 70)); P['kit'].append((ac1_ - 0.5, 's', 0.25, 92))
    P['kit'].append((ac1_, 'c', 2.0, 116)); P['kit'].append((ac1_, 'k', 0.25, 124))
    P['kit'].sort(key=lambda e_: e_[0])

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
    # (v27, section: the flat run 0:32-1:28 - Harry, 6 Nov 23:55: 'lots of contiguous music with very little change
    # or dynamism ... add subtle variation so it doesnt get boring'; tools/flatness.py read t6 70% flat, this its
    # longest run, 56 s) SOMETHING MOVES EVERY EIGHT BARS through the pull and the tide's first half, the groove, key
    # and parts unchanged: bars 17-24 the harmonium sits an octave down and the hats play only eighths (dark, spare -
    # the tide still far out); bars 25-32 the harmonium comes up into its own register and the sixteenths fill in
    # with the whistle's hook (the tide arriving); bars 33-36 the marimba and the sequencer drop out (the water
    # drawing back), and come back at bar 37 under the duet; bars 41-44 open hats on every off-beat lift the tide's
    # second wave, and a snare fill in sixteenths throws it into bar 45
    pv0_, pv1_, pv2_ = SEC['pull'] * 4.0, SEC['pull'] * 4.0 + 32.0, SEC['tide'] * 4.0
    def down_(ch_):
        tk_ = ch_.split(',')
        return ','.join([tk_[0]] + [f"m{float(x_[1:]) - 12:.3f}" for x_ in tk_[1:]])
    P['tide'] = [((e_[0], down_(e_[1])) + tuple(e_[2:])) if pv0_ - 1e-6 <= e_[0] < pv0_ + 32.0 - 1e-6 else e_ for e_ in P['tide']]
    P['hats'] = [e_ for e_ in P['hats'] if not (pv0_ - 1e-6 <= e_[0] < pv0_ + 32.0 - 1e-6 and abs((e_[0] * 2) - round(e_[0] * 2)) > 1e-6)]
    for key_ in ('near', 'acid'):
        P[key_] = [e_ for e_ in P[key_] if not (pv2_ - 1e-6 <= e_[0] < pv2_ + 16.0 - 1e-6)]
    # (v41, section w2: the pull 'little new vs w1' - the in-seam's harmonium, marimba and kora ran straight on into
    # it) THE SEA DRAWS BACK: before a wave the water pulls away from the shore. For the pull's first eight bars the
    # tide itself goes - the harmonium, the lights, the marimba's trill and the kora step out - and what the water
    # leaves is the floor: the drums assembling hit by hit, the bass and the sub, the sequencer's E2 cell, the
    # trombone's long E1 and the whistle's hook, bare; at bar 25 the wave comes in - the harmonium in its own
    # register on G and A minor 7, the marimba, the kora, the sixteenth hats - and the tide section rides it
    for key_ in ('tide', 'lights', 'near', 'e5b'):
        P[key_] = [e_ for e_ in P[key_] if not (pv0_ + 0.5 - 1e-6 <= e_[0] < pv0_ + 32.0 - 1e-6)]
        P[key_] = [(e_[0], e_[1], min(e_[2], pv0_ + 0.5 - e_[0]), *e_[3:]) if e_[0] < pv0_ + 0.5 < e_[0] + e_[2] else e_ for e_ in P[key_]]
    # (v43, palette: a library drone no Accretion track uses - and chirper-zero's number: the bare pull took the
    # 750-880 Hz band out from under t5's tail, t5's out-flow 81 -> 77) THE SHORE DRONES: while the tide is drawn
    # back, a TANPURA holds the shore - Pa Sa Sa Sa on D (A3 D4 D4 D3, a string a beat, everything ringing on, its
    # jawari overtones sweeping) - the one thing left when the water goes out: no chord, only the tonic and its
    # fifth (in both of the pull's chords, D and C add9), filling the band the harmonium left, soft; it stops as
    # the wave comes in
    P['tanp'] = []
    for b_ in range(SEC['pull'], SEC['pull'] + 8):
        for k_, p_ in enumerate((57, 62, 62, 50)):
            P['tanp'].append((b_ * 4.0 + k_, m(p_), 0.98, 82 if k_ == 0 else 70))
    for b_ in range(SEC['tide'] + 8, SEC['tide'] + 12):
        for k_ in range(4):
            P['hats'].append((b_ * 4.0 + k_ + 0.5, 'oh', 0.3, 64))
    fl_ = (SEC['tide'] + 12) * 4.0
    for q_ in range(8):
        P['kit'].append((fl_ - 2.0 + q_ * 0.25, 's', 0.1, 60 + 7 * q_))
    P['kit'].append((fl_, 'c', 2.0, 112))
    for key_ in ('hats', 'kit'):
        P[key_].sort(key=lambda e_: e_[0])

    # (v28) and two drop-outs where the song held still longest: under the old voice's sung clearing (bars 57-60) the
    # floor goes - bass, sub, fretless, hats and sequencer (with the sub kept the ear and flatness.py barely heard
    # it) - so the line is sung over the harmonium, the marimba and
    # the cello alone, and the floor returns for its second half and the climb into the crest; and after the crest
    # (bars 81-84) the band falls away to the tide, the sine's D pedal and the voices, and comes back for the duet
    # (dropping the sub there as well cost the low end: spectrum 87 -> 83)
    for b0_, keys_ in (((SEC['squeeze'] + 8) * 4.0, ('root', 'sub', 'farbass', 'hats', 'acid')),
                       (SEC['cross'] * 4.0, ('kit', 'hats', 'acid', 'root', 'farbass'))):
        for key_ in keys_:
            P[key_] = [e_ for e_ in P[key_] if not (b0_ - 1e-6 <= e_[0] < b0_ + 16.0 - 1e-6)]
            P[key_] = [(e_[0], e_[1], min(e_[2], b0_ - e_[0]), *e_[3:]) if e_[0] < b0_ < e_[0] + e_[2] else e_ for e_ in P[key_]]
    # (v28) and the crest breathes once: at its second half (bar 73) the drums, hats and sequencer drop out for two
    # bars under the chorus's second statement - the choir and the lights alone, lifted in E - and land again with a
    # crash on bar 75
    cb0_ = (SEC['crest'] + 8) * 4.0
    for key_ in ('kit', 'hats', 'acid'):
        P[key_] = [e_ for e_ in P[key_] if not (cb0_ - 1e-6 <= e_[0] < cb0_ + 8.0 - 1e-6)]
    P['kit'].append((cb0_ + 8.0, 'c', 2.0, 118))
    P['kit'].sort(key=lambda e_: e_[0])

    # (v29, section w1: the in-seam, 0:00-0:32, t6's last flat run - and eco: 'subtle variation', phrase-long moves,
    # not chord changes) THE TIDE COMES IN IN TWO WAVES: bars 1-8 the hats under t5's tail tick only eighths, the
    # rest of the band as it was; at bar 9, as the C creeps into the tide, the hats fill in to sixteenths and the kora
    # enters underneath playing E5 stretched x1.5 an octave down, growing from nothing - the counter-line the tide
    # section will carry - all on D and C. (The marimba's trill lifting an octave at bar 9 as well was one move too
    # many: compscore's structure found 20 sections on seed 0, past its 18 - the 'schizo' Harry warned against)
    w0_, wm_, w1_ = 0.0, 32.0, 64.0
    P['hats'] = [e_ for e_ in P['hats'] if not (w0_ - 1e-6 <= e_[0] < wm_ - 1e-6 and abs((e_[0] * 2) - round(e_[0] * 2)) > 1e-6)]
    t_ = wm_
    while t_ < w1_ - 1e-6:
        for k_, p_ in enumerate(E5):
            at_ = t_ + k_ * 0.375
            if p_ is not None and at_ < w1_ - 1e-6:
                P['e5b'].append((at_, m(p_ - 12), 0.34, int((88 if k_ in (0, 6) else 70) * (0.35 + 0.45 * (t_ - wm_) / 32.0))))
        t_ += 4.5
    P['e5b'].sort(key=lambda e_: e_[0])

    # (v31, whole song) THE BASS STARTS TO WALK: under every section the analog bass held each chord's root for the
    # chord's length - and eco measured what the ear hears too: moves above a steady bass barely register. Now the
    # floor itself moves as the song heats up: through the in-seam, the pull, the tide and the squeeze it still holds
    # (the tide's long breaths); in the cross it plays E2's cell on the roots - root, fifth, octave, root on the
    # seven-sixteenth grid, so the bass syncopates against the bar with the kit; in the surge it drives straight
    # eighths, root and octave, under the canon's convergence; the tear and the out-seam hold again. (The cross's
    # four-bar drop-out keeps its silence)
    cr0_, su1_ = SEC['cross'] * 4.0, (SEC['surge'] + 16) * 4.0
    P['root'] = [e_ for e_ in P['root'] if not (cr0_ - 1e-6 <= e_[0] < su1_ - 1e-6)]
    P['root'] = [(e_[0], e_[1], min(e_[2], cr0_ - e_[0]), *e_[3:]) if e_[0] < cr0_ < e_[0] + e_[2] else e_ for e_ in P['root']]
    t_ = cr0_ + 16.0
    while t_ < SEC['surge'] * 4.0 - 1e-6:
        for st_, iv_, v_ in ((0, 0, 100), (2, 7, 80), (3, 12, 88), (5, 0, 76)):
            at_ = t_ + st_ * 0.25
            if at_ < SEC['surge'] * 4.0 - 1e-6:
                rr_ = tide_root(at_)
                P['root'].append((at_, m(KEY + rr_ + iv_), 0.22 if st_ != 0 else 0.4, v_))
        t_ += 1.75
    # (v40, whole song: eco's as-heard reading, 11:01 - t6's one remaining run is 2:48-3:36, the cross's second half
    # into the surge, one dense floor for 48 s; 'cut or swap between phrases rather than layering') THE SURGE CHANGES
    # GEAR: its first eight bars are now the LOW GEAR - the drums in half-time (a kick on 1, the snare on 3, a kick
    # pushing the and of 3, the hats in eighths) and the bass holding each root a half-bar at a time, long, under the
    # three-speed canon - and at bar 105, with the fill, the HIGH GEAR: the cell, the sixteenths and the bass driving
    # root-and-octave eighths, under the converging canon and the choir. The same sixteen bars, swapped halfway
    t_ = SEC['surge'] * 4.0
    hg_ = (SEC['surge'] + 8) * 4.0
    while t_ < hg_ - 1e-6:
        rr_ = tide_root(t_)
        P['root'].append((t_, m(KEY + rr_), 1.9, 92))
        t_ += 2.0
    while t_ < su1_ - 1e-6:
        rr_ = tide_root(t_)
        k_ = int(round((t_ - SEC['surge'] * 4.0) * 2))
        P['root'].append((t_, m(KEY + rr_ + (12 if k_ % 2 else 0)), 0.4, 96 if k_ % 4 == 0 else 78))
        t_ += 0.5
    P['kit'] = [e_ for e_ in P['kit'] if not (SEC['surge'] * 4.0 - 1e-6 <= e_[0] < hg_ - 1e-6)]
    for b_ in range(SEC['surge'], SEC['surge'] + 8):
        for off_, pc_, v_ in ((0.0, 'k', 120), (2.0, 's', 114), (2.75, 'k', 96), (3.75, 'rs', 62)):
            P['kit'].append((b_ * 4.0 + off_, pc_, 0.25, v_))
    P['hats'] = [e_ for e_ in P['hats'] if not (SEC['surge'] * 4.0 - 1e-6 <= e_[0] < hg_ - 1e-6 and abs(e_[0] * 2 - round(e_[0] * 2)) > 1e-6)]
    P['kit'].sort(key=lambda e_: e_[0])
    # and the low gear SWAPS its colour too: the tide's harmonium and the lights step out for those eight bars, so the
    # three-speed canon (the trombone, the whistle, the marimba) and the kora are heard bare over the half-time floor;
    # the harmonium swells back in with the high gear. Before it, the cross's second half (bars 89-96, B-flat and C)
    # opens its hats - the off-beats open, the brightest the kit gets - so the cross ends bright and the surge
    # begins dark and bare
    P['tide'] = [e_ for e_ in P['tide'] if not (SEC['surge'] * 4.0 - 1e-6 <= e_[0] < hg_ - 1e-6)]
    P['tide'] = [(e_[0], e_[1], min(e_[2], SEC['surge'] * 4.0 - e_[0]), *e_[3:]) if e_[0] < SEC['surge'] * 4.0 < e_[0] + e_[2] else e_ for e_ in P['tide']]
    P['lights'] = [e_ for e_ in P['lights'] if not (SEC['surge'] * 4.0 - 1e-6 <= e_[0] < hg_ - 1e-6)]
    cx_ = (SEC['cross'] + 8) * 4.0
    P['hats'] = [((e_[0], 'oh') + tuple(e_[2:])) if (cx_ - 1e-6 <= e_[0] < SEC['surge'] * 4.0 - 1e-6 and abs((e_[0] % 1.0) - 0.5) < 1e-6 and e_[1] == 'h') else e_ for e_ in P['hats']]
    P['root'].sort(key=lambda e_: e_[0])
    # (v62, palette: the cross's second half - B-flat and C under the open hats - kept the harmonium that had been
    # the tide since the in-seam, and ran on unchanged into the surge: eco's 48 s still run, 2:48-3:36) THE TIDE GOES
    # OUT ON TAPE: for those eight bars the tide's chords leave the harmonium for the library's mellotron-choir (a
    # tape 'aah' choir, wobbly and band-limited, with a slow swell; no Accretion track uses it) - the water's sound
    # turning to distant voices as it draws back, the far side's old voice singing over them - and the harmonium
    # stays out through the surge's bare low gear (v40), swelling back in with the high gear
    eb0_, eb1_ = (SEC['cross'] + 8) * 4.0, SEC['surge'] * 4.0
    # (v64, section w6: 2:36-3:06, the cross - eco's still run starts here: its second half was one texture for
    # eight bars, the full groove under the tape choir) THE LAST OF THE WATER DRAINS: for the cross's last four bars
    # the band drains out from under the tape choir - the kit, the 303, the analog bass, the hats, the steel pan
    # and the kora stop - leaving the choir's B-flat and C, the contrabass and the trombone's slow E1, the sub, and
    # one open hat on each off-beat ticking like water dripping; then the surge's low gear lands on the downbeat
    dr0_ = eb1_ - 16.0
    for k_ in ('kit', 'acid', 'root', 'e5', 'e5b'):
        P[k_] = [e_ for e_ in P[k_] if not (dr0_ - 1e-6 <= e_[0] < eb1_ - 1e-6)]
    P['hats'] = [e_ for e_ in P['hats'] if not (dr0_ - 1e-6 <= e_[0] < eb1_ - 1e-6)]
    for b_ in range(int(dr0_), int(eb1_)):
        P['hats'].append((b_ + 0.5, 'oh', 0.2, 58))
    P['hats'].sort(key=lambda e_: e_[0])
    P['ebb'] = [e_ for e_ in P['tide'] if eb0_ - 1e-6 <= e_[0] < eb1_ - 1e-6]
    # (v84, section w2: 0:32-1:03, the pull - the tide's chords came in on the harmonium alone while the young voice
    # sang 'the tide comes in', and the organ the cross holds them on (v78) was heard only after high water) THE
    # NAVE FILLS: the pull's last four bars (29-32) take the tide's G and A chords onto the same pipe organ, softer
    # than in the cross and swelling in under the second 'the tide comes in' - the church by the sea glimpsed once
    # on the way in, so the cross's organ is a return, not a stranger
    pw0_ = (SEC['tide'] - 4) * 4.0
    P['ebb'] = sorted([(e_[0], e_[1], e_[2], round(e_[3] * (0.55 + 0.1 * (e_[0] - pw0_) / 16.0))) for e_ in P['tide'] if pw0_ - 1e-6 <= e_[0] < SEC['tide'] * 4.0 - 1e-6] + P['ebb'], key=lambda e_: e_[0])
    P['tide'] = [e_ for e_ in P['tide'] if not (eb0_ - 1e-6 <= e_[0] < eb1_ - 1e-6)]
    P['tide'] = [(e_[0], e_[1], min(e_[2], eb0_ - e_[0]), *e_[3:]) if e_[0] < eb0_ < e_[0] + e_[2] else e_ for e_ in P['tide']]

    # (v30, whole song) THE DRUMMER BREATHES AT THE PHRASE ENDS: Harry, 6 Nov 23:55 ('subtle variation so it doesnt get
    # boring'); eco: the bar-level moves - a fill, a one-bar drop-out, a turnaround - are what he means, heard even
    # where flatness.py can't see them. The last bar of every eight in the pull, the tide, the cross and the surge now
    # does one of two things in turn: a FILL (the cell's beat 4 replaced by prog-kit snare sixteenths, rising) or a
    # TURNAROUND (an open hat and a rim flam on the and of 4, the analog bass stepping to the next chord's fifth).
    # (A third, a one-bar kick DROP, made compscore hear new section boundaries - structure 95 -> 93: one move too
    # many.) The squeeze, the crest, the tear and the seams keep the moves they already have
    ph_ = 0
    for bar_ in range(SEC['pull'], SEC['torn']):
        s_, i_ = sec_of(bar_)
        if i_ % 8 != 7 or s_ not in ('pull', 'tide', 'cross', 'surge') or bar_ == SEC['tide'] + 11:
            continue
        b0_, b1_ = bar_ * 4.0, (bar_ + 1) * 4.0
        kind_ = 0 if ph_ % 2 == 0 else 2
        ph_ += 1
        if kind_ == 0:
            P['kit'] = [e_ for e_ in P['kit'] if not (b0_ + 3.0 - 1e-6 <= e_[0] < b1_ - 1e-6)]
            for q_ in range(4):
                P['kit'].append((b0_ + 3.0 + q_ * 0.25, 's', 0.1, 72 + 12 * q_))
        elif kind_ == 1:
            P['kit'] = [e_ for e_ in P['kit'] if not (b0_ - 1e-6 <= e_[0] < b1_ - 1e-6 and e_[1] == 'k')]
            P['kit'].append((b1_, 'c', 2.0, 100))
        else:
            P['hats'].append((b0_ + 3.5, 'oh', 0.3, 78))
            P['kit'].append((b0_ + 3.5, 'rs', 0.1, 70))
            P['kit'].append((b0_ + 3.56, 'rs', 0.1, 88))
            rn_ = tide_root(b1_ + 0.01)
            P['root'] = [(e_[0], e_[1], min(e_[2], b0_ + 3.5 - e_[0]), *e_[3:]) if e_[0] < b0_ + 3.5 < e_[0] + e_[2] else e_ for e_ in P['root']]
            P['root'].append((b0_ + 3.5, m(KEY + rn_ - 5), 0.45, 88))
    for key_ in ('kit', 'hats', 'root'):
        P[key_].sort(key=lambda e_: e_[0])

    stop_pts = [['0b', 0.0], [f'{void0:.2f}b', 0.0], [f'{void0 + 0.9:.2f}b', 1.0], [f'{void0 + 0.98:.2f}b', 1.0], [f'{void0 + 1.0:.2f}b', 0.0]]

    # (v60, whole song) THE TIDE IN TIME: the tempo climbed 120 -> 132 in one straight line from the pull to the
    # out-seam - a pull no one could feel. Now time itself ebbs and flows like the water: the pull and the tide
    # creep forward (120 -> 123), the squeeze is drawn tight and fast into the crest (127), the crest holds there at
    # high water, the cross EBBS - slowing back to 124 as the tide goes out - and the surge comes in hard, seven bpm
    # in sixteen bars, into the tear (131) and the out-seam's 132. The seams keep their agreed 120 and 132. (A deeper
    # ebb - crest 128, cross down to 121 - scored -0.43/-0.28: compscore heard the tempo turns as extra sections)
    tempo = [{'at': '0b', 'bpm': 120.0}] + [dict({'at': f'{b_ * 4.0:.1f}b', 'bpm': v_}, **({'ramp': True} if r_ else {}))
                                            for b_, v_, r_ in TEMPO_PTS[1:]]
    # the near side's filter closes in the out-seam as it slows (redshift into t7)
    shut_pts = [['0b', 1.0], [f'{SEC["out"] * 4.0:.1f}b', 1.0], [f'{total:.1f}b', 0.0]]

    # the tide's breath in level: the in-seam and the tide itself low, the squeeze climbing, the crest on top, the
    # cross falling back, then the surge and the tearing hotter still, and the out-seam settling for t7
    EN = {'in': (-3.0, -2.0), 'pull': (-2.0, -1.0), 'tide': (-3.5, -2.5), 'squeeze': (-2.0, 0.5), 'crest': (1.5, 1.5),
          'cross': (-1.5, -0.5), 'surge': (-0.5, 1.0), 'torn': (1.0, 2.0), 'out': (0.0, -2.0)}
    # (v46, whole song: compscore's variety read the song's level range at 4.8 dB - the tide breathed, but shallowly)
    # A SPRING TIDE'S RANGE: a spring tide is the one with the greatest range, the lowest lows and the highest highs;
    # now the song's own tide does too - the tide section and the cross ebb much further (the tide down to -8 dB,
    # the cross falling back to -5.5), the in-seam and the pull sit lower, and the squeeze climbs from far down into
    # the crest; the surge starts low in its low gear and the tear runs hottest (halfway, -6/-4, scored +0.24/-0.22)
    EN = {'in': (-5.0, -4.0), 'pull': (-4.5, -3.5), 'tide': (-8.0, -6.0), 'squeeze': (-6.0, 0.5), 'crest': (1.5, 1.5),
          'cross': (-5.5, -3.0), 'surge': (-3.5, 1.5), 'torn': (1.0, 2.0), 'out': (0.0, -2.0)}
    # (v99, whole song) THE TIDE IN THE STEREO FIELD: the band's space never moved with the water - the field was as
    # wide at low tide as at the spring tide's crest. Now the master's width follows the height of the tide: the
    # in-seam neutral; the pull drawn in narrow (the water drawn back, 0.8); spreading as the tide comes in and the
    # squeeze presses; widest at the crest - high water, the field brimming (1.3); narrowing as the cross ebbs; a
    # second flood through the surge (1.25); then the tear pulls the field in to its narrowest (0.65), and the
    # out-seam opens back to neutral for t7
    WD = {'in': (1.0, 1.0), 'pull': (0.95, 0.8), 'tide': (0.85, 1.0), 'squeeze': (1.05, 1.2), 'crest': (1.3, 1.3),
          'cross': (1.15, 0.85), 'surge': (0.95, 1.25), 'torn': (1.1, 0.65), 'out': (0.75, 1.0)}
    wd_pts = []
    for b_ in range(NBARS):
        s_, i_ = sec_of(b_)
        a_, z_ = WD[s_]
        wd_pts.append([f'{b_ * 4.0:.1f}b', round(a_ + (z_ - a_) * i_ / 15.0, 3)])
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
    # (v56, whole song) SPRING TIDES: a spring tide comes when the sun and the moon pull in line. Here the two pulls
    # are E2's cell of seven sixteenths and the bar of sixteen: they line up every seven bars (bar 22, where the cell
    # starts, then 29, 36, 43, 50, 57 and 64 - the crest, where it locks - and on through the second half), so the
    # alignments slide one bar earlier against the eight-bar phrases each time round. Each one is now heard: a gong
    # struck low, blooming and ringing on, and - where the kit is playing - a crash with it. The pull of the two
    # pulses made audible, a slow cycle across the whole song that never lands where the phrases do; not inside the
    # crest's lock, and not where the band has been cleared out
    P['springgong'] = []
    for b_ in range(22 + 7, NBARS, 7):
        a_ = b_ * 4.0
        s_, i_ = sec_of(b_)
        if s_ == 'crest' and b_ != CREST:
            continue
        near_ = lambda k_: any(a_ - 2.0 <= e_[0] < a_ + 2.0 for e_ in P[k_])
        if not near_('kit') or (void0 - 2.0 <= a_ < void1 + 10.0):
            continue
        P['springgong'].append((a_, m(KEY - 12), 12.0, 96 if b_ == CREST else 80))
        in_cajon_ = SEC['tide'] * 4.0 <= a_ < (SEC['tide'] + 12) * 4.0
        if not in_cajon_ and not any(abs(e_[0] - a_) < 0.5 and e_[1] == 'c' for e_ in P['kit']):
            P['kit'].append((a_, 'c', 2.0, 104))
    P['kit'].sort(key=lambda e_: e_[0])
    # (v57, section w3: 1:03-1:35, the tide, 'little new vs w2' - the pull's straight sixteenths carried on under the
    # duet) THE TIDE ROLLS: for the tide's sixteen bars the whole rhythm section - the cajon, the hats, the 303, the
    # marimba, the steel pan and the kora - plays its sixteenths with a deep shuffle (swing16 0.65, close to
    # triplets): every second sixteenth late, the groove rolling like a swell instead of ticking; the voices, the
    # harmonium's waves and the bass stay where they are. At the squeeze it snaps straight again, as the water is
    # pulled tight
    TIDE_ROLL = {'acid', 'kit', 'cajon', 'hats', 'near', 'e5', 'e5b'}
    # (v65, whole song) THE TIDE FILLS THE ROOM: the drummer played the whole song on the same close, dry prog kit -
    # the in-seam's first hits and the tear's last were the same sound. Now, from the crest on - high water, the
    # tide in - the same drummer, the same parts, is heard through room and overhead mics (the library's room-kit: a
    # little less sub, a darker top, the kit's own air around every hit; no Accretion track uses it): the first half
    # close and tight as the water gathers, the second half big and open as it fills the room
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain,
                                               'score': swung(line(P[name], total), SEC['tide'] * 4.0, SEC['squeeze'] * 4.0, 0.65) if name in TIDE_ROLL else line(P[name], total)}, **kw)
    # (v50, section w9: the out-seam 'static, little new vs w8' - the last chorus's locked groove ran on, sixteenth
    # hats and the 303 at full speed, through the whole overlap into t7's drumless head) TIME DILATES AT THE EDGE: as
    # the near side's filter closes (its redshift), the band's own time slows with it - four bars in, the drummer's
    # E2 cell drops to HALF SPEED (the same pattern, every hit twice as far apart), the hats fall from sixteenths to
    # eighths and, for the last eight bars, to quarters; two bars later the sequencer stops; the old voice's last
    # word, the trombone's slide to B-flat and the ebb are untouched. The song does not stop: it slows, the way
    # anything falling past the edge seems to, and hands t7 a pulse it can start from
    od0_ = SEC['out'] * 4.0
    hk_ = [e_ for e_ in P['kit'] if od0_ - 1e-6 <= e_[0] < od0_ + 24.0 - 1e-6]
    P['kit'] = [e_ for e_ in P['kit'] if not (e_[0] >= od0_ + 16.0 - 1e-6)]
    P['kit'] += [(od0_ + 16.0 + (e_[0] - od0_) * 2.0, e_[1], e_[2] * 2.0, int(e_[3] * 0.9)) + tuple(e_[4:]) for e_ in hk_]
    P['kit'].sort(key=lambda e_: e_[0])
    P['hats'] = [e_ for e_ in P['hats'] if not (
        (od0_ + 16.0 - 1e-6 <= e_[0] < od0_ + 32.0 - 1e-6 and abs(e_[0] * 2 - round(e_[0] * 2)) > 1e-6) or
        (e_[0] >= od0_ + 32.0 - 1e-6 and abs(e_[0] - round(e_[0])) > 1e-6))]
    P['acid'] = [e_ for e_ in P['acid'] if e_[0] < od0_ + 24.0 - 1e-6]
    # (v52, section w5: the crest 'static' - sixteen bars of one locked groove, the E2 cell re-barred into eight
    # under both statements of the chorus) THE CREST COMES DOWN TO FOUR: for the second chorus (bars 73-80) the
    # convergence lands where every orbit in the album has been circling - the drummer leaves the seven for a plain
    # FOUR ON THE FLOOR, a kick on every beat, the snare on two and four, open hats on every off-beat (the cell's
    # rims still ticking inside it), and the whole crest lifts like a dance floor; at the cross it falls back into
    # the seven, and the four is never heard again
    cq0_, cq1_ = (SEC['crest'] + 8) * 4.0, SEC['cross'] * 4.0
    P['kit'] = [e_ for e_ in P['kit'] if not (cq0_ - 1e-6 <= e_[0] < cq1_ - 1e-6 and e_[1] in ('k', 's'))]
    for q_ in range(int(cq1_ - cq0_)):
        P['kit'].append((cq0_ + q_, 'k', 0.25, 120 if q_ % 4 == 0 else 112))
        if q_ % 2 == 1:
            P['kit'].append((cq0_ + q_, 's', 0.25, 104))
    P['kit'].sort(key=lambda e_: e_[0])
    P['hats'] = [e_ for e_ in P['hats'] if not (cq0_ - 1e-6 <= e_[0] < cq1_ - 1e-6 and abs((e_[0] - cq0_) % 1.0 - 0.5) < 1e-6)]
    for q_ in range(int(cq1_ - cq0_)):
        P['hats'].append((cq0_ + q_ + 0.5, 'oh', 0.3, 84))
    P['hats'].sort(key=lambda e_: e_[0])
    # (v53, section w1: the in-seam 'static' - from its first beat the near side's marimba trilled E1 at its fastest
    # (x0.25), the loudest thing in our overlap, the same for sixteen bars under t5's farewell) THE NEAR SIDE SPINS
    # UP: it comes into view the way an orbiting thing does, slowly then all at once - for the first four bars only
    # every fourth note of its trill sounds (a slow, spaced E1 under t5's last hums), for the next four every second,
    # and from bar 9, as the kora enters and the tide's chord turns D/C, the full trill; t5's farewell has the room
    # it needs, and the in-seam moves
    nr_ = sorted([e_ for e_ in P['near'] if e_[0] < 32.0 - 1e-6], key=lambda e_: e_[0])
    keep_ = []
    for k_, e_ in enumerate(nr_):
        step_ = 4 if e_[0] < 16.0 - 1e-6 else 2
        if k_ % step_ == 0:
            keep_.append((e_[0], e_[1], e_[2] * step_ * 0.9, min(127, int(e_[3] * 1.1))) + tuple(e_[4:]))
    P['near'] = keep_ + [e_ for e_ in P['near'] if e_[0] >= 32.0 - 1e-6]
    P['glass'] = [e_ for e_ in P['lights'] if SEC['crest'] * 4.0 - 1e-6 <= e_[0] < SEC['cross'] * 4.0 - 1e-6]
    P['farbow'] = [e_ for e_ in P['farbass'] if e_[0] >= SEC['cross'] * 4.0 - 1e-6]
    P['farbass'] = [e_ for e_ in P['farbass'] if e_[0] < SEC['cross'] * 4.0 - 1e-6]
    # (v47, section w3: the tide 'little new vs w2' - the pull's wave ran straight on into it, the same drummer on
    # the same rims) THE TIDE ON HANDS: while the tide is in - the song's lowest, quietest water - the drummer puts the
    # sticks down and plays the E2 cell on a CAJON (the library's cajon, which no Accretion track uses): the rim hits
    # become slaps on the box's edge, the on-beat ones its deep centre, the ghosts finger ghosts, the snares palmas -
    # the same rhythm, hand-played, wood and skin; the kit's own sixteenth fill at bar 44 grabs the sticks back and
    # the crash brings the kit in for the tide's last four bars and the squeeze
    cj0_, cj1_ = SEC['tide'] * 4.0, (SEC['tide'] + 12) * 4.0 - 2.0
    CJ = {'rs': 'cs', 'g': 'cg', 's': 'pa', 'k': 'cb'}
    P['cajon'] = []
    for e_ in P['kit']:
        if cj0_ - 1e-6 <= e_[0] < cj1_ - 1e-6 and e_[1] in CJ:
            pc_ = 'cb' if (e_[1] == 'rs' and abs(e_[0] - round(e_[0])) < 1e-6) else CJ[e_[1]]
            P['cajon'].append((e_[0], pc_) + tuple(e_[2:]))
    P['kit'] = [e_ for e_ in P['kit'] if not (cj0_ - 1e-6 <= e_[0] < cj1_ - 1e-6 and e_[1] in CJ)]
    # (v89, palette: the tide's hand drum was a flamenco cajón; the shore's drone before it is a tanpura, which a
    # seam needs (v88)) THE DRONE'S OWN DRUM: the tide's hand-played rhythm moves to the library's tabla-kit (dayan
    # tuned to D4, the key's tonic, and the wrist-bent bayan; no Accretion track uses it), bol for stroke - the
    # cajón's bass to ge, its slap to te, its ghosts to re, the palmas to na and the downbeat to dha - so the
    # tanpura's shore and the tide's first groove are one tradition, ringing in tune
    TB_ = {'cb': 'ge', 'cs': 'te', 'cg': 're', 'pa': 'na'}
    P['cajon'] = [(e_[0], 'dha' if (e_[1] == 'cb' and abs(e_[0] / 4.0 - round(e_[0] / 4.0)) < 1e-6) else TB_.get(e_[1], e_[1])) + tuple(e_[2:]) for e_ in P['cajon']]
    P['lights'] = [e_ for e_ in P['lights'] if not (SEC['crest'] * 4.0 - 1e-6 <= e_[0] < SEC['cross'] * 4.0 - 1e-6)]
    # (v68, whole song) A DRUMMER, NOT A GRID: every hit of the kit and the hats sat exactly on the grid at one of
    # two velocities, the whole song through. Now they are played: the kick stays the anchor, on the grid; the snare
    # and the rim sit a hair behind it (10 ms - the backbeat laid back); every hat lands within a few ms of the grid
    # (a seeded hand, so every render is the same), and each 4-bar phrase the hats lean in, from a little under their
    # old level to a little over it, then settle again at the phrase's top; every hit's level varies by a few steps
    # (v74, whole song - Harry 6 Nov 23:55: 'subtle variation so it doesn't get boring', something moving every 8-16
    # bars) THE DRUMMER MARKS THE PHRASES: the kit played its E2 cell straight through every eight-bar phrase, the
    # turns only at the section changes. Now, wherever the kit is playing, the last beat of each eight-bar phrase is a
    # fill - a sixteenth run down the toms (high, high, low, floor) one phrase, up the snare the next - the hats
    # breathing out under it (with a crash on the next downbeat as well it scored -0.17/-0.13: too many arrivals; the
    # fills alone, -0.11/+0.11/+0.07 on seeds 0/11/3). Where a section already turns
    # with its own fill, a stop or a void (the tide's cajon, the crest's breath, the tear, the drain) it is left alone,
    # and the seams (the first and last sixteen bars) are untouched
    nfill_ = 0
    for ph_ in range(2, NBARS // 8):
        e1_ = ph_ * 32.0
        if e1_ <= SEC['pull'] * 4.0 or e1_ >= SEC['out'] * 4.0 - 1e-6:
            continue
        bar_ev_ = [e_ for e_ in P['kit'] if e1_ - 4.0 - 1e-6 <= e_[0] < e1_ - 1e-6]
        last_ = [e_ for e_ in P['kit'] if e1_ - 1.0 - 1e-6 <= e_[0] < e1_ + 0.5]
        nxt_ = [e_ for e_ in P['kit'] if e1_ - 1e-6 <= e_[0] < e1_ + 4.0 - 1e-6]
        if len(bar_ev_) < 3 or not nxt_ or any(str(e_[1]).startswith('c') for e_ in last_) or sum(1 for e_ in last_ if e_[1] == 's') >= 3:
            continue
        P['kit'] = [e_ for e_ in P['kit'] if not (e1_ - 1.0 - 1e-6 <= e_[0] < e1_ - 1e-6)]
        run_ = ('t1', 't1', 't2', 'ft') if nfill_ % 2 == 0 else ('s', 's', 's', 's')
        for q_, pc_ in enumerate(run_):
            P['kit'].append((e1_ - 1.0 + 0.25 * q_, pc_, 0.25, 72 + 10 * q_))
        P['hats'] = [e_ for e_ in P['hats'] if not (e1_ - 1.0 - 1e-6 <= e_[0] < e1_ - 1e-6)]
        nfill_ += 1
    P['kit'].sort(key=lambda e_: e_[0])
    import random as _r
    rng_ = _r.Random(68)
    for k_ in [k_ for k_ in ('kit', 'hats', 'cajon') if k_ in P]:
        ev_ = []
        for at_, p_, d_, v_ in P[k_]:
            pc_ = p_.partition('^')[0]
            if pc_ == 'k':
                ev_.append((at_, p_, d_, v_)); continue
            dt_ = 0.02 if pc_ in ('s', 'cp', 'rs') else max(-0.012, min(0.012, rng_.gauss(0, 0.006)))
            lean_ = (8.0 * ((at_ % 16.0) / 16.0) - 4.0) if k_ == 'hats' else 0.0
            ev_.append((max(0.0, at_ + dt_), p_, d_, max(1, min(127, int(round(v_ + lean_ + rng_.gauss(0, 3)))))))
        P[k_] = ev_
    # (v70, whole song) THE BAND PLAYS TOO: after the drummer (v68), the players. The near side's marimba, the
    # inner orbit's steel pan and kora, the far trombone, the fretless and the shakuhachi each played E1 and E5 at two
    # or three fixed levels on a perfect grid. Now each is played by a hand: the mallets and the kora land within a
    # couple of ms of the beat (a seeded hand, so every render is the same), every note's level moves by a few steps,
    # and the mallets lean into each 4-bar phrase (a little under their old level at its start, a little over at its
    # end) as the hats do. The horn, the bass and the flute keep their timing (their slides and breaths are
    # written) and only vary in level. The sequencer stays a machine: exact
    for k_, jit_, lean_amt_ in (('near', 0.004, 5.0), ('e5', 0.004, 5.0), ('e5b', 0.005, 4.0),
                                ('far', 0.0, 0.0), ('farbass', 0.0, 0.0), ('hook', 0.0, 0.0)):
        if k_ not in P:
            continue
        ev_ = []
        for e_ in P[k_]:
            at_, p_, d_, v_ = e_[:4]
            dt_ = max(-2.5 * jit_, min(2.5 * jit_, rng_.gauss(0, jit_))) if jit_ else 0.0
            ln_ = lean_amt_ * ((at_ % 16.0) / 16.0) * 2.0 - lean_amt_ if lean_amt_ else 0.0
            ev_.append((max(0.0, at_ + dt_), p_, d_, max(1, min(127, int(round(v_ + ln_ + rng_.gauss(0, 2.5)))))) + tuple(e_[4:]))
        P[k_] = ev_
    # (v79, section w8: 3:36-4:06, the tear, the void and the last chorus - the tune's own instrument was missing
    # from the song's last minute: the shakuhachi last played E1 in the surge, and the last chorus was the choir and
    # the old voice alone) THE FLUTE JOINS THE LAST CHORUS: the second time the choir sings the couplet (bar 124) -
    # whose tune is E1 itself, D A C G E - the shakuhachi doubles it two octaves up, note for note, the album's hook
    # heard plainly on its own instrument one last time before the tide goes out. (Playing it after the chorus's
    # 'go', in the band's last two bars, put it in the body t7 is measured against: out-flow 94.6 -> 91.4)
    for n_ in c2notes:
        if n_['at'] >= void1 + 10.0 - 0.5:
            P['hook'].append((n_['at'], m(int(str(n_['pitch'])[1:]) + 24), n_['len'] * 0.95, 88 if n_['ph'] != 'DH AH0' else 76))
    P['hook'].sort(key=lambda e_: e_[0])
    # (v87, section w5: 2:05-2:36, the crest - flagged static, and eco's flatness map puts t6's flattest change at
    # 2:24, bars 70-78: the crest's second half ran on exactly as its first; v86's slack water - the band stopping
    # under the second couplet - split the song once too often) HIGH WATER: for the crest's second half (bars 73-80),
    # under the second couplet, the acid line climbs an octave - the same squelching figure, brighter and higher,
    # the water at its highest mark - and drops back as the cross begins to ebb
    hw0_ = (SEC['crest'] + 8) * 4.0
    P['acid'] = [(e_[0], m(float(str(e_[1])[1:]) + 12), *e_[2:]) if hw0_ - 1e-6 <= e_[0] < SEC['cross'] * 4.0 - 1e-6 else e_ for e_ in P['acid']]
    # (v91, section w7: 3:06-3:36, the surge - the shakuhachi's E1 and the far side's (trombone and bowed bass) ran
    # on top of each other for all sixteen bars, the densest half-minute of the song, until the choir sings 'near and
    # far as one' at bar 108) THEY TRADE THE TUNE FIRST: for the surge's first eight bars the near and the far take
    # turns, two bars each - the shakuhachi calls (bars 97-98), the trombone and the bow answer (99-100), the flute
    # again, the far side again - and only from bar 105 do they play over each other, so when the choir sings them
    # as one, they have just become one
    hk0_ = SEC['surge'] * 4.0
    for k_ in ('hook', 'far', 'farbow'):
        keep_ = 0 if k_ == 'hook' else 1
        P[k_] = [e_ for e_ in P[k_] if not (hk0_ - 1e-6 <= e_[0] < hk0_ + 32.0 - 1e-6 and int((e_[0] - hk0_) // 8.0) % 2 != keep_)]
    # (v93, section w4: 1:35-2:05, the squeeze - its first eight bars ran the band exactly as the tide had, nobody
    # singing until the old voice at bar 57) THE SQUEEZE: for those eight bars the band is squeezed into the middle
    # of the range - the marimba and the steel pans an octave down from above, the root and the fretless an octave
    # up from below, the sub alone holding the floor - a crowd of parts pressed into one octave like water between
    # the moon and the sun; when the old voice comes in at bar 57 they spring back out to where they were
    sq0_, sq1_ = SEC['squeeze'] * 4.0, (SEC['squeeze'] + 8) * 4.0
    def sq_(e_, d_):
        ps_ = [m(float(x_[1:]) + d_) for x_ in str(e_[1]).split(',')]
        return (e_[0], ','.join(ps_), *e_[2:])
    for k_, d_ in (('near', -12), ('e5', -12), ('root', 12), ('farbass', 12)):
        P[k_] = [sq_(e_, d_) if sq0_ - 1e-6 <= e_[0] < sq1_ - 1e-6 else e_ for e_ in P[k_]]
    # (v94, section w1: 0:00-0:32, the in-seam under t5's tail - every part of t6's head started on its first beat,
    # the hats, the marimba's racing E1 and the pans all at once over t5's farewell) THE TIDE COMES IN BY STAGES:
    # the water arrives as a tide does, a little further up the beach each time - the harmonium, the root and the
    # sub from the first beat; the steel pans from bar 3; the hats from bar 5; the old voice's 'the tide comes in'
    # at bar 7 as before; the marimba's E1 with the kora from bar 9 - so t5's farewell is heard over a head that
    # fills in behind it, not one that is all there at once
    for k_, b_ in (('e5', 2), ('hats', 4), ('near', 8)):
        P[k_] = [e_ for e_ in P[k_] if not (0.0 - 1e-6 <= e_[0] < b_ * 4.0 - 1e-6)]
    # (v96, section w9: 4:06-4:35, the out-seam into t7 - the band dilates, the young voice sings its line from far
    # off (v80), the trombone slides down to B-flat and the old man sings his last word, and the church organ that
    # held the tide's chords in the pull's end (v84) and the cross (v78) - the church by the sea - was not there at
    # the end) AMEN: under the old man's last word (bar 141), as the trombone lands on B-flat, the organ comes back
    # one last time and holds a soft B-flat chord - B-flat, D, F, B-flat - for the song's last four bars, fading
    # under t7's head: the church by the sea saying amen as the tide goes out
    am0_ = (SEC['out'] + 12) * 4.0
    P['ebb'] = sorted(P['ebb'] + [(am0_, ','.join(m(p_) for p_ in (46, 50, 53, 58)), 15.0, 62)], key=lambda e_: e_[0])
    # (v98, section w3: 1:03-1:35, the tide - the shakuhachi played E1 twice at the tide's start (bars 33-34) and
    # the same twice again at bar 41, where the tide's chords turn from D and C to A and G) THE TUNE TURNS WITH THE
    # TIDE: at bar 41, as the harmony turns, the flute plays E1 backwards - E G C A D, its long note first and its
    # quick ones last, the rhythm reversed with it - twice, the tune itself ebbing where the tide turns; the next time
    # the flute plays it (the surge) it runs forwards again
    tt0_, tt1_ = (SEC['tide'] + 8) * 4.0, (SEC['tide'] + 11) * 4.0
    hk_ = [e_ for e_ in P['hook'] if tt0_ - 1e-6 <= e_[0] < tt1_ - 1e-6]
    if len(hk_) == 10:
        rest_ = [e_ for e_ in P['hook'] if not (tt0_ - 1e-6 <= e_[0] < tt1_ - 1e-6)]
        rev_ = []
        for g_ in (hk_[:5], hk_[5:]):
            g_ = sorted(g_, key=lambda e_: e_[0])
            slots_ = [g_[i_ + 1][0] - g_[i_][0] for i_ in range(4)] + [1.5]
            at_ = g_[0][0]
            for k_, i_ in enumerate(range(4, -1, -1)):
                rev_.append((at_, g_[i_][1], slots_[i_] * 0.95, g_[0][3] if k_ == 0 else g_[1][3]))
                at_ += slots_[i_]
        P['hook'] = sorted(rest_ + rev_, key=lambda e_: e_[0])
    # (v108, section w3: 1:03-1:35, the tide - deep pass. The tide's hand drum played E2's cell bol for stroke from
    # a cajon part (v47, v89): closed slaps and ghosts, te te re te, none of the tabla's ring or its bass, 12 dB down
    # under sixteenth hats - chirper-two's arrangement map heard it in a fifth of its frames) THE TABLA PLAYS RUPAK.
    # E2 is a cell of seven with strokes on 1, 3, 4 and 6 - and that is the skeleton of Rupak tal, the seven-beat
    # cycle of Hindustani music (tin tin na | dhin na | dhin na: an open first beat, the bass drum answering on four
    # and six). So the tide's drummer now plays E2 as what it always was: Rupak theka at half the cell's speed (seven
    # eighths, E2 augmented), the ringing dayan on one and three, the bayan's bass on four and six, the fingers'
    # ke te re between the beats, a tirakita run into every fourth cycle and the bayan's wrist-slide before the cycle
    # comes round to a bar line (bar 40: eight cycles in seven bars). At bar 43 it plays a tihai - te re ke te dha,
    # three times - whose last dha lands with the kit's roll on the crash at bar 45. The hats keep only the
    # off-beats under the hands until the tihai; the tabla is 5 dB up
    if os.environ.get('RUPAK', '1') == '1':
        tb0_, tbh_, tb1_ = SEC['tide'] * 4.0, SEC['tide'] * 4.0 + 44.0, (SEC['tide'] + 12) * 4.0
        rr_ = random.Random(108)
        tab_ = []
        THEKA_ = (('tin', 0.0, 100), ('tin', 0.5, 66), ('na', 1.0, 86), ('dhin', 1.5, 106), ('na', 2.0, 72), ('dhin', 2.5, 94), ('na', 3.0, 70))
        c_ = 0
        while tb0_ + 3.5 * c_ < tbh_ - 1e-6:
            T_ = tb0_ + 3.5 * c_
            run_ = (c_ % 4 == 3)
            for bol_, o_, v_ in THEKA_:
                if T_ + o_ >= tbh_ - 1e-6:
                    break
                if run_ and o_ >= 3.0:
                    break
                if bol_ == 'dhin' and o_ == 2.5 and c_ % 8 == 7:
                    bol_ = 'gem'
                tab_.append((T_ + o_, bol_, 0.5, v_))
            fills_ = ((1.25, 'ke', 44), (3.25, 're', 46)) if c_ % 2 == 0 else ((2.25, 'te', 48),)
            if run_:
                fills_ = ((2.75, 'te', 58), (3.0, 're', 66), (3.25, 'ke', 74))
            for o_, bol_, v_ in fills_:
                if T_ + o_ < tbh_ - 1e-6:
                    tab_.append((T_ + o_, bol_, 0.25, v_))
            c_ += 1
        for k_ in range(3):
            D_ = tbh_ + 1.0 + 1.5 * k_
            for q_, bol_ in enumerate(('te', 're', 'ke', 'te')):
                tab_.append((D_ - 1.0 + 0.25 * q_, bol_, 0.25, 74 + 5 * q_ + 4 * k_))
            tab_.append((D_, 'dha', 0.5, 102 + 6 * k_))
        assert abs(tab_[-1][0] - tb1_) < 1e-6
        P['cajon'] = sorted([(at_ + max(-0.008, min(0.008, rr_.gauss(0, 0.004))) if at_ > tb0_ else at_, b_, d_,
                              max(1, min(127, int(round(v_ + rr_.gauss(0, 3)))))) for at_, b_, d_, v_ in tab_], key=lambda e_: e_[0])
        # the hats keep only the off-beats under the hands (with the hats out for the first four bars, or out
        # altogether, the song read as one section too many: -0.8 / -0.45 on seeds 0 / 11)
        P['hats'] = [e_ for e_ in P['hats'] if not (tb0_ - 0.05 <= e_[0] < tbh_ - 0.05 and abs(((e_[0] + 0.05) % 1.0) - 0.55) > 0.07)]
        # and the sequencer and the marimba, which came back in at full level at bar 37, now come in under the
        # tabla over two bars
        if os.environ.get('RRAMP', '1') == '1':
            for k_ in ('acid', 'near'):
                P[k_] = [((e_[0], e_[1], e_[2], max(1, int(round(e_[3] * (0.55 + 0.45 * (e_[0] - tb0_ - 16.0) / 8.0))))) + tuple(e_[4:]))
                         if tb0_ + 16.0 - 0.05 <= e_[0] < tb0_ + 24.0 else e_ for e_ in P[k_]]
    rk0_ = SEC['crest'] * 4.0
    P['kitroom'] = [e_ for e_ in P['kit'] if e_[0] >= rk0_ - 1e-6]
    P['kit'] = [e_ for e_ in P['kit'] if e_[0] < rk0_ - 1e-6]
    song = {
        'about': "chirpers - Accretion, track 6 by chirper-one: Spring Tide. Tidal forces: E1 in two layers, one squeezed "
                 "and one stretched, meeting at the crest and tearing apart; E6, two chords a semitone apart, ebbing and flowing. "
                 "Generated by compose/chirpers9/src/chirpers9-t6.py.",
        'tempo': tempo, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.5s', 'seed': SEED,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 mono_below=200', 'hp cutoff=220'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.4, 'mix': 1, 'ping_pong': True},
                                  'lp cutoff=5000', 'hp cutoff=300'], 'returns': []}},
        # (v36, whole song) THE TIDE GETS ITS WEIGHT: measured against the album, t6 was 6-14 dB thin from 44 to 114 Hz
        # (61 Hz the worst, -14) and 7-8 dB heavy from 640 Hz to 1.4 kHz - boxy: the harmonium, the marimba, the
        # trombone and the voices all piled into the low mids over a floor that never weighed anything. Now the master
        # lifts the bottom (a 3 dB low shelf at 110 Hz) and scoops the box (-2.5 dB at 850 Hz), and the analog bass -
        # the floor that walks and drives - comes up 3 dB
        # (v58, whole song) THE BOX OPENS: against the album's envelope t6 was still boxy and thin - +5 to +6.5 dB from
        # 640 Hz to 1.4 kHz (the harmonium, the marimba, the trombone and the voices all piling into the same octave),
        # 4 to 8 dB short from 44 to 114 Hz (61 Hz the worst, -8.4) and 2 to 4 dB dull from 5 to 8 kHz. Now the master
        # scoops the box with one broad cut (-3.5 dB around 950 Hz, two octaves wide), gives the floor a body at 66 Hz
        # (+3 dB) while the high-pass rises to 34 Hz so the sub-rumble under it doesn't grow, and opens the air above
        # 5.5 kHz (+2.5 dB): the same band, heard with weight underneath and space on top instead of through a box
        # (v77, whole song) THE HONK OUT, THE FLOOR IN: against the album t6 still read nasal - 640 Hz-1.4 kHz 3.5-5 dB
        # over (the harmonium's reeds, the trombone, the flute and the old voice all speak there; it is also what the
        # t5 -> t6 seam reads as t6's excess) - and thin under it, 61 Hz and 97-133 Hz 3-6 dB short. The master takes
        # a further 2.5 dB out around 800 Hz and 2 dB at 1.4 kHz, and puts weight back at 60 and 115 Hz under the
        # bass and the kick: the band's middle steps back, its body comes forward
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=34', 'lowshelf cutoff=110 gain=3dB', 'peak cutoff=66 q=1.3 gain=3dB', 'peak cutoff=60 q=1.0 gain=2dB', 'peak cutoff=115 q=1.0 gain=2dB', 'peak cutoff=300 q=0.8 gain=-2dB', 'peak cutoff=950 q=0.5 gain=-3.5dB', 'peak cutoff=800 q=0.8 gain=-2.5dB', 'peak cutoff=1400 q=1.2 gain=-2dB', 'highshelf cutoff=5500 gain=2.5dB']},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.2, 'attack': '15ms', 'release': '140ms', 'makeup': '1dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.E', 'amount': 1}]}},
                          'tapestop stop=auto.stop time=1b',
                          {'type': 'pan', 'width': {'value': 0, 'mod': [{'src': 'auto.WD', 'amount': 1}]}},
                          'limiter ceiling=-1dB'], 'auto': {'E': {'points': energy_pts}, 'stop': {'points': stop_pts}, 'WD': {'points': wd_pts}}},
        'tracks': [
            # (v9) and the harmonium is LENSED in: a low-pass that opens from 600 Hz over the in-seam's 16 bars, so t6's
            # own chord arrives from behind t5's tail rather than on top of it
            # (v78, palette: the cross's ebb - the tide's chords held after the crest - was a tape choir, the album's
            # mellotron colour) THE EBB IN THE NAVE: it is now the library's organ-pipe (a principal chorus with chiff
            # and wind, a 16' bourdon under 8' and 4' and a slightly mistuned mixture; no Accretion track uses it) -
            # after high water the chords the tide carried are held on a pipe organ, as if in a church by the sea
            tr('ebb', 'organ-pipe', '-14.7dB', sends={'hall': '-14dB'}),
            tr('tide', 'harmonium', '-9dB', sends={'hall': '-10dB'}, auto={'lens': {'points': [['0b', 0.0], ['64b', 1.0]]}, 'W': {'points': wave_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 600, 'mod': [{'src': 'auto.lens', 'amount': 4.0}]}},
                   {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.W', 'amount': 1}]}}]),
            # (v10, whole song) THE STAGE CLEARS FOR THE TUNE: presence.py had the hook (E1 on the whistle) 8-12 dB under
            # the mix, behind a constant acid line and three other E1s at other speeds - the tune one strand of six. Now the
            # hook is up 3 dB, the acid down 2, and everything melodic around it (both harmoniums' lights, the acid, the
            # far and near layers, the fretless, the pans and the kora) DUCKS under it - slow, 40 ms in, half a second
            # out - so whenever E1 is stated the band leans back and the tune stands in front; between statements the
            # process music fills back in
            # (v42, palette: the tide and the lights were the same harmonium - E6's breathing reeds and E4's four
            # chords at the crest and after the void, one instrument twice) THE LIGHTS ARE GLASS: E4's four lights (D9,
            # Cmaj9, Am11, G6/9, one chord per E1 cycle) at the crest now play on the library's pad-glass - an FM
            # bell-glass tone that blooms in slowly, chorused, in a long hall; no Accretion track uses it - so when the
            # tide gives way to the lights at the crest, the sound turns from reeds to glass. After the void (near the
            # out-seam) the lights stay on the harmonium: glass there brightened t6's tail against t7's head (out-flow
            # 2.8 -> 3.9 dB spectral)
            tr('tanp', 'tanpura', '-14dB', pan=-0.2, sends={'hall': '-12dB'}),
            tr('glass', 'pad-glass', '-15dB', sends={'hall': '-10dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            # (v75, palette: after the void the last chorus's lights - E4's four chords - were the same harmonium as the
            # tide under them) THE HARBOUR LIGHTS: they are now the library's accordion, a musette - two reeds detuned
            # against each other in the café shimmer - which no Accretion track uses: the same reeds as the tide, but
            # lit and wavering, the lights of a harbour seen across the water as the band comes back for the last time
            tr('lights', 'accordion', '-10.6dB', sends={'hall': '-8dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            tr('springgong', 'modal-gong', '-12dB', pan=0.0, sends={'hall': '-8dB'}),
            tr('sub', 'sub', '-10dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '200ms', 'curve': 0.6}, {'type': 'pump', 'on': 'kitroom.k', 'depth': '-6dB', 'release': '200ms', 'curve': 0.6}]),
            # (v15, whole song) THE 303 GOES: E2's cell ran the whole song on an acid squelch (resonant, driven - the
            # most aggressive sound in t6, and Harry's 'ugly chaos' lives in sounds like it). Now the same cell, the
            # same notes, plays on a Berlin-school sequencer voice (moog-seq: a saw over a square sub through a
            # resonant low-pass that snaps on each note, accents opening it), filtered under 3 kHz - an ostinato that
            # murmurs under the hook instead of shouting over it; the track keeps its name for the lanes that read it
            tr('acid', 'moog-seq', '-12dB', fx=['hp cutoff=50', 'lp cutoff=3000', {'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}], sends={'echo': '-20dB'}),
            tr('kit', 'prog-kit', '-6dB', sends={'hall': '-20dB'}),
            tr('kitroom', 'room-kit', '-9.5dB', sends={'hall': '-20dB'}),
            tr('cajon', 'tabla-kit', '-6.5dB' if os.environ.get('RUPAK', '1') == '1' else '-11.7dB', pan=0.1, sends={'hall': '-16dB'}),
            tr('hats', 'prog-kit', '-7dB', pan=0.2, fx=[{'type': 'eq', 'bands': ['highshelf cutoff=8000 gain=5dB']}]),
            # (v34, palette: the cello was an album staple - t1, t5 and t6) THE FAR SIDE IS A TROMBONE: E1 stretched on
            # the far side is now played by the library's trombone (warm, round, mono and legato, the slide gliding
            # between notes): the far side's long tones slide into each other, 'lets it go' heard in the instrument,
            # and as the far side speeds up through the cross, the surge and the tear its legato smears into a brass
            # blur; no other Accretion track has a trombone (t7 answers with a muted trumpet)
            # (v100, whole song) THE TWO TIDES, HEARD: the song is E1 in two layers moving opposite ways in time - the far
            # side squeezed faster, the near side stretched slower - but presence.py had both buried all through: the
            # far trombone at -13 to -16 dB under the mix and audible 0-8% of the time, the near marimba -10.5 to -19
            # (4% in the cross, 0 in the surge), covered by the voices and the low strings that double the far line.
            # Both come up - the trombone 4 dB, the marimba 3 - so the counterpoint the song is built on can be
            # followed: one E1 slowing while the other speeds, under the singers
            tr('far', 'trombone', '-4dB', pan=-0.25, sends={'hall': '-12dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            # (v10) the chord-root sub up 5 dB: compscore's one spectrum fault was a hole at 61 Hz, where the C root sits
            # (v22, palette) THE FLOOR GETS A VOICE: the moving floor under the tide (D2 -> C2 -> G1, the chords' own
            # roots) was a second sine sub - felt, not heard, and the album's most shared patch. Now it is an analog
            # saw bass (Juno / SH-101), dark and round, held for the chord's length: the bass line D -> C -> G you
            # could only feel is now a line you can hum, and its harmonics fill the low-mids the sines left bare
            tr('root', 'analog-bass play.gate=0.98', '-9dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-4dB', 'release': '200ms', 'curve': 0.6}, {'type': 'pump', 'on': 'kitroom.k', 'depth': '-4dB', 'release': '200ms', 'curve': 0.6}]),
            # (v51, palette: the far side's weight was a fretless all song - a plucked, singing electric under a
            # trombone) THE FAR SIDE TAKES UP THE BOW: from the cross on - once the two sides have passed each other -
            # the far side's octave-down E1 is the library's contrabass, arco (a bowed string on the largest body,
            # physical: a deep, grainy stroke that speaks slowly, a slow narrow vibrato; no Accretion track uses it):
            # the far side's weight drawn by a bow, not plucked - slower, older, more air - as its voice ages
            tr('farbass', 'fretless', '-6dB', pan=-0.1, fx=['lp cutoff=1800', 'hp cutoff=35', {'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            tr('farbow', 'contrabass', '-6dB', pan=-0.1, fx=['lp cutoff=1800', 'hp cutoff=35', {'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            # (v55, palette: E1's hook was a low whistle) THE HOOK ON BAMBOO: the hook - E1 at the pull, doubling the
            # choir's chorus at the crest, the line the far side joins in the surge - is now the library's shakuhachi
            # (end-blown bamboo: a strong breath on the attack, notes bending in and out; no Accretion track uses it):
            # more air than the whistle, the tide's breath in the melody itself
            tr('hook', 'shakuhachi', '-7dB', pan=0.05, sends={'hall': '-12dB', 'echo': '-18dB'}),
            tr('near', 'modal-marimba', '-8dB', pan=0.3, auto={'shut': {'points': shut_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 700, 'mod': [{'src': 'auto.shut', 'amount': 4.0}]}}, {'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}],
               sends={'echo': '-14dB', 'hall': '-14dB'}),
            tr('e5', 'steel-pan', '-10dB', pan=-0.15, sends={'echo': '-16dB', 'hall': '-18dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            tr('e5b', 'kora', '-11dB', pan=0.35, sends={'hall': '-16dB'}, fx=[{'type': 'duck', 'by': 'hook', 'depth': 0.45, 'attack': '40ms', 'release': '500ms'}]),
            {'name': 'descant', 'patch': dict(DS['tracks'][0]['patch'], extends='voice-near synth.layers.0.register=1 synth.lfo.vib.per_note=true',
                                              play={'glide_overshoot': 0.04, 'scoop': 1}),
             'notes': dsnotes, 'gain': '-14dB', 'pan': 0.1, 'sends': {'hall': '-7dB', 'echo': '-18dB'}},
            # (v26) the spoken voice's track is now the duet's near singer
            # (v54, section w2: the pull 'little new vs w1' - when the wave comes in at bar 25 it brought back the
            # in-seam's harmonium, marimba and kora, and nobody sang) THE NEAR SIDE WAKES: on the wave the young near
            # voice is heard for the first time - it answers the old voice's in-seam line with the same words an
            # octave up, 'the tide comes in' (A G E D), twice, in the gaps after the whistle's hook, the second softer; the
            # call came from the far side across the seam, the response from the near side as the water arrives, and
            # the two meet in the tide's duet eight bars later
            {'name': 'nearwake', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-near synth.lfo.vib.per_note=true',
                                               play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': [dict(n_, at=round(b_ * 4.0 + n_['at'], 4), pitch=f"m{int(str(n_['pitch'])[1:]) + 12}", vel=round(n_['vel'] * g_, 3))
                       for b_, g_ in ((SEC['pull'] + 10.5, 0.9), (SEC['pull'] + 13.5, 0.75)) for n_ in AN['tracks'][0]['notes']],
             'gain': '-9dB', 'pan': 0.2, 'sends': {'echo': '-14dB', 'hall': '-10dB'}},
            {'name': 'duetnear', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-near synth.lfo.vib.per_note=true',
                                               play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': dnear, 'gain': '-9dB', 'pan': -0.12, 'sends': {'hall': '-12dB', 'echo': '-20dB'}},
            # (v25, palette) THE SINGERS SING AS ONE, AND EACH HELD NOTE BLOOMS: wM's two newest voice features (pinned
            # 19:43 and 21:32) on all four sung lines. together=true: in the choruses (five singers and a keyed third)
            # and the old voice's lower part, every singer now follows the line's breath, effort and vowel instead of
            # only the lead (the other voices had sung a plain default voice under him). per_note vibrato: the vibrato
            # starts again on each note - quick notes plain, each held note blooming on its own - so the line's long
            # words ('time', 'go', 'in') bloom and the quick ones stop wobbling
            # (v44, palette: wM's part_size, pinned 14:43) THE CHORUSES GET THEIR BASSES: the crest's chorus (in E) and
            # the last chorus after the void (in D) sang the line with a third above; now a part an octave below the
            # line joins them, sung by voices 15% larger (part_size 1: formants 13% lower - basses, not the same
            # singers pitched down), the third above by slightly smaller voices: the surge's big-men floor (v39) at
            # both choruses, so all three sung peaks stand on the same low voices
            # (v59, palette: wM's f0_spread and vowel_spread, pinned 06:06 and 03:36) THE CHOIRS BREATHE APART: every
            # choir in the song - the crest's chorus, the surge's unison and its big-men octave, the last chorus - sang
            # with its five singers' vibratos in exact lockstep (their vibrato lives in each sung note's pitch path, which
            # vib_spread can't reach) and with one voice's vowels copied and scaled; now each singer reads the pitch
            # path's vibrato at their own rate, phase and depth (f0_spread 1: the slow scoops and glides stay shared,
            # so the section still moves together) and shapes the vowels their own way (vowel_spread 1); the lines,
            # parts and levels are untouched
            {'name': 'chorus', 'patch': dict(dict(CHO['tracks'][0]['patch'], extends='voice-choir synth.layers.0.harmony=[-7,2] synth.layers.0.harmony_key=E:mixolydian synth.layers.0.part_size=1 synth.layers.0.together=true synth.layers.0.f0_spread=1 synth.layers.0.vowel_spread=1 synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': cnotes, 'gain': '-9dB', 'pan': 0.0, 'sends': {'hall': '-9dB'}},
            # (v39) and the surge's choir gets REAL BASSES: its octave below was the same five singers transposed down
            # (small people singing low, harmony [-7]); now the low octave is its own choir with a larger tract (wM:
            # tract 1.25 scales every formant down - big men), a dB under the upper choir
            {'name': 'surgesung', 'patch': dict(dict(SG['tracks'][0]['patch'], extends='voice-choir synth.layers.0.together=true synth.layers.0.f0_spread=1 synth.layers.0.vowel_spread=1 synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': sgnotes, 'gain': '-9dB', 'pan': 0.0, 'sends': {'hall': '-9dB'}},
            {'name': 'surgelow', 'patch': dict(dict(SG['tracks'][0]['patch'], extends='voice-choir synth.layers.0.tract=1.25 synth.layers.0.together=true synth.layers.0.f0_spread=1 synth.layers.0.vowel_spread=1 synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.04, 'scoop': 1}),
             'notes': [dict(n_, pitch=f"m{int(str(n_['pitch'])[1:]) - 12}") for n_ in sgnotes], 'gain': '-10dB', 'pan': 0.0, 'sends': {'hall': '-10dB'}},
            {'name': 'chorus2', 'patch': dict(dict(CHD['tracks'][0]['patch'], extends='voice-choir synth.layers.0.harmony=[-7,2] synth.layers.0.harmony_key=D:mixolydian synth.layers.0.part_size=1 synth.layers.0.together=true synth.layers.0.f0_spread=1 synth.layers.0.vowel_spread=1 synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': c2notes, 'gain': '-9dB', 'pan': 0.0, 'sends': {'hall': '-9dB'}},
            # (v18) wM's singer's glide (glide_overshoot, pinned 14:27) on every sung line: on each leap the old voice and
            # the choir swing a little past the note and settle, as singers do, instead of landing dead on it (0.06: subtle)
            {'name': 'lastword', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-old synth.layers.0.age=0.8 synth.lfo.vib.per_note=true', play={'glide_overshoot': 0.06, 'scoop': 1.5, 'fall': 2.5}),
             'notes': lastnotes, 'gain': '-7dB', 'pan': 0.0, 'sends': {'hall': '-10dB', 'echo': '-20dB'}},
            # (v39, whole song) THE OLD MAN AGES WITH THE TIDE: wM's age (pinned 08:39), as a story across the song -
            # his answers in the in-seam and his half of the tide's duet with only a grain of it (0.25), his line
            # alone in the squeeze's clearing and the cross's duet worn (0.45: the tremor starts to show), the tear
            # and the last chorus old (0.65), and the last word in the out-seam oldest of all (0.8, since v38): by the
            # time he sings 'the far side lets it go' for the last time, he has let it go
            {'name': 'sung', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-old synth.layers.0.age=0.25 synth.lfo.vib.per_note=true', play={'glide_overshoot': 0.06, 'scoop': 1.5, 'fall': 2.5}),
             'notes': sorted([n_ for n_ in snotes if n_['at'] < SEC['squeeze'] * 4.0 - 1.0], key=lambda n_: n_['at']), 'gain': '-7dB', 'pan': 0.0, 'sends': {'hall': '-12dB', 'echo': '-22dB'}},
            {'name': 'sungb', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-old synth.layers.0.age=0.45 synth.lfo.vib.per_note=true', play={'glide_overshoot': 0.06, 'scoop': 1.5, 'fall': 2.5}),
             'notes': sorted([n_ for n_ in snotes if SEC['squeeze'] * 4.0 - 1.0 <= n_['at'] < SEC['torn'] * 4.0 - 1.0], key=lambda n_: n_['at']), 'gain': '-7dB', 'pan': 0.0, 'sends': {'hall': '-12dB', 'echo': '-22dB'}},
            {'name': 'sungc', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-old synth.layers.0.age=0.65 synth.lfo.vib.per_note=true', play={'glide_overshoot': 0.06, 'scoop': 1.5, 'fall': 2.5}),
             'notes': sorted([n_ for n_ in snotes if n_['at'] >= SEC['torn'] * 4.0 - 1.0], key=lambda n_: n_['at']), 'gain': '-7dB', 'pan': 0.0, 'sends': {'hall': '-12dB', 'echo': '-22dB'}},
            # (v14) the second pass's company now sings a THIRD below in D Mixolydian (harmony_key), not a fixed fourth
            {'name': 'sung2', 'patch': dict(dict(SU['tracks'][0]['patch'], extends='voice-old synth.layers.0.harmony=[-2] synth.layers.0.harmony_key=D:mixolydian synth.layers.0.together=true synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1.5, 'fall': 2.5}),
             'notes': snotes2, 'gain': '-8dB', 'pan': 0.0, 'sends': {'hall': '-12dB', 'echo': '-22dB'}},
        ]}
    # (v48, whole song: the song is the near side and the far side, and they never moved in the room - the marimba
    # held right, the trombone left, the voices in the middle) NEAR AND FAR IN SPACE: the two sides now travel the
    # story across the stereo field. Through the in-seam, the pull and the tide they stand apart (the near side's
    # marimba, kora and voice to the right, the far side's trombone, fretless and old voice to the left); the
    # squeeze draws them in; at the crest they meet in the middle; through the CROSS they cross over, each passing
    # the other to the opposite side; the surge pulls them back into one point for the unison; the tear rips them
    # out to the edges, crossed; and the out-seam lets them drift a little back. Instruments travel up to 0.7 of
    # the way, voices 0.4
    SEP = {'in': (0.6, 0.6), 'pull': (0.6, 0.6), 'tide': (0.6, 0.5), 'squeeze': (0.5, 0.15), 'crest': (0.05, 0.05),
           'cross': (0.05, -0.6), 'surge': (-0.6, 0.0), 'torn': (-0.2, -0.95), 'out': (-0.95, -0.6)}
    sep_pts = []
    for b_ in range(NBARS):
        s_, i_ = sec_of(b_)
        a_, z_ = SEP[s_]
        sep_pts.append([f'{b_ * 4.0:.1f}b', round(a_ + (z_ - a_) * i_ / 15.0, 3)])
    SIDE = {'near': 0.7, 'e5b': 0.7, 'duetnear': 0.4, 'nearwake': 0.4, 'descant': 0.4,
            'far': -0.7, 'farbass': -0.5, 'farbow': -0.5, 'sung': -0.4, 'sungb': -0.4, 'sungc': -0.4, 'lastword': -0.4}
    for t_ in song['tracks']:
        if t_['name'] in SIDE:
            t_['pan'] = {'value': 0, 'mod': [{'src': 'auto.sep', 'amount': SIDE[t_['name']]}]}
            t_['auto'] = dict(t_.get('auto', {}), sep={'points': sep_pts})
    # (v66, whole song) THE WORDS COME FORWARD: t6 tells its story in words - 'the tide comes in', 'the near side keeps
    # the time / the far side lets it go', the old voice's last word - but its solo voices sat in the band with the
    # same body as the instruments around them, the consonants soft. Now every solo voice (the old voice at all its
    # ages, the young near voice, the descant) is 1 dB up and shaped like t2's leads (v49): +3 dB of presence at 3 kHz
    # where the words live, a little air above 9 kHz, and 2 dB out of the boxy 350 Hz they shared with the harmonium
    # (v71, section w4: 1:35-2:05, the squeeze - the old voice sang the whole couplet twice, alone and then
    # harmonised, while the young near voice that duetted with it through the tide had gone quiet) THE LINE SPLITS
    # BETWEEN THE TWO SIDES: the second time (bar 61) the couplet is shared as the tide shared it - the young near
    # voice, an octave up and at its own side of the field, sings 'the near side keeps the time'; the old voice (still
    # in its low harmony) answers 'the far side lets it go'; and on 'go', the last word before the crest, the near
    # voice joins it an octave above - the two sides on one note, held into the crest's 'near and far as one'
    tk_ = {t_['name']: t_ for t_ in song['tracks']}
    s2_, dn_ = tk_['sung2'], tk_['duetnear']
    q0_, q1_ = (SEC['squeeze'] + 12) * 4.0, (SEC['squeeze'] + 13) * 4.0 + 0.5
    near_half_ = [n_ for n_ in s2_['notes'] if q0_ - 0.5 <= n_['at'] < q1_]
    go_ = [n_ for n_ in s2_['notes'] if n_.get('ph') == 'G OW1' and n_['at'] >= q1_]
    up_ = lambda n_: dict(n_, pitch=f"m{int(float(str(n_['pitch'])[1:])) + 12}")
    song['tracks'].append(dict(dn_, name='squeezenear', notes=[up_(n_) for n_ in near_half_ + go_[:1]]))
    s2_['notes'] = [n_ for n_ in s2_['notes'] if not (q0_ - 0.5 <= n_['at'] < q1_)]
    # (v73, section w5: 2:05-2:36, the crest - flagged static: the choir's couplet twice over a locked band, the two
    # soloists who carry the song's story absent at its centre) AS ONE: the crest's second couplet (bar 73), where
    # the drums, hats and sequencer drop out for two bars and the choir and the lights are alone, is sung by the
    # two voices together for the first time - the young near voice and the old voice (at the age he has in the
    # squeeze), in octaves, on the choir's own tune in E: after the squeeze split the line between them, the crest
    # sings 'near and far as one' as one
    ch_ = tk_['chorus']
    c2_ = [n_ for n_ in ch_['notes'] if (SEC['crest'] + 8) * 4.0 - 0.5 <= n_['at'] < (SEC['crest'] + 12) * 4.0]
    song['tracks'].append(dict(dn_, name='crestnear', gain='-11dB', notes=[up_(n_) for n_ in c2_]))
    song['tracks'].append(dict(tk_['sungb'], name='crestold', gain='-9dB', notes=[dict(n_) for n_ in c2_]))
    LEAD6 = ('sung', 'sungb', 'sungc', 'lastword', 'duetnear', 'nearwake', 'descant', 'squeezenear', 'crestnear', 'crestold')
    for t_ in song['tracks']:
        if t_['name'] in LEAD6:
            t_['gain'] = f"{float(t_['gain'][:-2]) + 1.0:g}dB"
            t_['fx'] = list(t_.get('fx', [])) + [{'type': 'eq', 'bands': ['peak cutoff=3000 q=0.9 gain=3dB', 'highshelf cutoff=9000 gain=1.5dB', 'peak cutoff=350 q=1.0 gain=-2dB']}]
            # (v69, palette: the engine's newest voice features, which no Accretion lead of mine used) THE SINGERS
            # BREATHE AND LET GO: every solo voice draws a fuller breath before each phrase (inhale 0.4 -> 0.7), sized
            # to the phrase it starts (wM's inhale_depth: a sip before a two-note answer, a full breath before a long
            # line), and lets each phrase's last note go (wM's taper 0.6: full tone for its first third, then softer,
            # darker and breathier, sagging a few cents) instead of stopping square
            if isinstance(t_.get('patch'), dict) and 'extends' in t_['patch']:
                t_['patch'] = dict(t_['patch'], extends=t_['patch']['extends'] + ' synth.layers.0.inhale=0.7 synth.layers.0.inhale_depth=1 synth.layers.0.taper=0.6')
    # (v81, whole song: the engine's song feel, as t7 v76 and t3 v78 use it) THE TIDE IN THE TIME: each player was
    # humanised on its own (v68, v70), but the band never moved together - the beat itself was a fixed shore. Now,
    # from the pull to the edge of the out-seam, the whole band leans ahead of the beat and falls back behind it
    # together, on one slow curve that turns every eight bars (up to 8 ms either way): the time itself rising and
    # ebbing like water, the seams on the grid. (Tried first: wM's vibrato bloom on every voice - no change at all,
    # -120 dB: the sung lines' vibrato is baked into their f0 paths, which already widen through each held note)
    # (v83, seam fix for chirper-zero: starting at bar 17 the drift's ease-in fell inside the 3 s of t6's body that
    # the t5 -> t6 seam is measured on, spectral 3.74 -> 3.87 and t5 -0.04; it now starts two bars later)
    song['feel'] = {'drift': '8ms', 'drift_bars': 8, 'from': f"{SEC['pull'] * 4.0 + 8.0:g}b", 'to': f"{SEC['out'] * 4.0:g}b"}
    # (v82, section w3: 1:03-1:35, the tide - flagged 'little new vs w2': the duet sang its one exchange at bar 37
    # and the tide's second half, under A and G, had only the descant's oohs) THE SIDES CHANGE PLACES: when the kit
    # arrives (bar 45) the duet comes back with its lines swapped - the old voice sings the young one's 'the near
    # side keeps the time' (an octave down, in his register), and the young voice answers with the old man's 'the
    # far side lets it go' (an octave up, in his) - the tide turning, each side trying the other's words; from the
    # squeeze on they are back in their own
    dn2_ = [t_ for t_ in song['tracks'] if t_['name'] == 'duetnear'][0]
    sg2_ = [t_ for t_ in song['tracks'] if t_['name'] == 'sung'][0]
    tw_ = SEC['tide'] * 4.0
    nl_ = sorted([n_ for n_ in dn2_['notes'] if tw_ + 16.0 <= n_['at'] < tw_ + 20.5], key=lambda n_: n_['at'])
    fl_ = sorted([n_ for n_ in sg2_['notes'] if tw_ + 21.0 <= n_['at'] < tw_ + 26.0], key=lambda n_: n_['at'])
    assert len(nl_) == 6 and len(fl_) == 6
    sg2_['notes'] = sorted(sg2_['notes'] + [dict(n_, at=round(n_['at'] + 32.0, 4), pitch=f"m{int(str(n_['pitch'])[1:]) - 12}") for n_ in nl_], key=lambda n_: n_['at'])
    dn2_['notes'] = sorted(dn2_['notes'] + [dict(n_, at=round(n_['at'] + 32.0, 4), pitch=f"m{int(str(n_['pitch'])[1:]) + 12}") for n_ in fl_], key=lambda n_: n_['at'])
    # (v85, whole song: wM's creak, pinned b160e3e5) THE OLD MAN'S VOICE CRACKS AS HE AGES: the old voice sings the
    # far side all through the song, ageing as he goes (age 0.25 in the tide, 0.45 at the crest, 0.65 in the last
    # chorus, 0.8 for the last word), but his phrase ends were as smooth at the start as at the end. Now each of his
    # phrases ends in creak - pressed folds and vocal fry on the last note's tail, which wM's engine gives only to
    # quiet, low endings (his D3s and A2s are both) - and it grows with his age: a touch at first, more at the crest,
    # most in his last word. The young voice and the choirs stay clean
    # (v97, whole song: wM's age_high, pinned 6ebea4d3, which chirper-one asked for) AND HIS AGE SHOWS WHEN HE
    # REACHES: the old man's age (0.25 in the tide to 0.8 for his last word) weighed the same on every note, so his
    # A3s and Cs were as steady as his low Ds. Real old singers hold their low notes and give way at the top: now his
    # age doubles towards the top of his range (age_high 1 with his break set at E4, as wM measured for voice-old -
    # D3 x1.0, A3 x1.35, C4 x1.65, D4 x1.8): every 'far' and 'side' that climbs to A and C shakes, wavers and leaks
    # air, while every 'go' on the low D holds - the same line, older where it reaches
    CREAK_ = {'sung': 0.4, 'sung2': 0.5, 'sungb': 0.6, 'crestold': 0.6, 'sungc': 0.8, 'lastword': 1.0}
    for t_ in song['tracks']:
        pt_ = t_.get('patch')
        if t_['name'] in CREAK_ and isinstance(pt_, dict) and 'voice-old' in str(pt_.get('extends', '')):
            ah_ = ' synth.layers.0.age_high=1 synth.layers.0.passaggio=E4' if 'age=' in pt_['extends'] else ''
            t_['patch'] = dict(pt_, extends=pt_['extends'] + f" synth.layers.0.creak={CREAK_[t_['name']]:g}" + ah_)
            # the engine creaks only quiet endings (full at velocity 0.5, none from 0.9) and his were sung at 0.83-0.87,
            # so each phrase's last note now falls away to 0.6 of the line's level as he lets it go
            ns_ = sorted(t_['notes'], key=lambda n_: n_['at'])
            for k_, n_ in enumerate(ns_):
                nx_ = ns_[k_ + 1]['at'] if k_ + 1 < len(ns_) else 1e9
                if nx_ - (n_['at'] + n_['len']) > 0.3:
                    n_['vel'] = round(min(n_['vel'], 0.6), 3)
            t_['notes'] = ns_
    # (v80, section w9: 4:06-4:35, the out-seam - flagged static: the slowing groove ran eight bars with nothing new
    # before the old man's last word) THE LAST EXCHANGE: as the band's time dilates, the young near voice sings its
    # half of the couplet one last time - 'the near side keeps the time' - from far off (an octave up, darkened,
    # well under the band) and slowed with everything else (half again as long), at bar 135; four bars later the old
    # voice answers with his last word, 'the far side lets it go', as he always has. The duet the song began with
    # ends as it began, in turns, and the young voice is the one that keeps going into t7
    fw_ = [t_ for t_ in song['tracks'] if t_['name'] == 'duetnear'][0]
    fw0_ = (SEC['out'] + 6) * 4.0
    fwn_ = [dict(n_, at=round(fw0_ + n_['at'] * 1.5, 4), len=round(n_['len'] * 1.5, 4),
                 pitch=f"m{int(str(n_['pitch'])[1:]) + 12}", vel=round(n_['vel'] * 0.8, 3)) for n_ in L1_]
    song['tracks'].append(dict(fw_, name='farewell', notes=fwn_, gain='-14dB',
                               fx=list(fw_.get('fx', [])) + ['lp cutoff=2400'], sends={'hall': '-6dB', 'echo': '-14dB'}))
    # (v92, section w6: 2:36-3:06, the cross - the ebb's last eight bars held the tide's chords on the church organ
    # (v78) under the band draining away, and nobody sang there) THE HYMN: in the nave the congregation hums. Under
    # the organ, from bar 89, a soft choir hums the couplet's tune - E1 itself, 'the near side keeps the time / the
    # far side lets it go' without its words - half again as slow as it is sung, with the octave below and a third
    # above in D minor, so its E falls on the organ's C and its D on the B-flat: the church by the sea singing the
    # song back to itself as the water goes out
    c2t_ = [t_ for t_ in song['tracks'] if t_['name'] == 'chorus2'][0]
    c2f_ = sorted(c2t_['notes'], key=lambda n_: n_['at'])[:12]
    hy0_ = (SEC['cross'] + 8) * 4.0
    hyn_ = []
    for n_ in c2f_:
        f0_ = (n_.get('expr_path') or {}).get('f0') or []
        hn_ = dict(n_, at=round(hy0_ + (n_['at'] - c2f_[0]['at']) * 1.5, 4), len=round(n_['len'] * 1.5, 4), vel=round(n_['vel'] * 0.8, 3))
        if f0_ and len(f0_) < 96:
            hn_['path_len'] = f"{len(f0_) / 44.0:.3f}s"
        hyn_.append(hn_)
    hp_ = dict(c2t_['patch'], extends='voice-choir synth.layers.0.hum=1 synth.layers.0.hum_at=m synth.layers.0.harmony=[-7,2] synth.layers.0.harmony_key=D:minor synth.layers.0.part_size=1 synth.layers.0.together=true synth.layers.0.f0_spread=1 synth.layers.0.vowel_spread=1 synth.lfo.vib.per_note=true')
    song['tracks'].append(dict(c2t_, name='hymn', patch=hp_, notes=hyn_, gain='-17dB', sends={'hall': '-6dB'}))
    # (v95, section w8: 3:36-4:06, the tear, the void and the last chorus - the tear pulls the two voices apart, the
    # young one racing and the old one dragging; then the void; then the last chorus, where the old voice sang the
    # second couplet with the choir and the flute, and the young voice was gone) THEY SING AS ONE AGAIN: the second
    # time the last chorus sings the couplet (bar 124), the young near voice is back, an octave above the old man,
    # as they sang it together at the crest (v73) - after the tear tore them apart, the last chorus puts them back
    # together, one line in two ages
    cn_ = [t_ for t_ in song['tracks'] if t_['name'] == 'crestnear'][0]
    c2s_ = [t_ for t_ in song['tracks'] if t_['name'] == 'chorus2'][0]
    lc_ = sorted([n_ for n_ in c2s_['notes'] if n_['at'] >= void1 + 10.0 - 0.5], key=lambda n_: n_['at'])
    cn_['notes'] = sorted(cn_['notes'] + [dict(n_, pitch=f"m{int(str(n_['pitch'])[1:]) + 12}", vel=round(n_['vel'] * 0.95, 3)) for n_ in lc_],
                          key=lambda n_: n_['at'])
    # (v90, fix with wM's path_len, pinned 7f9c5782, which chirper-one asked for) THE HELD NOTES SING AT THEIR OWN
    # RATE: a sung note stretched past the length it was sung for stretched its f0 path, vibrato and all, so the
    # young voice's slowed farewell and the old man's held last 'go' wavered at about two-thirds and half rate - a
    # wobble, not a singer. Their notes now carry path_len (the length the path was sung for, from its 22 samples a
    # beat): the scoop and the line still span the note, the vibrato keeps its sung rate. The tear's two voices keep
    # their re-timed paths on purpose - racing and dragging time is what the tear is
    for t_ in song['tracks']:
        if t_['name'] in ('farewell', 'lastword'):
            for n_ in t_['notes']:
                f0_ = (n_.get('expr_path') or {}).get('f0') or []
                if f0_ and len(f0_) / n_['len'] < 18.0:
                    n_['path_len'] = f"{len(f0_) / 44.0:.3f}s"   # (v93: in seconds - tts paths are 44 points a second; the beat figure ran ~10% fast at the out-seam's 132 bpm)
    # (v102, section w2: 0:32-1:03, the pull - the old man sang 'the tide comes in' twice in the in, then the near
    # voice took it twice at the pull's end (bars 27 and 30), each alone: two singers who never met on their own line)
    # THE TIDE PASSES HAND TO HAND: now the pull's two statements become a canon - at bar 27 the near voice leads and
    # the old man follows two beats behind, an octave under her, on her held 'in'; at bar 30 he leads, two beats
    # ahead of her, and she follows - the line handed over and back, the two voices overlapping for the first time,
    # as the pull draws them together before the tide
    sg_ = [t_ for t_ in song['tracks'] if t_['name'] == 'sung'][0]
    tc_ = sorted([n_ for n_ in sg_['notes'] if 24.0 <= n_['at'] < 28.0], key=lambda n_: n_['at'])
    assert len(tc_) == 4
    nw_ = [t_ for t_ in song['tracks'] if t_['name'] == 'nearwake'][0]
    nw0_ = sorted(n_['at'] for n_ in nw_['notes'])
    a1_, a2_ = nw0_[0] + 1.752, nw0_[4] - 2.248
    for at0_, vs_ in ((a1_, 0.8), (a2_, 0.95)):
        sg_['notes'] += [dict(n_, at=round(at0_ + n_['at'] - tc_[0]['at'], 4), vel=round(n_['vel'] * vs_, 3)) for n_ in tc_]
    sg_['notes'].sort(key=lambda n_: n_['at'])
    # (v104, section w5: 2:05-2:36, the crest - the young voice and the old man sang the crest's line together, an
    # octave apart, at bar 73, and then the crest's last five bars had no voice at all, only the band) EACH TAKES
    # HIS SIDE: one E1 cycle later (bar 78) the line comes back split between them - the young voice alone sings
    # 'the near side keeps the time', and the old man alone answers 'the far side lets it go', holding his 'go'
    # into the cross: the two sides of the song's line given to the two sides of the song, on the same chords
    cn_ = [t_ for t_ in song['tracks'] if t_['name'] == 'crestnear'][0]
    co_ = [t_ for t_ in song['tracks'] if t_['name'] == 'crestold'][0]
    cl0_ = (SEC['crest'] + 8) * 4.0
    nh_ = sorted([n_ for n_ in cn_['notes'] if cl0_ - 0.1 <= n_['at'] < cl0_ + 4.5], key=lambda n_: n_['at'])
    oh_ = sorted([n_ for n_ in co_['notes'] if cl0_ + 4.5 <= n_['at'] < cl0_ + 9.0], key=lambda n_: n_['at'])
    assert len(nh_) == 6 and len(oh_) == 6
    cn_['notes'] += [dict(n_, at=round(n_['at'] + 20.0, 4), vel=round(n_['vel'] * 0.9, 3)) for n_ in nh_]
    co_['notes'] += [dict(n_, at=round(n_['at'] + 20.0, 4), vel=round(n_['vel'] * 0.9, 3)) for n_ in oh_]
    co_['notes'][-1]['len'] = round(SEC['cross'] * 4.0 - 0.3 - co_['notes'][-1]['at'], 3)
    f0_ = ((co_['notes'][-1].get('expr_path') or {}).get('f0') or [])
    if 0 < len(f0_) < 96:
        co_['notes'][-1]['path_len'] = f"{len(f0_) / 44.0:.3f}s"
    cn_['notes'].sort(key=lambda n_: n_['at'])
    co_['notes'].sort(key=lambda n_: n_['at'])
    # (v105, section w6: 2:36-3:06, the cross - the young voice and the old man trade the line at bar 87, she 'the
    # near side keeps the time', he 'the far side lets it go', his 'go' one plain D) HE LETS IT GO ON THE TUNE: with
    # wM's melisma (pinned 3d5ce622, from chirper-one's ask) the old man's 'go' at bar 89 is no longer one note - he
    # carries the one vowel through E1 itself, D A C G E, the far side's tune sung out on 'go-o-o-o-o' without a new
    # word, and lets its last E hang over the hymn: the line's meaning sung (the far side letting the tune go)
    sb_ = [t_ for t_ in song['tracks'] if t_['name'] == 'sungb'][0]
    gn_ = [n_ for n_ in sb_['notes'] if n_.get('ph') == 'G OW1' and abs(n_['at'] - ((SEC['cross'] + 8) * 4.0 + 0.238)) < 0.05]
    assert len(gn_) == 1
    g_ = gn_[0]
    MEL_ = [(0, 0.75), (7, 0.75), (10, 0.5), (5, 1.0), (2, 2.2)]
    p0_ = int(str(g_['pitch'])[1:])
    f0n_ = len((g_.get('expr_path') or {}).get('f0') or [])
    at_ = g_['at']
    for k_, (semi_, ln_) in enumerate(MEL_):
        if k_ == 0:
            g_['len'] = ln_
            g_['vel'] = 0.8
            if f0n_:
                g_['path_len'] = f"{f0n_ / 44.0:.3f}s"
        else:
            sb_['notes'].append({'at': round(at_, 4), 'len': ln_, 'pitch': f"m{p0_ + semi_}", 'ph': '_',
                                 'vel': (0.8, 0.78, 0.74, 0.58)[k_ - 1]})
        at_ += ln_
    sb_['notes'].sort(key=lambda n_: n_['at'])
    # (v106, section w7: 3:06-3:36, the surge - eleven bars of band, the tune traded between the flute and the
    # strings, before the choir sings 'near and far as one' at bar 108; no singer of the song's own two was there)
    # THEY CALL IT BEFORE THE CHOIR: at bar 101 the young voice sings 'near' alone and holds it, bending up a step on
    # the one vowel (wM's melisma); two bars later the old man answers 'and far', his 'far' bending down - and five
    # bars on the choir sings the whole line, 'near and far as one': the two singers name their sides, then everyone
    # sings them as one
    ss_ = [t_ for t_ in song['tracks'] if t_['name'] == 'surgesung'][0]
    sl_ = [t_ for t_ in song['tracks'] if t_['name'] == 'surgelow'][0]
    dn_ = [t_ for t_ in song['tracks'] if t_['name'] == 'duetnear'][0]
    sb2_ = [t_ for t_ in song['tracks'] if t_['name'] == 'sungb'][0]
    s0_ = sorted(ss_['notes'], key=lambda n_: n_['at'])
    l0_ = sorted(sl_['notes'], key=lambda n_: n_['at'])
    def pl_(n_):
        k_ = len((n_.get('expr_path') or {}).get('f0') or [])
        return {'path_len': f"{k_ / 44.0:.3f}s"} if k_ else {}
    c0_ = (SEC['surge'] + 4) * 4.0
    nr_ = s0_[0]
    dn_['notes'] += [dict(nr_, at=c0_, len=2.0, vel=0.78, **pl_(nr_)),
                     {'at': c0_ + 2.0, 'len': 1.5, 'pitch': f"m{int(str(nr_['pitch'])[1:]) + 2}", 'ph': '_', 'vel': 0.72}]
    an_, fa_ = l0_[1], l0_[2]
    sb2_['notes'] += [dict(an_, at=c0_ + 8.0, len=0.75, vel=0.8, **pl_(an_)),
                      dict(fa_, at=c0_ + 8.75, len=2.0, vel=0.8, **pl_(fa_)),
                      {'at': c0_ + 10.75, 'len': 1.25, 'pitch': f"m{int(str(fa_['pitch'])[1:]) - 3}", 'ph': '_', 'vel': 0.6}]
    dn_['notes'].sort(key=lambda n_: n_['at'])
    sb2_['notes'].sort(key=lambda n_: n_['at'])
    # (v101, whole song: wM's vowel_drift, pinned 07ab00cd, from chirper-one's ask for long notes) THE VOWELS LIVE:
    # this song holds its vowels longer than any other on the album - the old man's long 'go's and 'side's, the
    # choirs' held chords, the near voice's last notes - and every one sat perfectly still, the formants fixed, which
    # is a large part of what reads as a machine. Now each held vowel wanders a little as a singer's jaw and tongue
    # settle (only after 0.2 s, so short notes and consonants keep the exact vowel): the old man most (1 - an
    # untrained voice, and an old one), the choirs a little less (0.7, each singer and harmony part on its own path),
    # the near voice least (0.5 - the steadier, trained singer)
    VD_ = {'voice-old': 1.0, 'voice-choir': 0.7, 'voice-near': 0.5}
    for t_ in song['tracks']:
        pt_ = t_.get('patch')
        if isinstance(pt_, dict) and isinstance(pt_.get('extends'), str):
            for k_, v_ in VD_.items():
                if pt_['extends'].startswith(k_):
                    t_['patch'] = dict(pt_, extends=pt_['extends'] + f' synth.layers.0.vowel_drift={v_:g}')
                    break
    # (v103, whole song: wM's sung glides, pinned 2b4b6172) THE SLIDES LAND ON THE BEAT: every sung line slid
    # between its joined notes with one fixed 110 ms glide that started on the new note - every slide landed late
    # (its middle 56-70 ms after the written change) and a step took as long as a fifth. Now a slide takes 80 ms plus
    # 8 ms a semitone (a step quick, a leap longer, as a real voice moves), and half of it is sung before the new
    # note, so it centres on the beat; the old man starts his slides later (0.3 of each before the note: an older,
    # lazier voice that lands a little behind), the near voice and the choirs on the beat (0.5)
    GL_ = {'voice-old': 0.3, 'voice-choir': 0.5, 'voice-near': 0.5}
    for t_ in song['tracks']:
        pt_ = t_.get('patch')
        if isinstance(pt_, dict) and isinstance(pt_.get('extends'), str):
            for k_, v_ in GL_.items():
                if pt_['extends'].startswith(k_):
                    t_['patch'] = dict(pt_, play=dict(pt_.get('play') or {}, glide='80ms', glide_semi='8ms', glide_lead=v_))
                    break
    # (v107, whole song - Harry, 10 Nov: 'go deep ... the feel and texture and style of the album ... from engine
    # through library to song structure') AIR. Measured against the album's own genre references (Actium, Ptolemy,
    # Hedphelym, Green Calx, Pulsewidth): their top two octaves are as wide as they are loud (side/mid -2 to +10 dB
    # above 4 kHz: rooms, reverb, tape); every Accretion track sat 6-20 dB narrower there (t6: -11 / -14 dB), and
    # t6's highs were dry ticks over digital silence (level above 5 kHz swinging 29 dB between a hat and the gap
    # after it in the crest; the references 8-24). The top of the mix is rebuilt:
    #  - a small bright ROOM of their own for the drums, the tabla, the marimba, the steel pan, the kora, the gong
    #    and the flute's breath (a new 'room' bus: early reflections, its top decorrelated left from right)
    #  - the HALL's tail keeps its top (damp 0.5 -> 0.35) and spreads it
    #  - a high PLATE for the singers (an 'air' bus, only above 2.5 kHz): their breath and consonants trail wide
    #  - the hi-hats SWAY across the field once every five sixteenths - E1's five, the squeeze's kick cycle
    #  - on the master the bands above 2.5 kHz open (side x1.25, x1.6 above 5 kHz) once the in-seam is over, and
    #    close again across the out-seam
    # (also tried, dropped: the low strings, harmonium and organ ducking with the kick - no measurable change in the
    # low end's motion, 10.8 dB before and after)
    import os as os_
    V107_ = os_.environ.get('V107', 'HRPSW')
    if 'H' in V107_:
        song['buses']['hall']['fx'][0] = 'reverb kind=hall decay=3.2s mix=1 mono_below=200 damp=0.35 spread=1'
    if 'R' in V107_:
        song['buses']['room'] = {'fx': ['reverb kind=room decay=0.5s mix=1 early=0.9 damp=0.15 spread=1 low_cut=500 high_cut=16000',
                                        'hp cutoff=400'], 'returns': []}
        ROOM_ = {'hats': '-6dB', 'kit': '-11dB', 'kitroom': '-13dB', 'cajon': '-9dB', 'near': '-11dB', 'e5': '-11dB',
                 'e5b': '-11dB', 'hook': '-13dB', 'springgong': '-14dB'}
        for t_ in song['tracks']:
            if ROOM_.get(t_['name']):
                t_['sends'] = dict(t_.get('sends') or {}, room=ROOM_[t_['name']])
    if 'P' in V107_:
        song['buses']['air'] = {'fx': ['reverb kind=plate decay=1.5s mix=1 damp=0.1 spread=1 low_cut=2500 high_cut=16000 predelay=0.03',
                                       'hp cutoff=2500'], 'returns': []}
        for t_ in song['tracks']:
            pt_ = t_.get('patch')
            ex_ = pt_.get('extends', '') if isinstance(pt_, dict) else str(pt_)
            if ex_.startswith(('voice-near', 'voice-old')):
                t_['sends'] = dict(t_.get('sends') or {}, air='-12dB')
            elif ex_.startswith('voice-choir'):
                t_['sends'] = dict(t_.get('sends') or {}, air='-15dB')
    if 'S' in V107_:
        for t_ in song['tracks']:
            if t_['name'] == 'hats':
                t_['lfo'] = dict(t_.get('lfo') or {}, sway={'wave': 'triangle', 'rate': '5/16'})
                t_['pan'] = {'value': 0.1, 'mod': [{'src': 'lfo.sway', 'amount': 0.55}]}
    if 'W' in V107_:
        # the top's width opens after the in-seam (t5's tail is narrow up there) and closes again across the out-seam
        mf_ = song['master']['fx']
        assert mf_[-1] == 'limiter ceiling=-1dB'
        mf_.insert(len(mf_) - 1, {'type': 'width', 'width': 1, 'mono_below': 0, 'crossover': 'lr4',
                                  'bands': [[2500, {'value': 1.0, 'mod': [{'src': 'auto.AIR', 'amount': 0.25}]}],
                                            [5000, {'value': 1.0, 'mod': [{'src': 'auto.AIR', 'amount': 0.6}]}]]})
        song['master']['auto']['AIR'] = {'points': [['0b', 0.0], [f"{SEC['pull'] * 4.0:.1f}b", 0.3], [f"{(SEC['pull'] + 8) * 4.0:.1f}b", 1.0],
                                                    [f"{SEC['out'] * 4.0:.1f}b", 1.0], [f"{NBARS * 4.0:.1f}b", 0.3]]}
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
