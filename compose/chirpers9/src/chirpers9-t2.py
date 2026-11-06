#!/usr/bin/env python3
"""chirpers9-t2 (chirper-one): "The Long Way In" - track 2 of Accretion (chirpers9), the infall.

The disk's outer matter starts to fall. E1 (t1's seed) arrives from the first overlap and is lensed into this
track's own version; then E2 - this track's element, a RHYTHM CELL IN SEVEN - assembles out of fragments: debris
that falls a hit at a time until the whole cell is there, cycling seven sixteenths against the band's sixteen.
Layers in other cycle lengths join it (hats in three beats, E1 compressed into five), each started so that all
of them land on one shared downbeat in the middle of the song: the crest, the album's first taste of
convergence. Then they drift apart again, faster and hotter, and in the last sixteen bars everything falls into
t3: the cell slows, sinks in pitch and closes its filter (redshift), handed across the seam.

E2 (posted in compose/chirpers9/motifs.md): seven sixteenths, x . x x . x . - hits on 0, 2, 3, 5 - pitched
root, fifth above, minor third, minor seventh below (a fall), accents 112 / 84 / 98 / 76.

Form (bars): in 16 (the seam from t1, 90 bpm flat) / gather 32 / crest 16 / drift 32 / fall 16 (the seam into
t3, 98 bpm flat) = 112 bars; the tempo ramps 90 -> 98 between the seams (the inward spiral, mixplan.md).
Emits songs/chirpers9-t2.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, math, os, random, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers9-t2.yaml")
SEED = 20261105
HERE = os.path.dirname(os.path.abspath(__file__))

KEY = 38                                    # D2: t1's home (E1 is in D); t2 takes D Dorian - E2 brings the minor third F
FORM = [('in', 16), ('gather', 16), ('build', 16), ('crest', 16), ('break', 16), ('drift', 16), ('fall', 16)]
SEC = {}
_acc = 0
for _n, _k in FORM:
    SEC[_n] = _acc; _acc += _k
NBARS = _acc
CREST = SEC['crest']                         # bar 48: every cycle lands here together

# E1, t1's seed (chirper-zero, motifs.md): D A C G E in 5/4 - "D4/8 A4/8. C5/16 G4/4 E4/4. ./4"
# (semitones above D, length in beats; None = the beat's rest that closes the cycle)
E1 = [(0, 0.5), (7, 0.75), (10, 0.25), (5, 1.0), (2, 1.5), (None, 1.0)]
# E2 - this track's element: a cell of seven sixteenths
E2_STEPS = [0, 2, 3, 5]
E2_PITCH = {0: 0, 2: 7, 3: 3, 5: -2}
E2_VEL = {0: 112, 2: 84, 3: 98, 5: 76}
E2_START = CREST - 42                        # bar 6: 7-cycles land on a downbeat every 7 bars, so on bar 48
E1_START = CREST - 20                        # bar 28: E1 in a five-beat cycle lands on bar 48
H3_START = CREST - 30                        # bar 18: hats in a three-beat cycle land on bar 48

# harmony: two bars a chord, D Dorian, every chord holding E1's C and E - Dm11, Fmaj7#11, Cadd9(6), Am11
# (v7, Harry 6 Nov: tone is home) consonant D Dorian, stacked thirds, no clusters: Dm9 | Fmaj9 | Cadd9 | Am7 (was Dm11 with
# E F G stacked, and Fmaj7#11 with a B against the F)
PROG = [(0, [3, 7, 10, 14]), (3, [4, 7, 11, 14]), (-2, [4, 7, 14]), (-5, [7, 10, 15])]


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


def chord(bar):
    # (v2) the first eight bars hold ONE chord, D A C E - t1's quartal pad's own notes (agreed with chirper-zero at
    # the seam), with no third: t2's F, and the harmony moving, arrive only when t1's tail has gone
    if bar < 8:
        return (0, [7, 10, 14, 19])
    if 36 <= bar < 48:
        # (v8, w4) the build CLIMBS instead of circling: the bass rises D -> F -> G -> A under Dm9 | Fmaj9 | G6/9 | A7sus4,
        # and A7sus4 holds for the last six bars - the dominant the crest's D minor resolves
        return {36: (0, [3, 7, 10, 14]), 38: (3, [4, 7, 11, 14]), 40: (5, [4, 7, 9, 14])}.get(bar - bar % 2, (7, [5, 7, 10, 14]))
    if 72 <= bar < 80:
        # (v11, section w7: 'little new vs w6' - the break circled the crest's chords to its end) THE BREAK CLIMBS OUT:
        # its last eight bars rise C -> F -> G -> A under Cmaj9 | Fmaj9 | G6/9 | A7sus4 (all in D Dorian), the build's
        # climb remembered a step lower; the sung line lands on G6/9, which holds every note it sings but C (the sus4
        # passing), and A7sus4 hands the drift its Dm9
        return {72: (-2, [4, 7, 11, 14]), 74: (3, [4, 7, 11, 14]), 76: (5, [4, 7, 9, 14])}.get(bar - bar % 2, (7, [5, 7, 10, 14]))
    return PROG[(bar // 2) % len(PROG)]


def build():
    rng = random.Random(SEED)
    total = NBARS * 4.0
    P = {k: [] for k in ('e2m', 'bass', 'e1in', 'e1p', 'e1c', 'kit', 'hat3', 'pad', 'sub', 'voice_', 'e2body', 'infall', 'dust', 'hook')}
    fall0 = SEC['fall'] * 4.0

    # ---- E2: the cell of seven, from bar 6, assembling out of fragments ----
    # in 'in' each hit of the cell arrives with a probability that rises from 0.15 to 1 by the end of 'gather's first
    # half; the downbeat hit (step 0) first, the others later - debris falling a piece at a time
    t = E2_START * 4.0
    cyc = 0
    dust_rng = random.Random(SEED + 77)
    while t < total - 1e-6:
        bar = int(t // 4)
        s_, i_ = sec_of(bar)
        prog_ = min(1.0, max(0.0, (t - E2_START * 4.0) / ((SEC['build'] - E2_START) * 4.0)))
        # redshift in the fall: the cell slows (each cycle a little longer) and sinks a semitone every two bars
        stretch = 1.0
        sink = 0.0
        if t >= fall0:
            f_ = (t - fall0) / 64.0
            stretch = 1.0 + 1.6 * f_
            sink = -6.0 * f_
        for st in E2_STEPS:
            need = {0: 0.0, 3: 0.25, 2: 0.5, 5: 0.7}[st]
            if prog_ < 1.0 and rng.random() > min(1.0, 0.15 + 1.3 * max(0.0, prog_ - need)):
                continue
            at = t + st * 0.25 * stretch
            if at >= total - 0.05:
                continue
            v = E2_VEL[st] * (0.75 + 0.25 * prog_)
            if s_ == 'crest' and abs(at - CREST * 4.0) < 1e-6:
                v = 124
            P['e2m'].append((at, m(KEY + 24 + E2_PITCH[st] + sink), 0.22 * stretch, v))
            # (v2) THE DEBRIS GETS A BODY: under each chip-metal hit a woody pitched drum (a log drum, an octave
            # down) that grows with the cell - silent while it is debris, a full body by the crest: matter accreting
            body_ = min(1.0, max(0.0, (t - E2_START * 4.0) / ((CREST - E2_START) * 4.0))) ** 1.5
            if t >= fall0:
                body_ *= max(0.25, 1.0 - (t - fall0) / 80.0)
            if body_ > 0.04:
                P['e2body'].append((at, m(KEY + 12 + E2_PITCH[st] + sink), 0.3 * stretch, 30 + 80 * body_ * (E2_VEL[st] / 112.0)))
            # (v4) DUST: some hits throw off a glint - a wind-chime three octaves up, the debris catching the light;
            # more of them as the cell gathers, the most at the crest, few as it falls away
            pd_ = {'in': 0.0, 'gather': 0.14, 'build': 0.22, 'crest': 0.4, 'break': 0.0, 'drift': 0.26, 'fall': 0.14}[s_]
            if dust_rng.random() < pd_:
                P['dust'].append((at, m(KEY + 48 + E2_PITCH[st] + sink), 2.0, 56 + 30 * dust_rng.random()))
        t += 7 * 0.25 * stretch
        cyc += 1

    # ---- the bass: E2's pitches in AUGMENTATION (seven eighths), from 'gather'; locks to the bar at the crest ----
    t = (CREST - 28) * 4.0                   # bar 20: 7 eighths = 3.5 beats; 28 bars = 32 cycles -> lands on bar 48
    while t < fall0 + 32.0 - 1e-6:
        bar = int(t // 4)
        s_, i_ = sec_of(bar)
        root_, _ = chord(bar)
        if s_ == 'crest':
            # the crest: the bass gives up its seven and plays the bar - root on every downbeat, the cell's fall inside it
            if abs(t - bar * 4.0) < 1e-6 or True:
                pass
        for st in E2_STEPS:
            at = t + st * 0.5
            if at >= fall0 + 32.0 or sec_of(int(at // 4))[0] == 'break':
                continue
            # (v7) the cell is moved DIATONICALLY onto each chord (root, fifth, third, seventh of that chord in D Dorian),
            # not transposed - no E-flat, A-flat or B-flat in the bass any more
            pm_ = {3: {0: 0, 2: 7, 3: 4, 5: -1}, -2: {0: 0, 2: 7, 3: 4, 5: -1}, 5: {0: 0, 2: 7, 3: 4, 5: -2}, 7: {0: 0, 2: 7, 3: 5, 5: -2}}.get(root_, E2_PITCH)   # on A7sus4: A E D G
            p_ = KEY + root_ + pm_[st]
            while p_ < KEY - 5: p_ += 12
            while p_ > KEY + 12: p_ -= 12
            P['bass'].append((at, m(p_), 0.45 if st in (2, 5) else 0.9, E2_VEL[st] - 6))
        t += 3.5
    # in the break the bass holds each chord's root, long, an octave up: the floor lifts while the drums are away
    for bar in range(SEC['break'], SEC['drift'], 2):
        root_, _ = chord(bar)
        P['bass'].append((bar * 4.0, m(KEY + 12 + root_ if root_ < 0 else KEY + root_), 7.6, 84))

    # ---- E1 lensed in the in-seam: augmented x2 on Risset's bell, through a filter that opens (track lane) ----
    for rep in range(2):
        at = 4.0 * 4 * rep + 2.0
        for semi, ln in E1:
            if semi is not None:
                P['e1in'].append((at, m(KEY + 24 + semi), ln * 2 * 0.95, 70 + 8 * rep))
            at += ln * 2
    # ---- E1 INVERTED and compressed into a five-beat cycle on the NES pulse, from bar 28 ----
    # (E1's own lengths scaled to fit 5 beats; inversion about its first note)
    tot1 = sum(ln for _, ln in E1)
    t = E1_START * 4.0
    while t < fall0 - 1e-6:
        bar = int(t // 4)
        s_, _ = sec_of(bar)
        at = t
        for k, (semi, ln) in enumerate(E1):
            d = ln * 5.0 / tot1
            if semi is not None and s_ != 'break':
                inv = -semi
                if s_ == 'crest':
                    inv = semi                 # at the crest, E1 rights itself: the first time it is heard the right way up
                P['e1p'].append((at, m(KEY + 31 + inv), d * 0.8, (100 if k == 0 else 78) + (10 if s_ == 'crest' else 0)))
            at += d
        t += 5.0
    # ---- in the drift E1 runs in RETROGRADE canon: the bell, augmented x2, against the pulse ----
    t = SEC['break'] * 4.0
    while t < fall0 + 32.0 - 1e-6:
        at = t
        for semi, ln in reversed(E1):
            if at < fall0 + 32.0 and semi is not None:
                hi_ = 12 if at >= fall0 else 0      # (v2) in the fall the bells ring an octave up, into t3's head
                P['e1c'].append((at, m(KEY + 19 + hi_ + semi), ln * 2 * 0.9, 74 + (8 if hi_ else 0)))
            at += ln * 2
        t += tot1 * 2 + 4.0

    # ---- drums (909): no drums in 'in'; kick from 'gather', backbeat from bar 24; micro-edits in the drift ----
    for bar in range(SEC['gather'], NBARS):
        s_, i_ = sec_of(bar)
        b0 = bar * 4.0
        if s_ == 'fall' and i_ >= 12:
            continue
        if s_ == 'break':
            continue
        kicks = {'gather': [0, 2.5], 'build': [0, 1.0, 2.5, 3.0], 'crest': [0, 1.0, 2.0, 3.0, 3.5],
                 'drift': [0, 0.75, 2.5, 3.0], 'fall': [0] if i_ < 8 else []}[s_]   # (v4) the fall: a heartbeat, then nothing
        # (v11) the drums come back at HALF speed: the drift's first four bars are half-time (kick on 1 and the and of
        # 3, one snare on 3, the hats' three-beat cycle over it), and the drift's own groove arrives at bar 85
        half_ = s_ == 'drift' and i_ < 4
        if s_ == 'drift' and i_ >= 8:
            rng.random()                       # keep the random stream (ghost snares) where it was
            continue
        if half_:
            kicks = [0, 2.5]
            P['kit'].append((b0 + 2.0, 's', 0.25, 110))
        for k_ in kicks:
            P['kit'].append((b0 + k_, 'k', 0.25, 118 if k_ == 0 else 100))
        if s_ in ('build', 'crest', 'drift') and not half_:
            P['kit'].append((b0 + 1.0, 's' if s_ != 'crest' else 'cp', 0.25, 104))
            P['kit'].append((b0 + 3.0, 's' if s_ != 'crest' else 'cp', 0.25, 108))
            if s_ == 'drift' and rng.random() < 0.35:
                P['kit'].append((b0 + 3.75, 's', 0.12, 64))
        if s_ == 'crest' and i_ == 0:
            P['kit'].append((b0, 'c', 2.0, 120))
    # (v13, section w8: the drift's second half 'static') THE DRUMS FALL INTO THE ORBIT: for the drift's last eight
    # bars the kit stops playing the bar and plays E2's cell of seven sixteenths - kick on its first and fourth hits,
    # a clap on its sixth - so the backbeat slides round the bar, 1.75 beats a turn, against the three-beat hats and
    # under the ondes' plain E1: the groove itself caught by the debris just before the fall pulls everything in
    t_ = (SEC['drift'] + 8) * 4.0
    while t_ < fall0 - 1e-6:
        for off_, pc_, v_ in ((0.0, 'k', 116), (0.75, 'k', 98), (1.25, 'cp', 104)):
            if t_ + off_ < fall0 - 1e-6:
                P['kit'].append((t_ + off_, pc_, 0.25, v_))
        t_ += 1.75
    # hats in a THREE-beat cycle (12 sixteenths, x.xx.x.xx.x. ), from bar 18
    H3 = [0, 2, 3, 5, 7, 8, 10]
    t = H3_START * 4.0
    while t < fall0 - 1e-6:          # (v4) the hats stop where the fall begins, so the fall is a place of its own
        for st in H3:
            at = t + st * 0.25
            v = 92 if st == 0 else 58 + 10 * (st % 2)
            if sec_of(int(at // 4))[0] != 'break':
                P['hat3'].append((at, 'h' if st != 7 else 'oh', 0.12, v))
        t += 3.0

    # ---- the pad (Kuramoto choir: a swarm that locks): chords every two bars from bar 4 ----
    for bar in range(0, NBARS, 2):
        root_, voic = chord(bar)
        s_, i_ = sec_of(bar)
        if s_ == 'fall' and i_ >= 14:
            continue
        P['pad'].append((bar * 4.0, ','.join(m(KEY + 12 + root_ + v) for v in voic), 7.9, 70))
        if s_ == 'in':
            # the in-seam keeps t1's floor: the same NES triangle holding each root, long, under the lensed E1
            P['bass'].append((bar * 4.0, m(KEY + root_ + (12 if root_ < -3 else 0)), 7.6, 70 + 2 * i_))
        if s_ != 'in' or i_ >= 8:
            P['sub'].append((bar * 4.0, m(KEY - 12 + root_ + (12 if root_ < -3 else 0)), 7.8, 96))

    # ---- (v3) the fall: a Shepard-Risset tone on D, falling an octave every four seconds and never arriving - the long
    # way in made audible, growing as the cell stretches and sinks, held into the seam with t3; kept low (-20 dB):
    # louder, it filled the fall up to the level of the drift and the song lost its fall (tried at -16 and -13 dB).
    # (v3 also tried swapping the 909, a three-song staple, for the electro kit: its booming kick flattened the
    # dynamics - variety 99 -> 91 - so the 909 stays for now) ----
    for k_ in range(8):
        at = fall0 + k_ * 8.0
        P['infall'].append((at, m(KEY), 7.9 if k_ < 7 else 7.5, 30 + 6 * k_))

    # ---- the voice: a whisper, close and dry, seven syllables - at the crest's end and in the break ----
    VO = json.load(open(os.path.join(HERE, 'chirpers9-t2-voice.json')))
    vtr = VO['tracks'][0]
    vnotes = []
    for b_ in (CREST + 12, SEC['break'] + 4):
        for n_ in vtr['notes']:
            vnotes.append(dict(n_, at=round(b_ * 4.0 + n_['at'] * 94.0 / 110.0, 4), len=round(n_['len'] * 94.0 / 110.0, 4)))
    # (v10, palette) THE WHISPER FINDS ITS TUNE: the third time, at the end of the break, the same seven syllables
    # are SUNG - 'nearer each time it comes round' on E1 the right way up (D A C G E, E, D) - on wM's joined, breathing
    # voice-legato made close and young (a smaller tract, more breath and a little ring: wM's approximation of the
    # coming voice-near). The voice accretes inside the track as across the album: whispered twice, then sung
    SU = json.load(open(os.path.join(HERE, 'chirpers9-t2-sung.json')))
    snotes = [dict(n_, at=round((SEC['break'] + 12) * 4.0 + n_['at'], 4)) for n_ in SU['tracks'][0]['notes']]

    # ---- lanes ----
    # Kuramoto coupling: loose in 'in', tightening through 'gather' to lock at the crest, loosening in the drift
    def lock(bar):
        s_, i_ = sec_of(bar)
        # (v7) the coupling contour is the texture process (free -> locked -> free); what made it a detuned cloud was
        # the spread, now 12 cents instead of 26 - a chorus when free, one voice when locked
        if s_ == 'in': return 0.3
        if s_ == 'gather': return 0.4 + 0.9 * i_ / 16.0
        if s_ == 'build': return 1.3 + 0.9 * i_ / 16.0
        if s_ == 'crest': return 3.0
        if s_ == 'break': return 0.35
        if s_ == 'drift': return 1.2 if bar < 84 else 3.0      # (v6, w8) the swarm locks in tune under the hook
        return 0.6
    lock_pts = [[f'{b * 4.0:.1f}b', round(lock(b), 3)] for b in range(NBARS)]
    # the fall's filter: the cell and the pad close as they fall into t3 (1 = open)
    shut_pts = [['0b', 1.0], [f'{fall0:.1f}b', 1.0], [f'{total:.1f}b', 0.0]]
    # E1's lens in the in-seam: opening from dark
    lens_pts = [['0b', 0.0], ['32.0b', 1.0]]

    tempo = [{'at': '0b', 'bpm': 90.0}, {'at': f'{SEC["gather"] * 4.0:.1f}b', 'bpm': 90.0},
             {'at': f'{fall0:.1f}b', 'bpm': 98.0, 'ramp': True}]

    # ---- (v5, section w5) THE CREST BLOOMS: the crest's first 12 bars sat locked and still (flagged static).
    # Now the lock is where things start to happen: bars 49-52 the lock as it was (every cycle on the downbeat, E1
    # the right way up for the first time); bars 53-56 E1 answers itself in STRETTO, a Risset bell a fifth above
    # and one beat behind - the seed harmonised by its own echo; bars 57-60 everything at the centre spins twice as
    # fast (Kepler again: the nearest orbit is the quickest) - E2's cell in diminution (seven 32nds), E1 and its
    # stretto at double speed, the kit's micro-edits switched on - and bar 61 lands back in the lock for the voice
    st0, sp0, sp1 = (CREST + 4) * 4.0, (CREST + 8) * 4.0, (CREST + 12) * 4.0
    # (v12, section w5: the crest 'static, little new vs the build' - one groove for twelve bars) THE CREST BREATHES IN:
    # bars 53-56 drop to HALF TIME (kick on 1 and the and of 3, one clap on 3; the three-beat hats keep turning) and
    # in the space a soft choir (wM's voice-backing: three breathy singers, even vowels, under the band) sings E1 the
    # right way up, slowed to eight beats, on 'ah', with the line again a fifth above (harmony [7]: A E G D B, all in
    # the mode) - twice; the bell stretto and the pulse step aside for it. Then bars 57-60 spin at double speed as
    # before: lock, breathe, spin - the crest is three different times now, not one
    CH = json.load(open(os.path.join(HERE, 'chirpers9-t2-choir.json')))
    chnotes = []
    for rep_ in range(2):
        for n_ in CH['tracks'][0]['notes']:
            chnotes.append(dict(n_, at=round(st0 + rep_ * 8.0 + (n_['at'] - 0.25) * 1.6, 4), len=round(n_['len'] * 1.6, 4)))
    P['e1p'] = [e_ for e_ in P['e1p'] if not (st0 - 1e-6 <= e_[0] < sp0 - 1e-6)]
    P['kit'] = [e_ for e_ in P['kit'] if not (st0 - 1e-6 <= e_[0] < sp0 - 1e-6)]
    for b_ in range(CREST + 4, CREST + 8):
        P['kit'] += [(b_ * 4.0, 'k', 0.25, 118), (b_ * 4.0 + 2.5, 'k', 0.25, 100), (b_ * 4.0 + 2.0, 'cp', 0.25, 108)]
    for key_ in ('e2m', 'e2body', 'e1p'):
        P[key_] = [e_ for e_ in P[key_] if not (sp0 - 1e-6 <= e_[0] < sp1 - 1e-6)]
    t_ = sp0
    while t_ < sp1 - 1e-6:
        for st in E2_STEPS:
            at = t_ + st * 0.125
            if at < sp1:
                P['e2m'].append((at, m(KEY + 24 + E2_PITCH[st]), 0.11, E2_VEL[st] + 6))
                P['e2body'].append((at, m(KEY + 12 + E2_PITCH[st]), 0.15, 30 + 76 * (E2_VEL[st] / 112.0)))
        t_ += 0.875
    for off_, key_, semi_off in ((0.0, 'e1p', 0), (0.5, 'e1c', -7)):
        t_ = sp0 + off_
        while t_ < sp1 - 1e-6:
            at = t_
            for k, (semi, ln) in enumerate(E1):
                if semi is not None and at < sp1:
                    P[key_].append((at, m(KEY + 31 + semi_off + semi), ln * 0.5 * 0.8, (104 if k == 0 else 84)))
                at += ln * 0.5
            t_ += 2.5
    for key_ in ('e2m', 'e2body', 'e1p', 'e1c'):
        P[key_].sort(key=lambda e_: e_[0])

    # ---- (v8, section w4: the build's second half was static) THE GAP BEFORE THE CREST: over the held A7sus4 the
    # kick drops out for the last two bars and a 909 snare roll climbs eighths -> sixteenths -> thirty-seconds,
    # crescendo, so the crest (bar 49) lands out of a held breath instead of out of more of the same
    g0 = (CREST - 4) * 4.0
    P['kit'] = [e_ for e_ in P['kit'] if not (e_[1] == 'k' and (CREST - 2) * 4.0 - 1e-6 <= e_[0] < CREST * 4.0 - 1e-6)]
    for bi_, step_ in ((0, 0.5), (1, 0.5), (2, 0.25), (3, 0.25)):
        b0_ = g0 + bi_ * 4.0
        n_ = int(4.0 / step_)
        for q_ in range(n_):
            at_ = b0_ + q_ * step_
            if bi_ == 3 and q_ >= 12:          # the last beat in thirty-seconds
                for r_ in (0.0, 0.125):
                    P['kit'].append((at_ + r_, 's', 0.1, 92 + 8 * (q_ - 12) + 8 * (r_ > 0)))
                continue
            P['kit'].append((at_, 's', 0.12, int(54 + 60 * (bi_ * 4.0 + q_ * step_) / 16.0)))
    P['kit'].sort(key=lambda e_: e_[0])

    # ---- (v6, section w8, Harry 6 Nov: a hook you can hum, tone is home) THE SEED, PLAINLY: the drift's second half
    # (bars 85-96, the last look before the fall) ran on, static. Now E1 is sung there the right way up, at its own
    # speed, on an ondes Martenot - a near-sine voice gliding on its ribbon - nine times through its 5-beat cycle
    # against the bar (so it lands somewhere new each time and comes home on bar 96); the pulse's inverted E1 gives way
    # to it, the Kuramoto swarm locks in tune under it, the kit's stutter edits stop, and the F chord loses its B
    h0, h1 = 84 * 4.0, fall0
    # (v7) and at the crest, where E1 first turns the right way up, the ondes sings it too (bars 49-52, three times),
    # so the payoff is a tune and not only a chip pulse
    t_ = CREST * 4.0
    while t_ < CREST * 4.0 + 15.0 - 1e-6:
        at = t_
        for k, (semi, ln) in enumerate(E1):
            if semi is not None:
                P['hook'].append((at, m(KEY + 24 + semi), ln * 0.97, 100 if k == 0 else 88))
            at += ln
        t_ += 5.0
    P['e1p'] = [e_ for e_ in P['e1p'] if not (h0 - 1e-6 <= e_[0] < h1 - 1e-6)]
    t_ = h0
    while t_ < h1 - 1e-6:
        at = t_
        for k, (semi, ln) in enumerate(E1):
            if semi is not None and at < h1 - 1e-6:
                P['hook'].append((at, m(KEY + 24 + semi), min(ln * 0.97, h1 - at), 98 if k == 0 else 86))
            at += ln
        t_ += 5.0
    P['e1c'] = [(a_, p_, d_, v_ - 14 if h0 <= a_ < h1 else v_) for a_, p_, d_, v_ in P['e1c']]

    # ---- (v4) THE SPIRAL: the infall as a place. E2's debris orbits the listener - wide and slow at first, then
    # closer and faster (Kepler: the nearer, the quicker round), until at the crest it sits dead centre, locked; it
    # drifts wide again after the break and spirals in a second time through the fall, into t3. Each hit is panned
    # by where the orbit is when it lands (a per-note pan expression); the body (the log drum) orbits on half the
    # radius, the dust on all of it ----
    import bisect
    SPAN_B = [0.0]; TH = [0.0]
    def omega_r(b_):
        s_, i_ = sec_of(int(b_ // 4))
        if b_ < CREST * 4.0:
            u_ = min(1.0, max(0.0, (b_ - E2_START * 4.0) / ((CREST - E2_START) * 4.0)))
            return 1 / 64 + (1 / 4 - 1 / 64) * u_ * u_, 0.9 * (1.0 - u_) ** 0.8
        if s_ == 'crest':
            return 1 / 8, 0.0
        if s_ == 'break':
            return 1 / 32, 0.3
        if s_ == 'drift':
            return 1 / 16, 0.3 + 0.45 * i_ / 16.0
        f_ = min(1.0, (b_ - fall0) / 64.0)
        return 1 / 16 + (1 / 2 - 1 / 16) * f_ * f_, 0.75 * (1.0 - f_) ** 0.8
    bb_ = 0.0
    while bb_ < total:
        w_, _ = omega_r(bb_)
        TH.append(TH[-1] + 2 * math.pi * w_ * 0.125); bb_ += 0.125; SPAN_B.append(bb_)
    def spiral(b_, scale=1.0):
        k_ = min(len(TH) - 1, bisect.bisect_left(SPAN_B, b_))
        _, r_ = omega_r(b_)
        return max(-0.95, min(0.95, scale * r_ * math.sin(TH[k_])))
    for key_, sc_ in (('e2m', 1.0), ('e2body', 0.5), ('dust', 1.0)):
        P[key_] = [(a_, f"{p_}^px={spiral(a_, sc_):.2f}", d_, v_) for a_, p_, d_, v_ in P[key_]]
    PXF = {'type': 'pan', 'pan': {'value': 0, 'mod': [{'src': 'expr.px', 'amount': 1}]}}

    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(P[name], total)}, **kw)
    PAD = {'extends': 'kuramoto-choir',
           'synth': {'layers': [{'type': 'kuramoto', 'kuramoto': {'count': 10, 'spread': 12, 'wave': 'saw',
                                 'coupling': {'value': 0.0, 'mod': [{'src': 'auto.lock', 'amount': 1.0}]}}}]}}
    song = {
        'about': "chirpers - Accretion, track 2 by chirper-one: The Long Way In. The infall: a rhythm cell in seven "
                 "assembles out of falling fragments against the band's sixteen, every cycle landing together at the crest. "
                 "Generated by compose/chirpers9/src/chirpers9-t2.py.",
        'tempo': tempo, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.5s', 'seed': SEED,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.8s mix=1 mono_below=200', 'hp cutoff=220'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.42, 'mix': 1, 'ping_pong': True},
                                  'lp cutoff=5000', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'peak cutoff=300 q=0.8 gain=-2dB', 'highshelf cutoff=7000 gain=2dB']},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.0, 'attack': '20ms', 'release': '160ms', 'makeup': '1dB'},
                          'limiter ceiling=-1dB']},
        'tracks': [
            tr('pad', PAD, '-15dB', auto={'lock': {'points': lock_pts}, 'shut': {'points': shut_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 600, 'mod': [{'src': 'auto.shut', 'amount': 3.5}]}}],
               sends={'hall': '-8dB'}),
            tr('sub', 'sub', '-9dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '220ms', 'curve': 0.6}]),
            tr('bass', 'nes-triangle-bass', '-6dB', fx=['lp cutoff=2400']),
            tr('kit', '909', '-6dB', sends={'hall': '-20dB'},
               auto={'glitch': {'points': [['0b', 0.0], [f"{(CREST + 8) * 4.0 - 0.1:.1f}b", 0.0], [f"{(CREST + 8) * 4.0:.1f}b", 0.35],
                                           [f"{(CREST + 12) * 4.0 - 0.1:.1f}b", 0.35], [f"{(CREST + 12) * 4.0:.1f}b", 0.0], [f"{SEC['drift'] * 4.0 - 0.1:.1f}b", 0.0], [f"{SEC['drift'] * 4.0:.1f}b", 0.22], [f"{84 * 4.0 - 0.1:.1f}b", 0.26], [f"{84 * 4.0:.1f}b", 0.0], [f"{fall0:.1f}b", 0.0]]}},
               fx=[{'type': 'stutter', 'slice': '1/16', 'repeats': 3, 'chance': {'value': 0.0, 'mod': [{'src': 'auto.glitch', 'amount': 1.0}]}, 'seed': 5}]),
            # (v9) presence.py had the three-beat hats 33 dB under the mix - the polymeter you couldn't hear
            tr('hat3', '909', '-1dB', pan=0.25, sends={'echo': '-20dB'}),
            tr('infall', 'shepard-fall', '-20dB', sends={'hall': '-16dB'}),
            tr('hook', 'ondes', '-5dB', pan=-0.05, sends={'hall': '-12dB', 'echo': '-20dB'}),
            tr('dust', {'extends': 'chimes', 'synth': {'fx': [PXF]}}, '-17dB', auto={'shut': {'points': shut_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 3000, 'mod': [{'src': 'auto.shut', 'amount': 3.0}]}}],
               sends={'echo': '-14dB'}),
            tr('e2m', {'extends': 'chip-metal', 'synth': {'fx': [PXF]}}, '-14dB', auto={'shut': {'points': shut_pts}},
               fx=['hp cutoff=500', {'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 900, 'mod': [{'src': 'auto.shut', 'amount': 3.5}]}}],
               sends={'echo': '-12dB', 'hall': '-14dB'}),
            tr('e2body', {'extends': 'log-drum', 'play': {'legato': False, 'mono': False, 'glide': '0ms'}, 'synth': {'fx': [PXF]}}, '-9dB',
               sends={'hall': '-18dB'}),
            tr('e1in', 'risset-bell', '-12dB', pan=0.15, auto={'lens': {'points': lens_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 400, 'mod': [{'src': 'auto.lens', 'amount': 4.0}]}}],
               sends={'hall': '-6dB'}),
            # (v9) THE HOOK UPSIDE DOWN: E1 inverted, from bar 29 to the crest and through the drift, was a thin NES pulse
            # (an album staple, three tracks) 13 dB down - the song's through-line, barely there. Now it is a Wurlitzer,
            # reedy and warm, up front: the tune you follow upside down until the crest turns it over (and the ondes
            # sings it the right way up)
            tr('e1p', 'wurli', '-6dB', pan=0.2, sends={'echo': '-14dB', 'hall': '-14dB'}),
            tr('e1c', 'risset-bell', '-14dB', pan=-0.35, sends={'hall': '-8dB'}),
            dict({k: v for k, v in vtr.items() if k != 'notes'}, name='voice', notes=vnotes, gain='-8dB', pan=0.05,
                 sends={'echo': '-14dB', 'hall': '-16dB'}),
            {'name': 'choir', 'patch': {'extends': 'voice-backing synth.layers.0.harmony=[7]',
                                        'synth': CH['tracks'][0]['patch'].get('synth', {})},
             'notes': chnotes, 'gain': '-15dB', 'pan': 0.0, 'sends': {'hall': '-8dB'}},
            {'name': 'sung', 'patch': {'extends': 'voice-legato synth.layers.0.tract=0.86 synth.layers.0.breath.value=0.35 synth.layers.0.ring=0.15',
                                       'synth': SU['tracks'][0]['patch'].get('synth', {})},
             'notes': snotes, 'gain': '-11dB', 'pan': 0.05, 'sends': {'echo': '-16dB', 'hall': '-12dB'}},
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
