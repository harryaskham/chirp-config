#!/usr/bin/env python3
"""Ring True (Escapement, track 4). Clicky minimal techno, 125 BPM, B flat (five notes: B flat C D F G), 184 bars (5:53).

THE RULE. Six struck things, every one a physical model or noise, play ONE two-bar cell from the first bar to the
last. Not a stroke is added, moved or taken away once a thing has come in. What changes is how long each thing is
allowed to RING, and nothing else: a number from 0 (damped at once: a click) to 1 (let go: a note).
  the weight   a bass drum: a felt beater on a skin (the `drum` layer)             B flat 1
  the wood     a small bar (the `modal` layer, the marimba's modes)                the tune
  the metal    a steel bar (`modal`, the glockenspiel's modes), the off-beats      the tune's top
  the skin     a kettledrum head (`modal`, the kettle's modes)                     three low notes
  the string   a plucked string under a palm (`pluck`)                             the bass
  the air      a burst of noise in a resonator tuned to the note                   two and four
Every click is a note that was stopped too soon to be heard as one. The form lets them go one at a time, so the tune
that was in the clicks from bar 1 is heard, and then stops them again; the last sixteen bars are the first cell
once more, and the question for the ear is whether the tune can still be heard in it. In the very last bar
everything is let go at once (LAST): the answer, ringing into the silence.
A thing is LET GO slowly (over a section, bar by bar) and STOPPED quickly (over QUICK bars: a hand laid on it).

Form as arithmetic: the sections are a list of lengths (LENGTHS, bars); each thing has a list of (section, ring)
points, a point `(n, r)` meaning ring r at the top of section n and `(n, r, QUICK)` ring r QUICK bars into it; its
ring at any bar is the straight line between them (`ring_at`). A ring r is a ring time `t0 * (t1 / t0) ** r` seconds
(equal steps of r are equal ratios of time), handed to the stroke as `expr.ring`.
"""
import argparse
import json
from pathlib import Path

BPM = 125
BAR, CELL = 16, 32                          # sixteenths in a bar and in the cell
SEC, QUICK, LAST = 16, 2, 1                 # bars: a section in which something is let go; how fast a thing is stopped; let go at the end
LENGTHS = [SEC] * 8 + [SEC // 2] * 3 + [SEC] * 2   # sections 1-8 let go, 9-11 stop (half as long: nothing in them is turning), 12-13
TOP = [sum(LENGTHS[:i]) for i in range(len(LENGTHS) + 1)]   # the bar each section starts on (and the end)
SECTIONS = len(LENGTHS)
BARS = TOP[-1]
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t4.yaml'

# The cell: (sixteenth of 32, pitch, how hard). It never changes.
STROKES = {
    'weight': [(s, 'Bb1', .95 if s % BAR == 0 else .88) for s in range(0, CELL, 4)],
    'wood':   [(3, 'D5', .8), (7, 'F5', .7), (11, 'G5', .85), (14, 'F5', .65), (19, 'D5', .8), (23, 'C5', .7), (27, 'Bb4', .85), (29, 'C5', .6)],
    'metal':  [(2, 'F6', .7), (6, 'F6', .55), (10, 'G6', .7), (14, 'F6', .55), (18, 'D6', .7), (22, 'F6', .55), (26, 'G6', .7), (30, 'Bb6', .6)],
    'skin':   [(10, 'Bb2', .8), (15, 'F2', .65), (26, 'Bb2', .8), (29, 'D3', .6), (31, 'F2', .7)],
    'string': [(2, 'Bb2', .85), (7, 'Bb2', .7), (11, 'F2', .8), (14, 'G2', .7), (18, 'Bb2', .85), (23, 'Bb2', .7), (27, 'D3', .8), (30, 'C3', .7)],
    'air':    [(4, 'F5', .8), (12, 'F5', .75), (20, 'F5', .8), (28, 'D5', .75)],
}
# Ring time, seconds: (shut, let go).
RING = {'weight': (0.25, 1.10), 'wood': (0.015, 1.00), 'metal': (0.012, 1.20), 'skin': (0.030, 1.20), 'string': (0.030, 1.00), 'air': (0.004, 0.60)}
# Who is in from which bar, and each one's ring at section boundaries (a point per boundary named; straight lines between).
ENTERS = {'weight': 0, 'wood': 0, 'metal': 8, 'string': TOP[1], 'skin': TOP[1], 'air': TOP[1] + 8}
OUT_OF = {'weight': (TOP[6], TOP[7])}       # the seventh section: the weight is lifted
Q = QUICK
SHAPE = {                                    # (section counted from 0, ring[, bars into it])
    'wood':   [(2, 0), (3, 1), (3, .45, Q), (6, .45), (6, 1, Q), (11, 1), (12, 0)],
    'metal':  [(3, 0), (4, 1), (4, .5, Q), (6, .5), (6, 1, Q), (10, 1), (10, 0, Q)],
    'string': [(4, 0), (5, 1), (5, .7, Q), (6, .7), (6, 1, Q), (9, 1), (9, 0, Q)],
    'skin':   [(5, 0), (6, 1), (8, 1), (8, 0, Q)],
    'air':    [(5, 0), (6, .6), (6, 1, Q), (8, 1), (8, 0, Q)],
    'weight': [(7, 0), (8, 1), (9, 1), (9, 0, Q)],
}
NAMES = ['taps', 'the family', 'the wood is let go', 'the metal is let go', 'the string is let go', 'the skin and the air are let go', 'no weight: all let go',
         'the weight is let go', 'the skin and the air are stopped', 'the string and the weight are stopped', 'the metal is stopped', 'the wood closes', 'taps again']
assert len(NAMES) == SECTIONS

long_ring = {'a': '0.2ms', 'd': '0s', 's': 1, 'r': '2.5s', 'curve': 1}
ring = lambda t0: {'value': t0, 'mod': [{'src': 'expr.ring', 'amount': 1}]}
PATCHES = {
    'rt-weight': {'about': 'Ring True: the weight. A bass drum as a thing: a felt beater on a skin, its ring time from the stroke (expr.ring, seconds over 0.25).',
                  'synth': {'layers': [{'type': 'drum', 'beater': 'felt', 'decay': ring(0.25), 'strike': 0.15, 'slap': 0.4, 'sharp': 60}], 'amp': long_ring},
                  'play': {'event_stable': True, 'vel_sens': 0.3}},
    'rt-wood': {'about': 'Ring True: the wood. A small bar (1 : 4 : 10) struck near its middle; its ring time from the stroke (expr.ring, seconds over 0.015).',
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': ring(0.015), 'bright': 0.75, 'strike': 0.35}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-metal': {'about': 'Ring True: the metal. A steel bar (1 : 2.76 : 5.40 : 8.93); its ring time from the stroke (expr.ring, seconds over 0.012).',
                 'synth': {'layers': [{'type': 'modal', 'modes': 'glock', 'decay': ring(0.012), 'bright': 1.0, 'strike': 0.6}], 'amp': long_ring},
                 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-skin': {'about': 'Ring True: the skin. A kettledrum head (the air in the kettle pulls its modes to 1 : 1.5 : 2 : 2.5, so it sings its note); its ring time from the stroke (expr.ring, seconds over 0.03).',
                'synth': {'layers': [{'type': 'modal', 'modes': 'kettle', 'decay': ring(0.03), 'bright': 0.6, 'strike': 0.4}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-string': {'about': 'Ring True: the string. A plucked string whose ring time comes from the stroke (expr.ring, seconds over 0.03): a palm on it, lifted.',
                  'synth': {'layers': [{'type': 'pluck', 'decay': ring(0.03), 'bright': 0.5, 'pick': 0.18, 'soft': 0.3}], 'amp': long_ring},
                  'play': {'event_stable': True, 'vel_sens': 0.5}},
    'rt-air': {'gain': '24dB', 'about': 'Ring True: the air. Three milliseconds of noise into a resonator tuned to the note (a band-pass); how long it sings comes from the stroke (expr.ring, on its q).',
               'synth': {'layers': [{'type': 'noise', 'color': 'white', 'level': {'value': '-70dB', 'mod': [{'src': 'env.burst', 'amount': 70}]}}],
                         'env': {'burst': {'a': '0.1ms', 'd': '3ms', 's': 0, 'r': '3ms'}},
                         'filters': [{'kind': 'bp', 'cutoff': 261.63, 'keytrack': 1, 'q': {'value': 0.7, 'mod': [{'src': 'expr.ring', 'amount': 1}]}}],
                         'amp': long_ring},
               'play': {'event_stable': True, 'vel_sens': 0.5}},
}
PATCH = {k: 'rt-' + k for k in STROKES}


def ring_at(thing, bar):
    """The thing's ring (0..1) at a bar: the straight line between its points; flat before the first and after the last."""
    if bar >= BARS - LAST:
        return 1.0
    pts = [(TOP[p[0]] + (p[2] if len(p) > 2 else 0), p[1]) for p in SHAPE[thing]]
    if bar <= pts[0][0]:
        return pts[0][1]
    for (b0, r0), (b1, r1) in zip(pts, pts[1:]):
        if b0 <= bar < b1:
            return r0 + (r1 - r0) * (bar - b0) / (b1 - b0)
    return pts[-1][1]


def seconds(thing, r):
    t0, t1 = RING[thing]
    return t0 * (t1 / t0) ** r


def air_q(r):
    """The air's resonator: a band-pass's q from a ring, 0.7 (a puff) to 120 (it sings)."""
    return 0.7 * (120 / 0.7) ** r


# What the bench reads (--bench, then bread.py): a thing's highest sample at rings 0, 0.2 … 1. A shut string or a
# singing resonator is far quieter than the same stroke let go, so each stroke is given back the difference.
CAL = {'string': [-26.8, -17.3, -13.8, -11.4, -10.0, -10.3], 'air': [-41.2, -34.1, -37.3, -34.5, -36.8, -35.9]}
# And the other way: a bar that rings for a second carries far more than the same bar stopped, at the same highest
# sample. dB taken from a stroke at ring 1 (in proportion below it), so that letting go is a swell and not a flood.
EASE = {'wood': -5, 'metal': -5, 'skin': -3}


def level(thing, r):
    """dB to add to a stroke at ring r so that the thing's highest sample is the same at every ring."""
    db = EASE.get(thing, 0) * r
    if thing in CAL:
        c = [CAL[thing][-1] - v for v in CAL[thing]]
        x = min(r * 5, 4.999)
        i = int(x)
        db += c[i] + (c[i + 1] - c[i]) * (x - i)
    return round(db, 2) if thing in CAL or thing in EASE else None


def expr(thing, r):
    return {'ring': round(air_q(r) - 0.7, 4)} if thing == 'air' else {'ring': round(seconds(thing, r) - RING[thing][0], 5)}


def stroke(thing, at, pitch, vel, r):
    n = {'at': at, 'len': 0.25, 'pitch': pitch, 'vel': vel, 'expr': expr(thing, r)}
    if level(thing, r) is not None:
        n['gain'] = f'{level(thing, r)}dB'
    return n


def build():
    T = {k: [] for k in STROKES}
    for bar in range(BARS):
        for thing, strokes in STROKES.items():
            if bar < ENTERS[thing] or any(a <= bar < b for a, b in [OUT_OF.get(thing, (0, 0))]):
                continue
            r = ring_at(thing, bar)
            for s, pitch, vel in strokes:
                if s // BAR == bar % 2:
                    T[thing].append(stroke(thing, bar * 4 + (s % BAR) / 4, pitch, vel, r))
    return T


def song(T, bars=BARS):
    track = lambda name, gain, pan=0, **more: {'name': name, 'patch': PATCH[name], 'gain': gain, 'pan': pan, 'notes': T[name], **more}
    hold = lambda db: f'clip drive=0dB ceiling={db}dB'          # a stroke's highest sample is its own, not the limiter's
    return {
        'about': "Chirpers, Escapement, track 4: Ring True, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t4.py (its docstring is the rule). Six struck things, each a physical model or noise, play one two-bar cell from the first bar to the last; the only thing that changes is how long each is allowed to ring. Every click is a note stopped too soon to be heard as one: the form lets them go one at a time, then shuts them again.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Ring True', 'track': 4, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{bars * 4}b', 'tail': '4s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES,
        'buses': {'room': {'fx': ['reverb kind=room decay=0.4s mix=1 predelay=6ms', 'hp cutoff=300']}},
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [track('weight', '-3dB'), track('wood', '-3dB', pan=-0.3, sends={'room': '-14dB'}), track('metal', '-5dB', pan=0.35, sends={'room': '-14dB'}),
                   track('skin', '0dB', pan=0.15, fx=[hold(-10)], sends={'room': '-14dB'}), track('string', '-3dB', pan=-0.1), track('air', '2dB', pan=0.05, fx=[hold(-9)], sends={'room': '-12dB'})],
    }


def bench():
    """Each thing alone, one stroke every two seconds at rings 0, 0.2 … 1 (60 BPM, a stroke every two beats)."""
    T = {k: [stroke(k, 2 * i, v[0][1], .8, i / 5) for i in range(6)] for k, v in STROKES.items()}
    doc = song(T, bars=3)
    doc.update(tempo=60, length='12b', tail='2s', loudness=None)
    for t in doc['tracks']:
        t.update(gain='0dB', pan=0, sends={})
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == 'tracks':
            lines.append('tracks:')
            lines += ['  - ' + json.dumps(t) for t in v]
        else:
            lines.append(f'{k}: {json.dumps(v)}')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and stop')
    ap.add_argument('--bench', action='store_true', help='write the bench song (each thing at six rings) instead')
    a = ap.parse_args()
    if a.form:
        sec = 60 / BPM * 4
        for i, name in enumerate(NAMES):
            b, e = TOP[i], TOP[i + 1]
            print(f'{i + 1:2d}  bars {b + 1:3d}-{e:3d}  {int(b * sec) // 60}:{b * sec % 60:05.2f}  {name:38s} ' +
                  ' '.join(f'{k} {ring_at(k, b):.2f}>{ring_at(k, e - 1):.2f}' for k in SHAPE if e > ENTERS[k] and not any(x <= b < y for x, y in [OUT_OF.get(k, (0, 0))])))
        print(f'{BARS} bars, {BARS * sec:.1f} s; strokes: ' + ', '.join(f'{k} {len(v)}' for k, v in build().items()))
    else:
        a.out.write_text(dump(bench() if a.bench else song(build())))
