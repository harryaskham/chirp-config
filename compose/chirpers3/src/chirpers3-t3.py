#!/usr/bin/env python3
"""chirpers3-t3 (chirper-one): WARPED BOOM-BAP for 'Tape Weather' (Chirpers III).

A dusty, drunk head-nod beat off a worn sampler, at 84 bpm with swung sixteenths. Nothing sits on the grid:
- the kick is a hair early, the snare lazy-late, the hats swung and scattered by a seeded drift;
- rolled tape-piano chords (each note a few ms after the last) over a late, sliding synth bass;
- a wobbly boc-lead hook and vinyl crackle under everything.
Every few bars the loop TRIPS (a bar cut short to 7/8 or 3/4, a beat dropped) and catches itself. The WONK is the form:
the drift grows through the song, a tape-stop drops into the break, and the last chorus snaps back nearly onto the grid.

Form: intro (crackle and piano), A (the beat), A' (+ hook), break (tape-stop, then piano and bass only), A'' (the
drift at its widest), last (snapped tight, the hook doubled), outro (the piano alone, the tape running down).
Emits songs/chirpers3-t3.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers3-t3.yaml")
BPM = 84
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

# chords (MIDI, rolled bottom up): a 4-bar loop, two chords a bar; F minor-ish with bedroom colours
LOOP = [([41, 56, 60, 63, 67], [44, 58, 63, 67, 70]),     # Fm9 | Abmaj9
        ([39, 55, 58, 62, 65], [37, 53, 56, 60, 63]),     # Eb6/9 | Dbmaj9
        ([41, 56, 60, 63, 67], [46, 56, 61, 63, 68]),     # Fm9 | Bbm11
        ([36, 52, 55, 58, 63], [36, 52, 55, 59, 62])]     # C7#9 | C7b9
FORM = [('intro', 4), ('A', 8), ('A2', 8), ('break', 4), ('A3', 8), ('last', 8), ('outro', 4)]
# the trips: (section, bar index) -> bar length in beats (a bar cut short)
TRIPS = {('A', 3): 3.5, ('A2', 7): 3.0, ('A3', 3): 3.5, ('A3', 5): 3.0, ('A3', 7): 3.5}
DRIFT = {'intro': 0.5, 'A': 1.0, 'A2': 1.3, 'break': 1.0, 'A3': 1.8, 'last': 0.35, 'outro': 0.6}

_seed = [12345]
def rnd():
    """a seeded LCG in -1..1 (deterministic drift)"""
    _seed[0] = (_seed[0] * 1103515245 + 12345) & 0x7fffffff
    return (_seed[0] / 0x7fffffff) * 2 - 1

def bars():
    out, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            ln = TRIPS.get((name, i), 4.0)
            out.append({'sec': name, 'i': i, 'beats': ln, 't': t, 'loop': LOOP[i % 4]})
            t += ln
    return out, t

def line(events, total):
    """events: [(t_beats, pitchstr, dur_beats, vel)] -> one sequential token line with exact rests (overlaps trimmed)"""
    ev = sorted(events)
    toks, t = [], 0.0
    for k, (at, p, d, v) in enumerate(ev):
        if at < t - 1e-6:
            continue
        if at > t + 1e-4:
            toks.append(f"R/{at - t:.4f}b")
        nxt = ev[k + 1][0] if k + 1 < len(ev) else total
        d = max(0.02, min(d, nxt - at))
        toks.append(f"{p}/{d:.4f}b@{v}")
        t = at + d
    if total > t + 1e-4:
        toks.append(f"R/{total - t:.4f}b")
    return ' '.join(toks)

def swing(s16):
    """sixteenth index -> beats, swung ~62%"""
    pair, odd = divmod(s16, 2)
    return pair * 0.5 + (0.31 if odd else 0.0)

def build():
    B, total = bars()
    kit, piano, bass, lead, crackle = [], [], [], [], []
    for b in B:
        sec, t0, L, dr = b['sec'], b['t'], b['beats'], DRIFT[b['sec']]
        ms = lambda x: x / 1000 / SPB      # milliseconds -> beats
        n16 = int(L * 4)
        # ---- drums (the beat sections) ----
        if sec in ('A', 'A2', 'A3', 'last'):
            kicks = [0, 7, 10] if b['i'] % 2 == 0 else [0, 6, 11]
            for s in kicks:
                if s < n16: kit.append((t0 + swing(s) + ms(-15 * dr) + ms(4 * rnd()), 'k', 0.25, 104 if s == 0 else 92))
            for s in (4, 12):
                if s < n16: kit.append((t0 + swing(s) + ms(35 * dr) + ms(6 * rnd()), 's', 0.25, 98))
            for s in range(0, n16, 2):
                if (sec == 'A3' and s % 8 == 6 and b['i'] % 3 == 1):
                    continue                           # a dropped hat: the loop hiccups
                kit.append((t0 + swing(s) + ms(20 * dr * rnd()), 'h', 0.25, 72 + int(10 * rnd()) if s % 4 else 84))
            # the SHAKER in dotted eighths (every 3 sixteenths, straight, not swung): a second clock that never
            # lines up with the swung hats - the wonk you feel before you hear it
            for s in range(0, n16, 3):
                kit.append((t0 + s * 0.25 + ms(10 * dr * rnd()), 'sh', 0.25, 78 if s % 6 else 90))
            if b['i'] % 4 == 3 and n16 >= 15:
                kit.append((t0 + swing(15) + ms(25 * dr), 'oh', 0.25, 70))
            if sec in ('A2', 'A3', 'last') and b['i'] % 2 == 1:
                kit.append((t0 + swing(9) + ms(30 * dr), 'rs', 0.25, 60))
        # ---- piano: two rolled chords a bar (the second lands late), lazier in the drifting sections ----
        for half, ch in enumerate(b['loop']):
            at = t0 + half * 2.0 + (ms(40 * dr) if half else ms(10 * dr))
            if at >= t0 + L: continue
            for j, m in enumerate(ch[1:]):
                piano.append((at + ms(18 * j * (1 + dr / 2)), nm(m), (2.0 if half == 0 else L - 2.0) - 0.1, 64 - 3 * j))
        # ---- bass: the root late and gliding to the next chord's root ----
        if sec not in ('intro', 'outro'):
            r0, r1 = b['loop'][0][0], b['loop'][1][0]
            bass.append((t0 + ms(30 * dr), nm(r0), 1.4, 96))
            bass.append((t0 + 1.5 + ms(30 * dr), nm(r0 + 7 if r0 + 7 < 50 else r0 - 5), 0.4, 80))
            if L > 2.0:
                bass.append((t0 + 2.0 + ms(45 * dr), nm(r1), min(1.5, L - 2.1), 94))
        # ---- the hook (boc-lead): a 2-bar phrase answered a step lower, in A2 and A3 and doubled in 'last' ----
        if sec in ('A2', 'A3', 'last') and L >= 3.5:
            ph = [(0.5, 72, 0.5), (1.0, 75, 0.75), (2.0, 72, 0.5), (2.5, 70, 1.25)] if b['i'] % 2 == 0 else \
                 [(0.25, 68, 0.5), (0.75, 70, 0.5), (1.5, 67, 1.5)]
            for at, m, d in ph:
                lead.append((t0 + at + ms(25 * dr * rnd()), nm(m - (2 if b['i'] % 4 >= 2 else 0)), d, 80))
    # the crackle under everything
    crackle.append((0.0, 'C4', total - 0.5, 70))
    end_s = total * SPB
    # the master: a real TAPE-STOP into the break (the tapestop fx held for the two beats before it) and a dip
    tb = [b['t'] for b in B if b['sec'] == 'break' and b['i'] == 0][0] * SPB
    return {
        'about': "Chirpers - Tape Weather (Chirpers III), track 3 by chirper-one: WARPED BOOM-BAP. Generated by "
                 "compose/chirpers3/src/chirpers3-t3.py; see its docstring and compose/chirpers3/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2:.2f}s', 'ceiling': '-0.1dB',
        'master': {'fx': [{'type': 'tape', 'drive': 0.35, 'warmth': 0.6, 'mix': 0.6},
                          {'type': 'tapestop', 'time': '2b', 'mix': 1, 'stop': {'value': 0, 'mod': [{'src': 'auto.ts', 'amount': 1}]}},
                          {'type': 'eq', 'bands': ['highpass cutoff=35', 'peak cutoff=215 q=0.9 gain=-9dB', 'peak cutoff=52 q=1.2 gain=-5dB', 'highshelf cutoff=6000 gain=6dB']},
                          {'type': 'gain', 'gain': '+17dB'},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 3, 'attack': '15ms', 'release': '180ms', 'makeup': '2dB'},
                          {'type': 'compressor', 'threshold': '-10dB', 'ratio': 6, 'attack': '1ms', 'release': '60ms', 'makeup': '4dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   'auto': {'ts': {'points': [['0s', 0], [f'{tb - 2 * SPB - 0.05:.2f}s', 0], [f'{tb - 2 * SPB:.2f}s', 1], [f'{tb:.2f}s', 1], [f'{tb + 0.02:.2f}s', 0]]},
                            'fade': {'points': [['0s', -8], ['4s', 0], [f'{tb - 1.0:.2f}s', 0], [f'{tb:.2f}s', -14],
                                                [f'{tb + 2.0:.2f}s', -4], [f'{end_s - 8:.2f}s', 0], [f'{end_s:.2f}s', -30]]}}},
        'tracks': [
            {'name': 'kit', 'patch': 'lofi-kit', 'gain': '-2dB', 'score': line(kit, total)},
            {'name': 'piano', 'patch': 'tape-piano', 'gain': '-4dB', 'pan': -0.15, 'score': line(piano, total) if False else None,
             'notes': [{'at': f'{at * SPB:.4f}s', 'len': f'{d * SPB:.4f}s', 'pitch': p_midi, 'vel': v / 127}
                       for at, p, d, v in piano for p_midi in [NN.index(p[:-1]) + 12 * (int(p[-1]) + 1)]]},
            {'name': 'bass', 'patch': 'analog-bass', 'gain': '-3dB', 'score': line(bass, total)},
            {'name': 'lead', 'patch': 'boc-lead', 'gain': '-9dB', 'pan': 0.25, 'score': line(lead, total)},
            {'name': 'crackle', 'patch': 'fx-crackle', 'gain': '-7dB', 'score': line(crackle, total)},
            {'name': 'tapestop', 'patch': 'tape-piano', 'gain': '-60dB', 'score': f"R/{total - 0.5:.4f}b"},
        ]}

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    song = build()
    for t in song['tracks']:
        if t.get('score') is None:
            t.pop('score')
    song['tracks'] = [t for t in song['tracks'] if t['name'] != 'tapestop']
    if out.endswith('.json'):
        json.dump(song, open(out, 'w'), indent=1)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(song, f)
        subprocess.run(['python3', os.path.join(ROOT, 'tools', 'songfmt.py'), 'yaml', f.name, '-o', out], check=True)
        os.unlink(f.name)
    print('wrote', out, song['length'])
