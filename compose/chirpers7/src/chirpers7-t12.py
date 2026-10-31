#!/usr/bin/env python3
"""chirpers7-t12 (chirper-one): DUB HOUSE, "The Ghost Note", for 'The Endless Stair' (Chirpers VII mixtape).

Deep, wet, spacious dub house - chords thrown into a dark echo, a sub you feel, room in every bar - between Both Ways
(t11) and Faster Forever (t13). 123 -> 123.5 bpm (ramped inside), Bb minor (3A): Bbm9 - Gbmaj7 - Ebm9 - Fm7; the harmony
opens through the track (A on Bbm9 alone, B swinging to Gbmaj7, C the whole cycle), over a sub that holds Bb as a pedal.
THE ZWICKER TONE (Eberhard Zwicker, 1964): broadband noise with a NOTCH cut out of it, heard for a few seconds and
then stopped, leaves a faint after-tone - a ghost - pitched near the hole's lower edge, for a few seconds of silence.
At the end of each sixteen-bar phrase a wide wash of pink noise swells for two bars with an octave-wide notch at a
step of THE STAIR (Bb C Db F, around 2 kHz), then the whole track stops for one beat, and in that silence the ghost
note hangs where the hole was. In the break the washes come alone; in the last groove the Rhodes plays the ghost's
note out loud, as if the after-image had become real.
Under each wash the echo's feedback climbs toward self-oscillation (a dub throw) and is cut with the silence.
Form (bars): intro 16 (the seam from t11) / A 32 / B 32 / break 16 / C 32 / outro 16 (the seam to t13).
Master: chirper-zero's recipe and the song's loudness at -11 LUFS, ceiling -1 dB.
Emits songs/chirpers7-t12.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers7-t12.yaml")
BPM_IN, BPM_OUT = 123.0, 123.5
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('A', 32), ('B', 32), ('break', 16), ('C', 32), ('outro', 16)]
CH = [(34, [61, 65, 68, 72]), (30, [61, 65, 66, 70]), (39, [61, 63, 66, 70]), (41, [60, 63, 65, 68])]
STAIR_ST = [0, 2, 3, 7]                       # Bb C Db F, semitones above Bb
NOTCH_HZ = 1865.0                             # Bb6

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
    T = {k: [] for k in ('kit', 'sub', 'stab', 'pad', 'wash', 'ghost')}
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        # (v1) the harmony opens up through the track: A holds Bbm9 alone (the dub-techno way), B swings Bbm9 <-> Gbmaj7
        # eight bars each, C walks the whole cycle eight bars a chord
        if s in ('A', 'intro'):
            root, ch = CH[0]
        elif s in ('B', 'break'):
            root, ch = CH[(i // 8) % 2]
        else:
            root, ch = CH[(i // 8) % 4]
        if s != 'break':
            for q in range(4):
                T['kit'].append((t0 + q, 'k', 0.25, 114 if q == 0 else 106))
                T['kit'].append((t0 + q + 0.5, 'h' if s in ('intro', 'outro') else 'oh', 0.25, 76))
                T['kit'].append((t0 + q + 0.75, 'h', 0.25, 58))
                T['kit'].append((t0 + q + 0.25, 'h', 0.25, 46))
            if s in ('A', 'B', 'C'):
                T['kit'].append((t0 + 3.0, 'rs', 0.25, 84))
                if k % 2 == 1:
                    T['kit'].append((t0 + 2.75, 'rs', 0.25, 70))
            T['sub'].append((t0, nm(34), 3.7, 98))      # a PEDAL on Bb: the floor stays while the chords turn
        # the dub chord: one stab a bar on the and-of-1 (into the echo), and the 'a' of 3 every other bar
        if s in ('A', 'B', 'C'):
            T['stab'].append((t0 + 0.5, ','.join(nm(m) for m in ch), 0.3, 86))
            if k % 2 == 0:
                T['stab'].append((t0 + 2.75, ','.join(nm(m) for m in ch[1:]), 0.25, 72))
        if s in ('intro', 'break', 'outro') and k % 4 == 0:
            T['pad'].append((t0, ','.join(nm(m - 12) for m in ch), 15.8, 74))
    # THE WASHES: two bars of notched noise before each phrase end (every 16 bars from bar 16), then a beat of silence
    notch, gaps, fbl, thr = [['0b', 0]], [], [['0b', 0]], [['0b', 0]]
    ends = [16 * n for n in range(2, int(total // 64) + 1)]
    ends = [e * 4 for e in ends if e * 4 < total - 8]
    # also inside the break: two washes, eight bars apart
    tb = secs['break']
    ends = sorted(set(ends + [tb + 32, tb + 64]))
    for n, e in enumerate(ends):
        st = STAIR_ST[n % 4]
        a0 = e - 9.0
        T['wash'].append((a0, 'C4', 8.0, 92))
        notch += [[f'{a0 - 0.1:.2f}b', notch[-1][1]], [f'{a0:.2f}b', round(st / 12, 4)]]
        gaps.append(e - 1.0)
        # (v3) THE THROW: under each wash the echo's feedback climbs toward self-oscillation, the dub engineer's hand on the
        # knob, and is cut dead with everything else at the silence
        fbl += [[f'{a0:.2f}b', 0], [f'{e - 1.05:.2f}b', 0.33], [f'{e - 1.0:.2f}b', -0.5], [f'{e + 0.5:.2f}b', -0.5], [f'{e + 0.55:.2f}b', 0]]
        thr += [[f'{a0:.2f}b', 0], [f'{e - 1.05:.2f}b', 10], [f'{e - 1.0:.2f}b', -40], [f'{e + 0.5:.2f}b', -40], [f'{e + 0.55:.2f}b', 0]]
        # in C the Rhodes plays the ghost's note out loud on the downbeat after the silence
        if secs['C'] <= e < secs['outro']:
            T['ghost'].append((e, nm(70 + st + 12), 3.5, 84))
    lv = {'intro': -4, 'A': -1, 'B': 0, 'break': -4, 'C': 0, 'outro': -3}
    pts = []
    for name, _ in FORM:
        t_ = secs[name]
        pts += [(max(0.0, t_ - 0.5), pts[-1][1] if pts else lv[name]), (t_, lv[name])]
    # the beat of silence after each wash
    for g in gaps:
        before = [p for p in pts if p[0] <= g - 0.05]
        lvl = before[-1][1]
        after = [p for p in pts if p[0] >= g + 1.0]
        pts = before + [(g - 0.02, lvl), (g, -45), (g + 0.98, -45), (g + 1.0, lvl)] + after
    dyn = [[f'{p[0]:.2f}b', p[1]] for p in pts]
    dyn[0][0] = '0b'
    wash = {'synth': {'layers': [{'type': 'noise', 'color': 'pink'}], 'amp': {'a': '6s', 'd': '1s', 's': 1, 'r': '4ms'}}}
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(T[name], total)}, **kw)
    return {
        'about': "Chirpers - The Endless Stair (Chirpers VII), track 12 by chirper-one: DUB HOUSE, The Ghost Note. "
                 "Generated by compose/chirpers7/src/chirpers7-t12.py; see its docstring and compose/chirpers7/styles.md.",
        'tempo': [{'at': '0b', 'bpm': BPM_IN}, {'at': f'{total:.0f}b', 'bpm': BPM_OUT, 'ramp': True}],
        'length': f'{total * 60 / ((BPM_IN + BPM_OUT) / 2) + 0.15:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'loudness': -11.0, 'tail': '0.1s',
        'buses': {'echo': {'fx': [{'type': 'delay', 'time': '3/8', 'feedback': {'value': 0.55, 'mod': [{'src': 'auto.fb', 'amount': 1}]}, 'mix': 1}, 'lp cutoff=2200', 'hp cutoff=250',
                                  {'type': 'tape', 'drive': 0.25, 'mix': 0.5, 'wow': 6, 'flutter': 2, 'seed': 12},
                                  {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.thr', 'amount': 1}]}}], 'returns': [],
                           'auto': {'fb': {'points': fbl}, 'thr': {'points': thr}}},
                  'hall': {'fx': ['reverb kind=hall decay=4.5s mix=1', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=32', 'peak cutoff=58 q=0.9 gain=-5dB', 'peak cutoff=350 q=0.7 gain=-3dB', 'peak cutoff=3200 q=0.6 gain=5dB', 'highshelf cutoff=7000 gain=5dB']},
                          {'type': 'compressor', 'threshold': '-20dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': '+8dB'},
                          {'type': 'compressor', 'threshold': '-15dB', 'ratio': 8, 'attack': '0.3ms', 'release': '60ms'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}}],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            tr('kit', 'machine-kit', '-4dB', sends={'hall': '-18dB'}),
            tr('sub', 'sub', '-8dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '320ms', 'curve': 0.6}]),
            tr('stab', 'epiano-tine', '-9dB', sends={'echo': '-4dB'}, fx=['lp cutoff=2600', {'type': 'pump', 'on': 'kit.k', 'depth': '-4dB', 'release': '320ms', 'curve': 0.6}]),
            tr('pad', 'juno-pad', '-12dB', sends={'hall': '-8dB'}),
            tr('wash', wash, '-14dB',
               fx=['hp cutoff=200', 'lp cutoff=9000',
                   {'type': 'filter', 'kind': 'notch', 'q': 0.6, 'cutoff': {'value': NOTCH_HZ, 'mod': [{'src': 'auto.nt', 'amount': 1}]}},
                   {'type': 'filter', 'kind': 'notch', 'q': 0.9, 'cutoff': {'value': NOTCH_HZ * 0.92, 'mod': [{'src': 'auto.nt', 'amount': 1}]}}],
               auto={'nt': {'points': notch}}),
            tr('ghost', 'epiano-tine', '-10dB', sends={'echo': '-6dB', 'hall': '-10dB'}),
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
