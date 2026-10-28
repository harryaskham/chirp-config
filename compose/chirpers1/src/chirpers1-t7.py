#!/usr/bin/env python3
"""chirpers1-t7 "Ascent" (chirper-one): Ferrous Bloom's track 7, ~204 s at 112 BPM (bar = 2.143 s).

The ascent: a churning low riff that climbs a step each section while a dissonant, lyrical lead soars over it,
built to the album's emotional climax, then let go on the COLD CHORD that track 8 opens with.

- CHURN (rhythm): a 10-sixteenth cell over 4/4, `X . . x . . X . x .` (3+3+2+2), realigning every 5 bars, so
  sections are 5/10/15/20 bars. X = accented palm-muted root (kick in unison), x = palm-muted root; every second
  cell's last onset is an open root+fifth.
- STAIRS (harmony): the churn's root climbs a step each section: F1 -> Gb1 -> Ab1 -> A1 -> B1 (the tritone, the
  climax) and the riff falls back to F for the release.
- LATTICE RISING (t1's F-Gb-B-E line, transformed): the lead turns LATTICE into a soaring line, re-voiced upward
  (F4 Gb4 B4 E5 -> F5) and inverted on the way down (E5 B4 Gb4 F4); every phrase rides one step higher with the root.
- Breakdown: t1's line inverted on the clean (E4 B3 Gb3 F3) on the 3+3+2+2 cell, half-time kit.
- Ends on t5's COLD CHORD (F2 C3 E3 B3 G4), ringing into track 8's dawn.

Emits songs/chirpers1-t7.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers1-t7.yaml")
BPM, NB = 112, 100
SPB = 60 / BPM
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
def nm(m): return f"{NAMES[m % 12]}{m // 12 - 1}"
def mid(n):
    p, o = n[:-1], int(n[-1]); return NAMES.index({'F#': 'Gb', 'C#': 'Db'}.get(p, p)) + 12 * (o + 1)
def tr(n, k): return nm(mid(n) + k)

def join(b):
    return ' | '.join(' '.join(b.get(m) or ['R/4b']) for m in range(1, NB + 1))
def merge(*ds):
    o = {}
    for d in ds: o.update(d)
    return o
def drum_bar(slots):
    t = []
    for s in slots:
        if s:
            v = max(x[1] for x in s); t.append(','.join(sorted({x[0] for x in s})) + f'/0.25b@{v}')
        else:
            t.append('R/0.25b')
    return t

CELL = {0: 'X', 3: 'x', 6: 'X', 8: 'x'}          # 3+3+2+2 over 10 sixteenths
def churn(a, b, root, half=False):
    """gtr, bass, hits per bar for a churn on ROOT (e.g. 'F1') from bar a to b"""
    g, bs, hits = {}, {}, {}
    i = 0
    for m in range(a, b + 1):
        gt, bt, ht = [], [], []
        for s in range(16):
            p, cn = i % 10, i // 10; i += 1
            c = CELL.get(p)
            if c is None:
                gt.append('R/0.25b'); bt.append('R/0.25b'); ht.append(None)
            elif p == 8 and cn % 2 == 1:
                gt.append(f'{root},{tr(root, 7)},{tr(root, 12)}/0.25b@116'); bt.append(f'{root}/0.25b@112'); ht.append('O')
            else:
                v = 116 if c == 'X' else 102
                gt.append(f'{root}/0.25b@{v}^pm'); bt.append(f'{root}/0.25b@{v}'); ht.append(c)
        g[m], bs[m], hits[m] = gt, bt, ht
    return g, bs, hits

def drums(a, b, hits, half=False, crash_every=5, ride=False):
    out = {}
    for m in range(a, b + 1):
        sl = [[] for _ in range(16)]
        for s, h in enumerate(hits[m]):
            if h in ('X', 'O'): sl[s].append(('k', 114))
            elif h == 'x': sl[s].append(('k', 100))
            if h == 'O': sl[s].append(('x', 100))
        for s in range(0, 16, 2):
            sl[s].append(('rd' if ride else 'h', 90 if s % 4 == 0 else 74))
        if half: sl[8].append(('s', 118))
        else: sl[4].append(('s', 116)); sl[12].append(('s', 118))
        if (m - a) % crash_every == 0: sl[0].append(('c', 118))
        out[m] = drum_bar(sl)
    return out

# the lead: LATTICE rising, 4-bar phrases, transposed with the stairs
L1 = [['F4/2b@92', 'Gb4/1b@94', 'B4/1b@98'], ['E5/3b@104', 'D5/1b@96'], ['C5/2b@98', 'B4/2b@96'], ['Gb4/4b@94']]
L2 = [['F4/1b@96', 'B4/1b@100', 'E5/2b@106'], ['F5/3b@110', 'E5/1b@104'], ['B4/2b@100', 'C5/2b@102'], ['Gb5/4b@112']]
L3 = [['B4/1b@104', 'E5/1b@108', 'F5/2b@112'], ['Gb5/3b@116', 'F5/1b@110'], ['E5/2b@108', 'B5/2b@118'], ['F5/4b@114']]
INV = [['E5/2b@100', 'B4/2b@96'], ['Gb4/2b@94', 'F4/2b@92'], ['E5/1b@100', 'B4/1b@98', 'Gb4/1b@96', 'F4/1b@92'], ['F4/4b@88']]
def phr(a, b, P, k=0):
    out = {}
    for m in range(a, b + 1):
        out[m] = [f'{tr(t.split("/")[0], k)}/{t.split("/", 1)[1]}' for t in P[(m - a) % len(P)]]
    return out

def build():
    I, A, B, A2, BR, C1, A3, C2, X, RP, O = (1, 5), (6, 20), (21, 30), (31, 35), (36, 45), (46, 55), (56, 60), (61, 70), (71, 80), (81, 90), (91, 100)
    gA, bA, hA = churn(*A, 'F1'); gB, bB, hB = churn(*B, 'Gb1')
    gC1, bC1, hC1 = churn(*C1, 'Ab1'); gC2, bC2, hC2 = churn(*C2, 'A1'); gX, bX, hX = churn(*X, 'B1'); gR, bR, hR = churn(*RP, 'F1')
    gA2, bA2, hA2 = churn(*A2, 'F1'); gA3, bA3, hA3 = churn(*A3, 'F1')
    gtr = merge({m: [f'F1,B1,F2/4b@{124 - 8 * (m - 1)}'] for m in range(I[0], I[1] + 1)}, gA, gB, gA2, gC1, gA3, gC2, gX, gR,
                {m: (['F1,C2,F2/4b@118'] if m == O[0] else ['F2,C3,E3,B3/4b@100'] if m == O[0] + 1 else ['R/4b'])
                 for m in range(O[0], O[1] + 1)})
    bass = merge({m: ['F1/4b@90'] for m in range(I[0] + 2, I[1] + 1)}, bA, bB, bA2, bA3,
                 {m: ['F1/4b@80'] for m in range(BR[0], BR[1] + 1)}, bC1, bC2, bX, bR, {O[0]: ['F1/4b@118'], O[0] + 1: ['F1/4b@100']})
    kit = merge(drums(*A, hA), drums(*B, hB), drums(*A2, hA2), drums(*A3, hA3), drums(*C1, hC1), drums(*C2, hC2, ride=True), drums(*X, hX, crash_every=5, ride=False), drums(*RP, hR),
                {I[0]: drum_bar([[('c', 124), ('k', 124), ('x', 116)]] + [[]] * 7 + [[('c', 116)]] + [[]] * 3 + [[('sp', 110)]] + [[]] * 3),
                 I[0] + 1: drum_bar([[('c', 108)]] + [[]] * 15)},
                {m: drum_bar([[('rd', 70)] if s % 4 == 0 else [] for s in range(16)][:8] + [[('s', 100), ('k', 96)]] + [[]] * 7)
                 for m in range(BR[0] + 4, BR[1] + 1)},
                {O[0]: drum_bar([[('c', 126), ('k', 126), ('x', 118)]] + [[]] * 15)})
    lead = merge({m: ['E5/4b@80'] for m in range(I[0] + 1, I[1] + 1)},
                 phr(A[0] + 4, A[1], L1, 0), phr(B[0], B[1], L1, 1), phr(A2[0], A2[1], L1, 0), phr(A3[0], A3[1], L1, 0),
                 phr(C1[0], C1[1], L2, 3), phr(C2[0], C2[1], L2, 4), phr(X[0], X[1], L3, 6), phr(RP[0], RP[1], L1, 12),
                 {O[0]: ['F5/4b@110'], O[0] + 1: ['E5/4b@96'], O[0] + 2: ['E5/4b@84']})
    clean = merge(*[{m: t} for m, t in []])
    cl = {}
    k = 0
    line = ['E4', 'B3', 'Gb3', 'F3']
    for m in range(BR[0], BR[1] + 1):
        toks = []
        for s in range(16):
            gi = (m - BR[0]) * 16 + s
            if gi % 10 in CELL:
                toks.append(f'{line[k % 4]}/0.25b@70'); k += 1
            else:
                toks.append('R/0.25b')
        cl[m] = toks
    for m in range(O[0] + 2, O[1] + 1):
        cl[m] = ['F3/1b@60', 'C4/1b@58', 'E4/1b@58', 'B4/1b@56']
    pad = merge({m: ['F2,B2,E3/4b@62'] for m in range(I[0], I[1] + 1)},
                {m: ['F2,C3,Gb3,B3/4b@64'] for m in range(BR[0], BR[1] + 1)},
                {m: ['F2,C3,E3,B3,G4/4b@70'] for m in range(O[0] + 1, O[1] + 1)})
    # ---- the sound playground (Harry, 28 Oct) ----
    # HARM: the climax and the reprise sung a fifth above the lead (a second m8-lead, panned left)
    HARM = merge(phr(X[0], X[1], L3, 6 + 7), phr(RP[0], RP[1], L1, 12 + 7))
    # SUB-CRUSH on the landings: the F churn's returns doubled an octave down and bit-crushed (the landing sounds new)
    FUZZ = merge({m: gA2[m] for m in range(A2[0], A2[1] + 1)}, {m: gA3[m] for m in range(A3[0], A3[1] + 1)},
                 {m: gR[m] for m in range(RP[0], RP[1] + 1)})
    # HOCKET (borrowing chirper-three's SHARD from t2): in the A and B steps the CHURN's light chugs (x) leave the
    # pair for a bit-crushed m8 in the centre; the pair keeps the accents and the opens
    SHARD = {}
    for g_, h_, (a_, z_) in ((gC2, hC2, C2), (gX, hX, X)):
        for m in range(a_, z_ + 1):
            SHARD[m] = [tk if h == 'x' else 'R/0.25b' for tk, h in zip(g_[m], h_[m])]
            gtr[m] = ['R/0.25b' if h == 'x' else tk for tk, h in zip(g_[m], h_[m])]
    # STAIR TOMS (borrowing chirper-three's physical-tom idea from t1, with a stick): a fill down the stairs' own notes
    # (B A Ab F) in the last bar of every step; the climax's last bar rolls the whole bar
    TOMS = {}
    for b_ in (A[1], B[1], C1[1], A3[1], C2[1]):
        TOMS[b_] = ['R/2b'] + [f'{x}/0.25b@{v}' for x, v in zip(['t1', 't1', 't2', 't2', 't3', 't3', 'ft', 'ft'], range(96, 128, 4))]
    TOMS[X[1]] = [f'{x}/0.25b@{v}' for x, v in zip(['t1', 't1', 't1', 't1', 't2', 't2', 't2', 't2', 't3', 't3', 't3', 't3', 'ft', 'ft', 'ft', 'ft'],
                                                     range(88, 128, 2))]
    end_s = NB * 4 * SPB
    return {
        'about': 'Chirpers - Ferrous Bloom, track 7 "Ascent" by chirper-one. Generated by compose/chirpers1/src/'
                 'chirpers1-t7.py; see its docstring and compose/chirpers1/motifs.md.',
        'tempo': BPM, 'length': f'{end_s:.2f}s', 'ceiling': '-0.1dB',
        'patches': {'stair-toms': {'about': "Iron Stairs' toms: physical stick toms (chirper-two's drum layer) tuned to the STAIRS (B A Ab F).",
                                   'extends': 'metal-kit-punch',
                                   'kit': {k: {'pitch': p_, 'gain': '6dB', 'patch': {'synth': {'layers': [{'type': 'drum', 'beater': 'stick', 'decay': f'{d_}s', 'sharp': 35, 'reso': 1.0,
                                            'cavity': 0.1, 'reso_level': 0.1, 'air': 0.5, 'strike': 0.3, 'shell': 0.4, 'damp': 0.25, 'tune_sounding': True}],
                                            'filters': ['hp cutoff=40', 'peak cutoff=3k q=1 gain=2dB'],
                                            'amp': {'a': '0.3ms', 'd': f'{int(d_ * 900)}ms', 's': 0, 'r': '100ms', 'curve': 3}, 'drive': 0.08},
                                            'play': {'vel_sens': 0.6}}}
                                           for k, p_, d_ in (('t1', 'B2', 0.6), ('t2', 'A2', 0.7), ('t3', 'Ab2', 0.8), ('ft', 'F2', 1.0))}}},
        'master': {'fx': [{'type': 'eq', 'bands': ['peak cutoff=420 q=0.7 gain=-3dB']}, {'type': 'gain', 'gain': '+14.5dB'},
                          {'type': 'compressor', 'threshold': '-14dB', 'ratio': 2.5, 'attack': '10ms', 'release': '120ms', 'makeup': '5dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   'auto': {'fade': {'points': [['0s', -5], ['3s', -2], ['6s', 0], [f'{(O[0] + 3) * 4 * SPB:.1f}s', 0], [f'{end_s:.1f}s', -12]]}}},
        'tracks': [
            {'name': 'pad', 'patch': 'juno-pad', 'gain': '-9dB', 'fx': [{'type': 'tremolo', 'depth': 0.6, 'rate': 1.493}], 'score': join(pad)},   # a gate in 5 sixteenths (the CHURN's half) against the pad
            {'name': 'clean', 'patch': 'm8-clean', 'gain': '-8dB', 'pan': -0.2, 'score': join(cl)},
            {'name': 'gtr-l', 'patch': 'm8-emg-l', 'gain': '-5dB', 'pan': -1, 'score': join(gtr)},
            {'name': 'gtr-r', 'patch': 'm8-emg-r', 'gain': '-5dB', 'pan': 1, 'score': join(gtr)},
            {'name': 'bass', 'patch': 'bass-fat', 'gain': '-4dB', 'score': join(bass)},
            {'name': 'drums', 'patch': 'metal-kit-punch', 'gain': '-2dB', 'score': join(kit)},
            {'name': 'lead', 'patch': 'm8-lead', 'gain': '-6dB', 'pan': 0.1, 'fx': ['delay time=3/8 feedback=0.3 mix=0.15'], 'score': join(lead)},
            {'name': 'toms', 'patch': 'stair-toms', 'gain': '-3dB', 'score': join(TOMS)},
            {'name': 'harm', 'patch': 'm8-lead', 'gain': '-11dB', 'pan': -0.35, 'score': join(HARM)},
            {'name': 'shard', 'patch': 'm8-emg-r', 'gain': '-6dB', 'pan': 0, 'fx': [{'type': 'crush', 'bits': 6, 'rate': 5000, 'mix': 0.6}], 'score': join(SHARD)},
            {'name': 'fuzz', 'patch': 'm8-emg-r', 'gain': '-8dB', 'pan': 0,
             'fx': [{'type': 'pitch', 'semitones': -12, 'mix': 0.6}, {'type': 'crush', 'bits': 8, 'rate': 1, 'mix': 0.25}],
             'score': join(FUZZ)},
        ]}


# ---- guitar-like lead expression (chirper-one, tone push / bd-90c9d2): ^f0 paths on m8-lead via a song-local twin ----
import re as _re
_NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
_AL = {'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'}
def _mid(n):
    m = _re.match(r'([A-G][#b]?)(-?\d)$', n); return _NN.index(_AL.get(m[1], m[1])) + 12 * int(m[2])
def guitarize(song, tracks=('lead', 'harm')):
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
