#!/usr/bin/env python3
"""Wind Down (Escapement, track 8, the closer). Clicky minimal techno, 124 BPM running down to 50, G minor, 200 bars.

THE RULE. Nothing here is new. One thing is taken from each of the other seven songs, gathered a section at a time
on one grid in one key, held together, and then let go one at a time, last in, first out, until the first thing on
the record (a click off the beat) is alone again. Then the spring runs down: over the last eight bars the tempo
falls from 124 to 50, each tick is let ring a little longer than the last, and the final stroke, let go altogether
and an octave down, lands ON the one, where that click has never been.

  from 1 Give or Take      the grid: a bass drum on the four and one click on the off-beats (sixteenths 2 6 10 14)
  from 7 Out of Step       the half-bar pattern x x . x . x x . on a short saw click
  from 5 Hearing Things    the bass with no fundamental (harmonics two to six), its line a tone down, off the beat
  from 4 Ring True         the cell's tune on the wooden bar, stopped; let go once everything is gathered
  from 2 Least Common      the meeting tune: a ping where two of the cycles 3, 5 and 7 meet, a chord where all three do
  from 3 Standing Room     standing room: two walls 3 and 5 sixteenths away, round the click
  from 6 Small Change      one seed every two bars and a pair of coins, 3 and 5, a fifth up and a fourth down
The click itself is Ring True's wooden bar playing Give or Take's grid: a note stopped too soon, until the end.

Form as arithmetic: GATHER lists the things in the order they come; each comes STEP bars after the last, all are
held for HOLD bars, they go in reverse order LEAVE bars apart, and the last WIND bars are the spring running down.
"""
import argparse
import json
from math import log, log10
from pathlib import Path

BPM, SLOW = 124, 50
S16 = 60000 / BPM / 4                       # a sixteenth, ms
BAR = 16
STEP, HOLD, LEAVE, WIND = 16, 32, 8, 8      # bars
GATHER = ['grid', 'pattern', 'ghost', 'cell', 'meetings', 'room', 'change']
COMES = {k: i * STEP for i, k in enumerate(GATHER)}
ALL = len(GATHER) * STEP                    # the bar at which everything is in
GOES = {k: ALL + HOLD + (len(GATHER) - 1 - i) * LEAVE for i, k in enumerate(GATHER)}   # last in, first out
GOES['grid'] = GOES['pattern'] + LEAVE      # the drum goes here; the click stays to the end
RUNS_DOWN = GOES['grid']
BARS = RUNS_DOWN + WIND
DRUM_IN = 8                                 # the bass drum comes eight bars after the click (and turns the listener round)
LET_GO = (ALL + HOLD // 2, ALL + HOLD)      # the cell's ring goes from STOPPED to 1 across these bars
STOPPED = 0.15                              # the cell's ring while it is gathered
ALONE = 6                                   # dB the click's fader comes up while it is alone (before the drum; as the spring runs down)
SHUT = -0.25                                # the click's: stopped sooner than Ring True stops anything (5 ms), so it is a tick and not a note
TICK, LAST = 'G6', 'G5'                     # the click's note (an octave over Give or Take's, clear of the cell and the pings); the last stroke's
CYCLES = (3, 5, 7)
PING = {(3, 5): 'D5', (3, 7): 'Bb4', (5, 7): 'F4'}
CHORD = ('G3', 'Bb3', 'D4', 'F4', 'A4')
CELL = [(3, 'D5', .8), (7, 'F5', .7), (11, 'G5', .85), (14, 'F5', .65), (19, 'D5', .8), (23, 'C5', .7), (27, 'Bb4', .85), (29, 'C5', .6)]
PATTERN = (0, 1, 3, 5, 6)                   # of eight sixteenths
GHOST = (('G1', 'G1', 'G1', 'Bb1'), ('G1', 'G1', 'G1', 'G1'), ('G1', 'G1', 'G1', 'C2'), ('G1', 'G1', 'D2', 'F2'))
WALLS = (3, 5)                              # sixteenths there and back
COINS, UP, DOWN, GIVE = (3, 5), 7, -5, 0.62
LAG = {UP: 19.7, DOWN: 23.8}                # ms the pitch effect is late (Small Change's bench)
WOOD = (0.015, 1.0)                         # the bar's ring time, seconds: stopped, let go
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t8.yaml'

open_amp = {'a': '0.2ms', 'd': '0s', 's': 1, 'r': '2.5s', 'curve': 1}
PATCHES = {
    'wd-wood': {'about': "Wind Down: Ring True's wooden bar (1 : 4 : 10), its ring time given by each stroke (expr.ring, seconds over 0.015), with the stick's click on its front (2 ms of noise). It is the click and the cell.",
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': {'value': WOOD[0], 'mod': [{'src': 'expr.ring', 'amount': 1}]}, 'bright': 0.75, 'strike': 0.35},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.stick', 'amount': 70}]}}],
                          'env': {'stick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}}, 'amp': open_amp},
                'play': {'event_stable': True, 'vel_sens': 0.6}},
    'wd-kick': {'about': "Wind Down: the drum. The machine's bass drum on G, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.5, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'wd-saw': {'about': 'Wind Down: a click that is five cycles of a saw (after Out of Step): on G3 that is 51 ms.',
               'synth': {'layers': [{'wave': 'saw'}], 'filters': ['lp cutoff=9000'], 'amp': {'a': '0.1ms', 'd': '45ms', 's': 0, 'r': '6ms', 'curve': 0}},
               'play': {'event_stable': True, 'vel_sens': 0.5}},
    'wd-ghost': {'about': 'Wind Down: a bass with no fundamental (after Hearing Things): harmonics two to six of the note and nothing at the note.',
                 'synth': {'layers': [{'type': 'additive', 'partials': [[2, 1], [3, 0.85], [4, 0.6], [5, 0.42], [6, 0.3]]}],
                           'amp': {'a': '4ms', 'd': '0s', 's': 1, 'r': '40ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'wd-ping': {'about': 'Wind Down: what two cycles make when they meet (after Least Common): a vibraphone bar with no motor.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '650ms', 'bright': 0.55, 'strike': 0.3}],
                          'amp': {'a': '0.3ms', 'd': '900ms', 's': 0, 'r': '200ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
    'wd-chord': {'about': 'Wind Down: what three cycles make when they meet: a short filtered chord.',
                 'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}, {'wave': 'pulse', 'level': '-8dB'}],
                           'filters': [{'kind': 'lp', 'cutoff': {'value': 500, 'mod': [{'src': 'env.f', 'amount': 2.6}]}, 'q': 1.4}],
                           'env': {'f': {'a': '1ms', 'd': '140ms', 's': 0, 'r': '80ms'}},
                           'amp': {'a': '1ms', 'd': '220ms', 's': 0, 'r': '90ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'wd-seed': {'about': 'Wind Down: the seed (after Small Change): a short vibraphone bar with 2 ms of noise on its front.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '180ms', 'bright': 0.6, 'strike': 0.3},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.tick', 'amount': 70}]}}],
                          'env': {'tick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}},
                          'amp': {'a': '0.3ms', 'd': '250ms', 's': 0, 'r': '80ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
}


def ring_s(r):
    return WOOD[0] * (WOOD[1] / WOOD[0]) ** r


def wood(at, pitch, vel, r):
    """One stroke on the bar at ring r (0 stopped .. 1 let go): its ring time, and 5 dB off at ring 1 so that letting go is a swell."""
    return {'at': round(at, 4), 'len': 0.25, 'pitch': pitch, 'vel': vel, 'expr': {'ring': round(ring_s(r) - WOOD[0], 5)}, 'gain': f'{round(-5 * max(r, 0), 2)}dB'}


def here(thing, bar):
    return COMES[thing] <= bar < GOES[thing]


def build():
    T = {k: [] for k in ('kick', 'tick', 'saw', 'ghost', 'cell', 'ping', 'chord', 'seed')}
    for bar in range(BARS):
        b = bar * 4
        down = bar >= RUNS_DOWN
        # from 1: the grid. The click is there from the first bar to the last; in the last WIND bars it is let ring more each bar.
        r = SHUT + (1 - SHUT) * (bar - RUNS_DOWN + 1) / (WIND + 1) if down else SHUT
        for s in (2, 6, 10, 14):
            T['tick'].append(wood(b + s / 4, TICK, .8 if s in (2, 10) else .7, r))
        if DRUM_IN <= bar < RUNS_DOWN:
            for beat in range(4):
                T['kick'].append({'at': b + beat, 'len': 0.5, 'pitch': 'G1', 'vel': .95 if beat == 0 else .88})
        if here('pattern', bar):
            for half in (0, 8):
                for s in PATTERN:
                    T['saw'].append({'at': b + (half + s) / 4, 'len': 0.2, 'pitch': 'G3', 'vel': .8 if s == 0 else .62})
        if here('ghost', bar):
            for i, s in enumerate((2, 6, 10, 14)):
                T['ghost'].append({'at': b + s / 4, 'len': 0.45, 'pitch': GHOST[bar % 4][i], 'vel': .85})
        if here('cell', bar):
            lo, hi = LET_GO
            r = STOPPED if bar < lo else 1 if bar >= hi else STOPPED + (1 - STOPPED) * (bar - lo) / (hi - lo)
            for s, pitch, vel in CELL:
                if s // BAR == bar % 2:
                    T['cell'].append(wood(b + (s % BAR) / 4, pitch, vel, r))
        if here('meetings', bar):
            for s in range(bar * BAR, (bar + 1) * BAR):          # the cycles are counted from the top of the song; nobody plays them
                meet = tuple(c for c in CYCLES if s % c == 0)
                if len(meet) == 2:
                    T['ping'].append({'at': s / 4, 'len': 1, 'pitch': PING[meet], 'vel': .75})
                elif len(meet) == 3:
                    T['chord'].append({'at': s / 4, 'len': 0.5, 'pitch': ','.join(CHORD), 'vel': .8})
        if here('change', bar) and (bar - COMES['change']) % 2 == 0:
            T['seed'].append({'at': b, 'len': 0.25, 'pitch': 'Bb4', 'vel': .9})
    # the final stroke: the click, let go altogether, on the one
    T['tick'].append(wood(BARS * 4, LAST, .9, 1))
    T['tick'][-1]['gain'] = '0dB'
    return T


def door(thing):
    """A bus fader that is shut (-60 dB) until its thing comes, open while it is here, and shut again over two bars as it goes."""
    a, z = COMES[thing] * 4, GOES[thing] * 4
    return {'points': [['0b', -60]] + ([[f'{a - 8}b', -60]] if a >= 8 else []) + [[f'{a}b', 0], [f'{z}b', 0], [f'{z + 8}b', -60], [f'{BARS * 4}b', -60]], 'curve': 0}


def alone():
    """The click's fader ride: ALONE dB before the drum comes, 0 while anything else plays, back up over the first bar of the wind-down."""
    a, z = DRUM_IN * 4, RUNS_DOWN * 4
    return {'points': [['0b', ALONE], [f'{a - 0.5}b', ALONE], [f'{a}b', 0], [f'{z}b', 0], [f'{z + 4}b', ALONE], [f'{BARS * 4 + 4}b', ALONE]], 'curve': 0}


def song():
    T = build()
    db = lambda x: f'{20 * log10(x):.2f}dB'
    under = {'type': 'pump', 'on': 'kick', 'depth': '-4dB', 'release': '170ms'}
    hold = lambda d: f'clip drive=0dB ceiling={d}dB'
    buses = {'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=25ms', 'hp cutoff=350', 'lp cutoff=6000']}}
    for me, you, n, side in (('wall-l', 'wall-r', WALLS[0], -0.7), ('wall-r', 'wall-l', WALLS[1], 0.7)):
        buses[me] = {'pan': side, 'gain': {'value': '0dB', 'mod': [{'src': 'auto.door', 'amount': 1}]}, 'auto': {'door': door('room')},
                     'fx': ['lp cutoff=4500', 'hp cutoff=300'],
                     'returns': [{'from': 'tick', 'gain': '-4dB', 'time': f'{n}/16'}, {'from': you, 'gain': '-3dB', 'time': f'{n}/16'}]}
    for me, you, n, semi, side in (('coin-up', 'coin-down', COINS[0], UP, -0.5), ('coin-down', 'coin-up', COINS[1], DOWN, 0.5)):
        t = f'{n * S16 - LAG[semi]:.2f}ms'
        buses[me] = {'pan': side, 'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, 'lp cutoff=10000', 'hp cutoff=150'],
                     'returns': [{'from': 'seed', 'gain': '0dB', 'time': t}, {'from': me, 'gain': db(GIVE), 'time': t}, {'from': you, 'gain': db(GIVE), 'time': t}]}
    end = BARS * 4
    return {
        'about': "Chirpers, Escapement, track 8: Wind Down, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t8.py (its docstring is the rule). The closer: one thing from each of the other seven songs, gathered a section at a time on one grid in G minor, held, and let go one at a time until the click that opened the record is alone; then the tempo runs down from 124 to 50 and the last stroke, let ring, lands on the one.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Wind Down', 'track': 8, 'year': 2026},
        'tempo': [{'at': '0b', 'bpm': BPM}, {'at': f'{RUNS_DOWN * 4}b', 'bpm': BPM}, {'at': f'{end}b', 'bpm': SLOW, 'ramp': True}],
        'seed': 1, 'event_stable': True, 'length': f'{end + 4}b', 'tail': '4s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES, 'buses': buses,
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [
            {'name': 'kick', 'patch': 'wd-kick', 'gain': '-9dB', 'notes': T['kick'], 'fx': [{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]},
            {'name': 'ghost', 'patch': 'wd-ghost', 'gain': '-20dB', 'notes': T['ghost'], 'fx': ['lp cutoff=900', under]},
            {'name': 'tick', 'patch': 'wd-wood', 'gain': {'value': '-7dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()}, 'pan': 0, 'notes': T['tick'], 'fx': [hold(-12)], 'sends': {'hall': '-16dB'}},
            {'name': 'saw', 'patch': 'wd-saw', 'gain': '-12dB', 'pan': -0.25, 'notes': T['saw']},
            {'name': 'cell', 'patch': 'wd-wood', 'gain': '-1dB', 'pan': 0.3, 'notes': T['cell'], 'sends': {'hall': '-12dB'}},
            {'name': 'ping', 'patch': 'wd-ping', 'gain': '-12dB', 'pan': -0.15, 'notes': T['ping'], 'sends': {'hall': '-10dB'}},
            {'name': 'chord', 'patch': 'wd-chord', 'gain': '-8dB', 'pan': 0.1, 'notes': T['chord'], 'fx': [hold(-8), under], 'sends': {'hall': '-8dB'}},
            {'name': 'seed', 'patch': 'wd-seed', 'gain': '-6dB', 'notes': T['seed'], 'fx': [hold(-12)]},
        ],
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


def clock(bar):
    """Seconds at the top of a bar: steady to RUNS_DOWN, then a tempo falling in a straight line (against beats) to SLOW."""
    t = min(bar, RUNS_DOWN) * 4 * 60 / BPM
    if bar > RUNS_DOWN:
        n, x = WIND * 4, (bar - RUNS_DOWN) * 4
        k = (SLOW - BPM) / n
        t += 60 / k * log((BPM + k * x) / BPM)
    return t


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and stop')
    a = ap.parse_args()
    if a.form:
        marks = sorted([(COMES[k], f'{k} comes') for k in GATHER] + [(DRUM_IN, 'the drum comes'), (ALL, 'all gathered'), (LET_GO[0], 'the cell is let go')] +
                       [(GOES[k], f'{k} goes' if k != 'grid' else 'the drum goes; the spring runs down') for k in GATHER] + [(BARS, 'the last stroke, on the one')])
        for bar, what in marks:
            t = clock(bar)
            print(f'bar {bar + 1:3d}  {int(t) // 60}:{t % 60:05.2f}  {what}')
        T = build()
        print(f'{BARS} bars, {clock(BARS):.1f} s to the last stroke; strokes: ' + ', '.join(f'{k} {len(v)}' for k, v in T.items()))
        ticks = [clock(RUNS_DOWN + (bar * 16 + s) / 16) for bar in range(WIND) for s in (2, 6, 10, 14)] + [clock(BARS)]
        print('the spring: the gap between ticks goes ' + ' '.join(f'{(b - a) * 1000:.0f}' for a, b in zip(ticks, ticks[1:]))[:60] + ' ... ' +
              ' '.join(f'{(b - a) * 1000:.0f}' for a, b in zip(ticks[-5:], ticks[-4:])) + ' ms (the last is the half beat to the one)')
    else:
        a.out.write_text(dump(song()))
