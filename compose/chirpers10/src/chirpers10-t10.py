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
# v5: 'called in' puts the straight clock into the right guitarist's hands.
# Semitones above the low part; the left joins that register at par. Empty = v4.
STRAIGHT = os.environ.get('C10T10_STRAIGHT', '12' if COURSES else '')
# v6: repay each clock gap as the length of a note. Empty restores v5;
# omitting STRAIGHT still gives the pre-crossing arrangement.
PAYBACK = os.environ.get('C10T10_PAYBACK', '1' if STRAIGHT else '')
# v7: breath and pick are the two halves before anybody borrows a tick.
# Empty gives v6 exactly; PAYBACK empty still gives the pre-fill version.
BREATH = os.environ.get('C10T10_BREATH', '-15' if PAYBACK else '')
# v8: count the first debts on damped bronze keys. Track gain; empty = v7.
CHANGE = os.environ.get('C10T10_CHANGE', '-11.5' if BREATH else '')
# v9: once the answer arrives early in 'called in', a pressure drum takes the
# terrain key's stroke and bends to the pitch of the square guitar. Empty = v8.
PRESS = os.environ.get('C10T10_PRESS', '-13' if CHANGE else '')
# v10: the distance between the two markers becomes the bassist's step.
# Fraction of the step held; empty restores v9 and earlier switches.
STRIDE = os.environ.get('C10T10_STRIDE', '.80' if PRESS else '')
# Before a downbeat moves, the brush borrows *duration*. Empty restores v10.
BRUSH = os.environ.get('C10T10_BRUSH', '-7' if STRIDE else '')
# v12: at the crest the baritone still plays the call in the bar it was given.
# First time on each ground only (the second time has the backwards pickup).
# Semitones over the guitars' call ; its lift over the opening, dB ; 1 = the
# third guitar gives its call chord to the reed. Empty restores v11.
# Benched an octave lower (its opening register): 10 dB under the mix and the
# short third note 13-14 under. Up here it is a line, so it needs less lift,
# and the third guitar keeps its chord where each new ground arrives.
RECALL = os.environ.get('C10T10_RECALL', '24;3;0' if BRUSH and BREATH else '')
# v13: what the mallet buys is kept on account. The bronze count is damped,
# so each new note of the answer was gone as soon as it was struck. Now the
# newest key is left sounding (a bow on the bar's edge, so it holds under the
# band) until the next one is bought: G flat, F, C, then E flat, the answer
# at a thirty-third of its speed over the riff that will not leave E flat.
# Each lasts one pair and the sixteenth just borrowed; the last is damped a
# sixteenth before the plain late pairs. Its shimmer is the drummer's clock:
# one beat of the paired tuning for every straight sixteenth.
# Track gain in dB ; depth of the shimmer. Benched at -17: 7.5 dB under the
# raw mix and four fifths of everything at 500-1000 Hz, a test tone. At -24:
# 14 under, but the passage read 2.3 dB over the records at 500-1000 Hz
# (0.4 without it). So -27, and the two lower keys 2 dB less again: the band
# leaves less in their semitones, and they stood 5 dB further out of it.
# Empty restores v12; it is on only
# while every older switch is, so each of those still gives what it gave.
KEPT = os.environ.get('C10T10_KEPT', '-27;0.55' if all((
    RECALL, BRUSH, STRIDE, PRESS, CHANGE, BREATH, PAYBACK, STRAIGHT, COURSES, ADVANCE, TRADE)) else '')
# v14, whole song: THE GROUND RISES WITH THE CREDIT. From the pocket at 1:30 to
# the line at 2:17 the riff sat on E flat for seven pairs running, and the
# line's first low chord, A flat, arrived from nowhere. Once the answer starts
# to come EARLY, the whole band now climbs to meet that chord: the pair four
# ticks in credit is on F, the pair six in credit on G flat, and the line's
# A flat is the next step. The song's first minute borrows on a ground that
# will not move and climbs only at full debt (E flat, G flat, A flat); its
# second half now climbs as the debt turns to credit, by step, to the same A
# flat. Guitars, bass, the straight guitar and the pressure drum all move
# together (the drum bends to the answer's first note on each new ground).
# And the third guitar, the wall chord that carries the crest and the line,
# strikes each new ground and its answer: the three climbs share one voice.
# Semitones over E flat for the pairs two, four and six ticks in credit ;
# 1 = the wall chord on each raised ground. Empty restores v13; it is on only
# while KEPT is.
LADDER = os.environ.get('C10T10_LADDER', '0,2,3;1' if KEPT else '')
# v15 (palette): THE QUIET ROOM HAS ITS OWN BASS AND ITS OWN FOOT. The song is played by two bands: the loud one, and a
# small quiet one that is heard before it at 0:00 and inside it at 1:30: a baritone sax, a clean guitar, a piano, a
# brush on the snare (0:26). The quiet band had no bass of its own: in both of its rooms the eight-string band's bass
# guitar played for it, and at 0:04 and 0:08 the metal kit's kick. Now the quiet band has an UPRIGHT BASS, plucked
# (the library's `upright-bass`; no other song on the record has one): the two low E flats under the sax, the four
# pedals of the pocket (A flat, G flat, E flat, E flat) and the three notes that pay the pocket's debts back (G flat,
# F, C, with the toms). And its foot is the brush kit's feathered bass drum, on the brush's own track. So the first
# stroke of the bass guitar and of the metal kick drum is the loud band's entrance at 0:12.9 (its hat, snare and one
# muted guitar still steal in at 0:08.6, as they did), and after the pocket the bass guitar comes back on the
# downbeat of 1:47.1. No note is added, moved or removed. In v14 the metal kick at 0:08.6 was the introduction's
# loudest instant, 5 dB over full scale before the limiter, which turned everything down 6 dB to pass it.
# patch (with overrides) ; track gain dB ; semitones against the bass guitar's written notes ; the feathered kick's
# gain over the brush track (dB ; empty leaves the metal kick in the introduction). Empty restores v14; it is on only
# while LADDER is.
# Benched raw, seed 0. The library patch as it is, at 0 dB: 2 to 10 dB over the bass guitar's notes (K), and its
# pedal 24 dB down before the end of its ten sixteenths (the bass guitar's is held). So: the string's decay doubled
# (1.7 s to 3.4 s: 10 to 12 dB down at the end), the note's whole written length (gate 1), and a track gain at which
# the pocket reads as loud as it did (at -4 it was 0.15 LU over v14 finished, at -5 0.27 under).
ROOM = os.environ.get('C10T10_ROOM', 'upright-bass play.gate=1 play.humanize.time=0ms play.humanize.vel=0 '
                      'synth.layers.0.decay.value=3.4s;-4.5;0;0' if LADDER and BRUSH else '')
# A plucked pedal dies away where the bass guitar's was held, so a few of the pocket's quietest moments fall under
# the loudness meter's gate and the file read 0.024 dB louder: every other bar came out that much quieter. This target
# gives those bars the gain they had in v14.
ROOM_LUFS = -9.976
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


def pressure_skin():
    # The short, inharmonic skin sound dies before the pitched bend. Only one
    # fingertip attack: the wrist moves the remaining modes up to the reply.
    layers = [
        {'type':'additive','partials':[[1,.85],[2,.88],[3,.55],[4.02,.38],[5.01,.21],[6.02,.13]],'damp':.38},
        {'type':'additive','partials':[[1.54,1],[2.43,.68],[3.14,.33],[5.16,.22]],
         'level':{'value':'-65dB','mod':[{'src':'env.skin','amount':56}]}},
        {'wave':'sine','ratio':.67,'level':{'value':'-65dB','mod':[{'src':'env.thud','amount':56}]}},
        {'type':'noise','color':'pink','level':{'value':'-66dB','mod':[{'src':'env.tap','amount':58}]}}
    ]
    return {
        'about':'Tuned pressure drum: a fingertip strike, a lower thud and a ringing head. The wrist moves the head pitch without a second attack.',
        'play':{'gate':1,'vel_sens':.6},
        'synth':{
            'layers':layers,
            'env':{'tap':{'a':'0.3ms','d':'17ms','s':0},'thud':{'a':'1ms','d':'95ms','s':0},
                   'skin':{'a':'0.4ms','d':'85ms','s':0}},
            'pitch':{'value':0,'mod':[{'src':'expr.press','amount':1}]},
            'filters':['hp cutoff=95','lp cutoff=6000'],
            'amp':{'a':'1ms','d':'2.4s','s':.24,'r':'45ms','curve':2}
        }
    }


def kept_key():
    # One key of the same bronze, bowed instead of struck: the bar's own pitch
    # with a little of its second and third modes, slow to speak, level while
    # the bow is on it. The song's track adds the shimmer, locked to the tempo.
    return {
        'about':'Still Owing: the bronze key the mallet has just struck, kept sounding with a bow on the edge of the bar. No attack of its own; the damped mallet stroke is its attack.',
        'play':{'gate':1,'vel_sens':.3,'humanize':{'time':'0ms','vel':0}},
        'synth':{
            'layers':[{'type':'additive','partials':[[1,1],[2.52,.085],[4.95,.022]]}],
            'filters':['hp cutoff=150','lp cutoff=5200'],
            'amp':{'a':'170ms','d':'1.2s','s':.82,'r':'120ms','curve':2}
        }
    }


def build():
    voices = defaultdict(list)
    sections = []
    fold_sources, fold_patches = {}, {}
    air_points = [[0,0]]
    call_heads = [p for p,_,_,how in CALL if how!='m']
    change_pitches = [semi for _,_,semi,how in REPLY if how!='m']
    def shade_breath(at, phrase):
        # The bore needs time to speak at Eb2. Articulate an already sounding
        # note rather than restarting it for two 90 ms strokes of mere air.
        for start,end in zip(call_heads,call_heads[1:]+[BAR]):
            taps=[p for p,_,_,h in CALL if start<p<end and h=='m']
            if not taps or phrase==0 or (phrase==1 and start!=0): continue
            pts=[(taps[0]-.65,0),(taps[0]-.25,-30)]
            if phrase==1:  # two short openings of the same low Eb
                for p in taps:
                    pts.extend([(p-.08,-30),(p+.06,0),(p+.51,0),(p+.68,-30)])
            pts.extend([(end-.26,-30),(end-.04,0)])
            air_points.extend([[f'{(at+p)/SUB:g}b',db] for p,db in pts])

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

    def straight_gate(pattern, pos):
        # Lift the pick before the next pitched attack. No repeated pedal notes
        # between: this line has three strokes in the call and four in the answer.
        end = next((p for p,_,_,how in pattern if p>pos and how!='m'), BAR)
        return .72*(end-pos)

    pair = 2*BAR
    crest_roots = (0,0,3,3,5,5)
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
            if s == 'still owing': root += crest_roots[j]
            if s == 'two clocks': root += (5,3,0,0)[j]
            if s == 'square': root += (0,-2,-4,-2,0)[j]
            if LADDER and s == 'called in' and d < 0:
                rungs = [int(x) for x in LADDER.split(';')[0].split(',')]
                credit = sorted((-v for v in debts if v < 0))
                assert len(rungs) == len(credit)
                root += rungs[credit.index(-d)]
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
            early = change_pitches[:d] if CHANGE and s=='on account' and 0 < d <= len(change_pitches) else ()
            if early:
                # The mallet strikes the straight midpoint, always on Gb. Each
                # borrowed tick buys one more note before the full answer.
                for slot, semi in enumerate(early):
                    note('change',t+BAR+slot,.84,root+36+semi,.79 if slot==0 else .70)
                    if slot == 0:
                        voices['change'][-1]['gain'] = '3.5dB'  # keep the piano's downbeat accent
                if KEPT:
                    # The key bought this time rings until the next is bought,
                    # one sixteenth later in the following pair. After the
                    # whole answer there is nothing left to buy: lift it one
                    # sixteenth before the bar line.
                    bought = t+BAR+d-1
                    until = bought+pair+1 if d < len(change_pitches) else t+pair-1
                    note('kept',bought,until-bought,root+36+early[-1],.80)
                    if early[-1] < change_pitches[1]:
                        voices['kept'][-1]['gain'] = '-2dB'  # C and E flat, under the two keys that began the answer
            elif s in ('at par','in hand','on account','two clocks','across the line','square'):
                note('rule',t+BAR,2.2,HOME+31,.72 if s!='two clocks' else .89)
            if PRESS and s=='called in' and d<0:
                # The three early answers leave two, four and six ticks to the
                # straight reply. Start on its other three pitches, nearest
                # first (F3, Eb3, C3); squeeze the head up to Gb3 at the beat.
                target = root + change_pitches[0] + 12
                starts = sorted({root+p+12 for p in change_pitches if root+p+12<target}, reverse=True)
                gaps = sorted(-v for v in debts if v<0)
                assert len(starts)==len(gaps) and turn-d==t+BAR
                base = starts[gaps.index(-d)]
                ticks = -d
                note('pressure',turn,ticks+1,base,.86)
                # The note lasts one more tick at the destination. Half-tick
                # knots keep the bend on time even on the shortest stroke.
                path = []
                for half in range(2*(ticks+1)+1):
                    u = min(1., half/(2*ticks))
                    path.append(round((target-base)*u*u*(3-2*u),5))
                voices['pressure'][-1]['expr_path']={'press':path}
            else:
                tally(turn,root+39,d,4.2 if s=='two clocks' else 2.7)

            if s == 'two clocks':
                # A bass pedal to stand on; listen for the distance between
                # piano and tally contracting 6,4,2,0. No guitar or kit marks
                # their entrances, and they really do become one attack.
                note('bass',t,10,root,.82)
                note('clean',t,12,chord(root+24,root+31),.82)
                if PAYBACK:
                    # No attack between the markers. In the spare air at the end
                    # of each pair the clean string spends exactly its debt on
                    # ONE of the reply notes. At par, string lengths become a
                    # descending bass/tom fill; the next pair supplies the Eb.
                    amounts = [delta for delta in debts if delta>0]
                    pitches = [HOME+semi for _,_,semi,how in REPLY if how!='m']
                    if d:
                        pickup = t + pair-d
                        assert pickup > turn
                        note('clean',pickup,d-.24,pitches[j]+12,.92)
                    else:
                        pickup = t + pair-sum(amounts)
                        assert pickup >= turn+SUB and len(amounts)==len(pitches)-1
                        for dur,p,piece in zip(amounts,pitches[:-1],('t1','t2','ft'),strict=True):
                            note('bass',pickup,dur-.24,p,.90)
                            # Lighten the stick as the notes shorten: the last
                            # floor tom should not cover the bass player's C.
                            kit(piece,pickup,.35+.30*dur/max(amounts))
                            pickup += dur
                        assert pickup == t+pair
                else:
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
            straight_call = bool(RECALL) and s == 'still owing' and j%2==0
            if straight_call:
                # The guitars take 22 sixteenths over Eb-Bb-F. The reed takes
                # the 16 it took at 0:00, so each note of its call comes a
                # little further ahead of theirs, and it stops on the bar line.
                register,lift,_ = RECALL.split(';')
                for p0,_,semi,how in CALL:
                    if how=='m': continue
                    following = next((pos for pos in call_heads if pos>p0), BAR)
                    note('breath',t+p0,following-p0-.25,root+semi+int(register),.90 if p0==0 else .83,sub=.12)
                    voices['breath'][-1]['gain'] = f'{float(lift):g}dB'
            crossing = bool(STRAIGHT) and s == 'called in'
            if crossing:
                for half,shape in enumerate((CALL,REPLY)):
                    for pos,_,semi,how in shape:
                        if how=='m': continue
                        p = root+semi+int(STRAIGHT)
                        # One player stays on 16+16 while the other's answer
                        # moves from six ticks behind to six ticks ahead.
                        note('right',t+half*BAR+pos,straight_gate(shape,pos),
                             chord(p,p+7) if how=='o' else p,.99 if pos==0 else .92)
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
            if BREATH and s=='at par':
                shade_breath(t,j)
            for back, (pattern,at,w) in enumerate(((CALL,t,width),(REPLY,turn,pair-width))):
                for ix,(p0,gate,semi,how) in enumerate(pattern):
                    hit = at+p0*w/BAR
                    dur = gate*w/BAR
                    pitch = (root if back else call_root)+semi
                    mute = how=='m'
                    vel = (.76 if mute else .92) if p0 else .99
                    if s=='at par':
                        # Give the answer a face before its first displacement.
                        if BREATH and not back:
                            # The baritone calls an octave below the original
                            # clean guitar. First connect the three pitches.
                            # Second, tongue the first double stroke on Eb;
                            # third, leave BOTH short pairs to the left guitar.
                            if not mute:
                                following = next((pos for pos in call_heads if pos>p0), BAR)
                                note('breath',hit,following-p0-.25,pitch+12,vel-.09,sub=.12)
                        elif not mute:
                            note('clean',hit,dur,pitch+24,vel-.09)
                        if j>=1 and not back and not p0:
                            note('bass',hit,dur,root,.83); kit('k',hit,.86)
                        if j==2 and mute: note('left',hit,dur,pitch,.70,pm=1)
                        continue
                    # Low Eb call, high Gb answer. In the first crest the right
                    # hand lets its reply ring instead of adding more mutes.
                    for side in ('left','right'):
                        if crossing:
                            if side=='right': continue  # already played the square version
                            if back and d==0 and mute: continue
                        if repay and back and side == 'right' and p0 < dry_from:
                            continue  # no right-hand chugs between the notes given to the open courses
                        if (advance or early) and side=='right' and not back and hit>=t+BAR:
                            continue  # the left guitar keeps the tail of the call; the right makes room
                        if trade and back and p0 not in reunited:
                            if mute and (side=='right' or (d<0 and hit<lay_out_until)): continue
                            if not mute and (d<0 or side=='left'): continue
                        if s=='called in' and j<3 and side=='right' and not back: continue
                        if s=='still owing' and side=='right' and back and mute: continue
                        meeting = crossing and back and d==0
                        gp = pitch+int(STRAIGHT) if meeting else pitch
                        voiced = chord(gp,gp+7) if how=='o' else gp
                        if s=='square' and back and not mute and side=='right':
                            voiced=chord(pitch,pitch+7)
                        guitar_gate = straight_gate(pattern,p0) if meeting else dur
                        if early and side=='right' and not back:
                            guitar_gate = min(guitar_gate, t+BAR-hit)
                        note(side,hit,guitar_gate,voiced,vel,**({'pm':1} if mute else {}))
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
                    if s in ('still owing','across the line') and how=='o' and not (trade and back and j<6) and not (
                            straight_call and not back and RECALL.split(';')[2]=='1'):
                        note('weight',hit,dur,chord(pitch,pitch+7),.93)
                    if LADDER and LADDER.split(';')[1]=='1' and s=='called in' and root!=HOME and how=='o':
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
            # Three still-square pairs just before the first unequal one. The
            # two strokes always start on beat two, and always share eight ticks.
            spread = (j-(len(debts)-2) if s=='in hand' and j>=len(debts)-2 else
                      2 if s=='on account' and j==0 else None)
            if BRUSH and spread is not None: assert d==0
            for i in range(pair//SUB):
                q = t+i*SUB
                if s=='at par' and j<2: continue
                if s in ('called in','at par') and i%2: continue
                if trade and d<0 and turn<=q<lay_out_until:
                    kit('h',q,.56 if i%4==0 else .44)
                    continue
                if BRUSH and spread is not None and i%4==1:
                    # 4+4, 5+3, 6+2 sixteenths of wire on the head. Nothing
                    # new strikes as the longer sweep passes the backbeat.
                    note('sweep',q,SUB+(spread if i<4 else -spread),'sw',.88)
                elif BRUSH and spread is not None and i%4==2:
                    kit('hp',q,.64)  # the foot counts three while the hands brush and strike
                else:
                    kit('x' if s=='across the line' else 'rde' if s=='still owing' else 'h',q,.57 if i%4==0 else .47)
                snare_beats = (1,3) if s in ('still owing','across the line') else (2,)
                if i%4 in snare_beats:
                    kit('s',q,.96 if i%4!=1 else .83)
            if j==0 and s not in ('at par','called in'): kit('c',t,.83)
            if s in ('on account','across the line') and j==len(debts)-1:
                for off,pc in ((4,'t1'),(2,'t2'),(1,'ft')): kit(pc,t+pair-off,.76)
            t+=pair

    if STRIDE:
        hold = float(STRIDE)
        assert 0 < hold <= 1, 'C10T10_STRIDE must be a fraction of a step'
        # Read the last *pitched* stroke of the original riff on the bassist's
        # clock. A short palm stroke is not another note of the melody.
        def bass_pitch(pos, d, root):
            width = BAR+d
            back = pos>=width
            pat = REPLY if back else CALL
            local = (pos-width if back else pos)*BAR/(pair-width if back else width)
            semi = next(s for p,_,s,h in reversed(pat) if h!='m' and p<=local)
            return root+semi-(12 if back and semi>=12 else 0)

        marks = dict(sections)
        debts = dict(FORM)
        def clear(a,b):
            voices['bass'] = [n for n in voices['bass'] if not a/SUB <= n['at'] < b/SUB]

        # Three pairs on the maximum debt. Six does not divide 32, but it
        # divides 96: don't restart on each bar. Where a step would cover the
        # backwards guitar, let the breath last until the compressed reply.
        start = marks['still owing'] + 2*pair
        stop = start + 3*pair
        clear(start,stop)
        for at in range(start,stop,MAX_DEBT):
            j,pos = divmod(at-marks['still owing'],pair)
            d = debts['still owing'][j]
            if ADVANCE and j%2 and BAR<=pos<BAR+d: continue
            root = HOME+crest_roots[j]
            note('bass',at,MAX_DEBT*hold,bass_pitch(pos,d,root),.92)

        # On the way down each positive debt names a new stride: 6, 4, 2.
        # Let the previous step go before the pair ends. At zero stop counting;
        # the old bass part returns on the two guitarists' shared reply.
        repayment = debts['called in']
        for j,d in enumerate(repayment):
            base = marks['called in']+pair*j
            if d==0:
                # No gap left to count. Hold Eb, lift for one last two-tick
                # stride, then strike Gb with both players on the same beat.
                clear(base,base+BAR)
                note('bass',base,BAR-repayment[j-1],HOME,.93)
                break
            if d<0: break
            clear(base,base+pair)
            for pos in range(0,pair,d):
                note('bass',base+pos,min(d,pair-pos)*hold,bass_pitch(pos,d,HOME),.92)

    if ROOM:
        _,_,shift,foot = ROOM.split(';')
        where = dict(sections)
        quiet = lambda n: n['at']*SUB < where['in hand'] or where['two clocks'] <= n['at']*SUB < where['called in']
        midi = lambda name: NOTES.index(name[:-1])+12*(int(name[-1])+1)
        # Level-matched note by note to the bass guitar's own notes (K-weighted, each alone, raw): a plucked string
        # speaks hardest when it is short and when it is high. In dB: the two E flats under the sax; the pedals
        # A flat, G flat, E flat, E flat; the three notes of the fill (the last, on C, stays under its floor tom).
        trims = (-5,-5, -2.5,-1,0,0, -1.5,-4.5,-10)
        moved = sorted((n for n in voices['bass'] if quiet(n)), key=lambda n: n['at'])
        assert len(moved) == len(trims)
        for n,trim in zip(moved,trims):
            voices['room'].append({**n,'pitch':nm(midi(n['pitch'])+int(shift)),**({'gain':f'{trim:g}dB'} if trim else {})})
        voices['bass'] = [n for n in voices['bass'] if not quiet(n)]
        assert len(voices['room']) == 2+4+3
        if foot:
            early = [n for n in voices['kick'] if n['at']*SUB < where['in hand']]
            assert len(early) == 2
            voices['kick'] = [n for n in voices['kick'] if n not in early]
            voices['sweep'].extend({**n,'gain':f'{float(foot):g}dB'} for n in early)

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
    if BRUSH:
        tracks.append(track('sweep','brush-kit kit.sw.patch.synth.amp.a=28ms kit.sw.patch.synth.amp.r=32ms '
                            'play.humanize.time=0ms play.humanize.vel=0 fx.3.mix=0',
                            float(BRUSH),-.18,out='drums'))
    if ROOM:
        tracks.append(track('room',ROOM.split(';')[0],float(ROOM.split(';')[1]),.08))
    if BREATH:
        tracks.append(track('breath','bari-sax synth.amp.r=65ms fx.0.mix=0.075',float(BREATH),-.16,
                            auto={'tongue':{'points':air_points,'curve':0}},
                            fx=[{'type':'gain','gain':{'value':'0dB','mod':[{'src':'auto.tongue','amount':1}]}}]))
    if TRADE:
        tracks.append(track('bow','tagelharpa-bass-bowed synth.amp.r=80ms fx.0.mix=0.035',
                            float(TRADE),-.66,fx=['hp cutoff=120']))
    for name in fold_patches:
        tracks.append(track(name,name,float(ADVANCE),.66))
    if CHANGE:
        bronze = ('gamelan play.gate=1 play.humanize.time=0ms play.humanize.vel=0 '
                  'synth.amp.r=14ms synth.env.ring.r=16ms fx.0.mix=0')
        tracks.append(track('change',bronze,float(CHANGE),-.35))
    if PRESS:
        tracks.append(track('pressure','owing-skin',float(PRESS),.38,sends={'spring':'-20dB'}))
    if KEPT:
        level,shimmer = KEPT.split(';')
        # A sixteenth is a quarter of a beat: the tremolo is loudest on every
        # straight sixteenth from the top of the song, where each key starts.
        tracks.append(track('kept','owing-kept',float(level),-.35,
                            fx=[f'tremolo rate=0.25b depth={float(shimmer):g}']))
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
        'tempo':BPM,'seed':1,'event_stable':True,'length':f'{t//SUB}b','tail':'3s','loudness':ROOM_LUFS if ROOM else -10,'ceiling':'-1dB','true_peak':True,
        **({'songs':fold_sources} if fold_sources else {}),
        'patches':{'owing-key':key_patch,**fold_patches,**({'owing-skin':pressure_skin()} if PRESS else {}),
                   **({'owing-kept':kept_key()} if KEPT else {})},
        'buses':{'spring':{'fx':['reverb kind=spring drip=0.65 mix=1 decay=1.2s low_cut=350 predelay=18ms']},
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
