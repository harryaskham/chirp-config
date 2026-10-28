#!/usr/bin/env python3
"""chirpers1-t8 "The Long Unwinding" (chirper-one): Ferrous Bloom's closer, ~494 s at 96 BPM (bar = 2.5 s).

The album's motifs come home and come apart. Movements (bars):
  A  1-24    dawn: COLD CHORD pad (t5) and LATTICE's F-Gb-B-E line on the clean, walking on the 3+2+2 cell (t1)
  B  25-56   gathering: a 5-note clean arpeggio (LATTICE's 5-cell diminution as a figure, 5 against 8), bass roots,
             ride and toms in crescendo, a low swell; Phrygian pads (Fm add9 / Dbmaj7 / Bbm / Gb)
  C1 57-80   the cog, half time: LATTICE's 7-cell (x..x.x.) as F1 chugs, an F1+B1 tritone stab every 4th cell
  C2 81-104  the cog, full time: the root moves F -> Gb (t5's minor 2nd) every 7 bars, hats on eighths
  D1 105-120 the climb: an 11-cell (3+2+2+2+2) with a B tritone stab; the CLIMB LINE on the lead
  D2 121-136 t5's EXHALE in augmentation x2 on the lead over the 11-cell
  E  137-152 the crush: half-time blocks F / Gb / F-Ab / B, ending on the album's cluster F1 B1 E2 (+Gb5)
  F1 153-172 dissolve: t5's BREATH CELL (F3 C4 E4 B4 G4) on 16ths over the COLD CHORD
  F2 173-196 the end: the BREATH CELL slowing, then LATTICE's line in long notes, the F-B-E cluster rings to silence

Emits songs/chirpers1-t8.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers1-t8.yaml")
BPM, NB = 96, 196
SPB = 60 / BPM

NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def trn(n, k):
    if not k: return n
    p, o = n[:-1], int(n[-1]); p = {'F#': 'Gb', 'C#': 'Db'}.get(p, p)
    v = NN.index(p) + 12 * o + k
    return f'{NN[v % 12]}{v // 12}'

def join(barmap):
    return ' | '.join(' '.join(barmap.get(m) or ['R/4b']) for m in range(1, NB + 1))

def merge(*ds):
    o = {}
    for d in ds:
        o.update(d)
    return o

def stream16(a, b, fn):
    """per bar 16 sixteenth slots; fn(global_index) -> token body (e.g. 'F1@100^pm') or None; returns {bar: tokens}"""
    out = {}
    i = 0
    for m in range(a, b + 1):
        toks = []
        for s in range(16):
            c = fn(i); i += 1
            if c is None:
                toks.append('R/0.25b')
            else:
                n, rest = (c.split('@', 1) + ['100'])[:2] if '@' in c else (c, '100')
                vel, art = (rest.split('^', 1) + [''])[:2] if '^' in rest else (rest, '')
                toks.append(f'{n}/0.25b@{vel}' + (f'^{art}' if art else ''))
        out[m] = toks
    return out

def drum_bar(slots):
    toks = []
    for s in slots:
        if s:
            v = max(x[1] for x in s)
            toks.append(','.join(sorted({x[0] for x in s})) + f'/0.25b@{v}')
        else:
            toks.append('R/0.25b')
    return toks

# ---------------- harmony ----------------
COLD = 'F2,C3,E3,B3,G4'                       # t5's COLD CHORD (F lydian colour, no third)
PADS = ['F2,C3,Ab3,G4', 'Db2,Ab2,C4,G4', 'Bb1,F2,Db3,Ab3', 'Gb2,Db3,Bb3,F4']
ROOTS = ['F1', 'Db1', 'Bb0', 'Gb1']
CLUSTER = 'F1,B1,E2'                           # t1's closing cluster
def pad_phryg(m, vel):
    return [f'{PADS[((m - 1) // 2) % 4]}/4b@{vel}']

# ---------------- A: LATTICE line on the 3+2+2 cell ----------------
LAT_LINE = ['F3', 'Gb3', 'B3', 'E4']
def lattice_clean(a, b, vel=66, octave=0):
    k = [0]
    def fn(i):
        p = i % 7
        if p in (0, 3, 5):
            n = LAT_LINE[k[0] % 4]; k[0] += 1
            if octave:
                n = n[:-1] + str(int(n[-1]) + octave)
            return f'{n}@{vel}'
        return None
    return stream16(a, b, fn)

# ---------------- B: the 5-note arpeggio on eighths ----------------
ARP5 = ['F3', 'C4', 'Ab4', 'G4', 'Db4']
GOVERNOR = ['F3', 'B3', 'E4', 'F4', 'Gb4', 'F4', 'E4', 'B3', 'F3', 'Gb3', 'B3', 'C4', 'E4']   # t6's line, an octave down
def arp(a, b, cell, step, vel):
    out = {}; i = 0
    for m in range(a, b + 1):
        toks = []; t = 0.0
        while t < 4 - 1e-9:
            toks.append(f'{cell[i % len(cell)]}/{step:g}b@{vel}'); i += 1; t += step
        out[m] = toks
    return out

# ---------------- C: the cog (LATTICE 7-cell chugs) ----------------
def cog(a, b, roots, full_time):
    """7-cell 3+2+2: onsets 0,3,5; every 4th cell's first onset is a tritone stab. roots: function(bar)->(root, fifth)"""
    g, bs, hits = {}, {}, {}
    i = 0
    for m in range(a, b + 1):
        r, tri = roots(m)
        gt, bt, ht = [], [], []
        for s in range(16):
            p, cellno = i % 7, i // 7; i += 1
            if p == 0 and cellno % 4 == 3:
                gt.append(f'{r},{tri}/0.25b@122'); bt.append(f'{r}/0.25b@118'); ht.append('stab')
            elif p == 0:
                gt.append(f'{r}/0.25b@116^pm'); bt.append(f'{r}/0.25b@112'); ht.append('acc')
            elif p in (3, 5):
                gt.append(f'{r}/0.25b@104^pm'); bt.append(f'{r}/0.25b@100'); ht.append('pm')
            else:
                gt.append('R/0.25b'); bt.append('R/0.25b'); ht.append(None)
        g[m], bs[m], hits[m] = gt, bt, ht
    return g, bs, hits

# ---------------- t2's TRIAD: the 7-cell's three rotations chained (21 sixteenths) ----------------
TRIAD = [(0, 'F1/0.25b@118'), (3, 'F1/0.25b@104^pm'), (5, 'F1/0.25b@104^pm'),
         (7, 'Gb1/0.25b@118'), (9, 'F1/0.25b@104^pm'), (12, 'F1/0.25b@104^pm'),
         (14, 'F1,E2/0.25b@122'), (16, 'F1/0.25b@104^pm'), (18, 'F1/0.25b@104^pm')]
def triad(a, b):
    on = dict(TRIAD); g, bs, hits = {}, {}, {}; i = 0
    for m in range(a, b + 1):
        gt, bt, ht = [], [], []
        for s in range(16):
            p = i % 21; i += 1
            c = on.get(p)
            if c is None:
                gt.append('R/0.25b'); bt.append('R/0.25b'); ht.append(None)
            else:
                gt.append(c); bt.append(c.split(',')[0].split('/')[0] + '/0.25b@' + c.split('@')[1].split('^')[0])
                ht.append('stab' if p == 14 else 'acc' if p in (0, 7) else 'pm')
        g[m], bs[m], hits[m] = gt, bt, ht
    return g, bs, hits

# ---------------- D: the 11-cell (3+2+2+2+2) ----------------
def climb(a, b, k=0):
    g, bs, hits = {}, {}, {}
    i = 0
    on = {0: 'F1,C2,F2@118', 3: 'F1@104^pm', 5: 'Gb1@108', 7: 'B1,F#2,B2@122', 9: 'Ab1@106'}
    on = {q: ','.join(trn(x, k) for x in c.split('@')[0].split(',')) + '@' + c.split('@')[1] for q, c in on.items()}
    for m in range(a, b + 1):
        gt, bt, ht = [], [], []
        for s in range(16):
            p = i % 11; i += 1
            c = on.get(p)
            if c is None:
                gt.append('R/0.25b'); bt.append('R/0.25b'); ht.append(None)
            else:
                n, rest = c.split('@'); vel, art = (rest.split('^') + [''])[:2]
                gt.append(f'{n}/0.25b@{vel}' + (f'^{art}' if art else '')); bt.append(f'{n.split(",")[0]}/0.25b@{vel}')
                ht.append('stab' if p == 7 else 'acc' if p == 0 else 'pm')
        g[m], bs[m], hits[m] = gt, bt, ht
    return g, bs, hits

# ---------------- drums ----------------
def drums_build(a, b):
    out = {}
    for m in range(a, b + 1):
        p = (m - a) / max(1, b - a); v = int(55 + 50 * p)
        sl = [[] for _ in range(16)]
        for s in range(0, 16, 4 if m < a + 16 else 2):
            sl[s].append(('rd', v))
        sl[0].append(('k', v + 5))
        if m >= a + 16:
            sl[8].append(('s', v)); sl[10].append(('k', v))
        if (m - a) % 8 == 7 or m == b:
            for s, t in zip(range(8, 16), ['t1', 't1', 't2', 't2', 't3', 't3', 'ft', 'ft']):
                sl[s] = [(t, min(120, v + 10))]
        out[m] = drum_bar(sl)
    return out

def drums_cell(a, b, hits, full_time, crash_every):
    out = {}
    for m in range(a, b + 1):
        sl = [[] for _ in range(16)]
        for s, h in enumerate(hits[m]):
            if h: sl[s].append(('k', 114 if h != 'pm' else 102))
            if h == 'stab': sl[s].append(('x', 104))
        for s in (range(0, 16, 2) if full_time else (0, 4, 8, 12)):
            sl[s].append(('h', 86 if s % 4 == 0 else 70))
        if full_time:
            sl[4].append(('s', 116)); sl[12].append(('s', 118))
        else:
            sl[8].append(('s', 118))
        if (m - a) % crash_every == 0:
            sl[0].append(('c', 118))
        out[m] = drum_bar(sl)
    return out

def drums_crush(a, b):
    out = {}
    for m in range(a, b + 1):
        sl = [[] for _ in range(16)]
        if m == b:
            sl[0] += [('c', 127), ('k', 127), ('x', 120)]
            out[m] = drum_bar(sl); continue
        sl[0] += [('c', 124), ('k', 124)]; sl[8] += [('s', 124), ('k', 110)]
        sl[6].append(('k', 108)); sl[14].append(('k', 104))
        for s in (4, 12): sl[s].append(('c', 100))
        if (m - a) % 4 == 3:
            for s, t in zip(range(8, 16), ['t1', 't2', 't2', 't3', 't3', 'ft', 'ft', 'ft']):
                sl[s] = [(t, 120)] + ([('k', 110)] if s % 2 == 0 else [])
        out[m] = drum_bar(sl)
    return out

# ---------------- E: crush blocks ending on the cluster ----------------
BLOCKS = [['F1,C2,F2/2b@124', 'F1,C2,F2/1.5b@118^pm', 'R/0.5b'],
          ['Gb1,Db2,Gb2/2b@124', 'Gb1,Db2,Gb2/1.5b@118^pm', 'R/0.5b'],
          ['F1,C2,F2/2b@124', 'Ab1,Eb2,Ab2/2b@120'],
          ['B1,F#2,B2/3b@126', 'R/1b']]
def crush(a, b):
    g, bs = {}, {}
    for m in range(a, b + 1):
        if m == b:
            g[m] = [f'{CLUSTER}/4b@127']; bs[m] = ['F1/4b@124']; continue
        blk = BLOCKS[(m - a) % 4]; g[m] = blk
        bs[m] = [t if t.startswith('R') else t.split(',')[0] + '/' + t.split('/', 1)[1].split('^')[0] for t in blk]
    return g, bs

# ---------------- leads ----------------
CLIMB = [['Ab4/2b@96', 'G4/2b@92'], ['F4/1b@90', 'C5/3b@100'], ['Bb4/2b@96', 'Ab4/1b@92', 'G4/1b@90'], ['F4/4b@92'],
         ['Ab4/2b@98', 'Bb4/2b@98'], ['C5/1b@100', 'Db5/3b@108'], ['C5/2b@100', 'Bb4/1b@96', 'Ab4/1b@94'], ['G4/2b@96', 'B4/2b@104']]
EXHALE2 = [['E5/4b@108'], ['B4/2b@102', 'C5/2b@104'], ['G4/4b@100'], ['G4/2b@98', 'A4/2b@100'],   # t5's EXHALE x2
           ['E5/3b@110', 'D5/1b@104'], ['B4/4b@104'], ['F4/4b@100'], ['F4/4b@96']]
CRUSHL = [['C5/4b@110'], ['Db5/4b@112'], ['C5/2b@110', 'Bb4/2b@106'], ['B4/4b@114']]
def cyc(a, b, phr):
    return {m: phr[(m - a) % len(phr)] for m in range(a, b + 1)}

# ---------------- F: BREATH CELL (t5) and the last LATTICE ----------------
BREATH = ['F3', 'C4', 'E4', 'B4', 'G4']
# t7 'Iron Stairs': its LATTICE RISING phrase, half speed, as a memory in the dissolve
STAIRS_ECHO = [['F4/4b@64'], ['Gb4/2b@62', 'B4/2b@64'], ['E5/4b@66'], ['D5/2b@62', 'C5/2b@60'], ['B4/4b@60'], ['Gb4/4b@58'],
               ['F4/2b@56', 'B4/2b@56'], ['E5/4b@54']]
def breath16(a, b, vel):
    return stream16(a, b, lambda i: f'{BREATH[i % 5]}@{vel}')

def build():
    A, B = (1, 24), (25, 56)
    C1, C2 = (57, 80), (81, 104)
    D1, D2 = (105, 120), (121, 136)
    E = (137, 152)
    F1, F2 = (153, 172), (173, NB)
    pad = merge({m: [f'{COLD}/4b@{60 if m < 9 else 66}'] for m in range(*A)} | {A[1]: [f'{COLD}/4b@66']},
                {m: pad_phryg(m, 72) for m in range(B[0], B[1] + 1)},
                {m: pad_phryg(m, 48) for m in range(C2[0], C2[1] + 1)},
                {m: pad_phryg(m, 80) for m in range(E[0], E[1])},
                {m: [f'{COLD}/4b@70'] for m in range(F1[0], F2[0])},
                {m: ['Db2,Ab2,C4,G4/4b@60'] for m in range(F2[0], F2[0] + 8)},
                {m: [f'{COLD}/4b@58'] for m in range(F2[0] + 8, NB - 8)},
                {m: [f'{CLUSTER[3:]},E3,B3,Gb5/4b@62'] if False else [f'F2,B2,E3,Gb4/4b@60'] for m in range(NB - 8, NB - 1)})
    clean = merge(lattice_clean(5, A[1], 62), arp(B[0], B[0] + 15, GOVERNOR, 0.5, 72), arp(B[0] + 16, B[1], ARP5, 0.5, 74),
                  breath16(F1[0], F1[1], 66),
                  arp(F2[0], F2[0] + 7, BREATH, 0.5, 60), arp(F2[0] + 8, F2[0] + 13, BREATH, 1.0, 56),
                  {m: [f'{LAT_LINE[(m - F2[0] - 14) % 4][:-1]}{int(LAT_LINE[(m - F2[0] - 14) % 4][-1]) + 1}/4b@54']
                   for m in range(F2[0] + 14, NB - 1)})
    gC1, bC1, hC1 = cog(*C1, lambda m: ('F1', 'B1'), False)
    AXIS = [('F1', 'B1'), ('Ab1', 'D2'), ('B1', 'F2'), ('D2', 'Ab2')]   # t4's minor-third axis
    gC2, bC2, hC2 = cog(*C2, lambda m: AXIS[((m - C2[0]) // 6) % 4], True)
    gD, bD, hD = {}, {}, {}
    for q, k in enumerate((0, 4, 8, 0)):   # t3's THIRDS WHEEL: F -> A -> C# -> F, 4 bars each
        g_, b_, h_ = climb(D1[0] + 4 * q, D1[0] + 4 * q + 3, k=k); gD.update(g_); bD.update(b_); hD.update(h_)
    gD2, bD2, hD2 = climb(*D2, k=3)
    gD.update(gD2); bD.update(bD2)
    gT, bT, hT = triad(C1[0] + 12, C1[1] - 1)   # t2's TRIAD takes over the cog's second half
    gC1.update(gT); bC1.update(bT); hC1.update(hT)
    gC1[C1[1]] = [f'{CLUSTER}/2b@124', 'R/2b']; bC1[C1[1]] = ['F1/2b@120', 'R/2b']
    gE, bE = crush(*E)
    gtr = merge({m: ['F1,C2/4b@70'] for m in range(B[1] - 7, B[1] + 1)}, gC1, gC2, gD, gE)
    bass = merge({m: [f'{ROOTS[((m - 1) // 2) % 4]}/4b@84'] for m in range(B[0], B[1] + 1)}, bC1, bC2, bD, bE)
    drums = merge(drums_build(*B), drums_cell(*C1, hC1, False, 7), drums_cell(*C2, hC2, True, 7),
                  drums_cell(*D1, hD, True, 11), drums_cell(*D2, hD2, False, 11), drums_crush(*E),
                  {C1[1]: drum_bar([[('c', 126), ('k', 126), ('x', 118)]] + [[]] * 15)})
    lead = merge(cyc(D1[0], D1[1], CLIMB), cyc(D2[0], D2[1], EXHALE2), cyc(E[0], E[1] - 1, CRUSHL),
                 {E[1]: ['Gb5/4b@116']})
    ECHO = {F1[0] + 4 + i: [t] if isinstance(t, str) else t for i, t in enumerate(STAIRS_ECHO)}   # t7's LATTICE RISING, remembered
    # ---- the sound playground (Harry, 28 Oct): three new rigs traded against the m8 pair ----
    # FUZZ: the crush's second half doubled by an octave-down, bit-crushed m8 (the crush grows a sub-floor)
    FUZZ = {m: gE[m] for m in range(E[0] + 8, E[1] + 1)}
    # RING: the climb's tritone stabs alone, through a ring modulator (hocketed against the pair's chugs)
    hits_all = dict(hD); hits_all.update(hD2)
    RING = {}
    for m in range(D1[0], D2[1] + 1):
        RING[m] = [tk if h == 'stab' else 'R/0.25b' for tk, h in zip(gD[m], hits_all[m])]
    # HALO: LATTICE's line as long frozen notes over the dissolve's breath cell (e-bow-like sustain, octave shimmer)
    HALO = {F1[0] + i: [f'{LAT_LINE[(i // 5) % 4][:-1]}{int(LAT_LINE[(i // 5) % 4][-1]) + 1}/4b@70'] for i in range(F1[1] - F1[0] + 1)}
    end_s = NB * 4 * SPB
    fade0 = (F2[0] + 6) * 4 * SPB
    return {
        'about': 'Chirpers - Ferrous Bloom, track 8 "The Long Unwinding" (outro) by chirper-one. Generated by '
                 'compose/chirpers1/src/chirpers1-t8.py; see its docstring and compose/chirpers1/motifs.md.',
        'tempo': BPM, 'length': f'{end_s + 4:.2f}s', 'ceiling': '-0.1dB',
        'master': {'fx': [{'type': 'eq', 'bands': ['peak cutoff=420 q=0.7 gain=-4dB', 'highshelf cutoff=3000 gain=2dB']}, {'type': 'gain', 'gain': '+15.5dB'},
                          {'type': 'compressor', 'threshold': '-14dB', 'ratio': 2.5, 'attack': '10ms', 'release': '120ms', 'makeup': '5dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   'auto': {'fade': {'points': [['0s', -17], ['10s', 0], [f'{fade0:.1f}s', 0],
                                                [f'{end_s - 12:.1f}s', -30], [f'{end_s:.1f}s', -70]]}}},
        'tracks': [
            {'name': 'pad', 'patch': 'juno-pad', 'gain': '-9dB', 'score': join(pad)},
            {'name': 'clean', 'patch': 'm8-clean', 'gain': '-8dB', 'pan': 0.2, 'score': join(clean)},
            {'name': 'gtr-l', 'patch': 'm8-emg-l', 'gain': '-5dB', 'pan': -1, 'score': join(gtr)},
            {'name': 'gtr-r', 'patch': 'm8-emg-r', 'gain': '-5dB', 'pan': 1, 'score': join(gtr)},
            {'name': 'bass', 'patch': 'bass-fat', 'gain': '-4dB', 'score': join(bass)},
            {'name': 'drums', 'patch': 'metal-kit-punch', 'gain': '-2dB', 'score': join(drums)},
            {'name': 'echo', 'patch': 'm8-clean', 'gain': '-11dB', 'pan': 0.35, 'score': join(ECHO)},
            {'name': 'lead', 'patch': 'm8-lead', 'gain': '-8dB', 'pan': -0.15, 'score': join(lead)},
            {'name': 'fuzz', 'patch': 'm8-emg-r', 'gain': '-7dB', 'pan': 0,
             'fx': [{'type': 'pitch', 'semitones': -12, 'mix': 0.6}, {'type': 'crush', 'bits': 8, 'rate': 1, 'mix': 0.25}],
             'score': join(FUZZ)},
            {'name': 'ring', 'patch': 'm8-emg-l', 'gain': '-9dB', 'pan': 0.35,
             'fx': [{'type': 'ring', 'freq': 233, 'mix': 0.6}], 'score': join(RING)},
            {'name': 'halo', 'patch': 'm8-clean', 'gain': '-13dB', 'pan': -0.3,
             'fx': [{'type': 'freeze', 'hold': 1, 'size': 0.8, 'mix': 0.5}, {'type': 'pitch', 'semitones': 12, 'mix': 0.25}],
             'score': join(HALO)},
        ]}

# ---- guitar-like lead expression (chirper-one, tone push / bd-90c9d2): ^f0 paths on m8-lead via a song-local twin ----
import re as _re
_NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
_AL = {'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'}
def _mid(n):
    m = _re.match(r'([A-G][#b]?)(-?\d)$', n); return _NN.index(_AL.get(m[1], m[1])) + 12 * int(m[2])
def guitarize(song, tracks=('lead',)):
    """long notes (>= 2 beats) scoop up a semitone into the note; a note within 5 semitones of the previous held note
    slides from it (^f0 cents paths); the lead patch gets a twin binding pitch to expr.f0 (amount 0.01)."""
    pats = song.setdefault('patches', {})
    def path(vals): return '^f0=' + '>'.join(str(int(round(v))) for v in vals)
    for t in song['tracks']:
        if t['name'] not in tracks:
            continue
        if t['patch'].split()[0] == 'm8-lead':
            pats['m8-lead-f0'] = {'extends': t['patch'], 'synth': {'pitch': {'value': 0, 'mod': [
                {'src': 'lfo.vib', 'amount': 0.3}, {'src': 'expr.f0', 'amount': 0.01}]}}}
            t['patch'] = 'm8-lead-f0'
        prev, nb = None, []
        for bar in t['score'].split(' | '):
            o = []
            for tk in bar.split(' '):
                m = _re.match(r'([A-G][#b]?-?\d)/([0-9.]+)b(.*)$', tk)
                if not m:
                    if tk.startswith('R'):
                        prev = None
                    o.append(tk); continue
                n, dur, rest = m[1], float(m[2]), m[3]
                p = _mid(n)
                if dur >= 2:
                    vals = [-100 + 100 * min(1, i / 1.5) for i in range(9)]
                elif prev is not None and 0 < abs(p - prev) <= 5:
                    d0 = (prev - p) * 100
                    vals = [d0 * max(0, 1 - i / 1.2) for i in range(9)]
                else:
                    vals = None
                o.append(tk if vals is None else f'{n}/{m[2]}b{rest}{path(vals)}')
                prev = p
            nb.append(' '.join(o))
        t['score'] = ' | '.join(nb)
    return song

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    song = guitarize(build())
    if out.endswith('.json'):
        json.dump(song, open(out, 'w'), indent=1)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(song, f)
        subprocess.run(['python3', os.path.join(ROOT, 'tools', 'songfmt.py'), 'yaml', f.name, '-o', out], check=True)
        os.unlink(f.name)
    print('wrote', out, song['length'])
