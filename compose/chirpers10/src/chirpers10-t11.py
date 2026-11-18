#!/usr/bin/env python3
"""On Its Hinge — one guitar phrase with two possible walks underneath it.

One cell = twelve eighths. The quick drummer counts six quarters (144/min);
without changing the riff, the broad drummer counts four dotted quarters (96).
A pump organ already breathes in the second time while the first is playing.
Times are in sixteenths here, in regular quarter-note beats in the output.
"""
import argparse
import json
import os
from collections import defaultdict
from pathlib import Path

BPM, SUB, CELL, HOME = 144, 4, 24, 34  # B flat on the next string up from low F
FORM = [('latch', 4), ('quick', 12), ('lean', 8), ('broad', 12), ('bellows', 8),
        ('shoulder', 12), ('swing', 16), ('home', 8), ('shut', 2)]
PITCH = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t11.yaml'
ORGAN = os.getenv('C10T11_REED', '-9dB')
PUMP = os.getenv('C10T11_PUMP', '-13dB')
# v2: the pitched drum answers the anticipated notes on the next broad footfall.
# Track gain; semitones above the riff. Empty = published v1.
KETTLE = os.getenv('C10T11_KETTLE', '-7dB;0')
# v3: at home the delayed note changes hands, from the opening harmonic
# to a bowed metal rod. Empty restores v2; KETTLE empty still defaults to v1.
ROD = os.getenv('C10T11_ROD', '-9dB' if KETTLE else '')
# v4: keep a double stop ringing over each of the last five changes of feet.
# Register in semitones. Empty restores v3; older version switches still work.
STAY = os.getenv('C10T11_STAY', '0' if ROD else '')
# v5: the muted half of the heavy riff is heard on skins before it is picked.
# Empty restores v4 (and the older switches retain their published defaults).
PICKUP = os.getenv('C10T11_PICKUP', '1' if STAY else '')
# v6: F stays in the clean guitar while the bass changes what that F means.
# Clean harmonic's trim in the middle (dB). Empty restores v5.
PIVOT = os.getenv('C10T11_PIVOT', '4.5' if PICKUP else '')
# v7: a reed phrase around (not inside) the control. Register over low Bb;
# empty restores v6. The four notes come straight from the open guitar strokes.
COUNTER = os.getenv('C10T11_COUNTER', '24' if PIVOT else '')
# v8: open the broad phrases of the swing around a fixed release. Register
# above the original answer in semitones; empty restores v7 byte for byte.
EARLY = os.getenv('C10T11_EARLY', '12' if COUNTER else '')
# v9: when the band stops, the organ is still breathing the broad walk. It
# comes in under the last chord on the dyad it held at 0:50 and keeps it for
# one more cell alone, at the level it always had. That dyad (F, D flat) has
# no root: on the next downbeat the kettle, which only ever had D flat, F and
# C, lands its first B flat and the reeds close.
# The dyad's trim in dB (benched 0, 6 and 10: 0 already stands 10 dB under
# the chord) ; the kettle's B flat in semitones over the low string (empty: no
# kettle) ; its velocity. Empty restores v8 exactly.
BREATH = os.getenv('C10T11_BREATH', '0;0;0.9' if EARLY else '')
if BREATH:
    FORM[-1] = ('shut', 3)
# v10: before the organ arrives, one guitar says the riff from its middle.
# The two halves have their answers in the same places, so D flat and F sound
# together; the clipped strokes no longer coincide. Semitones the turned
# guitar's answers sit above the written ones. Empty restores v9 exactly.
HALF = os.getenv('C10T11_HALF', '12' if BREATH else '')
# v11: the last changes of feet get the grounds of 1:30. Each time the broad
# walk comes back in the second half of the swing, the bass leaves the
# guitars' B flat at the half cell (where the two walks agree, and where the
# band already re-enters) and plants G flat, then E flat, then F under the
# unchanged riff. The quick cells and 'home' stay on B flat. Semitones from
# the low B flat, one for each broad phrase; empty restores v10.
GROUND = os.getenv('C10T11_GROUND', '-4,-7,-5' if HALF else '')
# v12: before the quiet bridge the riff shows its bones. The song opens on the
# riff's open notes alone (harmonics) and comes home on them as ringing
# chords; in the last cell before the bridge the band plays them once in
# between, as stops: no clipped strokes, and guitars, bass and kick strike
# only the four open notes while the broad walk goes on. The opening's
# harmonic plays them too, for the first time since 0:10.
# How many cells thin out: 1 = the last cell only; 2 = the cell before it
# loses its second half's clipped strokes first; 3 = one more cell does that
# and the last two are bare. Scored on seeds 0/11/5 against v11's
# 97.6/94.4/99.3 without the harmonic: 97.0/93.8/99.2, 95.8/93.5/98.9 and
# 90.6/92.3/97.8. Empty restores v11.
BONES = os.getenv('C10T11_BONES', '1' if GROUND else '')
BROAD = CELL // 4
# Offset, duration, semitones, open power chord / single ringing note / palm mute.
# The two short strokes before the Db and the delayed F are the tell in both walks.
RIFF = [(0,3.55,0,'p'), (4,0.65,0,'m'), (5,0.65,0,'m'), (7,2.7,3,'n'),
        (11,0.68,0,'m'), (12,2.0,0,'p'), (15,0.72,0,'m'), (17,0.75,0,'m'),
        (19,2.55,7,'n'), (22,0.83,0,'m')]
LAST_ANSWER = max(t for t,_,_,kind in RIFF if kind=='n')
# In the heavier verse the answers arrive BEFORE the root, and hang over the
# drummer's next footfall. A different phrase, not the first riff cut or sped up.
LIFT = [(0,0.70,0,'m'), (2,0.70,0,'m'), (3,3.65,3,'p'), (8,0.65,0,'m'),
        (10,0.7,0,'m'), (11,3.8,7,'p'), (16,0.7,0,'m'), (18,1.1,0,'m'),
        (20,3.5,2,'n')]


def note(n):
    return PITCH[n%12] + str(n//12 - 1)


def chord(*ns):
    return ','.join(note(n) for n in ns)


def make():
    notes = defaultdict(list)
    marks = {}
    def put(tr, at, dur, p, v, mute=False):
        ev = dict(at=round(at/SUB, 5), len=round(dur/SUB, 5), pitch=note(p) if isinstance(p,int) else p, vel=round(v,3))
        if mute:
            ev['expr'] = {'pm': 1.0}
        notes[tr].append(ev)
    def drum(p, at, v):
        tr = {'k':'kick', 's':'snare', 'h':'hat', 'rde':'metal', 'x':'metal', 'c':'metal'}.get(p,'skins')
        put(tr, at, 4.5 if p in ('x','rde','c') else 1.2, p, v)
    def walk(start, period, bronze, back=True):
        for j,t in enumerate(range(0,CELL,period)):
            drum(bronze, start+t, (.68 if j==0 else .52) if bronze=='h' else (.65 if j==0 else .54))
            if back and j%2==1:
                drum('s',start+t,.98 if j==1 else .91)
    def answer(i,semi):
        # Every fourth cell its high fifth folds down to the major second instead.
        return 2 if i%4==3 and semi==7 else semi
    def strings(at, dur, midi, typ, vel, wide=False):
        pitch=chord(midi,midi+7) if typ=='p' else midi
        for tr in (('gl','gr','wallL','wallR') if wide else ('gl','gr')):
            put(tr, at, dur, pitch, vel, typ=='m')
    def reed(start,i,melody=False):
        if not ORGAN: return
        if melody:
            # The two answers from the riff, each granted half a cell to ring.
            for k,semi in enumerate((3,answer(i,7))):
                # After the heavy band stops, let the bass and harmonic speak
                # one broad step before the organ. Its second note is not delayed.
                wait = BROAD if PIVOT and i==0 and k==0 else 0
                put('bellows', start+k*CELL/2+wait, CELL/2-.5-wait, HOME+36+semi, .90)
        else:
            # F4 under Db5/C5: the upper bench makes the bellows motion less buried.
            put('bellows',start,CELL-.15,chord(HOME+31,HOME+36+(2 if i%4 in (2,3) else 3)),.78)
    def other_walk(start, cell, step):
        # Two cells = five seconds. The same four-note sentence fits twice at
        # four steps a cell, three times at six. Carry it across cell boundaries.
        tune = [s for _,_,s,k in RIFF if k!='m']
        steps = CELL//step
        for j in range(steps):
            pos = (cell*steps+j) % len(tune)
            put('bellows',start+j*step,step*(.80,.70,.52,.92)[pos],
                HOME+int(COUNTER)+tune[pos],(.89,.84,.78,.92)[pos])

    def swing_slow(i):
        return i<4 or 8<=i<10 or (12<=i<16 and i%2==0)

    def main_riff(start,i,lift=False,wide=False,lend=False,carry_out=False,count_in=False,bass_floor=None,plant=None,bare=0):
        pattern = LIFT if lift else RIFF
        meet = CELL//2             # both walks hit 12: three quarters or two dotted quarters
        last = max(t for t,_,_,kind in pattern if kind=='n')
        if count_in:
            for foot in range(0,meet,4 if lift else BROAD):
                drum('k',start+foot,.98 if not foot else .85)
        for pos,d,s,kind in pattern:
            t=pos
            if kind=='m' and (bare>1 or (bare and t>=meet)):
                continue  # the clipped stroke, with its bass note and its kick, is left out
            if count_in and t<meet:
                if lift and kind=='p' and t+d>meet:
                    d -= meet-t; t=meet   # untie the anticipation: keep the original release
                else:
                    continue
            m=HOME+answer(i,s); v=.87 if kind=='m' else .96
            if lend and kind!='m':
                if kind=='n':
                    continue  # C is now the drum's alone, at the following cell head.
                d=min(d,BROAD-t%BROAD-.25)  # release the chord just before the footfall
            if carry_out and t>=last:
                strings(start+t,d,m,kind,v)   # outside pair still finishes the old riff
                if t==last:
                    gate=CELL-t+meet-.20
                    put('wallL',start+t,gate,HOME+int(STAY),.94)
                    put('wallR',start+t,gate,m+int(STAY),.94)
            else:
                strings(start+t,d,m,kind,v,wide)
            if plant is not None and t>=meet:
                # One long note under the second half of the riff: the lowest
                # the bass goes under distortion, an octave-and-more of floor.
                if t==meet:
                    put('bass',start+t,CELL-meet-.3,plant,.93)
            elif kind!='m' or t in (4,15,16):
                # The first hint: the riff is unchanged over Gb. Its Db still
                # has a bass fifth; the guitar's F is now the major seventh.
                low = m if bass_floor is None else bass_floor + (7 if s==3 else 0)
                put('bass',start+t,d,low,.91,kind=='m')
            if pos in ((0,3,8,11,18) if lift else (0,4,7,12,17)):
                drum('k',start+t,.98 if kind!='m' or t==0 else .82)
            elif bare and kind=='n':
                # Its kick used to fall on the clipped stroke before it. With
                # that gone the foot goes to the late answer itself, as at home.
                drum('k',start+t,.98)
    start=0
    for section,count in FORM:
        marks[section]=start
        for i in range(count):
            a=start+CELL*i
            if section=='latch':
                for t,d,s,kind in RIFF:
                    if kind=='m': continue
                    put('latch',a+t,d*1.1,HOME+24+answer(i,s),.77)
                if PICKUP and i:
                    # Nothing invented for a fill: the two clipped strokes
                    # before Db, the single hits, and the later pair are all
                    # muted slots of the riff the band is about to play.
                    for t,d,_,kind in RIFF:
                        if kind!='m' or (i==1 and t>=CELL//2): continue
                        if i==count-1 or (i==count-2 and t<CELL//2):
                            put('gl',a+t,d,HOME,.84,True)
                            # The other amp catches the last three strokes. The
                            # full chord, the bass and the kick still wait for 0:10.
                            if i==count-1 and t>=CELL//2:
                                put('gr',a+t,d,HOME,.84,True)
                        else:
                            # High drum at the front of the phrase, low at the
                            # back; very last stroke is a pickup to the repeat.
                            piece = 't1' if t<CELL//2 else ('t2' if t==22 else 'ft')
                            drum(piece,a+t,(.32 if t in (4,15) else .23) + .16*(i-1))
                elif not PICKUP and i>=2:
                    for t,p in ((0,'t1'),(CELL//2,'ft')): drum(p,a+t,.60)
            elif section=='shut':
                if i==0:
                    for t,s in ((0,3),(6,2),(12,0)):
                        dur = CELL+11.5 if t==12 else 5.3
                        strings(a+t,dur,HOME+s,'p',.96,True)
                        put('bass',a+t,dur,HOME+s,.94); drum('k',a+t,.9)
                    put('glass',a+12,CELL+11.5,HOME+31,.82); drum('c',a+12,.92)
                    if BREATH and ORGAN:
                        # No new attack after the band's last one: the reeds
                        # start under the chord and are simply left sounding.
                        put('bellows',a+12,count*CELL-12.5,chord(HOME+31,HOME+36+3),.78)
                        trim,low,touch=(BREATH.split(';')+['',''])[:3]
                        if float(trim):
                            notes['bellows'][-1]['gain']=f'{float(trim):g}dB'
                        if KETTLE and low:
                            put('kettle',a+count*CELL,10,HOME+int(low),float(touch))
                            marks['close']=3
            elif section=='bellows':
                reed(a,i,True)
                # Two phrases on each ground: Bb, Gb, Eb, F. The upper F is
                # fifth, major seventh, ninth, then root; it never transposes.
                turn = 4*i//count
                floor = HOME + ((0,-4,-7,-5)[turn] if PIVOT else 0)
                for t in (0,12):
                    put('bass',a+t,9.5,floor+(0 if t==0 else 7),.76)
                    drum('ft' if t==0 else 't2',a+t,.57)
                if PIVOT:
                    put('glass',a,CELL-1,HOME+19,.80)
                    # Answer below the harmonic at the riff's original Db/F
                    # attacks. Only on the final F does the suspended Bb go to A.
                    for t,_,_,k in RIFF:
                        if k=='n':
                            inner = (15,12,8,12)[turn] - int(i==count-1 and t==LAST_ANSWER)
                            put('glass',a+t,min(5,CELL-t-.2),HOME+inner,.82)
                else:
                    for t,d,s,k in RIFF:
                        if k!='m': put('glass',a+t,d,HOME+24+answer(i,s),.76)
                if i>=count//2:
                    for t in range(0,CELL,4): drum('h',a+t,.46 if t else .6)
            elif section=='home':
                # The open attacks keep their original positions; the spaces between
                # are now holes, or a single muted pickup on alternate cells.
                for t,d,s,k in RIFF:
                    if k=='m' and not (i%2 and t in (4,5)): continue
                    m=HOME+answer(i,s); dur=d if k=='m' else min(5.5,CELL-t-.2)
                    # Keep the first quarter of the return as it was. For the
                    # high answer only, the outer guitars stay and the second
                    # pair give up their chord to a different kind of metal.
                    late = bool(ROD) and i>=count//4 and t==LAST_ANSWER
                    strings(a+t,dur,m,'m' if k=='m' else 'p',.94,not late)
                    if late:
                        if i<3*count//4:
                            # Same octave and touch as the note in 'latch'.
                            put('latch',a+t,d*1.1,m+24,.77)
                        if i>=count//2:
                            # Its bow swells an octave below the sounding
                            # harmonic; carry through the next downbeat, but
                            # lift early on the last C so the cadence is clear.
                            put('rod',a+t,CELL-t+2 if i<count-1 else CELL-t-1.6,m+24,.88)
                    if k!='m': put('bass',a+t,dur,m,.94); drum('k',a+t,.98)
                walk(a,6,'rde')
                if i in (0,4): drum('c',a,.84)
            else:
                slow=section in ('broad','shoulder')
                if section=='swing':
                    slow = swing_slow(i)
                lifted=section=='shoulder' or (section=='swing' and not slow)
                reply = bool(KETTLE) and section=='shoulder' and i>=count//3
                # After the first two-cell broad statement, only the kit attacks
                # the new walk until its midpoint. Do not carry into 'home'.
                split = bool(STAY) and section=='swing'
                count_in = split and i>count//2 and slow!=swing_slow(i-1)
                carry_out = split and count//2<=i<count-1 and slow!=swing_slow(i+1)
                floor = HOME-4 if PIVOT and section=='quick' and count//3<=i<count//2 else None
                thin = 0
                if BONES and section=='broad':
                    back = count-1-i            # cells before the bridge
                    thin = 2 if back==0 or (back==1 and int(BONES)>=3) else int(back<int(BONES))
                plant = None
                if GROUND and split and slow and i>=count//2:
                    # 8-9, 12 and 14: the broad phrases among the last five
                    # changes. The first cell of each is planted at its half;
                    # a second cell walks the riff's rhythm on that ground.
                    heads = [k for k in range(count//2,count) if swing_slow(k) and not swing_slow(k-1)]
                    ground = HOME+int(GROUND.split(',')[max(n for n,k in enumerate(heads) if k<=i)])
                    if i in heads: plant = ground
                    else: floor = ground
                main_riff(a,i,lift=lifted,wide=section in ('shoulder','swing'),lend=reply and i>=2*count//3,
                          carry_out=carry_out,count_in=count_in,bass_floor=floor,plant=plant,
                          bare=thin)
                if thin==2 and i==count-1:
                    # Same octave and touch as the opening. It rings into the
                    # stops, and the bridge's clean F takes over from it.
                    for t,d,s,k in RIFF:
                        if k!='m': put('latch',a+t,d*1.1,HOME+24+answer(i,s),.77)
                if reply:
                    for t,_,s,k in LIFT:
                        if k=='m': continue
                        landing=(t//BROAD+1)*BROAD
                        put('kettle',a+landing,2.1 if k=='p' else 3.7,
                            HOME+answer(i,s)+int(KETTLE.split(';')[1]), .93 if k=='p' else .98)
                walk(a,6 if slow else 4,'x' if section in ('shoulder','swing') else 'h')
                if COUNTER and ORGAN and section=='lean' and i<2:
                    other_walk(a,i,BROAD)  # organ anticipates the four; drummer still plays six
                elif COUNTER and ORGAN and section=='broad' and 4<=i<6:
                    other_walk(a,i-4,SUB)  # keep one memory of the six after the kit changes
                elif section=='lean' or (section=='broad' and i<count-4): reed(a,i)
                if section in ('quick','shoulder','swing') and i==0: drum('c',a,.88)
                if section=='broad' and i==count-1:
                    for t,p in ((18,'t1'),(20,'t2'),(22,'ft')):drum(p,a+t,.73)
        start+=count*CELL
    if EARLY:
        start_swing = marks['swing']
        calls = [(t,d,s) for t,d,s,k in RIFF if k=='n']
        first = calls[0][0]
        assert len(calls)==2 and calls[1][0]==first+CELL//2
        attacks = (first, BROAD, SUB, 0)  # late; broad foot; quick foot; downbeat
        assert all(swing_slow(i) for i in range(len(attacks))) and not swing_slow(len(attacks))
        pair = ('wallL','wallR')
        for i, attack in enumerate(attacks):
            if i==0: continue  # hear the whole riff once after the kettle's last C
            a = start_swing + CELL*i
            for tr in pair:
                notes[tr] = [n for n in notes[tr] if not a <= n['at']*SUB < a+CELL]
            for which,(old,d,semi) in enumerate(calls):
                head = which*(CELL//2)
                now, off = head+attack, old+d
                # The low fifth occupies the front of the same space. As one
                # player's answer opens, the other player's chord closes.
                if attack:
                    put(pair[1-which],a+head,attack-.28,chord(HOME,HOME+7),.91)
                put(pair[which],a+now,off-now,HOME+int(EARLY)+answer(i,semi),.96)
                stop,gate,_,_ = next(n for n in RIFF if n[0]>=off and n[3]=='m')
                put(pair[which],a+stop,gate,HOME,.84,True)  # catch the ring on the original clipped stroke
                # The facing amp and bass keep the old attack: the high voice
                # starts alone, the octave joins late, and they release together.
                same_side = ('gl','gr')[which]
                notes[same_side] = [n for n in notes[same_side] if n['at']*SUB!=a+old]
        # The fourth answer is C, not F. The same hand takes it up one fret
        # to the first Db of the quick riff, then rejoins the low guitars.
        turn = start_swing + len(attacks)*CELL
        landing,gate,semi,_ = next(n for n in LIFT if n[3]=='p')
        notes['wallR'] = [n for n in notes['wallR'] if not turn <= n['at']*SUB <= turn+landing]
        put('wallR',turn+landing,gate,HOME+int(EARLY)+semi,.96)
    if HALF:
        # Last four cells of the quick verse (0:30-0:40). First the right hand
        # only trades the two answers; then it plays the whole riff starting
        # at the half cell, where both walks agree; then the left hand does.
        # The fourth cell, with its C, is the written unison again. Bass and
        # kick stay with the written riff throughout.
        quick, half = marks['quick'], CELL//2
        for i,(tr,turned) in zip(range(8,11), (('gr',False),('gr',True),('gl',True))):
            a = quick + CELL*i
            assert answer(i,7)==7 and not swing_slow(4)
            written = [n for n in notes[tr] if a <= n['at']*SUB < a+CELL]
            assert len(written)==len(RIFF)
            notes[tr] = [n for n in notes[tr] if n not in written]
            for pos,d,semi,kind in RIFF:
                if turned:
                    at = (pos+half) % CELL
                else:
                    at = pos
                    if kind=='n':
                        # Same place and gate, the other half's pitch.
                        semi = next(s for t,_,s,k in RIFF if k=='n' and t==(pos+half)%CELL)
                m = HOME+semi+(int(HALF) if kind=='n' else 0)
                put(tr,a+at,d,chord(m,m+7) if kind=='p' else m,.87 if kind=='m' else .96,kind=='m')
    # The control comparison for the hinge: all non-drum attacks, pitches, gates,
    # velocities and expressions repeat exactly. Drums are counted independently.
    hinge=marks['broad']/SUB; span=4*CELL/SUB
    def window(tr,a,b):return [dict(e,at=round(e['at']-a,5)) for e in notes[tr] if a<=e['at']<b]
    for tr in ['gl','gr','wallL','wallR','latch','glass','bass','bellows','kick']:
        assert window(tr,hinge-span,hinge)==window(tr,hinge,hinge+span),tr
    assert [len(window('hat',a,a+span)) for a in (hinge-span,hinge)]==[24,16]
    assert [len(window('snare',a,a+span)) for a in (hinge-span,hinge)]==[12,8]
    def tr(name,patch,gain,pan=0,out=None,fx=None):
        d={'name':name,'patch':patch,'gain':gain,'pan':pan,'notes':sorted(notes[name],key=lambda n:n['at'])}
        if out:d['out']=out
        if fx:d['fx']=fx
        return d
    # The twin pair supplies the pick; the second pair joins after the exposed
    # bellows, on a wider-bodied amp. Both play actual rests.
    tracks=[tr('gl','ct-twin fx.1.model=gojira fx.2.cone=81','0.5dB',-1,'gtrs'),
            tr('gr','ct-twin fx.1.model=gojira fx.2.cone=82','0.5dB',1,'gtrs'),
            tr('wallL','ct-wall-stop-l','-3dB',-.72,'gtrs'),tr('wallR','ct-wall-stop-r','-3dB',.72,'gtrs'),
            tr('latch','ct-bell','6.5dB',0),tr('glass','ct-bell','-1.5dB',-.20),
            tr('bass','ct-bass','0.7dB',0,'low'),tr('kick','ct-kit','2dB',0,'drums',[{'type':'eq','bands':['peak cutoff=4500 q=0.8 gain=8dB']}]),
            tr('snare','ct-kit','3dB',0,'drums'),tr('hat','ct-kit','12dB',-.28,'drums'),
            tr('metal','ct-kit','-4dB',.25,'drums'),tr('skins','ct-kit','3dB',0,'drums')]
    if PIVOT:
        # A long harmonic is much quieter than the old picked figure. Lift it
        # in the bridge only; the same guitar's final F stays at its old gain.
        glass = next(t for t in tracks if t['name']=='glass')
        glass['gain'] = {'value':glass['gain'],'mod':[{'src':'auto.pivot','amount':1}]}
        end = marks['shoulder']/SUB
        glass['auto'] = {'pivot':{'curve':0,'points':[['0b',float(PIVOT)],
                          [f'{end:g}b',float(PIVOT)],[f'{end+1:g}b',0]]}}
    if ORGAN:
        pump=[{'type':'pump','every':'3/8','attack':'12ms','hold':'28ms','release':'395ms','depth':PUMP,'curve':0.65}] if PUMP else []
        organ = tr('bellows','harmonium',ORGAN,.12,fx=pump)
        if COUNTER and pump:
            # The fingers make these attacks. Leave only a little of the deep
            # pedal duck on them; full bellows depth returns for the held dyads.
            wet=[['0b',1.0]]
            for tick in (marks['lean'], marks['broad']+4*CELL):
                b0,b1=tick/SUB,(tick+2*CELL)/SUB
                wet += [[f'{b0:g}b',1.0],[f'{b0+.01:g}b',.25],
                        [f'{b1-.01:g}b',.25],[f'{b1:g}b',1.0]]
            pump[0]['mix']={'value':0,'mod':[{'src':'auto.hand','amount':1}]}
            organ['auto']={'hand':{'points':wet,'curve':0}}
        tracks.append(organ)
    if KETTLE:
        tracks.append(tr('kettle','timpani fx.0.mix=0.07 synth.amp.r=240ms',KETTLE.split(';')[0],-.15))
    if ROD:
        # Shorter bow and smaller water movement than the ambient patch: the
        # dissonant upper partials carry the sound, not a detuned six-second hall.
        tracks.append(tr('rod','waterphone synth.amp.a=150ms synth.amp.r=135ms synth.pitch.mod.0.amount=0.12 synth.pitch.mod.1.amount=0.18 fx.0.decay=0.8s fx.0.mix=0.09',ROD,-.15))
    doc={'about':'On Its Hinge — chirpers, Common Time, track eleven. A twelve-eighth riff in B flat; the drummer swaps six quick steps for four broad ones, on an unchanged riff. The reed organ breathes the broad walk before the kit takes it.' + (' The kettledrum answers the heavy riff on the next broad steps, then takes its last C.' if KETTLE else ''),
         'tempo':BPM,'seed':1,'length':f'{start//SUB+marks.pop("close",0)}b','tail':'4s','ceiling':'-1dB','loudness':-10,'event_stable':True,
         'buses':{'drums':{'fx':['reverb kind=room decay=0.62s mix=0.13 predelay=7ms',{'type':'glue','threshold':'-22dB','ratio':2.5,'attack':'20ms','release':'135ms'},'clip drive=0dB ceiling=-13dB',{'type':'eq','bands':['peak cutoff=400 q=0.8 gain=-5dB','highshelf cutoff=9000 gain=-2dB']}]},
                  'gtrs':{'fx':[{'type':'eq','bands':['peak cutoff=350 q=1 gain=-2dB','peak cutoff=720 q=0.9 gain=2dB']},'reverb kind=room decay=0.35s mix=0.06 predelay=6ms']},
                  'low':{'fx':[{'type':'eq','bands':['peak cutoff=58 q=1.5 gain=-6dB','peak cutoff=116 q=1 gain=5dB','peak cutoff=350 q=1 gain=-6dB','peak cutoff=1500 q=1 gain=3dB']},{'type':'compressor','threshold':'-26dB','ratio':6,'attack':'12ms','release':'120ms','makeup':'2dB'}]}},
         'master':{'fx':[{'type':'eq','bands':['hp cutoff=24']},'gain gain=2.7dB']},'tracks':tracks}
    return doc,marks


def dump(d):
    return '\n'.join('tracks:\n'+'\n'.join('  - '+json.dumps(t) for t in v) if k=='tracks' else k+': '+json.dumps(v) for k,v in d.items())+'\n'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('-o','--out',type=Path,default=Path(os.environ.get('C10T11_OUT',OUT)));p.add_argument('--map',action='store_true'); a=p.parse_args(); doc,marks=make()
    if a.map:
        for name,cells in FORM:
            t=marks[name];print(f'{name:10} {t/16+1:g}-{(t+CELL*cells)/16+1:g} bars; {t/SUB*60/BPM:g}s, {cells} cells')
    else: a.out.write_text(dump(doc))
