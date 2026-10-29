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

FORM = [('intro', 8, 'A'), ('A', 16, 'A'), ('B', 16, 'B'), ('A2', 16, 'A'), ('C', 8, 'C'), ('D', 12, 'D'),
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

def build():
    B = bars()
    full = lambda b: b['sec'] in ('A', 'A2', 'A3', 'B', 'D')
    TAP = lambda b: 0.25 if b['sec'] in ('A', 'A2', 'A3', 'D') else 0.5     # tapping sixteenths where the band plays
    g1 = loop_part(B, 5, 1, 70, lambda b: b['sec'] != 'B' or b['i'] % 2 == 0, step=TAP)
    g2 = loop_part(B, 7, 1, 64, lambda b: (b['sec'] != 'intro' or b['i'] >= 4) and b['sec'] not in ('outro',) and not (b['sec'] == 'C' and b['i'] < 4), offset=3)
    bass = bass_part(B, lambda b: full(b) or (b['sec'] == 'C' and b['i'] >= 4))
    kit = kit_part(B, lambda b: full(b), half=lambda b: b['sec'] == 'B', tap16=lambda b: b['sec'] in ('A', 'A2', 'A3', 'D'))
    mar = marimba_part(B, lambda b: b['sec'] in ('B', 'A3', 'D') or (b['sec'] == 'outro' and b['i'] < 4))
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
        'master': {'fx': [{'type': 'eq', 'bands': ['lowshelf cutoff=120 gain=4dB', 'peak cutoff=640 q=0.7 gain=-4dB', 'highshelf cutoff=6000 gain=5dB']},
                          {'type': 'gain', 'gain': '+14dB'}, {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 2, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   'auto': {'dyn': {'points': dyn}, 'fade': {'points': [['0s', 0], [f'{end_s - 8:.1f}s', 0], [f'{end_s:.1f}s', -40]]}}},
        'tracks': [
            {'name': 'gtr1', 'patch': 'starcaster-clean', 'gain': '-6dB', 'pan': -0.5, 'score': J(g1)},
            {'name': 'gtr2', 'patch': 'clean-dry', 'gain': '-7dB', 'pan': 0.5, 'score': J(g2)},
            {'name': 'bass', 'patch': 'bass-pick-di', 'gain': '-2dB', 'score': J(bass)},
            {'name': 'kit', 'patch': 'prog-kit', 'gain': '-4dB', 'score': J(kit)},
            {'name': 'marimba', 'patch': 'marimba', 'gain': '-4dB', 'pan': 0.1, 'score': J(mar)},
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
