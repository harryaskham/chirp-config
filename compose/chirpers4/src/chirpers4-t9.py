#!/usr/bin/env python3
"""chirpers4-t9 (chirper-one): POLYMETRIC TOOL TECHNO, "where is the one", for 'Phantom Downbeat' (Chirpers IV).

A hypnotic warehouse tool at 132 bpm.
- Against the 4/4 kick, three loops of 3, 5 and 7 sixteenths turn: a rim, a comb-filtered stab and the open-hat
  accents. They realign only every 105 sixteenths.
- THE PHANTOM BASS: an additive voice with only harmonics 2-5 of E1 (82-206 Hz) and no energy at 41 Hz. The ear
  supplies the fundamental, so it sounds deeper than it is.
- THE ONE AS ILLUSION: the bass's strongest hit is the and-of-2. When the kick drops out in the first break, the ear
  re-hears that hit as the downbeat; when the kick slams back the phrase seems to flip by an eighth.
- THE BUILD seems to accelerate without the tempo moving: the hats double their rate every four bars
  (eighths, sixteenths, triplet sixteenths, thirty-seconds) under a Shepard riser.
- The kick feeds a dark reverb bus (the rumble), and the bass and stabs pump against the kick.

Form: intro, A, break (kick out), B, build, C (peak), outro.
Emits songs/chirpers4-t9.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers4-t9.yaml")
BPM = 132
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('A', 32), ('break', 16), ('B', 32), ('build', 16), ('C', 32), ('outro', 16)]
HAS = {
    'intro': {'kick', 'hat', 'rim'},
    'A': {'kick', 'hat', 'rim', 'bass', 'stab'},
    'break': {'bass', 'stab', 'rim'},
    'B': {'kick', 'hat', 'rim', 'bass', 'stab', 'acc', 'clap'},
    'build': {'bass', 'buildhat', 'roll', 'riser'},
    'C': {'kick', 'hat', 'rim', 'bass', 'stab', 'acc', 'clap'},
    'outro': {'kick', 'rim', 'hat'},
}
# the bass bar (sixteenth, length in sixteenths, velocity): the and-of-2 is the strongest hit, the one is empty
BASS = [(6, 2, 120), (10, 1, 92), (13, 1, 84), (14, 2, 100)]
STAB_CHORD = [52, 55, 59, 62]          # E minor 7, the stab through a comb

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

def merge_kit(events, total):
    """kit hits that land together become one chord token"""
    by = {}
    for at, p, d, v in events:
        key = round(at, 4)
        by.setdefault(key, []).append((p, v))
    ev = [(at, ','.join(sorted({p for p, _ in hs})), 0.25, max(v for _, v in hs)) for at, hs in by.items()]
    return line(ev, total)

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 'n': n, 't': t}); t += 4.0
    total = t
    kit, bass, stab, sub, riser = [], [], [], [], []
    for b in bars:
        s, t0, h, i = b['sec'], b['t'], HAS[b['sec']], b['i']
        g0 = int(round(t0 * 4))                       # global sixteenth index of the bar's one
        root = 28 if s != 'B' or (i // 8) % 2 == 0 else 31   # E1, G1 for alternate eight-bar halves of B
        for q in range(16):
            g = g0 + q
            at = t0 + q * 0.25 + (0.035 if q % 2 else 0.0)   # the odd sixteenths lean late (a little swing)
            if 'kick' in h and q % 4 == 0:
                kit.append((at, 'k', 0.25, 120))
                sub.append((at, nm(28), 0.9, 110))
            if 'hat' in h and q % 4 == 2:
                kit.append((at, 'h', 0.25, 92))
            if 'hat' in h and q % 2 == 1 and s in ('B', 'C'):
                kit.append((at, 'h', 0.25, 58))
            if 'rim' in h and g % 3 == 0:
                kit.append((at, 'rs', 0.25, 96 if s != 'break' else 110))
            if 'acc' in h and g % 7 == 0:
                kit.append((at, 'oh', 0.25, 100))
            if 'clap' in h and q % 4 == 2:
                kit.append((at, 'rd', 0.25, 76))
            if 'clap' in h and q in (4, 12):
                kit.append((at, 'cp', 0.25, 100))
            if 'stab' in h and g % 5 == 0:
                stab.append((at, ','.join(nm(m) for m in STAB_CHORD), 0.2, 96 if g % 15 == 0 else 80))
        if 'bass' in h:
            for q, ln, v in BASS:
                bass.append((t0 + q * 0.25, root, ln * 0.25 - 0.02, v))
        if 'buildhat' in h:
            # THE ACCELERATING BUILD: the hat rate doubles every four bars (8ths, 16ths, 16th triplets, 32nds)
            step = (0.5, 0.25, 1 / 6, 0.125)[min(3, i // 4)]
            x = 0.0
            while x < 4.0 - 1e-6:
                kit.append((t0 + x, 'h', 0.25, 70 + 2 * i))
                x += step
        if 'roll' in h and i >= 8:
            st = 0.5 if i < 12 else 0.25
            x = 0.0
            while x < 4.0 - 1e-6:
                kit.append((t0 + x, 's', 0.25, 60 + 3 * i))
                x += st
        if 'riser' in h and i % 4 == 0:
            riser.append((t0, 'C4', 15.9, 80 + 2 * i))
    end_s = total * SPB
    # dynamics: the intro and outro sit lower, the break drops, the build climbs from low
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'] * SPB)
    lv = {'intro': -5, 'A': -1, 'break': -6, 'B': 0, 'build': -7, 'C': 0, 'outro': -4}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.3):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    tb, tc = secs['build'], secs['C']
    dyn = [p for p in dyn if not (tb < float(p[0][:-1]) < tc)]
    dyn.insert([k for k, p in enumerate(dyn) if float(p[0][:-1]) >= tc][0], [f'{tc - 0.31:.3f}s', -1])
    return {
        'about': "Chirpers - Phantom Downbeat (Chirpers IV), track 9 by chirper-one: POLYMETRIC TOOL TECHNO. Generated by "
                 "compose/chirpers4/src/chirpers4-t9.py; see its docstring and compose/chirpers4/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2:.2f}s', 'ceiling': '-0.1dB',
        'buses': {'rumble': {'fx': ['reverb kind=hall decay=2.5s mix=1', 'lp cutoff=180', 'drive drive=0.4 mix=1'],
                             'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=32', 'peak cutoff=45 q=1 gain=-4dB', 'peak cutoff=300 q=0.8 gain=-3dB', 'lowshelf cutoff=200 gain=-7dB', 'peak cutoff=3000 q=0.7 gain=4dB', 'highshelf cutoff=4500 gain=6dB']},
                          {'type': 'gain', 'gain': '+17dB'},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 3, 'attack': '10ms', 'release': '120ms', 'makeup': '2dB'},
                          {'type': 'compressor', 'threshold': '-8dB', 'ratio': 6, 'attack': '1ms', 'release': '50ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'gain', 'gain': '+8dB'}, 'limiter ceiling=-0.3dB'],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            {'name': 'kit', 'patch': '909', 'gain': '-2dB', 'sends': {'rumble': '-15dB'}, 'score': merge_kit(kit, total)},
            {'name': 'sub', 'patch': '808', 'gain': '-17dB', 'fx': [{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '300ms', 'curve': 0.6}], 'score': line(sub, total)},
            # THE PHANTOM BASS: harmonics 2-5 only (no fundamental), driven, pumping against the kick
            {'name': 'bass', 'patch': {'synth': {'layers': [{'type': 'additive', 'partials': [[2, 1.0], [3, 0.8], [4, 0.6], [5, 0.45]]}],
                                                 'amp': {'a': '2ms', 'd': '180ms', 's': 0.5, 'r': '60ms'}}},
             'gain': '-8dB', 'fx': [{'type': 'drive', 'drive': 0.3, 'mix': 0.5}, {'type': 'pump', 'on': 'kit.k', 'depth': '-9dB', 'release': '300ms', 'curve': 0.6}],
             'notes': [{'at': f'{at * SPB:.4f}s', 'len': f'{d * SPB:.4f}s', 'pitch': m, 'vel': round(v / 127, 3)} for at, m, d, v in bass]},
            {'name': 'stab', 'patch': 'brass-stab', 'gain': '-5dB', 'pan': 0.2,
             'fx': [{'type': 'filter', 'kind': 'comb', 'cutoff': 220, 'q': 7}, {'type': 'pump', 'on': 'kit.k', 'depth': '-8dB', 'release': '300ms', 'curve': 0.6},
                    {'type': 'delay', 'time': '3/16', 'feedback': 0.35, 'mix': 0.25}], 'score': line(stab, total)},
            {'name': 'riser', 'patch': 'fx-riser-shepard', 'gain': '-10dB', 'score': line(riser, total)},
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
