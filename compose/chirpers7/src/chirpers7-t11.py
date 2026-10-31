#!/usr/bin/env python3
"""chirpers7-t11 (chirper-one): MODERN MINIMAL, "Both Ways", for 'The Endless Stair' (Chirpers VII mixtape).

Tight, tech-leaning minimal house: a rolling sixteenth bass under a ladder filter that breathes on odd-length LFOs,
crisp machine drums, dub stabs - the tape's cool, clean middle. 122.5 -> 123 bpm (ramped inside), Eb minor (2A):
Ebm9 - Cbmaj7 - Abm9 - Bbm7, two bars each.
THE TRITONE PARADOX (Diana Deutsch): two Shepard tones a tritone apart have no true direction - octave-spaced
partials under a fixed bell envelope, so the second tone is exactly as far above the first as below it. Some
listeners hear the pair rise, some hear it fall, and the answer depends on where the tones' spectral envelope sits.
Each bar the hook plays a step of THE STAIR (Eb F Gb Bb) and answers it with its tritone (A B C E). Through the track
the pairs cross-fade from a LOW-centred envelope (250 Hz) to a HIGH-centred one (1 kHz), so for many ears the stair
turns round; in the last groove both envelopes sound at once, and it goes both ways.
Form (bars): intro 16 (the seam from t10: kick, hats, the sub) / A 32 (the rolling bass, the pairs low) / B 32
(dub stabs; the pairs cross-fade low -> high) / break 16 (no drums: the pairs alone, high, a slow glide) / C 32
(everything; both envelopes at once) / outro 16 (the seam to t12: kick, hats, bass, the low pair fading).
Master: chirper-zero's clean recipe and the song's loudness at -11 LUFS, ceiling -1 dB.
Emits songs/chirpers7-t11.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers7-t11.yaml")
BPM_IN, BPM_OUT = 122.5, 123.0
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('A', 32), ('B', 32), ('break', 16), ('C', 32), ('outro', 16)]
CH = [(39, [58, 61, 65, 66, 70]), (35, [58, 63, 66, 70]), (32, [59, 63, 66, 70]), (34, [58, 61, 65, 68])]
STAIR = [63, 65, 66, 70]                     # Eb F Gb Bb (pitch class matters, not octave: Shepard tones)
BASS = [0, 0, 12, 0, 7, 0, 12, 0, 0, 0, 12, 10, 0, 7, 12, 0]

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

def shep(center):
    return {'synth': {'layers': [{'type': 'shepard', 'shepard': {'center': center, 'width': 1.1, 'octaves': 8,
                                                                  'position': {'value': 0, 'mod': [{'src': 'auto.glide', 'amount': 1}]}}}],
                      'amp': {'a': '8ms', 'd': '300ms', 's': 0.7, 'r': '250ms'}}}

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 't': t}); t += 4.0
    total = t
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'])
    T = {k: [] for k in ('kit', 'sub', 'bass', 'stab', 'pairlo', 'pairhi')}
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        root, ch = CH[(k // 2) % 4]
        if s != 'break':
            for q in range(4):
                T['kit'].append((t0 + q, 'k', 0.25, 114 if q == 0 else 106))
                T['kit'].append((t0 + q + 0.5, 'oh' if s in ('B', 'C') else 'h', 0.25, 80))
                T['kit'].append((t0 + q + 0.75, 'h', 0.25, 66))
                T['kit'].append((t0 + q + 0.25, 'h', 0.25, 50))
            if s in ('A', 'B', 'C'):
                T['kit'].append((t0 + 1.0, 'cp', 0.25, 92)); T['kit'].append((t0 + 3.0, 'cp', 0.25, 96))
            if s in ('B', 'C') and k % 4 == 3:
                T['kit'].append((t0 + 3.5, 'rs', 0.25, 84)); T['kit'].append((t0 + 3.75, 'rs', 0.25, 76))
        # the sub and the rolling sixteenth bass
        if s != 'break':
            T['sub'].append((t0, nm(root), 3.8, 96 if s != 'intro' else 84))
        if s in ('A', 'B', 'C') or (s == 'outro' and i < 12):
            for q, o in enumerate(BASS):
                if o is not None and (q % 4 != 0):
                    T['bass'].append((t0 + q * 0.25, nm(root + 12 + o), 0.2, 92 if q % 4 == 2 else 78))
        if s in ('B', 'C') and k % 2 == 0:
            T['stab'].append((t0 + 0.75, ','.join(nm(m) for m in ch), 0.35, 88))
            T['stab'].append((t0 + 2.5, ','.join(nm(m) for m in ch[1:]), 0.3, 74))
        # THE PAIRS: a stair step on the one (dotted quarter), its tritone on the and-of-2
        if s != 'intro' and not (s == 'outro' and i >= 12):
            step = STAIR[(k // 8) % 4]
            for at, m in ((0.0, step), (1.5, step + 6)):
                T['pairlo'].append((t0 + at, nm(m), 1.3, 92))
                T['pairhi'].append((t0 + at, nm(m), 1.3, 92))
            if s in ('B', 'C') and k % 2 == 1:      # and an answer on the four, the pair reversed
                T['pairlo'].append((t0 + 3.0, nm(step + 6), 0.9, 80)); T['pairlo'].append((t0 + 3.5, nm(step), 0.45, 74))
                T['pairhi'].append((t0 + 3.0, nm(step + 6), 0.9, 80)); T['pairhi'].append((t0 + 3.5, nm(step), 0.45, 74))
    # the cross-fade of envelopes: low alone in A, low -> high through B, high in the break, both in C, low in the outro
    tA, tB, tbr, tC, tO = secs['A'], secs['B'], secs['break'], secs['C'], secs['outro']
    lo = [['0b', 0], [f'{tB:.1f}b', 0], [f'{tbr:.1f}b', -30], [f'{tC - 0.1:.1f}b', -30], [f'{tC:.1f}b', -3], [f'{tO:.1f}b', -3], [f'{tO + 1:.1f}b', 0], [f'{total:.1f}b', -8]]
    hi = [['0b', -40], [f'{tB:.1f}b', -40], [f'{tbr:.1f}b', 0], [f'{tC - 0.1:.1f}b', 0], [f'{tC:.1f}b', -3], [f'{tO:.1f}b', -3], [f'{tO + 1:.1f}b', -40]]
    # the break: the Shepard position glides up a whole octave, slowly - an endless rise under the pairs
    glide = [['0b', 0], [f'{tbr:.1f}b', 0], [f'{tC:.1f}b', 1.0], [f'{tC + 0.01:.1f}b', 0]]
    # the bass's ladder breathes on two odd LFOs (5 and 7 bars)
    lv = {'intro': -4, 'A': -1, 'B': 0, 'break': -5, 'C': 0, 'outro': -3}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.5):.2f}b', dyn[-1][1] if dyn else lv[name]], [f'{t_:.2f}b', lv[name]]]
    dyn[0][0] = '0b'
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(T[name], total)}, **kw)
    pair_fx = lambda lane: [{'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': f'auto.{lane}', 'amount': 1}]}}]
    return {
        'about': "Chirpers - The Endless Stair (Chirpers VII), track 11 by chirper-one: MODERN MINIMAL, Both Ways. "
                 "Generated by compose/chirpers7/src/chirpers7-t11.py; see its docstring and compose/chirpers7/styles.md.",
        'tempo': [{'at': '0b', 'bpm': BPM_IN}, {'at': f'{total:.0f}b', 'bpm': BPM_OUT, 'ramp': True}],
        'length': f'{total * 60 / ((BPM_IN + BPM_OUT) / 2) + 1.2:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'loudness': -11.0,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=4s mix=1', 'hp cutoff=300'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.4, 'mix': 1}, 'lp cutoff=3000', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=32', 'peak cutoff=55 q=0.9 gain=-5dB', 'peak cutoff=110 q=0.9 gain=-3dB', 'peak cutoff=400 q=0.7 gain=-2dB', 'peak cutoff=3200 q=0.6 gain=5dB', 'highshelf cutoff=6000 gain=3dB']},
                          {'type': 'compressor', 'threshold': '-20dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': '+8dB'},
                          {'type': 'compressor', 'threshold': '-15dB', 'ratio': 8, 'attack': '0.3ms', 'release': '60ms'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}}],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            tr('kit', 'machine-kit', '-4dB', sends={'hall': '-20dB'}),
            tr('sub', 'sub', '-9dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '320ms', 'curve': 0.6}]),
            tr('bass', 'bass', '-9dB', lfo={'a': 'sine rate=5/1 phase=0', 'b': 'sine rate=7/1 phase=0.25'},
               fx=[{'type': 'filter', 'kind': 'ladder', 'q': 0.55, 'cutoff': {'value': 900, 'mod': [{'src': 'lfo.a', 'amount': 0.9}, {'src': 'lfo.b', 'amount': 0.6}]}},
                   {'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '320ms', 'curve': 0.6}]),
            tr('stab', 'epiano-tine', '-11dB', sends={'echo': '-8dB', 'hall': '-10dB'}, fx=['lp cutoff=2800']),
            tr('pairlo', shep('250hz'), '-9dB', fx=pair_fx('lo'), auto={'lo': {'points': lo}, 'glide': {'points': glide}}, sends={'hall': '-10dB'}),
            tr('pairhi', shep('1000hz'), '-12dB', fx=pair_fx('hi'), auto={'hi': {'points': hi}, 'glide': {'points': glide}}, sends={'hall': '-10dB'}),
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
