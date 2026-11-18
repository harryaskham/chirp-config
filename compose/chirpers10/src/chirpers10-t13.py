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


def compose(phrase_return=True, recover=True, wood=True, wood_gain=-12, held_back=True, afterimage=True, drum_memory=True, edges=True,
            rim=True, rim_gain=-18):
    # Previous versions remain reproducible, including their track lists.
    recover = recover and phrase_return
    wood = wood and recover
    held_back = held_back and wood
    afterimage = afterimage and held_back
    drum_memory = drum_memory and afterimage
    edges = edges and drum_memory
    rim = rim and edges
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

    def old_fourth_beat(start):
        """The intro put F on beat four. It echoes there while the tune walks off.
        Keep the opening THREE heavy cells: these are 'The tune' on wiw-negative.
        Its clip ends precisely when the right player changes from E-flat to F.
        """
        foot = HEADS[-1]
        furthest = len(HEADS)
        first = furthest-2
        echo_at = start + first*BAR + foot
        meet_at = start + 2*furthest*CELL + foot
        parts['right'] = [e for e in parts['right'] if not echo_at <= round(e['at']*SUB) < meet_at]
        for i in range(first, 2*furthest):
            # The first three F's keep bar time (12 ticks); the next three
            # close the gap in ten ticks each. Leave the low unison F at meet_at.
            late = (furthest-abs(furthest-i))*(BAR-CELL)
            offset = i*CELL+foot+late
            # Ring across the next E-flat and C, but lift for its A-flat.
            gate = (i+1)*CELL+HEADS[-2]-offset-.4
            guitars(start+offset,F+12,gate,.91,rigs=('right',),fifth=True)

    def recovery(start, span):
        """The glass chord occupies only the missing head. The bass finds a new note
        at the end of one cell, then plays it in its proper place in the next."""
        repeats, remainder = divmod(span, CELL*len(HEADS))
        assert repeats >= 2 and remainder == 0
        for i in range(repeats*len(HEADS)):
            group, take = divmod(i, repeats)
            first = len(HEADS)-1-group
            a = start + i*CELL
            if HEADS[first]:
                dyad = ('F3,C4', 'Ab3,Eb4', 'Eb3,Bb3')[group]
                # v9: a held glass tone, not a pluck: it stands exactly as long
                # as the tune's head is still missing, and lifts for the bass.
                put('rim' if rim else 'glass', a, HEADS[first]-.65, dyad, .82)
            pickup = take==repeats-1 and first>0
            for j in range(first, len(HEADS)):
                k = HEADS[j]; end = (HEADS+(CELL,))[j+1]
                # Shorten F by one triplet tick to make a breath for the pickup.
                if pickup and j==len(HEADS)-1: end -= 1
                put('bass',a+k,end-k-.20,F+TUNE[j], .93 if j==first else .84)
                # First time, the bassist says it alone. The ring remembers the
                # old tail on the second turn and catches the newest note last.
                if take and (j>first or take==repeats-1):
                    put('ring',a+k,min(1.7,end-k-.25),F+TUNE[j]+24,.71)
            if pickup:
                put('bass',a+CELL-1,.78,F+TUNE[first-1],.86)
        for beat in range(span//SUB):
            i,k = divmod(beat*SUB,CELL); group,take = divmod(i,repeats)
            first = len(HEADS)-1-group
            if take==0 and k>=HEADS[first]: continue  # no tom over the discovery
            q=beat%4
            if q in (0,2): drums('ft' if q==0 else 't2',start+beat*SUB,.55 if q==0 else .4)
        for off,piece in zip((3,2,1),('t1','t2','ft')):
            drums(piece,start+span-off,.59+(3-off)*.1)

    def box_stroke(cell, cells, head, slot, end):
        """The box borrows the negative; it never doubles the borrowed chug.
        Let the last pair of cells return to two guitars before the cadence card.
        """
        first = slot == head+1
        multi = end-head > 2
        if 2 <= cell < 4:
            take = multi and slot == end-1  # hear just the two rim answers
        elif 4 <= cell < cells-4:
            take = True
        elif cells-4 <= cell < cells-2:
            take = not first   # give the starts of the groups back first
        else:
            take = False
        if not take: return None
        # 2 + 3 + 1 + 1: centre/slap, centre/ghost/slap, centre, slap.
        if slot==end-1 and (multi or end==CELL): return 'cs'
        return 'cb' if first else 'cg'

    def hands_remember(start, span, section):
        """One sticking for the four missing notes. Remove backbeats wherever
        it speaks; the descent is in the touch, not four tuned drums."""
        def rest(tracks, a, b):
            for tr in tracks:
                parts[tr] = [e for e in parts[tr] if not a <= round(e['at']*SUB) < b]
        def stroke(at, j):
            if j==len(HEADS)-1:             # a left-hand grace into the last F
                put('snare',at-.15,.12,'g',.77)
            piece,vel = (('s',.89),('s',.61),('ss',.91),('s',.85))[j]
            put('snare',at,.8,piece,vel)
        cells = span//CELL
        if section=='the handover':
            # In the middle cell of each group the drum learns just the new
            # mallet attack. The last cell is left intact before the review clip.
            repeats = cells//len(HEADS)
            for j,k in enumerate(HEADS):
                a = start+(j*repeats+repeats//2)*CELL
                rest(('snare',),a,a+CELL)
                stroke(a+k,j)
        elif section=='where it was':
            # State the four on the holes of the low riff, then hear them with
            # no strings or kick for one cell. The quarter hat never disappears.
            # Both cells are well after the 65–71.875 s comparison.
            for i in (cells-4,cells-3):
                a=start+i*CELL
                rest(('snare',),a,a+CELL)
                if i==cells-3: rest(('left','right','bass','kick'),a,a+CELL)
                for j,k in enumerate(HEADS): stroke(a+k,j)
        elif section=='both sides':
            # The last negative has a beat of silence: don't fill it. Carry
            # the unplayed fourth stroke to the actual low F of the slow coda.
            a = start+span-CELL
            rest(('snare',),a,a+CELL)
            for j,k in enumerate(HEADS[:-1]): stroke(a+k,j)
        elif section=='one impression':
            stroke(start+2*HEADS[-1],len(HEADS)-1)

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
        elif section == 'under glass' and recover:
            recovery(start, span)
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
                if drum_memory: hands_remember(start, span, section)
                start += span
                continue
            half = span // CELL // 2
            for i in range(span // CELL):
                # Halfway through 'lit through' the same four scale tones sit over Ab; the
                # subsequent return of low F should therefore feel like a physical drop.
                on_ab = section == 'lit through' and i >= half
                pedal = F + (3 if on_ab else 0)
                # The seven chugs needn't be duplicated by the entire band.
                # Bass keeps the little strokes on the way out; kick keeps them
                # on the way back. The two guitars frame opposite ends of each gap.
                lead_in = edges and section=='the handover' and 0<i<span//CELL-1
                follow = edges and section=='lit through' and i>0 and not on_ab
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
                    if afterimage and on_ab:
                        # On Ab the holes coalesce into four strokes of lengths
                        # 2, 3, 1, 1. Keep the mallet's four actual places empty
                        # on both strings: the right strings first echo its pitch,
                        # then anticipate the NEXT pitch in the same gap.
                        turn = i-half
                        lead = turn >= half//2
                        borrowed = F + 12 + TUNE[(j + int(lead)) % len(HEADS)]
                        length = end-k-1
                        guitars(t+1, borrowed, length-.23, .95, ('right',))
                        # Give the first two answers the old clipped pulse. Then
                        # the low guitar and foot strike each group only once.
                        for n in range(length if turn<2 else 1):
                            dur = .61 if turn<2 else length-.30
                            guitars(t+1+n, pedal, dur, .94 if not n else .76,
                                    ('left',), mute=turn<2 or length==1)
                            drums('k',t+1+n,.93 if not n else .73)
                        continue
                    if shadow:
                        opposite = (sides[1-(i%2)],) if section == 'turn the sheet' else sides
                        for n in range(k+1, end):
                            a = start + i*CELL + n
                            reinforce = (not lead_in or n==end-1) and (not follow or n==k+1)
                            piece = box_stroke(i,span//CELL,k,n,end) if wood and section=='turn the sheet' else None
                            if piece:
                                put('box-'+opposite[0], a, .65, piece, .90 if piece=='cs' else .80)
                            elif reinforce:
                                guitars(a, pedal, .61, .94 if n == k+1 else .76, opposite, mute=True)
                            if section in ('where it was','the handover','both sides'):
                                put('bass', a, .65, pedal, .82 if n == k+1 else .68)
                            if (not lead_in or reinforce) and (section != 'turn the sheet' or n == k+1):
                                drums('k', a, .93 if n == k+1 else .73)
            if held_back and section=='the shape':
                old_fourth_beat(start)
            if section in ('the shape','under glass','turn the sheet'):
                for off, piece in zip((3,2,1), ('t1','t2','ft')):
                    drums(piece, start + span - off, .59+(3-off)*.1)
        if drum_memory and section in ('the handover','where it was','one impression'):
            hands_remember(start, span, section)
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
              # The short wooden click and the flam grace were 21–26 dB
              # under the accent on the stock kit. Bring up those two pieces
              # only; the old backbeat and its fader stay where they were.
              track('snare','ct-kit'+(' kit.ss.gain=7dB kit.g.gain=-5dB' if drum_memory else ''),3,
                    out='drums',sends={'chamber':'-14dB'}),
              track('metal','ct-kit',1.5,out='drums'), track('skins','ct-kit',3,out='drums')]
    if rim:
        # The library's FM glass pad, made to speak and stop like a rubbed rim:
        # 160 ms in, 220 ms out, its own long hall nearly shut (the song's
        # chamber carries it, as it carried the guitar it replaces). Benched
        # at -9 dB the tone WAS the bridge (+2.8 dB on the section); at -18 it
        # holds just under where the pluck's attack stood and the section
        # is within 0.2 dB of v8.
        tracks.append(track('rim','pad-glass synth.amp.a=160ms synth.amp.r=220ms synth.env.glint.a=300ms '
                            'synth.env.glint.r=220ms fx.1.mix=0.05',rim_gain,-.18,sends={'chamber':'-9dB'}))
    if wood:
        for side,pan in zip(sides,(-.58,.58)):
            tracks.append(track('box-'+side,'cajon kit.cb.pitch=F2 kit.cs.gain=4dB kit.cg.gain=1dB fx.0.mix=0.06',wood_gain,pan))
    assert not parts
    return {'about':'Where It Was. A four-note tune on eleven triplet eighths; the band learns to play its negative. Common Time t13 '+('v9.' if rim else 'v8.' if edges else 'v7.' if drum_memory else 'v6.' if afterimage else 'v5.' if held_back else 'v4.' if wood else 'v3.' if recover else 'v2.' if phrase_return else 'v1.'),
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
    previous = parser.add_mutually_exclusive_group()
    previous.add_argument('--v1', action='store_true', help='reproduce the original alternating-cell return')
    previous.add_argument('--v2', action='store_true', help='restore the sustained glass and doubled bass in the clean middle')
    previous.add_argument('--v3', action='store_true', help='restore both guitar parts in the side-to-side trade')
    previous.add_argument('--v4', action='store_true', help='keep the two guitars in unison through the first heavy section')
    previous.add_argument('--v5', action='store_true', help='restore the seven muted strokes over the A-flat pedal')
    previous.add_argument('--v6', action='store_true', help='restore the original backbeat in the negative and its returns')
    previous.add_argument('--v7', action='store_true', help='restore the doubled chugs on both sides of the break')
    previous.add_argument('--v8', action='store_true', help='restore the plucked clean dyads in the quiet middle')
    parser.add_argument('--wood-gain', type=float, default=-12, help='cajon track gain in dB')
    parser.add_argument('--rim-gain', type=float, default=-18, help='held glass track gain in dB')
    args = parser.parse_args()
    doc = compose(not args.v1, not args.v2, not args.v3, args.wood_gain, not args.v4, not args.v5, not args.v6, not args.v7,
                  not args.v8, args.rim_gain)
    # Same line-oriented YAML as the other generators: JSON flow values, one track per line.
    args.out.write_text('\n'.join(k+': '+json.dumps(v) if k!='tracks' else
                        'tracks:\n'+'\n'.join('  - '+json.dumps(t) for t in v) for k,v in doc.items())+'\n')
