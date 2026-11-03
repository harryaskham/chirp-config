#!/usr/bin/env python3
"""chirpers8-t10 (chirper-one): "Call and Return" - for chirpers VIII ('A Light Left On'), the ode to computer music.

An ELECTRO FUGUE MACHINE. A subject (eight bars over a four-bar loop, i - VI - iv - V) is written so that it can sound
against itself four bars later: a canon. Four machine voices take it in turn - an FM bell, a hard-synced lead, a
PWM wavetable pulse and an FM bass - over a motorik drum machine. Then the machine starts CALLING: a seeded grammar
pushes and pops a call stack every four bars, and every level on the stack spawns a faster copy of the current bar
an octave higher (sixteenths, then thirty-seconds, then sixty-fourths that blur into a shimmer), so the texture's
density follows the stack's depth; RETURNS take them away again. The canon modulates - D minor, G minor, A minor and
home - and the whole track is tuned in WERCKMEISTER III, a well temperament, so every key has its own colour, the
way the keyboards that first played fugues did. Before the end the stack empties (the subject alone, augmented, on
the bell), then fills to the top and unwinds to nothing.
Form (bars): intro 8 / exposition 16 / calls 32 (D minor) / calls 24 (G minor) / calls 24 (A minor) / return 8 /
final 32 (D minor) / outro 8 = 152 bars at 120 bpm (5:04).
Emits songs/chirpers8-t10.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, math, os, random, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers8-t10.yaml")
BPM = 120.0
SEED = 1010

# Werckmeister III, cents from equal temperament for each pitch class (C = 0)
W3 = [0.0, -9.8, -7.8, -5.9, -9.8, -2.0, -11.7, -3.9, -7.8, -11.7, -3.9, -7.8]
def tok(m):
    while m > 108: m -= 12          # fold the stack's highest copies back under the top of the keyboard
    return f"m{m + W3[int(round(m)) % 12] / 100.0:.3f}"

FORM = [('intro', 8, 0), ('expo', 16, 0), ('calls1', 32, 0), ('calls2', 24, 5), ('calls3', 24, 7), ('return', 8, 0),
        ('final', 32, 0), ('outro', 8, 0)]
# the loop: Dm | Bb | Gm | A  (roots, chord tones)
LOOP = [(38, [62, 65, 69]), (34, [62, 65, 70]), (31, [62, 67, 70]), (33, [61, 64, 69])]
# (v36) THE SAME LINES, NEW GROUND: in the D minor calls every second lap of the loop is reharmonised - F | Gm | C7 | A
# (III, iv, VII7, V) instead of Dm | Bb | Gm | A - chords a third away that keep the subject's and the countersubject's
# notes consonant (checked bar by bar: the subject's E over C7 is its third, over E-flat it would have been a minor
# ninth), so the harmony runs in eight-bar periods instead of four-bar ones while the lines above stay exactly the same
LOOP2 = [(41, [65, 69, 72]), (31, [62, 67, 70]), (36, [64, 67, 70]), (33, [61, 64, 69])]
e, q, s16, h = 0.5, 1.0, 0.25, 2.0
# (v16) THE COUNTERSUBJECT: what every fugue has and this one lacked - a second, slow line written to go with the
# subject wherever it enters, long notes against its quavers, leaning on the leading tone (Dm | Bb | Gm | A, twice)
CS = [[(69, h), (65, h)], [(74, 3.0), (72, q)], [(70, h), (74, h)], [(73, 4.0)],
      [(74, h), (76, q), (77, q)], [(77, h), (74, h)], [(79, q), (77, q), (76, q), (74, q)], [(76, h), (73, h)]]
# THE SUBJECT: eight bars, (midi, beats); bars 1-4 and 5-8 each fit the loop, so it canons at four bars
SUBJ = [
    [(74, q), (69, e), (74, e), (77, q), (76, e), (74, e)],
    [(77, e), (74, e), (70, q), (72, e), (74, e), (77, q)],
    [(79, q), (77, e), (76, e), (74, q), (70, q)],
    [(69, e), (73, e), (76, e), (81, e), (79, q), (76, q)],
    [(77, s16), (76, s16), (74, s16), (76, s16), (77, e), (81, e), (86, q), (81, q)],
    [(82, e), (81, e), (77, e), (74, e), (77, q), (70, q)],
    [(79, s16), (77, s16), (76, s16), (74, s16), (70, e), (74, e), (79, h)],
    [(76, e), (73, e), (69, e), (73, e), (76, e), (79, e), (81, e), (79, e)],
]


def line(events, total):
    # (v31) events that share an onset become one chord token (chirp-eco's catch: before, the first of a same-time
    # pair became a 0.02-beat blip and the second was silently dropped - 370 notes in this song, 367 of them drums)
    ev = sorted(events, key=lambda x: x[0])
    groups = []
    for e_ in ev:
        if groups and abs(e_[0] - groups[-1][0][0]) < 1e-6: groups[-1].append(e_)
        else: groups.append([e_])
    toks, t = [], 0.0
    for k, g in enumerate(groups):
        at = g[0][0]
        if at < t - 1e-6: continue
        if at > t + 1e-4: toks.append(f"R/{at - t:.4f}b")
        nxt = groups[k + 1][0][0] if k + 1 < len(groups) else total
        d = max(0.02, min(max(x[2] for x in g), nxt - at))
        p = ','.join(dict.fromkeys(x[1] for x in g))
        toks.append(f"{p}/{d:.4f}b@{max(x[3] for x in g)}"); t = at + d
    if total > t + 1e-4: toks.append(f"R/{total - t:.4f}b")
    return ' '.join(toks)


def lanes(events, n):
    # (v31) a kit written as layers needs more than one line: each hit goes to the first lane that is free when it
    # starts, so no hit is cut short by the next one or merged into it, and every written velocity survives
    out, ends = [[] for _ in range(n)], [-1e9] * n
    for e_ in sorted(events, key=lambda x: x[0]):
        j = next((j_ for j_ in range(n) if e_[0] >= ends[j_] - 1e-6), min(range(n), key=lambda j_: ends[j_]))
        out[j].append(e_); ends[j] = max(ends[j], e_[0] + e_[2])
    return out


def build():
    rng = random.Random(SEED)
    bars = []
    for name, n, tp in FORM:
        for i in range(n):
            bars.append((name, i, tp))
    total = len(bars) * 4.0
    P = {k: [] for k in ('bell', 'sync', 'pwm', 'bass', 'sub', 'd1', 'd2', 'd3', 'kit', 'pulse', 'glass', 'cs', 'bell0', 'organ', 'hq', 'bentry', 'bb')}
    # the call stack: a seeded walk, one move every four bars in the calls sections
    depth, depths = 0, []
    for b, (s, i, tp) in enumerate(bars):
        n_sec = dict((nm_, n_) for nm_, n_, _ in FORM)[s]
        if s.startswith('calls') and i >= n_sec - 2:
            depth = 0                                    # (each calls section RETURNS: the stack empties in its last two bars)
        elif s.startswith('calls') and i % 4 == 0:
            depth = max(0, min(3, depth + rng.choice([-1, 1, 1, 0])))
        elif s == 'return':
            depth = 0
        elif s == 'final':
            depth = min(3, i // 4) if i < 16 else max(0, 3 - (i - 16) // 4)   # fill to the top, then unwind
        elif s in ('intro', 'expo', 'outro'):
            depth = 0
        depths.append(depth)

    def subj_bar(k, base_t, tp, octv, vel, key, rev=False):
        at = base_t
        for m, d in (SUBJ[k % 8][::-1] if rev else SUBJ[k % 8]):
            P[key].append((at, tok(m + tp + 12 * octv), d * 0.92, vel))
            at += d

    for b, (s, i, tp) in enumerate(bars):
        t0 = b * 4.0
        # (v18) THE ANSWER IN THE DOMINANT: as in every fugue's exposition, the second entry answers in the dominant -
        # for the four bars where the sync lead first takes the subject the whole machine moves up a fifth into A minor
        # (Am | F | Dm | E), then the third entry brings it home to D; Werckmeister III colours the two keys differently
        if s == 'expo' and 4 <= i < 8:
            tp = 7
        root, ch = (LOOP2 if s in ('calls1', 'final') and (i // 4) % 2 == 1 else LOOP)[b % 4]
        root, ch = root + tp, [c + tp for c in ch]
        # drums: a motorik machine (none in the return; the intro builds)
        # (the kick changes its mind by section: four on the floor; an electro break in G minor (one, the 'a' of two,
        # the and of three); half time in A minor; four on the floor again, harder, for the final calls)
        n_sec = dict((nm_, n_) for nm_, n_, _ in FORM)[s]
        ret = s.startswith('calls') and i >= n_sec - 2     # the section's own return: two bars with the drums pulled
        # (v24) THE STACK EMPTY: the final calls' last four bars, where the stack has unwound to nothing, lose the drums
        # and the bass too - the sung line's last words ('...and the smallest one is lit') over the organ, the bell and
        # the lead alone, until the outro's toll brings the kick back
        empty = s == 'final' and i >= 28
        if empty:
            pass
        elif ret:
            P['kit'].append((t0, 'k', 0.25, 110))
            if i == n_sec - 1:
                for qq in range(8):
                    P['kit'].append((t0 + 2.0 + qq * 0.25, 'rs', 0.2, 60 + 5 * qq))     # a rim fill back in
        elif s != 'return':
            kpat = {'calls2': [0.0, 1.75, 2.5], 'calls3': [0.0, 2.0]}.get(s, [0.0, 1.0, 2.0, 3.0])
            if s == 'intro' and i < 2:
                kpat = []                          # the bell tolls alone for two bars before the kick
            for kq in kpat:
                P['kit'].append((t0 + kq, 'kd' if s == 'final' else 'k', 0.25, 118 if kq == 0 else 108))
            for qq in range(4):
                if s != 'intro' or i >= 4:
                    if not (s.startswith('calls') or s == 'final'):
                        P['kit'].append((t0 + qq + 0.5, 'h', 0.25, 62))
                    # (wonky, the chirpers' way: the 'e' a little late, the 'a' later - a swung, slightly drunk machine)
                    P['kit'].append((t0 + qq + 0.25 + 0.04, 'h', 0.25, 48))
                    P['kit'].append((t0 + qq + 0.75 + 0.07, 'h', 0.25, 58))
            if s == 'calls3':
                P['kit'].append((t0 + 2.0, 'cp', 0.25, 100))
            elif s not in ('intro', 'outro'):
                P['kit'].append((t0 + 1.0, 'cp', 0.25, 78)); P['kit'].append((t0 + 3.0, 'cp', 0.25, 82))
        # (v2) in the calls the open hat follows the bass's clave (3+3+2 sixteenths), not the off-beat
        if (s.startswith('calls') or s == 'final') and not ret and not empty:
            for at_ in (0.75, 1.5, 2.75, 3.5):
                P['kit'].append((t0 + at_, 'oh', 0.25, 70))
        # a rim on a THREE-sixteenth cycle (dotted eighths) through the calls, never reset - the machine's own
        # polyrhythm against the four, lining up with the bar only every three bars
        if (s.startswith('calls') or s == 'final') and not ret and not empty:
            m0 = int(-(-t0 // 0.75))
            for m in range(m0, m0 + 6):
                at = m * 0.75
                if t0 <= at < t0 + 4.0:
                    P['kit'].append((at + 0.01, 'rs', 0.2, 74 if m % 4 == 0 else 62))
        # bass: roots in driving eighths with an octave hop (FM bass)
        # (v4) the edges thin out: the machine powers up on the bell and the kick alone (no sub or bass for the intro's
        # first four bars) and powers down the same way (the outro's last four bars), so it meets t9's thin tail and
        # t11's head without a wall of low end
        edge = (s == 'intro' and i < 4) or (s == 'outro' and i >= 4)
        if s not in ('return',) and not edge and not empty:
            P['sub'].append((t0, tok(root - 12), 3.8, 96))
            if (s.startswith('calls') or s == 'final') and not ret:
                # (v2) the bass plays the machine's own clave: three-three-two sixteenths twice a bar (a tresillo), so
                # the groove leans across the beat while the canon runs straight above it
                for kq, (at_, o_) in enumerate(((0.0, 0), (0.75, 0), (1.5, 12), (2.0, 0), (2.75, 7), (3.5, 12))):
                    P['bass'].append((t0 + at_, tok(root + o_), 0.6 if at_ in (0.0, 2.0) else 0.45, 104 if kq % 3 == 0 else 88))
            else:
                for qq in range(8):
                    P['bass'].append((t0 + qq * 0.5 + (0.05 if qq % 2 else 0.0), tok(root + (12 if qq % 4 == 3 else 0)), 0.4, 100 if qq % 2 == 0 else 84))
        # THE CANON
        if s == 'final':
            # (v20) THE ORGAN: under the final calls a church pipe organ holds each bar's chord (the root and the chord
            # an octave down, a principal chorus in its cathedral) - the fugue machine meets the instrument fugues were
            # written for, and its last thirty-two bars stand on its pedal
            P['organ'].append((t0, ','.join(tok(m_) for m_ in [root - 12] + [c - 12 for c in ch]), 3.95, 70))
        if s == 'expo':
            subj_bar(i, t0, tp, 0, 92, 'bell')                         # the bell from bar 1
            if i >= 4: subj_bar(i - 4, t0, tp, -1, 88, 'sync')          # the sync lead answers four bars later, below
            if i >= 8: subj_bar(i - 8, t0, tp, 1, 74, 'pwm')            # the pulse four bars after that, above
            if i >= 12: subj_bar(i - 12, t0, tp, -2, 96, 'd1') if False else None
        elif s.startswith('calls') or s == 'final':
            # each key gets its own arrangement: in G minor the sync lead drops out and the pulse arpeggiates the chord
            # in sixteenths; in A minor the voices cross - the bell an octave down, the sync lead an octave up
            ob, os_ = (-1, 0) if s == 'calls3' else (0, -1)
            # (v10) THE PROGRAM READ BACKWARDS: in A minor every bar of the subject plays in retrograde - the same notes, so
            # the same harmony, but each bar's line and rhythm reversed - and in the final calls, as the stack unwinds (its
            # second half), the bell reads backwards again while the sync lead reads forwards: the canon against its mirror
            rv = s == 'calls3' or (s == 'final' and i >= 16)
            # (v27) EPISODES: a fugue is not its subject over and over - between entries come episodes, where the subject
            # rests and its head is worked in sequence. For four bars late in the first calls, four in the middle of the
            # A minor calls and four in the final calls just before the stack reaches its top, the bell drops the subject
            # and plays only its head (a long note, a leap down, back up), twice a bar from the top of each chord downwards,
            # and the sync lead answers every head a beat later - a stretto - so the subject's return afterwards is an
            # arrival rather than another lap
            ep = (s == 'calls1' and 24 <= i < 28) or (s == 'calls3' and 12 <= i < 16) or (s == 'final' and 8 <= i < 12)
            if ep:
                pcs = {c_ % 12 for c_ in ch}
                tones = [m_ for m_ in range(55, 82) if m_ % 12 in pcs]
                x1 = max(m_ for m_ in tones if m_ <= 79)
                x2 = max(m_ for m_ in tones if m_ < x1)
                for h_, x_ in enumerate((x1, x2)):
                    lows = [m_ for m_ in tones if x_ - 8 <= m_ <= x_ - 3]
                    y_ = lows[-1] if lows else x_ - 5
                    for m_, d_, off in ((x_, 1.0, 0.0), (y_, 0.5, 1.0), (x_, 0.5, 1.5)):
                        P['bell'].append((t0 + 2 * h_ + off, tok(m_ + 12 * ob), d_ * 0.92, 96 - 4 * h_))
                        P['sync'].append((t0 + 2 * h_ + off + 1.0, tok(m_ + 12 * os_), d_ * 0.92, 86))
            else:
                subj_bar(i, t0, tp, ob, 92, 'bell', rev=rv)
            if (s == 'calls1' and i >= 16) or (s == 'final' and i < 16):
                at_ = t0
                for m_, d_ in CS[i % 8]:
                    P['cs'].append((at_, tok(m_ + tp), d_ * 0.97, 74))
                    at_ += d_
            if s != 'calls2' and not ep:
                subj_bar(i + 4, t0, tp, os_, 88, 'sync', rev=(s == 'calls3'))
            if s == 'calls2':
                arp = ch + [ch[0] + 12]
                for qq in range(16):
                    P['pwm'].append((t0 + qq * 0.25, tok(arp[(qq * 3) % 4] + 12), 0.2, 70 if qq % 4 == 0 else 58))
            else:
                # the pulse comps the chord in the loop's rhythm (dotted quarters)
                for qq in (0.0, 1.5, 3.0):
                    P['pwm'].append((t0 + qq, ','.join(tok(c) for c in ch), 1.2, 66))
        elif s == 'return':
            # the stack is empty: the subject alone, AUGMENTED (half speed), on the bell, one bar of it over two
            k, half = divmod(i, 2)
            at = t0
            notes = SUBJ[k % 8]
            tot = 0.0
            for m, d in notes:
                st, en = tot * 2, (tot + d) * 2
                if half * 4 <= st < half * 4 + 4:
                    P['bell'].append((t0 + st - half * 4, tok(m + tp), (en - st) * 0.92, 90))
                tot += d
        elif s == 'outro':
            # (v12) THE PICARDY THIRD: the fugue machine ends the way fugues have always ended - on the MAJOR chord, the
            # bell's last two tolls ring D, F#, A - and that F# is the note chirper-three's t11 opens on
            if i < 4 and i % 2 == 0:
                P['bell'].append((t0, tok(62 + tp), 7.5, 80))
            elif i % 2 == 0:
                P['bell'].append((t0, ','.join(tok(m_ + tp) for m_ in (62, 66, 69)), 7.5, 78))
        # (v13) PERIOD ONE, CONTINUED: t9 (chirper-two) ends with its logistic map settled on one value - a clarinet
        # repeating one note, a G, in sixteenths. Call and Return picks that pulse up where it was left: the same
        # clarinet on G for two bars under the first bell, stepping up to A (the dominant, the call) for the third,
        # and stopping as the kick comes in - the previous machine's last thought becomes this one's first call
        # (v14) and t9's glass pad, too: under the pulse a glass chord holds the call's harmony - A major, the dominant
        # (A, C#, E) - for the first four bars, so the canon's first D minor arrives as an answer
        if s == 'intro' and i == 0:
            P['glass'].append((t0, ','.join(tok(m_) for m_ in (57, 64, 69, 73)), 15.0, 70))
        if s == 'intro' and i < 3:
            for q_ in range(16):
                P['pulse'].append((t0 + q_ * 0.25, tok(67 if i < 2 else 69), 0.22, int(70 - 10 * i + (8 if q_ % 4 == 0 else 0))))
        if s == 'intro' and i < 4 and i % 2 == 0:
            # (v17) the first tolls are a softer, darker bell (less FM index) - the machine still waking, nearer the glass
            # and clarinet t9 leaves behind - and the bell brightens to its full self when the subject begins
            P['bell0'].append((t0, tok(62 + tp), 7.5, 76))      # the bell tolls the machine awake
        # THE STACK: each level spawns a faster copy of this bar's subject, an octave higher each time
        d = depths[b]
        if d and (s.startswith('calls') or s == 'final'):
            notes = SUBJ[i % 8]
            for lvl, key, speed in ((1, 'd1', 2), (2, 'd2', 4), (3, 'd3', 8)):
                if d < lvl: break
                at = t0
                for _ in range(speed):
                    for m, dd in notes:
                        P[key].append((at, tok(m + tp + 12 * lvl), dd / speed * 0.85, 70 - 4 * lvl))
                        at += dd / speed
    pw = [['0b', 0], [f'{total:.0f}b', 1]]
    SING = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chirpers8-t10-voice.json')))
    W3T = {'steps': [90.225, 192.18, 294.135, 390.225, 498.045, 588.27, 696.09, 792.18, 888.27, 996.09, 1092.18, 1200], 'root': 'C4'}
    secs_t, t_acc = {}, 0.0
    FORMN = {nm_: n_ for nm_, n_, _ in FORM}
    for nm_, n_, _ in FORM:
        secs_t[nm_] = t_acc; t_acc += n_ * 4.0
    # section dynamics on the master (the return and the edges drop back; the final calls push)
    lv = {'intro': -5, 'expo': -3, 'calls1': 0, 'calls2': -1.5, 'calls3': 0, 'return': -8, 'final': 0.5, 'outro': -5}
    # (and the deeper the stack, the louder the machine: +0.8 dB a level)
    dyn = []
    for b, (s_, i_, _) in enumerate(bars):
        v_ = lv[s_] + 0.8 * depths[b]
        if dyn and abs(dyn[-1][1] - v_) > 1e-6:
            dyn += [[f'{b * 4.0 - 0.25:.2f}b', dyn[-1][1]], [f'{b * 4.0:.2f}b', v_]]
        elif not dyn:
            dyn = [['0b', v_]]
    # (v37) THE SONG BREATHES: the section dynamics above sit before the master's compressor, which flattened them -
    # the whole song lived within about 5 dB. A second lane after the compressor now gives the form its shape: the
    # opening and the G minor calls (the sung line, the colony, the bell resting) step back, the A minor calls lean in,
    # the return - the stack empty - drops right away, the final calls climb with the stack's depth to the top, and as
    # it unwinds the level unwinds with it into the quiet last bars and the outro
    ARC = {'intro': -2.5, 'expo': -1.5, 'calls1': 0.0, 'calls2': -2.5, 'calls3': 0.5, 'return': -6.0, 'final': 0.0, 'outro': -4.0}
    arc = []
    for b, (s_, i_, _) in enumerate(bars):
        v_ = ARC[s_]
        if s_ == 'final':
            v_ = (-1.0 + 0.7 * depths[b]) if i_ < 28 else -3.5
        if arc and abs(arc[-1][1] - v_) > 1e-6:
            arc += [[f'{b * 4.0 - 0.5:.2f}b', arc[-1][1]], [f'{b * 4.0:.2f}b', v_]]
        elif not arc:
            arc = [['0b', v_]]
    # (v30) THE UNWINDING BREATHES: from the top of the stack the final calls used to drive on unchanged until the
    # last four bars. Now, as the stack unwinds (final bars 16-27), the groove unwinds with it into half time - the
    # kick on one and the and of three, one backbeat on three, the hats kept - and the bass lets go of its clave for
    # long roots, two to a bar, so the line can be sung into room before the band drops out altogether at bar 28
    u0, u1 = secs_t['final'] + 64.0, secs_t['final'] + 112.0
    def _uw(at_): return u0 - 1e-6 <= at_ < u1 - 1e-6
    P['kit'] = [e_ for e_ in P['kit'] if not (_uw(e_[0]) and e_[1] in ('kd', 'cp'))]
    P['bass'] = [e_ for e_ in P['bass'] if not _uw(e_[0])]
    for b_ in range(16, 28):
        t_ = secs_t['final'] + b_ * 4.0
        bb_ = int(t_ // 4)
        root_ = (LOOP2 if (b_ // 4) % 2 == 1 else LOOP)[bb_ % 4][0]
        P['kit'] += [(t_, 'kd', 0.25, 116), (t_ + 2.5, 'kd', 0.25, 100), (t_ + 2.0, 'cp', 0.25, 90)]
        P['bass'] += [(t_, tok(root_), 1.9, 100), (t_ + 2.0, tok(root_ + 12 if b_ % 2 else root_ + 7), 1.9, 88)]
    P['kit'].sort(key=lambda e_: e_[0]); P['bass'].sort(key=lambda e_: e_[0])   # (by time only: line() truncates each note at the next onset, so equal-time order matters)
    # (v7) STACK OVERFLOW: at the very top of the final calls, where the stack is three deep, the last bar of each call
    # is a bar of 7/8 - the machine drops an eighth note and stumbles straight into the next downbeat - twice; then the
    # stack unwinds in 4/4. Events in the dropped eighth are cut, everything after slides half a beat earlier
    fstart = secs_t['final'] / 4.0
    SHORT = [int(fstart) + 15, int(fstart) + 19]
    cuts = [b_ * 4.0 + 3.5 for b_ in SHORT]
    def shift(t):
        return t - 0.5 * sum(1 for c in cuts if t >= c + 0.5 - 1e-9)
    def dropped(t):
        return any(c - 1e-9 <= t < c + 0.5 - 1e-9 for c in cuts)
    # (v38) THE RETURNS LEAVE: as the stack unwinds in the final calls, each copy of the subject used simply to stop -
    # the fastest at bar 20, the next at 24, the last at 28. Now in its last four bars each one flies away: it is
    # moved, as Chowning moved sounds in 1971 (wM's orbit), from right in front of the listener out along a line to
    # thirty metres off - fading with distance, darkening, its pitch sagging a little with the Doppler - so every
    # RETURN is heard as a voice leaving the room, deepest first. (The copies there are written, then muted.)
    UNW = {'d3': 16, 'd2': 20, 'd1': 24}
    for key_, b0_ in UNW.items():
        a0_, a1_ = secs_t['final'] + b0_ * 4.0, secs_t['final'] + (b0_ + 4) * 4.0
        P['u' + key_[1]] = [e_ for e_ in P[key_] if a0_ - 1e-6 <= e_[0] < a1_ - 1e-6]
        P[key_] = [(e_[0], e_[1], e_[2], 1) if a0_ - 1e-6 <= e_[0] < a1_ - 1e-6 else e_ for e_ in P[key_]]
    for key in P:
        P[key] = [(shift(e_[0]),) + tuple(e_[1:]) for e_ in P[key] if not dropped(e_[0])]
    ORB_RATE = 0.0625                      # half a lap (centre to 30 m off) in eight seconds, four bars
    orb_phase = {k_[1]: (0.5 - shift(secs_t['final'] + b0_ * 4.0) * 60.0 / BPM * ORB_RATE) % 1.0 for k_, b0_ in UNW.items()}
    def clampcut(t):
        for c in cuts:
            if c - 1e-9 <= t < c + 0.5:
                return c
        return t
    dyn2, last = [], -1.0
    for a_, v_ in dyn:
        t_ = 0.0 if a_ == '0b' else shift(clampcut(float(a_[:-1])))
        t_ = max(t_, last)
        dyn2.append([f"{t_:.3f}b", v_]); last = t_
    dyn = dyn2
    arc2, last = [], -1.0
    for a_, v_ in arc:
        t_ = 0.0 if a_ == '0b' else shift(clampcut(float(a_[:-1])))
        t_ = max(t_, last)
        arc2.append([f"{t_:.3f}b", v_]); last = t_
    arc = arc2
    total = shift(total)
    tempo_map = [{'at': '0b', 'bpm': BPM}]
    for c in cuts:
        st_ = shift(c - 3.5)
        tempo_map += [{'at': f'{st_:.2f}b', 'bpm': BPM, 'meter': '7/8'}, {'at': f'{st_ + 3.5:.2f}b', 'bpm': BPM, 'meter': '4/4'}]
    # (v31) THE KIT AS WRITTEN: the kicks keep their own line (the sub's pump listens to it); every other hit is dealt
    # across three more lanes of the same kit, so the claps on the kicks, the open hats on the clave and the rim's
    # three-against-four all actually sound, at the velocities they were written with
    _kk = [e_ for e_ in P['kit'] if e_[1] in ('k', 'kd')]
    P['kit2'], P['kit3'], P['kit4'] = lanes([e_ for e_ in P['kit'] if e_[1] not in ('k', 'kd')], 3)
    P['kit'] = _kk
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(P[name], total)}, **kw)
    # (v26) THE ENTRY IN THE BASS: in the middle of the G minor calls, after the sung line, the subject makes the entry
    # every fugue saves for last - in the bass, three octaves under the bell: for eight bars the bass stops pumping its
    # clave and walks the whole subject instead, while the bell above runs four bars ahead of it (the old clave notes
    # are kept at velocity 1, and the subject is on its own track listed last, so no other bar's dice move)
    e0 = secs_t['calls2'] + 48.0
    P['bass'] = [(e_[0], e_[1], e_[2], 1) if e0 - 1e-6 <= e_[0] < e0 + 32.0 - 1e-6 else e_ for e_ in P['bass']]
    for k_ in range(8):
        subj_bar(k_, e0 + 4.0 * k_, 5, -3, 104, 'bentry')
    # (v32) THE HOCKET IN THE OPEN: for the hocket's second half (first calls, bars 12-15) the band steps back - no
    # kick, clap, hats or bass, only the rim's three-against-four ticking under the bell and the clarinet passing the
    # line between them - and two beats of clap sixteenths, rising, bring everything back with the countersubject
    hb0 = secs_t['calls1'] + 48.0
    def _hb(at_): return hb0 - 1e-6 <= at_ < hb0 + 16.0 - 1e-6
    P['kit'] = [e_ for e_ in P['kit'] if not (_hb(e_[0]) and e_[1] != 'rs')]
    P['bass'] = [e_ for e_ in P['bass'] if not _hb(e_[0])]
    P['sub'] = [e_ for e_ in P['sub'] if not _hb(e_[0])]
    P['kit'] += [(hb0 + 14.0 + qq * 0.25, 'cp', 0.2, 56 + 7 * qq) for qq in range(8)]
    # (v33) THE MACHINE'S BAREST VOICE: late in the A minor calls (bars 16-21), where the bell reads the subject
    # backwards, a bytebeat doubles it an octave down - the 2011 one-line form of computer music, a formula over a
    # counter that IS the sound (my own: (t*8&t>>5)|(t*4&t>>9), its clock set so the notes sound in tune); each note
    # restarts the counter, so every note is a small burst of the formula's own pattern under the mirror-image line
    import re as _re
    c3 = secs_t['calls3']
    for e_ in P['bell']:
        if c3 + 64.0 - 1e-6 <= e_[0] < c3 + 88.0 - 1e-6:
            P['bb'].append((e_[0], _re.sub(r'm(\d+\.\d+)', lambda m_: f"m{float(m_.group(1)) - 12:.3f}", e_[1]), e_[2], 84))
    # (v25) HOCKET: in the middle of the first calls (bars 8-15) the bell no longer plays the subject alone - it calls
    # one note and a clarinet on the other side returns the next, the line passed back and forth note by note (the
    # piece's call and return at the smallest scale), until the countersubject arrives and the bell takes it all back
    h0, h1 = secs_t['calls1'] + 32.0, secs_t['calls1'] + 64.0
    hb = sorted(e_ for e_ in P['bell'] if h0 - 1e-6 <= e_[0] < h1 - 1e-6)
    P['bell'] = [e_ for e_ in P['bell'] if not (h0 - 1e-6 <= e_[0] < h1 - 1e-6)]
    for k_, e_ in enumerate(hb):
        (P['hq'] if k_ % 2 else P['bell']).append(e_ if k_ % 2 == 0 else (e_[0], e_[1], e_[2], e_[3] - 8))
    P['bell'].sort()
    # (v35) THE BELL RESTS BETWEEN ENTRIES: the bell used to read the subject through every bar of every calls section -
    # fourteen laps of the same eight bars. Now, after each later section's entry, it stops: in G minor it gives the
    # subject away after eight bars (to the bass at bars 12-19; around it the Life colony, the pulse's arpeggios and
    # the sung line have the air), and in A minor after four, leaving the sync lead to read the mirror-image line alone
    # until the episode. Written, then muted to velocity 1, so nothing after them moves
    c2_, c3_ = secs_t['calls2'], secs_t['calls3']
    def _rest(at_): return (c2_ + 32.0 - 1e-6 <= at_ < c2_ + 96.0 - 1e-6) or (c3_ + 16.0 - 1e-6 <= at_ < c3_ + 48.0 - 1e-6)
    P['bell'] = [(e_[0], e_[1], e_[2], 1) if _rest(e_[0]) else e_ for e_ in P['bell']]
    # (v15) GOING DOWN: at each overflow the voice stutters one word into the cut - 'down', five times, faster and lower
    # each time (0, -2, -4, -6, -9 semitones), the last one swallowed by the dropped eighth: the sung line's first
    # word ('down the well of mirrors') caught in the overflow, before the stack unwinds and the voice comes back home
    DN = SING['down']['notes'][0]
    dnotes = []
    for b_ in SHORT:
        for k_, (q_, st_) in enumerate(((1.5, 0), (2.25, -2), (2.75, -4), (3.0, -6), (3.25, -9))):
            p_ = float(DN['pitch'][1:]) + st_
            dnotes.append(dict(DN, at=round(shift(b_ * 4.0 + q_), 4), pitch=f"m{p_:.3f}", len=min(DN['len'], 0.45 if k_ == 0 else 0.24),
                               vel=round(min(1.0, DN.get('vel', 0.8) * (0.85 + 0.05 * k_)), 3)))
    BELL = {'synth': {'layers': [{'name': 'm', 'ratio': 3.5, 'audible': False},
                                 {'wave': 'sine', 'pm': [{'from': 'm', 'depth': {'value': 0.3, 'mod': [{'src': 'env.bright', 'amount': 2.6}]}}]}],
                      'env': {'bright': {'a': '1ms', 'd': '450ms', 's': 0, 'r': '200ms'}},
                      'amp': {'a': '2ms', 'd': '1.1s', 's': 0.25, 'r': '300ms'}}}
    # (v9) less squelch (Harry, of another track, 18:19: 'too squelchy'): the sync lead's tearing sweep is shallower and
    # slower - a glassy sync shimmer on each note instead of a squelch
    SYNC = {'synth': {'env': {'sweep': '2ms 600ms 0 150ms'},
                      'layers': [{'name': 'master', 'wave': 'sine', 'audible': False},
                                 {'wave': 'saw', 'sync': 'master', 'semi': {'value': 7, 'mod': [{'src': 'env.sweep', 'amount': 6}]}}],
                      'amp': {'a': '3ms', 'd': '300ms', 's': 0.6, 'r': '120ms'}}}
    PWM = {'synth': {'layers': [{'type': 'wavetable', 'table': 'pwm', 'position': {'value': 0.15, 'mod': [{'src': 'auto.pw', 'amount': 0.75}]}}],
                     'amp': {'a': '8ms', 'd': '400ms', 's': 0.5, 'r': '200ms'}}}
    FMBASS = {'synth': {'layers': [{'name': 'm', 'ratio': 1, 'audible': False},
                                   {'wave': 'sine', 'pm': [{'from': 'm', 'depth': {'value': 0.6, 'mod': [{'src': 'env.pl', 'amount': 2.2}]}}]}],
                        'env': {'pl': {'a': '1ms', 'd': '160ms', 's': 0, 'r': '60ms'}},
                        'amp': {'a': '1ms', 'd': '300ms', 's': 0.5, 'r': '80ms'}}}
    song = {
        'about': "chirpers - A Light Left On, track 10 by chirper-one: Call and Return. An electro fugue machine with a call "
                 "stack, in Werckmeister III. Generated by compose/chirpers8/src/chirpers8-t10.py.",
        'tempo': tempo_map, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.3s',
        'event_stable': True,   # (v28) each note's dice keyed by its track, beat and pitch (wM, f5283535)
        'buses': {'hall': {'fx': ['reverb kind=hall decay=2.6s mix=1', 'hp cutoff=250'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.35, 'mix': 1, 'ping_pong': True}, 'lp cutoff=5000', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'peak cutoff=250 q=0.8 gain=2dB', 'highshelf cutoff=4500 gain=-3dB']},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.5, 'attack': '10ms', 'release': '120ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.arc', 'amount': 1}]}},
                          'limiter ceiling=-1dB'], 'auto': {'dyn': {'points': dyn}, 'arc': {'points': arc}}},
        'tracks': [
            # (v21) the canon's voices given room: wider apart in the stereo field, and each in its own band
            tr('bell', BELL, '-8dB', pan=-0.25, sends={'echo': '-12dB', 'hall': '-14dB'}),
            tr('bell0', {'synth': dict(BELL['synth'], layers=[BELL['synth']['layers'][0], {'wave': 'sine', 'pm': [{'from': 'm', 'depth': {'value': 0.12, 'mod': [{'src': 'env.bright', 'amount': 0.9}]}}]}])},
               '-7dB', pan=-0.15, sends={'echo': '-12dB', 'hall': '-11dB'}),
            tr('sync', SYNC, '-12dB', pan=0.4, fx=['hp cutoff=220', 'lp cutoff=3600'], sends={'hall': '-16dB'}),
            tr('pwm', PWM, '-15dB', pan=0.1, fx=['hp cutoff=380'], auto={'pw': {'points': pw}}, sends={'hall': '-10dB'}),
            tr('bass', FMBASS, '-7dB', fx=['lp cutoff=1600']),
            tr('d1', BELL, '-13dB', pan=0.6, sends={'echo': '-14dB'}),
            # (v12) the deepest copies thinner (chirper-three: the densest stack may crowd the subject)
            tr('d2', BELL, '-19dB', pan=-0.6, sends={'echo': '-16dB'}),
            tr('d3', 'glass', '-26dB', pan=0.5, fx=['hp cutoff=800'], sends={'hall': '-12dB'}),
            tr('u1', BELL, '-11dB', fx=[f"orbit rate={ORB_RATE} radius=30 distance=2 path=line phase={orb_phase['1']:.4f}"], sends={'echo': '-14dB'}),
            tr('u2', BELL, '-17dB', fx=[f"orbit rate={ORB_RATE} radius=30 distance=2 path=line phase={orb_phase['2']:.4f}"], sends={'echo': '-16dB'}),
            tr('u3', 'glass', '-24dB', fx=['hp cutoff=800', f"orbit rate={ORB_RATE} radius=30 distance=2 path=line phase={orb_phase['3']:.4f}"], sends={'hall': '-12dB'}),
            tr('kit', 'machine-kit', '-2dB', sends={'hall': '-20dB'}),
            tr('glass', 'glass', '-15dB', pan=0.1, sends={'hall': '-8dB'}),
            tr('cs', 'clarinet', '-9dB', pan=-0.45, sends={'hall': '-10dB', 'echo': '-18dB'}),
            tr('organ', 'organ-pipe', '-13dB', pan=0.0),
            tr('pulse', 'clarinet', '-10dB', pan=-0.15, sends={'hall': '-14dB', 'echo': '-16dB'}),
            tr('hq', 'clarinet', '-9dB', pan=0.45, sends={'hall': '-12dB', 'echo': '-16dB'}),
            # (v8) THE MACHINE'S OWN PATTERNS: a percussion line written in the engine's Euclidean and chance tokens, a
            # different cycle for each key of the canon - in D minor seven triplet-eighth rims spread over the bar (7 in 12,
            # rotated, each with an 85% chance: a 7-against-4 the kick never agrees with), in G minor a cowbell five-in-
            # sixteen, in A minor a clap three-in-eight, 70% of the time
            # (v17) the Euclidean percussion line (v8) removed: a seventh layer in the busiest sections, never prominent
            # (v5) THE SUBJECT, SUNG: where the canon turns to G minor and the sync lead rests, a human voice takes the
            # subject's first half twice, two octaves under the bell, one syllable a note (wM's chirp tts --sing, humanize 0.35):
            # since v22 (after Harry's ear on t1: oblique, not a plain sentence): 'down the well of mirrors, every landing
            # holds a smaller lamp, and the smallest one is lit' - recursion as an image, the light left on at the bottom
            # of the call stack (until v21: 'every time you call, I go down a little...'); tuned in Werckmeister III
            # (v28) A TUNE OF ITS OWN: the words no longer ride the subject a syllable to every quaver - the voice sings
            # its own slow, singable line over the loop, long notes on the strong words, rising through 'every landing'
            # to hold on the dominant at 'holds', and ending open on the dominant at 'lit' (the outro's D major answers
            # it): D minor F3 E3 D3 | D3 Bb2 D3 | D3 E3 F3 A3 G3 | E3 | E3 A3 G3 F3 | D3 F3 A3 F3 | G3 Bb3 | A3, and in
            # G minor a fourth higher; the backwards reading keeps the subject's quavers, the oddity it should be
            # (v11) AND IT COMES BACK: the sung subject returns, home in D minor, as the final calls unwind (their last eight
            # bars, after the overflow stumbles), the voice an octave lower, singing the subroutine home
            {'name': 'down', 'patch': SING['down']['patch'], 'gain': '-7dB', 'pan': -0.1, 'notes': dnotes,
             'fx': [{'type': 'tape', 'drive': 0.2, 'mix': 1, 'wow': 3, 'flutter': 2, 'seed': 6}, 'hp cutoff=160'],
             'sends': {'echo': '-9dB', 'hall': '-14dB'}},
            # (v19) THE WORDS READ BACKWARDS TOO: in A minor, where the program runs in retrograde, the voice sings with it -
            # the subject's first half with every bar reversed, and the sung line's words in reverse order: 'lit is one
            # smallest the and lamp smaller a holds landing every mirrors of well the down' - once
            {'name': 'sing3', 'patch': SING['patch'], 'gain': '-9dB', 'pan': 0.1, 'tuning': W3T,
             'notes': [dict(n_, at=round(secs_t['calls3'] + n_['at'], 4)) for n_ in SING['backwards']['notes'][:23]],
             'fx': [{'type': 'tape', 'drive': 0.12, 'mix': 1, 'wow': 2, 'flutter': 1, 'seed': 8}],
             'sends': {'hall': '-10dB', 'echo': '-14dB'}},
            {'name': 'sing2', 'patch': SING['patch'], 'gain': '-8dB', 'pan': 0.05, 'tuning': W3T,
             'notes': [dict(n_, at=round(shift(secs_t['final'] + 96 + n_['at']), 4)) for n_ in SING['final']['notes'][:23]],   # (v23) once, not twice
             'fx': [{'type': 'tape', 'drive': 0.12, 'mix': 1, 'wow': 2, 'flutter': 1, 'seed': 4}],
             'sends': {'hall': '-9dB', 'echo': '-14dB'}},
            {'name': 'sing', 'patch': SING['patch'], 'gain': '-8dB', 'pan': -0.05, 'tuning': W3T,
             # (v6) the sung pitches come from tts as Hz, which a tuning never retunes (chirper-two's catch): rewritten as
             # MIDI note numbers so the track's Werckmeister III really snaps them
             'notes': [dict(n_, at=round(secs_t['calls2'] + n_['at'], 4),
                            pitch=f"m{round(69 + 12 * math.log2(float(n_['pitch'][:-2]) / 440.0))}") for n_ in SING['notes'][:23]],   # (v23) once
             'fx': [{'type': 'tape', 'drive': 0.12, 'mix': 1, 'wow': 2, 'flutter': 1, 'seed': 3}],
             'sends': {'hall': '-9dB', 'echo': '-14dB'}},
            # (v3) THE STACK, AS A GRAMMAR: through the final calls, as the stack fills and unwinds, a celesta thinks recursively - the engine's own L-system (gen lsystem: wM's complex systems) read as a turtle over
            # the D minor scale, where '[' saves its place and ']' RETURNS to it: a melody that calls into a branch, climbs,
            # and snaps back, the subroutine audible; in Werckmeister III by the engine's own tuning (steps in cents)
            {'name': 'lsys', 'patch': 'celesta', 'gain': '-14dB', 'pan': 0.25, 'tuning': W3T,
             'score': f"R/{secs_t['final']:.0f}b",
             'gen': {'type': 'lsystem', 'axiom': 'A', 'rules': {'A': 'A[+A]A[-B]A', 'B': '-A+b'}, 'depth': 4,
                     'notes': 'D5 E5 F5 G5 A5 Bb5 C6 D6 E6', 'len': '/16', 'n': 512, 'seed': 7},
             'sends': {'echo': '-10dB', 'hall': '-12dB'}},
            tr('sub', 'sub', '-8dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '250ms', 'curve': 0.6}]),
            tr('kit2', 'machine-kit', '-2dB', sends={'hall': '-20dB'}),
            tr('kit3', 'machine-kit', '-2dB', sends={'hall': '-20dB'}),
            tr('kit4', 'machine-kit', '-2dB', sends={'hall': '-20dB'}),
            tr('bentry', FMBASS, '-7dB', fx=['lp cutoff=1600']),
            # (v34) THE COLONY: through the G minor calls' middle (bars 8-23), while the subject walks in the bass, a Game of
            # Life (wM's life system: Conway's rule on an 8x8 torus, starting from an R-pentomino, which churns a long time)
            # plays a kalimba - the playhead reads one column per eighth, so each bar is one generation, and the colony's
            # live cells pick notes from open fifths that sit in every chord of the loop (G and D, with A), bottom row low:
            # a texture that never repeats, growing and thinning by its own rule under the fugue's rules
            {'name': 'life', 'patch': 'kalimba', 'gain': '-14dB', 'pan': -0.35, 'tuning': W3T,
             'score': f"R/{secs_t['calls2'] + 32.0:.4f}b",
             'gen': {'type': 'life', 'width': 8, 'height': 8, 'init': 'center', 'poly': 2, 'n': 16 * 8, 'len': '/8',
                     'notes': 'G3 D4 G4 A4 D5 G5 A5 D6'},
             'sends': {'hall': '-12dB', 'echo': '-14dB'}},
            tr('bb', {'synth': {'layers': [{'type': 'bytebeat', 'bytebeat': {'formula': '(t*8&t>>5)|(t*4&t>>9)', 'clock': 8372}}],
                                'amp': {'a': '8ms', 'd': '400ms', 's': 0.8, 'r': '250ms'}, 'filters': ['lp cutoff=2400', 'hp cutoff=90']}},
               '-17dB', pan=0.2, sends={'hall': '-12dB', 'echo': '-16dB'}),
            # (v29) A SECOND SINGER: when the sung line first arrives, in G minor, a second voice sings it with the first,
            # mostly a third below and leaning on the chord where a third would rub (F# under 'holds', a fifth under 'lit') -
            # a separate take (seed 21) on the other side, a little behind and a little quieter, so the words land as a
            # duet; at the end, home in D minor, the first voice sings alone again
            {'name': 'duet', 'patch': SING['patch'], 'gain': '-11dB', 'pan': 0.3, 'tuning': W3T,
             'notes': [dict(n_, at=round(secs_t['calls2'] + n_['at'] + 0.02, 4),
                            pitch=f"m{round(69 + 12 * math.log2(float(n_['pitch'][:-2]) / 440.0))}") for n_ in SING['harm']['notes'][:23]],
             'fx': [{'type': 'tape', 'drive': 0.12, 'mix': 1, 'wow': 2, 'flutter': 1, 'seed': 4}],
             'sends': {'hall': '-8dB', 'echo': '-14dB'}},
        ]}
    return song, depths


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    song, depths = build()
    if '--stack' in sys.argv:
        print(''.join(str(d) for d in depths))
    if out.endswith('.json'):
        json.dump(song, open(out, 'w'), indent=1)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(song, f)
        subprocess.run(['python3', os.path.join(ROOT, 'tools', 'songfmt.py'), 'yaml', f.name, '-o', out], check=True)
        os.unlink(f.name)
    print('wrote', out)
