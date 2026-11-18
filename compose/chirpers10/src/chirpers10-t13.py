#!/usr/bin/env python3
"""Where It Was — Common Time, t13. A four-note tune becomes four rests.

The bar has twelve triplet eighths; the tune has eleven. Its four notes descend
Eb C Ab F. When the tune passes to a struck ring, each guitar attack it gives
away buys one group of muted notes in the negative of that tune. Then even the
ring is taken away. No tempo change; the drummer gives the ear a plain four.
"""
import argparse
import json
from collections import defaultdict
from math import lcm
from pathlib import Path

BPM, SUB, BAR, F = 96, 3, 12, 29
CELL = 11
LANDING = lcm(BAR, CELL)
HEADS = (0, 3, 7, 9)
TUNE = (10, 7, 3, 0)  # a falling answer to the album's F / Ab / C / Eb
FORM = [('chalk', 4 * BAR), ('the shape', LANDING), ('the handover', LANDING),
        ('where it was', LANDING), ('under glass', LANDING), ('lit through', LANDING),
        ('turn the sheet', LANDING), ('both sides', LANDING), ('one impression', 2 * BAR)]
PITCH = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t13.yaml'


def name(n):
    return PITCH[n % 12] + str(n // 12 - 1)


def compose(phrase_return=True):
    parts = defaultdict(list)
    def put(tr, at, dur, p, v, mute=False):
        event = dict(at=round(at / SUB, 6), len=round(dur / SUB, 6),
                     pitch=name(p) if isinstance(p, int) else p, vel=round(v, 3))
        if mute:
            event['expr'] = {'pm': 1.0}
        parts[tr].append(event)

    def drums(piece, t, v):
        track = {'k': 'kick', 's': 'snare', 'h': 'metal', 'x': 'metal',
                 'rde': 'metal', 'c': 'metal'}.get(piece, 'skins')
        put(track, t, 3.6 if piece in ('rde', 'c', 'x') else 0.8, piece, v)

    sides = ('left', 'right')
    def guitars(t, p, d, v, rigs=sides, mute=False, fifth=False):
        for rig in rigs:
            pitch = name(p) + ',' + name(p + 7) if fifth else p
            put(rig, t, d, pitch, v, mute)

    def last_exchange(start, span):
        """Twelve cells for the two sides to finish their sentences, 3:25's cadence untouched."""
        n = span // CELL
        assert n == 12

        def say(first, size):
            # Keep the contour AND its irregular spacing. Four times as broad
            # it is a line of ringing chords, not twelve more turns of the riff.
            for j, k in enumerate(HEADS):
                t = start + (first*CELL + size*k)
                gap = size * ((HEADS + (CELL,))[j+1] - k)
                p = F + TUNE[j]
                dur = min(9.5, gap * .72)
                guitars(t, p, dur, .97 if j in (0,3) else .90, fifth=True)
                put('bass', t, gap-.37, p, .93)
                drums('k', t, .97 if j in (0,3) else .88)

        def answer(first, count, stop=False):
            for i in range(count):
                for j,k in enumerate(HEADS):
                    end = (HEADS + (CELL,))[j+1]
                    for pos in range(k+1, end):
                        # At the last answer the drummer lifts his sticks and the
                        # strings leave the last beat free for the slower coda.
                        if stop and i==count-1 and pos>=CELL-SUB:
                            continue
                        t = start + (first+i)*CELL + pos
                        v = .93 if pos==k+1 else .76
                        guitars(t, F, .61, v, mute=True)
                        put('bass', t, .65, F, v-.1)
                        drums('k', t, v)

        say(0,4); answer(4,4)       # one long statement; four short negatives
        say(8,2); say(10,1)        # then in two cells, then in one
        answer(11,1,stop=True)

    start = 0
    for section, span in FORM:
        if section == 'chalk':
            # Four little statements at the bar line, a spare slot to breathe.
            for b in range(span // BAR):
                for j, k in enumerate(HEADS):
                    t = start + b * BAR + k
                    put('ring', t, 1.6, F + 36 + TUNE[j], .83 if j == 0 else .7)
                    if b >= 2:
                        put('glass', t, 1.75, F + 24 + TUNE[j], .79)
                if b >= 1:
                    drums('ft', start + b * BAR, .52 + b * .08)
        elif section == 'one impression':
            # The four-note song, its proportions intact, twice as slow. No triplet ticks.
            for j, k in enumerate(HEADS):
                t, p = start + 2*k, F + TUNE[j]
                dur = (span - 2*k - .2) if j == 3 else 2.8
                guitars(t, p, dur, .95, fifth=True)
                put('bass', t, dur, p, .93)
                put('ring', t, dur, p + 36, .86)
                drums('k', t, 1)
                if j == 3:
                    drums('c', t, .85)
        else:
            assert span % CELL == 0 and span % BAR == 0
            # Kit is on bar time, not cell time. Two distinct feels either side of the break.
            for beat in range(span // SUB):
                t, q = start + beat*SUB, beat % 4
                if phrase_return and section == 'both sides' and t >= start+span-SUB:
                    continue
                if section == 'under glass':
                    if q in (0, 2):
                        drums('ft' if q == 0 else 't2', t, .55 if q == 0 else .4)
                    continue
                if q == 2 or (section in ('the handover', 'turn the sheet', 'both sides') and q == 0 and beat > 0 and beat % 8 == 4):
                    drums('s', t, .98 if q == 2 else .73)
                cym = 'rde' if section in ('lit through','turn the sheet') else 'h'
                if beat == 0 and section not in ('where it was',):
                    drums('c', t, .76)
                elif section == 'both sides' and q == 0:
                    drums('x', t, .59)
                else:
                    drums(cym, t, .66 if q == 0 else .52)
                if section == 'turn the sheet' and beat % 2:
                    drums('h', t + 2, .43)
            if phrase_return and section == 'both sides':
                last_exchange(start, span)
                start += span
                continue
            for i in range(span // CELL):
                # Halfway through 'lit through' the same four scale tones sit over Ab; the
                # subsequent return of low F should therefore feel like a physical drop.
                pedal = F + (3 if section == 'lit through' and i >= span // CELL // 2 else 0)
                for j, k in enumerate(HEADS):
                    t, p = start + i*CELL + k, F + TUNE[j]
                    end = HEADS[j+1] if j+1 < len(HEADS) else CELL
                    hand = section == 'the handover' and j < 1 + i // 3
                    overt = section == 'the shape' or (section == 'the handover' and not hand)
                    shadow = section == 'where it was' or hand
                    if overt:
                        guitars(t, p, min(2, end-k-.25), .98 if j == 0 else .89,
                                fifth=(j == 0))
                        put('bass', t, min(2, end-k-.2), p, .92)
                        drums('k', t, .99 if j == 0 else .86)
                    if hand or section == 'lit through' or (section == 'turn the sheet' and i % 2 == 0):
                        put('ring', t, 1.45, p+36, .91 if j == 0 else .79)
                    if section == 'under glass':
                        # Rebuild the tune from its LOW end while the clean string holds dyads.
                        if j >= 3 - i//3:
                            put('bass', t, end-k-.2, p, .89)
                            put('ring', t, 1.7, p+24, .71)
                        if j == 0:
                            dyad = ('F3,C4', 'Ab3,Eb4', 'Eb3,Bb3')[i // 4]
                            put('glass', t, CELL-.8, dyad, .82)
                    if section in ('lit through','turn the sheet','both sides'):
                        # Hocket from side to side, then both shapes in the same stereo space.
                        if section == 'turn the sheet':
                            half = i % 2
                            guitars(t, p, 1.4, .94, rigs=(sides[half],), fifth=j in (0,3))
                        elif section == 'both sides' and i % 2 == 0:
                            guitars(t, p, end-k-.35, .99, fifth=True)
                        if section != 'both sides' or i % 2 == 0:
                            put('bass', t, end-k-.3, p if section != 'lit through' else pedal, .90)
                        if section == 'both sides' and i % 2 == 0:
                            drums('k', t, .98)
                        shadow = section != 'both sides' or i % 2 != 0
                    if shadow:
                        opposite = (sides[1-(i%2)],) if section == 'turn the sheet' else sides
                        for n in range(k+1, end):
                            a = start + i*CELL + n
                            guitars(a, pedal, .61, .94 if n == k+1 else .76, opposite, mute=True)
                            if section in ('where it was','the handover','both sides'):
                                put('bass', a, .65, pedal, .82 if n == k+1 else .68)
                            if section != 'turn the sheet' or n == k+1:
                                drums('k', a, .93 if n == k+1 else .73)
            if section in ('the shape','under glass','turn the sheet'):
                for off, piece in zip((3,2,1), ('t1','t2','ft')):
                    drums(piece, start + span - off, .59+(3-off)*.1)
        start += span

    def track(tr, patch, gain, pan=0, **kw):
        ns = sorted(parts.pop(tr), key=lambda n:n['at'])
        assert ns and all(n['at'] >= 0 and n['at'] < start/SUB for n in ns)
        return dict(name=tr, patch=patch, gain=f'{gain}dB', pan=pan, notes=ns, **kw)
    tracks = [track('left','ct-twin fx.2.cone=73',1,-.9),
              track('right','ct-twin fx.1.model=gojira fx.2.cone=74',1,.9),
              track('bass','ct-bass',-.5,fx=[{'type':'eq','bands':['hp cutoff=29','peak cutoff=320 q=1 gain=-4dB']}]),
              track('ring','scanned-mallet',-13,.06,sends={'chamber':'-12dB'}),
              track('glass','ct-clean',-2,-.18,sends={'chamber':'-9dB'}),
              track('kick','ct-kit',2,out='drums',fx=[{'type':'eq','bands':['peak cutoff=4300 q=0.8 gain=7dB']}]),
              track('snare','ct-kit',3,out='drums',sends={'chamber':'-14dB'}),
              track('metal','ct-kit',1.5,out='drums'), track('skins','ct-kit',3,out='drums')]
    assert not parts
    return {'about':'Where It Was. A four-note tune on eleven triplet eighths; the band learns to play its negative. Common Time t13 '+('v2.' if phrase_return else 'v1.'),
            'tempo': BPM, 'seed': 1, 'event_stable': True, 'length':f'{start//SUB}b', 'tail':'3s',
            'ceiling':'-1dB', 'true_peak':True, 'loudness':-10,
            'buses':{'drums':{'fx':['reverb kind=room decay=0.45s mix=0.07',
                                     'glue threshold=-22dB ratio=2 attack=18ms release=120ms',
                                     {'type':'eq','bands':['peak cutoff=390 q=0.9 gain=-4dB','lp cutoff=14800']}]},
                     'chamber':{'fx':['reverb kind=chamber mix=1 decay=1.1s predelay=14ms low_cut=280 high_cut=7200']}},
            'master':{'fx':[{'type':'eq','bands':['hp cutoff=25']}]}, 'tracks':tracks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUT)
    parser.add_argument('--v1', action='store_true', help='reproduce the original alternating-cell return')
    args = parser.parse_args()
    doc = compose(not args.v1)
    # Same line-oriented YAML as the other generators: JSON flow values, one track per line.
    args.out.write_text('\n'.join(k+': '+json.dumps(v) if k!='tracks' else
                        'tracks:\n'+'\n'.join('  - '+json.dumps(t) for t in v) for k,v in doc.items())+'\n')
