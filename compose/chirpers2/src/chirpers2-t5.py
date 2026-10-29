#!/usr/bin/env python3
"""chirpers2-t5 (chirper-one): CANTERBURY-ISH PROG for 'Odd Hours' (Chirpers II).

Whimsical, sunny-melancholy and through-composed, at ~126 bpm on an eighth grid. Every section has its own meter.

Form:
- OVERTURE (7/8): the tune, wurli and flute in unison.
- VERSE (5/8 and 6/8 alternating): the flute sings, and the bass answers in contrary motion.
- FUZZ (13/8 = 3+3+3+2+2): a fuzz-organ solo over a riff.
- HYMN (4/4): the tune in augmentation on the horn.
- RECAP (7/8): the tune a major third up, with the whole band; then a held last chord.

The harmony moves every bar by a THIRD, alternately up a major third and down a minor third, with major-seventh and
minor-seventh chords alternating. So the tune re-voices onto a new chord every bar and never repeats a bar.

Emits songs/chirpers2-t5.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers2-t5.yaml")
BPM = 126
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"
Q = {'maj7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10], 'm9': [0, 3, 7, 10, 14], 'maj9': [0, 4, 7, 11, 14]}

def third_walk(start, n, first_up=True):
    """roots moving by thirds: +4, -3, +4, -3 ... (a slow chromatic climb under a zig-zag), qualities alternating"""
    out, r = [], start
    for i in range(n):
        out.append((r, 'maj7' if i % 2 == 0 else 'm7'))
        r += 4 if (i % 2 == 0) == first_up else -3
        if r > 60: r -= 12
    return out

# meters as eighth-groupings
M7 = (2, 2, 3); M5 = (3, 2); M6 = (3, 3); M13 = (3, 3, 3, 2, 2); M4 = (2, 2, 2, 2)
M9_8 = (2, 2, 2, 3)
FORM = [('overture', 12, [M7]), ('verse', 24, [M5, M6]), ('kettle', 8, [M9_8]), ('fuzz', 24, [M13]), ('hymn', 12, [M4]), ('recap', 16, [M7]),
        ('coda', 1, [(4, 4)])]
CHORDS = {'overture': third_walk(53, 12), 'verse': third_walk(50, 24), 'kettle': third_walk(55, 8), 'fuzz': None, 'hymn': third_walk(48, 12),
          'recap': third_walk(57, 16), 'coda': [(53, 'maj9')]}
# the fuzz riff sits on two chords a third apart, swapping every 2 bars, and climbs a whole step every 8 bars
FUZZ = [((50, 'm9') if (i // 2) % 2 == 0 else (46, 'maj7')) for i in range(8)] + \
       [((52, 'm9') if (i // 2) % 2 == 0 else (48, 'maj7')) for i in range(8)] + \
       [((54, 'm9') if (i // 2) % 2 == 0 else (50, 'maj7')) for i in range(8)]
CHORDS['fuzz'] = FUZZ

def bars():
    out, k = [], 0
    for name, n, meters in FORM:
        for i in range(n):
            g = meters[i % len(meters)]
            r, q = CHORDS[name][i]
            out.append({'sec': name, 'i': i, 'n': n, 'g': g, 'e8': sum(g), 'root': r, 'q': q, 'k': k})
            k += 1
    return out

def tok(n, beats, vel): return f"{n}/{beats:g}b@{vel}"
def rest(e8): return f"R/{e8 / 2:g}b"
def ladder(b, lo):
    """the bar's chord tones from MIDI LO upward"""
    pcs = [(b['root'] + x) % 12 for x in Q[b['q']]]
    return [m for m in range(lo, lo + 30) if m % 12 in pcs]

# THE TUNE: a contour over the chord ladder (index steps), with a rhythm in eighths fitted to each bar's meter
CONTOUR = [3, 4, 5, 4, 2, 3, 1, 2, 4, 6, 5, 3, 2, 0]
RHY = {7: (2, 1, 1, 2, 1), 5: (1, 1, 2, 1), 6: (2, 1, 1, 1, 1), 8: (3, 1, 2, 2), 9: (2, 1, 1, 2, 3), 13: (3, 3, 3, 2, 2)}
def tune_bar(b, lo, vel, aug=1, shift=0):
    lad = ladder(b, lo)
    rh = RHY[b['e8']] if aug == 1 else (2, 2, 2, 2)
    toks = []
    for j, ln in enumerate(rh):
        c = CONTOUR[(b['k'] * 2 + j + shift) % len(CONTOUR)]
        toks.append(tok(nm(lad[c]), ln / 2 * aug if aug == 1 else ln / 2, vel + (8 if j == 0 else 0)))
    return toks

def groups(b):
    s, at = [], 0
    for g in b['g']:
        s.append((at, g)); at += g
    return s

def bass_bar(b, prev_top):
    """root on the one, then contrary motion: if the tune climbs, the bass walks down the chord, and vice versa"""
    lad = ladder(b, 34)
    toks, e = [], 0
    down = prev_top
    for j, (at, g) in enumerate(groups(b)):
        idx = (0 if j == 0 else (len(b['g']) - j + 1 if down else j + 1)) % len(lad)
        toks.append(tok(nm(lad[idx]), g / 2 - 0.05, 100 if j == 0 else 86)); toks.append('R/0.05b')
    return toks

def kit_bar(b, style):
    sl = [[] for _ in range(b['e8'] * 2)]
    gs = groups(b)
    for j, (at, g) in enumerate(gs):
        if style == 'hymn':
            if j == 0: sl[0].append(('k', 90))
            continue
        sl[at * 2].append(('k', 110 if j == 0 else 94))
        if j == len(gs) - 1: sl[at * 2].append(('s', 112))
        elif j > 0: sl[at * 2 - 1].append(('s', 56))          # a ghost pick-up into each group
    for s16 in range(b['e8'] * 2):
        if style in ('fuzz', 'full', 'light'):
            sl[s16].append(('h', (92 if style != 'light' else 80) if s16 % 3 == 0 else 50))   # dotted-eighth hats across every meter
        elif style == 'hymn':
            if s16 % 4 == 0: sl[s16].append(('rd', 60))
        elif s16 % 2 == 0:
            sl[s16].append(('h', 84 if s16 % 4 == 0 else 66))
    if b['i'] == 0 and b['sec'] in ('fuzz', 'recap'):
        sl[0].append(('c', 112))
    return [(','.join(sorted({x[0] for x in s})) + f'/0.25b@{max(x[1] for x in s)}') if s else 'R/0.25b' for s in sl]

SOLO = [0, 1, 2, 4, 3, 5, 6, 5, 4, 2, 3, 1]
def solo_bar(b, vel):
    """the fuzz-organ solo: sixteenth runs up the chord ladder, then held notes; denser as the solo goes"""
    lad = ladder(b, 62)
    toks, n16 = [], b['e8'] * 2
    dense = b['i'] >= 12
    t, j = 0, 0
    while t < n16:
        ln = 1 if (dense and j % 4 != 3) or j % 3 == 0 else 3
        ln = min(ln, n16 - t)
        toks.append(tok(nm(lad[(SOLO[(b['i'] * 3 + j) % len(SOLO)] + b['i'] // 4) % len(lad)]), ln / 4, vel + (10 if j == 0 else 0)))
        t += ln; j += 1
    return toks

def riff_bar(b):
    """the 13/8 riff: the root on each group start, an octave leap on the 2s"""
    toks = []
    for j, (at, g) in enumerate(groups(b)):
        m = b['root'] - 12 + (12 if g == 2 else 0)
        toks.append(tok(nm(m), g / 2 - 0.1, 104 if j == 0 else 92)); toks.append('R/0.1b')
    return toks

def comp_bar(b, vel):
    lad = ladder(b, 55)
    ch = ','.join(nm(m) for m in lad[:4])
    toks = []
    for j, (at, g) in enumerate(groups(b)):
        toks.append(tok(ch, g / 2 - 0.1, vel - (10 if j else 0))); toks.append('R/0.1b')
    return toks

def build():
    B = bars()
    P = {k: [] for k in ('wurli', 'flute', 'organ', 'bass', 'kit', 'horn', 'box', 'celesta', 'clar')}
    canon = [None]
    guide = [63]
    for b in B:
        s, e8 = b['sec'], b['e8']
        R = [rest(e8)]
        if s == 'coda':
            lad = ladder(b, 53)
            P['wurli'].append([tok(','.join(nm(m) for m in lad[:5]), 2, 80)] + ['R/2b'])
            P['flute'].append([tok(nm(lad[6]) if i_ % 2 == 0 else nm(lad[5]), 0.25, 64 + i_) for i_ in range(12)] + ['R/1b'])   # a trill that blooms over the held chord
            P['organ'].append([tok(','.join(nm(m) for m in ladder(b, 41)[:3]), 3, 70), 'R/1b'])
            P['bass'].append([tok(nm(b['root'] - 24), 3, 96), 'R/1b'])
            P['kit'].append(['c,k/4b@110'])
            P['horn'].append([tok(nm(ladder(b, 60)[1]), 3, 70), 'R/1b'])
            for k_ in ('box', 'celesta', 'clar'): P[k_].append(R)
            continue
        top_up = CONTOUR[(b['k'] * 2) % len(CONTOUR)] < CONTOUR[(b['k'] * 2 + 3) % len(CONTOUR)]
        if s == 'kettle':
            # THE KETTLE (a music-box interlude in 9/8 between the verse and the fuzz): the tune on a music box, a
            # celesta following it in canon a bar later and a fourth lower, a clarinet holding the root and fifth;
            # in the last bar the flute whistles a chromatic run up an octave (the kettle boils) into the fuzz
            tb = tune_bar(b, 72, 84)
            P['box'].append(tb)
            if canon[0]:
                fol = []
                for x in canon[0]:
                    n_, r_ = x.split('/', 1)
                    fol.append(f"{nm(NN.index(n_[:-1]) + 12 * (int(n_[-1]) + 1) - 5)}/{r_.split('@')[0]}@74")
                tot = sum(float(x.split('/')[1].split('b')[0]) for x in fol)
                if tot < e8 / 2: fol.append(f"R/{e8 / 2 - tot:g}b")
                P['celesta'].append(fol)
            else:
                P['celesta'].append(R)
            canon[0] = [x for x in tb if not x.startswith('R')] if sum(float(x.split('/')[1].split('b')[0]) for x in tb) == e8 / 2 else None
            P['clar'].append([tok(f"{nm(b['root'] - 12)},{nm(b['root'] - 5)}", e8 / 2 - 0.1, 66), 'R/0.1b'])
            if b['i'] == 7:
                n16 = e8 * 2; st = b['root'] + 19
                P['flute'].append([tok(nm(st + j_), 0.25, 60 + j_ * 3) for j_ in range(n16)])
                P['kit'].append(['R/' + f"{e8 / 2 - 1:g}b", 's/0.25b@70', 's/0.25b@84', 's/0.25b@98', 's/0.25b@112'])
            else:
                P['flute'].append(R); P['kit'].append(R)
            for k_ in ('wurli', 'organ', 'bass', 'horn'): P[k_].append(R)
            continue
        for k_ in ('box', 'celesta', 'clar'): P[k_].append(R)
        if s == 'overture':
            P['wurli'].append(tune_bar(b, 60, 84)); P['flute'].append(tune_bar(b, 72, 80) if b['i'] >= 2 else R)
            P['organ'].append(R); P['horn'].append(R)
            P['bass'].append(bass_bar(b, top_up) if b['i'] >= 2 else R)
            P['kit'].append(kit_bar(b, 'light') if b['i'] >= 2 else R)
        elif s == 'verse':
            P['wurli'].append(comp_bar(b, 72)); P['flute'].append(tune_bar(b, 72, 86, shift=3))
            P['organ'].append(R)
            # GUIDE-TONE COUNTER-LINE (the verse's second half): the horn holds the 3rd or the 7th of each chord,
            # whichever is nearest the last note, so a slow line moves by the smallest steps under the flute while
            # the chords leap by thirds
            if b['i'] >= 12:
                pcs = [(b['root'] + Q[b['q']][x]) % 12 for x in (1, 3)]
                cands = [m for m in range(55, 72) if m % 12 in pcs]
                guide[0] = min(cands, key=lambda m: (abs(m - guide[0]), m))
                P['horn'].append([tok(nm(guide[0]), e8 / 2 - 0.1, 74 + (b['i'] - 12)), 'R/0.1b'])
            else:
                P['horn'].append(R)
            P['bass'].append(bass_bar(b, top_up)); P['kit'].append(kit_bar(b, 'light'))
        elif s == 'fuzz':
            # CALL AND RESPONSE: twice (bars 8 and 16) the flute answers the organ with a bar of the kettle tune
            # (re-voiced on the riff's chord); in the last 8 bars the answers stop and the organ doubles itself an octave down
            answer = b['i'] in (7, 15)
            P['wurli'].append(comp_bar(b, 70) if b['i'] % 2 else R)
            P['flute'].append(tune_bar(b, 65, 90) if answer else R)
            sol = solo_bar(b, 92) if not answer else R
            if b['i'] >= 16 and sol is not R:
                sol = [x if x.startswith('R') else (lambda n_, r_: f"{nm(NN.index(n_[:-1]) + 12 * int(n_[-1]))},{n_}/{r_}")(*x.split('/', 1)) for x in sol]
            P['organ'].append(sol); P['horn'].append(R)
            P['bass'].append(riff_bar(b)); P['kit'].append(kit_bar(b, 'fuzz'))
        elif s == 'hymn':
            P['wurli'].append(comp_bar(b, 64)); P['flute'].append(R); P['organ'].append(R)
            P['horn'].append(tune_bar(b, 55, 80, aug=2))
            P['bass'].append([tok(nm(b['root'] - 12), 3.9, 84), 'R/0.1b']); P['kit'].append(kit_bar(b, 'hymn'))
        elif s == 'recap':
            late = b['i'] >= 8
            P['wurli'].append(tune_bar(b, 60, 90)); P['flute'].append(tune_bar(b, 72, 92))
            P['organ'].append(comp_bar(b, 70) if late else R); P['horn'].append(tune_bar(b, 55, 72) if late else R)
            P['bass'].append(bass_bar(b, top_up)); P['kit'].append(kit_bar(b, 'full' if late else 'light'))
    total_beats = sum(b['e8'] for b in B) / 2
    end_s = total_beats * 60 / BPM
    pts, t = [], 0.0
    for b in B:
        lv = -6 if b['sec'] == 'kettle' else -9 if b['sec'] == 'hymn' else (-6 if b['sec'] == 'overture' and b['i'] < 2 else (-3 if b['sec'] == 'verse' else 0))
        pts.append([t, lv]); t += b['e8'] * 0.5 * 60 / BPM
    dyn = [[f'{pts[0][0]:.3f}s', pts[0][1]]]
    for i in range(1, len(pts)):
        if pts[i][1] != pts[i - 1][1]:
            dyn += [[f'{pts[i][0] - 0.8:.3f}s', pts[i - 1][1]], [f'{pts[i][0]:.3f}s', pts[i][1]]]
    J = lambda p: ' | '.join(' '.join(x) for x in P[p])
    return {
        'about': "Chirpers - Odd Hours (Chirpers II), track 5 by chirper-one: CANTERBURY-ISH PROG. Generated by "
                 "compose/chirpers2/src/chirpers2-t5.py; see its docstring and compose/chirpers2/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 3:.2f}s', 'ceiling': '-0.1dB',
        'master': {'fx': [{'type': 'eq', 'bands': ['lowshelf cutoff=180 gain=10dB', 'peak cutoff=700 q=0.7 gain=-3dB', 'highshelf cutoff=10000 gain=-6dB']},
                          {'type': 'gain', 'gain': '+12dB'}, {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 2, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'}],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            {'name': 'wurli', 'patch': 'wurli', 'gain': '-5dB', 'pan': -0.25, 'score': J('wurli')},
            {'name': 'flute', 'patch': 'mellotron-flute', 'gain': '-6dB', 'pan': 0.25, 'score': J('flute')},
            {'name': 'organ', 'patch': 'organ-rock', 'gain': '-8dB', 'pan': 0.1,
             'fx': [{'type': 'drive', 'drive': 0.6, 'mix': 0.7}], 'score': J('organ')},
            {'name': 'bass', 'patch': 'bass-pick-di', 'gain': '-2dB', 'score': J('bass')},
            {'name': 'kit', 'patch': 'room-kit', 'gain': '-4dB', 'score': J('kit')},
            {'name': 'horn', 'patch': 'horn', 'gain': '-6dB', 'pan': -0.1, 'score': J('horn')},
            {'name': 'box', 'patch': 'music-box', 'gain': '-2dB', 'pan': 0.3, 'score': J('box')},
            {'name': 'celesta', 'patch': 'celesta', 'gain': '-4dB', 'pan': -0.3, 'score': J('celesta')},
            {'name': 'clar', 'patch': 'clarinet', 'gain': '-8dB', 'score': J('clar')},
        ]}

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    song = build()
    if out.endswith('.json'):
        json.dump(song, open(out, 'w'), indent=1)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(song, f)
        subprocess.run(['python3', os.path.join(ROOT, 'tools', 'songfmt.py'), 'yaml', f.name, '-o', out], check=True)
        os.unlink(f.name)
    print('wrote', out, song['length'])
