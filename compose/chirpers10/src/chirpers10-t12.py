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
# v9: per-note trim of the pedal hat that keeps counting under the last four strips.
FOOT_COUNT = '-3dB'
# Seventeen quiet seconds lower the song's integrated loudness by 0.15 LU. Ask for
# that much less, so the mastering gain on everything before the page is v8's.
PAGE_LOUDNESS = -10.15
# v10: the ribbon's one long note over the opposed guitars, against its track's level.
PALINDROME_TRIM = '-3dB'
# v11 (chirper-alpha, whole song): THE KIT GETS THE ALBUM'S EAR. The song had been read against the album's eleven
# records once, at v1, on one stretch (+3.3 dB at 250-500 Hz, 2.4 short at 60-120), and nothing was done. Read whole
# and by part at v10 (stembal, each band as a share of the mix, against the records' passages without a voice): every
# stretch with a backbeat stood 2.6 to 6.1 dB over at 250-500 Hz (the unison opening 1.2) and 1.7 to 3.1 short at
# 60-120 Hz. Part by part, the SNARE held half of 250-500 Hz wherever it plays two and four, and the kick most of the
# rest; the kick is also 56 to 77% of 60-120 Hz. Every other song of the album that uses this kit cuts its bus at
# 400 Hz (4 to 6 dB); this one, alone, did not. So the drums' bus gets the album's eq, after its clip: the cut at
# 400 Hz, the small lift at 5.5 kHz and the shelf over 9 kHz as Common Time's kit has them, and one band of its own:
# a lift at 92 Hz, because here the foot plays only the four open notes of a strip and the bass only two, so the
# low end is few strokes and each has to carry more. No note changes.
# (Benched: the same lift on the kick's own track, before the bus's compressor and clip, bought 0.5 dB of the band
# for 3 dB of eq; on the bus after them 3 dB buys 1.0. At 4.5 dB the tuned toms' answers at 3:36 read 1.4 over.)
KIT_EQ = ['peak cutoff=92 q=1.2 gain=3.5dB', 'peak cutoff=400 q=0.8 gain=-6dB', 'peak cutoff=5500 q=0.9 gain=1dB', 'highshelf cutoff=9000 gain=-2dB']
# With the snare's body out of the way the ribbon's long note (v10, mine) was nearly all of its own octave (1.0 dB
# under the mix there) and that stretch still read 4.1 over. Two dB less: 14.7 under the whole mix, where the
# signature at the close stands (14.1), and still the strongest partial near it in nine frames of ten.
PALINDROME_TRIM_KIT = '-5dB'
# v12: the steel's notes on the four strips on C. A fifth up, all four of its notes lie inside 250-500 Hz, where it
# already held three quarters of the band: at its own level those strips read 7.6 dB over the eleven records there
# (6.3 on F) and the steel stood 0.6 dB further forward against the band (K). With this trim on each of those notes
# the band reads what it read on F.
STEEL_ON_C = '-1.5dB'
# v13 (chirper-three, palette): THE THUMBPRINT IS LEFT BY THUMBS. In 'thumbprint' (1:49.6-2:17.0) a wordless voice
# calls and a clean guitar answers with the same four notes read from the other end; nothing else plays until two
# toms join half way. The answer moves from the clean guitar (ct-clean, a staple of six songs here) to a THUMB
# PIANO: the library's kalimba, on no other song of the record. Same forty notes at the same times and
# velocities, two octaves up, where a kalimba lives (A-flat 4 to E-flat 5): the answer was an octave under the
# voice and is now an octave over it, and where the voice climbs for two strips (2:06-2:11.5) they share an octave.
# And it is played as the instrument is: two thumbs, the tines laid out alternately left and right as they rise
# (A-flat left, A right, B left, E-flat right), a track to a thumb. So the tune read forwards is LEFT, LEFT, RIGHT,
# RIGHT and read backwards RIGHT, RIGHT, LEFT, LEFT: turning the strip over swaps the hands. The song's other thumb
# is the bass player's (from 1:06, on its card); this is the section its name was waiting for. The clean guitar
# still opens the song, rings the fold's F and closes the page.
# (Benched, raw seed 0. FIRST: the same notes at the guitar's own pitch (A-flat 2 to E-flat 3): a kalimba down there
# is nearly a pure fundamental at 104-156 Hz, a soft bass and not a tine, and at -2 dB it was 20 dB over the guitar
# it replaced. An octave up it stood in the voice's own octave. KEPT, two octaves up at -23.5 dB: alone it is within
# 1.1 dB of the guitar (K, first 150 ms of each note) and the voice stands 8.6 dB over it where it stood 8.3 over
# the guitar. The tine's overtone is lifted 8 dB: 12 to 18 dB under the fundamental in a note's first 30 ms, where
# the library's is 20 to 26. The section loses the guitar's pick: -1.2 dB at 2-4 kHz and -2.7 at 4-8 kHz; every
# band under 2 kHz is within 0.6 dB.)
# the patch (the song's chamber in place of its own room ; each tine rings 0.6 s after the thumb leaves it ; the
# overtone's level) ; each thumb's track gain ; how far each sits from centre ; semitones over the guitar's notes.
TINES = ('kalimba fx.0.mix=0 synth.amp.r=600ms synth.layers.2.level.value=-18dB', '-23.5dB', .4, 24)
# With the swap the song reads 0.007 LU louder to the meter, so at v12's target every other bar came out 0.004 to
# 0.010 dB quieter (seeds 0 and 11). Ask for that much more.
THUMBS_LOUDNESS = -10.143
# v14 (chirper-alpha, palette): THE CARBON IS TAKEN ON A SECOND AMP. 'Carbon' (1:27.7-1:49.6) is one guitarist and
# eight strips, and it has always gone page, copy, page, copy: on the first strip of each pair the hand plays the
# whole strip, on the second only its four open notes, the strokes that were pressed hard enough to go through (the palm
# strokes do not transfer), while the drummer's tuned heads take over the voice's words. But page and copy were
# the same sound: the same saturated amp, which presses every stroke alike. Now the copy is taken on a second amp
# from the same guitar and the same cabinet: a clean one, short of breaking up. The four notes of each odd strip
# move to it (sixteen notes; nothing added, nothing moved). On it a stroke shows its pressure: the note speaks,
# then falls, where the ink holds level; it is fainter and has no fizz. The page strips, the voice, the heads,
# the bass and the foot are as they were. It is the song's first clean electric note that is not the high clean
# guitar's: 'thumbprint', all clean, follows. (The clean voicing is on this record otherwise only inside ct-glass,
# in three other songs.)
# (Benched, raw seed 0, the sixteen notes alone. Turning the ink amp down does nothing: at gain 0.3 without its
# boost, or on the crunch voicing at 0.5, the notes read within 0.4 dB, 30 Hz of centroid and 0.3 dB of crest of
# the ink: the compressor and screamer in front keep it saturated. The clean voicing at 0.6: centroid 2110 ->
# 1770 Hz, 1.4 dB less of its power over 2 kHz, crest 12.5 -> 15.5 dB, and the second half of each note 3.3 dB
# under the first where the ink's is 1.0 under. At 0.35 it is a bare pick (crest 17.9); with the microphone moved
# off the cone it goes dull (1360 Hz). Kept: 0.6, on the ink's own cone. At the ink's own fader the clean notes
# read 5.3 dB under it (K); at 3.8 dB they stand 2.0 under: a copy is fainter, but it has to read.)
# the amp ; the copy's track gain.
COPY = ('ct-twin fx.1.model=clean fx.1.gain=0.6 fx.1.boost=0dB fx.2.cone=37', '3.8dB')
# The copy strips are quieter to the meter (the fizz is most of what it hears), so at v13's target every other bar
# came out 0.042 dB louder (seed 0). Ask for that much less.
COPY_LOUDNESS = -10.185
# v15 (chirper-alpha): HARRY'S THREE ANSWERS, 19 Nov 02:31, and the guitars.
# (1) 'Can you follow the ringing line as it changes hands?' (the pedal steel in 'turn over', my v2; asked at v11
# beside the same bars with the steel taken out): "Prefer both heavy". So in 'turn over' (2:49.9-3:22.8) the hand
# reading back is a heavy guitar again, as it was in v1: both hands heavy, one reading the strip forwards and one
# back, changing chairs on every strip. The steel is out of the song. v12's move to C on the last four strips
# stands, now on both guitars. --with-steel gives v14.
# (2) 'Do the bass pops help you follow the two guitars?' -> "Keep the pops": kept. (3) 'Can you follow both
# guitars when one turns back?' -> "I can follow both": kept.
HEAVY_LOUDNESS = -10.185
# THE TWO HANDS' RIG (the round was drawn as an instrument round; Harry, 19 Nov: "better guitars"). With both hands
# heavy the song is two guitars from end to end, and against the album's eleven records its guitar stretches all
# read the same way (finished file, each band as a share of the mix): 500 Hz-1 kHz 1.6 to 2.0 dB short, 2-4 kHz 2.2
# to 2.7 over, 4-8 kHz 0.6 to 1.4 short. In those stretches the two guitars ARE those bands (raw, 'ink': within 0.8
# dB of the whole mix from 500 Hz to 4 kHz, two thirds of 4-8 kHz), so it is the rig: a honk at 3 kHz with too
# little body under it and too little edge over it. Three changes, each benched on the guitars alone and then read
# in the mix:
#   the amp     the album's own voicing (`gojira`, as tracks 4, 7, 8, 9, 14 and 15 have it): +1.5 dB at 500 Hz-1 kHz,
#               -3.2 at 120-250 and -1.7 at 250-500 (the boxiness under the body)
#   the mic     nearer the cone's centre (0.4 -> 0.25): +1.8 dB at 4-8 kHz. (The album's usual 0.5 goes the other
#               way: benched, it cost this song a further 1.1 dB there.)
#   the honk    one cut at 2.6 kHz after the cabinet: 2-4 kHz -1.5 dB net of the brighter mic
#   THE FADERS STAY where they were. The pair alone reads 1.07 dB quieter on the new rig; a first take gave that
#   back at the fader and the mix read worse for it (2-4 kHz only 0.5 dB better, and the stretches were already
#   1 to 2.5 dB short at 60-120 Hz, which is the kit and bass the guitars stand over).
# Not kept: the amp's presence at 0.7 (0.1 dB); treble 0.35 (took 4-8 kHz down with 2-4); a shelf over 5 kHz
# (the cut under it ate it). The second amp of 'carbon' (the copy) is not touched. --stock-rig keeps the old rig.
HANDS_RIG = ('fx.1.model=gojira fx.2.mic=0.25', None, ['peak cutoff=2600 q=1.4 gain=-3.5dB'])

# v16 (chirper-one, section w7, 2:55.4-3:06.3): THE PAGE IS TURNED OVER. The song reads its strip from both ends; it
# had never turned it upside down. In 'turn over', after the first pair of strips, the page is turned top to bottom
# for two pairs (four strips): every open chord stands as far BELOW the low F as it stood above it, brought up an
# octave so it stays on the neck. A flat (a minor third up) becomes D (a minor third down), G flat (a semitone up)
# becomes E (a semitone down), C (a fifth up) becomes B flat (a fifth down). The rhythm, the palm strokes, the
# chairs, the bass's F and the kit are as written; both hands are heavy, as Harry chose. What turns is the colour:
# the strip's F, A flat, G flat, C is the dark side of F; F, D, E, B flat is its bright side. Where the two hands
# meet (ticks 3 and 15) they used to make A flat major seventh over the bass's F; turned over they make B flat
# major seventh over it. Then the page is turned back for the last pair on F, whose closing C is left ringing and
# becomes the ground (v12), and the section ends on C as before. A crash marks each turn of the page.
# The strips of 'turn over' read upside down (first, one past the last) ; the crash's velocity on each turn (0: no
# crash) ; the loudness target. --without-turned-page gives v15.
TURNED = (2, 6, 0.8, -10.185)


def pitch(m): return PITCH[m % 12] + str(m // 12 - 1)
def strip(back=False):
    return sorted(((STRIP-1-t if back else t), p, k) for t,p,k in ROW)

def build(drum_hand=True, crease=True, mirror_bass=True, picking_hand=True, signature=True, ties=True, facing=True, palindrome=True, album_kit=True, dominant=True, thumbs=True, copy=True, heavy=True, turned=True, rig=HANDS_RIG):
    crease = crease and drum_hand  # --without-drum-hand still reproduces v2
    mirror_bass = mirror_bass and crease  # --without-crease still reproduces v3
    picking_hand = picking_hand and mirror_bass  # --without-mirror-bass still gives v4
    signature = signature and picking_hand       # --without-picking-hand still gives v5
    ties = ties and signature                    # --without-signature still gives v6
    facing = facing and ties                     # --without-ties still gives v7
    palindrome = palindrome and facing           # --without-facing-page still gives v8
    album_kit = album_kit and palindrome         # --without-palindrome still gives v9
    dominant = dominant and album_kit            # --without-album-kit still gives v10
    thumbs = thumbs and dominant                 # --without-dominant still gives v11
    copy = copy and thumbs                       # --without-thumbs still gives v12
    heavy = heavy and copy                       # --without-carbon-copy still gives v13
    rig = rig if heavy else None                 # --with-steel still gives v14
    turned = turned and heavy and rig is not None  # --stock-rig is v15's notes on the old rig
    ev = defaultdict(list); sections = []; tie_gains = {}; start = 0
    def put(tr, t, n, dur, v, mute=False, **expr):
        e = {'at':round(t/GRID, 5), 'len':round(dur/GRID, 5), 'pitch':pitch(n) if isinstance(n,int) else n, 'vel':v}
        if mute: expr['pm'] = 1
        if expr: e['expr'] = expr
        ev[tr].append(e)
    def kit(tr,t,p,v): put(tr,t,p,3.8 if p in ('c','x','rde') else 1.15,v)
    def chord(root): return pitch(root)+','+pitch(root+7)
    front,back = strip(),strip(True)
    opens = [{t:p for t,p,k in r if k=='o'} for r in (front,back)]
    # The right picking hand tries the reflection before the fretted tune does.
    # The nearest three palm strokes move first; then all five move, twice.
    # Recompute the gaps from each new row: an early mute chokes the open note.
    by_centre = sorted((t for t,_,k in front if k=='m'), key=lambda t: abs(2*t-(STRIP-1)))
    def turn_mutes(how_many):
        move = set(by_centre[:how_many])
        r = sorted((STRIP-1-t if t in move else t, p, k) for t,p,k in front)
        assert len({t for t,_,_ in r}) == len(r)
        return r
    meetings = sorted(opens[0].keys() & opens[1].keys())
    assert meetings == [3,15]
    # Immediately inside the shared attacks is a reflected pair of gaps.
    # Neither guitar picks at 4 or 14. Leave the silent centre, tick 9, alone.
    gaps = [meetings[0]+1, meetings[1]-1]
    assert sum(gaps) == STRIP-1 and set(gaps).isdisjoint(t for t,_,_ in front+back)
    taps = (2,7,13,17)
    assert set(taps) <= {t for t,_,k in front if k=='m'}
    for sec,count in FORM:
        sections.append((sec,start,count))
        for i in range(count):
            a = start + i*STRIP
            slapping = mirror_bass and sec == 'opposite' and i >= count//2
            # F all through the introduction and first traversal. The quiet centre
            # moves to its minor third; the high answer alone bends on the way home.
            root = 29 + (3 if sec in ('carbon','thumbprint') else 1 if sec=='raised' and i<count//2 else 0)
            # v12: THE FOURTH NOTE IS A GROUND. The strip has four open notes:
            # F, A-flat, G-flat, C. The song has stood on the first three, in
            # that order (F; A-flat from 'carbon'; G-flat in 'raised'), and
            # never on the fourth. The last four strips of 'turn over' move up
            # to C. The forward hand's last open chord in a strip IS C: on the
            # strip before, it is left ringing (its closing palm stroke is not
            # played) and becomes the ground. And 'one hand' begins on C: read
            # from the far end, the strip's first open chord is that same C,
            # and it comes down C, G-flat, A-flat, F. So the form reads the
            # strip forwards, a ground at a time, before the signature reads
            # it backwards in four chords.
            lifted = dominant and sec=='turn over' and i >= count-4
            if lifted: root += dict((t,p) for t,p,k in ROW if k=='o')[max(t for t,p,k in ROW if k=='o')]
            pivot = dominant and sec=='turn over' and i == count-5
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
                    for t,p in opens[1-i%2].items():
                        # v13: the answer is a thumb piano's; the tines alternate sides as they rise
                        side = ('left','right')[sorted(opens[0].values()).index(p) % 2]
                        put('tines-'+side if thumbs else 'wire',a+t,root+12+p+(TINES[3] if thumbs else 0),2.6,.86)
                    if i>=count//2:
                        for t in (3,15): kit('skins',a+t,'ft' if t==3 else 't1',.71)
                continue
            rightback = sec in ('opposite','carbon','raised') or (sec=='turn over' and i%2==0)
            leftback = sec=='turn over' and i%2==1 or sec=='one hand'
            for tr,rev in [('left',leftback),('right',rightback or sec=='one hand')]:
                # Carbon is one guitarist with a delayed memory, not a stereo solo.
                if sec=='carbon' and tr=='right': continue
                if sec=='ink' and i<4 and tr=='right': continue
                if sec=='turn over' and rev and not heavy:
                    # (v2 to v14) The hand reading back picks up a volume steel. First hold just
                    # the two meeting notes (C, Ab); then fill in the reflected tune.
                    # The other hand still chugs. Swap chairs on every new strip.
                    stops = [t for t in sorted(opens[1]) if i>=4 or t in (3,15)]
                    end = 10 if i==count-1 else STRIP
                    stops = [t for t in stops if t<end]
                    for j,t in enumerate(stops):
                        until = stops[j+1] if j+1<len(stops) else end
                        put('steel-'+tr,a+t,root+24+opens[1][t],until-t-.12,.87)
                        if lifted: ev['steel-'+tr][-1]['gain'] = STEEL_ON_C
                    continue
                r = back if rev else front
                if picking_hand and sec=='ink' and tr=='right':
                    lap = i - count//2
                    if 0 <= lap < 3:
                        r = turn_mutes((len(by_centre)+1)//2 if lap==0 else len(by_centre))
                last_open = max(t for t,_,k in r if k=='o')
                for j,(t,p,k) in enumerate(r):
                    if not inside(t): continue
                    if pivot and t > last_open: continue     # v12: nothing damps the C that is about to be the ground
                    if tom_reply and not (i==count-1 and t==STRIP-1): continue
                    if sec=='one hand' and k=='m' and (i>=4 or t%2): continue
                    if sec=='carbon' and k=='m' and i%2: continue
                    if sec=='turn over' and i==count-1 and t>=10: continue
                    gap = (r[j+1][0] if j+1<len(r) else STRIP)-t
                    if pivot and t == last_open: gap = STRIP-t
                    dur = .64 if k=='m' else min(gap-.23, 3.45)
                    n = root+p
                    if turned and sec=='turn over' and TURNED[0] <= i < TURNED[1]:
                        n = root+(12-p)%12       # v16: the page upside down
                    if picking_hand and sec=='ink' and tr=='right' and k=='m' and t not in by_centre:
                        # The travelling strokes are up-picks. Keep them short,
                        # but lift the palm a little so they cut through the note
                        # still ringing on the left. Ordinary down-picks stay put.
                        put(tr,a+t,n,dur,.84,pm=.55,up=1)
                    else:
                        # v14: an odd strip of 'carbon' is the copy, and it is taken on the second amp
                        amp = 'copy' if copy and sec=='carbon' and i%2 else tr
                        assert amp==tr or (tr=='left' and k=='o')
                        put(amp,a+t,chord(n) if k=='o' and sec in ('raised','turn over','one hand') else n,dur,.94 if k=='o' else .79,k=='m')
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
                            put('thumb' if slapping else 'bass',a+t,root+(0 if apart else p),3 if apart else 1.7,.92)
                        kit('foot',a+t,'k',.98 if t in (0,3,15,18) else .83)
                if slapping:
                    # Pop AFTER the first thumb and BEFORE its reflection. First
                    # quote the forward guitarist's pitches, then the other's.
                    lap = i - count//2
                    source = opens[int(lap >= (count-count//2)//2)]
                    for j,(cross,gap) in enumerate(zip(meetings,gaps)):
                        if j == 1 and lap < 2: continue
                        # A-flat is the next section's ground. The last two
                        # pickups ring across the low F to point the way to it.
                        dur = .83
                        if j == 1 and i >= count-2:
                            dur = STRIP-gap-.4 if i == count-1 else 2.5
                        put('thumb',a+gap,root+12+source[cross],dur,.78 if j==0 else .72,pop=1)
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
            if turned and sec=='turn over' and i in TURNED[:2] and TURNED[2]: kit('brass',a,'c',TURNED[2])
        start+=count*STRIP
    if ties:
        # At each key change the two transpositions of this four-note hook
        # share just one pitch class. Keep it sounding: third -> root at
        # carbon, flat second -> minor third at raised. No new clock or patch.
        marks = {name:t for name,t,_ in sections}
        def bridge(section, old_root, new_root):
            outgoing = {(old_root+v)%12:t for t,v in opens[1].items()}
            incoming = {(new_root+v)%12:t for t,v in opens[1].items()}
            pc, = outgoing.keys() & incoming.keys()
            seam = marks[section]
            return seam-STRIP+outgoing[pc], seam+incoming[pc], pc
        tick = lambda n: round(n['at']*GRID)
        a,b,pc = bridge('carbon',29,32)
        pop = next(n for n in ev['thumb'] if tick(n)==a-1)
        vowel = next(n for n in ev['mouth'] if tick(n)==b)
        assert pop['pitch']==pitch(36+pc) and vowel['pitch']==pitch(48+pc)
        ev['right'] = [n for n in ev['right'] if not a<=tick(n)<b]
        put('right',a,pop['pitch']+','+vowel['pitch'],b-a-.3,.90)
        # The saturated rig doesn't decay like the popped string. Let it
        # withdraw across the quieter strip rather than stay as loud as the riff.
        tie_gains['right'] = [(marks['carbon'],0),(b-.3,-8),(b+GRID,-8),(b+2*GRID,0)]

        a,b,pc = bridge('raised',32,30)
        vowel = next(n for n in ev['mouth'] if tick(n)==a)
        assert vowel['pitch']==pitch(48+pc)
        ev['mouth'] = [n for n in ev['mouth'] if not a<tick(n)<=b]
        vowel['len'] = round((b-a-.3)/GRID,5)
        seam = marks['raised']
        # The same mouth is exposed before this seam and inside two amps
        # after it. Open its fader only while it is carrying A through the band.
        tie_gains['mouth'] = [(seam,0),(seam+GRID,3),(b-.3,3),(b+1,0)]
        next_open = seam+min(t for t in opens[1] if t>b-seam)
        # The upper sound still belongs to the vowel: single low strings on
        # the right until that player catches its A3, then let that octave
        # ring to the closing G-flat without the intervening palm stroke.
        for n in ev['right']:
            t = tick(n)
            if seam<=t<b and t-seam in opens[1]: n['pitch']=n['pitch'].split(',')[0]
            if t==b:
                n['pitch']=n['pitch'].split(',')[0]+','+vowel['pitch']
                n['len']=round((next_open-b-.3)/GRID,5)
        ev['right'] = [n for n in ev['right'] if not b<tick(n)<next_open]
    if signature:
        # The mouth teaches its last opening strip to a ribbon instrument. The
        # same hand signs forwards against the guitars' backward cadence.
        _, p0, strips = next(s for s in sections if s[0]=='pencil')
        learn = p0 + (strips-1)*STRIP
        def lesson(n): return learn <= round(n['at']*GRID) < learn+STRIP
        taught = [n for n in ev['mouth'] if lesson(n)]
        tune = [p for _,p in sorted(opens[0].items())]
        assert len(taught) == len(tune)
        ev['ribbon'] = [{**n, 'pitch':pitch(29+36+p)} for n,p in zip(taught,tune)]
        ev['mouth'] = [n for n in ev['mouth'] if not lesson(n)]
        _, sign, _ = next(s for s in sections if s[0]=='signed')
        stabs = [n for n in ev['right'] if n['at']*GRID >= sign]
        assert len(stabs) == len(tune)
        for j,(n,p) in enumerate(zip(stabs,tune)):
            tick = round(n['at']*GRID)
            # Keep the right guitarist's low string for its original length;
            # the fifth, not the weight, goes to the answering instrument.
            n['pitch'] = n['pitch'].split(',')[0]
            dur = round(n['len']*GRID)
            put('ribbon',tick,29+36+p,dur,.84 if j==len(tune)-1 else .85)
            if j == len(tune)-1:
                # Slide C5 down to F4 at the fold without a second note-on.
                curve = []
                for t in range(dur+1):
                    u = max(0.,min(1.,(t-(STRIP//2-GRID))/GRID))
                    curve.append(round((tune[0]-p)*u*u*(3-2*u),4))
                ev['ribbon'][-1]['expr_path'] = {'ribbon':curve}
    if palindrome:
        # THE LINE BOTH HANDS MAKE. Read from opposite ends, the two guitars'
        # open notes add up to something neither plays: F, C over A-flat,
        # G-flat, G-flat, C over A-flat, F. Its top is the same from either
        # end. The ribbon, which learned the tune forwards and will sign it at
        # the close, draws that top once without lifting: it is on each note
        # when a guitar strikes it and holds G-flat across the silent centre,
        # from the right hand's G-flat to the left's. Four strips, the second
        # half of the plain opposition; it stops where the thumb starts.
        _, opp, strips = next(s for s in sections if s[0]=='opposite')
        first, laps = strips//4, strips//4
        top = {t:max(opens[0].get(t,-1), opens[1].get(t,-1)) for t in opens[0].keys()|opens[1].keys()}
        assert [top[t] for t in sorted(top)] == [0,7,1,1,7,0] and all(top[t]==top[STRIP-1-t] for t in top)
        # It stays on C for two ticks on the inner side of each meeting, on
        # G-flat between the two hands' G-flats, and on F from a tick before
        # the strip's last note to a tick after the next strip's first.
        # Between those, a straight slide: so the drawn line is its own mirror.
        centre, hold = STRIP//2, []
        for t,v in sorted(top.items()):
            if t in meetings: hold += [(t,v), (t+(2 if t<centre else -2), v)]
            elif t in (0, STRIP-1): hold.append((1 if t==0 else STRIP-2, v))
            else: hold.append((t,v))
        hold = [(-2, top[STRIP-1])] + sorted(hold) + [(STRIP+1, top[0])]
        def at(t):
            for (a,va),(b,vb) in zip(hold, hold[1:]):
                if a <= t <= b: return va + (vb-va)*(t-a)/(b-a)
        strip_curve = [round(at(t),4) for t in range(STRIP)]
        assert all(strip_curve[t]==strip_curve[STRIP-1-t] for t in range(STRIP))
        assert all(strip_curve[t]==v for t,v in top.items())
        begin = opp + first*STRIP
        put('ribbon', begin, 29+36, laps*STRIP, .85)      # it lets go on the thumb's first strip
        # The engine reaches point k of a path at (k+1)/N of the note (benched:
        # with a point for each tick AND one for the end, the first strip ran a
        # tick late and the last a quarter). So N is the note's ticks, and
        # point k is where the line should be at tick k+1.
        ev['ribbon'][-1]['expr_path'] = {'ribbon': (strip_curve*laps + [strip_curve[0]])[1:]}
        # An unbroken tone over single-string riffs carries further than the
        # same fader does over the closing chords: at the track's level it stood
        # 9.8 dB under the band, where the signature stands 14.1 under.
        ev['ribbon'][-1]['gain'] = PALINDROME_TRIM_KIT if album_kit else PALINDROME_TRIM
    if facing:
        # THE FACING PAGE. Close a book on wet ink and the other page takes its
        # mirror image. The song's first six strips (the pencil's four, then
        # the left guitar's first two in ink) are read from the far end by the
        # other hand. Six, because then the backward reading's last note, F,
        # is the only strip ending that falls on the drummer's ONE: bar 109.
        mirrored = 6
        page = start
        last = page + mirrored*STRIP - 1
        assert last % (4*GRID) == 0 and [n for n,_,c in sections[:2]] == ['pencil','ink'] and sections[0][2] == 4
        sections.append(('facing page', page, mirrored))
        for j in range(mirrored):
            a = page + j*STRIP
            source = mirrored-1-j           # the opening strip this one reflects
            for t in range(a, a+STRIP):
                if t%GRID: continue
                beat = t//GRID
                if source >= 4:             # ink's count: a hat in quarters, the snare on three
                    kit('hat',t,'h',.65 if beat%4==0 else .48)
                    if beat%4==2: kit('snare',t,'s',.94)
                else:                       # the sticks are down; the foot goes on counting
                    kit('hat',t,'hp',.5 if beat%4==0 else .4)
                    ev['hat'][-1]['gain'] = FOOT_COUNT
            if source >= 4:
                # Ink began with the left hand alone, forwards, and a crash on
                # its first note. The right hand alone, backwards, ends on it.
                for i,(t,p,k) in enumerate(back):
                    gap = (back[i+1][0] if i+1<len(back) else STRIP)-t
                    dur = .64 if k=='m' else 3.45 if source==4 and t==STRIP-1 else min(gap-.23, 3.45)
                    put('right',a+t,29+p,dur,.94 if k=='o' else .79,k=='m')
                for t,p in opens[1].items():
                    put('bass',a+t,29+p,1.7,.92); kit('foot',a+t,'k',.98 if t in (0,3,15,18) else .83)
                if source == 4: kit('brass',a+STRIP-1,'c',.88)
                continue
            if source >= 2:                 # the clean guitar answered backwards; now it leads, forwards
                for t,p in opens[0].items(): put('wire',a+t,29+12+p,2.4,.82)
            for t,p in opens[1].items():    # ribbon, then the mouth: C, G-flat, A-flat, F
                if source == 3: put('ribbon',a+t,29+36+p,2.4,.78)
                else: put('mouth',a+t,29+24+p,2.4,.78)
        # The song began with a short F on the one. It ends on the same F, held.
        ev['mouth'][-1]['len'] = round(8/GRID,5)
        assert round(ev['mouth'][-1]['at']*GRID) == last
        start = last + 8
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
    for tr in tracks:
        if tr['name'] in tie_gains:
            tr['gain']={'value':tr['gain'],'mod':[{'src':'auto.carry','amount':1}]}
            pts=[['0b',0]]+[[f'{t/GRID:g}b',db] for t,db in tie_gains[tr['name']]]
            tr['auto']={'carry':{'points':pts,'curve':0}}
    if mirror_bass:
        # Let the upper string ring without choking the low thumb. Same bass
        # bus as the picked part; no low-octave double or added kick.
        tracks.append(track('thumb','slap-bass play.mono=false','-4.5dB',0,'low'))
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
        if not heavy: tracks.append(track('steel-'+side,steel,'-5.5dB',pan,'strings'))
    assert heavy == (not ev['steel-left'] and not ev['steel-right'])
    if rig:
        for t in tracks:
            if t['name'] in ('left','right'):
                t['patch'] = t['patch'].replace('ct-twin ', 'ct-twin '+rig[0]+' ')
                if rig[1] and isinstance(t['gain'], dict): t['gain']['value'] = rig[1]   # the right hand's fader has a lane (v7's ties)
                elif rig[1]: t['gain'] = rig[1]
                if rig[2]: t['fx'] = [{'type':'eq','bands':rig[2]}]
    if thumbs:
        for side,way in [('left',-1),('right',1)]:
            tracks.append(track('tines-'+side,TINES[0],TINES[1],way*TINES[2],fx=room))
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
    if signature:
        patch = {'extends':'ondes synth.amp.r=90ms fx.0.mix=0.1 fx.0.decay=1.1s fx.1.mix=0.04 fx.1.decay=0.8s',
                 'synth':{'pitch':{'value':0,'mod':[{'src':'lfo.vib','amount':.13},{'src':'expr.ribbon','amount':1}]}}}
        ribbon = track('ribbon',patch,{'value':'-14.5dB','mod':[{'src':'auto.sign','amount':-1.5}]},
                       {'value':-.2,'mod':[{'src':'auto.sign','amount':.78}]})
        ribbon['auto'] = {'sign':{'points':[['0b',0],[f'{(learn+STRIP)/GRID:g}b',0],[f'{sign/GRID:g}b',1]],'curve':0}}
        if facing:
            # Back beside the mouth, at its first level, to hand the tune home.
            ribbon['auto']['sign']['points'] += [[f'{page/GRID:g}b',1],[f'{(page+2*STRIP)/GRID:g}b',0]]
        tracks.append(ribbon)
    if copy:
        # The same guitar, the same chair and the same cabinet as the left hand; only the amp differs.
        left = next(t for t in tracks if t['name']=='left')
        tracks.append(track('copy',COPY[0]+palm,COPY[1],left['pan'],'strings'))
    buses={'strings':{'fx':[{'type':'eq','bands':['peak cutoff=360 q=0.8 gain=-2dB','peak cutoff=730 q=1 gain=1.5dB']}]},
           'drums':{'fx':['reverb kind=room mix=0.10 decay=0.53s predelay=7ms',{'type':'glue','threshold':'-22dB','ratio':2.5,'attack':'18ms','release':'120ms'},'clip ceiling=-13dB']},
           'low':{'fx':[{'type':'eq','bands':['peak cutoff=48 q=1.4 gain=-4dB','peak cutoff=98 q=1 gain=3dB','peak cutoff=310 q=0.9 gain=-4dB']},{'type':'compressor','threshold':'-24dB','ratio':5,'attack':'14ms','release':'115ms'}]}}
    if album_kit: buses['drums']['fx'].append({'type':'eq','bands':KIT_EQ})
    doc=dict(about='The Other Hand — chirpers, Common Time, track twelve. One strip of attacks read forwards and back under an unbroken count of four.',tempo=BPM,seed=1,length=f'{start/GRID:g}b',tail='1.3s',ceiling='-1dB',loudness=(HEAVY_LOUDNESS if heavy else COPY_LOUDNESS if copy else THUMBS_LOUDNESS if thumbs else PAGE_LOUDNESS) if facing else -10,event_stable=True,buses=buses,master={'fx':[{'type':'eq','bands':['hp cutoff=24']},'gain gain=2dB']},tracks=tracks)
    return doc,sections

def dump(d):
    return '\n'.join('tracks:\n'+'\n'.join('  - '+json.dumps(t) for t in v) if k=='tracks' else k+': '+json.dumps(v) for k,v in d.items())+'\n'

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('-o','--out',type=Path,default=OUT); ap.add_argument('--map',action='store_true'); ap.add_argument('--without-drum-hand',action='store_true',help='regenerate v2'); ap.add_argument('--without-crease',action='store_true',help='regenerate v3')
    ap.add_argument('--without-mirror-bass',action='store_true',help='regenerate v4')
    ap.add_argument('--without-picking-hand',action='store_true',help='regenerate v5')
    ap.add_argument('--without-signature',action='store_true',help='regenerate v6')
    ap.add_argument('--without-ties',action='store_true',help='regenerate v7, without the two common-tone handoffs')
    ap.add_argument('--without-facing-page',action='store_true',help='regenerate v8, ending on the signed chord')
    ap.add_argument('--without-palindrome',action='store_true',help='regenerate v9, without the ribbon over the opposed guitars')
    ap.add_argument('--without-album-kit',action='store_true',help="regenerate v10, the kit's bus without the album's eq")
    ap.add_argument('--without-dominant',action='store_true',help="regenerate v11, 'turn over' on F throughout")
    ap.add_argument('--without-thumbs',action='store_true',help="regenerate v12, the clean guitar answering the voice in 'thumbprint'")
    ap.add_argument('--without-carbon-copy',action='store_true',help="regenerate v13, the copy strips of 'carbon' on the ink's own amp")
    ap.add_argument('--with-steel',action='store_true',help="regenerate v14, the pedal steel reading back in 'turn over'")
    ap.add_argument('--without-turned-page',action='store_true',help="regenerate v15, 'turn over' read the right way up throughout")
    ap.add_argument('--stock-rig',action='store_true',help="v15's notes on the two hands' rig as it was up to v14 (not a version)"); a=ap.parse_args()
    doc,sections=build(not a.without_drum_hand,not a.without_crease,not a.without_mirror_bass,not a.without_picking_hand,not a.without_signature,not a.without_ties,not a.without_facing_page,not a.without_palindrome,not a.without_album_kit,not a.without_dominant,not a.without_thumbs,not a.without_carbon_copy,not a.with_steel,not a.without_turned_page,None if a.stock_rig else HANDS_RIG)
    if a.map:
        for sec,t,n in sections: print(f'{sec:12s} {t/GRID*60/BPM:6.2f}s — {(t+n*STRIP)/GRID*60/BPM:6.2f}s')
    else: a.out.write_text(dump(doc))
