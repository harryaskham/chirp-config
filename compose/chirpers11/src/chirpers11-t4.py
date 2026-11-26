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

v2 (26 Nov), five switches, each `--without-…` (all five off is v1 byte for byte):
  PLATE  a seventh thing, and the one that RINGS FALSE: a small plate (`modal`, the plate's dense inharmonic modes) on
         the second sixteenth of every beat, so that with the weight on the beat, the metal on the off-beat and the
         wood on the fourth sixteenth the cell runs in sixteenths across four materials. Stopped it is the bright
         tick this family lacked; it comes in with the air, last of the family. It is the last to be let go
         (through the section with no weight), and let go it is a wash, never a note; it is choked in two bars
         with the string and the weight.
  BOOM   the weight becomes a thing that can ring true: the felt thud as it was, and under it a kettle's head on
         the same B flat whose ring time the stroke gives. Stopped: a thud. Let go: a drum that holds its note.
  ROOM   a stopped thing is dry; a thing let go is heard in a hall, in proportion to its ring (a second copy of
         each ringing stroke sent to the hall only, 20 log10(ring) dB under ROOM_DEPTH).
  TOLL   in the last bar before each new thing is let go, the weight itself is let go for that one bar: four
         strokes that hold their note, then a thud again. Nothing is added: it is the same four strokes.
  HUSH   in the last bar before the weight is lifted, a hand is laid on everything else: one bar of the whole
         family stopped dead under the weight's toll, and on the next one they are all let go.

v3 (26 Nov), four more switches (`--without-listen`, `-off`, `-fore`, `-note`; with v2's five also off it is v1 byte for byte):
  LISTEN the others stop to listen. For the first four bars of its turn a thing is heard ALONE and let go altogether:
         the wood at bar 33, the metal at 49, the string at 65, the skin and the air together at 81, and at 113,
         after sixteen bars without it, the weight by itself, ringing B flat. Then everything comes back in, and the
         thing goes on being let go among the others. Until now a thing's turn was a slow change under six others.
         Alone it is 3 dB down, so that the others coming back is a step up.
  OFF    the hand comes off. A thing's turn no longer begins stopped and creeps: on the one of its section it is
         let go half way at once (ring 0.5: the wood goes from a 15 ms click to a 120 ms note in one bar), and the
         rest of the way over the sixteen bars. Every section now begins with something heard to change.
  FORE   a foretaste. Eight bars before its turn, each thing gives ONE stroke let go altogether (the last of its
         bar), in the middle of a section where it is otherwise stopped: one ring of a second among clicks, on a count.
  NOTE   the weight's note. In v2 the kettle under the thud rang for 1.2 s at most, so it was 17 dB gone by the
         next beat and 25 dB under its own thud. Let go, it now rings three seconds, the thud gives way (6 dB)
         and the head comes up (6 dB): each stroke lands on the last one's note, and the drum holds B flat.

Form as arithmetic: the sections are a list of lengths (LENGTHS, bars); each thing has a list of (section, ring)
points, a point `(n, r)` meaning ring r at the top of section n and `(n, r, QUICK)` ring r QUICK bars into it; its
ring at any bar is the straight line between them (`ring_at`). A ring r is a ring time `t0 * (t1 / t0) ** r` seconds
(equal steps of r are equal ratios of time), handed to the stroke as `expr.ring`.
"""
import argparse
import json
from math import log10
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

# ---- v2: the switches, and what each adds. Nothing above is changed by them.
ON = {'plate': True, 'boom': True, 'room': True, 'toll': True, 'hush': True, 'listen': True, 'off': True, 'fore': True, 'note': True}
LISTEN = 4                                   # bars at the top of its turn that a thing is heard alone, let go altogether
ALONE = -3                                   # dB on its strokes while it is alone (unhushed the wood alone read 2.4 dB OVER the groove it broke off, and the others' return was a step down)
OFF = 0.5                                    # the share of its ring a thing is given at once, on the one of its turn
FORE = SEC // 2                              # bars before its turn that a thing gives one stroke let go
NOTE = {'ring': (0.04, 3.0), 'thud': -2, 'note': 2, 'from': '-6dB', 'ease': -3.5}   # the head's ring time, seconds (v2: to 1.2: 17 dB gone by the next beat); dB a second of ring on the felt layer and on the head; the head's level stopped; dB at ring 1
PLATE = {'strokes': [(1, 'F7', .6), (5, 'F7', .5), (9, 'F7', .6), (13, 'F7', .5), (17, 'F7', .6), (21, 'F7', .5), (25, 'F7', .6)],
         'ring': (0.010, 1.5), 'enters': ENTERS['air'], 'shape': [(6, 0), (7, 1), (9, 1), (9, 0, Q)], 'ease': -8, 'gain': '-9dB', 'pan': -0.5}
BOOM = {'ring': (0.04, 1.2), 'gain': '-3dB'}
ROOM_DEPTH = -16                             # dB under its dry fader that a thing let go altogether is sent to the hall
TOLLS = [TOP[i] - 1 for i in range(2, 7)]    # the bar before each of sections 3 to 7: the weight is let go for it
HUSH = TOP[6] - 1                            # the bar before the weight is lifted: everything else is stopped for it
ROOM_FROM = 0.05                             # strokes with less ring than this are not sent at all
ROOM_THINGS = ('wood', 'metal', 'skin', 'string', 'air', 'plate')
NEW = {
    'rt-plate': {'about': 'Ring True: the plate, the thing that rings false. A small thin plate (dense inharmonic modes) struck near its edge; its ring time from the stroke (expr.ring, seconds over 0.010). Stopped, a bright tick; let go, a wash and never a note.',
                 'synth': {'layers': [{'type': 'modal', 'modes': 'plate', 'decay': ring(0.010), 'bright': 1.0, 'strike': 0.7}], 'amp': long_ring},
                 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'rt-boom': {'about': "Ring True: the weight as a thing that can ring true. The felt beater's thud on a skin (fixed), and under it a kettledrum head on the same note whose ring time comes from the stroke (expr.ring, seconds over 0.04).",
                'synth': {'layers': [{'type': 'drum', 'beater': 'felt', 'decay': 0.35, 'strike': 0.15, 'slap': 0.4, 'sharp': 60},
                                     {'type': 'modal', 'modes': 'kettle', 'decay': ring(0.04), 'bright': 0.4, 'strike': 0.2, 'level': '-3dB'}], 'amp': long_ring},
                'play': {'event_stable': True, 'vel_sens': 0.3}},
}


def things():
    """The cell's things in order, with the plate when it is on."""
    return list(STROKES) + (['plate'] if ON['plate'] else [])


def drum_patch():
    """rt-boom with the stroke's ring on the two layers' levels as well: the thud gives way to the note."""
    felt, kettle = (dict(x) for x in NEW['rt-boom']['synth']['layers'])
    felt['level'] = {'value': '0dB', 'mod': [{'src': 'expr.ring', 'amount': NOTE['thud']}]}
    kettle['level'] = {'value': NOTE['from'], 'mod': [{'src': 'expr.ring', 'amount': NOTE['note']}]}
    return {'about': "Ring True: the weight whose thud gives way to its note (v3). rt-boom's two layers, a felt thud and a kettledrum head on the same note; the stroke's ring (expr.ring, seconds) sets the head's ring time and also takes the thud down and brings the head up.",
            'synth': {'layers': [felt, kettle], 'amp': NEW['rt-boom']['synth']['amp']}, 'play': NEW['rt-boom']['play']}


def strokes_of(thing):
    return PLATE['strokes'] if thing == 'plate' else STROKES[thing]


def ring_range(thing):
    return PLATE['ring'] if thing == 'plate' else (NOTE['ring'] if ON['note'] else BOOM['ring']) if thing == 'weight' and ON['boom'] else RING[thing]


def enters(thing):
    return PLATE['enters'] if thing == 'plate' else ENTERS[thing]


def patch_of(thing):
    return 'rt-plate' if thing == 'plate' else ('rt-drum' if ON['note'] else 'rt-boom') if thing == 'weight' and ON['boom'] else PATCH[thing]


def ring_at(thing, bar):
    """The thing's ring (0..1) at a bar: the straight line between its points; flat before the first and after the last."""
    if bar >= BARS - LAST:
        return 1.0
    if thing == 'weight' and ON['toll'] and bar in TOLLS:
        return 1.0
    if thing != 'weight' and ON['hush'] and bar == HUSH:
        return 0.0
    pts = [(TOP[p[0]] + (p[2] if len(p) > 2 else 0), p[1]) for p in (PLATE['shape'] if thing == 'plate' else SHAPE[thing])]
    if ON['off'] and pts[0][1] == 0 and pts[0][0] <= bar < pts[1][0]:      # its turn: half at once, the rest across the section
        (b0, _), (b1, r1) = pts[0], pts[1]
        return r1 * (OFF + (1 - OFF) * (bar - b0) / (b1 - b0))
    if bar <= pts[0][0]:
        return pts[0][1]
    for (b0, r0), (b1, r1) in zip(pts, pts[1:]):
        if b0 <= bar < b1:
            return r0 + (r1 - r0) * (bar - b0) / (b1 - b0)
    return pts[-1][1]


def listened(bar):
    """The things whose turn began within the last LISTEN bars (they are heard alone); empty when nothing is listened to."""
    if not ON['listen']:
        return set()
    return {k for k, pts in SHAPE.items() if pts[0][1] == 0 and TOP[pts[0][0]] <= bar < TOP[pts[0][0]] + LISTEN}


def foretaste(thing):
    """The bar in which a thing gives its one let-go stroke before its turn (None for the weight: it has its tolls)."""
    if thing == 'weight':
        return None
    first = (PLATE['shape'] if thing == 'plate' else SHAPE[thing])[0]
    return TOP[first[0]] - FORE


def seconds(thing, r):
    t0, t1 = ring_range(thing)
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
    db = (PLATE['ease'] if thing == 'plate' else NOTE['ease'] if thing == 'weight' and ON['boom'] and ON['note'] and NOTE['ease'] else EASE.get(thing, 0)) * r
    if thing in CAL:
        c = [CAL[thing][-1] - v for v in CAL[thing]]
        x = min(r * 5, 4.999)
        i = int(x)
        db += c[i] + (c[i + 1] - c[i]) * (x - i)
    return round(db, 2) if thing in CAL or thing in EASE or thing == 'plate' or (thing == 'weight' and ON['boom'] and ON['note'] and NOTE['ease']) else None


def expr(thing, r):
    return {'ring': round(air_q(r) - 0.7, 4)} if thing == 'air' else {'ring': round(seconds(thing, r) - ring_range(thing)[0], 5)}


def stroke(thing, at, pitch, vel, r):
    n = {'at': at, 'len': 0.25, 'pitch': pitch, 'vel': vel, 'expr': expr(thing, r)}
    if level(thing, r) is not None:
        n['gain'] = f'{level(thing, r)}dB'
    return n


def build():
    T = {k: [] for k in things()}
    if ON['room']:
        T.update({k + '-room': [] for k in ROOM_THINGS if k in T})
    for bar in range(BARS):
        for thing in things():
            if bar < enters(thing) or any(a <= bar < b for a, b in [OUT_OF.get(thing, (0, 0))]):
                continue
            alone = listened(bar)
            if alone and thing not in alone:
                continue
            r_bar = 1.0 if alone else ring_at(thing, bar)
            mine = [x for x in strokes_of(thing) if x[0] // BAR == bar % 2]
            for s, pitch, vel in strokes_of(thing):
                if s // BAR == bar % 2:
                    r = 1.0 if ON['fore'] and bar == foretaste(thing) and s == mine[-1][0] else r_bar
                    n = stroke(thing, bar * 4 + (s % BAR) / 4, pitch, vel, r)
                    if alone and ALONE:
                        n['gain'] = f"{round(float(n.get('gain', '0dB')[:-2]) + ALONE, 2)}dB"
                    T[thing].append(n)
                    if thing + '-room' in T and r >= ROOM_FROM:      # the room hears a thing as far as it is let go
                        own = float(n.get('gain', '0dB')[:-2])
                        T[thing + '-room'].append({**n, 'gain': f'{round(own + 20 * log10(r), 2)}dB'})
    return T


def song(T, bars=BARS):
    track = lambda name, gain, pan=0, **more: {'name': name, 'patch': patch_of(name), 'gain': gain, 'pan': pan, 'notes': T[name], **more}
    hold = lambda db: f'clip drive=0dB ceiling={db}dB'          # a stroke's highest sample is its own, not the limiter's
    doc = {
        'about': "Chirpers, Escapement, track 4: Ring True, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t4.py (its docstring is the rule). " + ('Seven' if ON['plate'] else 'Six') + " struck things, each a physical model or noise, play one two-bar cell from the first bar to the last; the only thing that changes is how long each is allowed to ring. Every click is a note stopped too soon to be heard as one: the form lets them go one at a time, then shuts them again.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Ring True', 'track': 4, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{bars * 4}b', 'tail': '4s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES,
        'buses': {'room': {'fx': ['reverb kind=room decay=0.4s mix=1 predelay=6ms', 'hp cutoff=300']}},
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [track('weight', '-3dB'), track('wood', '-3dB', pan=-0.3, sends={'room': '-14dB'}), track('metal', '-5dB', pan=0.35, sends={'room': '-14dB'}),
                   track('skin', '0dB', pan=0.15, fx=[hold(-10)], sends={'room': '-14dB'}), track('string', '-3dB', pan=-0.1), track('air', '2dB', pan=0.05, fx=[hold(-9)], sends={'room': '-12dB'})],
    }
    by_name = {t['name']: t for t in doc['tracks']}
    if ON['boom'] and ON['note']:
        doc['patches'] = {**doc['patches'], 'rt-drum': drum_patch()}
    elif ON['boom']:
        doc['patches'] = {**doc['patches'], 'rt-boom': NEW['rt-boom']}
        by_name['weight']['gain'] = BOOM['gain']
    if ON['plate'] and 'plate' in T:
        doc['patches'] = {**doc['patches'], 'rt-plate': NEW['rt-plate']}
        doc['tracks'].append(track('plate', PLATE['gain'], pan=PLATE['pan'], sends={'room': '-16dB'}))
        by_name['plate'] = doc['tracks'][-1]
    if ON['room']:
        doc['buses'] = {**doc['buses'], 'hall': {'fx': ['reverb kind=hall decay=2.4s mix=1 predelay=20ms', 'hp cutoff=300', 'lp cutoff=7000']}}
        for k in ROOM_THINGS:
            if k + '-room' in T:
                dry = by_name[k]
                doc['tracks'].append({'name': k + '-room', 'patch': dry['patch'], 'gain': f"{float(dry['gain'][:-2]) + ROOM_DEPTH}dB", 'pan': dry['pan'],
                                      'notes': T[k + '-room'], 'out': 'hall', **({'fx': dry['fx']} if 'fx' in dry else {})})
    return doc


def bench():
    """Each thing alone, one stroke every two seconds at rings 0, 0.2 … 1 (60 BPM, a stroke every two beats)."""
    was = ON['room']
    ON['room'] = False                                           # the bench reads the things dry
    T = {k: [stroke(k, 2 * i, strokes_of(k)[0][1], .8, i / 5) for i in range(6)] for k in things()}
    doc = song(T, bars=3)
    ON['room'] = was
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
    for k in ON:
        ap.add_argument(f'--without-{k}', action='store_true', help=f'leave out {k} (all nine off is v1; the last four off is v2)')
    a = ap.parse_args()
    for k in ON:
        ON[k] = not getattr(a, f'without_{k}')
    if a.form:
        sec = 60 / BPM * 4
        for i, name in enumerate(NAMES):
            b, e = TOP[i], TOP[i + 1]
            print(f'{i + 1:2d}  bars {b + 1:3d}-{e:3d}  {int(b * sec) // 60}:{b * sec % 60:05.2f}  {name:38s} ' +
                  ' '.join(f'{k} {ring_at(k, b):.2f}>{ring_at(k, e - 1):.2f}' for k in list(SHAPE) + (['plate'] if ON['plate'] else []) if e > enters(k) and not any(x <= b < y for x, y in [OUT_OF.get(k, (0, 0))])))
        print(f'{BARS} bars, {BARS * sec:.1f} s; strokes: ' + ', '.join(f'{k} {len(v)}' for k, v in build().items()))
    else:
        a.out.write_text(dump(bench() if a.bench else song(build())))
