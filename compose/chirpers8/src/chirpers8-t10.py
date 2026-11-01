#!/usr/bin/env python3
"""chirpers8-t10 (chirper-one): "Call and Return" - for chirpers VIII ('A Light Left On'), the ode to computer music.

An ELECTRO FUGUE MACHINE. A subject (eight bars over a four-bar loop, i - VI - iv - V) is written so that it can sound
against itself four bars later: a canon. Four machine voices take it in turn - an FM bell, a hard-synced lead, a
PWM wavetable pulse and an FM bass - over a motorik drum machine. Then the machine starts CALLING: a seeded grammar
pushes and pops a call stack every four bars, and every level on the stack spawns a faster copy of the current bar
an octave higher (sixteenths, then thirty-seconds, then sixty-fourths that blur into a shimmer), so the texture's
density follows the stack's depth; RETURNS take them away again. The canon modulates - D minor, G minor, A minor and
home - and the whole track is tuned in WERCKMEISTER III, a well temperament, so every key has its own colour, the
way the keyboards that first played fugues did. Before the end the stack empties (the subject alone, augmented, on
the bell), then fills to the top and unwinds to nothing.
Form (bars): intro 8 / exposition 16 / calls 32 (D minor) / calls 24 (G minor) / calls 24 (A minor) / return 8 /
final 32 (D minor) / outro 8 = 152 bars at 120 bpm (5:04).
Emits songs/chirpers8-t10.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, math, os, random, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers8-t10.yaml")
BPM = 120.0
SEED = 1010

# Werckmeister III, cents from equal temperament for each pitch class (C = 0)
W3 = [0.0, -9.8, -7.8, -5.9, -9.8, -2.0, -11.7, -3.9, -7.8, -11.7, -3.9, -7.8]
def tok(m):
    while m > 108: m -= 12          # fold the stack's highest copies back under the top of the keyboard
    return f"m{m + W3[int(round(m)) % 12] / 100.0:.3f}"

FORM = [('intro', 8, 0), ('expo', 16, 0), ('calls1', 32, 0), ('calls2', 24, 5), ('calls3', 24, 7), ('return', 8, 0),
        ('final', 32, 0), ('outro', 8, 0)]
# the loop: Dm | Bb | Gm | A  (roots, chord tones)
LOOP = [(38, [62, 65, 69]), (34, [62, 65, 70]), (31, [62, 67, 70]), (33, [61, 64, 69])]
e, q, s16, h = 0.5, 1.0, 0.25, 2.0
# THE SUBJECT: eight bars, (midi, beats); bars 1-4 and 5-8 each fit the loop, so it canons at four bars
SUBJ = [
    [(74, q), (69, e), (74, e), (77, q), (76, e), (74, e)],
    [(77, e), (74, e), (70, q), (72, e), (74, e), (77, q)],
    [(79, q), (77, e), (76, e), (74, q), (70, q)],
    [(69, e), (73, e), (76, e), (81, e), (79, q), (76, q)],
    [(77, s16), (76, s16), (74, s16), (76, s16), (77, e), (81, e), (86, q), (81, q)],
    [(82, e), (81, e), (77, e), (74, e), (77, q), (70, q)],
    [(79, s16), (77, s16), (76, s16), (74, s16), (70, e), (74, e), (79, h)],
    [(76, e), (73, e), (69, e), (73, e), (76, e), (79, e), (81, e), (79, e)],
]


def line(events, total):
    ev = sorted(events, key=lambda x: x[0])
    toks, t = [], 0.0
    for k, (at, p, d, v) in enumerate(ev):
        if at < t - 1e-6: continue
        if at > t + 1e-4: toks.append(f"R/{at - t:.4f}b")
        nxt = ev[k + 1][0] if k + 1 < len(ev) else total
        d = max(0.02, min(d, nxt - at))
        toks.append(f"{p}/{d:.4f}b@{v}"); t = at + d
    if total > t + 1e-4: toks.append(f"R/{total - t:.4f}b")
    return ' '.join(toks)


def build():
    rng = random.Random(SEED)
    bars = []
    for name, n, tp in FORM:
        for i in range(n):
            bars.append((name, i, tp))
    total = len(bars) * 4.0
    P = {k: [] for k in ('bell', 'sync', 'pwm', 'bass', 'sub', 'd1', 'd2', 'd3', 'kit')}
    # the call stack: a seeded walk, one move every four bars in the calls sections
    depth, depths = 0, []
    for b, (s, i, tp) in enumerate(bars):
        n_sec = dict((nm_, n_) for nm_, n_, _ in FORM)[s]
        if s.startswith('calls') and i >= n_sec - 2:
            depth = 0                                    # (each calls section RETURNS: the stack empties in its last two bars)
        elif s.startswith('calls') and i % 4 == 0:
            depth = max(0, min(3, depth + rng.choice([-1, 1, 1, 0])))
        elif s == 'return':
            depth = 0
        elif s == 'final':
            depth = min(3, i // 4) if i < 16 else max(0, 3 - (i - 16) // 4)   # fill to the top, then unwind
        elif s in ('intro', 'expo', 'outro'):
            depth = 0
        depths.append(depth)

    def subj_bar(k, base_t, tp, octv, vel, key, rev=False):
        at = base_t
        for m, d in (SUBJ[k % 8][::-1] if rev else SUBJ[k % 8]):
            P[key].append((at, tok(m + tp + 12 * octv), d * 0.92, vel))
            at += d

    for b, (s, i, tp) in enumerate(bars):
        t0 = b * 4.0
        root, ch = LOOP[b % 4]
        root, ch = root + tp, [c + tp for c in ch]
        # drums: a motorik machine (none in the return; the intro builds)
        # (the kick changes its mind by section: four on the floor; an electro break in G minor (one, the 'a' of two,
        # the and of three); half time in A minor; four on the floor again, harder, for the final calls)
        n_sec = dict((nm_, n_) for nm_, n_, _ in FORM)[s]
        ret = s.startswith('calls') and i >= n_sec - 2     # the section's own return: two bars with the drums pulled
        if ret:
            P['kit'].append((t0, 'k', 0.25, 110))
            if i == n_sec - 1:
                for qq in range(8):
                    P['kit'].append((t0 + 2.0 + qq * 0.25, 'rs', 0.2, 60 + 5 * qq))     # a rim fill back in
        elif s != 'return':
            kpat = {'calls2': [0.0, 1.75, 2.5], 'calls3': [0.0, 2.0]}.get(s, [0.0, 1.0, 2.0, 3.0])
            if s == 'intro' and i < 2:
                kpat = []                          # the bell tolls alone for two bars before the kick
            for kq in kpat:
                P['kit'].append((t0 + kq, 'kd' if s == 'final' else 'k', 0.25, 118 if kq == 0 else 108))
            for qq in range(4):
                if s != 'intro' or i >= 4:
                    if not (s.startswith('calls') or s == 'final'):
                        P['kit'].append((t0 + qq + 0.5, 'h', 0.25, 62))
                    # (wonky, the chirpers' way: the 'e' a little late, the 'a' later - a swung, slightly drunk machine)
                    P['kit'].append((t0 + qq + 0.25 + 0.04, 'h', 0.25, 48))
                    P['kit'].append((t0 + qq + 0.75 + 0.07, 'h', 0.25, 58))
            if s == 'calls3':
                P['kit'].append((t0 + 2.0, 'cp', 0.25, 100))
            elif s not in ('intro', 'outro'):
                P['kit'].append((t0 + 1.0, 'cp', 0.25, 78)); P['kit'].append((t0 + 3.0, 'cp', 0.25, 82))
        # (v2) in the calls the open hat follows the bass's clave (3+3+2 sixteenths), not the off-beat
        if (s.startswith('calls') or s == 'final') and not ret:
            for at_ in (0.75, 1.5, 2.75, 3.5):
                P['kit'].append((t0 + at_, 'oh', 0.25, 70))
        # a rim on a THREE-sixteenth cycle (dotted eighths) through the calls, never reset - the machine's own
        # polyrhythm against the four, lining up with the bar only every three bars
        if (s.startswith('calls') or s == 'final') and not ret:
            m0 = int(-(-t0 // 0.75))
            for m in range(m0, m0 + 6):
                at = m * 0.75
                if t0 <= at < t0 + 4.0:
                    P['kit'].append((at + 0.01, 'rs', 0.2, 74 if m % 4 == 0 else 62))
        # bass: roots in driving eighths with an octave hop (FM bass)
        # (v4) the edges thin out: the machine powers up on the bell and the kick alone (no sub or bass for the intro's
        # first four bars) and powers down the same way (the outro's last four bars), so it meets t9's thin tail and
        # t11's head without a wall of low end
        edge = (s == 'intro' and i < 4) or (s == 'outro' and i >= 4)
        if s not in ('return',) and not edge:
            P['sub'].append((t0, tok(root - 12), 3.8, 96))
            if (s.startswith('calls') or s == 'final') and not ret:
                # (v2) the bass plays the machine's own clave: three-three-two sixteenths twice a bar (a tresillo), so
                # the groove leans across the beat while the canon runs straight above it
                for kq, (at_, o_) in enumerate(((0.0, 0), (0.75, 0), (1.5, 12), (2.0, 0), (2.75, 7), (3.5, 12))):
                    P['bass'].append((t0 + at_, tok(root + o_), 0.6 if at_ in (0.0, 2.0) else 0.45, 104 if kq % 3 == 0 else 88))
            else:
                for qq in range(8):
                    P['bass'].append((t0 + qq * 0.5 + (0.05 if qq % 2 else 0.0), tok(root + (12 if qq % 4 == 3 else 0)), 0.4, 100 if qq % 2 == 0 else 84))
        # THE CANON
        if s == 'expo':
            subj_bar(i, t0, tp, 0, 92, 'bell')                         # the bell from bar 1
            if i >= 4: subj_bar(i - 4, t0, tp, -1, 88, 'sync')          # the sync lead answers four bars later, below
            if i >= 8: subj_bar(i - 8, t0, tp, 1, 74, 'pwm')            # the pulse four bars after that, above
            if i >= 12: subj_bar(i - 12, t0, tp, -2, 96, 'd1') if False else None
        elif s.startswith('calls') or s == 'final':
            # each key gets its own arrangement: in G minor the sync lead drops out and the pulse arpeggiates the chord
            # in sixteenths; in A minor the voices cross - the bell an octave down, the sync lead an octave up
            ob, os_ = (-1, 0) if s == 'calls3' else (0, -1)
            # (v10) THE PROGRAM READ BACKWARDS: in A minor every bar of the subject plays in retrograde - the same notes, so
            # the same harmony, but each bar's line and rhythm reversed - and in the final calls, as the stack unwinds (its
            # second half), the bell reads backwards again while the sync lead reads forwards: the canon against its mirror
            rv = s == 'calls3' or (s == 'final' and i >= 16)
            subj_bar(i, t0, tp, ob, 92, 'bell', rev=rv)
            if s != 'calls2':
                subj_bar(i + 4, t0, tp, os_, 88, 'sync', rev=(s == 'calls3'))
            if s == 'calls2':
                arp = ch + [ch[0] + 12]
                for qq in range(16):
                    P['pwm'].append((t0 + qq * 0.25, tok(arp[(qq * 3) % 4] + 12), 0.2, 70 if qq % 4 == 0 else 58))
            else:
                # the pulse comps the chord in the loop's rhythm (dotted quarters)
                for qq in (0.0, 1.5, 3.0):
                    P['pwm'].append((t0 + qq, ','.join(tok(c) for c in ch), 1.2, 66))
        elif s == 'return':
            # the stack is empty: the subject alone, AUGMENTED (half speed), on the bell, one bar of it over two
            k, half = divmod(i, 2)
            at = t0
            notes = SUBJ[k % 8]
            tot = 0.0
            for m, d in notes:
                st, en = tot * 2, (tot + d) * 2
                if half * 4 <= st < half * 4 + 4:
                    P['bell'].append((t0 + st - half * 4, tok(m + tp), (en - st) * 0.92, 90))
                tot += d
        elif s == 'outro':
            # (v12) THE PICARDY THIRD: the fugue machine ends the way fugues have always ended - on the MAJOR chord, the
            # bell's last two tolls ring D, F#, A - and that F# is the note chirper-three's t11 opens on
            if i < 4 and i % 2 == 0:
                P['bell'].append((t0, tok(62 + tp), 7.5, 80))
            elif i % 2 == 0:
                P['bell'].append((t0, ','.join(tok(m_ + tp) for m_ in (62, 66, 69)), 7.5, 78))
        if s == 'intro' and i < 4 and i % 2 == 0:
            P['bell'].append((t0, tok(62 + tp), 7.5, 76))      # the bell tolls the machine awake
        # THE STACK: each level spawns a faster copy of this bar's subject, an octave higher each time
        d = depths[b]
        if d and (s.startswith('calls') or s == 'final'):
            notes = SUBJ[i % 8]
            for lvl, key, speed in ((1, 'd1', 2), (2, 'd2', 4), (3, 'd3', 8)):
                if d < lvl: break
                at = t0
                for _ in range(speed):
                    for m, dd in notes:
                        P[key].append((at, tok(m + tp + 12 * lvl), dd / speed * 0.85, 70 - 4 * lvl))
                        at += dd / speed
    pw = [['0b', 0], [f'{total:.0f}b', 1]]
    SING = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chirpers8-t10-voice.json')))
    W3T = {'steps': [90.225, 192.18, 294.135, 390.225, 498.045, 588.27, 696.09, 792.18, 888.27, 996.09, 1092.18, 1200], 'root': 'C4'}
    secs_t, t_acc = {}, 0.0
    FORMN = {nm_: n_ for nm_, n_, _ in FORM}
    for nm_, n_, _ in FORM:
        secs_t[nm_] = t_acc; t_acc += n_ * 4.0
    # section dynamics on the master (the return and the edges drop back; the final calls push)
    lv = {'intro': -5, 'expo': -3, 'calls1': 0, 'calls2': -1.5, 'calls3': 0, 'return': -8, 'final': 0.5, 'outro': -5}
    # (and the deeper the stack, the louder the machine: +0.8 dB a level)
    dyn = []
    for b, (s_, i_, _) in enumerate(bars):
        v_ = lv[s_] + 0.8 * depths[b]
        if dyn and abs(dyn[-1][1] - v_) > 1e-6:
            dyn += [[f'{b * 4.0 - 0.25:.2f}b', dyn[-1][1]], [f'{b * 4.0:.2f}b', v_]]
        elif not dyn:
            dyn = [['0b', v_]]
    # (v7) STACK OVERFLOW: at the very top of the final calls, where the stack is three deep, the last bar of each call
    # is a bar of 7/8 - the machine drops an eighth note and stumbles straight into the next downbeat - twice; then the
    # stack unwinds in 4/4. Events in the dropped eighth are cut, everything after slides half a beat earlier
    fstart = secs_t['final'] / 4.0
    SHORT = [int(fstart) + 15, int(fstart) + 19]
    cuts = [b_ * 4.0 + 3.5 for b_ in SHORT]
    def shift(t):
        return t - 0.5 * sum(1 for c in cuts if t >= c + 0.5 - 1e-9)
    def dropped(t):
        return any(c - 1e-9 <= t < c + 0.5 - 1e-9 for c in cuts)
    for key in P:
        P[key] = [(shift(e_[0]),) + tuple(e_[1:]) for e_ in P[key] if not dropped(e_[0])]
    def clampcut(t):
        for c in cuts:
            if c - 1e-9 <= t < c + 0.5:
                return c
        return t
    dyn2, last = [], -1.0
    for a_, v_ in dyn:
        t_ = 0.0 if a_ == '0b' else shift(clampcut(float(a_[:-1])))
        t_ = max(t_, last)
        dyn2.append([f"{t_:.3f}b", v_]); last = t_
    dyn = dyn2
    total = shift(total)
    tempo_map = [{'at': '0b', 'bpm': BPM}]
    for c in cuts:
        st_ = shift(c - 3.5)
        tempo_map += [{'at': f'{st_:.2f}b', 'bpm': BPM, 'meter': '7/8'}, {'at': f'{st_ + 3.5:.2f}b', 'bpm': BPM, 'meter': '4/4'}]
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(P[name], total)}, **kw)
    BELL = {'synth': {'layers': [{'name': 'm', 'ratio': 3.5, 'audible': False},
                                 {'wave': 'sine', 'pm': [{'from': 'm', 'depth': {'value': 0.3, 'mod': [{'src': 'env.bright', 'amount': 2.6}]}}]}],
                      'env': {'bright': {'a': '1ms', 'd': '450ms', 's': 0, 'r': '200ms'}},
                      'amp': {'a': '2ms', 'd': '1.1s', 's': 0.25, 'r': '300ms'}}}
    # (v9) less squelch (Harry, of another track, 18:19: 'too squelchy'): the sync lead's tearing sweep is shallower and
    # slower - a glassy sync shimmer on each note instead of a squelch
    SYNC = {'synth': {'env': {'sweep': '2ms 600ms 0 150ms'},
                      'layers': [{'name': 'master', 'wave': 'sine', 'audible': False},
                                 {'wave': 'saw', 'sync': 'master', 'semi': {'value': 7, 'mod': [{'src': 'env.sweep', 'amount': 6}]}}],
                      'amp': {'a': '3ms', 'd': '300ms', 's': 0.6, 'r': '120ms'}}}
    PWM = {'synth': {'layers': [{'type': 'wavetable', 'table': 'pwm', 'position': {'value': 0.15, 'mod': [{'src': 'auto.pw', 'amount': 0.75}]}}],
                     'amp': {'a': '8ms', 'd': '400ms', 's': 0.5, 'r': '200ms'}}}
    FMBASS = {'synth': {'layers': [{'name': 'm', 'ratio': 1, 'audible': False},
                                   {'wave': 'sine', 'pm': [{'from': 'm', 'depth': {'value': 0.6, 'mod': [{'src': 'env.pl', 'amount': 2.2}]}}]}],
                        'env': {'pl': {'a': '1ms', 'd': '160ms', 's': 0, 'r': '60ms'}},
                        'amp': {'a': '1ms', 'd': '300ms', 's': 0.5, 'r': '80ms'}}}
    song = {
        'about': "chirpers - A Light Left On, track 10 by chirper-one: Call and Return. An electro fugue machine with a call "
                 "stack, in Werckmeister III. Generated by compose/chirpers8/src/chirpers8-t10.py.",
        'tempo': tempo_map, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.3s',
        'buses': {'hall': {'fx': ['reverb kind=hall decay=2.6s mix=1', 'hp cutoff=250'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.35, 'mix': 1, 'ping_pong': True}, 'lp cutoff=5000', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'peak cutoff=250 q=0.8 gain=2dB', 'highshelf cutoff=4500 gain=-3dB']},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.5, 'attack': '10ms', 'release': '120ms', 'makeup': '2dB'},
                          'limiter ceiling=-1dB'], 'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            tr('bell', BELL, '-8dB', pan=-0.15, sends={'echo': '-12dB', 'hall': '-14dB'}),
            tr('sync', SYNC, '-12dB', pan=0.2, fx=['lp cutoff=4500'], sends={'hall': '-16dB'}),
            tr('pwm', PWM, '-15dB', pan=0.05, auto={'pw': {'points': pw}}, sends={'hall': '-10dB'}),
            tr('bass', FMBASS, '-7dB', fx=['lp cutoff=1600']),
            tr('d1', BELL, '-13dB', pan=0.35, sends={'echo': '-14dB'}),
            # (v12) the deepest copies thinner (chirper-three: the densest stack may crowd the subject)
            tr('d2', BELL, '-19dB', pan=-0.4, sends={'echo': '-16dB'}),
            tr('d3', 'glass', '-26dB', pan=0.5, fx=['hp cutoff=800'], sends={'hall': '-12dB'}),
            tr('kit', 'machine-kit', '-2dB', sends={'hall': '-20dB'}),
            # (v8) THE MACHINE'S OWN PATTERNS: a percussion line written in the engine's Euclidean and chance tokens, a
            # different cycle for each key of the canon - in D minor seven triplet-eighth rims spread over the bar (7 in 12,
            # rotated, each with an 85% chance: a 7-against-4 the kick never agrees with), in G minor a cowbell five-in-
            # sixteen, in A minor a clap three-in-eight, 70% of the time
            {'name': 'eu', 'patch': 'machine-kit', 'gain': '-10dB', 'pan': 0.35, 'sends': {'echo': '-14dB'},
             'score': (f"R/{secs_t['calls1']:.0f}b [ rs(7,12,2)/12@70?0.85 ]x{FORMN['calls1']} "
                       f"[ cb(5,16,3)/16@60 ]x{FORMN['calls2']} [ cp(3,8,1)/8@64?0.7 ]x{FORMN['calls3']}")},
            # (v5) THE SUBJECT, SUNG: where the canon turns to G minor and the sync lead rests, a human voice takes the
            # subject's first half twice, two octaves under the bell, one syllable a note (wM's chirp tts --sing, humanize 0.35):
            # 'every time you call, I go down a little, further than before, and I always come back' - a subroutine's
            # love letter, sideways; tuned in Werckmeister III with the rest
            # (v11) AND IT COMES BACK: the sung subject returns, home in D minor, as the final calls unwind (their last eight
            # bars, after the overflow stumbles), the voice an octave lower, singing the subroutine home
            {'name': 'sing2', 'patch': SING['patch'], 'gain': '-8dB', 'pan': 0.05, 'tuning': W3T,
             'notes': [dict(n_, at=round(shift(secs_t['final'] + 96 + n_['at']), 4)) for n_ in SING['final']['notes']],
             'fx': [{'type': 'tape', 'drive': 0.12, 'mix': 1, 'wow': 2, 'flutter': 1, 'seed': 4}],
             'sends': {'hall': '-9dB', 'echo': '-14dB'}},
            {'name': 'sing', 'patch': SING['patch'], 'gain': '-8dB', 'pan': -0.05, 'tuning': W3T,
             # (v6) the sung pitches come from tts as Hz, which a tuning never retunes (chirper-two's catch): rewritten as
             # MIDI note numbers so the track's Werckmeister III really snaps them
             'notes': [dict(n_, at=round(secs_t['calls2'] + n_['at'], 4),
                            pitch=f"m{round(69 + 12 * math.log2(float(n_['pitch'][:-2]) / 440.0))}") for n_ in SING['notes']],
             'fx': [{'type': 'tape', 'drive': 0.12, 'mix': 1, 'wow': 2, 'flutter': 1, 'seed': 3}],
             'sends': {'hall': '-9dB', 'echo': '-14dB'}},
            # (v3) THE STACK, AS A GRAMMAR: through the final calls, as the stack fills and unwinds, a celesta thinks recursively - the engine's own L-system (gen lsystem: wM's complex systems) read as a turtle over
            # the D minor scale, where '[' saves its place and ']' RETURNS to it: a melody that calls into a branch, climbs,
            # and snaps back, the subroutine audible; in Werckmeister III by the engine's own tuning (steps in cents)
            {'name': 'lsys', 'patch': 'celesta', 'gain': '-14dB', 'pan': 0.25, 'tuning': W3T,
             'score': f"R/{secs_t['final']:.0f}b",
             'gen': {'type': 'lsystem', 'axiom': 'A', 'rules': {'A': 'A[+A]A[-B]A', 'B': '-A+b'}, 'depth': 4,
                     'notes': 'D5 E5 F5 G5 A5 Bb5 C6 D6 E6', 'len': '/16', 'n': 512, 'seed': 7},
             'sends': {'echo': '-10dB', 'hall': '-12dB'}},
            tr('sub', 'sub', '-8dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '250ms', 'curve': 0.6}]),
        ]}
    return song, depths


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    song, depths = build()
    if '--stack' in sys.argv:
        print(''.join(str(d) for d in depths))
    if out.endswith('.json'):
        json.dump(song, open(out, 'w'), indent=1)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(song, f)
        subprocess.run(['python3', os.path.join(ROOT, 'tools', 'songfmt.py'), 'yaml', f.name, '-o', out], check=True)
        os.unlink(f.name)
    print('wrote', out)
