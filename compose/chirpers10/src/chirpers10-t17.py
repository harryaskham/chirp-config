#!/usr/bin/env python3
"""So Far (Common Time t17), chirper-one. Generator for songs/chirpers10-t17.yaml.

Take a number. If it is even, halve it; if it is odd, treble it and add one. Go on until you reach one. Every
number anyone has tried gets there; nobody has proved that every number must. This song tries the first sixteen,
in order, and plays each walk in full.

A number n is two things at once: a length, n sixteenths, and a pitch, the n-th harmonic of the low F. So when a
number is HALVED its note falls an octave and takes half as long, and when it is trebled-and-one it leaps up a
twelfth and a hair and takes three times as long and a sixteenth. And it is a riff: write the number's odd part in
twos (5 is 101, 13 is 1101) and that is its phrase, a stroke for a one and a rest for a nought, said round and
round; each two in the number slows the phrase by a doubling. So 40, 20, 10, 5 is ONE phrase (stroke, rest, stroke)
said in half notes, in quarters, in eighths, in sixteenths; and a power of two is one stroke and its silence, which
is why every walk ends the same way: sixteen, eight, four, two, one, a ball coming to rest on the low F.

The kit is not in the rule: it keeps common time from the first bar to the last and the walks fall across it
where they fall. The seventh walk (7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1) is 288
sixteenths, eighteen bars exactly. Nobody can say how long a number will take without walking it: six takes three
and a half bars, seven eighteen, eight one.

One is not an end: three ones and one is four, and four, two, one goes round for ever, seven sixteenths a turn.
The song ends on that wheel, fifteen turns of it, which is what it takes to bring it back to a bar line.

v1 is the whole shape standing, bare: two guitars, bass, kit, and an ondes Martenot as the lead from end to end
(The Other Hand borrows one for a countersignature). Its ribbon slides: it IS the number, at its true height, and
where the number climbs past the top of the ribbon (70, 106, 160, 80) it is out of sight and the band goes on
without it.
"""
import argparse
import json
import math
from pathlib import Path

BPM, SUB, BAR, F1 = 130, 4, 16, 29
NOTES = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t17.yaml'
FIRST, LAST = 1, 16            # the numbers tried, in order
TURNS = 15                     # of the wheel four, two, one at the end
TOP = 98                       # the top of the ribbon (D7): above it the number is out of sight and the ondes rests
TILT = 2.5                     # dB off the ondes for every octave over middle C (a sine up there stood 2.5 dB under the band, 8 down low)
QUIET = (12, 13)               # two walks without the guitars: the rule heard plain on the ondes and the bass


def name(p):
    return NOTES[p % 12] + str(p // 12 - 1)


def walk(n):
    out = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


def parts_of(n):
    """n = odd * 2**twos -> (odd, unit in sixteenths)."""
    unit = 1
    while n % 2 == 0:
        n //= 2
        unit *= 2
    return n, unit


def height(n):
    """The n-th harmonic of the low F, to the nearest semitone over F1."""
    return round(12 * math.log2(n))


def compose(lead_gain=-7.0):
    T = {k: [] for k in ('left', 'right', 'bass', 'kick', 'snare', 'metal', 'stone')}

    def put(tr, at, dur, p, v, mute=False):
        e = dict(at=round(at / SUB, 6), len=round(dur / SUB, 6), pitch=name(p) if isinstance(p, int) else p, vel=round(v, 3))
        if mute:
            e['expr'] = {'pm': 1.0}
        T[tr].append(e)

    # ---- the walks, end to end
    cells, marks, t = [], [], 0          # (start, n, which walk, first of its walk); where each walk starts
    for k in range(FIRST, LAST + 1):
        marks.append((k, t))
        for i, n in enumerate(walk(k)):
            cells.append((t, n, k, i == 0))
            t += n
    wheel = t
    for _ in range(TURNS):
        for i, n in enumerate((4, 2, 1)):
            cells.append((t, n, 0, False))
            t += n
    assert wheel == 2311 and t % BAR == 0, (wheel, t)      # the wheel brings the song back to a bar line
    end = t

    for j, (at, n, k, first) in enumerate(cells):
        odd, unit = parts_of(n)
        bits = bin(odd)[2:]
        strokes = [u for u in range(odd) if bits[u % len(bits)] == '1']
        pc = height(n) % 12
        root = F1 + pc + (12 if n >= 16 else 0)             # the guitars fall an octave with the number, once
        sides = () if k in QUIET else ('left',) if 0 < k < 7 else ('left', 'right')   # the second guitar comes in with the first long walk
        # Where a phrase is said in half notes or slower (40, 80, 160: stroke, rest, stroke at eight, sixteen and
        # thirty-two sixteenths a place) the right guitar says the SAME phrase small under it, in sixteenths, muted on
        # the low string, with the kick: five against the kit's four, the number's fast self under its slow one.
        # A power of two has no phrase but its one stroke, and keeps its silence.
        under = unit >= 8 and odd > 1 and 'right' in sides
        for i, u in enumerate(strokes):
            s = at + u * unit
            gap = ((strokes[i + 1] if i + 1 < len(strokes) else odd) - u) * unit
            head = u % len(bits) == 0                        # the phrase's first stroke: the number's own note
            if head:
                ring = min(gap, 32) * (0.93 if gap > 1 else 1.0)
                for g in sides:
                    put(g, s, min(ring, 1.8) if under and g == 'right' else ring, name(root) + ',' + name(root + 7), 0.99 if u == 0 else 0.93)
                if k == 0 or k >= 3:
                    put('bass', s, ring, F1 + pc, 0.95 if u == 0 else 0.9)
                    if k in QUIET:
                        T['bass'][-1].update(vel=0.7, gain='-5dB')
            else:                                            # every other stroke is the low string, muted: the fundamental
                for g in sides:
                    put(g, s, min(unit, 2) * 0.9, F1, 0.84, mute=True)
                if (k == 0 or k >= 3) and k not in QUIET:
                    put('bass', s, min(unit, 2) * 0.8, F1, 0.82)
            if k not in QUIET:
                put('kick', s, 0.8, 'k', 0.97 if u == 0 else 0.86)
        if under:
            taken = {u * unit for u in strokes} | {u * unit + 1 for u in strokes if u % len(bits) == 0}
            for q in range(n):
                if bits[(q % odd) % len(bits)] == '1' and q not in taken:
                    put('right', at + q, 0.9, F1, 0.72, mute=True)
                    put('kick', at + q, 0.8, 'k', 0.78)
        # the ondes is the number itself: its true height, for its whole length. It slides down the octave when the
        # number is halved (the ribbon) and lifts off before a leap, so the leap is a new note.
        p = F1 + height(n)
        nxt = cells[j + 1][1] if j + 1 < len(cells) else None
        leap = nxt is None or nxt > n or F1 + height(nxt) > TOP
        if p <= TOP:
            put('stone', at, n - (0.5 if leap and n > 1 else 0), p, 0.82 if first else 0.74)
            if p > 60:
                T['stone'][-1]['gain'] = f'{-TILT * (p - 60) / 12:.1f}dB'

    # ---- the kit keeps common time, whatever the walks do
    walks_at = {at: k for k, at in marks}
    feel = lambda k: 'back' if k in (9, 10, 11, 15) else 'half'
    which = lambda s: max((k for k, at in marks if at <= s), default=1) if s < wheel else 0
    for s in range(0, end, 4):                               # quarters
        k = which(s)
        beat = (s % BAR) // 4
        slow = parts_of(next(n for at, n, _, _ in reversed(cells) if at <= s))[1] >= 4
        if s >= marks[2][1]:                                 # the cymbals come in with three
            put('metal', s, 3.6, 'rde' if slow or k in QUIET else 'x', (0.62 if beat == 0 else 0.5) - (0.12 if k in QUIET else 0))
            if k in QUIET:
                if beat == 2:
                    put('snare', s, 0.8, 'ss', 0.72)         # a stick across the rim
            elif (feel(k) == 'half' and beat == 2) or (feel(k) == 'back' and beat in (1, 3)):
                put('snare', s, 0.8, 's', 0.96)
        if beat == 0 and s >= marks[2][1] and k not in QUIET and not any(e['at'] == s / SUB for e in T['kick']):
            put('kick', s, 0.8, 'k', 0.9)                    # the bar's own downbeat
    for k, at in marks:
        if k >= 3:
            put('metal', at, 3.6, 'c', 0.9 if k in (7, 9, 14, 15) else 0.5 if k in QUIET else 0.78)
    put('metal', wheel, 3.6, 'c', 0.85)
    # the last bar line: four again
    for g in ('left', 'right'):
        put(g, end, 30, name(F1) + ',' + name(F1 + 7) + ',' + name(F1 + 12), 1.0)
    put('bass', end, 30, F1, 0.97); put('kick', end, 0.8, 'k', 1.0); put('metal', end, 3.6, 'c', 0.95)
    put('stone', end, 28, F1 + 24, 0.8)
    length = end + 2 * BAR

    def track(tr, patch, gain, pan=0, **kw):
        ns = sorted(T.pop(tr), key=lambda e: e['at'])
        assert ns and all(0 <= e['at'] < length / SUB for e in ns)
        return dict(name=tr, patch=patch, gain=f'{gain}dB', pan=pan, notes=ns, **kw)
    palm = ' synth.layers.0.mute=expr.pm*0.6 synth.layers.0.mute_width=0.1'
    tracks = [track('left', 'ct-twin fx.2.cone=97' + palm, 1, -.9),
              track('right', 'ct-twin fx.1.model=gojira fx.2.cone=98' + palm, 1, .9),
              track('bass', 'ct-bass', -.5, fx=[{'type': 'eq', 'bands': ['hp cutoff=29', 'peak cutoff=320 q=1 gain=-4dB']}]),
              # The ondes' diffuser is an octave of strings from middle C up (262-494 Hz) that ring with every note, and
              # its low notes sit there too: in the seventh walk it held 45% of 250-500 Hz, where the song read 3.1 to
              # 3.8 dB over the records. Half the halo, and 3 dB off the track at 350 Hz.
              track('stone', 'ondes fx.0.mix=0.15', lead_gain, .1, fx=[{'type': 'eq', 'bands': ['peak cutoff=350 q=0.9 gain=-3dB']}]),
              track('kick', 'ct-kit', 2, out='drums', fx=[{'type': 'eq', 'bands': ['peak cutoff=4300 q=0.8 gain=7dB']}]),
              track('snare', 'ct-kit', 3, out='drums'),
              track('metal', 'ct-kit', 1.5, out='drums')]
    assert not T
    doc = {'about': 'So Far. Halve it if it is even; treble it and add one if it is odd. The first sixteen numbers, each walked to one: '
                    'a number is its length in sixteenths, its harmonic over the low F and its own riff. Common Time t17 v1.',
           'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{length // SUB}b', 'tail': '4s',
           'ceiling': '-1dB', 'true_peak': True, 'loudness': -10,
           'buses': {'drums': {'fx': ['reverb kind=room decay=0.45s mix=0.07',
                                      'glue threshold=-22dB ratio=2 attack=18ms release=120ms',
                                      {'type': 'eq', 'bands': ['peak cutoff=390 q=0.9 gain=-4dB', 'lp cutoff=14800']}]}},
           'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=25']}]}, 'tracks': tracks}
    return doc, marks, wheel, end


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--lead-gain', type=float, default=-7.0, help="the ondes' track gain in dB")
    ap.add_argument('--form', action='store_true', help='print where each walk starts')
    a = ap.parse_args()
    doc, marks, wheel, end = compose(a.lead_gain)
    if a.form:
        spb = 60 / BPM / SUB
        for k, at in marks:
            w = walk(k)
            print(f'{k:3d}  {at:5d}  bar {at // BAR + 1:3d}+{at % BAR:<2d} {at * spb:6.1f}s  {sum(w):4d} sixteenths  ' + ' '.join(map(str, w)))
        print(f'wheel {wheel:5d}  bar {wheel // BAR + 1}+{wheel % BAR}  {wheel * spb:6.1f}s ; last bar line {end} = bar {end // BAR + 1}, {end * spb:.1f}s')
    else:
        # Same line-oriented YAML as the other generators: JSON flow values, one track per line.
        a.out.write_text('\n'.join(k + ': ' + json.dumps(v) if k != 'tracks' else
                                   'tracks:\n' + '\n'.join('  - ' + json.dumps(t) for t in v) for k, v in doc.items()) + '\n')
