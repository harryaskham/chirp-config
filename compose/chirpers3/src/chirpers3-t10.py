#!/usr/bin/env python3
"""chirpers3-t10 (chirper-one): CHILLWAVE DUSK, the closer of 'Tape Weather' (Chirpers III).

A sunset synth piece at 78 bpm: a soft drum machine and a juno pad that breathes against the kick (sidechain duck),
under a dreamy wordless vox melody, a slow arpeggio through a warbling tape deck, and a pulsing bass.
THE RUN-OUT is the form. After the full band, every section loses something - the kick, then the arp, then the bass
- until only the vox and the pad are left; then the tape slows to a stop and the record ends in crackle.

Harmony: Dmaj9, Bm11, Gmaj7#11, A6sus, four bars each (v5; two bars each before).
Form: dawn (pad and crackle, the vox fragment), A (the band), B (+ the vox melody), runout1 (no kick), runout2 (no
arp), runout3 (no bass), end (the pad alone, the tape stops).
Emits songs/chirpers3-t10.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers3-t10.yaml")
BPM = 78
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

# (v9) the harmony slows in the long sections: A holds each chord eight bars, B six
# the B section (the vox's full song) turns to its own progression - Gmaj7#11 A6sus F#m11 Bm9 (IV V iii vi) - so the
# sunset peak is a new place, not the same loop with a voice on it
CHORDS_B = [(31, [50, 54, 59, 61, 66]), (33, [52, 57, 59, 62, 66]), (30, [49, 52, 57, 59, 64]), (35, [50, 54, 57, 61, 64])]
CHORDS = [(38, [54, 57, 61, 64, 66]), (35, [50, 54, 57, 61, 64]), (31, [50, 54, 59, 61, 66]), (33, [52, 57, 59, 62, 66])]
# the vox melody: two 4-bar phrases (MIDI, beats), the second answering higher
VOX = [[(66, 2), (69, 2)], [(71, 3), (69, 1)], [(67, 2), (66, 2)], [(64, 4)],
       [(69, 2), (71, 2)], [(74, 3), (73, 1)], [(71, 2), (69, 2)], [(66, 4)]]
FORM = [('dawn', 8), ('A', 16), ('B', 24), ('runout1', 8), ('runout2', 8), ('runout3', 8), ('end', 6), ('lock', 4)]
HAS = {   # which voices play in each section (the run-out removes one at a time)
    'dawn': {'pad', 'voxfrag'}, 'A': {'pad', 'kick', 'kit', 'bass', 'arp'}, 'B': {'pad', 'kick', 'kit', 'bass', 'arp', 'vox'},
    'runout1': {'pad', 'kit', 'bass', 'arp', 'vox'}, 'runout2': {'pad', 'kit', 'bass', 'vox'},
    'runout3': {'pad', 'vox'}, 'end': {'pad', 'lastvox'}, 'lock': set()}

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

def notes(events):
    return [{'at': f'{at * SPB:.4f}s', 'len': f'{d * SPB:.4f}s', 'pitch': m, 'vel': round(v / 127, 3)} for at, m, d, v in events]

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 't': t, 'c': (CHORDS_B[(i // 6) % 4] if name == 'B' else CHORDS[(i // 8) % 4] if name == 'A' else CHORDS[(len(bars) // 4) % 4])}); t += 4.0
    total = t
    kit, pad, bass, arp, vox, locked = [], [], [], [], [], []
    for k, b in enumerate(bars):
        s, t0, (root, ch) = b['sec'], b['t'], b['c']
        h = HAS[s]
        if 'pad' in h:
            for j, m in enumerate(ch):
                pad.append((t0 + j * 0.03, m, 3.95, 62 if s != 'end' else 56 - 3 * b['i']))
        if 'kick' in h:
            for q in range(4): kit.append((t0 + q, 'k', 0.25, 100))
        if 'kit' in h:
            for q in (1, 3): kit.append((t0 + q, 'cp' if s in ('B', 'runout1') else 's', 0.25, 84))
            for e in range(8):
                if e % 2: kit.append((t0 + e * 0.5, 'h', 0.25, 70 if e % 4 == 1 else 60))
        if 'kit' in h and s in ('A', 'B', 'runout1', 'runout2'):
            # a CLAVE in dotted eighths (every 3 sixteenths, two bars across) - the dusk's slow-turning second clock
            for q in range(16):
                if ((k % 2) * 16 + q) % 3 == 0:
                    kit.append((t0 + q * 0.25, 'cl', 0.25, 64))
        if 'bass' in h:
            for e in range(8):
                bass.append((t0 + e * 0.5, nm(root), 0.4, 96 if e % 2 == 0 else 74))
        if 'arp' in h:
            seq = ch[1:] + ch[-2:0:-1]
            for e in range(16):
                arp.append((t0 + e * 0.25, nm(seq[e % len(seq)] + 12), 0.22, 70 if e % 4 == 0 else 58))
        if s == 'lock':
            # THE LOCKED GROOVE (after the tape stops): the needle sticks in the record's run-out - a two-beat shred of
            # the vox line (F#4, A4) repeats, muffled and wobbling, over a louder crackle, until it fades
            for q in range(2):
                locked.append((t0 + 2 * q, 66, 0.9, 64 - 3 * b['i']))
                locked.append((t0 + 2 * q + 1, 69, 0.9, 60 - 3 * b['i']))
        if 'lastvox' in h and b['i'] < 4:
            # THE LAST WORD: over the bare pad, as the tape begins to sag, the vox sings the first phrase once more,
            # softer each bar
            at = t0
            for m, d in VOX[b['i']]:
                vox.append((at, m, d - 0.1, 60 - 4 * b['i'])); at += d
        if 'vox' in h or ('voxfrag' in h and b['i'] >= 4):
            phrase = VOX[(k - (8 if s == 'B' else 0)) % 8] if 'vox' in h else VOX[3 + (b['i'] % 2) * 4]
            at = t0
            for m, d in phrase:
                vox.append((at, m, d - 0.1, 78 if s in ('B', 'runout1', 'runout2') else 64)); at += d
    end_s = total * SPB
    # THE SWEEP (chirper-two's new ladder filter): the arp lives behind a resonant 4-pole that stays nearly shut
    # through A, opens over the whole of B (450 Hz -> 4 kHz, the song's sunset peak), and closes again through the
    # first run-out before the arp leaves
    tb = [b['t'] for b in bars if b['sec'] == 'B'][0] * SPB
    tr1 = [b['t'] for b in bars if b['sec'] == 'runout1'][0] * SPB
    tr2 = [b['t'] for b in bars if b['sec'] == 'runout2'][0] * SPB
    sw = [['0s', 0.1], [f'{tb:.2f}s', 0.15], [f'{tr1:.2f}s', 1.0], [f'{tr2:.2f}s', 0.2]]
    # THE WEAR (chirper-two's tape-deck warp): the pad's and the vox's tape wears harder as the voices leave - the
    # wow and flutter at x1 through the full band, x1.4 in the second run-out, x1.8 in the third, x2 at the end
    secs = {b['sec']: b['t'] * SPB for b in reversed(bars)}
    wear = [['0s', 1.0], [f"{secs['runout2']:.2f}s", 1.0], [f"{secs['runout2'] + 6:.2f}s", 1.4],
            [f"{secs['runout3']:.2f}s", 1.4], [f"{secs['runout3'] + 6:.2f}s", 1.8], [f"{secs['end']:.2f}s", 1.8], [f"{secs['end'] + 5:.2f}s", 2.0]]
    # THE LAST BREATH (wM's cloud fx on the vox): the vox's last word dissolves into grains as it fades, and the
    # grains FREEZE on its final note, hanging over the bare pad while the tape stops under them
    t_end = secs['end']
    vm = [['0s', 0], [f'{t_end + 2 * 4 * SPB:.2f}s', 0], [f'{t_end + 4 * 4 * SPB:.2f}s', 0.7]]
    vf = [['0s', 0], [f'{t_end + 3.5 * 4 * SPB - 0.02:.2f}s', 0], [f'{t_end + 3.5 * 4 * SPB:.2f}s', 1]]
    t_lock = secs['lock']
    # THE TAPE CHEWS (wM's chop fx on the master): in the last two bars of the third run-out the deck starts eating
    # the tape - the bar is cut into eight and replayed with doubles, reversals and gaps - just before the end section
    tr3 = [b['t'] for b in bars if b['sec'] == 'runout3'][0]
    a_, e_ = (tr3 + 6 * 4) * SPB, (tr3 + 8 * 4) * SPB
    chew = [['0s', 0], [f'{a_ - 0.02:.3f}s', 0], [f'{a_:.3f}s', 1], [f'{e_ - 0.02:.3f}s', 1], [f'{e_:.3f}s', 0]]
    t_end = bars[[b['sec'] for b in bars].index('end')]['t'] * SPB
    return {
        'about': "Chirpers - Tape Weather (Chirpers III), track 10 by chirper-one: CHILLWAVE DUSK, the closer. Generated by "
                 "compose/chirpers3/src/chirpers3-t10.py; see its docstring and compose/chirpers3/styles.md.",
        'tempo': BPM, 'feel': {'drift': '4ms', 'drift_bars': 4}, 'length': f'{end_s + 3:.2f}s', 'ceiling': '-0.1dB',
        'master': {'fx': [{'type': 'chop', 'slices': 8, 'pattern': '0 0 r1 . 3 r3 _ 5', 'length': '1/1', 'mix': {'value': 0, 'mod': [{'src': 'auto.chew', 'amount': 1}]}},
                          {'type': 'tapestop', 'time': '4b', 'mix': 1, 'stop': {'value': 0, 'mod': [{'src': 'auto.ts', 'amount': 1}]}},
                          {'type': 'eq', 'bands': ['highpass cutoff=30', 'lowshelf cutoff=70 gain=6dB', 'peak cutoff=400 q=1 gain=-4dB', 'highshelf cutoff=6000 gain=7dB']},
                          {'type': 'gain', 'gain': '+21dB'},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 3, 'attack': '15ms', 'release': '180ms', 'makeup': '2dB'},
                          {'type': 'compressor', 'threshold': '-10dB', 'ratio': 6, 'attack': '1ms', 'release': '60ms', 'makeup': '3dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   'auto': {'chew': {'points': chew}, 'ts': {'points': [['0s', 0], [f'{t_lock - 4 * 4 * SPB:.2f}s', 0], [f'{t_lock - 4 * 4 * SPB + 0.05:.2f}s', 1], [f'{t_lock - 0.05:.2f}s', 1], [f'{t_lock:.2f}s', 0]]},
                            'fade': {'points': [['0s', -14], ['20s', -10], ['24.5s', 0], [f'{t_end - 2:.2f}s', 0], [f'{t_end:.2f}s', -9], [f'{end_s:.2f}s', -20]]}}},
        'tracks': [
            {'name': 'kit', 'patch': 'electro-kit', 'gain': '-4dB', 'fx': ['crush bits=12 rate=26kHz mix=0.4'], 'score': line(kit, total)},
            {'name': 'pad', 'patch': 'juno-pad', 'gain': '-8dB', 'fx': [{'type': 'duck', 'by': 'kit', 'depth': 0.6, 'attack': '5ms', 'release': '220ms'},
                                                                          {'type': 'tape', 'drive': 0.1, 'mix': 0.5, 'wow': 14, 'flutter': 2, 'drift': 1.5, 'tone': 7000, 'sweep': 0.5, 'seed': 8,
                                                                           'warp': {'value': 0, 'mod': [{'src': 'auto.wear', 'amount': 1}]}}],
             'auto': {'wear': {'points': wear}},
             'notes': notes(pad)},
            {'name': 'bass', 'patch': 'analog-bass', 'gain': '-5dB', 'score': line(bass, total)},
            {'name': 'arp', 'patch': 'arp-pluck', 'gain': '-10dB', 'pan': 0.3, 'auto': {'sw': {'points': sw}}, 'fx': [{'type': 'filter', 'kind': 'ladder', 'cutoff': {'value': 450, 'mod': [{'src': 'auto.sw', 'amount': 3.2}]}, 'q': 9}, 'tape drive=0.15 mix=0.5 wow=10 flutter=2.5 drift=1 tone=6500 sweep=0.6 seed=2', {'type': 'delay', 'time': '3/16', 'feedback': 0.35, 'mix': 0.3}], 'score': line(arp, total)},
            {'name': 'vox', 'patch': 'dream-vox', 'gain': '-6dB', 'pan': -0.1, 'auto': {'wear': {'points': wear}, 'vm': {'points': vm}, 'vf': {'points': vf}},
             'fx': [{'type': 'cloud', 'size': '200ms', 'density': 14, 'position': '600ms', 'spray': '450ms', 'pitch': 0, 'scatter': 0.1, 'reverse': 0.3, 'spread': 0.9, 'seed': 6,
                     'freeze': {'value': 0, 'mod': [{'src': 'auto.vf', 'amount': 1}]}, 'mix': {'value': 0, 'mod': [{'src': 'auto.vm', 'amount': 1}]}},
                    {'type': 'tape', 'drive': 0.05, 'mix': 0.4, 'wow': 8, 'flutter': 1.5, 'drift': 1, 'tone': 8000, 'sweep': 0.4, 'seed': 14,
                     'warp': {'value': 0, 'mod': [{'src': 'auto.wear', 'amount': 1}]}}], 'notes': notes(vox)},
            {'name': 'locked', 'patch': 'dream-vox', 'gain': '-8dB', 'fx': [{'type': 'filter', 'kind': 'lp', 'cutoff': 1500, 'q': 0.7},
                                                                             'tape drive=0.2 mix=0.7 wow=22 flutter=4 drift=2 tone=4000 sweep=0.8 seed=41'],
             'notes': notes(locked)},
            {'name': 'crackle', 'patch': 'fx-crackle', 'gain': '-8dB', 'score': f"C4/{total - 0.2:.4f}b@80 R/0.2b"},
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
