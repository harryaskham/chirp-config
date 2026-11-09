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
import json
import re, math, os, random, subprocess, sys, tempfile

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


def swung(score, at0, at1, amt):
    # (v44) put a 16th shuffle on a score between two beats: split the token that crosses each boundary (a rest) and
    # put the engine's swing16= directive there
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


def chord(bar):
    # (v2) the first eight bars hold ONE chord, D A C E - t1's quartal pad's own notes (agreed with chirper-zero at
    # the seam), with no third: t2's F, and the harmony moving, arrive only when t1's tail has gone
    if bar < 8:
        return (0, [7, 10, 14, 19])
    if 36 <= bar < 48:
        # (v8, w4) the build CLIMBS instead of circling: the bass rises D -> F -> G -> A under Dm9 | Fmaj9 | G6/9 | A7sus4,
        # and A7sus4 holds for the last six bars - the dominant the crest's D minor resolves
        return {36: (0, [3, 7, 10, 14]), 38: (3, [4, 7, 11, 14]), 40: (5, [4, 7, 9, 14])}.get(bar - bar % 2, (7, [5, 7, 10, 14]))
    if 48 <= bar < 60:
        # (v18, section w5) THE LIGHT COMES ON: when E1 rights itself at the crest, the mode turns too - D Dorian's F
        # becomes F#, D Mixolydian, E1's own scale and the album's language - and the harmony turns bright and plain:
        # Dadd9 | G6/9 | Cadd9 | Dadd9 | G6/9 | Cadd9 (I - IV - bVII), every chord holding E1's notes; at bar 61 the
        # Am7 brings the F back and the break is Dorian again
        return {48: (0, [4, 7, 14]), 50: (5, [4, 7, 9, 14]), 52: (-2, [4, 7, 14]),
                54: (0, [4, 7, 14]), 56: (5, [4, 7, 9, 14])}.get(bar - bar % 2, (-2, [4, 7, 14]))
    if 72 <= bar < 80:
        # (v11, section w7: 'little new vs w6' - the break circled the crest's chords to its end) THE BREAK CLIMBS OUT:
        # its last eight bars rise C -> F -> G -> A under Cmaj9 | Fmaj9 | G6/9 | A7sus4 (all in D Dorian), the build's
        # climb remembered a step lower; the sung line lands on G6/9, which holds every note it sings but C (the sus4
        # passing), and A7sus4 hands the drift its Dm9
        return {72: (-2, [4, 7, 11, 14]), 74: (3, [4, 7, 11, 14]), 76: (5, [4, 7, 9, 14])}.get(bar - bar % 2, (7, [5, 7, 10, 14]))
    if bar >= 96:
        # (v22, section w9: the fall) THE FALL HANDS t3 ITS CHORDS: the fall's harmony becomes E3 itself - D | B-flat |
        # C, t3's progression - as Dm7 | B-flat maj7 | Csus2 | Dm7, every chord without an E or a B: across the seam
        # t3's dust pad plays Dm(add9) / E-flat maj7#11 / C11, and the old PROG's E naturals (in all four of its
        # chords) rubbed against its E-flat; now both sides share D F A C and the B-flat
        return [(0, [3, 7, 10, 15]), (-4, [4, 7, 11, 16]), (-2, [2, 7, 12, 14]), (0, [3, 7, 10, 15])][((bar - 96) // 2) % 4]
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
    snapped_ = False
    while t < total - 1e-6:
        # (v68) once the flung-out break is over (the debris silent from bar 73), the cell falls back onto its old
        # grid, so the drift's half-speed return lands exactly where it always did
        if not snapped_ and t >= (SEC['break'] + 8) * 4.0 - 1e-6:
            t0_ = E2_START * 4.0
            t = t0_ + math.ceil((t - t0_) / 1.75 - 1e-9) * 1.75
            snapped_ = True
        bar = int(t // 4)
        s_, i_ = sec_of(bar)
        prog_ = min(1.0, max(0.0, (t - E2_START * 4.0) / ((SEC['build'] - E2_START) * 4.0)))
        # redshift in the fall: the cell slows (each cycle a little longer) and sinks a semitone every two bars
        stretch = 1.0
        sink = 0.0
        if t >= fall0:
            f_ = (t - fall0) / 64.0
            stretch = 1.0 + 1.6 * f_
            # (v22) the sink was a slide of a tritone - continuous, so for most of the fall the cell sat BETWEEN
            # pitches, out of tune with everything (Harry: tone is home). Now it sinks in the cell's own notes: the
            # first half home, the second half an octave down - the redshift as a drop in register, D A F C throughout
            # (all four in t3's chords as well)
            sink = 0.0 if f_ < 0.5 else -12.0
        # (v68, section w6: 2:37-3:07, the crest's last bars and the break's first half - the debris ran on through
        # the break at the crest's speed and pitch, the floating break and its clock at odds) FLUNG OUT: past the
        # crest, its nearest pass, the cell is slung outward like a body past perihelion - Kepler: the farther out,
        # the slower - so through the break's first eight bars each turn of E2 takes longer (7 sixteenths stretching
        # to twice that), the chip-metal climbs an octave for the last four (thrown up and away), the log drum's
        # body thins and the hits fade, until the debris stops for the room to clear at bar 73; it returns at half
        # speed with the drums at bar 81 - the orbit coming back round
        rise_, fade_ = 0.0, 1.0
        if SEC['break'] * 4.0 - 1e-6 <= t < (SEC['break'] + 8) * 4.0 - 1e-6:
            f_ = (t - SEC['break'] * 4.0) / 32.0
            stretch = 1.0 + 1.0 * f_
            rise_ = 0.0 if f_ < 0.5 else 12.0
            fade_ = 1.0 - 0.4 * f_
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
            P['e2m'].append((at, m(KEY + 24 + E2_PITCH[st] + sink + rise_), 0.22 * stretch, v * fade_))
            # (v2) THE DEBRIS GETS A BODY: under each chip-metal hit a woody pitched drum (a log drum, an octave
            # down) that grows with the cell - silent while it is debris, a full body by the crest: matter accreting
            body_ = min(1.0, max(0.0, (t - E2_START * 4.0) / ((CREST - E2_START) * 4.0))) ** 1.5
            if t >= fall0:
                body_ *= max(0.25, 1.0 - (t - fall0) / 80.0)
            body_ *= fade_ ** 2
            if body_ > 0.04:
                P['e2body'].append((at, m(KEY + 12 + E2_PITCH[st] + sink), 0.3 * stretch, 30 + 80 * body_ * (E2_VEL[st] / 112.0)))
            # (v4) DUST: some hits throw off a glint - a wind-chime three octaves up, the debris catching the light;
            # more of them as the cell gathers, the most at the crest, few as it falls away
            pd_ = {'in': 0.0, 'gather': 0.14, 'build': 0.22, 'crest': 0.4, 'break': 0.0, 'drift': 0.26, 'fall': 0.14}[s_]
            if dust_rng.random() < pd_:
                P['dust'].append((at, m(KEY + 48 + E2_PITCH[st] + sink), 2.0, 56 + 30 * dust_rng.random()))
        t += 7 * 0.25 * stretch
        cyc += 1

    # (v16, section w1: the in-seam 'static' - one chord, a lensed bell, debris arriving at random) THE CELL FALLS IN
    # FROM FAR AWAY: before E2 arrives at its own speed (bar 7) it is already there, slowed - a log drum playing the
    # cell at x4 (seven beats a turn) from the first bar, twice, then at x2 (three and a half) with the chip-metal
    # catching it, twice, landing exactly where the cell begins at x1: the infall heard as an accelerando of one
    # rhythm, the debris speeding up as it nears. And while t1's quartal pad is still sounding, the slowed cell
    # sings t1's notes - D A E C, E for F - the minor third arrives only when the cell is up to speed
    for t0_, sx_ in ((3.0, 4.0), (10.0, 4.0), (17.0, 2.0), (20.5, 2.0)):
        for st in E2_STEPS:
            at = t0_ + st * 0.25 * sx_
            pc_ = {0: 0, 2: 7, 3: 2, 5: -2}[st]
            P['e2body'].append((at, m(KEY + 12 + pc_), 0.3 * sx_, (60 if sx_ == 4.0 else 72) + (12 if st == 0 else 0)))
            if sx_ == 2.0:
                P['e2m'].append((at, m(KEY + 24 + pc_), 0.22, 54 + (14 if st == 0 else 0)))
    for key_ in ('e2body', 'e2m'):
        P[key_].sort(key=lambda e_: e_[0])

    # (v17, section w7: 'little new vs w6' - the break's two halves shared one texture) THE ROOM CLEARS FOR THE VOICE:
    # for the break's last eight bars - the climb out, C F G A - E2's debris stops for the first time since bar 7: no
    # chip-metal, no log drum, no glints; only the climbing pad, the lifted bass and the bells' retrograde canon, and
    # under the sung line a soft backing choir holds 'ooh' on D4 with a third below in D Dorian (B3; wM's
    # voice-backing with harmony_key) - D and B sit in both G6/9 and A7sus4 - breathing once between the two chords.
    # The debris comes back with the drums at bar 81, at half speed: the return is an event now
    cl0_, cl1_ = 72 * 4.0, 80 * 4.0
    for key_ in ('e2m', 'e2body', 'dust'):
        P[key_] = [e_ for e_ in P[key_] if not (cl0_ - 1e-6 <= e_[0] < cl1_ - 1e-6)]

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
        # (v14, section w4: the build 'static') THE ORBIT DECAYS: as the build climbs, E1's upside-down cycle turns
        # faster - five beats, then four (from bar 40), then three (from bar 44) - Kepler again, the nearer the quicker
        # - until the crest catches it, turns it the right way up and gives it back its own five beats
        L_ = 4.0 if 157.0 - 1e-6 <= t < 173.0 - 1e-6 else (3.0 if 173.0 - 1e-6 <= t < 191.0 - 1e-6 else 5.0)
        for k, (semi, ln) in enumerate(E1):
            d = ln * L_ / tot1
            if semi is not None and s_ != 'break':
                inv = -semi
                if s_ == 'crest':
                    inv = semi                 # at the crest, E1 rights itself: the first time it is heard the right way up
                P['e1p'].append((at, m(KEY + 31 + inv), d * 0.8, (100 if k == 0 else 78) + (10 if s_ == 'crest' else 0)))
            at += d
        t += L_
        if abs(t - 191.0) < 1e-6:
            t = 192.0                     # the crest's downbeat
    for t0_, n_ in ((98.25, 3), (104.0, 5)):
        at = t0_
        for k, (semi, ln) in enumerate(E1[:n_] if n_ < 5 else E1):
            if semi is not None:
                P['e1p'].append((at, m(KEY + 31 - semi), ln * 0.8, (88 if k == 0 else 70) - (10 if t0_ < 100 else 0)))
            at += ln
    P['e1p'].sort(key=lambda e_: e_[0])
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
        # (v14) and the hats' orbit decays with it: the three-beat cycle shrinks to two beats (bars 40-43) and one
        # (44-47), the polymeter collapsing into the beat as the crest arrives; from the crest, three again
        steps_, L_ = H3, 3.0
        if 159.0 - 1e-6 <= t < 175.0 - 1e-6:
            steps_, L_ = [0, 2, 3, 5, 6], 2.0
        elif 175.0 - 1e-6 <= t < 192.0 - 1e-6:
            steps_, L_ = [0, 2, 3], 1.0
        for st in steps_:
            at = t + st * 0.25
            v = 92 if st == 0 else 58 + 10 * (st % 2)
            if sec_of(int(at // 4))[0] != 'break':
                P['hat3'].append((at, 'h' if st != 7 else 'oh', 0.12, v))
        t += L_

    # ---- the pad (Kuramoto choir: a swarm that locks): chords every two bars from bar 4 ----
    for bar in range(0, NBARS, 2):
        root_, voic = chord(bar)
        s_, i_ = sec_of(bar)
        if s_ == 'fall' and i_ >= 14:
            continue
        P['pad'].append((bar * 4.0, ','.join(m(KEY + 12 + root_ + v) for v in voic), 7.9, 70))
        if s_ == 'in' and i_ >= 8:
            # the in-seam keeps t1's floor: the same NES triangle holding each root, long, under the lensed E1
            # (v21, agreed with chirper-zero: from bar 9 only - t1's own NES triangle holds D2 until then, and two of
            # them on one note half a cycle apart cancelled each other in the crossfade)
            P['bass'].append((bar * 4.0, m(KEY + root_ + (12 if root_ < -3 else 0)), 7.6, 70 + 2 * i_))
        if s_ != 'in' or i_ >= 8:
            # (v17) agreed with chirper-zero: t1's tail has a D1 sine pedal under the whole overlap, so in the in-seam
            # the sub holds D1 - the same note - whatever the chords do (C1 against D1 would beat at 4 Hz)
            rs_ = 0 if s_ == 'in' else root_
            P['sub'].append((bar * 4.0, m(KEY - 12 + rs_ + (12 if rs_ < -3 else 0)), 7.8, 96))

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
    # (v27, section w6: the crest's end and the break's first half; the line WHISPERED twice there, on a speech
    # voice) THE CHORUS ECHOES: the whispers go. In their place a far little choir (voice-backing, three singers,
    # breathing together - wM's 'together' - in a big hall) sings the crest's line back as an echo: at bar 61, just
    # after the chorus, softly; at bar 69, deep in the break, slower (x1.5) and further away - the chorus going out
    # like light from the crest. Then at bar 77 the near voice finds it again, alone. Chorus -> echo -> found: every
    # statement of the line is now SUNG (Harry: the sung line at the crest is the moment), none spoken
    echonotes = []
    for b_, sx_, vm_ in ((CREST + 12, 1.0, 0.8), (SEC['break'] + 4, 1.5, 0.62)):
        for n_ in SU['tracks'][0]['notes']:
            echonotes.append(dict(n_, at=round(b_ * 4.0 + (n_['at'] - 0.25) * sx_, 4), len=round(n_['len'] * sx_, 4),
                                  vel=round(n_.get('vel', 0.8) * vm_, 3)))
    OOH = json.load(open(os.path.join(HERE, 'chirpers9-t2-ooh.json')))
    oohn = [dict(OOH['tracks'][0]['notes'][0], at=round(b_ * 4.0, 4), len=7.3) for b_ in (76, 78)]
    # (v23, section w1, bars 5-8: chirper-zero's seam tool found t2's head thin there - -27 / -30 dB alone in bars 7-8,
    # a valley in the crossfade just before the bass and sub arrive at bar 9) THE HEAD BREATHES IN: the backing
    # voices that close the break open the song - 'ooh' on D4 with the open fifth above (A4, in key: no third, so it
    # sits inside t1's quartal D A C E), twice, the second louder - an inhale over four bars that the bass, the sub
    # and the gather land on at bar 9. The ooh comes back at the end of the break (bars 77-80): the song's two
    # thresholds share one breath
    # (v35, whole song) THE CREST OPENS UP: compscore's sections still hear 1:05-2:50 as ONE 105-s section - the
    # verse, the pre-chorus, the build and the crest run together because the crest's light only adds brightness to
    # the same band. Now the crest has a sound of its own for all sixteen bars: the backing voices, all together, hold
    # 'ooh' chords under it - a full triad in D Mixolydian on each chord (G B D, C E G, D F# A, and A C E as the
    # Am7 comes), mid-register under the sung lines - the chorus's room, the way a record's chorus opens up; and it
    # stops where the break begins
    crestpad = []
    for b_ in range(CREST, CREST + 16, 2):
        r_ = chord(b_)[0]
        p_ = KEY + 24 + r_
        while p_ > 66:
            p_ -= 12
        while p_ < 55:
            p_ += 12
        crestpad.append(dict(OOH['tracks'][0]['notes'][0], at=round(b_ * 4.0, 4), len=7.7, vel=0.72, pitch=f"m{p_}"))
    # (v41, palette: wM's closed-mouth hum, pinned 13:43, which t2 has not used) THE BREAK IS HUMMED: under the bells,
    # the floating guitar and the far choir's echo, the backing voices that held the crest's chords now HUM the
    # break's - mouths closed ('mmm': hum 1, hum_at m - a murmur near 270 Hz, no air), the chords in D Dorian (Dm9,
    # Fmaj9, Cadd9, Am7, then the climb C F G A) - the crest remembered with the mouth shut: what people do with a
    # tune they can't stop hearing. Quiet, low in the hall; it stops where the found voice sings at the break's end
    breakhum = []
    for b_ in range(SEC['break'], SEC['break'] + 12, 2):
        r_ = chord(b_)[0]
        p_ = KEY + 12 + r_
        while p_ > 57:
            p_ -= 12
        while p_ < 48:
            p_ += 12
        breakhum.append(dict(OOH['tracks'][0]['notes'][0], at=round(b_ * 4.0, 4), len=7.7, vel=0.8, pitch=f"m{p_}"))
    # (v46, whole song: the last chorus - the line Harry stopped for, four times, the last lifted to E - had less under
    # it than the crest itself: no choir, the line, the ondes and the band) THE LAST CHORUS IS THE BIGGEST: the crest's
    # backing voices come back for it, the same 'ooh' triads with their basses an octave below (part_size 1) on the
    # drift's chords (A minor, D minor, F, C in D Dorian), and on the lift the whole choir rises with the line into
    # B minor in E Dorian - so the song's last statement of its hook is its fullest, as a record's last chorus is
    lastpad, lastpadE = [], []
    for b_ in range(86, 96, 2):
        r_ = chord(b_)[0]
        p_ = KEY + 24 + r_
        while p_ > 66:
            p_ -= 12
        while p_ < 55:
            p_ += 12
        if b_ >= 94:
            lastpadE.append(dict(OOH['tracks'][0]['notes'][0], at=round(b_ * 4.0, 4), len=7.7, vel=0.8, pitch=f"m{p_ + 2}"))
        else:
            lastpad.append(dict(OOH['tracks'][0]['notes'][0], at=round(b_ * 4.0, 4), len=7.7, vel=0.72 + 0.03 * (b_ - 86) / 2, pitch=f"m{p_}"))
    # (v53, section w9: the fall 'static' since the first day - forty seconds of instruments sinking, the song's
    # people gone from it the moment the last chorus ended) THE VOICES GO UNDER: for the fall's first eight bars - the
    # heartbeat half - the backing choir that held the crest and the last chorus holds the fall's own chords (D minor,
    # B-flat major 7, C, D minor) with its mouths closed: a hum, basses and all (part_size), each singer on their own
    # vibrato (wM's vib_spread, pinned tonight), each chord softer than the last; when the heartbeat stops at bar 105
    # the voices have gone under, and t3's wind has the space
    fallhum = []
    for k_, b_ in enumerate(range(96, 104, 2)):
        r_ = chord(b_)[0]
        p_ = KEY + 24 + r_
        while p_ > 64:
            p_ -= 12
        while p_ < 53:
            p_ += 12
        fallhum.append(dict(OOH['tracks'][0]['notes'][0], at=round(b_ * 4.0, 4), len=7.7, vel=round(0.82 - 0.1 * k_, 2), pitch=f"m{p_}"))
    oohin = [dict(OOH['tracks'][0]['notes'][0], at=16.0, len=7.6, vel=0.6), dict(OOH['tracks'][0]['notes'][0], at=24.0, len=7.9, vel=0.88)]
    # (v30, section w3: 1:03-1:35, 'static' - the second verse sang into the same groove as the first, and the wurli
    # entered on its own two bars later) THE SECOND VERSE IS ANSWERED: the backing voices hold 'ooh' (D4 and the open
    # fifth above) under its second line, and the wurli ANSWERS the voice - three notes of E1 upside down (A D B)
    # after 'all that falls', the whole upside-down phrase after 'falls a little nearer' - so the wurli's long
    # upside-down E1 (from bar 29 to the crest) now begins as a reply to the singer instead of out of nowhere
    oohin.append(dict(OOH['tracks'][0]['notes'][0], at=100.0, len=3.8, vel=0.55))
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
    # (v59, section w1: 0:00-0:32, the in-seam, 'static' since the first day - one quartal chord held eight bars at
    # full brightness under t1's tail, the bell and the debris arriving through it) THE CHORD FALLS IN FROM DOWN THE
    # WELL: the pad's chord - t1's own notes, D A C E - now arrives the way the bell does, from far below and behind:
    # it starts dark (its low-pass near 700 Hz, the hall doing most of the talking) and opens over the eight bars to
    # full light exactly as the harmony starts moving at bar 9; and the two 'ooh's in bars 5 and 7 are sung from deep
    # in the well, the trio standing at its own depths (wM's depth_spread 1, pinned 07:40: later, quieter and darker
    # the further back) with more hall
    padshut_pts = [['0b', 0.15], ['32.0b', 1.0], [f'{fall0:.1f}b', 1.0], [f'{total:.1f}b', 0.0]]
    # E1's lens in the in-seam: opening from dark
    lens_pts = [['0b', 0.0], ['32.0b', 1.0]]

    # (v19, whole song) DYNAMICS, AIR AND A LIGHTER FLOOR: every section of t2 sat within 3 dB of every other (the
    # level range compscore's variety reads, and what a listener hears as 'always the same weight'). Now an energy
    # lane on the master shapes the song: the in-seam and the gather low and gathering, the build climbing, the crest
    # on top, the break FALLING AWAY (4 dB under the crest's neighbours), the drift rising back, the fall sinking out
    # (v20, agreed with chirper-zero: t1's body is the louder side of our seam, 8.7 dB over the gather) the gather
    # lifted 2.5 dB - t1 takes the end of its lock down ~2 dB to meet it
    EN = {'in': (-3.0, -1.5), 'gather': (0.0, 1.0), 'build': (-1.0, 1.0), 'crest': (1.5, 1.0), 'break': (-4.0, -3.0),
          'drift': (-1.5, 0.5), 'fall': (0.0, -3.0)}
    # (v77, whole song) THE NEAREST PASS HITS: the crest sat only half a dB over the build (-10.7 against -11.3 dB),
    # the break 3 dB under - an orbit drawn too round. The arc is wider now: the build starts lower and climbs
    # further (-1.5 -> +1.5), the crest lands a dB higher (+2.5, easing to +1.5), the break falls further away
    # (-5 -> -3.5), and the drift climbs from deeper (-2 -> +1) into the last chorus; the in-seam, the gather's
    # first bars and the fall - the two seams - are as they were. (Measured: the limiter and the loudness target hold
    # the crest, so it gains only 0.3 dB on the build; the arc widens mostly below - the break 0.8 dB deeper, the
    # build's start 0.3 lower)
    EN = dict(EN, gather=(0.0, 0.5), build=(-1.5, 1.5), crest=(2.5, 1.5), drift=(-2.0, 1.0))
    EN['break'] = (-5.0, -3.5)
    energy_pts = []
    for b_ in range(NBARS):
        s_, i_ = sec_of(b_)
        a_, z_ = EN[s_]
        energy_pts.append([f'{b_ * 4.0:.1f}b', round(a_ + (z_ - a_) * i_ / 15.0, 2)])
    # (v20, section w4: the build 'static, little new vs w3' - one texture climbing for twelve bars) THE DARK BEFORE
    # THE LIGHT: at bar 37, where the bass starts its climb, the whole band drops behind a low-pass (about 3 kHz) and
    # then opens, bar by bar, to full brightness exactly as the crest arrives - so the crest's change of mode (v18,
    # D Dorian -> D Mixolydian, 'the light comes on') is prepared by twelve bars of the light being held back
    open_pts = [['0b', 1.0], [f'{36 * 4.0 - 0.05:.2f}b', 1.0], [f'{36 * 4.0:.1f}b', 0.4], [f'{CREST * 4.0 - 1.0:.1f}b', 0.72],
                [f'{CREST * 4.0 - 0.05:.2f}b', 0.72], [f'{CREST * 4.0:.1f}b', 1.0]]   # (v31) the light comes ON at the crest
    # (v56, whole song) THE FIELD FALLS IN: the song is an infall, but its space never moved - the debris, the band
    # and the voices stood as wide at the end as at the start. Now the whole stereo field draws inward as the song
    # falls: full width for the in-seam's debris arriving from everywhere, narrowing a little through the gather
    # and the build, opening a touch as the light comes on at the crest, closing again through the break and the
    # drift, and in the fall - the last sixteen bars, into t3 - collapsing towards a single point in the middle,
    # everything converging where it falls (the master's width, 1.0 down to 0.15)
    WID = {'in': (1.0, 1.0), 'gather': (1.0, 0.94), 'build': (0.94, 0.86), 'crest': (0.92, 0.86), 'break': (0.86, 0.78),
           'drift': (0.78, 0.68), 'fall': (0.62, 0.15)}
    wid_pts = []
    for b_ in range(NBARS):
        s_, i_ = sec_of(b_)
        a_, z_ = WID[s_]
        wid_pts.append([f'{b_ * 4.0:.1f}b', round(a_ + (z_ - a_) * i_ / 15.0, 3)])
    tempo = [{'at': '0b', 'bpm': 90.0}, {'at': f'{SEC["gather"] * 4.0:.1f}b', 'bpm': 90.0},
             {'at': f'{fall0:.1f}b', 'bpm': 98.0, 'ramp': True}]
    # (v73, whole song) KEPLER'S SECOND LAW: a body in orbit moves fastest at its nearest pass and slowest far out. The
    # song's tempo climbed in one straight line from t1's 90 to t3's 98. Now it follows the orbit: it quickens
    # through the gather and the build into the crest (90 -> 97 at the crest's downbeat, 98 at its height), slows as
    # the break flings the debris outward (back to 94 by the break's end - with E2's own slowing), and quickens again
    # through the drift to the fall's 98, so both seams keep their tempos
    tempo = [{'at': '0b', 'bpm': 90.0}, {'at': f'{SEC["gather"] * 4.0:.1f}b', 'bpm': 90.0},
             {'at': f'{CREST * 4.0:.1f}b', 'bpm': 97.0, 'ramp': True},
             {'at': f'{(CREST + 8) * 4.0:.1f}b', 'bpm': 98.0, 'ramp': True},
             {'at': f'{SEC["drift"] * 4.0:.1f}b', 'bpm': 94.0, 'ramp': True},
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
    # (v21, whole song) THE CREST GETS ITS WORDS: t2's line - 'nearer each time it comes round', E1's own notes -
    # was sung only once, alone, at the end of the break. Now it is the crest's chorus too: where E1 first turns the
    # right way up and the light comes on (D Mixolydian, v18), the near voice sings it WITH the ondes (the same
    # notes, the same octave), with a third above that the key gives (F# A C E B G over D A C G E: harmony_key, D
    # Mixolydian, so the F# of the lit crest is in the harmony too), the first and third time the ondes plays it;
    # the second time the ondes answers alone. Then the whispers remember it, and at the end of the break the voice
    # finds it again, alone, softer: chorus -> memory -> the tune found
    CS = json.load(open(os.path.join(HERE, 'chirpers9-t2-sung.json')))
    csnotes = []
    for b_ in (CREST * 4.0, CREST * 4.0 + 10.0):
        for n_ in CS['tracks'][0]['notes']:
            csnotes.append(dict(n_, at=round(b_ + n_['at'] - 0.25, 4)))
    # (v33, section w5: the crest's second half 'static, little new vs w4' - after the line and its echo, eight bars of
    # the same lit groove with nothing new to sing) THE CHORUS GETS ITS SECOND LINE: the crest's line, which Harry
    # stopped for, stays exactly as it is; then, over the crest's second G6/9 and C (bars 57-60), the same near voice
    # answers it with a new phrase - 'round and round, the middle draws us in' (B A G, then G A C B A G: falling,
    # rising, falling home to G) - and sings it again over C and Am7 (bars 61-64) as the light turns Dorian for the
    # break, both times with its keyed third above. A chorus of two lines, call and answer, instead of one line and a
    # vamp
    # (v34, section w4: the build 'static, little new vs w3' - twelve bars of the climb with no voice between the
    # second verse and the crest) THE PRE-CHORUS: the song now has verse -> pre-chorus -> chorus. As the bass climbs
    # D -> F -> G -> A under the dark filter, the near voice sings what the build does - Kepler: 'the nearer, the
    # faster' (A A G A C A over F, then a step up, B B A B D B over G), and over the long A7sus4 'round and round and
    # round' climbing to E5, held into the snare ladder - her top notes (D5, E5) flipping into head voice (wM's
    # passaggio at C5, so the climb lightens instead of pushing); then the beat of silence, and the chorus drops
    # back down to her D4: 'nearer each time it comes round'
    PC = json.load(open(os.path.join(HERE, 'chirpers9-t2-prech.json')))
    pcnotes = [dict(n_, at=round(38 * 4.0 + n_['at'] - 0.245, 4)) for n_ in PC['tracks'][0]['notes']]
    # (v47, whole song: after the first verse (bars 20-26) no voice sings for twelve bars - 1:09 to 1:40 - and the
    # hook Harry stopped for is first heard at 2:06, more than two minutes in) THE HOOK, GLIMPSED: at the end of the
    # gather the near voice sings the crest's line once, from far off - 'nearer each time it comes round', alone, no
    # third above, low in level, darker and deep in the hall, as if heard from the other side of the disk - so the
    # listener has it in their ear before the pre-chorus; when the crest sings it close, with its third and the
    # ondes, it is a return, not a first meeting. The infall's whole idea: each time round, nearer
    eh_ = [dict(n_, at=round(29 * 4.0 + n_['at'] - 0.25, 4), vel=round(n_.get('vel', 0.8) * 0.8, 3)) for n_ in CS['tracks'][0]['notes']]
    CB = json.load(open(os.path.join(HERE, 'chirpers9-t2-crestb.json')))
    cbnotes = []
    for b_, g_ in (((CREST + 8) * 4.0, 1.0), ((CREST + 12) * 4.0, 0.9)):
        for n_ in CB['tracks'][0]['notes']:
            cbnotes.append(dict(n_, at=round(b_ + n_['at'] - 0.245, 4), vel=round(n_['vel'] * g_, 3)))
    # (v24, whole song) THE LAST CHORUS: Harry, 6 Nov 18:05, at the crest's words: 'woah this track is sick'. So the
    # line comes back to end the song: in the drift, where the ondes plays E1 plainly over the returning drums (bars
    # 85-96), the near voice sings 'nearer each time it comes round' with it four times - every other statement, the
    # ondes answering alone between - with its third above now in D Dorian (the drift is Dorian again: F, C, E, B, G
    # over D A C G E), each time a little louder, the last landing on the fall. The voice's arc is now: chorus at the
    # crest -> whispered memory -> found alone at the end of the break -> the last chorus, home
    # (v26, whole song) A VERSE BEFORE THE CHORUS: Harry loved the crest's words; but nobody sang until 2:06. Now the
    # near voice sings a verse in the gather, alone (no harmony: the chorus keeps that), on E2's own notes - the
    # debris's D A F C - 'all that falls / falls a little nearer', twice (bars 21-22 and 25-26), so the crest's
    # 'nearer each time it comes round' answers it: verse -> chorus, the song shape Harry's ear wants under the process
    V1 = json.load(open(os.path.join(HERE, 'chirpers9-t2-verse1.json')))
    V2 = json.load(open(os.path.join(HERE, 'chirpers9-t2-verse2.json')))
    vsnotes = []
    for b_ in (80.0, 96.0):
        for n_ in V1['tracks'][0]['notes']:
            vsnotes.append(dict(n_, at=round(b_ + n_['at'] - 0.25, 4)))
        for n_ in V2['tracks'][0]['notes']:
            vsnotes.append(dict(n_, at=round(b_ + 4.0 + n_['at'] - 0.25, 4)))
    # (v36, whole song) THE SECOND VERSE: the song had one verse and then only its chorus. Now, as the drums come back
    # at half speed after the break (bars 81-85), the same near voice sings a SECOND verse on the first's tune (D A F,
    # F A F C D D) with the next thought - 'all that turns / turns a little faster' (Kepler, what the pre-chorus
    # promised: the nearer, the faster) - twice, the second time as the drift's own groove arrives; then the last
    # chorus. The form is now verse -> pre-chorus -> chorus -> break -> verse -> chorus -> fall
    V3 = json.load(open(os.path.join(HERE, 'chirpers9-t2-verse3.json')))
    V4 = json.load(open(os.path.join(HERE, 'chirpers9-t2-verse4.json')))
    for b_, g_ in ((322.0, 0.95), (336.0, 1.0)):
        for n_ in V3['tracks'][0]['notes']:
            vsnotes.append(dict(n_, at=round(b_ + n_['at'] - 0.245, 4), vel=round(n_['vel'] * g_, 3)))
        for n_ in V4['tracks'][0]['notes']:
            vsnotes.append(dict(n_, at=round(b_ + 4.0 + n_['at'] - 0.245, 4), vel=round(n_['vel'] * g_, 3)))
    dsnotes = []
    dsnotes2 = []
    for k_, b_ in enumerate((346.0, 356.0, 366.0, 376.0)):
        for n_ in CS['tracks'][0]['notes']:
            (dsnotes if k_ < 3 else dsnotes2).append(dict(n_, at=round(b_ + n_['at'] - 0.25, 4), vel=round(min(1.0, n_.get('vel', 0.8) * (0.82 + 0.06 * k_)), 3)))
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
    P['e1v'] = [e_ for e_ in P['e1c'] if e_[0] < fall0 - 1e-6]
    P['e1c'] = [e_ for e_ in P['e1c'] if e_[0] >= fall0 - 1e-6]

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
    # (v18) and in the crest's twelve bars every F the cell and its bass play becomes F# (the lit mode), and the
    # bass's cell on G takes F# for its seventh
    c0_, c1_ = CREST * 4.0, (CREST + 12) * 4.0
    def lit_(p_):
        base_, sep_, attr_ = p_.partition('^')
        n_ = float(base_[1:])
        if abs(n_ - round(n_)) < 1e-6 and int(round(n_)) % 12 == 5:
            n_ += 1
        return m(n_) + sep_ + attr_
    for key_ in ('e2m', 'e2body', 'dust', 'bass'):
        P[key_] = [((a_, lit_(p_), d_, v_) if c0_ - 1e-6 <= a_ < c1_ - 1e-6 else (a_, p_, d_, v_)) for a_, p_, d_, v_ in P[key_]]
    for key_, sc_ in (('e2m', 1.0), ('e2body', 0.5), ('dust', 1.0)):
        P[key_] = [(a_, f"{p_}^px={spiral(a_, sc_):.2f}", d_, v_) for a_, p_, d_, v_ in P[key_]]
    PXF = {'type': 'pan', 'pan': {'value': 0, 'mod': [{'src': 'expr.px', 'amount': 1}]}}

    # (v44, whole song: t2 played dead straight from first bar to last - a machine's grid under a sung song) THE INFALL
    # SHUFFLES: once t1's tail has gone (bar 17) and until the fall (bar 97), the groove's parts - both drummers, the
    # lofi hats, the triangle bass, the cutting guitar and E2's log drum and chip debris - play a 16th shuffle (the
    # engine's swing16, never used on the album): every off-beat sixteenth lands late, the lazy lean of a lofi/IDM
    # drummer; the seams, the voices and the pads stay straight
    SWUNG = ('kit', 'kitb', 'hat3', 'bass', 'gtr', 'gtrd', 'e2body', 'e2m')
    # (v45, whole song: t2 sat between a light neighbour and a heavy one - t1's body has almost nothing at 38 Hz, t3's
    # floor is a3-deep on D1 - and its own D1 sub held one weight from the gather to the fall; compscore heard it as
    # the seams' worst band, +25 dB against t1 and -23 dB against t3) GRAVITY GROWS: the infall's pull deepens as it
    # falls - the sub is all but gone in the gather (after the in-seam's agreed D1 pedal), comes in through the build,
    # is full at the crest, lifts away in the break (floating), and is heaviest in the drift and the fall, so t2 hands
    # t3 the depth t3 starts from. The same notes; only how much the floor weighs
    # (v47) chirper-zero: the gather at -12 dB cost t1's out-flow 74.5 -> 71.6 (t2's head 2.5 dB under t1's body), so
    # the gather starts lighter but not empty
    # (v48) chirper-zero: t1 v41 took its pad down 6 dB, so -4 might overshoot; measured from t2's side -8 read worse
    # (in-flow level jump 0.9 dB against 0.6 at -4), so the gather stays at -4
    GRAV = {'in': (0.0, 0.0), 'gather': (-4.0, -5.0), 'build': (-5.0, -1.0), 'crest': (0.0, 0.0), 'break': (-6.0, -3.0),
            'drift': (1.0, 3.0), 'fall': (3.0, 3.0)}
    grav_pts = []
    for b_ in range(NBARS):
        s_, i_ = sec_of(b_)
        a_, z_ = GRAV[s_]
        grav_pts.append([f'{b_ * 4.0:.1f}b', round(a_ + (z_ - a_) * i_ / 15.0, 2)])
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': swung(line(P[name], total), SEC['gather'] * 4.0, fall0, 0.62) if name in SWUNG else line(P[name], total)}, **kw)
    PAD = {'extends': 'kuramoto-choir',
           'synth': {'layers': [{'type': 'kuramoto', 'kuramoto': {'count': 10, 'spread': 12, 'wave': 'saw',
                                 'coupling': {'value': 0.0, 'mod': [{'src': 'auto.lock', 'amount': 1.0}]}}}]}}
    # (v29, whole song) THE DRUMMER BREATHES AT EVERY PHRASE END: Harry, 6 Nov 23:55 - 'subtle variation so it
    # doesnt get boring'; eco: brief fills, one-bar drop-outs and turnarounds are what he means. So the last bar of
    # every eight in the gather, the build, the crest and the drift's first half now does one of three things, in
    # turn: a FILL (beat 4 in rising 909 snare sixteenths, the kick out under it), a DROP (no kick for the bar, the
    # hats and the bass carrying it, and a crash on the next downbeat), or a TURNAROUND (an open hat on the and of 4,
    # a clap flam, and the NES bass stepping up to the next chord's fifth on the and of 4). Never the same twice in a
    # row; the groove, the key and the parts are otherwise untouched
    ph_ = 0
    for bar_ in range(SEC['gather'], SEC['drift'] + 8):
        s_, i_ = sec_of(bar_)
        if i_ % 8 != 7 or s_ not in ('gather', 'build', 'crest', 'drift') or bar_ in (46, 47, 79):
            continue
        b0_, b1_ = bar_ * 4.0, (bar_ + 1) * 4.0
        kind_ = ph_ % 3
        ph_ += 1
        if kind_ == 0:
            P['kit'] = [e_ for e_ in P['kit'] if not (b0_ + 3.0 - 1e-6 <= e_[0] < b1_ - 1e-6 and e_[1] in ('k', 's', 'cp'))]
            for q_ in range(4):
                P['kit'].append((b0_ + 3.0 + q_ * 0.25, 's', 0.1, 70 + 12 * q_))
        elif kind_ == 1:
            P['kit'] = [e_ for e_ in P['kit'] if not (b0_ - 1e-6 <= e_[0] < b1_ - 1e-6 and e_[1] == 'k')]
            P['kit'].append((b1_, 'c', 2.0, 104))
        else:
            P['kit'].append((b0_ + 3.5, 'oh', 0.3, 80))
            P['kit'].append((b0_ + 3.0, 'cp', 0.2, 84))
            P['kit'].append((b0_ + 3.06, 'cp', 0.2, 100))
            rn_ = chord(bar_ + 1)[0]
            P['bass'].append((b0_ + 3.5, m(KEY + rn_ + 7 - (12 if rn_ + 7 > 5 else 0)), 0.45, 92))
    P['kit'].sort(key=lambda e_: e_[0]); P['bass'].sort(key=lambda e_: e_[0])

    # (v32, palette: 'add the part the song lacks') A GUITAR COMPS: t2 had pads, bells, a wurli, chips and voices but
    # nothing playing the chords in time - the thing a band's guitarist does. Now a clean, compressed, chorused Tele
    # (the library's cutting-guitar, which no Accretion track uses) plays short chord stabs: in the gather's second
    # half only the skank (the ands of 2 and 4), in the build and the crest a sixteenth-note funk figure (the a of 1,
    # the and and a of 2, the and of 3, the and of 4), out for the break (bells and the far choir), the skank again
    # as the drift comes back, the funk figure from the drift's own groove, silent where the floor falls away, and
    # gone for the fall. Each chord voiced in G3-D5, the voicing nearest the last, so the comp moves by step
    P['gtr'] = []
    prev_ = 64.0
    SKANK, FUNK = [6, 14], [3, 6, 7, 10, 14]
    for bar_ in range(24, SEC['fall']):
        s_, i_ = sec_of(bar_)
        if s_ == 'break' or 91 <= bar_ < 94:
            continue
        pat_ = SKANK if (s_ == 'gather' or (s_ == 'drift' and i_ < 4)) else FUNK
        rt_, iv_ = chord(bar_)
        pcs_ = sorted({(KEY + rt_ + v_) % 12 for v_ in [0] + list(iv_)})
        best_ = None
        for lo_ in range(55, 64):
            vo_ = sorted(lo_ + ((pc_ - lo_) % 12) for pc_ in pcs_)
            vo_ = [n_ for n_ in vo_ if n_ <= 74][:4]
            c_ = sum(vo_) / len(vo_)
            if best_ is None or abs(c_ - prev_) < abs(best_[0] - prev_):
                best_ = (c_, vo_)
        prev_ = best_[0]
        ch_ = ','.join(m(n_) for n_ in best_[1])
        for q_ in pat_:
            acc_ = q_ in (6, 14)
            P['gtr'].append((bar_ * 4.0 + q_ * 0.25, ch_, 0.3, (84 if acc_ else 66) + (8 if s_ == 'crest' else 0)))
    P['gtr'] = [e_ for e_ in P['gtr'] if not (91.0 * 4.0 - 1e-6 <= e_[0] < 94.0 * 4.0 - 1e-6)]
    # (v38, section w6: 2:37-3:07, the break's first twelve bars - pad, bass, debris, the bells' retrograde and the
    # far choir, nothing in time above the debris) THE GUITAR FLOATS: the guitar that comped through the build and
    # the crest doesn't leave for the break - it stops comping and rings out each chord as a slow broken chord, up
    # and back down in eighths (four notes up, two down), soft, through a long ping-pong echo, so every note trails
    # behind it like the debris does: the band's rhythm instrument turned into weather. Twelve bars, then it thins
    # (every other bar) as the break climbs out, and stops where the drums come back
    P['gtrarp'] = []
    prev_ = 64.0
    for bar_ in range(SEC['break'], SEC['break'] + 16):
        rt_, iv_ = chord(bar_)
        pcs_ = sorted({(KEY + rt_ + v_) % 12 for v_ in [0] + list(iv_)})
        best_ = None
        for lo_ in range(52, 62):
            vo_ = sorted(lo_ + ((pc_ - lo_) % 12) for pc_ in pcs_)
            vo_ = [n_ for n_ in vo_ if n_ <= 76][:4]
            c_ = sum(vo_) / len(vo_)
            if best_ is None or abs(c_ - prev_) < abs(best_[0] - prev_):
                best_ = (c_, vo_)
        prev_ = best_[0]
        vo_ = best_[1]
        seq_ = vo_ + vo_[-2:0:-1]
        if bar_ - SEC['break'] >= 12 and (bar_ - SEC['break']) % 2 == 1:
            continue
        for q_ in range(8):
            n_ = seq_[q_ % len(seq_)]
            P['gtrarp'].append((bar_ * 4.0 + q_ * 0.5, m(n_), 0.45, (70 if q_ == 0 else 56) - (6 if bar_ - SEC['break'] >= 12 else 0)))

    # (v54, section w4: 1:35-2:06, the build, 'little new vs w3' - the same groove, flute and debris as the second
    # verse, only the bass climbing) THE ORBIT TIGHTENS: as the build climbs (Dm9, Fmaj9, G6/9, A7sus4) a bright
    # plucked synth arpeggiates each chord, up through it and round again, and it speeds up as the crest nears -
    # eighths for the first four bars, triplets for the next four, sixteenths for the last four - each a little
    # louder: 'the nearer, the faster' played rather than sung. The library's arp-pluck, which no Accretion track
    # uses. The flute's E1 steps aside for the triplets and sixteenths (bars 41-48); it stops for the door like
    # everything else
    P['buildarp'] = []
    prev_ = 70.0
    for bar_ in range(36, 48):
        rt_, iv_ = chord(bar_)
        pcs_ = sorted({(KEY + rt_ + v_) % 12 for v_ in [0] + list(iv_)})
        best_ = None
        for lo_ in range(62, 70):
            vo_ = sorted(lo_ + ((pc_ - lo_) % 12) for pc_ in pcs_)[:4]
            c_ = sum(vo_) / len(vo_)
            if best_ is None or abs(c_ - prev_) < abs(best_[0] - prev_):
                best_ = (c_, vo_)
        prev_ = best_[0]
        vo_ = best_[1]
        div_ = 2 if bar_ < 40 else (3 if bar_ < 44 else 4)
        for q_ in range(4 * div_):
            n_ = vo_[q_ % len(vo_)] + (12 if (q_ // len(vo_)) % 2 == 1 and div_ == 4 else 0)
            P['buildarp'].append((bar_ * 4.0 + q_ / div_, m(n_), 0.8 / div_, int(52 + 2.2 * (bar_ - 36)) + (8 if q_ % div_ == 0 else 0)))
    P['e1p'] = [e_ for e_ in P['e1p'] if not (160.0 - 1e-6 <= e_[0] < 192.0 - 1e-6)]

    # (v25, section w8: the drift 'static' - one groove under the last chorus to the end) THE FLOOR FALLS AWAY FOR THE
    # THIRD TIME: at the last chorus's third statement (bars 92-94) the band drops out - no kit, no hats, no debris,
    # no bass, no sub - and only the voice, the ondes, the pad and the bells are left, the line sung nearly alone;
    # then half a bar of 909 snare in sixteenths, rising, and the whole band lands with the fourth and last statement
    # (bar 95), which carries the song into the fall. The arrangement breathes the way the words do
    bd0_, bd1_, bd2_ = 91.0 * 4.0, 93.5 * 4.0, 94.0 * 4.0
    for key_ in ('kit', 'hat3', 'e2m', 'e2body', 'dust', 'bass', 'sub'):
        P[key_] = [e_ for e_ in P[key_] if not (bd0_ - 1e-6 <= e_[0] < bd2_ - 1e-6)]
    for q_ in range(8):
        P['kit'].append((bd1_ + q_ * 0.25, 's', 0.1, 64 + 6 * q_))
    P['kit'].append((bd2_, 'k', 0.2, 124))
    P['kit'].append((bd2_, 'c', 2.0, 110))
    for key_ in ('bass', 'sub'):
        # the notes already sounding when the floor falls away stop with it (the bar-95 ones are the band's return)
        P[key_] = [(e_[0], e_[1], min(e_[2], bd0_ - e_[0]), *e_[3:]) if e_[0] < bd0_ < e_[0] + e_[2] else e_ for e_ in P[key_]]
    for key_ in ('kit', 'bass', 'sub'):
        P[key_].sort(key=lambda e_: e_[0])
    # (v28, whole song) THE LAST CHORUS LIFTS: after the breakdown and the snare pickup, the fourth and last statement
    # of the line comes back a whole tone UP - the band, the bass, the pad, the debris, the ondes and the voices all in
    # E Dorian for those two bars (the voices' third above follows the key: harmony_key E Dorian) - the pop record's
    # last-chorus lift, landed on the crash; and then the fall drops the song back into D with t3's chords: the lift
    # is the last thing before the infall, so the fall is a real fall
    lf0_, lf1_ = 94.0 * 4.0, 96.0 * 4.0
    def lift_(ev_):
        if not isinstance(ev_[1], str) or not re.match(r'm\d', ev_[1]):
            return ev_
        return (ev_[0], re.sub(r'm(\d+(?:\.\d+)?)', lambda q_: f"m{float(q_.group(1)) + 2:.3f}", ev_[1]), *ev_[2:])
    for key_ in list(P.keys()):
        if key_ in ('kit', 'hat3'):
            continue
        P[key_] = [lift_(e_) if lf0_ - 1e-6 <= e_[0] < lf1_ - 1e-6 else e_ for e_ in P[key_]]

    # (v31, whole song) THE CREST ARRIVES: compscore's sections showed what a listener feels - from the second verse to
    # the break (1:05-2:50) the song is one long climb with no door in it: the build and the crest blur, because the
    # light opens gradually all the way to the crest. Now the crest has a door: after the snare ladder the whole band
    # stops for the last beat before it - one beat of nothing but the hall ringing - and the light, held back since
    # bar 37 (the low-pass now opening only to about 9 kHz through the build, no longer all the way), comes fully ON
    # with the crash and the sung line. The breath before the drop, here the moment the infall reaches the middle.
    # (Holding the build darker still, to 4.5 kHz, cost more than it gave: 30 s of a dull band)
    gp0_, gp1_ = CREST * 4.0 - 1.0, CREST * 4.0
    for key_ in list(P.keys()):
        P[key_] = [e_ for e_ in P[key_] if not (gp0_ - 1e-6 <= e_[0] < gp1_ - 1e-6)]
        P[key_] = [(e_[0], e_[1], min(e_[2], gp0_ - e_[0]), *e_[3:]) if (len(e_) > 2 and isinstance(e_[2], (int, float)) and e_[0] < gp0_ < e_[0] + e_[2]) else e_ for e_ in P[key_]]
    # (v40, palette: the 909 played the whole song) THE DRIFT IS A BREAK: after the break, when the drums come back at
    # half speed for the second verse, they come back as a different drummer - the library's break-kit (an Amen-style
    # funk kit as a sampler hears it, squashed and gritty; no Accretion track uses it) for the whole drift: the
    # half-time return, the groove under the last chorus, the floor falling away and the snare pickup into the lift.
    # The 909 keeps everything before the break, and the fall's heartbeat into t3; the clap becomes the break's
    # snare. IDM's two drummers: the clean machine for the infall, the dusty break for the drift
    dr0_ = SEC['drift'] * 4.0
    P['kitb'] = [((e_[0], 's' if e_[1] == 'cp' else e_[1]) + tuple(e_[2:])) for e_ in P['kit'] if dr0_ - 1e-6 <= e_[0] < fall0 - 1e-6]
    P['kit'] = [e_ for e_ in P['kit'] if not (dr0_ - 1e-6 <= e_[0] < fall0 - 1e-6)]
    # (v62, section w7: 3:07-3:37, the break climbing out into the drift - the bass alone carrying it (-1 dB), the
    # line's return at bar 77 sung over a floating guitar and a hum, nothing in it from the crest it remembers) THE
    # ONDES FINDS HER: the ondes Martenot that sang E1 with the voice at the crest comes back for the climb-out - first
    # alone, softly, once through E1 at its own speed over the C and F (bars 73-74), like something remembered, then
    # doubling the voice's line note for note when she sings 'nearer each time it comes round' at bar 77, as it did at
    # the crest (Harry: the near voice with the ondes); it lets go as the drift's drums come back
    t_ = (SEC['break'] + 8) * 4.0
    at = t_
    for k, (semi, ln) in enumerate(E1):
        if semi is not None:
            P['hook'].append((at, m(KEY + 24 + semi), ln * 0.97, 70 if k == 0 else 62))
        at += ln
    for n_ in snotes:
        if (SEC['break'] + 12) * 4.0 - 0.5 <= n_['at'] < SEC['drift'] * 4.0:
            P['hook'].append((n_['at'], n_['pitch'], n_['len'] * 0.97, int(80 * n_.get('vel', 0.8) + 10)))
    P['hook'].sort(key=lambda e_: e_[0])
    answers = []
    # (v63, section w8: 3:37-4:07, the drift's last chorus - three statements of the line over the ondes' E1 and the
    # last choir, the same answer-less shape the crest had before v61) THE CHOIR ANSWERS AGAIN: in the last chorus
    # the congregation answers each of the first three 'nearer each time it comes round' with 'comes round' - the
    # third answer sung into the floor's falling away (bars 93-94), voices alone in the gap before the lift to E
    ANS_ = [(csnotes, 194.9, 197.0, 198.5), (cbnotes, 232.9, 235.0, 237.0), (cbnotes, 248.9, 251.0, 253.0)]
    ANS_ += [(dsnotes, b_ + 2.6, b_ + 4.9, b_ + 6.5) for b_ in (346.0, 356.0, 366.0)]
    # (the drift is D Dorian - its F natural under the answers - so its answers sing on their own track, 'answer2')
    for src_, a0_, a1_, to_ in ANS_:
        grp_ = [n_ for n_ in src_ if a0_ <= n_['at'] < a1_]
        if not grp_:
            continue
        off_ = to_ - grp_[0]['at']
        for n_ in grp_:
            answers.append(dict(n_, at=round(n_['at'] + off_, 4), len=round(min(n_['len'], 1.9), 4), vel=round(n_.get('vel', 0.7) * 0.85, 3)))
    # (v67, section w3: 1:03-1:35, the gather's second verse and the build's first four bars - the gather's groove
    # simply ran on across the build's first bar line, the build only beginning with its arp at bar 37) THE BUILD
    # STARTS FROM THE FLOOR: at bar 33 the drums, the hats and the comp drop away for three bars and a half, leaving
    # the chip bass, the sub, the swarm pad, E2's debris and the flute's E1 - the song's matter without its engine;
    # then the 909's snare rolls it back in, eighths and then sixteenths, rising from a whisper (bars 35.5-36), and
    # the kit lands with the arp at bar 37
    # (v72, section w2: 0:32-1:03, the end of the in-seam and the gather's first eight bars - never focused: when the
    # overlap ends and the band arrives at bar 17 there was only the kit, the debris and the pad for four bars before
    # the verse, nothing to hum) THE HOOK ARRIVES WITH THE BAND: as the kit comes in, the ondes - the voice Harry
    # heard singing with the crest - plays E1 twice, softly, D A C G E in its five beats, the second time a little
    # quieter, and is gone before the verse begins; the crest's tune heard first as the song's own sign-on
    # (v74, for chirper-zero: two statements cost t1's out-flow -0.18/-0.21 - the ondes' 342 Hz in t2's body just
    # after the overlap, the 3 s the seam is measured on - so the ondes plays E1 once, entering a bar and a beat after
    # the kit, where the second statement was: the kit lands first, then the tune)
    for k0_, vel0_ in ((SEC['gather'] * 4.0 + 5.0, 46),):
        at_ = k0_
        for k, (semi, ln) in enumerate(E1):
            if semi is not None:
                P['hook'].append((at_, m(KEY + 24 + semi), ln * 0.97, vel0_ + (8 if k == 0 else 0)))
            at_ += ln
    P['hook'].sort(key=lambda e_: e_[0])
    P['hat3'] = [(e_[0], 'gz' if str(e_[1]).partition('^')[0] == 'h' else 'pd', *e_[2:]) for e_ in P['hat3']]
    dp0_, dp1_ = SEC['build'] * 4.0, SEC['build'] * 4.0 + 16.0
    # (v70, whole song) THE MACHINES AND THE HANDS: every part of the song played at two or three fixed levels on a
    # perfect grid. The song is about a mechanism - E2's clock, the 3-beat hats, E1's 5/4 and the band's 4 all landing
    # on one downbeat at the crest - so the machines keep their time exactly: E2, the hats, the 909, the arp and the
    # chip bass do not move by a sample. But the 909 and the hats get a drum machine's accents (each hit's level
    # moves a few steps, and they lean into every 4-bar phrase), and the players get hands: the drift's break-kit
    # (laid back: its snares 10 ms behind, everything else within a few ms), the electric piano's comp, the scanned
    # mallet and the flute land within a couple of ms of the beat, their levels moving and leaning with the phrase;
    # the ondes and the bells keep their written timing and only breathe in level. Seeded, so every render is the same
    import random as _r
    rh_ = _r.Random(70)
    for k_, jit_, late_, lean_amt_, vsd_ in (('kit', 0.0, 0.0, 4.0, 3.0), ('hat3', 0.0, 0.0, 6.0, 3.0),
                                             ('kitb', 0.005, 0.02, 4.0, 3.0), ('gtr', 0.004, 0.0, 4.0, 2.5),
                                             ('e1v', 0.004, 0.0, 4.0, 2.5), ('e1p', 0.004, 0.0, 4.0, 2.5),
                                             ('hook', 0.0, 0.0, 0.0, 2.0), ('e1c', 0.0, 0.0, 0.0, 2.0)):
        if k_ not in P:
            continue
        ev_ = []
        for e_ in P[k_]:
            at_, p_, d_, v_ = e_[:4]
            pc_ = str(p_).partition('^')[0]
            if pc_ == 'k':
                dt_ = 0.0
            elif pc_ in ('s', 'cp', 'rs') and late_:
                dt_ = late_
            else:
                dt_ = max(-2.5 * jit_, min(2.5 * jit_, rh_.gauss(0, jit_))) if jit_ else 0.0
            ln_ = lean_amt_ * ((at_ % 16.0) / 16.0) * 2.0 - lean_amt_ if lean_amt_ else 0.0
            ev_.append((max(0.0, at_ + dt_), p_, d_, max(1, min(127, int(round(v_ + ln_ + rh_.gauss(0, vsd_)))))) + tuple(e_[4:]))
        P[k_] = ev_
    for k_ in ('kit', 'hat3', 'gtr'):
        P[k_] = [e_ for e_ in P[k_] if not (dp0_ - 1e-6 <= e_[0] < dp1_ - 1e-6)]
    roll_ = [dp1_ - 6.0 + 0.5 * i_ for i_ in range(4)] + [dp1_ - 4.0 + 0.25 * i_ for i_ in range(16)]
    for i_, at_ in enumerate(roll_):
        P['kit'].append((at_, 's', 0.12, int(36 + 80 * (i_ / (len(roll_) - 1)) ** 1.4)))
    P['kit'].sort(key=lambda e_: e_[0])
    # (v84, palette: the drift's comping - the flattest change in the song by eco's flatness map, 3:44, bars 85-91 -
    # was the same Rhodes-style epiano that comps the gather and the crest) THE DRIFT ON A GUITAR: from the drift to
    # the fall the comping moves to the library's clean-dry (a dry, dark, close-miked clean electric through a Twin
    # barely breaking up; no Accretion track uses it), the same voicings and the same hands - a guitarist sitting in
    # for the second verse, so the drift is its own room; the gather and the crest keep the epiano
    P['gtrd'] = [e_ for e_ in P['gtr'] if SEC['drift'] * 4.0 - 1e-6 <= e_[0] < fall0 - 1e-6]
    P['gtr'] = [e_ for e_ in P['gtr'] if not (SEC['drift'] * 4.0 - 1e-6 <= e_[0] < fall0 - 1e-6)]
    song = {
        'about': "chirpers - Accretion, track 2 by chirper-one: The Long Way In. The infall: a rhythm cell in seven "
                 "assembles out of falling fragments against the band's sixteen, every cycle landing together at the crest. "
                 "Generated by compose/chirpers9/src/chirpers9-t2.py.",
        'tempo': tempo, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.5s', 'seed': SEED,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.8s mix=1 mono_below=200', 'hp cutoff=220'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.42, 'mix': 1, 'ping_pong': True},
                                  'lp cutoff=5000', 'hp cutoff=300'], 'returns': []}},
        # (v19) and air: t2 measured 20 dB darker than t1 at 15 kHz and 14 dB darker than t3 at 9 kHz - a second,
        # higher shelf opens the top so the song breathes like its neighbours
        # (v43, whole song: against the album, t2 was thin where a groove's weight lives - 44-133 Hz 4-8 dB under the
        # album's envelope, 342-641 Hz 4 dB over: the NES bass's body lost under boxy mids) THE FLOOR GETS ITS WEIGHT:
        # a low shelf (+3.5 dB below 120 Hz) and a second mid cut (520 Hz, -2 dB) on the master, the triangle bass 2 dB
        # up - the same parts and the same line, but the bass now carries the groove instead of ticking under it
        # (v75, whole song) THE ROOM AROUND IT: measured against the album, t2 was a boxy, dark song with a thin floor -
        # 60-115 Hz 4-6 dB under the others (since v64's quieter chip bass), 210-470 Hz 3-5 dB over (the voices, the
        # comp and the choirs' chests all piling up there), and the air above 6 kHz 3-7 dB short. The master now
        # gives the floor its weight back under the bass and the kick (+3 dB around 75 Hz), takes the box out
        # (-3 dB around 340 Hz, -1.5 at 470) and opens the top (+3 dB above 13 kHz): the same mix, heard in a bigger room
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'lowshelf cutoff=120 gain=3.5dB', 'peak cutoff=75 q=0.9 gain=3dB', 'peak cutoff=300 q=0.8 gain=-2dB', 'peak cutoff=340 q=0.8 gain=-3dB', 'peak cutoff=520 q=0.8 gain=-2dB', 'peak cutoff=470 q=1.0 gain=-1.5dB', 'highshelf cutoff=7000 gain=2dB', 'highshelf cutoff=11000 gain=4.5dB', 'highshelf cutoff=13000 gain=3dB']},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.0, 'attack': '20ms', 'release': '160ms', 'makeup': '1dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.E', 'amount': 1}]}},
                          {'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 1200, 'mod': [{'src': 'auto.open', 'amount': 4.0}]}},
                          {'type': 'pan', 'width': {'value': 0, 'mod': [{'src': 'auto.WID', 'amount': 1}]}},
                          'limiter ceiling=-1dB'], 'auto': {'E': {'points': energy_pts}, 'open': {'points': open_pts}, 'WID': {'points': wid_pts}}},
        'tracks': [
            tr('pad', PAD, '-15dB', auto={'lock': {'points': lock_pts}, 'shut': {'points': padshut_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 600, 'mod': [{'src': 'auto.shut', 'amount': 3.5}]}}],
               sends={'hall': '-8dB'}),
            # (v19) the D1 sub 4 dB down: the t1 -> t2 mix seam read t2 28 dB over t1's body at 38 Hz
            tr('sub', 'sub', '-13dB', auto={'grav': {'points': grav_pts}}, fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '220ms', 'curve': 0.6},
                                                 {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.grav', 'amount': 1}]}}]),
            # (tried in v15: moog-seq for the staple NES bass - the sections blurred into each other, structure 100 -> 84,
            # spectrum 98 -> 94; the chip bass's dry edge is what tells the sections apart)
            tr('bass', 'nes-triangle-bass', '-4dB', fx=['lp cutoff=2400']),
            tr('kit', '909', '-6dB', sends={'hall': '-20dB'},
               auto={'glitch': {'points': [['0b', 0.0], [f"{(CREST + 8) * 4.0 - 0.1:.1f}b", 0.0], [f"{(CREST + 8) * 4.0:.1f}b", 0.35],
                                           [f"{(CREST + 12) * 4.0 - 0.1:.1f}b", 0.35], [f"{(CREST + 12) * 4.0:.1f}b", 0.0], [f"{SEC['drift'] * 4.0 - 0.1:.1f}b", 0.0], [f"{SEC['drift'] * 4.0:.1f}b", 0.22], [f"{84 * 4.0 - 0.1:.1f}b", 0.26], [f"{84 * 4.0:.1f}b", 0.0], [f"{fall0:.1f}b", 0.0]]}},
               fx=[{'type': 'stutter', 'slice': '1/16', 'repeats': 3, 'chance': {'value': 0.0, 'mod': [{'src': 'auto.glitch', 'amount': 1.0}]}, 'seed': 5}]),
            tr('kitb', 'break-kit', '-12dB', sends={'hall': '-20dB'},
               auto={'glitch': {'points': [['0b', 0.0], [f"{(CREST + 8) * 4.0 - 0.1:.1f}b", 0.0], [f"{(CREST + 8) * 4.0:.1f}b", 0.35],
                                           [f"{(CREST + 12) * 4.0 - 0.1:.1f}b", 0.35], [f"{(CREST + 12) * 4.0:.1f}b", 0.0], [f"{SEC['drift'] * 4.0 - 0.1:.1f}b", 0.0], [f"{SEC['drift'] * 4.0:.1f}b", 0.22], [f"{84 * 4.0 - 0.1:.1f}b", 0.26], [f"{84 * 4.0:.1f}b", 0.0], [f"{fall0:.1f}b", 0.0]]}},
               fx=[{'type': 'stutter', 'slice': '1/16', 'repeats': 3, 'chance': {'value': 0.0, 'mod': [{'src': 'auto.glitch', 'amount': 1.0}]}, 'seed': 5}]),
            # (v9) presence.py had the three-beat hats 33 dB under the mix - the polymeter you couldn't hear
            # (v37, palette: the 909's hats are the haake-hat, an album staple - t2, t3, t5 and t6 all tick on it) THE HATS
            # GO DUSTY: the three-beat hat cycle (x.xx.x.xx.x. against the band's four) now plays on the library's
            # lofi-kit - soft, rounded hats through a worn sampler, low-passed and saturated - which no Accretion track
            # uses: the polymeter's top line warmer and grainier against the 909's clean kick and snare (the master's
            # air shelf at 11 kHz up 1.5 dB to 4.5 dB: the low-passed hats took 1.5 dB of 15 kHz with them)
            # (v79, palette: the hats' three-beat orbit - one of the four cycles that meet at the crest - was a lo-fi
            # drum machine's hat, buried at -12 to -20 dB under the 909) THE ORBIT ON A SHAKER: it is now the
            # library's samba-kit, played by hand - a ganzá (the metal shaker) for every step, its accent on the
            # cycle's open step a pandeiro's jingles - which no Accretion track uses: the three-against-four you could
            # barely hear now shakes in the right of the room, organic against the 909's machine
            tr('hat3', 'samba-kit', '-3dB', pan=0.25, sends={'echo': '-20dB'}),
            tr('infall', 'shepard-fall', '-20dB', sends={'hall': '-16dB'}),
            tr('hook', 'ondes', '-5dB', pan=-0.05, sends={'hall': '-12dB', 'echo': '-20dB'}),
            # (v52, palette: the debris's glints were wind-chimes, buried under the groove at -20 to -26 dB) THE DUST
            # CRYSTALLISES: the glints the E2 cell throws off now strike on the library's fb-crystal (chirper-three's
            # Ferrous Bloom crystal: an inharmonic chime strike over a sustained near-harmonic body; no Accretion track
            # uses it) - accretion's first step, dust becoming crystal, catching the light three octaves up, still
            # spiralling round the stereo field; heard now, not buried
            tr('dust', {'extends': 'fb-crystal', 'synth': {'fx': [PXF]}}, '-28dB', auto={'shut': {'points': shut_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 3000, 'mod': [{'src': 'auto.shut', 'amount': 3.0}]}}],
               sends={'echo': '-14dB'}),
            tr('e2m', {'extends': 'chip-metal', 'synth': {'fx': [PXF]}}, '-14dB', auto={'shut': {'points': shut_pts}},
               fx=['hp cutoff=500', {'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 900, 'mod': [{'src': 'auto.shut', 'amount': 3.5}]}}],
               sends={'echo': '-12dB', 'hall': '-14dB'}),
            tr('e2body', {'extends': 'log-drum', 'play': {'legato': False, 'mono': False, 'glide': '0ms'}, 'synth': {'fx': [PXF]}}, '-9dB',
               sends={'hall': '-18dB'}),
            # (v71, palette: the engine's Risset rhythm, which no Accretion track uses) THE APPROACH NEVER ARRIVES: under
            # the build - from the floor's opening at bar 33 to the crest - E2's cell on the log drum plays as a Risset
            # accelerando: three copies an octave of tempo apart, each doubling its speed every four bars while the
            # fastest fades out and the slowest fades in, so the debris speeds up for sixteen bars and never gets
            # faster; and each copy rises in pitch with its speed (an octave per doubling, so always D A F C), a
            # blueshift - the approach heard as it is in the sky, quicker and higher - until the crest lands on it
            {'name': 'approach', 'patch': {'extends': 'log-drum', 'play': {'legato': False, 'mono': False, 'glide': '0ms'}},
             'gain': '-11dB', 'pan': 0.0, 'at': f"{SEC['build'] * 4.0:g}b",
             'risset': {'cycle': '4bar', 'layers': 3, 'length': '16bar', 'pitch': True},
             'sends': {'hall': '-14dB'}, 'score': f"{m(KEY + 12)}/0.5b@100 {m(KEY + 19)}/0.25b@70 {m(KEY + 15)}/0.5b@88 {m(KEY + 10)}/0.5b@72"},
            tr('e1in', 'risset-bell', '-12dB', pan=0.15, auto={'lens': {'points': lens_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 400, 'mod': [{'src': 'auto.lens', 'amount': 4.0}]}}],
               sends={'hall': '-6dB'}),
            # (v9) THE HOOK UPSIDE DOWN: E1 inverted, from bar 29 to the crest and through the drift, was a thin NES pulse
            # (an album staple, three tracks) 13 dB down - the song's through-line, barely there. Now it is a Wurlitzer,
            # reedy and warm, up front: the tune you follow upside down until the crest turns it over (and the ondes
            # sings it the right way up)
            # (v50, palette: the break's arpeggios were the cutting guitar - the same electric that skanks and funks
            # through the groove) THE BREAK GOES UNPLUGGED: the floating arpeggios in the break are now fingerpicked on
            # the library's acoustic (a steel-string dreadnought, close-miked: wound-string attack, body and air; no
            # Accretion track uses it) - wood and steel in the one place the band falls away, the electric back for
            # the drift
            # (v80, palette: the build's climbing arpeggio - eighths, then triplets, then sixteenths - was the library's
            # arp-pluck, an EDM saw-and-square pluck) THE ARPEGGIO ON A PIANO: it is now the library's concert grand
            # (felt hammers, stretched tuning, a sympathetic-string shimmer; no Accretion track uses a piano), the same
            # notes quickening through the build - a player's hands speeding up as the crest nears
            tr('buildarp', 'piano', '-4.2dB', pan=-0.25, sends={'echo': '-14dB', 'hall': '-12dB'}),
            # (v66, palette: the break's floating arp was the acoustic guitar - a plucked string like a dozen others on
            # the album) FIREFLIES: the break's arp is now the library's kuramoto-flies (wM's chirpers8 swarm: every note
            # starts as eight triangles at random phases and finds its pitch out of a shimmer in its first tenth of a
            # second; no Accretion track uses it) - the swarm the pad locked into tune at the crest scattering into
            # points of light, each note pulling itself together as it sounds, which is the song's whole idea in miniature
            tr('gtrarp', 'kuramoto-flies', '-8dB', pan=0.3, sends={'echo': '-8dB', 'hall': '-12dB'}),
            # (v60, palette: the comp was a cutting guitar, buried under the band at -18 to -19 dB from the gather to
            # the drift) THE COMP ON TINES: the off-beat skank and the funk sixteenths are now stabs on the library's
            # epiano (a Rhodes-style tine piano: a soft hammer on a tine, a pure bell-like attack and a warm body; no
            # Accretion track uses it), a little longer so each chord blooms - the band's rhythm part, heard for the
            # first time. (Through a Leslie, rhodes-rotary, it swirled each repeat differently: seed 11's recurrence
            # fell to 92)
            tr('gtr', 'epiano', '-10dB', pan=-0.35, sends={'hall': '-18dB'}),
            tr('gtrd', 'clean-dry', '-8.8dB', pan=-0.35, sends={'hall': '-16dB'}),
            # (v48, palette: the E1 keys were a wurli - another electric piano among the album's keys) THE ANSWERS ON
            # TAPE: E1's answers through the gather, the crest and the second verse now play on the library's
            # mellotron-flute (a breathy tape flute, band-limited, with wow and a soft swell; no Accretion track uses
            # it) - the lofi, Beatles/Radiohead tape colour, softer-edged than the wurli's tines, under the near voice
            tr('e1p', 'mellotron-flute', '-1dB', pan=0.2, sends={'echo': '-14dB', 'hall': '-14dB'}),
            # (v39, palette: Risset's bell played E1 twice over - the in-seam's lensed tune and the drift's retrograde
            # canon - one colour for two jobs) THE MEMORY ON VIBES: from the break to the end of the drift the
            # retrograde canon of E1 (augmented x2, against the wurli) is now a VIBRAPHONE - chirper-two's modal-vibes,
            # soft mallet, long ring, no Accretion track using it - warm wood-and-metal under the far choir and the
            # floating guitar instead of a second set of bells; Risset's bell keeps the in-seam (t1's tune arriving)
            # and the fall (its octave-up bells into t3's head, as agreed at the seam)
            # (v51, palette: E1's bells in the break and its retrograde canon before the fall were modal vibes - a
            # struck bar, like a dozen mallet parts on the album) THE BELLS RIPPLE: they now play on wM's
            # scanned-mallet (scanned synthesis: a narrow strike on a ring with no hand, the sharp shape splitting
            # into ripples that run round the ring and smooth away - a struck tone that mellows and shimmers as it
            # dies; no Accretion track uses it) - each note an orbit settling, the song's idea in one sound
            tr('e1v', 'scanned-mallet', '-9dB', pan=-0.35, sends={'hall': '-10dB', 'echo': '-20dB'}),
            # (v65, palette: the fall's E1 was the same Risset bell as the in-seam's - the song's bookends one sound)
            # THE BELLS TOLL AS IT FALLS IN: in the fall E1 rings on the library's tubular-bells (struck brass tubes,
            # clangorous, a long slowly beating tone; no Accretion track uses them) - the in-seam's lensed bell came
            # in from far away, the fall's tolls the song down into t3's storm
            tr('e1c', 'tubular-bells', '-19dB', pan=-0.35, sends={'hall': '-8dB'}),
            # (v27) the whisper's track is now the far choir's echo, 'farchoir' (below)
            {'name': 'farchoir', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-backing synth.layers.0.together=true synth.layers.0.breath.value=0.55 synth.lfo.vib.per_note=true',
                                           play={'scoop': 1, 'fall': 2.5}),
             'notes': echonotes, 'gain': '-10dB', 'pan': -0.1, 'sends': {'echo': '-12dB', 'hall': '-6dB'}},
            {'name': 'choir', 'patch': {'extends': 'voice-backing synth.layers.0.harmony=[7] synth.layers.0.together=true',
                                        'synth': CH['tracks'][0]['patch'].get('synth', {})},
             'notes': chnotes, 'gain': '-15dB', 'pan': 0.0, 'sends': {'hall': '-8dB'}},
            # (v15) and the sung line is wM's voice-near - close, young, breathy, dry, even vowels - made for this track,
            # in place of voice-legato pushed toward it
            {'name': 'breakhum', 'patch': dict(OOH['tracks'][0]['patch'], extends='voice-backing synth.layers.0.hum=1 synth.layers.0.hum_at=m synth.layers.0.harmony=[2,4] synth.layers.0.harmony_key=D:dorian synth.layers.0.together=true'),
             'notes': breakhum, 'gain': '-17dB', 'pan': 0.0, 'sends': {'hall': '-8dB'}},
            # (v42, palette: wM's part_size, pinned 14:43, which no Accretion track has used yet) THE CREST GETS ITS
            # BASSES: the ooh triads that back the crest gain a part an octave below the root, sung by voices 15%
            # larger (part_size 1: formants 13% lower) - real basses under the choir, not the same singers pitched
            # down - and the thirds and fifths above by slightly smaller voices: a SATB spread for the album's hook
            {'name': 'fallhum', 'patch': dict(OOH['tracks'][0]['patch'], extends='voice-backing synth.layers.0.hum=1 synth.layers.0.hum_at=m synth.layers.0.harmony=[-7,2,4] synth.layers.0.harmony_key=D:minor synth.layers.0.together=true synth.layers.0.part_size=1 synth.layers.0.vib_spread=1'),
             'notes': fallhum, 'gain': '-12dB', 'pan': 0.0, 'sends': {'hall': '-6dB'}},
            {'name': 'lastpad', 'patch': dict(OOH['tracks'][0]['patch'], extends='voice-backing synth.layers.0.harmony=[-7,2,4] synth.layers.0.harmony_key=D:dorian synth.layers.0.together=true synth.layers.0.part_size=1'),
             'notes': lastpad, 'gain': '-14dB', 'pan': 0.0, 'sends': {'hall': '-10dB'}},
            {'name': 'lastpadE', 'patch': dict(OOH['tracks'][0]['patch'], extends='voice-backing synth.layers.0.harmony=[-7,2,4] synth.layers.0.harmony_key=E:dorian synth.layers.0.together=true synth.layers.0.part_size=1'),
             'notes': lastpadE, 'gain': '-13dB', 'pan': 0.0, 'sends': {'hall': '-10dB'}},
            {'name': 'crestpad', 'patch': dict(OOH['tracks'][0]['patch'], extends='voice-backing synth.layers.0.harmony=[-7,2,4] synth.layers.0.harmony_key=D:mixolydian synth.layers.0.together=true synth.layers.0.part_size=1'),
             'notes': crestpad, 'gain': '-14dB', 'pan': 0.0, 'sends': {'hall': '-8dB'}},
            {'name': 'ooh', 'patch': dict(OOH['tracks'][0]['patch'], extends='voice-backing synth.layers.0.harmony=[-2] synth.layers.0.harmony_key=D:dorian synth.layers.0.together=true'),
             'notes': oohn, 'gain': '-17dB', 'pan': 0.0, 'sends': {'hall': '-8dB'}},
            {'name': 'oohin', 'patch': dict(dict(OOH['tracks'][0]['patch'], extends='voice-backing synth.layers.0.harmony=[4] synth.layers.0.harmony_key=D:dorian synth.layers.0.together=true synth.layers.0.depth_spread=1'), play={'scoop': 1}),
             'notes': oohin, 'gain': '-14dB', 'pan': 0.0, 'sends': {'hall': '-4dB'}},
            {'name': 'verse', 'patch': dict(V1['tracks'][0]['patch'], extends='voice-near synth.lfo.vib.per_note=true', play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': vsnotes, 'gain': '-13dB', 'pan': -0.05, 'sends': {'echo': '-16dB', 'hall': '-12dB'}},
            {'name': 'driftsung', 'patch': dict(dict(CS['tracks'][0]['patch'], extends='voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:dorian synth.layers.0.together=true synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': dsnotes, 'gain': '-9dB', 'pan': 0.0, 'sends': {'echo': '-18dB', 'hall': '-12dB'}},
            {'name': 'driftlift', 'patch': dict(dict(CS['tracks'][0]['patch'], extends='voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=E:dorian synth.layers.0.together=true synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1, 'fall': 2}),
             'notes': [dict(n_, pitch=f"m{int(str(n_['pitch'])[1:]) + 2}") for n_ in dsnotes2], 'gain': '-8dB', 'pan': 0.0, 'sends': {'echo': '-18dB', 'hall': '-12dB'}},
            {'name': 'earlyhook', 'patch': dict(dict(CS['tracks'][0]['patch'], extends='voice-near synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06}),
             'notes': eh_, 'gain': '-13dB', 'pan': -0.15, 'fx': ['lp cutoff=2600', 'hp cutoff=200'], 'sends': {'echo': '-12dB', 'hall': '-4dB'}},
            {'name': 'crestsung', 'patch': dict(dict(CS['tracks'][0]['patch'], extends='voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian synth.layers.0.together=true synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06}),
             'notes': csnotes, 'gain': '-9dB', 'pan': 0.0, 'sends': {'echo': '-18dB', 'hall': '-12dB'}},
            {'name': 'prech', 'patch': dict(dict(PC['tracks'][0]['patch'], extends='voice-near synth.layers.0.passaggio=C5 synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1}),
             'notes': pcnotes, 'gain': '-10dB', 'pan': 0.0, 'sends': {'echo': '-16dB', 'hall': '-12dB'}},
            {'name': 'crestb', 'patch': dict(dict(CB['tracks'][0]['patch'], extends='voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian synth.layers.0.together=true synth.lfo.vib.per_note=true'), play={'glide_overshoot': 0.06, 'scoop': 1}),
             'notes': cbnotes, 'gain': '-9dB', 'pan': 0.0, 'sends': {'echo': '-18dB', 'hall': '-12dB'}},
            # (v61, section w5: 2:06-2:37, the crest, 'static, little new vs w4' - the line and the band, the same
            # density bar after bar; the line itself is untouched, Harry's 'woah this track is sick') THE CHOIR
            # ANSWERS: in the gaps the line leaves, the backing choir sings its last words back - 'comes round' after
            # the first 'nearer each time it comes round', 'draws us in' after each 'the middle draws us in' - in
            # three parts (an octave below, the line, a third above), five singers each at their own depths: a
            # congregation answering the voice, call and response at the centre of the song
            {'name': 'answer', 'patch': dict(CS['tracks'][0]['patch'], extends='voice-backing synth.layers.0.harmony=[-7,2] synth.layers.0.harmony_key=D:mixolydian synth.layers.0.together=true synth.layers.0.part_size=1 synth.layers.0.singers=5 synth.layers.0.vowel_spread=1 synth.layers.0.f0_spread=1 synth.layers.0.depth_spread=1'),
             'notes': [n_ for n_ in answers if n_['at'] < SEC['drift'] * 4.0], 'gain': '-6dB', 'pan': 0.0, 'sends': {'hall': '-6dB'}},
            {'name': 'answer2', 'patch': dict(CS['tracks'][0]['patch'], extends='voice-backing synth.layers.0.harmony=[-7,2] synth.layers.0.harmony_key=D:dorian synth.layers.0.together=true synth.layers.0.part_size=1 synth.layers.0.singers=5 synth.layers.0.vowel_spread=1 synth.layers.0.f0_spread=1 synth.layers.0.depth_spread=1'),
             'notes': [n_ for n_ in answers if n_['at'] >= SEC['drift'] * 4.0], 'gain': '-6dB', 'pan': 0.0, 'sends': {'hall': '-6dB'}},
            {'name': 'sung', 'patch': dict(SU['tracks'][0]['patch'], extends='voice-near synth.lfo.vib.per_note=true'),
             'notes': snotes, 'gain': '-11dB', 'pan': 0.05, 'sends': {'echo': '-16dB', 'hall': '-12dB'}},
        ]}
    # (v49, whole song: the near voice - the song's singer, the line Harry stopped for - sat under the triangle bass
    # in every groove (presence: the bass the loudest thing in the mix, the verse 6-8 dB behind it)) THE SINGER STEPS
    # FORWARD: every lead line (verse, pre-chorus, the crest's line and its answer, the last chorus and its lift, the
    # line found at the break's end) gets a singer's presence - a lift at 3 kHz where the words live, a little air
    # above 9 kHz, a little less boxiness at 350 Hz - and comes up 1.5 dB, while the triangle bass steps back 1.5 dB
    # to make room; the backing voices, the far choir and the glimpse stay where they are (the voice alone, the bass
    # unchanged, scored level: it is the room the bass gives that lets the line through)
    LEAD = ('verse', 'prech', 'crestsung', 'crestb', 'driftsung', 'driftlift', 'sung')
    for t_ in song['tracks']:
        if t_['name'] in LEAD:
            t_['gain'] = f"{float(t_['gain'][:-2]) + 1.5:g}dB"
            t_['fx'] = list(t_.get('fx', [])) + [{'type': 'eq', 'bands': ['peak cutoff=3000 q=0.9 gain=3dB', 'highshelf cutoff=9000 gain=2dB', 'peak cutoff=350 q=1.0 gain=-2dB']}]
        # (v69, palette: the engine's newest voice features, as on t6 v69) THE SINGER BREATHES AND LETS GO: the near
        # voice's own lines around the chorus - the verses, the pre-chorus, the early glimpse of the hook and the line
        # found at the break's end - draw a fuller breath before each phrase (inhale 0.4 -> 0.7), sized to the phrase
        # (wM's inhale_depth: a sip before 'all that falls', a full breath before the pre-chorus's long climb), and
        # let each phrase's last note go (wM's taper 0.6) instead of stopping square. The crest line itself - at the
        # crest, its answer and in the last chorus - is untouched, as Harry heard it
        if t_['name'] in ('verse', 'prech', 'earlyhook', 'sung') and isinstance(t_.get('patch'), dict) and 'extends' in t_['patch']:
            t_['patch'] = dict(t_['patch'], extends=t_['patch']['extends'] + ' synth.layers.0.inhale=0.7 synth.layers.0.inhale_depth=1 synth.layers.0.taper=0.6')
        if t_['name'] == 'bass':
            # (v64, whole song) THE FLOOR STEPS BACK: the chip bass was the loudest thing in every window of the song
            # (presence -0.2 to -2.9 dB, everything else 4-15 dB under it) - the whole song heard through its floor.
            # It comes down a further 3.5 dB, so the voice, the debris, the comp and the bells sit on it rather than
            # behind it; the sub, the gravity lane and the master's low shelf are untouched (-2 alone scored worse)
            t_['gain'] = f"{float(t_['gain'][:-2]) - 1.5 - 3.5:g}dB"
    # (v55, whole song: wM's vowel_spread, pinned 03:36) THE CHOIR ACCRETES: every backing choir in the song was the
    # same trio - three singers, their vowels one voice's formants copied and scaled - from the in-seam's first
    # 'ooh' to the fall. Now the backing voices gather as the song falls in, the way the cell does: a trio for the
    # in-seam's breath and the far choir's echo, four for the verse's ooh and the break's hum, five for the crest's
    # E1 choir, six for the crest's chord pad and the fall's hum, eight for the last chorus - and every singer
    # shapes the vowels their own way (vowel_spread 1, F1/F2 apart by up to 8%), so each choir is a group of
    # different people rather than one voice copied; the lines, parts and levels are untouched
    # (v58, palette: wM's f0_spread, pinned 06:06) ...and each singer now has their own vibrato too: the backing
    # voices sing tts lines whose vibrato lives in each note's pitch path, so every singer in a choir wobbled in
    # exact lockstep (vib_spread could not reach it - v53's hum was byte-identical with it); f0_spread 1 reads the
    # path's vibrato at each singer's own rate, phase and depth while the slow scoops and glides stay shared
    GATHER = {'oohin': 3, 'farchoir': 3, 'ooh': 4, 'breakhum': 4, 'choir': 5, 'crestpad': 6, 'fallhum': 6,
              'lastpad': 8, 'lastpadE': 8}
    for t_ in song['tracks']:
        if t_['name'] in GATHER:
            t_['patch'] = dict(t_['patch'], extends=t_['patch']['extends'] + f" synth.layers.0.singers={GATHER[t_['name']]} synth.layers.0.vowel_spread=1 synth.layers.0.f0_spread=1")
    # (v78, section w4: 1:35-2:06, the build's last twelve bars - flagged 'static, little new vs w3': after the
    # pre-chorus's 'round and round and round' the voice fell silent for the four bars of A sus before the crest,
    # the band climbing alone) THE APPROACH SINGS: over the held dominant (bars 45-48) the near voice keeps going -
    # 'the nearer' three times, each a step higher (B B A, D D B, E E D), then 'the faster' held high on E and D,
    # letting go just before the crest's 'nearer each time it comes round' drops back to its low D: the pre-chorus's
    # own words, climbing the last of the way in
    pr_ = [t_ for t_ in song['tracks'] if t_['name'] == 'prech'][0]
    tpl_ = sorted(pr_['notes'], key=lambda n_: n_['at'])[:6]
    add_ = []
    for f0_, pits_ in ((176.0, (71, 71, 69)), (178.0, (74, 74, 71)), (180.0, (76, 76, 74))):
        for k_, n_ in enumerate(tpl_[:3]):
            add_.append(dict(n_, at=round(f0_ + 0.5 * k_, 4), pitch=f"m{pits_[k_]}", vel=round(min(1.0, n_.get('vel', 0.8) * (1.0 + 0.04 * (f0_ - 176.0) / 2.0)), 3)))
    for at_, n_, pit_, ln_ in ((182.0, tpl_[3], 74, 0.495), (182.5, tpl_[4], 76, 1.45), (184.0, tpl_[5], 74, 3.4)):
        add_.append(dict(n_, at=at_, pitch=f"m{pit_}", len=ln_))
    pr_['notes'] = sorted(pr_['notes'] + add_, key=lambda n_: n_['at'])
    # (v76, palette: the engine's track double, which only t7's leads use) THE VERSES DOUBLED: the near voice's own
    # lines around the chorus - both verses ('all that falls', 'all that turns'), the pre-chorus, the early glimpse
    # of the hook and the line found at the break's end - are double-tracked: two takes, 30% left and right on
    # their own seeds, so their breaths, drift and vibrato differ, each 3 dB down (the centre held). The crest's line
    # stays one voice in the middle with its keyed third, exactly as Harry heard it - so the verses open wide and
    # the chorus arrives as one voice stepping forward. (Tried first: wM's breathy vocal attack on the sustained
    # oohs - it measured -35 to -55 dB, the choirs' own slow swell already hides it)
    for t_ in song['tracks']:
        if t_['name'] in ('verse', 'prech', 'earlyhook', 'sung'):
            t_['double'] = {'pan': 30, 'seeds': [76, 67]}
            t_['gain'] = f"{float(str(t_['gain'])[:-2]) - 3:g}dB"
    # (v83, whole song: the engine's orbit fx, as t3 v82 uses it) THE MOTIF IN ORBIT: E2 - the seven sixteenths
    # whose cycle the whole song falls through - sat still in the stereo field. Now its bright metal voice (and the
    # dust around it) circles the listener (distance 0, no Doppler, so only its position moves: no pitch or level
    # change), and its laps follow the song's orbit as Kepler would: slow and wide at the start (a lap every four
    # bars), quickening as it falls in through the gather and the build, a lap a bar at the crest and faster through
    # it; flung out at the break it all but stops (as E2 stretches, v68); the drift picks it up again and the fall
    # spins it in fastest of all, two laps a bar into t3
    # (v84, seam fix for chirper-zero: the orbit turning inside the t1 -> t2 overlap cost t1 0.055/0.085 and crossed
    # t1's own slowly turning ring of seed voices; until bar 19 the orbit is now out of the signal altogether (its
    # mix at 0, so E2 and the dust sit where they always sat), then it fades in over two bars and sets off)
    spin_ = {'points': [['0b', 0.0], ['72b', 0.0], ['80b', 0.35], ['128b', 0.6], ['192b', 1.0], ['254b', 1.5], ['256b', 0.15],
                        ['318b', 0.15], ['320b', 0.4], ['384b', 1.0], ['440b', 2.0], ['460b', 2.0]]}
    for t_ in song['tracks']:
        if t_['name'] in ('e2m', 'dust'):
            t_['fx'] = list(t_.get('fx') or []) + [{'type': 'orbit', 'path': 'circle', 'distance': 0, 'doppler': 0.0,
                                                     'rate': '1/1', 'phase': 0.0 if t_['name'] == 'e2m' else 0.5,
                                                     'speed': {'value': 0, 'mod': [{'src': 'auto.spin', 'amount': 1}]},
                                                     'mix': {'value': 0, 'mod': [{'src': 'auto.omix', 'amount': 1}]}}]
            t_['auto'] = dict(t_.get('auto') or {}, spin=spin_, omix={'points': [['0b', 0.0], ['72b', 0.0], ['80b', 1.0]]})
    # (v82, section w7: 3:04-3:34, the break's last eight bars into the drift - the break hummed the crest's line
    # at bar 77, ending on 'comes round', and then nothing was sung until the second verse's 'all that turns' at
    # bar 81) ROUND, AND ROUND: the near voice picks up the crest's last word and keeps turning on it - the
    # pre-chorus's 'round and round and round' (D D E D E, an octave down from the build's), soft and wet over the
    # break's rising chords (bars 79-80) - so the break hands the drift its word: round -> round and round -> all
    # that turns
    pc_ = [t_ for t_ in song['tracks'] if t_['name'] == 'prech'][0]
    rr_ = sorted([n_ for n_ in pc_['notes'] if 167.5 <= n_['at'] < 176.0], key=lambda n_: n_['at'])
    assert len(rr_) == 5
    rr0_ = SEC['break'] * 4.0 + 56.0
    rrn_ = [dict(n_, at=round(rr0_ + (n_['at'] - rr_[0]['at']), 4), pitch=f"m{int(str(n_['pitch'])[1:]) - 12}",
                 vel=round(n_['vel'] * 0.85, 3), len=(2.9 if k_ == 4 else n_['len'])) for k_, n_ in enumerate(rr_)]
    rrt_ = dict(pc_, name='roundround', notes=rrn_, gain='-15dB', sends={'hall': '-6dB', 'echo': '-12dB'})
    rrt_.pop('double', None)
    song['tracks'].append(rrt_)
    # (v81, section w9: 4:04-4:45, the fall into t3 - flagged static: once the kit, the bass, the bells and the hum
    # stop at bar 105, the fall's last eight bars were the pad, the sub and E2 sinking alone) THE FIRST WORDS, LAST:
    # at bar 105 the near voice sings the song's first line once more - 'all that falls, falls a little nearer' -
    # from far off (darkened, 3.5 dB under the verse and wetter, single-tracked) and slowed by half again, as if
    # falling itself; its D minor sits in the fall's D | B-flat | C. The song that began with the line ends on it,
    # and hands t3 a voice still falling
    vs_ = [t_ for t_ in song['tracks'] if t_['name'] == 'verse'][0]
    v1_ = sorted([n_ for n_ in vs_['notes'] if 79.0 <= n_['at'] < 88.0], key=lambda n_: n_['at'])
    lv0_ = (fall0 + 32.0)
    lvn_ = [dict(n_, at=round(lv0_ + (n_['at'] - v1_[0]['at']) * 1.5, 4), len=round(n_['len'] * 1.5, 4),
                 vel=round(n_['vel'] * 0.85, 3)) for n_ in v1_]
    lv_ = dict(vs_, name='lastverse', notes=lvn_, gain='-18dB',
               fx=list(vs_.get('fx', [])) + ['lp cutoff=2600'], sends={'hall': '-6dB', 'echo': '-12dB'})
    lv_.pop('double', None)
    song['tracks'].append(lv_)
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
