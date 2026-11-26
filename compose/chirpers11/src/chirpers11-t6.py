#!/usr/bin/env python3
"""Small Change (Escapement, track 6). Clicky minimal techno, 122 BPM, G minor, 192 bars (6:18).

THE RULE (the coin problem). Almost nothing is written: a bass drum, a bass, and one SEED, a single struck note every
bar or two. Everything else is change given for it. A pair of COINS is two echoes, p and q sixteenths long, that
feed themselves and each other. Every pass through the p coin lifts the sound a fifth (+7 semitones); every pass
through the q coin drops it a fourth (-5). So an echo that was passed a times through p and b times through q
  lands  p*a + q*b  sixteenths after the seed,
  sounds 7*a - 5*b  semitones from it (one step round the circle of fifths for every coin spent, whichever coin),
  and is heard on the side of the last coin it went through (p left, q right).
With coins of 3 and 5 the amounts 1, 2, 4 and 7 cannot be made, and from 8 on every sixteenth can (the largest
amount that cannot is p*q - p - q): a seed is answered by a few separate notes and then by a roll. The first five
steps round the fifths from B flat are B flat, F, C, G, D: G minor's five notes. Later steps leave the key, and the
loop gain (G) is set so that they have nearly gone by then.

The form changes the coins: 3 and 5 (7 cannot be made), 3 and 4 (5: it fills at once), 5 and 7 (23: sparse and long).
Form as arithmetic: SECTIONS is the table; each row says which pairs of coins hear the seed, how often it is
struck, on which sixteenth and note, and whether the drum and the bass play.

The pitch change is the engine's granular `pitch` effect inside each loop. It is late each pass, by about 14 ms
(up) and 18 ms (down) the first time and more on later passes, so LAG is taken off each loop's time: read on the
first seed, the change then peaks between 14 ms before and 23 ms after its sixteenths (sixteenths 3 to 16).
"""
import argparse
import json
from math import log10
from pathlib import Path

BPM = 122
S16 = 60000 / BPM / 4                       # a sixteenth, ms
BAR, SEC = 16, 16                           # sixteenths in a bar; bars in a section
UP, DOWN = 7, -5                            # a fifth up through the first coin, a fourth down through the second
LAG = {UP: 19.7, DOWN: 23.8}                # ms taken off a coin's time for the pitch effect's lateness (bench: late.py, lattice.py)
G = 0.62                                    # what a coin gives back each pass (the loop loses about 4 dB more: bench)
ALONE = 0                                   # dB the seeds' faders come up where there is no drum. 0: tried at 6, the finished sections came up 1.9 dB and the rest went to the master's limiter
PAIRS = {'a': (3, 5), 'b': (3, 4), 'c': (5, 7)}
PAN = {'a': 0.6, 'b': 0.3, 'c': 0.9}
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t6.yaml'

# name, pairs that hear the seed (in turn, one per strike), bars between strikes, sixteenth of the bar, seed notes in turn, drum, bass
SECTIONS = [
    ('one seed',            'a',   4, 0, ['Bb4'],               0, 0),
    ('the drum',            'a',   2, 0, ['Bb4'],               1, 0),
    ('the bass',            'a',   2, 0, ['Bb4', 'Eb4'],        1, 1),
    ('threes and fours',    'b',   2, 0, ['Bb4'],               1, 1),
    ('both purses',         'ab',  1, 0, ['Bb4', 'F4'],         1, 1),
    ('fives and sevens',    'c',   4, 0, ['Eb4', 'F4'],         0, 0),
    ('the drum again',      'c',   2, 0, ['Eb4', 'F4'],         1, 1),
    ('three purses',        'abc', 1, 0, ['Bb4', 'F4', 'Eb4'],  1, 1),
    ('off the beat',        'a',   2, 6, ['Eb4'],               1, 1),
    ('off the beat, up',    'a',   2, 6, ['F4'],                1, 1),
    ('home',                'a',   2, 0, ['Bb4'],               1, 1),
    ('the last seed',       'a',   4, 0, ['Bb4'],               0, 0),
]
BARS = len(SECTIONS) * SEC

PATCHES = {
    'sc-seed': {'about': 'Small Change: the seed. One vibraphone bar with no motor, short, with two milliseconds of noise on its front (a click that the coins carry too): the only struck note in the song.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '180ms', 'bright': 0.6, 'strike': 0.3},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.tick', 'amount': 70}]}}],
                          'env': {'tick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}},
                          'amp': {'a': '0.3ms', 'd': '250ms', 's': 0, 'r': '80ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'sc-kick': {'about': "Small Change: the drum. The machine's bass drum on G, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.5, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
}


def frobenius(p, q):
    return p * q - p - q


def lattice(p, q, upto):
    """{sixteenth: [semitones, ...]} for every way of making it from the two coins."""
    out = {}
    for a in range(upto // p + 1):
        for b in range((upto - p * a) // q + 1):
            if a + b:
                out.setdefault(p * a + q * b, []).append(UP * a + DOWN * b)
    return dict(sorted(out.items()))


def build():
    T = {'kick': [], 'bass': [], **{f'seed-{k}': [] for k in PAIRS}}
    for i, (name, pairs, every, at16, notes, drum, bass) in enumerate(SECTIONS):
        n = 0
        for bar in range(i * SEC, (i + 1) * SEC):
            if (bar - i * SEC) % every == 0:
                T[f'seed-{pairs[n % len(pairs)]}'].append({'at': bar * 4 + at16 / 4, 'len': 0.25, 'pitch': notes[n % len(notes)], 'vel': 0.9})
                n += 1
            if drum:
                for beat in range(4):
                    T['kick'].append({'at': bar * 4 + beat, 'len': 0.5, 'pitch': 'G1', 'vel': .95 if beat == 0 else .88})
            if bass:
                for off, ln, p in ((2, 1.5, 'G2'), (7, 1, 'G2'), (10, 1.5, 'F2' if bar % 4 == 3 else 'G2')):
                    T['bass'].append({'at': bar * 4 + off / 4, 'len': ln / 4, 'pitch': p, 'vel': .85})
    return T


def alone():
    """The seeds' fader ride: ALONE dB through the sections with no drum, 0 elsewhere, moved over the half beat before a section."""
    pts = []
    for i, sec in enumerate(SECTIONS):
        v = 0 if sec[5] else ALONE
        if pts and pts[-1][1] != v:
            pts.append([f'{i * SEC * 4 - 0.5}b', pts[-1][1]])
        if not pts or pts[-1][1] != v:
            pts.append([f'{i * SEC * 4}b', v])
    return {'points': pts + [[f'{BARS * 4}b', pts[-1][1]]], 'curve': 0}


def song():
    T = build()
    db = lambda x: f'{20 * log10(x):.2f}dB'
    under = {'type': 'pump', 'on': 'kick', 'depth': '-4dB', 'release': '170ms'}
    buses = {}
    for k, (p, q) in PAIRS.items():
        for coin, other, semi, side in ((p, q, UP, -1), (q, p, DOWN, 1)):
            me, you = f'{k}{coin}', f'{k}{other}'
            t = f'{coin * S16 - LAG[semi]:.2f}ms'
            buses[me] = {'pan': side * PAN[k], 'gain': '0dB',
                         'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, 'lp cutoff=10000', 'hp cutoff=150'],
                         'returns': [{'from': f'seed-{k}', 'gain': '0dB', 'time': t}, {'from': me, 'gain': db(G), 'time': t}, {'from': you, 'gain': db(G), 'time': t}]}
    return {
        'about': "Chirpers, Escapement, track 6: Small Change, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t6.py (its docstring is the rule). One struck note every bar or two, a bass drum and a bass are all that is written; the rest is change given for it by pairs of coins: two echoes, p and q sixteenths long, feeding themselves and each other, one lifting the sound a fifth each pass and the other dropping it a fourth. An echo lands p*a + q*b sixteenths after its seed, 7*a - 5*b semitones from it.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Small Change', 'track': 6, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{BARS * 4}b', 'tail': '5s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES, 'buses': buses,
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [{'name': 'kick', 'patch': 'sc-kick', 'gain': '-9dB', 'notes': T['kick'],
                    'fx': [{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]},
                   {'name': 'bass', 'patch': 'sub-sine', 'gain': '-13dB', 'notes': T['bass'], 'fx': [under]}] +
                  [{'name': f'seed-{k}', 'patch': 'sc-seed', 'gain': {'value': '-3dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()},
                    'notes': T[f'seed-{k}'], 'fx': ['clip drive=0dB ceiling=-12dB']} for k in PAIRS],   # the seed's highest sample is its own, not the limiter's
    }


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
    ap.add_argument('--form', action='store_true', help='print the form and the coins and stop')
    a = ap.parse_args()
    if a.form:
        sec = 60 / BPM * 4
        for k, (p, q) in PAIRS.items():
            lat = lattice(p, q, 24)
            print(f'coins {k}: {p} and {q}; largest amount that cannot be made {frobenius(p, q)}; made up to 24: ' + ' '.join(f'{s}:{"/".join(f"{x:+d}" for x in v)}' for s, v in lat.items()))
        for i, (name, pairs, every, at16, notes, drum, bass) in enumerate(SECTIONS):
            b = i * SEC
            print(f'{i + 1:2d}  bars {b + 1:3d}-{b + SEC:3d}  {int(b * sec) // 60}:{b * sec % 60:05.2f}  {name:20s} coins {pairs:3s} a seed every {every} bar(s) on sixteenth {at16} {"/".join(notes):12s} {"drum " if drum else ""}{"bass" if bass else ""}')
        T = build()
        print(f'{BARS} bars, {BARS * sec:.1f} s; written notes: ' + ', '.join(f'{k} {len(v)}' for k, v in T.items()))
    else:
        a.out.write_text(dump(song()))
