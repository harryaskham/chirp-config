#!/usr/bin/env python3
"""The Other Hand: two guitarists read the same strip from opposite ends.
The strip holds 19 sixteenths; a drummer outside it counts quarters in four.
An attack is reflected about tick 9, including its pitch and articulation;
this is a backwards performance, not backwards audio. --map prints real times.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

BPM, GRID, STRIP = 104, 4, 19
# section lengths are strips, not bars
FORM = [('pencil', 4), ('ink', 12), ('opposite', 16), ('carbon', 8),
        ('thumbprint', 10), ('raised', 12), ('turn over', 12), ('one hand', 8), ('signed', 3)]
# position, semitones above F1, type. Four open notes, five dry consonants.
ROW = [(0,0,'o'), (2,0,'m'), (3,3,'o'), (6,0,'m'), (7,0,'m'),
       (10,1,'o'), (13,0,'m'), (15,7,'o'), (17,0,'m')]
PITCH = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t12.yaml'

def pitch(m): return PITCH[m % 12] + str(m // 12 - 1)
def strip(back=False):
    return sorted(((STRIP-1-t if back else t), p, k) for t,p,k in ROW)

def build(drum_hand=True, crease=True):
    crease = crease and drum_hand  # --without-drum-hand still reproduces v2
    ev = defaultdict(list); sections = []; start = 0
    def put(tr, t, n, dur, v, mute=False):
        e = {'at':round(t/GRID, 5), 'len':round(dur/GRID, 5), 'pitch':pitch(n) if isinstance(n,int) else n, 'vel':v}
        if mute: e['expr']={'pm':1}
        ev[tr].append(e)
    def kit(tr,t,p,v): put(tr,t,p,3.8 if p in ('c','x','rde') else 1.15,v)
    def chord(root): return pitch(root)+','+pitch(root+7)
    front,back = strip(),strip(True)
    opens = [{t:p for t,p,k in r if k=='o'} for r in (front,back)]
    assert opens[0].keys() & opens[1].keys() == {3,15}
    taps = (2,7,13,17)
    assert set(taps) <= {t for t,_,k in front if k=='m'}
    for sec,count in FORM:
        sections.append((sec,start,count))
        for i in range(count):
            a = start + i*STRIP
            # F all through the introduction and first traversal. The quiet centre
            # moves to its minor third; the high answer alone bends on the way home.
            root = 29 + (3 if sec in ('carbon','thumbprint') else 1 if sec=='raised' and i<count//2 else 0)
            # v4: fold the last three G-flat strips about their shared, silent
            # centre. The two open meetings at 3 and 15 are the first fold's
            # edges. The second keeps half that span; the last keeps just the
            # centre. The independent quarter-note count stays outside the fold.
            centre = STRIP // 2
            step = i - (count//2 - 3)
            folding = crease and sec=='raised' and 0 <= step < 3
            radius = (centre - min(opens[0].keys() & opens[1].keys())) * (2-step)//2 if folding else centre
            def inside(t): return abs(t-centre) <= radius
            if folding:
                assert centre not in {t for t,_,_ in front+back}
                put('wire',a+centre,29+36,(2,5,STRIP-centre-.25)[step],.88)
            # In 'carbon' the mouth hands its line to the drummer from the tail
            # backwards: one note, two, then all four. In 'one hand' the drummer
            # answers two full strips, at the guitarists' timing this time.
            tom_reply = drum_hand and sec=='one hand' and i in (count-3,count-1)
            if sec=='signed':
                # No counting-out: the last two chord changes are read right to left.
                if i==0: cadence=[(0,7,5),(8,1,7)]
                elif i==1: cadence=[(0,3,11)]
                else: cadence=[(0,0,STRIP-1)]
                for t,p,dur in cadence:
                    for tr in ('left','right'): put(tr,a+t,chord(root+p),dur,.95)
                    put('bass',a+t,root+p,dur,.92); kit('foot',a+t,'k',.95)
                    if i==2: kit('brass',a+t,'c',.84); put('mouth',a+t,root+24,dur,.78)
                continue
            if sec=='pencil' or sec=='thumbprint':
                # A wordless VOSIM voice has time to open its vowel: the two hands
                # are a sung call and an unhurried clean answer, never two walls.
                if sec=='pencil':
                    for t,p in opens[0].items(): put('mouth',a+t,root+24+p,2.4,.78)
                    if i>=2:
                        for t,p in opens[1].items(): put('wire',a+t,root+12+p,2.4,.82)
                else:
                    for t,p in opens[i%2].items():
                        put('mouth',a+t,root+24+p+(12 if i in (6,7) else 0),2.1,.84)
                    for t,p in opens[1-i%2].items(): put('wire',a+t,root+12+p,2.6,.86)
                    if i>=count//2:
                        for t in (3,15): kit('skins',a+t,'ft' if t==3 else 't1',.71)
                continue
            rightback = sec in ('opposite','carbon','raised') or (sec=='turn over' and i%2==0)
            leftback = sec=='turn over' and i%2==1 or sec=='one hand'
            for tr,rev in [('left',leftback),('right',rightback or sec=='one hand')]:
                # Carbon is one guitarist with a delayed memory, not a stereo solo.
                if sec=='carbon' and tr=='right': continue
                if sec=='ink' and i<4 and tr=='right': continue
                if sec=='turn over' and rev:
                    # The hand reading back picks up a volume steel. First hold just
                    # the two meeting notes (C, Ab); then fill in the reflected tune.
                    # The other hand still chugs. Swap chairs on every new strip.
                    stops = [t for t in sorted(opens[1]) if i>=4 or t in (3,15)]
                    end = 10 if i==count-1 else STRIP
                    stops = [t for t in stops if t<end]
                    for j,t in enumerate(stops):
                        until = stops[j+1] if j+1<len(stops) else end
                        put('steel-'+tr,a+t,root+24+opens[1][t],until-t-.12,.87)
                    continue
                r = back if rev else front
                for j,(t,p,k) in enumerate(r):
                    if not inside(t): continue
                    if tom_reply and not (i==count-1 and t==STRIP-1): continue
                    if sec=='one hand' and k=='m' and (i>=4 or t%2): continue
                    if sec=='carbon' and k=='m' and i%2: continue
                    if sec=='turn over' and i==count-1 and t>=10: continue
                    gap = (r[j+1][0] if j+1<len(r) else STRIP)-t
                    dur = .64 if k=='m' else min(gap-.23, 3.45)
                    n = root+p
                    put(tr,a+t,chord(n) if k=='o' and sec in ('raised','turn over','one hand') else n,dur,.94 if k=='o' else .79,k=='m')
            if sec=='carbon':
                n_take = min(4, 2**(i//2)) if drum_hand and i%2 else 0
                for j,(t,p) in enumerate(sorted(opens[1].items())):
                    if j < len(opens[1])-n_take:
                        put('mouth',a+t,root+24+p,2.15,.84)
                    else:
                        # Lead the missing word on a vacated palm stroke, never
                        # double it. The four head pitches are the same tune.
                        put('drum-hand',a+taps[j],'head'+str(root+12+p),2.3,.86)
                for t in (3,15): put('bass',a+t,root,3,.87); kit('foot',a+t,'k',.87)
            else:
                # In the opposing voices the bass recognises only the two common
                # open attacks; the contrasting pitches form Ab/C then C/Ab.
                apart = sec in ('opposite','turn over','raised')
                rb = opens[1 if leftback else 0]
                for t,p in rb.items():
                    if not inside(t): continue
                    if sec=='turn over' and i==count-1 and t>=10: continue
                    if tom_reply:
                        put('drum-hand',a+t,'head'+str(root+12+p),2.3,.92)
                        # One low pedal on the first beat of the answer; leave
                        # the rest to the drum pitches, not the bass doubling them.
                        if t==min(rb):
                            put('bass',a+t,root,3,.92); kit('foot',a+t,'k',.95)
                    else:
                        if not apart or t in (3,15):
                            put('bass',a+t,root+(0 if apart else p),3 if apart else 1.7,.92)
                        kit('foot',a+t,'k',.98 if t in (0,3,15,18) else .83)
                if sec=='raised':
                    for t in (3,15):
                        if inside(t): put('mouth',a+t,root+24+opens[1][t],2.65,.85)
                    if folding and step>0:
                        # Even when the guitars no longer meet here, the foot
                        # remembers ONE of their two meetings. Hold that last
                        # low G-flat up to the clean F, not across its attack.
                        anchor = min(opens[0].keys() & opens[1].keys())
                        put('bass',a+anchor,root,centre-anchor-.4,.92)
                        kit('foot',a+anchor,'k',.98)
                    if crease and i==count//2:
                        # The high F has told us the key already. Meet the
                        # returning left guitar three octaves down, then go
                        # back to the bass's two meetings a strip; no crash.
                        put('bass',a,root,2.7,.95)
                if sec=='opposite' and i in (3,7,11,15): kit('skins',a+17,'ft',.84)
            # The drummer counts through the strip seams, not from strip zero.
            for t in range(a, a+STRIP):
                if sec=='turn over' and i==count-1 and t>=a+10: break
                if t%GRID: continue
                beat=t//GRID
                if sec=='carbon':
                    if beat%4==2: kit('snare',t,'s',.76)
                else:
                    if beat%4==(2 if sec in ('ink','one hand') else 1) or (sec not in ('ink','one hand') and beat%4==3): kit('snare',t,'s',.94)
                    if sec in ('raised','turn over'): kit('brass',t,'x' if sec=='turn over' else 'rde',.72 if beat%4==0 else .60)
                    elif not tom_reply or t-a not in opens[1]: kit('hat',t,'h',.65 if beat%4==0 else .48)
            if sec in ('ink','opposite','raised','one hand') and i==0: kit('brass',a,'c',.88)
        start+=count*STRIP
    assert all(0<=e['at']<start/GRID and e['at']+e['len'] <= start/GRID for tr in ev.values() for e in tr)
    def track(name,patch,gain,pan=0,out=None,fx=None):
        d=dict(name=name,patch=patch,gain=gain,pan=pan,notes=sorted(ev[name],key=lambda e:e['at']))
        if out: d['out']=out
        if fx: d['fx']=fx
        return d
    # One physical hand-width mute per guitar. The chamber belongs to the two
    # exposed sounds only, so the rests between the chugs stay dry.
    palm=' synth.layers.0.mute=expr.pm*0.56 synth.layers.0.mute_width=0.10'
    room=['reverb kind=chamber mix=0.12 decay=0.85s predelay=12ms']
    tracks=[track('left','ct-twin fx.2.cone=37'+palm,'0.5dB',-.92,'strings'),
            track('right','ct-twin fx.2.cone=41'+palm,'0.5dB',.92,'strings'),
            track('mouth','vosim-voice synth.amp.a=11ms synth.amp.r=78ms','-14dB',-.12,fx=room),
            track('wire','ct-clean','-4dB',.21,fx=room),track('bass','ct-bass','0dB',0,'low'),
            track('foot','ct-kit','2dB',0,'drums',[{'type':'eq','bands':['peak cutoff=4400 q=0.84 gain=6dB']}]),
            track('snare','ct-kit','2dB',0,'drums'),track('hat','ct-kit','11dB',-.18,'drums'),
            track('brass','ct-kit','-4.5dB',.15,'drums'),track('skins','ct-kit','1.5dB',0,'drums')]
    if crease:
        # Bring the quiet middle's clean guitar up on the fader for the first
        # two strokes under the distorted pair, then return to its original
        # level for the exposed one. No gain change in either of its old parts.
        _, onset, strips = next(s for s in sections if s[0]=='raised')
        first = onset + (strips//2-3)*STRIP
        wire = next(t for t in tracks if t['name']=='wire')
        wire['gain']={'value':wire['gain'],'mod':[{'src':'auto.crease','amount':1}]}
        points=[['0b',0],[f'{first/GRID:g}b',0]]
        for j,boost in enumerate((6,4,0)):
            middle=(first+j*STRIP+STRIP//2)/GRID
            points.extend([[f'{middle-.5:g}b',boost],[f'{middle+.5:g}b',boost]])
        wire['auto']={'crease':{'curve':0,'points':points}}
    # Shorten the borrowed pedal's swell enough to speak on the strip's last
    # sixteenth. No echo crossing into the other player's chair, or over the stop.
    steel = 'pedal-steel synth.amp.a=85ms synth.amp.r=80ms fx.1.mix=0 fx.2.mix=0 play.glide=65ms'
    for side,pan in [('left',-.77),('right',.77)]:
        tracks.append(track('steel-'+side,steel,'-5.5dB',pan,'strings'))
    if drum_hand:
        # Seven fixed drums for the two keys, lowest at the drummer's right.
        pitches = sorted({base+p for base in (41,44) for p in opens[1].values()})
        heads = {'head'+str(m): {'patch':'modal-tom','pitch':pitch(m),
                 'pan':round(.45-.8*j/(len(pitches)-1),3)} for j,m in enumerate(pitches)}
        # The mouth is a much quieter partner than the heavy guitars. Bring the
        # rack up between passages, while the stick is off it.
        beats = {name:t/GRID for name,t,_ in sections}
        drums = track('drum-hand',{'kit':heads},
                      {'value':'0dB','mod':[{'src':'auto.touch','amount':1}]},out='drums')
        drums['auto'] = {'touch':{'curve':0,'points':[['0b',-13],
                         [f"{beats['thumbprint']:g}b",-13],[f"{beats['one hand']:g}b",0]]}}
        tracks.append(drums)
    buses={'strings':{'fx':[{'type':'eq','bands':['peak cutoff=360 q=0.8 gain=-2dB','peak cutoff=730 q=1 gain=1.5dB']}]},
           'drums':{'fx':['reverb kind=room mix=0.10 decay=0.53s predelay=7ms',{'type':'glue','threshold':'-22dB','ratio':2.5,'attack':'18ms','release':'120ms'},'clip ceiling=-13dB']},
           'low':{'fx':[{'type':'eq','bands':['peak cutoff=48 q=1.4 gain=-4dB','peak cutoff=98 q=1 gain=3dB','peak cutoff=310 q=0.9 gain=-4dB']},{'type':'compressor','threshold':'-24dB','ratio':5,'attack':'14ms','release':'115ms'}]}}
    doc=dict(about='The Other Hand — chirpers, Common Time, track twelve. One strip of attacks read forwards and back under an unbroken count of four.',tempo=BPM,seed=1,length=f'{start/GRID:g}b',tail='1.3s',ceiling='-1dB',loudness=-10,event_stable=True,buses=buses,master={'fx':[{'type':'eq','bands':['hp cutoff=24']},'gain gain=2dB']},tracks=tracks)
    return doc,sections

def dump(d):
    return '\n'.join('tracks:\n'+'\n'.join('  - '+json.dumps(t) for t in v) if k=='tracks' else k+': '+json.dumps(v) for k,v in d.items())+'\n'

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('-o','--out',type=Path,default=OUT); ap.add_argument('--map',action='store_true'); ap.add_argument('--without-drum-hand',action='store_true',help='regenerate v2'); ap.add_argument('--without-crease',action='store_true',help='regenerate v3'); a=ap.parse_args()
    doc,sections=build(not a.without_drum_hand,not a.without_crease)
    if a.map:
        for sec,t,n in sections: print(f'{sec:12s} {t/GRID*60/BPM:6.2f}s — {(t+n*STRIP)/GRID*60/BPM:6.2f}s')
    else: a.out.write_text(dump(doc))
