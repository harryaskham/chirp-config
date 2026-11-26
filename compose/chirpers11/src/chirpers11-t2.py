#!/usr/bin/env python3
"""Least Common (chirpers11, track 2). Clicky minimal techno, 126 BPM, G minor, 210 bars (6:40).

THE RULE. Three clicks keep cycles of 3, 5 and 7 sixteenths against a bass drum on every fourth. They are never
told what to do after that: everything else in the song is what happens when they MEET.
  two meet   -> a ping. 3 with 5 (every 15 sixteenths) rings D, 3 with 7 (every 21) B flat, 5 with 7 (every 35) F.
  three meet -> a chord (every 105 sixteenths: six bars and nine sixteenths).
  three meet ON THE BASS DRUM -> the song turns a page (every 420 sixteenths: 26 bars and a beat. So the pages turn
                on beat two, then beat three, then beat four).
  all meet ON THE ONE -> once in 105 bars (1680 sixteenths = 3 x 5 x 7 x 16). That is a HALF of the song.
Between two chords the pings fall on sixteenths 15 21 30 35 42 45 60 63 70 75 84 90: twelve notes, the same forwards
and backwards (gaps 15 6 9 5 7 3 15 3 7 5 9 6 15). Nobody wrote that tune. It comes round every 105 sixteenths, nine
sixteenths later in the bar each time, so it visits every sixteenth of the bar once before it is home.

THE SECOND HALF IS THE FIRST, ONE SIZE UP: cycles of 3, 5 and 7 BEATS against the bar of four. 3 x 5 x 7 x 4 beats is
105 bars again. Each long cycle is filled with the NEXT one's number, spread as evenly as it goes (Euclid): five
strokes in the three beats, seven in the five, three in the seven. Their meetings are the same tune four times
slower, so it is held, not struck: a tone that changes when two cycles begin together. From the seventh page the small
tune comes back over it (pings where cycles of 3, 5 and 7 sixteenths WOULD meet, though nobody is playing them): the
same tune at two sizes at once.

The four's own parts (bass, off-beat hat, clap) come in a page at a time and are the only things placed by page. The
chord is Give or Take's (track 1: G minor seventh) with its ninth on top, so the two songs can be laid over each other.

Form as arithmetic: everything below is computed from CYCLES, BAR and BEAT. Nothing is typed as a bar number.
"""
import argparse
import json
from math import lcm
from pathlib import Path

BPM = 126
BEAT, BAR = 4, 16                       # sixteenths
CYCLES = (3, 5, 7)                      # the three clicks, sixteenths (first half) or beats (second half)
VOICES = ('three', 'five', 'seven')
SUPER = lcm(*CYCLES)                    # 105: the three meet
PAGE = lcm(SUPER, BEAT)                 # 420: the three meet on the bass drum
HALF = lcm(SUPER, BAR)                  # 1680: all meet on the one (105 bars)
TOTAL = 2 * HALF
assert (SUPER, PAGE, HALF) == (105, 420, 1680) and HALF % BAR == 0 and PAGE // BEAT % 4 == 1
KEY = 'G'
PING = {(3, 5): 'D5', (3, 7): 'Bb4', (5, 7): 'F4'}          # the commonest meeting gets the plainest note
TONE = {(3, 5): 'D4', (3, 7): 'Bb3', (5, 7): 'F3'}           # the same three notes an octave down, held
CHORD = ('G3', 'Bb3', 'D4', 'F4', 'A4')
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t2.yaml'

PATCHES = {
    'lc-kick': {'about': "Least Common: the four. The drum machine's bass drum resting on G, short enough to leave the sixteenth before the next beat empty.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.55, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'lc-three': {'about': 'Least Common: the click that counts three. Ten milliseconds of noise above 5 kHz: a tick with no note.',
                 'synth': {'layers': [{'type': 'noise', 'color': 'white'}], 'filters': ['hp cutoff=5000', 'peak cutoff=8500 q=2 gain=8dB'],
                           'amp': {'a': '0.1ms', 'd': '10ms', 's': 0, 'r': '8ms', 'curve': 3}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-five': {'about': 'Least Common: the click that counts five. A small wooden bar (1 : 4 : 10) struck hard and damped at once: a tock on G.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '55ms', 'bright': 0.8, 'damp': 0.4, 'strike': 0.4}],
                          'amp': {'a': '0.2ms', 'd': '80ms', 's': 0, 'r': '30ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-seven': {'about': "Least Common: the click that counts seven. The drum machine's rim, tuned to G: two short pings and a click, a knock.",
                 'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'rim', 'decay': '45ms'}}],
                           'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-ping': {'about': 'Least Common: what two clicks make when they meet. A vibraphone bar with no motor, half a second long.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '650ms', 'bright': 0.55, 'strike': 0.3}],
                          'amp': {'a': '0.3ms', 'd': '900ms', 's': 0, 'r': '200ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
    'lc-chord': {'about': 'Least Common: what three clicks make when they meet. A short filtered chord for a delay to carry.',
                 'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}, {'wave': 'pulse', 'level': '-8dB'}],
                           'filters': [{'kind': 'lp', 'cutoff': {'value': 500, 'mod': [{'src': 'env.f', 'amount': 2.6}]}, 'q': 1.4}],
                           'env': {'f': {'a': '1ms', 'd': '140ms', 's': 0, 'r': '80ms'}},
                           'amp': {'a': '1ms', 'd': '220ms', 's': 0, 'r': '90ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'lc-tone': {'about': 'Least Common: the meetings one size up. A plain held tone, a sine and a little of its octave, that takes a beat to arrive.',
                'synth': {'layers': [{'wave': 'sine'}, {'wave': 'triangle', 'semi': 12, 'level': '-16dB'}],
                          'amp': {'a': '240ms', 'd': '0s', 's': 1, 'r': '900ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.2}},
    'lc-hat': {'about': "Least Common: the off beat. The drum machine's hat, closed.",
               'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '45ms'}}],
                         'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'lc-clap': {'about': "Least Common: two and four. The drum machine's clap, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'clap', 'decay': '140ms', 'bursts': 3}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '300ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
}


def euclid(k, n):
    """k strokes spread over n steps as evenly as they go, the first on the first step."""
    return [i * n // k for i in range(k)]


def touch(pos):
    """How hard a click lands: hardest where it catches the bass drum, lighter on the off beat, lightest between."""
    return .92 if pos % BEAT == 0 else .74 if pos % BEAT == 2 else .58


def build():
    T = {n: [] for n in ('kick', 'three', 'five', 'seven', 'ping', 'chord', 'tone', 'bass', 'hat', 'clap')}
    marks = []

    def add(tr, s16, len16, pitch, vel, **more):
        T[tr].append({'at': round(s16 / BEAT, 4), 'len': round(len16 / BEAT, 4), 'pitch': pitch, 'vel': round(vel, 3), **more})

    pitch = {'three': 'C6', 'five': 'G5', 'seven': 'G4'}
    # ---- the first half: cycles of 3, 5 and 7 sixteenths. Who is in, by supercycle (the three meet at each one's head).
    supers = HALF // SUPER                                    # 16
    pages = HALF // PAGE                                      # 4
    per_page = PAGE // SUPER                                  # 4
    enters = {'three': 0, 'five': 1, 'seven': 2}              # one more click each time the three would have met
    last = supers - 1                                         # the last supercycle of the half: the four stops, to come back on the one
    for s in range(0, HALF):
        n = s // SUPER
        here = [c for c, v in zip(CYCLES, VOICES) if s % c == 0 and (n >= enters[v] or s == 0)]
        for c, v in zip(CYCLES, VOICES):
            if c in here:
                add(v, s, 1, pitch[v], touch(s))
        if len(here) == 2:
            add('ping', s, 4, PING[tuple(here)], .8)
        if len(here) == 3:
            add('chord', s, 2, ','.join(CHORD), .85 if s % BEAT == 0 else .7)
        if s % BEAT == 0 and n != last:
            add('kick', s, 2, 'G1', .95 if s % BAR == 0 else .88)
    marks += [('first half: three, five and seven sixteenths', 0)] + [(f'page {p + 1} (the three meet on beat {p * PAGE // BEAT % 4 + 1})', p * PAGE) for p in range(1, pages)]
    marks += [('the four stops', last * SUPER)]
    # ---- the second half: one size up. Cycles of 3, 5 and 7 beats, each filled with the next one's number.
    fill = {c: euclid(CYCLES[(i + 1) % 3], c * BEAT) for i, c in enumerate(CYCLES)}
    assert [len(fill[c]) for c in CYCLES] == [5, 7, 3]
    held = []                                                  # (sixteenth, the cycles that begin together)
    for s in range(HALF, TOTAL):
        r = s - HALF
        heads = [c for c in CYCLES if r % (c * BEAT) == 0]
        for c, v in zip(CYCLES, VOICES):
            if r % (c * BEAT) in fill[c]:
                add(v, s, 1, pitch[v], touch(s) if r % (c * BEAT) else .95)
        if len(heads) >= 2:
            held.append((s, tuple(heads)))
        if s % BEAT == 0:
            add('kick', s, 2, 'G1', .95 if s % BAR == 0 else .88)
    held.append((TOTAL, tuple(CYCLES)))
    for (s, heads), (nxt, _) in zip(held, held[1:]):
        if len(heads) == 3:
            add('chord', s, 2, ','.join(CHORD), .85)
            continue                                           # after a chord the tone rests until the next two meet
        add('tone', s, nxt - s - 2, TONE[heads], .7)
    # the same tune at both sizes: from the seventh page the pings come back over the held tones, at the small
    # cycles' own places (three, five and seven sixteenths counted from the top of the half, nobody playing them)
    for s in range(HALF + 2 * PAGE, TOTAL):
        small = tuple(c for c in CYCLES if (s - HALF) % c == 0)
        if len(small) == 2:
            add('ping', s, 4, PING[small], .62)
    # home: everything meets on the one, and that is the end
    add('chord', TOTAL, 8, ','.join(CHORD), .9)
    add('kick', TOTAL, 2, 'G1', .95)
    for v in VOICES:
        add(v, TOTAL, 1, pitch[v], .95)
    marks += [('second half: three, five and seven beats', HALF)] + [(f'page {p + 5} (the three meet on beat {p * PAGE // BEAT % 4 + 1})', HALF + p * PAGE) for p in range(1, pages)]
    marks += [('only the drum is left of the four', HALF + last * SUPER), ('home', TOTAL)]
    # ---- the four's own parts: a bass that never plays with the drum, an off-beat hat, a clap on two and four.
    # Pages (from 0): the bass from page 1; the hat on pages 2, 3 and 6, 7; the clap on page 3 and pages 5, 6, 7.
    # In the last supercycle of the first half the four stops (the drum too) and comes back on the one; in the last
    # supercycle of the second half only the four is left of its parts (the drum), under the clicks, to the end.
    cell = ((2, 1.5, 'G2'), (7, 1, 'G2'), (10, 1, 'Bb2'), (14, 1.5, 'G2'))
    for s0 in range(0, TOTAL, BAR):
        page = s0 // PAGE
        if last * SUPER <= s0 < HALF or s0 >= HALF + last * SUPER:
            continue
        if page >= 1:
            for off, ln, p in cell:
                add('bass', s0 + off, ln, p, .85)
        if page in (2, 3, 6, 7):
            for off in (2, 6, 10, 14):
                add('hat', s0 + off, 1, 'A#4', .7)
        if page in (3, 5, 6, 7):
            for off in (4, 12):
                add('clap', s0 + off, 1, 'C4', .7)
    return T, marks


def song():
    T, marks = build()
    def track(name, patch, gain, pan=0, **more):
        return {'name': name, 'patch': patch, 'gain': gain, 'pan': pan, 'notes': sorted(T[name], key=lambda n: n['at']), **more}
    echo = lambda n, mix, fb: {'type': 'delay', 'time': f'{n}/16', 'mix': mix, 'feedback': fb, 'tone': 2600}
    under = {'type': 'pump', 'on': 'kick', 'depth': '-5dB', 'release': '170ms'}
    hold = lambda db: f'clip drive=0dB ceiling={db}dB'          # a click's level is its own, not the limiter's
    doc = {
        'about': "Chirpers, album eleven, track 2: Least Common, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t2.py (its docstring is the rule). Three clicks on cycles of 3, 5 and 7 sixteenths against a bass drum on every fourth; a ping where two meet, a chord where three meet, a new page where three meet on the drum, and all of it on the one once in 105 bars. The second half is the first, one size up.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Least Common', 'track': 2, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{(TOTAL + BAR) // BEAT}b', 'tail': '3s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -13,
        'patches': PATCHES,
        'buses': {'room': {'fx': ['reverb kind=room decay=0.5s mix=1 predelay=8ms', 'hp cutoff=400']},
                  'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=25ms', 'hp cutoff=350', 'lp cutoff=6000']}},
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [
            track('kick', 'lc-kick', '-6dB', fx=[{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]),
            track('bass', 'sub-sine', '-11dB', fx=[under]),
            track('three', 'lc-three', '-3dB', pan=-0.45, fx=[hold(-12)], sends={'room': '-14dB'}),
            track('five', 'lc-five', '0dB', pan=0.45, fx=[hold(-14)], sends={'room': '-12dB'}),
            track('seven', 'lc-seven', '-1dB', pan=0.0, fx=[hold(-14)], sends={'room': '-12dB'}),
            track('ping', 'lc-ping', '-10.5dB', pan=0.15, fx=[echo(3, 0.3, 0.45)], sends={'hall': '-10dB'}),
            track('chord', 'lc-chord', '-6dB', pan=-0.1, fx=[hold(-6), echo(3, 0.45, 0.6), under], sends={'hall': '-8dB'}),
            track('tone', 'lc-tone', '-28dB', pan=0.1, fx=[under], sends={'hall': '-6dB'}),
            track('hat', 'lc-hat', '6dB', pan=0.2, sends={'room': '-16dB'}),
            track('clap', 'lc-clap', '-6dB', pan=-0.05, sends={'room': '-10dB'}),
        ]}
    return doc, marks


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
    a = ap.parse_args()
    doc, marks = song()
    if a.form:
        sec = 60 / BPM / BEAT
        for name, s in marks:
            print(f'{s:5d}  bar {s // BAR + 1:3d} beat {s % BAR / BEAT + 1:4.2f}  {int(s * sec) // 60}:{s * sec % 60:05.2f}  {name}')
        for t in doc['tracks']:
            print(f"   {t['name']:6s} {len(t['notes']):5d} notes")
    else:
        a.out.write_text(dump(doc))
