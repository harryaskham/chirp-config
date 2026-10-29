#!/usr/bin/env python3
"""chirpers2-t3 (chirper-one): MATH ROCK WITH MALLETS for 'Odd Hours' (Chirpers II).

Bright, clean, interlocking and fast. ~150 bpm on an eighth grid.
- Every bar is an ADDITIVE GROUPING of 2s and 3s, so bar lengths run 5 to 13 eighths.
- Two tapped clean guitars braid loops of 5 and 7 notes against the groupings, so the braid never lines up the same
  way twice. The kick and bass hit every group start; the snare hits the last.
- A marimba carries the tune.
Form: intro, A, B (half-time marimba), A2, C (a 5/8 breakdown), D (the build: groupings grow by one 3 each bar),
A3, outro.
Emits songs/chirpers2-t3.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers2-t3.yaml")
BPM = 150
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

# THE GROUPING ROW: one grouping per bar, cycling; A sections use ROW_A, B uses ROW_B
ROW_A = [(3, 3, 2), (2, 2, 3), (3, 2, 2, 2), (3, 3, 3, 2), (3, 3, 2), (2, 3), (3, 2, 2, 2), (3, 3, 2, 2, 3)]
ROW_B = [(3, 3, 3, 3), (2, 2, 2, 3, 3), (3, 3, 3, 3), (3, 2, 3, 2, 2)]
ROW_C = [(3, 2)]
def row_d(i): return (2, 2) + (3,) * (1 + i % 6)          # the build: one more 3 each bar, six steps

# chords (pitch sets, MIDI) per bar, cycling
E = 4
CH_A = [[52, 56, 59, 63, 66], [49, 52, 56, 59, 63], [45, 49, 52, 56, 63], [47, 51, 54, 56, 61]]  # Emaj9 C#m9 Amaj7(9) B6/9
CH_B = [[43, 47, 50, 54, 57], [40, 43, 47, 50, 54], [48, 52, 55, 59, 66], [50, 54, 57, 59, 64]]  # Gmaj9 Em9 Cmaj7#11 D6/9

FORM = [('intro', 8, 'A'), ('A', 16, 'A'), ('B', 16, 'B'), ('S', 8, 'S'), ('A2', 16, 'A'), ('C', 8, 'C'), ('D', 12, 'D'),
        ('A3', 16, 'A'), ('outro', 8, 'A')]

def bars():
    out = []
    k = 0
    for name, n, kind in FORM:
        for i in range(n):
            if kind == 'A':
                g = ROW_A[i % len(ROW_A)]; ch = CH_A[(i // 2) % 4]
            elif kind == 'B':
                g = ROW_B[i % len(ROW_B)]; ch = CH_B[(i // 2) % 4]
            elif kind == 'S':          # the solo break: B's harmony on A's row, one chord per bar
                g = ROW_A[i % len(ROW_A)]; ch = CH_B[i % 4]
            elif kind == 'C':
                g = ROW_C[0]; ch = CH_A[(i // 2) % 2 * 2]
            else:
                g = row_d(i); ch = CH_B[i % 4] if i < 6 else CH_A[i % 4]
            if name in ('A3', 'outro'):      # the last return is a whole step up: F# major
                ch = [m + 2 for m in ch]
            out.append({'sec': name, 'i': i, 'n': n, 'g': g, 'e8': sum(g), 'ch': ch, 'k': k})
            k += 1
    return out

def tok(n, beats, vel): return f"{n}/{beats:g}b@{vel}"
def rest(e8): return f"R/{e8 / 2:g}b"

def loop_part(B, length, octv, vel, active, offset=0, step=0.5):
    """a tapped loop: chord tones in a LENGTH-note cycle that runs on across bar lines"""
    pos = offset
    out = []
    for b in B:
        if not active(b):
            out.append([rest(b['e8'])]); continue
        toks = []
        st = step(b) if callable(step) else step
        n_steps = int(round(b['e8'] * 0.5 / st))
        for e in range(n_steps):
            i = pos % length
            ch = b['ch']
            m = ch[(i * 2) % len(ch)] + 12 * octv + (12 if i >= len(ch) else 0)
            accent = vel + (12 if e == 0 else 0) + (14 if i == 0 else 0)
            toks.append(tok(nm(m), st, accent))
            pos += 1
        out.append(toks)
    return out

def groups(b):
    s, at = [], 0
    for g in b['g']:
        s.append((at, g)); at += g
    return s

def bass_part(B, active):
    out = []
    for b in B:
        if not active(b):
            out.append([rest(b['e8'])]); continue
        toks = []
        root = b['ch'][0] - 12 if b['ch'][0] >= 40 else b['ch'][0]
        for j, (at, g) in enumerate(groups(b)):
            m = root + (7 if j % 3 == 2 else 0) + (12 if j == len(b['g']) - 1 and g == 2 else 0)
            toks.append(tok(nm(m), g / 2 - 0.05, 104 if j == 0 else 92))
            toks.append('R/0.05b')
        out.append(toks)
    return out

def kit_part(B, active, half=lambda b: False, tap16=lambda b: False):
    out = []
    for b in B:
        if not active(b):
            out.append([rest(b['e8'])]); continue
        sl = [[] for _ in range(b['e8'])]
        gs = groups(b)
        for j, (at, g) in enumerate(gs):
            if half(b):
                if j == 0: sl[at].append(('k', 112))
                if j == len(gs) - 1 and len(gs) > 1: sl[at].append(('s', 108))
            else:
                sl[at].append(('k', 112 if j == 0 else 98))
                if j == len(gs) - 1: sl[at].append(('s', 114))
        if b['i'] == 0 and b['sec'] not in ('intro',):
            sl[0].append(('c', 112))
        # HATS IN DOTTED EIGHTHS: sixteenths accented every third one (3 against the eighth grid) where the band
        # taps; plain eighths elsewhere
        toks = []
        for e in range(b['e8']):
            for h in (0, 1):
                p = list(sl[e]) if h == 0 else []
                if tap16(b):
                    n16 = e * 2 + h
                    p.append(('h', 94 if n16 % 3 == 0 else 52))
                    # GHOSTS: a soft snare on the sixteenth before each group start (the pick-up that pushes the bar)
                    if h == 1 and any(at == e + 1 for at, g in groups(b)[1:]):
                        p.append(('s', 60))
                elif h == 0:
                    p.append(('h', 86 if e % 2 == 0 else 66))
                toks.append((','.join(sorted({x[0] for x in p})) + f'/0.25b@{max(x[1] for x in p)}') if p else 'R/0.25b')
        out.append(toks)
    return out

TUNE = [0, 2, 4, 3, 1, 4, 2, 0]          # chord-tone indices: the marimba tune walks the chord
def marimba_part(B, active):
    out = []
    for b in B:
        if not active(b):
            out.append([rest(b['e8'])]); continue
        toks = []
        if b['sec'] in ('A3', 'D'):
            # DOTTED: in the build and the last return the marimba runs dotted eighths straight through the groupings
            n16 = b['e8'] * 2
            t16 = 0
            while t16 < n16:
                ln = min(3, n16 - t16)
                ci = TUNE[(b['k'] * 3 + t16 // 3) % len(TUNE)]
                toks.append(tok(nm(b['ch'][ci] + 24), ln / 4, 94 if t16 == 0 else 82))
                t16 += ln
        else:
            for j, (at, g) in enumerate(groups(b)):
                ci = TUNE[(b['k'] + j) % len(TUNE)]
                toks.append(tok(nm(b['ch'][ci] + 24), g / 2, 92 if j == 0 else 80))
        out.append(toks)
    return out

SOLO_SHAPES = [(0, 2, 4, 7, 9, 7, 4, 2), (0, 4, 7, 11, 9, 7, 4, 0), (2, 4, 6, 9, 11, 9, 6, 4), (0, 3, 7, 10, 12, 10, 7, 3)]
def solo_part(B):
    """THE TAPPED SOLO (section S): the left guitar breaks out of its 5-loop into wide two-octave tapping arpeggios in
    sixteenths. Each group of the bar's grouping gets its own shape climbing from a new chord tone, the shapes widen
    bar by bar, and the last two bars climb an octave for the hand-off back to the braid."""
    out = []
    for b in B:
        if b['sec'] != 'S':
            out.append([rest(b['e8'])]); continue
        toks, ch = [], b['ch']
        oct_up = 12 if b['i'] >= 6 else 0
        for j, (at, g) in enumerate(groups(b)):
            shape = SOLO_SHAPES[(b['i'] + j) % len(SOLO_SHAPES)]
            base = ch[(j + b['i']) % len(ch)] + 24 + oct_up
            for n in range(g * 2):
                toks.append(tok(nm(base + shape[n % len(shape)] + (12 if b['i'] >= 3 and n >= 4 else 0)), 0.25, 96 if n == 0 else (84 if n % 2 == 0 else 74)))
        out.append(toks)
    return out

def dialogue(B, solo, mar):
    """A2's DIALOGUE: over the braid, the soloist and the marimba talk in 2-bar turns. The guitar CALLS with a short
    tapping shape (the first two groups of the bar, then air); the marimba ANSWERS the next bar with the same notes in
    its register at half speed, the shape turned upside down every other time, so each answer bends the question."""
    last = None
    for k, b in enumerate(B):
        if b['sec'] != 'A2':
            continue
        turn = b['i'] % 2
        if turn == 0:
            ch, toks, notes, t = b['ch'], [], [], 0
            for j, (at, g) in enumerate(groups(b)[:2]):
                shape = SOLO_SHAPES[(b['i'] // 2 + j) % len(SOLO_SHAPES)]
                base = ch[j % len(ch)] + 24
                for n in range(g * 2):
                    m = base + shape[n % len(shape)]
                    toks.append(tok(nm(m), 0.25, 96 if n == 0 else 80)); notes.append(m); t += 1
            toks.append(f"R/{(b['e8'] * 2 - t) / 4:g}b")
            solo[k] = toks; last = notes
        elif last:
            seq = last if (b['i'] // 2) % 2 == 0 else [2 * last[0] - m for m in last]   # inverted around its first note
            toks, t = [], 0
            for m in seq[: b['e8']]:
                toks.append(tok(nm(m), 0.5, 90 if t == 0 else 78)); t += 1
            if t < b['e8']:
                toks.append(f"R/{(b['e8'] - t) / 2:g}b")
            mar[k] = toks

def stop_after_one(parts, B, sec, i):
    """THE STOP: in bar I of SEC everything plays its first note and then rests to the bar line"""
    for p in parts:
        for k, b in enumerate(B):
            if b['sec'] == sec and b['i'] == i and p[k] and not p[k][0].startswith('R'):
                first = p[k][0]
                dur = float(first.split('/')[1].split('b')[0])
                p[k] = [first, f"R/{b['e8'] / 2 - dur:g}b"] if b['e8'] / 2 - dur > 0 else [first]

def build():
    B = bars()
    full = lambda b: b['sec'] in ('A', 'A2', 'A3', 'B', 'D', 'S')
    TAP = lambda b: 0.25 if b['sec'] in ('A', 'A2', 'A3', 'D') else 0.5     # tapping sixteenths where the band plays
    g1 = loop_part(B, 5, 1, 70, lambda b: b['sec'] not in ('B', 'S', 'outro') or (b['sec'] == 'B' and b['i'] % 2 == 0) or (b['sec'] == 'outro' and b['i'] < 4), step=TAP)
    g2 = loop_part(B, 7, 1, 64, lambda b: (b['sec'] != 'intro' or b['i'] >= 4) and b['sec'] not in ('outro', 'S') and not (b['sec'] == 'C' and b['i'] < 4), offset=3)
    bass = bass_part(B, lambda b: full(b) or (b['sec'] == 'C' and b['i'] >= 4))
    kit = kit_part(B, lambda b: full(b), half=lambda b: b['sec'] == 'B', tap16=lambda b: b['sec'] in ('A', 'A2', 'A3', 'D', 'B', 'S'))
    mar = marimba_part(B, lambda b: b['sec'] in ('B', 'A3', 'D') or (b['sec'] == 'outro' and b['i'] < 4))
    # THE LAST WORD (outro): the braid stops after four bars and the marimba is left alone with the GLASS TUNE, its
    # notes lengthening bar by bar (eighths, dotted eighths, quarters, then one held roll on the tonic chord)
    for k, b in enumerate(B):
        if b['sec'] == 'outro' and b['i'] >= 4:
            j = b['i'] - 4
            if j == 3:
                ch = ','.join(nm(m + 26) for m in CH_A[0][:4])   # the home chord of the last key (F#maj7)
                mar[k] = [f"{ch}/{b['e8'] / 2 - 0.25:g}b@70", 'R/0.25b']
                continue
            step16 = (2, 3, 4)[j]
            toks, t16, n16, q = [], 0, b['e8'] * 2, 0
            while t16 < n16:
                ln = min(step16, n16 - t16)
                toks.append(tok(nm(b['ch'][TUNE[(b['k'] + q) % len(TUNE)]] + 24), ln / 4, 84 - 6 * j)); t16 += ln; q += 1
            mar[k] = toks
    solo = solo_part(B)
    dialogue(B, solo, mar)
    # THE CELL, answered (breakdown C, 3+2): chirper-two's Mallet Chamber in Phase (t8) phases a 12-eighth marimba
    # CELL (degrees 0 4 8 4 2 4 | 5 4 1 4 2 6); here two marimbas play it in eighths over the 5/8 breakdown in each
    # chord's lydian, running across the bar lines (12 against 5), in unison for four bars, then the second steps
    # an eighth ahead: t8's process in miniature, inside the math rock
    T8CELL = [0, 4, 8, 4, 2, 4, 5, 4, 1, 4, 2, 6]
    LYD = [0, 2, 4, 6, 7, 9, 11]
    mar2 = []
    pos = 0
    for k, b in enumerate(B):
        if b['sec'] != 'C':
            mar2.append([rest(b['e8'])]); continue
        root = b['ch'][0] % 12 + 60
        def cellnote(q):
            d = T8CELL[q % 12]
            return nm(root + LYD[d % 7] + 12 * (d // 7))
        mar[k] = [tok(cellnote(pos + e), 0.5, 88 if (pos + e) % 12 == 0 else 74) for e in range(b['e8'])]
        ahead = 1 if b['i'] >= 4 else 0
        mar2.append([tok(cellnote(pos + e + ahead), 0.5, 84 if (pos + e + ahead) % 12 == 0 else 70) for e in range(b['e8'])])
        pos += b['e8']
    # GLASS: on the last return (A3, a whole step up) a glockenspiel doubles the marimba's dotted line an octave
    # up on every group's first note only, a sparkle that marks the key change
    glock = []
    for k, b in enumerate(B):
        if b['sec'] == 'A3' and mar[k] and not mar[k][0].startswith('R'):
            line, t16, starts = [], 0, {at * 2 for at, g in groups(b)}
            for x in mar[k]:
                n_, r_ = x.split('/', 1)
                ln = float(r_.split('b')[0])
                if t16 in starts and not n_.startswith('R'):
                    line.append(f"{nm(NN.index(n_[:-1]) + 12 * (int(n_[-1]) + 1) + 12)}/{ln:g}b@{80}")
                else:
                    line.append(f"R/{ln:g}b")
                t16 += int(round(ln * 4))
            glock.append(line)
        else:
            glock.append([rest(b['e8'])])
    # the build ends in a STOP: its last bar is one unison hit and a bar of air before the last return
    stop_after_one([g1, g2, bass, kit, mar], B, 'D', 11)
    total_beats = sum(b['e8'] for b in B) / 2
    end_s = total_beats * 60 / BPM
    # DYNAMICS: the quiet sections sit 7 dB under the band (a lane on the master; ramps of one bar)
    pts, t = [], 0.0
    for b in B:
        lv = -7 if b['sec'] in ('intro', 'C') else (-3 if b['sec'] == 'B' else 0)
        pts.append([f'{t:.3f}s', lv]); t += b['e8'] * 0.5 * 60 / BPM
    lane = [pts[0]] + [p for i, p in enumerate(pts[1:], 1) if p[1] != pts[i - 1][1]]
    dyn = []
    for i, p in enumerate(lane):
        if i: dyn.append([f'{float(p[0][:-1]) - 0.6:.3f}s', lane[i - 1][1]])
        dyn.append(p)
    J = lambda p: ' | '.join(' '.join(x) for x in p)
    return {
        'about': "Chirpers - Odd Hours (Chirpers II), track 3 by chirper-one: MATH ROCK WITH MALLETS. Generated by "
                 "compose/chirpers2/src/chirpers2-t3.py; see its docstring and compose/chirpers2/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 3:.2f}s', 'ceiling': '-0.1dB',
        'master': {'fx': [{'type': 'eq', 'bands': ['lowshelf cutoff=150 gain=8dB', 'peak cutoff=640 q=0.7 gain=-4dB', 'peak cutoff=1300 q=1 gain=-4dB', 'peak cutoff=7000 q=0.8 gain=5dB', 'highshelf cutoff=12000 gain=-5dB']},
                          {'type': 'gain', 'gain': '+14dB'}, {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 2, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   'auto': {'dyn': {'points': dyn}, 'fade': {'points': [['0s', 0], [f'{end_s - 8:.1f}s', 0], [f'{end_s:.1f}s', -40]]}}},
        'tracks': [
            {'name': 'gtr1', 'patch': 'starcaster-clean', 'gain': '-6dB', 'pan': -0.5, 'score': J(g1)},
            {'name': 'gtr2', 'patch': 'clean-dry', 'gain': '-7dB', 'pan': 0.5, 'score': J(g2)},
            {'name': 'bass', 'patch': 'bass-pick-di', 'gain': '-2dB', 'score': J(bass)},
            {'name': 'kit', 'patch': 'prog-kit', 'gain': '-4dB', 'score': J(kit)},
            {'name': 'solo', 'patch': 'starcaster-clean', 'gain': '-4dB', 'pan': -0.3, 'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.3, 'mix': 0.25}], 'score': J(solo)},
            {'name': 'marimba', 'patch': 'marimba', 'gain': '-4dB', 'pan': 0.1, 'score': J(mar)},
            {'name': 'mar2', 'patch': 'marimba', 'gain': '-5dB', 'pan': -0.45, 'score': J(mar2)},
            {'name': 'glock', 'patch': 'glock', 'gain': '-10dB', 'pan': 0.4, 'score': J(glock)},
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
