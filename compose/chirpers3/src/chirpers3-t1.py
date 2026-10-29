#!/usr/bin/env python3
"""chirpers3-t1 (chirper-one): BEAT-TAPE INTRO, the opener of 'Tape Weather' (Chirpers III).

A crate-digger's first track: a soul-jazz record is found, then flipped on an MPC in front of you. 86 bpm.
- The sample is chop-souljazz: the library's 4-bar soul-jazz part cut into 16 slices, one a quarter note
  (C4 = slice 1).
- THE FLIP as form. Each section rearranges the same 16 slices further from the original order:
  found (in order, muffled like a record on the shelf), then flipped, then (after the sax) the record found again
  under the sax alone, then stuttered, then flipped harder,
  then found again as the record lifts.
- A light boom-bap kick and snare reinforce the flip. A tenor sax (physical reed) answers the chops in C mixolydian.
Emits songs/chirpers3-t1.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers3-t1.yaml")
BPM = 86
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"
def sl(i): return nm(60 + i)            # chop slice i (0..15)

FOUND = list(range(16))
FLIP1 = [0, 1, 0, 3, 8, 1, 10, 3] * 2      # two-bar flips: the new beat's cycle is half the sample's
FLIP1B = [0, 1, 0, 3, 4, 4, 6, 7, 8, 1, 10, 3, 12, 13, 4, 15]   # the sax section's four-bar flip
FLIP2 = [12, 13, 12, 3, 0, 1, 0, 6] * 2
ETHIO = [0, 4, 5, 3, 8, 9, 12, 2]          # the second record's slices used in the hard flip
# per section: (name, 4-bar blocks, pattern, muffled?)
FORM = [('found', 1, 'found'), ('flip', 2, 'flip1'), ('sax', 4, 'flip1b'), ('down', 1, 'found'), ('stutter', 1, 'stutter'),
        ('flip2', 3, 'flip2'), ('last', 1, 'found')]
# the sax: a call per 2 bars (C mixolydian), answered by the chops
SAX = [[(0.5, 67, 0.5), (1.0, 70, 0.5), (1.5, 72, 1.0), (3.0, 74, 0.5), (3.5, 72, 1.5), (5.0, 70, 0.5), (5.5, 67, 2.0)],
       [(0.5, 72, 0.5), (1.0, 74, 0.5), (1.5, 75, 1.5), (3.0, 74, 0.5), (3.5, 72, 0.5), (4.0, 70, 1.0), (5.0, 67, 2.5)]]

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
    chops, muff, kit, sax, sub, muff2, chops2 = [], [], [], [], [], [], []
    t = 0.0
    sections = []
    for name, blocks, pat in FORM:
        for blk in range(blocks):
            t0 = t
            if pat == 'stutter':
                # THE STUTTER BUILD: slice 12 in quarters, then eighths, then sixteenths, then 1 and 13 trading
                for q in range(4): chops.append((t0 + q, sl(12), 0.95, 96))
                for e in range(8): chops.append((t0 + 4 + e * 0.5, sl(12), 0.45, 92))
                for s in range(16): chops.append((t0 + 8 + s * 0.25, sl(12 if s % 4 else 13), 0.22, 88 + s))
                for s in range(8): chops.append((t0 + 12 + s * 0.5, sl(0 if s % 2 == 0 else 13), 0.45, 100))
            else:
                order = {'found': FOUND, 'flip1': FLIP1, 'flip1b': FLIP1B, 'flip2': FLIP2}[pat]
                target = muff if name in ('found', 'last') else (muff2 if name == 'down' else chops)
                for q, i in enumerate(order):
                    if pat == 'flip2' and q % 4 in (1, 2) and q % 8 != 2:
                        # THE SECOND RECORD in the hard flip: the dig's ethio-jazz slices take beats 2 and 3 of
                        # alternate bars, so two records argue inside one beat
                        chops2.append((t0 + q, sl(ETHIO[q % 8]), 0.97, 90))
                    elif pat == 'flip2' and q % 4 == 3:
                        # the harder flip: the last quarter of every bar is two eighth stabs of a different slice
                        target.append((t0 + q, sl(i), 0.45, 96)); target.append((t0 + q + 0.5, sl((i + 5) % 16), 0.45, 90))
                    else:
                        target.append((t0 + q, sl(i), 0.97, 92 if q % 4 == 0 else 84))
            # the reinforcing kit: boom-bap kick and snare once the flip starts
            if name not in ('found', 'last', 'down'):
                for bar in range(4):
                    b0 = t0 + bar * 4
                    for at in (0, 1.75, 2.5): kit.append((b0 + at + 0.01, 'k', 0.25, 104 if at == 0 else 90))
                    for at in (1, 3): kit.append((b0 + at + 0.03, 's', 0.25, 96))
                    sub.append((b0, 'C2' if FLIP1[bar * 4] < 8 else 'F2', 1.5, 96))
                    sub.append((b0 + 2.5, 'C2', 1.0, 86))
            if name in ('sax', 'flip2', 'down'):
                for ph in range(2):
                    for at, m, d in SAX[(blk * 2 + ph) % 2]:
                        sax.append((t0 + ph * 8 + at, nm(m + (12 if name == 'flip2' and ph == 1 else 0)), d, 92))
            sections.append((name, t0))
            t += 16.0
    total = t
    end_s = total * SPB
    # THE FLIP OF THE FLIP (wM's chop fx on the chops track): the last bar of each flipped section is resampled from
    # its own previous bar and replayed out of order - the producer's hand on the pads at the end of each phrase
    ends = {}
    for name, t0 in sections:
        ends[name] = t0 + 16.0
    spans = [(ends[n] - 4.0, ends[n]) for n in ('flip', 'sax', 'flip2') if n in ends]
    cp = [['0s', 0]]
    for a_, e_ in sorted(spans):
        cp += [[f'{a_ * SPB - 0.02:.3f}s', 0], [f'{a_ * SPB:.3f}s', 1], [f'{e_ * SPB - 0.02:.3f}s', 1], [f'{e_ * SPB:.3f}s', 0]]
    return {
        'about': "Chirpers - Tape Weather (Chirpers III), track 1 by chirper-one: BEAT-TAPE INTRO, the opener. Generated by "
                 "compose/chirpers3/src/chirpers3-t1.py; see its docstring and compose/chirpers3/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2.5:.2f}s', 'ceiling': '-0.1dB',
        'master': {'fx': [{'type': 'tapestop', 'time': '2b', 'mix': 1, 'stop': {'value': 0, 'mod': [{'src': 'auto.ts', 'amount': 1}]}},
                          {'type': 'eq', 'bands': ['highpass cutoff=30', 'peak cutoff=40 q=1 gain=5dB', 'peak cutoff=78 q=1.2 gain=-6dB', 'peak cutoff=330 q=0.7 gain=5dB', 'highshelf cutoff=6000 gain=6dB']},
                          {'type': 'gain', 'gain': '+14dB'},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 3, 'attack': '15ms', 'release': '180ms', 'makeup': '2dB'},
                          {'type': 'compressor', 'threshold': '-10dB', 'ratio': 6, 'attack': '1ms', 'release': '60ms', 'makeup': '3dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   # THE TURNTABLE: the record spins up to speed at the start (the tape-stop released over the first two
                   # beats) and spins down as it lifts at the end (the stop engaged over the last bar)
                   'auto': {'ts': {'points': [['0s', 1], [f'{2 * SPB:.2f}s', 1], [f'{2 * SPB + 0.02:.2f}s', 0], [f'{end_s - 4 * SPB:.2f}s', 0], [f'{end_s - 4 * SPB + 0.02:.2f}s', 1]]},
                            'fade': {'points': [['0s', -6], ['6s', 0], [f'{end_s - 8:.2f}s', 0], [f'{end_s:.2f}s', -24]]}}},
        'tracks': [
            {'name': 'chops', 'patch': 'chop-souljazz', 'gain': '-2dB', 'auto': {'cp': {'points': cp}}, 'fx': [{'type': 'chop', 'slices': 8, 'pattern': '0 r1 2 2 . r5 6 _', 'length': '1/1', 'mix': {'value': 0, 'mod': [{'src': 'auto.cp', 'amount': 1}]}}, 'tape drive=0.15 mix=0.5 wow=8 flutter=2 drift=1 tone=7000 sweep=0.5 seed=6'], 'score': line(chops, total)},
            # the record as found: the same slices through a muffled filter, like a record playing in the next room
            # THE SECOND RECORD (the dig): mid-song the digger pulls another record, an ethio-jazz side, muffled and
            # worn under the sax; the hard flip then chops it in with the soul-jazz
            {'name': 'found2', 'patch': 'chop-ethiojazz', 'gain': '-4dB', 'fx': [{'type': 'filter', 'kind': 'lp', 'cutoff': 1400, 'q': 0.7},
                                                                                'vinyl crackle=0.7 dust=0.6 noise=-56dB rumble=0.4 warp=10 wear=0.7 seed=9',
                                                                                'tape drive=0.15 mix=0.6 wow=16 flutter=3 drift=2 tone=5000 sweep=0.7 seed=12'],
             'score': line(muff2, total)},
            {'name': 'chops2', 'patch': 'chop-ethiojazz', 'gain': '-4dB', 'pan': -0.2, 'fx': ['tape drive=0.15 mix=0.5 wow=8 flutter=2 drift=1 tone=7000 sweep=0.5 seed=13'],
             'score': line(chops2, total)},
            {'name': 'found', 'patch': 'chop-souljazz', 'gain': '-4dB', 'fx': [{'type': 'filter', 'kind': 'lp', 'cutoff': 1200, 'q': 0.7},
                                                                              'vinyl crackle=0.6 dust=0.5 noise=-58dB rumble=0.4 warp=8 wear=0.6 seed=5',
                                                                              'tape drive=0.15 mix=0.6 wow=14 flutter=3 drift=2 tone=5000 sweep=0.7 seed=11'],
             'score': line(muff, total)},
            {'name': 'kit', 'patch': 'lofi-kit', 'gain': '-5dB', 'fx': ['crush bits=12 rate=26kHz mix=0.5'], 'score': line(kit, total)},
            {'name': 'sax', 'patch': 'tenor-sax', 'gain': '-6dB', 'pan': 0.2, 'score': line(sax, total)},
            {'name': 'sub', 'patch': 'sub-saturated', 'gain': '-8dB', 'score': line(sub, total)},
            {'name': 'crackle', 'patch': 'fx-crackle', 'gain': '-8dB', 'score': f"C4/{total - 0.2:.4f}b@85 R/0.2b"},
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
