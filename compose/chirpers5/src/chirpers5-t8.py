#!/usr/bin/env python3
"""chirpers5-t8 (chirper-one): JUNGLE-TINGED LIQUID, "Wet Brick", for 'Soft Concrete' (Chirpers V).

Liquid with jungle in its bones, 170 bpm, F minor: the amen played as a whole break and then edited live, the way a
jungle producer works an MPC - over a deep, dubby liquid bed.
- THE BREAK: wM's amen-chops played in its own order (the whole four-bar amen, slice after slice) - and on the
  fourth bar of every phrase EDITED: slices reversed (^rev), re-pitched up and down (^tune), the snare doubled, the
  last beat stuttered into a roll. The edits grow through the track.
- THE BOOM: an 808 sub with long notes that GLIDE between roots (overlapping notes slide), jungle's rolling
  low end under liquid chords.
- THE BED: a juno pad on Fm9 - Dbmaj7 - Ebsus2 - Cm7, four bars each (slow, dubby), with a dotted-quarter echo on a
  Rhodes stab answering every chord.
- THE VOICE: a low wordless "ooh" (formants down) in the break, the only melody, into a long hall.
- (v3, Harry's Soft Concrete notes) the boom gains weight (phantom harmonics, drive, harder pump) and the mix is darker
  (the top eased 1.5 dB, a 12 kHz low-pass).
Form: intro 16 / drop 32 / break 16 (bed, voice, the boom alone) / drop2 32 (heavier edits; its first sixteen bars
DRY - no pad, the break and the boom alone - v2) / outro 16.
Levels on the album standard (-12.5 LUFS +-1.5, true peak <= -1 dBTP, no pinned runs): drums compressed on their
track; master glue, +9 dB into a fast 10:1 compressor (+1.5 makeup), a 13.5 kHz low-pass, then a SOFT clip (ceiling
-2.3 dB, knee 0.55 - the low knee rounds early, so no corners and no inter-sample overs), -1 dB ceiling, volume 0 dB:
-13.3 LUFS, true peak -1.2 dBTP, longest pinned run 1.
Emits songs/chirpers5-t8.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers5-t8.yaml")
BPM = 170
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('drop', 32), ('break', 16), ('drop2', 32), ('outro', 16)]
DROPS = ('drop', 'drop2')
# (root, pad voicing): Fm9, Dbmaj7, Ebsus2, Cm7 - four bars each
CHORDS = [(29, [56, 60, 63, 67]), (25, [53, 56, 60, 65]), (27, [51, 55, 58, 65]), (24, [51, 55, 58, 63])]

def line(events, total):
    ev = sorted(events)
    toks, t = [], 0.0
    for k, (at, p, d, v) in enumerate(ev):
        if at < t - 1e-6: continue
        if at > t + 1e-4: toks.append(f"R/{at - t:.4f}b")
        nxt = ev[k + 1][0] if k + 1 < len(ev) else total
        d = max(0.02, min(d, nxt - at))
        base, _, attr = p.partition('^')
        toks.append(f"{base}/{d:.4f}b@{v}" + (f"^{attr}" if attr else "")); t = at + d
    if total > t + 1e-4: toks.append(f"R/{total - t:.4f}b")
    return ' '.join(toks)

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 't': t}); t += 4.0
    total = t
    amen, pad, keys, boom, voice = [], [], [], [], []
    edit_bars = []
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        root, ch = CHORDS[(k // 4) % 4]
        drums = s in DROPS or (s == 'intro' and i >= 8) or (s == 'outro' and i < 8)
        if drums:
            bar_in_break = k % 4               # which bar of the four-bar amen
            heavy = s == 'drop2'
            edit = (bar_in_break == 3) or (heavy and bar_in_break == 1 and i % 8 >= 4)
            for e in range(8):
                sl = bar_in_break * 8 + e
                at = t0 + e * 0.5
                attr = ''
                if edit:
                    # THE EDIT: reverse the odd slices, re-pitch the snares, double the last snare into sixteenths
                    if e % 2 == 1:
                        attr = '^rev=1'
                    if e in (2, 6):
                        attr = f"^tune={5 if heavy else 3}"
                    if e == 7:
                        amen.append((at, nm(36 + 4) + '^tune=7', 0.25, 96))
                        amen.append((at + 0.25, nm(36 + 4) + '^tune=12', 0.25, 104))
                        if heavy:
                            edit_bars.append(t0)
                        continue
                amen.append((at, nm(36 + sl) + attr, 0.5, 108 if e in (0, 2, 4, 6) else 88))
        # the bed: the pad holds each chord four bars
        # (v2) the second drop starts DRY - no pad for its first sixteen bars, the break and the boom alone, jungle
        # bare - and the bed returns for its second half
        if k % 4 == 0 and not (s == 'drop2' and i < 16):
            pad.append((t0, ','.join(nm(m) for m in ch), 15.8, 78 if s != 'break' else 86))
        # the Rhodes answers each chord on the and-of-2 of its first bar, into the dotted-quarter echo
        if k % 4 == 0 and s != 'intro':
            keys.append((t0 + 1.5, ','.join(nm(m + 12) for m in ch[1:]), 0.6, 84))
        # THE BOOM: long gliding sub - root for three bars, then a slide up an octave and back into the next root
        if s in DROPS or s == 'break':
            if k % 4 == 0:
                boom.append((t0, nm(root), 10.5, 104))
            if k % 4 == 2:
                boom.append((t0 + 2.5, nm(root + 12), 2.0, 96))       # overlapping notes slide
                boom.append((t0 + 4.4, nm(root + 7), 1.6, 92))
        if s == 'break' and k % 4 == 0:
            voice.append((t0, nm(ch[-1]) + '^u', 7.5, 88))
            voice.append((t0 + 8.0, nm(ch[-2]) + '^u', 7.5, 84))
    end_s = total * SPB
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'] * SPB)
    lv = {'intro': -7, 'drop': 0, 'break': -5, 'drop2': 0, 'outro': -6}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.3):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    dyn.append([f'{end_s:.3f}s', -14])
    op = [['0s', 1], [f"{secs['intro'] + 8 * 4 * SPB:.3f}s", 0.6], [f"{secs['drop'] - 0.05:.3f}s", 0.2], [f"{secs['drop']:.3f}s", 0]]
    gl = [['0s', 0]]
    for t_ in edit_bars:
        a0 = (t_ + 3.0) * SPB
        gl += [[f'{a0 - 0.01:.3f}s', 0], [f'{a0:.3f}s', 1], [f'{(t_ + 4.0) * SPB - 0.01:.3f}s', 1], [f'{(t_ + 4.0) * SPB:.3f}s', 0]]
    return {
        'about': "Chirpers - Soft Concrete (Chirpers V), track 8 by chirper-one: JUNGLE-TINGED LIQUID, Wet Brick. Generated by "
                 "compose/chirpers5/src/chirpers5-t8.py; see its docstring and compose/chirpers5/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2:.2f}s', 'ceiling': '-1dB', 'volume': '0dB',
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.8s mix=1', 'hp cutoff=250'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/8', 'feedback': 0.45, 'mix': 1}, 'lp cutoff=2500', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'filter', 'kind': 'lp', 'q': 0.7, 'cutoff': {'value': 18000, 'mod': [{'src': 'auto.op', 'amount': -4.5}]}},
                          {'type': 'eq', 'bands': ['highpass cutoff=28', 'peak cutoff=120 q=0.8 gain=2dB', 'peak cutoff=1100 q=0.9 gain=-3dB', 'highshelf cutoff=7000 gain=-3.5dB']},
                          {'type': 'compressor', 'threshold': '-22dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'gain', 'gain': '+9dB'},
                          {'type': 'compressor', 'threshold': '-5dB', 'ratio': 10, 'attack': '0.3ms', 'release': '60ms', 'makeup': '1.5dB'},
                          'lp cutoff=12000',
                          {'type': 'clip', 'drive': '0dB', 'ceiling': '-2.3dB', 'knee': 0.55, 'link': True}],
                   'auto': {'dyn': {'points': dyn}, 'op': {'points': op}}},
        'tracks': [
            {'name': 'amen', 'patch': 'amen-chops', 'gain': '-7dB',
             'fx': [{'type': 'compressor', 'threshold': '-20dB', 'ratio': 6, 'attack': '0.5ms', 'release': '50ms', 'makeup': '6dB'},
                    {'type': 'stutter', 'slice': '1/16', 'repeats': 4, 'roll': 0.5, 'floor': '1/64', 'chance': 1,
                     'mix': {'value': 0, 'mod': [{'src': 'auto.gl', 'amount': 1}]}}],
             'auto': {'gl': {'points': gl}}, 'score': line(amen, total)},
            # (v3) the boom gains weight that reads on small speakers: wM's phantom harmonics above 90 Hz and a little drive,
            # pumped harder by the break
            {'name': 'boom', 'patch': '808', 'gain': '-4dB', 'fx': [{'type': 'phantom', 'cutoff': 90, 'harmonics': '-10dB', 'odd': 0.4},
                                                                {'type': 'drive', 'drive': 0.2, 'mix': 0.3},
                                                                {'type': 'pump', 'on': 'amen', 'depth': '-5dB', 'release': '230ms', 'curve': 0.6}],
             'score': line(boom, total)},
            {'name': 'pad', 'patch': 'juno-pad', 'gain': '-12dB', 'sends': {'hall': '-10dB'},
             'fx': [{'type': 'pump', 'on': 'amen', 'depth': '-5dB', 'release': '230ms', 'curve': 0.6}], 'score': line(pad, total)},
            {'name': 'keys', 'patch': {'extends': 'epiano-tine', 'play': {'release': {'patch': 'epiano-damper', 'decay': '2s'}}},
             'gain': '-11dB', 'sends': {'echo': '-6dB'}, 'score': line(keys, total)},
            {'name': 'voice', 'patch': 'voice', 'gain': '-10dB', 'sends': {'hall': '-5dB'},
             'fx': [{'type': 'pitch', 'semitones': 0, 'formant': -3}], 'score': line(voice, total)},
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
