#!/usr/bin/env python3
"""Still Owing (Common Time t10). Two bars to spend, never a tick more.

Each half has a recognisable touch: a low open E-flat and two palm strokes
on the call; a higher chord and a four-note falling answer on the reply.
With debt d, the two halves take 16+d and 16-d sixteenths. The players really
stretch their figures; it is not just a shifted downbeat. The kit never follows
that private tempo. A dry piano marks the middle of the pair; a struck key on
a wave terrain marks where the reply actually arrives. They part, then meet.
"""
import argparse
import json
import os
from collections import defaultdict
from pathlib import Path

BPM, SUB, BAR, HOME = 112, 4, 16, 27  # E-flat 1
MAX_DEBT = 6
FORM = [('at par', [0]*3), ('in hand', [0]*5), ('on account', list(range(MAX_DEBT+1))),
        ('still owing', [MAX_DEBT]*6), ('two clocks', [6, 4, 2, 0]),
        ('called in', list(range(MAX_DEBT, -MAX_DEBT-1, -2))),
        ('across the line', [d for width in (6, 5, 4, 2) for d in (width, -width)]),
        ('square', [0]*5), ('the receipt', [0])]
NOTES = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t10.yaml'
# v2: the length of the reply picks its player in 'across the line' alone.
# Bowed lyre on the left, picked guitar on the right. As the two clocks
# converge the guitars rejoin from the end of the phrase. Empty = v1 exactly.
TRADE = os.environ.get('C10T10_TRADE', '-5')
# v3: on the repeat of each crest root, spend the six borrowed sixteenths
# on a reverse pickup made from the following answer. Empty = published v2.
ADVANCE = os.environ.get('C10T10_ADVANCE', '7.5')
# v4: after the players return to straight time, one more note of the answer
# can ring each time around. Track gain in dB; empty reproduces v3 exactly.
COURSES = os.environ.get('C10T10_COURSES', '-11')
# Offset in an ordinary bar, gate, semitones, open / palm / single note.
CALL = [(0,2.50,0,'o'), (3,.64,0,'m'), (4,.78,0,'m'), (6,2.25,7,'n'),
        (9,.62,0,'m'), (10,.78,0,'m'), (13,2.12,2,'n')]
# Four answer pitches Gb, F, C, Eb, from the album hook in a new order. The
# mutes between are pedal Eb. With six on credit this whole bar lasts ten ticks.
REPLY = [(0,3.35,15,'o'), (4,.74,0,'m'), (5,2.32,14,'n'), (8,.7,0,'m'),
         (9,.7,0,'m'), (11,1.76,9,'n'), (14,1.55,12,'n')]


def nm(p):
    return NOTES[p % 12] + str(p//12 - 1)


def chord(*p):
    return ','.join(map(nm,p))


def build():
    voices = defaultdict(list)
    sections = []
    fold_sources, fold_patches = {}, {}
    def note(track, tick, gate, pitch, vel, **expr):
        assert tick >= 0 and gate > 0 and 0 < vel <= 1
        n = {'at':round(tick/SUB,6), 'len':round(gate/SUB,6),
             'pitch':nm(pitch) if isinstance(pitch,int) else pitch, 'vel':round(vel,3)}
        if expr:
            n['expr'] = {k:round(v,5) for k,v in expr.items()}
        voices[track].append(n)

    def kit(piece, at, vel):
        tr = {'k':'kick','s':'snare','t1':'skins','t2':'skins','ft':'skins'}.get(piece,'metal')
        note(tr, at, 4 if piece in ('c','x','rde') else 1, piece, vel)

    def tally(at, p, d, length=3.0, vel=.83):
        note('tally', at, length, p, vel, owing=abs(d)/MAX_DEBT)

    def borrow(root, debt, midpoint):
        # Record this ground's first `debt` ticks of the COMPRESSED answer on
        # the introduction's clean guitar; no external samples or helper songs.
        ratio = (BAR-debt)/BAR
        name = f'owing-advance-{root}'
        src = name+'-source'
        heads = [{'at':round(pos*ratio/SUB,6), 'len':round(min(gate*ratio,debt-pos*ratio)/SUB,6),
                  'pitch':nm(root+semi+24), 'vel':.90 if pos==0 else .83}
                 for pos,gate,semi,how in REPLY if how!='m' and pos*ratio<debt]
        fold_sources[src] = {'tempo':BPM,'length':f'{debt/SUB:g}b','tail':'0s','seed':1,
                             'tracks':[{'name':'source','patch':'ct-clean synth.layers.0.inharm=0.00008 play.gate=1 play.humanize.time=0ms play.humanize.vel=0',
                                        'notes':heads}]}
        fold_patches[name] = {'play':{'gate':1},'synth':{'amp':{'a':'3ms','s':1,'r':'6ms'},
                              'layers':[{'type':'sample','song':src,'root':'C4','reverse':True}]}}
        note(name,midpoint,debt,'C4',1)

    pair = 2*BAR
    t = 0
    for s, debts in FORM:
        sections.append((s,t))
        for j,d in enumerate(debts):
            width = BAR+d
            turn = t+width
            assert width+(BAR-d)==pair and 0<width<pair
            # The sustained middle climbs Eb -> Gb -> Ab. The following pocket
            # strips this to two strokes and lets the bass settle home on Eb.
            root = HOME
            if s == 'still owing': root += (0,0,3,3,5,5)[j]
            if s == 'two clocks': root += (5,3,0,0)[j]
            if s == 'square': root += (0,-2,-4,-2,0)[j]
            if s == 'the receipt':
                # One straight low chord; the two middle markers coincide for
                # the last time, over the fifth returning to E-flat.
                for g in ('left','right'):
                    note(g,t,10,chord(HOME,HOME+7),.97)
                    note(g,turn,15.4,chord(HOME,HOME+7,HOME+12),1)
                for at,dur in ((t,10),(turn,15.4)):
                    note('bass',at,dur,HOME,.95); kit('k',at,1)
                note('rule',turn,7,HOME+36,.75); tally(turn,HOME+36,0,10,.88)
                kit('c',turn,.85); t+=pair; continue

            # What stays at home is a different sound from what moves. The
            # piano sometimes sits out, so the pair's end is not another click.
            if s in ('at par','in hand','on account','two clocks','across the line','square'):
                note('rule',t+BAR,2.2,HOME+31,.72 if s!='two clocks' else .89)
            tally(turn,root+39,d,4.2 if s=='two clocks' else 2.7)

            if s == 'two clocks':
                # A bass pedal to stand on; listen for the distance between
                # piano and tally contracting 6,4,2,0. No guitar or kit marks
                # their entrances, and they really do become one attack.
                note('bass',t,10,root,.82)
                note('clean',t,12,chord(root+24,root+31),.82)
                note('clean',turn+3,4,root+26,.75)
                if j == len(debts)-1:
                    for i,piece in enumerate(('ft','t2','t1','s')):
                        kit(piece,t+pair-4+i,.53+i*.10)
                t+=pair; continue

            # One lick becomes an open chord. On the final Eb, the upper four
            # courses of a twelve-string tuned down a semitone take frets
            # 2/0/2/2 (Eb3/Gb3/C4/F4). Pick in melody order, not string order.
            repay = {}
            dry_from = 0
            if COURSES and s == 'square':
                positions = [pos for pos,_,_,how in REPLY if how != 'm']
                octaves = (12,24,24,12)
                assert len(positions) == len(octaves)
                count = len(positions) if len(debts)==1 else j*len(positions)//(len(debts)-1)
                repay = dict(zip(positions[:count], octaves[:count]))
                dry_from = positions[count] if count < len(positions) else BAR
            advance = bool(ADVANCE) and s == 'still owing' and j%2==1
            if advance:
                borrow(root, d, t+BAR)
            trade = bool(TRADE) and s == 'across the line'
            # Each smaller swing starts on a new low chord. The answer stays
            # Gb-F-C-Eb against them all; the call comes home as the hands meet.
            call_root = root + (5,3,-2,0)[j//2] if trade else root
            # Four swings on either side of the midpoint. With each swing let
            # another note at the END of the answer belong to the whole band.
            heads = [(pos,semi) for pos,_,semi,how in REPLY if how!='m'] if trade else []
            reunited = {pos for pos,_ in heads[len(heads)-j//2:]} if trade else set()
            # Keep a quarter-note hat under the early bow. The china and snare
            # return with the reunited tail, sooner each time.
            lay_out_until = turn + min(reunited, default=BAR)*(pair-width)/BAR
            if trade and d < 0:
                # Time for a bass note to ring: Bb, Db, Ab, home to Eb under
                # successive long answers, instead of doubling their four pitches.
                note('bass',turn,pair-width-.55,root+(7,10,5,0)[j//2],.91)
                # Bow through the spaces where the guitars palm-mute. The four
                # pitches and their stretched onsets are the SAME reply; the
                # duration changes from a pick stroke to a breath of the bow.
                for i,(pos,semi) in enumerate(heads):
                    end = heads[i+1][0] if i+1 < len(heads) else BAR
                    pitch = root+semi+12
                    if i==len(heads)-1 and j==len(debts)-1:
                        pitch = chord(pitch,pitch+7)  # let the fifth lead home
                    note('bow',turn+pos*(pair-width)/BAR,(end-pos)*(pair-width)/BAR-.32,
                         pitch, (.92,.87,.82,.90)[i])
            for back, (pattern,at,w) in enumerate(((CALL,t,width),(REPLY,turn,pair-width))):
                for ix,(p0,gate,semi,how) in enumerate(pattern):
                    hit = at+p0*w/BAR
                    dur = gate*w/BAR
                    pitch = (root if back else call_root)+semi
                    mute = how=='m'
                    vel = (.76 if mute else .92) if p0 else .99
                    if s=='at par':
                        # Give the answer a face before its first displacement.
                        if not mute:
                            note('clean',hit,dur,pitch+24,vel-.09)
                        if j>=1 and not back and not p0:
                            note('bass',hit,dur,root,.83); kit('k',hit,.86)
                        if j==2 and mute: note('left',hit,dur,pitch,.70,pm=1)
                        continue
                    # Low Eb call, high Gb answer. In the first crest the right
                    # hand lets its reply ring instead of adding more mutes.
                    for side in ('left','right'):
                        if repay and back and side == 'right' and p0 < dry_from:
                            continue  # no right-hand chugs between the notes given to the open courses
                        if advance and side=='right' and not back and hit>=t+BAR:
                            continue  # the left guitar keeps the tail of the call; the right makes room
                        if trade and back and p0 not in reunited:
                            if mute and (side=='right' or (d<0 and hit<lay_out_until)): continue
                            if not mute and (d<0 or side=='left'): continue
                        if s=='called in' and j<3 and side=='right' and not back: continue
                        if s=='still owing' and side=='right' and back and mute: continue
                        voiced = chord(pitch,pitch+7) if how=='o' else pitch
                        if s=='square' and back and not mute and side=='right':
                            voiced=chord(pitch,pitch+7)
                        note(side,hit,dur,voiced,vel,**({'pm':1} if mute else {}))
                    # Bass keeps the hook's accents clear, not a second fast solo.
                    long_answer = trade and back and d<0
                    if not mute and not long_answer:
                        bp = pitch-12 if back and semi>=12 else pitch
                        note('bass',hit,dur,bp,vel-.05)
                    elif not back and s not in ('called in','square'):
                        note('bass',hit,dur*.84,call_root,.78)
                    if (not back and (not mute or ix in (1,2))) or (back and (p0==0 or (s in ('still owing','across the line') and not mute))):
                        if not long_answer or p0 in (0,REPLY[-1][0]):
                            kit('k',hit,vel)
                    if s in ('still owing','across the line') and how=='o' and not (trade and back and j<6):
                        note('weight',hit,dur,chord(pitch,pitch+7),.93)
                    if s=='square' and back and not mute:
                        if p0 in repay:
                            # Lift together before the next low call. The last
                            # reply outlasts the receipt's first low chord by a
                            # beat. For that beat the chord can ring on its own;
                            # leave two ticks of breath before the last Eb.
                            damp = t + pair + (BAR-2 if j == len(debts)-1 else 0)
                            note('courses',hit,damp-hit-.12,pitch+repay[p0],.90 if p0==0 else .84)
                        else:
                            note('clean',hit,dur,pitch+24,.90)
            # No borrowing in this part: the drummer's quarters and backbeat
            # can be followed across both displaced halves of the guitar riff.
            for i in range(pair//SUB):
                q = t+i*SUB
                if s=='at par' and j<2: continue
                if s in ('called in','at par') and i%2: continue
                if trade and d<0 and turn<=q<lay_out_until:
                    kit('h',q,.56 if i%4==0 else .44)
                    continue
                kit('x' if s=='across the line' else 'rde' if s=='still owing' else 'h',q,.57 if i%4==0 else .47)
                snare_beats = (1,3) if s in ('still owing','across the line') else (2,)
                if i%4 in snare_beats:
                    kit('s',q,.96 if i%4!=1 else .83)
            if j==0 and s not in ('at par','called in'): kit('c',t,.83)
            if s in ('on account','across the line') and j==len(debts)-1:
                for off,pc in ((4,'t1'),(2,'t2'),(1,'ft')): kit(pc,t+pair-off,.76)
            t+=pair

    def track(tr,patch,db,pan=0,**more):
        ns=sorted(voices.pop(tr),key=lambda e:e['at']); assert ns
        assert all(0<=n['at']<t/SUB and n['at']+n['len']<=t/SUB+.00001 for n in ns)
        return {'name':tr,'patch':patch,'gain':f'{db}dB','pan':pan,'notes':ns,**more}
    palm=' synth.layers.0.mute=expr.pm*0.6 synth.layers.0.mute_width=0.1'
    tracks=[track('left','ct-twin fx.2.cone=81'+palm,1,-.93),
            track('right','ct-twin fx.1.model=gojira fx.2.cone=84'+palm,1,.93),
            track('weight','ct-wall-stop-l',-5,.05,fx=['hp cutoff=130']),
            track('clean','ct-clean synth.layers.0.inharm=0.00008',-2,-.26,sends={'spring':'-15dB'}),
            track('bass','ct-bass',-.8,fx=[{'type':'eq','bands':['hp cutoff=27','peak cutoff=330 q=1 gain=-4dB']}]),
            track('rule','piano-additive',-9,-.35), track('tally','owing-key',-9,.38,sends={'spring':'-15dB'}),
            track('kick','ct-kit',2,out='drums',fx=['peak cutoff=4100 q=0.85 gain=6dB']),
            track('snare','ct-kit',3,out='drums'), track('metal','ct-kit',2,out='drums'),track('skins','ct-kit',2,out='drums')]
    if TRADE:
        tracks.append(track('bow','tagelharpa-bass-bowed synth.amp.r=80ms fx.0.mix=0.035',
                            float(TRADE),-.66,fx=['hp cutoff=120']))
    for name in fold_patches:
        tracks.append(track(name,name,float(ADVANCE),.66))
    if COURSES:
        # The written gates only lift the dampers. Lengthen the strings' own
        # decays too, or the first courses are already dead when the last rings.
        acoustic = ("twelve-string play.tuning='Eb2 Ab2 Db3 Gb3 Bb3 Eb4' play.gate=1 "
                    "synth.layers.0.decay.value=12s synth.layers.1.decay.value=9s "
                    "synth.amp.r=90ms fx.3.mix=0.05")
        tracks.append(track('courses',acoustic,float(COURSES),.42,fx=['hp cutoff=130']))
    assert not voices
    key_patch={'about':'Still Owing: the reply marker. Its orbit opens in proportion to the sixteenths borrowed in this pair.',
      'synth':{'amp':{'a':'2ms','d':'450ms','s':.2,'r':'95ms'},'layers':[{'type':'terrain','terrain':{
          'surface':'sines','k':1.7,'cx':.13,'cy':-.18,'rx':{'value':.16,'mod':[{'src':'expr.owing','amount':.46}]},
          'ry':{'value':.12,'mod':[{'src':'expr.owing','amount':.34}]}}}]},'fx':['hp cutoff=185']}
    return {'about':'Still Owing, Common Time track 10: a low call borrows time from a higher answer and pays it back within each two-bar phrase.',
        'tempo':BPM,'seed':1,'event_stable':True,'length':f'{t//SUB}b','tail':'3s','loudness':-10,'ceiling':'-1dB','true_peak':True,
        **({'songs':fold_sources} if fold_sources else {}),
        'patches':{'owing-key':key_patch,**fold_patches}, 'buses':{'spring':{'fx':['reverb kind=spring drip=0.65 mix=1 decay=1.2s low_cut=350 predelay=18ms']},
        'drums':{'fx':['reverb kind=room decay=0.48s mix=0.08','glue threshold=-23dB ratio=2.2 attack=18ms release=130ms',
                     {'type':'eq','bands':['peak cutoff=390 q=0.9 gain=-4dB','lp cutoff=14900']}]}},
        'master':{'fx':['hp cutoff=25']},'tracks':tracks}, sections


def dump(song):
    return '\n'.join('tracks:\n'+'\n'.join('  - '+json.dumps(x) for x in v) if k=='tracks' else k+': '+json.dumps(v) for k,v in song.items())+'\n'


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=OUT); parser.add_argument('--form',action='store_true')
    args=parser.parse_args(); song, marks=build()
    if args.form:
        for n,t in marks: print(f'{n:18} {t/BAR+1:5.0f}  {t/SUB*60/BPM:6.2f}s')
    else: args.out.write_text(dump(song))
