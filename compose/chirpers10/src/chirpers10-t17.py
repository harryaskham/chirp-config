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
# v2 (chirper-three; section round, 3:43.2-4:10.9, the top of the fifteenth walk and its first step down): THE SUMMIT
# HAS ITS FALL INSIDE IT. v1's note asked that 160 be the biggest thing in the song. It was ten bars on one chord and
# mostly air: the left guitar struck twice and rang for half of it. But 160 is not one number. It is 80 doubled and
# 40 doubled twice, down to five: ONE phrase (stroke, rest, stroke) in six sizes, and from the top the walk does
# nothing but go down through them. v1 played two sizes there (the number's own, two bars a place, on the left
# guitar; the smallest, in sixteenths, on the right guitar and the kick). Now the sizes between are heard too, each
# on what will have it next: TWO MORE GUITARS say eighty's phrase (a bar a place) a storey under the number, on the
# low A; the BASS says forty's (half a bar a place). At 80 the left guitar comes down to what the new pair is
# already playing; at 40 the pair stops and the whole band is on the riff the bass has had since the top. So the top
# is four guitars, every chord of the next thirty seconds already going, and the fall takes a storey off at a time.
# The hands stay in common time and go to the china for the ten bars of 160; a crash marks the top.
# Nothing is cut, repeated or moved: 18 notes are added on two new tracks, the bass's six notes become eighteen.
SUMMIT = (160, 80)             # the numbers of the fifteenth walk that carry the storeys under them
STOREY = ('ct-wall-stop-{}', -1, .5, -1, -6)  # the second pair: rig ; track gain ; pan ; octaves from the left guitar's chord ; dB at 380 Hz
SUMMIT_LOUDNESS = -9.81        # the loudness target with the storeys in: at -10 every other bar came out 0.17 to 0.18 dB quieter
# v4 (chirper-one, instrument): THE KIT. Read alone against the eleven records' drums (their drum stems, as a share
# of their mixes) and in the mix against their mixes, on the ninth walk and on the climb to 160 (raw), then on
# the finished song. What the read said of v3: the kit as a whole stood 1.3 to 1.8 dB over the records' drums, and
# the KICK alone was 44 to 50% of the whole mix's power: 77 to 88% of everything under 60 Hz, where the song read
# 1.4 to 1.7 dB over the records, with its drum on the low A (55 Hz) and so almost all under 60. The CYMBALS were
# 95% and more of 8-16 kHz, 1.2 to 1.5 over (3.2 in the climb). The kit held 6.6 dB more of 250-500 Hz than the
# records' drums do, where the song read 2.2 to 2.6 over. So:
#   the kick's drum is tuned a semitone up, to B flat (58 Hz: the fourth of the key, and it straddles 60 Hz as the
#     records' kicks do, half its weight on either side), and its fader comes down 1.5 dB
#   the cymbals get the album's shelf (2 dB off over 9 kHz); their fader stays where it was
#   the drums bus gets the album's top (2 dB off over 9 kHz, low-pass at 14.25 kHz, where this one had a low-pass
#     at 14.8 only) and a deeper, narrower cut for the box (7 dB at 340 Hz, q 1.2: the song is SHORT at 500 Hz to
#     1 kHz, so the album's wide cut at 400 Hz would have taken from the wrong place too)
# Tried and not kept: the kick's drum on C (65 Hz): the song went from 1.6 over to 2.6 UNDER below 60 Hz; and 3 dB
# off the cymbals over 9 kHz, or 1 dB off their fader: the long walks came out 0.6 to 1.3 and 0.2 to 0.8 under
# at 8-16 kHz, and the top (160) and the last walk, which were not over, lost the most.
# The kick's drum (its pitch) ; its fader ; the cymbals' fader ; their eq ; the drums bus's eq ; the loudness target.
KIT = {'kick': {'pitch': 'A#1'}, 'kick gain': 0.5, 'metal gain': 1.5, 'metal': ['highshelf cutoff=9000 gain=-2dB'],
       'bus': ['peak cutoff=340 q=1.2 gain=-7dB', 'highshelf cutoff=9000 gain=-2dB', 'lp cutoff=14250 q=0.8'], 'loudness': -9.81}
# v3 (chirper-alpha, instrument): THE BASS. See the note above the bass's track. Track gain ; the album's chain.
BASS = (0, [{'type': 'eq', 'bands': ['hp cutoff=29', 'peak cutoff=44 q=1.5 gain=-7dB', 'peak cutoff=90 q=1 gain=7.5dB',
                                       'peak cutoff=350 q=1 gain=-8dB', 'peak cutoff=1500 q=1 gain=4dB']},
             {'type': 'compressor', 'threshold': '-26dB', 'ratio': 8.0, 'attack': '12ms', 'release': '120ms', 'makeup': '2.5dB'},
             {'type': 'eq', 'bands': ['peak cutoff=170 q=1.2 gain=-3dB']}])
# (The album's bass is at 0.5 dB into that chain on a bus. Here the chain is on the track and the fader comes after
# it, so the fader is 0: benched, the bass alone then stands within 0.1 dB of the bus arrangement.)
BASS_LOUDNESS = -9.81
BASS_QUIET = -1.5              # dB on the bass's fader through the two quiet walks, where it is half the band (see the track)


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


def phrase(m):
    """Number m's phrase, once round: [(sixteenths in, sixteenths to its next stroke, whether it is a head)]."""
    odd, unit = parts_of(m)
    bits = bin(odd)[2:]
    strokes = [u for u in range(odd) if bits[u % len(bits)] == '1']
    return [(u * unit, ((strokes[i + 1] if i + 1 < len(strokes) else odd) - u) * unit, u % len(bits) == 0) for i, u in enumerate(strokes)]


def compose(lead_gain=-7.0, storeys=True, low_bus=True, kit=True):
    low_bus = low_bus and storeys  # --without-storeys still gives v1
    T = {k: [] for k in ('left', 'right', 'bass', 'kick', 'snare', 'metal', 'stone') + (('wall-left', 'wall-right') if storeys else ())}
    lifted = []

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
        storey = storeys and k == 15 and n in SUMMIT        # v2: forty's phrase is the bass's here, eighty's the second pair's
        for i, u in enumerate(strokes):
            s = at + u * unit
            gap = ((strokes[i + 1] if i + 1 < len(strokes) else odd) - u) * unit
            head = u % len(bits) == 0                        # the phrase's first stroke: the number's own note
            if head:
                ring = min(gap, 32) * (0.93 if gap > 1 else 1.0)
                for g in sides:
                    put(g, s, min(ring, 1.8) if under and g == 'right' else ring, name(root) + ',' + name(root + 7), 0.99 if u == 0 else 0.93)
                if (k == 0 or k >= 3) and not storey:
                    put('bass', s, ring, F1 + pc, 0.95 if u == 0 else 0.9)
                    if k in QUIET:
                        T['bass'][-1].update(vel=0.7, gain='-5dB')
            else:                                            # every other stroke is the low string, muted: the fundamental
                for g in sides:
                    put(g, s, min(unit, 2) * 0.9, F1, 0.84, mute=True)
                if (k == 0 or k >= 3) and k not in QUIET and not storey:
                    put('bass', s, min(unit, 2) * 0.8, F1, 0.82)
            if k not in QUIET:
                put('kick', s, 0.8, 'k', 0.97 if u == 0 else 0.86)
        if storey:
            for c in range(n // 40):
                for off, gap, head in phrase(40):            # exactly what the bass plays at 40 itself
                    put('bass', at + 40 * c + off, *((min(gap, 32) * 0.93, F1 + pc, 0.95 if off == 0 else 0.9) if head else (1.6, F1, 0.82)))
            low = root + 12 * STOREY[3]
            for c in range(n // 80):
                for off, gap, head in phrase(80):
                    for g in ('wall-left', 'wall-right'):
                        if head:
                            put(g, at + 80 * c + off, min(gap, 32) * 0.93, ','.join(name(low + i) for i in (0, 7, 12)), 0.97 if off == 0 else 0.93)
                        else:
                            put(g, at + 80 * c + off, 1.8, F1, 0.84)
                    if head:
                        lifted.append(at + 80 * c + off)
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

    for s in lifted:                                          # the foot goes with the second pair's chords
        hit = [e for e in T['kick'] if e['at'] == round(s / SUB, 6)]
        assert hit, s
        hit[0]['vel'] = max(hit[0]['vel'], 0.95)
    top = next(at for at, n, k, _ in cells if n == 160)
    # ---- the kit keeps common time, whatever the walks do
    walks_at = {at: k for k, at in marks}
    feel = lambda k: 'back' if k in (9, 10, 11, 15) else 'half'
    which = lambda s: max((k for k, at in marks if at <= s), default=1) if s < wheel else 0
    for s in range(0, end, 4):                               # quarters
        k = which(s)
        beat = (s % BAR) // 4
        slow = parts_of(next(n for at, n, _, _ in reversed(cells) if at <= s))[1] >= 4
        if s >= marks[2][1]:                                 # the cymbals come in with three
            put('metal', s, 3.6, 'x' if storeys and top <= s < top + 160 else 'rde' if slow or k in QUIET else 'x', (0.62 if beat == 0 else 0.5) - (0.12 if k in QUIET else 0))
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
    if storeys:
        put('metal', top, 3.6, 'c', 0.9)
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
    quiet = {}
    if low_bus:
        # In the two quiet walks (twelve, thirteen) the bass and the ondes are alone, and v1 plays the bass 5 dB down
        # there. The chain's compressor gives most of that back (the stretch came out 0.6 dB louder in the finished
        # file: the song's one quiet place would have lost a tenth of its drop), and a trim on the notes is undone
        # the same way (tried: 1.5 dB off each note moved the stretch 0.02 dB). So the trim is on the fader, after
        # the chain, for those two walks only.
        a, z = (dict(marks)[QUIET[0]] / SUB, dict(marks)[QUIET[-1] + 1] / SUB)
        quiet = {'auto': {'quiet': {'curve': 0, 'points': [['0b', 0], [f'{a - 0.02:g}b', 0], [f'{a:g}b', BASS_QUIET],
                                                           [f'{z - 0.02:g}b', BASS_QUIET], [f'{z:g}b', 0]]}}}
    drum = 'ct-kit-so-far' if kit else 'ct-kit'
    tracks = [track('left', 'ct-twin fx.2.cone=97' + palm, 1, -.9),
              track('right', 'ct-twin fx.1.model=gojira fx.2.cone=98' + palm, 1, .9),
              *([track('wall-' + side, STOREY[0].format(side[0]), STOREY[1], sign * STOREY[2],
                       fx=[{'type': 'eq', 'bands': [f'peak cutoff=380 q=1 gain={STOREY[4]}dB']}])   # the album's cut for this rig, deeper
                 for side, sign in (('left', -1), ('right', 1))] if storeys else []),
              # v3: THE BASS GETS THE ALBUM'S CHAIN (the `low` bus of tracks 1, 7, 8 and 14, here on the bass's own track). v1 and v2 had the bass on a bare track. Read against the album's
              # eleven records the long walks stood 1.9 to 2.3 dB over at 20-60 Hz and 1.5 to 2.0 short at 60-120, and
              # the bass sat 10.8 dB under the rest of the band (K, the ninth walk), its level moving 4.7 dB from note
              # to note. Tracks 1, 7, 8 and 14 put this same bass through one chain: its weight moved from the
              # fundamental (44 Hz, the low F) to the octave above (90 Hz), the box out at 350 Hz, 4 dB of string at
              # 1.5 kHz, and a compressor at 8:1. With it the bass stands 9.0 dB under the rest, steadier (3.3 dB), and
              # it holds more of 60-120 Hz and less of 20-60. It cannot mend 20-60 Hz alone: the kick is 78% of it.
              {**track('bass', 'ct-bass', BASS[0], fx=BASS[1], **quiet),
               'gain': {'value': f'{BASS[0]}dB', 'mod': [{'src': 'auto.quiet', 'amount': 1}]}} if low_bus else
              track('bass', 'ct-bass', -.5, fx=[{'type': 'eq', 'bands': ['hp cutoff=29', 'peak cutoff=320 q=1 gain=-4dB']}]),
              # The ondes' diffuser is an octave of strings from middle C up (262-494 Hz) that ring with every note, and
              # its low notes sit there too: in the seventh walk it held 45% of 250-500 Hz, where the song read 3.1 to
              # 3.8 dB over the records. Half the halo, and 3 dB off the track at 350 Hz.
              track('stone', 'ondes fx.0.mix=0.15', lead_gain, .1, fx=[{'type': 'eq', 'bands': ['peak cutoff=350 q=0.9 gain=-3dB']}]),
              track('kick', drum, KIT['kick gain'] if kit else 2, out='drums', fx=[{'type': 'eq', 'bands': ['peak cutoff=4300 q=0.8 gain=7dB']}]),
              track('snare', drum, 3, out='drums'),
              track('metal', drum, KIT['metal gain'] if kit else 1.5, out='drums', **({'fx': [{'type': 'eq', 'bands': KIT['metal']}]} if kit and KIT['metal'] else {}))]
    assert not T
    doc = {'about': 'So Far. Halve it if it is even; treble it and add one if it is odd. The first sixteen numbers, each walked to one: '
                    'a number is its length in sixteenths, its harmonic over the low F and its own riff. Common Time t17 v1.'
                    + (' v2: at the top of the fifteenth walk (160) two more guitars and the bass already say the phrases of 80 and 40.' if storeys else ''),
           'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{length // SUB}b', 'tail': '4s',
           'ceiling': '-1dB', 'true_peak': True, 'loudness': BASS_LOUDNESS if low_bus else SUMMIT_LOUDNESS if storeys else -10,
           'buses': {'drums': {'fx': ['reverb kind=room decay=0.45s mix=0.07',
                                      'glue threshold=-22dB ratio=2 attack=18ms release=120ms',
                                      {'type': 'eq', 'bands': KIT['bus'] if kit else ['peak cutoff=390 q=0.9 gain=-4dB', 'lp cutoff=14800']}]}},
           **({'patches': {'ct-kit-so-far': {'extends': 'ct-kit', 'kit': {'k': KIT['kick']}}}} if kit else {}),
           'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=25']}]}, 'tracks': tracks}
    if kit:
        doc['loudness'] = KIT['loudness']
    return doc, marks, wheel, end


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--lead-gain', type=float, default=-7.0, help="the ondes' track gain in dB")
    ap.add_argument('--form', action='store_true', help='print where each walk starts')
    ap.add_argument('--without-storeys', action='store_true', help='regenerate v1: 160 and 80 without the phrases of 80 and 40 under them')
    ap.add_argument('--without-kit', action='store_true', help="regenerate v3: the kit before the kick was retuned and the cymbals and the bus had the album's eq")
    ap.add_argument('--without-low-bus', action='store_true', help="regenerate v2: the bass on its bare track, before it had the album's chain")
    a = ap.parse_args()
    doc, marks, wheel, end = compose(a.lead_gain, not a.without_storeys, not a.without_low_bus, not a.without_kit and not a.without_low_bus and not a.without_storeys)
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
