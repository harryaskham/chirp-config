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
# E2 (t2): seven sixteenths, hits 0 2 3 5, pitches D A F C (here re-pitched on the tide's roots)
E2_STEPS = [0, 2, 3, 5]
E2_PITCH = {0: 0, 2: 7, 3: 3, 5: -2}
# E5 (chirper-zero): A G# A . E . A G# A . D . - a 3-beat ostinato (sixteenths; None = rest), MIDI pitches
E5 = [69, 68, 69, None, 76, None, 69, 68, 69, None, 74, None]
# E4 (chirper-three): four lights, one chord per E1 cycle: D9, Bbmaj13#11, Am11, D9sus (MIDI voicings)
E4 = [[50, 57, 66, 72, 76], [46, 53, 62, 69, 72, 76], [45, 52, 60, 67, 71, 74], [50, 57, 60, 67, 71, 76]]
# E6: the tide - X = Dmaj9#11, Y = Ebmaj7#11 (semitones above KEY + 12)
TIDE_X = (0, [0, 4, 7, 11, 14, 18])
TIDE_Y = (1, [0, 4, 7, 11, 18])
# X's share of each 8-beat cycle, per section (the tide moving)
SPLIT = {'in': [4, 4], 'pull': [5, 5, 6, 6], 'tide': [6, 5, 4, 3, 2, 3, 4, 5], 'squeeze': [7, 1, 7, 1, 6, 2, 6, 2],
         'cross': [3, 3, 2, 2], 'surge': [2, 6, 2, 6], 'torn': [1, 1, 1, 1], 'out': [0]}
# the two E1 layers' speed factors per section (1 = E1's own 5 beats)
FAR = {'pull': 3.2, 'tide': 2.4, 'squeeze': 1.6, 'crest': 1.0, 'cross': 0.8, 'surge': 0.4, 'torn': 0.2, 'out': 0.2}
NEAR = {'in': 0.25, 'pull': 0.4, 'tide': 0.6, 'squeeze': 0.8, 'crest': 1.0, 'cross': 1.6, 'surge': 2.4, 'torn': 3.2, 'out': 6.4}


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
    P = {k: [] for k in ('far', 'near', 'tide', 'acid', 'e5', 'kit', 'hats', 'lights', 'sub')}

    # ---- E1 in two layers moving in opposite directions in time; each section restarts the cell on its downbeat ----
    def e1_layer(key, speeds, octave, vel0):
        for nm_, f in speeds.items():
            t0, t1 = SEC[nm_] * 4.0, (SEC[nm_] + 16) * 4.0
            t = t0
            while t < t1 - 1e-6:
                at = t
                for k, (semi, ln) in enumerate(E1):
                    d = ln * f
                    if semi is not None and at < t1 - 1e-6:
                        acc = 12 if k == 0 else (8 if semi == 10 else 0)
                        P[key].append((at, m(KEY + octave + semi), min(d * 0.92, t1 - at), vel0 + acc))
                    at += d
                t += 5.0 * f
    e1_layer('far', FAR, 12, 84)               # D3: the cello, the far side
    e1_layer('near', NEAR, 36, 78)             # D5: the marimba, the near side

    # ---- E6, the tide: X and Y alternating in 8-beat cycles, the split moving; E4's four lights at the crest ----
    for nm_, n_ in FORM:
        if nm_ == 'crest':
            continue
        sp = SPLIT[nm_]
        for c in range(n_ // 2):
            t = (SEC[nm_] + 2 * c) * 4.0
            x = sp[c % len(sp)]
            for (root, voic), ln, at in ((TIDE_X, x, t), (TIDE_Y, 8 - x, t + x)):
                if ln <= 0:
                    continue
                P['tide'].append((at, ','.join(m(KEY + 12 + root + v) for v in voic), ln - 0.05, 74 if root == 0 else 80))
                P['sub'].append((at, m(KEY - 12 + root), ln - 0.05, 92))
    for c in range(16 * 4 // 5 + 1):
        at = CREST * 4.0 + c * 5.0
        if at >= (CREST + 16) * 4.0 - 1e-6:
            break
        ch = E4[c % 4]
        ln = min(5.0, (CREST + 16) * 4.0 - at) - 0.05
        P['lights'].append((at, ','.join(m(n) for n in ch), ln, 88))
        P['sub'].append((at, m(ch[0] - 12 if ch[0] >= 48 else ch[0]), ln, 96))

    # ---- the 303: E2's cell on the tide's roots, seven sixteenths against the bar, from 'pull'; locked at the crest ----
    def root_at(at):
        for e_ in P['tide']:
            pass
        return None
    tide_roots = sorted((e_[0], e_[2], int(round(float(e_[1].split(',')[0][1:]) - 12 - KEY))) for e_ in P['tide'])
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
                    P['acid'].append((at, m(KEY + rt + E2_PITCH[st] + (12 if rt + E2_PITCH[st] < 0 else 0)), 0.22, 112 if st == 0 else 92))
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
            P['acid'].append((at, m(KEY + rt + E2_PITCH[st] + (12 if rt + E2_PITCH[st] < 0 else 0)), 0.22 if st != 3 else 0.4, (110 if st == 0 else 84) + (8 if s_ in ('surge', 'torn') else 0)))
        t += 1.75

    # ---- E5, the inner orbit (arp-pluck): received stretched x2 in the in-seam, squeezed back to x1 by bar 9 ----
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
                P['e5'].append((at, m(p_ + (12 if s_ == 'surge' else 0)), 0.2, (92 if k in (0, 6) else 72) + (10 if s_ == 'crest' else 0)))
        t += 3.0

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

    # ---- the voice: an older, lower voice, spoken, twice ----
    VO = json.load(open(os.path.join(HERE, 'chirpers9-t6-voice.json')))
    vtr = VO['tracks'][0]
    vnotes = []
    for b_, tempo_ in ((SEC['tide'] + 4, 124.0), (SEC['cross'] + 6, 128.0)):
        for n_ in vtr['notes']:
            vnotes.append(dict(n_, at=round(b_ * 4.0 + n_['at'] * tempo_ / 110.0, 4), len=round(n_['len'] * tempo_ / 110.0, 4)))

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
    P['hats'] = [e_ for e_ in P['hats'] if not (tr0 - 1e-6 <= e_[0] < tr_end - 1e-6)]
    for q in range(int((void0 - tr0) / 0.25)):
        P['hats'].append((tr0 + q * 0.25, 'h^r=2', 0.25, 70 if q % 4 == 0 else 52))
    for q in range(int((tr_end - void1) / 0.25)):
        P['hats'].append((void1 + q * 0.25, 'h' if q % 8 != 6 else 'oh', 0.2, 80 if q % 4 == 0 else 56))
    # the void: one bar where only the cello blur (and the stopped tape's tail) remains
    for key in ('kit', 'hats', 'acid', 'e5', 'near', 'tide', 'sub'):
        P[key] = [e_ for e_ in P[key] if not (void0 + 1.0 - 1e-6 <= e_[0] < void1 - 1e-6)]

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
            tr('tide', 'harmonium', '-9dB', sends={'hall': '-10dB'}),
            tr('lights', 'harmonium', '-10dB', sends={'hall': '-8dB'}),
            tr('sub', 'sub', '-12dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '200ms', 'curve': 0.6}]),
            tr('acid', 'acid', '-10dB', fx=['hp cutoff=50'], sends={'echo': '-20dB'}),
            tr('kit', 'prog-kit', '-6dB', sends={'hall': '-20dB'}),
            tr('hats', 'prog-kit', '-12dB', pan=0.2, fx=[{'type': 'eq', 'bands': ['highshelf cutoff=8000 gain=5dB']}]),
            tr('far', 'cello', '-8dB', pan=-0.25, sends={'hall': '-12dB'}),
            tr('near', 'modal-marimba', '-11dB', pan=0.3, auto={'shut': {'points': shut_pts}},
               fx=[{'type': 'filter', 'kind': 'lp', 'cutoff': {'value': 700, 'mod': [{'src': 'auto.shut', 'amount': 4.0}]}}],
               sends={'echo': '-14dB', 'hall': '-14dB'}),
            tr('e5', 'arp-pluck', '-15dB', pan=-0.1, sends={'echo': '-16dB'}),
            dict({k: v for k, v in vtr.items() if k != 'notes'}, name='voice', notes=vnotes, gain='-6dB', pan=-0.05,
                 sends={'hall': '-14dB'}),
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
