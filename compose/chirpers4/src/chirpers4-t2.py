#!/usr/bin/env python3
"""chirpers4-t2 (chirper-one): ROLLING / BROKEN TECHNO, "the gallop splits", for 'Phantom Downbeat' (Chirpers IV).

A broken-kick roller at 130 bpm built on an AUDITORY-STREAMING illusion (van Noorden's gallop).
- THE GALLOP: two bleeps, A and B, play A-B-A-rest in sixteenths. While B sits a semitone or two from A, the ear
  hears one stream with a galloping rhythm. As B moves away (a fifth, an octave, a tenth), the gallop breaks: the
  ear splits it into two streams, A twice as fast as B, and the galloping rhythm disappears although no note's timing
  has changed. A and B are on their own tracks; as they split they also pan apart.
- The drums are broken: no four-on-the-floor. The kick rolls on 1, the and-of-2 and 3-and, with a ghost before 4,
  and in the peak it uses the harder kick on the ones.
- (v2) The gallop breathes and is rounder: the square under the sine is quieter, a 3.2 kHz low-pass takes the edge
  off, and more of it goes to the space delay; it enters eight bars into A, rests through the end of B, and leaves for
  two bars in every eight of the peak.
- (v5) In the second groove and the peak the floor moves: the reese's root and the gallop's A step A - F - C - G,
  eight bars each.
- A reese bass rolls in sixteenths, jumping octaves, pumping against the kick.
- Form: intro (drums), A (bass, gallop close), B (claps, the gallop drifting to the edge), break (no kick: the gallop
  pulled apart to a tenth, two streams), C (peak: the distance swings every four bars, so the ear flips between one
  gallop and two streams), outro.

Emits songs/chirpers4-t2.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers4-t2.yaml")
BPM = 130
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('A', 32), ('B', 32), ('break', 16), ('C', 32), ('outro', 16)]
HAS = {
    'intro': {'kick', 'hat'},
    'A': {'kick', 'hat', 'bass', 'gallop'},
    'B': {'kick', 'hat', 'bass', 'gallop', 'clap', 'oh'},
    'break': {'gallop', 'hat'},
    'C': {'kick', 'hat', 'bass', 'gallop', 'clap', 'oh', 'rim'},
    'outro': {'kick', 'hat'},
}
KICK = [(0, 124), (6, 112), (10, 118), (13, 80)]          # broken: 1, the and-of-2, 3-and, a ghost before 4
BASS = [0, 0, 12, 0, 0, 12, 0, 7, 0, 0, 12, 0, 10, 0, 12, 0]   # the reese's rolling sixteenths (offsets from A1)
A_NOTE = 69                                                   # A4

def gap(sec, i):
    """the semitone distance from A to B: the illusion's control"""
    if sec == 'A': return 1 if i < 16 else 2
    if sec == 'B': return 2 + (i // 8)                        # 2, 3, 4, 5: drifting to the edge
    if sec == 'break': return min(16, 5 + i)                  # pulled apart: two streams by the end
    if sec == 'C': return (2, 16, 3, 19, 2, 12, 4, 24)[i // 4]   # swings: one gallop, two streams, ...
    return 0

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
    by = {}
    for at, p, d, v in events:
        by.setdefault(round(at, 4), []).append((p, v))
    return line([(at, ','.join(sorted({p for p, _ in hs})), 0.25, max(v for _, v in hs)) for at, hs in by.items()], total)

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 'n': n, 't': t}); t += 4.0
    total = t
    kit, bass, ga, gb, pad = [], [], [], [], []
    # (v7) THE CORRIDOR'S CHORD: Behind the Door (t1) ends in its corridor on a deep Am9 pad; The Gallop Splits opens
    # with that chord still ringing (A2 C3 E3 G3 B3), fading over the first eight bars as the broken kick takes the floor
    for k in range(2):
        pad.append((k * 16.0, ','.join(nm(m) for m in (45, 48, 52, 55, 59)), 15.8, 70 - 14 * k))
    for b in bars:
        s, t0, h, i = b['sec'], b['t'], HAS[b['sec']], b['i']
        # (v5) THE TIDE TURNS: in the second groove and the peak the whole floor moves, eight bars per step, A - F - C - G
        # (the reese's root and the gallop's A note together, the gap kept), then home; the first groove and the break
        # stay on A, so the harmony is a reward for the second half
        rt = (0, -4, 3, -2)[(i // 8) % 4] if s in ('B', 'C') else 0
        for q in range(16):
            at = t0 + q * 0.25 + (0.03 if q % 2 else 0.0)
            if 'kick' in h:
                for kq, kv in KICK:
                    if kq == q:
                        kit.append((at, 'kh' if (s == 'C' and q == 0) else 'k', 0.25, kv))
            if 'hat' in h:
                kit.append((at, 'h', 0.25, (88 if q % 4 == 2 else 56) if s != 'intro' or q % 2 == 0 else 0))
            if 'oh' in h and q % 4 == 2 and (i % 2 == 1):
                kit.append((at, 'oh', 0.25, 82))
            if 'clap' in h and q in (4, 12):
                kit.append((at, 'cp', 0.25, 104))
            if 'rim' in h and q in (3, 7, 11):
                kit.append((at, 'rs', 0.25, 78))
            if 'bass' in h:
                bass.append((at, nm(33 + rt + BASS[q]), 0.22, 96 if q % 4 == 0 else 80))
        # (v2) the gallop breathes: it enters eight bars into A, rests for the last eight bars of B, and drops out for
        # two bars at the end of every eight in the peak - so each return of the illusion is heard fresh
        rest = (s == 'A' and i < 8) or (s == 'B' and i >= 24) or (s == 'C' and i % 8 >= 6)
        if 'gallop' in h and not rest:
            d = gap(s, i)
            for beat in range(4):
                x = t0 + beat
                ga.append((x, nm(A_NOTE + rt), 0.2, 92))
                gb.append((x + 0.25, nm(A_NOTE + rt + d), 0.2, 88))
                ga.append((x + 0.5, nm(A_NOTE + rt), 0.2, 84))
    kit = [k for k in kit if k[3] > 0]
    end_s = total * SPB
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'] * SPB)
    # the streams pull apart in space as they split: B's pan follows the gap
    pan_pts = []
    for b in bars:
        if 'gallop' in HAS[b['sec']]:
            pan_pts.append([f"{b['t'] * SPB:.3f}s", round(min(1.0, gap(b['sec'], b['i']) / 16), 3)])
    lv = {'intro': -5, 'A': -1, 'B': 0, 'break': -6, 'C': 0, 'outro': -4}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.3):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    # (v4) THE HELD BREATH: the last beat of the break - the gallop at its widest, split into two streams - is cut to
    # silence, and the peak's first hard kick lands out of it
    tg = secs['C']; g0 = tg - SPB
    pts = [(float(p[0][:-1]), p[1]) for p in dyn]
    before = [p for p in pts if p[0] <= g0 - 0.02]; after = [p for p in pts if p[0] >= tg - 0.004]
    pts = before + [(g0 - 0.01, before[-1][1]), (g0, -40), (tg - 0.006, -40)] + after
    dyn = [['0s', pts[0][1]]] + [[f'{t_:.3f}s', v] for t_, v in pts if t_ > 0]
    gal = {'synth': {'layers': [{'type': 'osc', 'wave': 'sine'}, {'type': 'osc', 'wave': 'square', 'level': 0.1}],
                     'amp': {'a': '1ms', 'd': '90ms', 's': 0.0, 'r': '40ms'}}}
    return {
        'about': "Chirpers - Phantom Downbeat (Chirpers IV), track 2 by chirper-one: ROLLING / BROKEN TECHNO, the gallop splits. "
                 "Generated by compose/chirpers4/src/chirpers4-t2.py; see its docstring and compose/chirpers4/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2:.2f}s', 'ceiling': '-1dB',
        'buses': {'rumble': {'fx': ['reverb kind=hall decay=2.2s mix=1', 'lp cutoff=170', 'drive drive=0.35 mix=1'], 'returns': []},
                  'space': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.4, 'mix': 1}, 'lp cutoff=3500', 'hp cutoff=400'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=34', 'peak cutoff=44 q=1 gain=-8dB', 'lowshelf cutoff=200 gain=-6dB', 'peak cutoff=160 q=0.9 gain=-3dB',
                                                   'peak cutoff=2200 q=0.6 gain=6dB', 'highshelf cutoff=4500 gain=3dB', 'highshelf cutoff=10000 gain=-3dB']},
                          {'type': 'gain', 'gain': '+17dB'},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 3, 'attack': '10ms', 'release': '120ms', 'makeup': '2dB'},
                          {'type': 'compressor', 'threshold': '-8dB', 'ratio': 6, 'attack': '1ms', 'release': '50ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'compressor', 'threshold': '-6dB', 'ratio': 4, 'attack': '3ms', 'release': '80ms', 'makeup': '6dB'}, 'lp cutoff=15000'],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            {'name': 'kit', 'patch': '909', 'gain': '-2dB', 'sends': {'rumble': '-15dB'}, 'score': merge_kit(kit, total)},
            # (v3) THE BREATHING REESE: a slow LFO (one cycle every eight bars) sweeps a low-pass over the rolling bass, so the
            # sixteenths open and close like a tide under the gallop instead of sitting still
            {'name': 'bass', 'patch': 'reese', 'gain': '-9dB', 'lfo': {'tide': 'sine rate=8/1 phase=0.75'},
             'fx': [{'type': 'filter', 'kind': 'lp', 'q': 1.1, 'cutoff': {'value': 2000, 'mod': [{'src': 'lfo.tide', 'amount': 1.0}]}},
                    {'type': 'pump', 'on': 'kit.k', 'depth': '-9dB', 'release': '300ms', 'curve': 0.6}], 'score': line(bass, total)},
            {'name': 'pad', 'patch': 'juno-pad', 'gain': '-10dB', 'fx': ['lp cutoff=2500'], 'score': line(pad, total)},
            {'name': 'galA', 'patch': gal, 'gain': '-13dB', 'pan': -0.15, 'sends': {'space': '-10dB'}, 'fx': ['lp cutoff=3200'], 'score': line(ga, total)},
            {'name': 'galB', 'patch': gal, 'gain': '-13dB', 'sends': {'space': '-10dB'}, 'fx': ['lp cutoff=3200'],
             'pan': {'value': 0.15, 'mod': [{'src': 'auto.split', 'amount': 0.7}]}, 'auto': {'split': {'points': pan_pts}},
             'score': line(gb, total)},
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
