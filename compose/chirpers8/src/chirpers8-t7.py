#!/usr/bin/env python3
"""chirpers8-t7 (chirper-one): "Annealing" - for chirpers VIII, the ode to computer music.

A machine that composes its own tune while you listen, by SIMULATED ANNEALING - the way the chirpers' own songs are
hill-climbed, turned inside out and played. A sixteen-step sequence starts as noise: random notes across three
octaves, random rests, every pitch tens of cents off any scale. Every bar is one round: the machine proposes small
mutations and keeps the ones that lower its error - and, while it is still HOT, sometimes keeps a worse one, so it
can climb out of a wrong valley. The TEMPERATURE falls through the track. The listener hears the search: wild,
detuned, glitching blips that slowly find a key, then a rhythm, then a tune, until - minutes in - a catchy little
minor riff locks into 5-limit JUST INTONATION and the chords stop beating. Then the machine reheats once, for luck.

Every part anneals at its own rate:
- seq: the candidate tune (moog-seq through a filter and a bit-crusher that open and dirty with temperature);
- pad: pure sine partials for each chord, each voice detuned at random by the temperature - audible BEATING that
  slows, and stops, as the tuning cools into just ratios;
- bass: octave-bouncing roots whose cents drift with the temperature;
- drums: an electro kit whose sixteen-step pattern is sampled from noise at high temperature and from a motorik
  target as it cools.
Tuning: A = 220 Hz, 5-limit just A minor (1, 9/8, 6/5, 4/3, 3/2, 8/5, 9/5), every pitch written in Hz.
Form (bars): power-on 12 / epochs 20, 18, 24, 14, 28 (cooling) / converged 16 / reheat 10 / coda 14 = 156 at 116 bpm.
Emits songs/chirpers8-t7.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, math, os, random, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers8-t7.yaml")
BPM = 116.0
SEED = 20261101

RATIOS = [1, 9 / 8, 6 / 5, 4 / 3, 3 / 2, 8 / 5, 9 / 5]          # 5-limit just A minor
A3 = 220.0
def hz(deg, cents=0.0, base=A3):
    o, d = divmod(deg, 7)
    return base * (2 ** o) * RATIOS[d] * 2 ** (cents / 1200.0)
def tok(f): return f"m{69 + 12 * math.log2(f / 440.0):.3f}"     # fractional MIDI: any pitch, chords too

FORM = [('power', 12), ('e1', 20), ('e2', 18), ('e3', 24), ('e4', 14), ('e5', 28), ('converged', 16), ('reheat', 10), ('coda', 14)]
# THE TARGET: what the search is looking for (degrees above A3; None = rest). A4 . C5 E5 D5 . C5 . A4 G4 . E4 G4 A4 . .
TARGET = [7, None, 9, 11, 10, None, 9, None, 7, 6, None, 4, 6, 7, None, None]
# chords (root degree for the bass; voices for the pad), spans in bars, cycling: Am - F - C - G (just)
CHORDS = [(0, [0, 2, 4, 7]), (5, [5, 7, 9, 12]), (2, [2, 4, 6, 9]), (6, [6, 8, 10, 13])]
SPANS = [6, 5, 7, 6, 5, 8, 6, 7]
# drums: the motorik target (16 steps)
DT = {'k': [0, 4, 8, 12], 's': [4, 12], 'h': [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15], 'oh': [2, 10], 'cp': [12]}


def line(events, total):
    ev = sorted(events, key=lambda e: e[0])
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
    for name, n in FORM:
        for i in range(n):
            bars.append((name, i))
    nb = len(bars)
    total = nb * 4.0
    # ---- the temperature schedule ----
    T = []
    cool_start, cool_end = 12, 12 + 20 + 18 + 24 + 14 + 28          # bars 12..116 cool from 1 to ~0.03
    for b, (s, i) in enumerate(bars):
        if s == 'power':
            T.append(1.0)
        elif b < cool_end:
            x = (b - cool_start) / (cool_end - cool_start)
            T.append(round(math.exp(-3.5 * x), 4))
        elif s == 'converged':
            T.append(0.0)
        elif s == 'reheat':
            T.append(round(0.85 * (1 - i / 10) ** 0.5, 4))
        else:                                                    # coda: cold again
            T.append(round(max(0.0, 0.25 * (1 - i / 8)), 4))
    # ---- the annealing search ----
    cand = [(rng.randint(0, 20) if rng.random() > 0.3 else None, rng.uniform(-60, 60)) for _ in range(16)]
    def step_loss(c, t):
        d, cents = c
        if t is None:
            return 0.0 if d is None else 1.0
        if d is None:
            return 1.2
        return min(3.0, abs(d - t) * 0.5) + abs(cents) / 40.0
    def loss(cs): return sum(step_loss(c, t) for c, t in zip(cs, TARGET))
    seq_states, losses = [], []
    for b, (s, i) in enumerate(bars):
        temp = T[b]
        if s == 'converged' or (s == 'coda' and i >= 8):
            cand = [(t, 0.0) for t in TARGET]
        elif s == 'reheat' and i == 0:
            # the reheat: half the steps thrown back into noise
            cand = [((rng.randint(0, 20) if rng.random() > 0.3 else None), rng.uniform(-50, 50)) if rng.random() < 0.5 else c for c in cand]
        else:
            for _ in range(3 if s != 'power' else 1):
                j = rng.randrange(16)
                d, cents = cand[j]
                if rng.random() < 0.25:
                    nd = None if d is not None else rng.randint(0, 20)
                else:
                    k = 1 + int(4 * temp)
                    nd = max(0, min(20, (d if d is not None else rng.randint(0, 20)) + rng.randint(-k, k)))
                nc = cents * 0.8 + rng.gauss(0, 40 * temp)
                new = list(cand); new[j] = (nd, nc)
                dl = loss(new) - loss(cand)
                if dl <= 0 or rng.random() < math.exp(-dl / (temp * 1.5 + 1e-6)):
                    cand = new
        seq_states.append(list(cand)); losses.append(round(loss(cand), 3))
    # ---- render the parts ----
    P = {k: [] for k in ('seq', 'pad', 'bass', 'kit')}
    span_i, span_left, chord_i = 0, SPANS[0], 0
    pad_cents = [0.0] * 4
    for b, (s, i) in enumerate(bars):
        t0 = b * 4.0
        temp = T[b]
        on = s != 'power' or i >= 4
        # seq: the candidate, sixteen steps
        if on:
            for q, (d, cents) in enumerate(seq_states[b]):
                if d is None: continue
                acc = 92 if q % 4 == 0 else 78
                P['seq'].append((t0 + q * 0.25, tok(hz(d, cents)), 0.22, acc))
        # chords: spans cycle; the pad's voices re-detune at each span by the temperature
        if span_left == 0:
            span_i += 1; span_left = SPANS[span_i % len(SPANS)]; chord_i = (chord_i + 1) % 4
        root, voices = CHORDS[chord_i]
        if span_left == SPANS[span_i % len(SPANS)] or b == 0:
            pad_cents = [rng.gauss(0, 35 * temp) for _ in voices]
        span_left -= 1
        if s not in ('power',) or i >= 8:
            chord = ','.join(tok(hz(v, c)) for v, c in zip(voices, pad_cents))
            P['pad'].append((t0, chord, 3.9, 70))
            bc = rng.gauss(0, 30 * temp)
            for q in range(8):
                f = hz(root, bc, base=55.0) * (2 if q % 2 else 1)
                P['bass'].append((t0 + q * 0.5, tok(f), 0.4, 96 if q % 2 == 0 else 80))
        # drums: sampled per step from noise (hot) or from the motorik target (cold)
        if s != 'power' or i >= 6:
            for piece, tgt in DT.items():
                for q in range(16):
                    p = (1 - temp) * (1.0 if q in tgt else 0.0) + temp * (0.22 if piece != 'k' else 0.3)
                    if rng.random() < p:
                        P['kit'].append((t0 + q * 0.25, piece, 0.2, 100 if q in tgt else 76))
    # the temperature as a lane (one point a bar)
    Tpts = [[f'{b * 4.0:.1f}b', T[b]] for b in range(nb)]
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(P[name], total)}, **kw)
    song = {
        'about': "chirpers - chirpers VIII, track 7 by chirper-one: Annealing. A sequence that composes itself by simulated "
                 "annealing while you listen. Generated by compose/chirpers8/src/chirpers8-t7.py.",
        'tempo': BPM, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '2s',
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3s mix=1', 'hp cutoff=200'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.4, 'mix': 1}, 'lp cutoff=4000', 'hp cutoff=250'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=30', 'peak cutoff=60 q=0.9 gain=-5dB', 'peak cutoff=300 q=0.8 gain=-2dB', 'highshelf cutoff=4500 gain=7dB']},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.5, 'attack': '10ms', 'release': '120ms', 'makeup': '2dB'},
                          'limiter ceiling=-1dB']},
        'tracks': [
            tr('seq', 'moog-seq', '-7dB', sends={'echo': '-12dB', 'hall': '-16dB'},
               fx=[{'type': 'filter', 'kind': 'lp', 'q': 1.2, 'cutoff': {'value': 3200, 'mod': [{'src': 'auto.T', 'amount': 1.8}]}},
                   {'type': 'crush', 'bits': 5, 'rate': {'value': 6000}, 'mix': {'value': 0, 'mod': [{'src': 'auto.T', 'amount': 0.7}]}}],
               auto={'T': {'points': Tpts}}),
            tr('pad', 'partial', '-12dB', sends={'hall': '-8dB'}),
            tr('bass', 'moog-seq', '-8dB', fx=['lp cutoff=900']),
            tr('kit', 'electro-kit', '-5dB', sends={'hall': '-20dB'}),
        ]}
    return song, losses, T


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    song, losses, T = build()
    if '--loss' in sys.argv:
        print([losses[b] for b in range(0, len(losses), 8)])
    if out.endswith('.json'):
        json.dump(song, open(out, 'w'), indent=1)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(song, f)
        subprocess.run(['python3', os.path.join(ROOT, 'tools', 'songfmt.py'), 'yaml', f.name, '-o', out], check=True)
        os.unlink(f.name)
    print('wrote', out)
