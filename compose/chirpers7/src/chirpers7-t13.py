#!/usr/bin/env python3
"""chirpers7-t13 (chirper-one): HEAVY DEEP HOUSE, PEAK TIME, "Faster Forever", for 'The Endless Stair' (Chirpers VII).

The tape reaching its plateau - a heavy kick, a driven bass, big minor-ninth stabs, the room full - and the mirror of
chirper-zero's 'Slower Forever'. 123.5 -> 124 bpm (ramped inside), F minor (4A): Fm9 - Dbmaj7 - Bbm9 - C7sus, four bars
each.
THE RISSET ACCELERANDO (Jean-Claude Risset): a percussion bed - rims, a shaker, a clave and a hat figure - speeds up
forever: three tempo octaves of the same bar, each doubling its speed over eight bars while the fastest fades out and
the slowest fades in, so the bed is always accelerating and never arrives, over a kick that never changes. The build
that never lands, used as the peak's engine. THE STAIR (F G Ab C) rides it on a stab.
Form (bars): intro 16 (the seam from t12: kick, hats, sub) / A 32 (the driven bass, the stabs; the accelerando enters
at bar 8) / B 32 (full: the stair on the stab) / break 16 (no kick: the accelerando alone under a filtered pad - the
rush with nothing to rush to) / C 32 (the peak) / outro 16 (the seam to t14: kick, hats, sub).
Master: chirper-zero's clean recipe and the song's loudness at -11 LUFS, ceiling -1 dB.
Emits songs/chirpers7-t13.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers7-t13.yaml")
BPM_IN, BPM_OUT = 123.5, 124.0
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('A', 32), ('B', 32), ('break', 16), ('C', 32), ('outro', 16)]
CH = [(41, [60, 63, 67, 68, 72]), (37, [60, 65, 68, 72]), (34, [61, 65, 68, 72]), (36, [60, 65, 67, 70])]
STAIR = [65, 67, 68, 72]                      # F G Ab C
BASS = [0, None, 12, 0, None, 7, 12, None, 0, None, 12, 10, None, 7, 12, None]
RISSET_PAT = "rs/16 R/16 shk/16 rs/16 R/16 clv/16 shk/16 R/16 rs/16 shk/16 R/16 h/16 clv/16 R/16 shk/16 h/16"

def line(events, total):
    ev = sorted(events)
    toks, t = [], 0.0
    for k, (at, p, d, v) in enumerate(ev):
        if at < t - 1e-6: continue
        if at > t + 1e-4: toks.append(f"R/{at - t:.4f}b")
        nxt = ev[k + 1][0] if k + 1 < len(ev) else total
        d = max(0.02, min(d, nxt - at))
        toks.append(f"{p}/{d:.4f}b@{v}"); t = at + d
    if total > t + 1e-4: toks.append(f"R/{total - t:.4f}b")
    return ' '.join(toks)

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 't': t}); t += 4.0
    total = t
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'])
    T = {k: [] for k in ('kit', 'sub', 'bass', 'stab', 'pad')}
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        root, ch = CH[(k // 4) % 4]          # four bars a chord: the plateau moves slowly
        if s != 'break':
            for q in range(4):
                T['kit'].append((t0 + q, 'kd' if s == 'C' else 'k', 0.25, 118 if q == 0 else 110))
                T['kit'].append((t0 + q + 0.5, 'oh', 0.25, 82))
                T['kit'].append((t0 + q + 0.75, 'h', 0.25, 60))
            if s in ('A', 'B', 'C'):
                T['kit'].append((t0 + 1.0, 'cp', 0.25, 100)); T['kit'].append((t0 + 3.0, 'cp', 0.25, 104))
        if s != 'break':
            T['sub'].append((t0, nm(root), 3.8, 100 if s != 'intro' else 86))
        if s in ('A', 'B', 'C') or (s == 'outro' and i < 8):
            for q, o in enumerate(BASS):
                if o is not None:
                    T['bass'].append((t0 + q * 0.25, nm(root + 12 + o), 0.2, 100 if q % 4 == 2 else 84))
        if s in ('A', 'B', 'C') and k % 4 in (0, 2):
            T['stab'].append((t0 + 0.5, ','.join(nm(m) for m in ch), 0.4, 92))
        # THE STAIR on the stab: in B and C, every other bar, F G Ab C on the off-beats
        if s in ('B', 'C') and k % 2 == 1:
            for q, m in zip((0.5, 1.5, 2.5, 3.5), STAIR):
                T['stab'].append((t0 + q, f"{nm(m)},{nm(m + 12)}" if s == 'C' else nm(m + 12), 0.3, 88))
        if s in ('break', 'intro') and k % 4 == 0:
            T['pad'].append((t0, ','.join(nm(m) for m in ch), 15.8, 80))
    lv = {'intro': -4, 'A': -1, 'B': 0, 'break': -5, 'C': 0, 'outro': -3}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.5):.2f}b', dyn[-1][1] if dyn else lv[name]], [f'{t_:.2f}b', lv[name]]]
    dyn[0][0] = '0b'
    # the break's pad through a closed low-pass that opens into C
    tb, tc = secs['break'], secs['C']
    padop = [['0b', 0], [f'{tb:.1f}b', 0], [f'{tc - 1:.1f}b', 1], [f'{tc:.1f}b', 0]]
    risset = lambda at_bar, nbars: {
        'name': f'rush{at_bar}', 'patch': 'machine-kit', 'gain': '-11dB', 'pan': 0.2, 'at': f'{at_bar * 4}b',
        'risset': {'cycle': '8bar', 'down': False, 'layers': 3, 'length': f'{nbars}bar'},
        'sends': {'hall': '-14dB'}, 'score': RISSET_PAT}
    start_A = int(secs['A'] // 4)
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(T[name], total)}, **kw)
    return {
        'about': "Chirpers - The Endless Stair (Chirpers VII), track 13 by chirper-one: HEAVY DEEP HOUSE, Faster Forever. "
                 "Generated by compose/chirpers7/src/chirpers7-t13.py; see its docstring and compose/chirpers7/styles.md.",
        'tempo': [{'at': '0b', 'bpm': BPM_IN}, {'at': f'{total:.0f}b', 'bpm': BPM_OUT, 'ramp': True}],
        'length': f'{total * 60 / ((BPM_IN + BPM_OUT) / 2) + 1.2:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'loudness': -11.0,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.5s mix=1', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=32', 'peak cutoff=55 q=0.9 gain=-4dB', 'peak cutoff=400 q=0.7 gain=-2dB', 'peak cutoff=3200 q=0.6 gain=4dB', 'highshelf cutoff=6000 gain=2dB']},
                          {'type': 'compressor', 'threshold': '-20dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': '+8dB'},
                          {'type': 'compressor', 'threshold': '-15dB', 'ratio': 8, 'attack': '0.3ms', 'release': '60ms'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}}],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            tr('kit', 'machine-kit', '-4dB', sends={'hall': '-20dB'}),
            tr('sub', 'sub', '-8dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '320ms', 'curve': 0.6}]),
            tr('bass', 'bass', '-8dB', fx=[{'type': 'drive', 'drive': 0.35, 'mix': 0.5}, 'lp cutoff=1600',
                                           {'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '320ms', 'curve': 0.6}]),
            tr('stab', 'epiano-tine', '-10dB', sends={'hall': '-10dB'}, fx=['lp cutoff=3500']),
            tr('pad', 'juno-pad', '-12dB', sends={'hall': '-8dB'},
               fx=[{'type': 'filter', 'kind': 'lp', 'q': 0.8, 'cutoff': {'value': 600, 'mod': [{'src': 'auto.op', 'amount': 3.0}]}}],
               auto={'op': {'points': padop}}),
            risset(start_A + 8, 24), risset(int(secs['B'] // 4), 32), risset(int(secs['break'] // 4), 16), risset(int(secs['C'] // 4), 32),
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
