#!/usr/bin/env python3
"""chirpers5-t3 (chirper-one): REESE-LED, DARK TO LIGHT, "Ring Road Sunrise", for 'Soft Concrete' (Chirpers V).

Liquid drum & bass at 174 bpm that starts in the dark and drives into the light: the ring road at 5 a.m.
(v4 re-styled: it had been a second euphoric piano anthem, too close to chirper-zero's closer Streetlights Off.)
- THE DARK: G minor. A REESE carries the verses as the lead - a moody, gliding line in the mid-range (overlapping
  notes slide), its filter breathing on an eight-bar LFO - over a sub, a low pad and the amen roll. No piano, no voice.
- THE LIGHT: each drop turns to the relative major: a concert grand arrives for the first time with house stabs on
  Ebmaj9 - Bbmaj7 - Fadd9 - Gm9 (IV - I - V - vi of Bb), and the reese steps down to be the bass. The piano is the
  sunrise; the reese is the road.
- THE MEETING: the break puts the reese's line over the piano's held major chords - the dark tune in the light key.
- THE DAWN BREAKS (v5): the last beat before each drop is caught and replayed rising (a stutter with a pitch ramp),
  the dark winding itself up into the light.
- THE HANDOVER: the outro ends on a held Ebmaj9 with a low G under it, ringing into Hairline's Gm9 (chirper-zero's
  t4), and the render tail is short.
- The amen rolls straight (no garage skip - that is Last Night Bus) with a crash every phrase and a machine-kit kick
  under the amen's own kicks; the break's last bars ride wM's endless Shepard rise under a snare roll.
Form: intro 16 (the dark, filtered) / verse 16 / build 8 / drop 32 (the light) / break 16 / verse2 8 / drop2 32 /
outro 16.
Levels on the album standard (-12.5 LUFS +-1.5, true peak <= -1 dBTP, no pinned runs): master glue, +8 dB into a fast
10:1 compressor, 15 kHz low-pass, low-knee soft clip, -1 dB ceiling, volume 0 dB, true_peak on.
Emits songs/chirpers5-t3.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers5-t3.yaml")
BPM = 174
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('verse', 16), ('build', 8), ('drop', 32), ('break', 16), ('verse2', 8), ('drop2', 32), ('outro', 16)]
DROPS = ('drop', 'drop2')
DARK = ('intro', 'verse', 'build', 'verse2')
# the dark: G minor roots under the reese (Gm, Ebmaj7, Cm, D), two bars each
DARK_ROOTS = [(31, [55, 58, 62]), (27, [55, 58, 63]), (24, [55, 60, 63]), (26, [54, 57, 62])]
# the light: Ebmaj9, Bbmaj7, Fadd9, Gm9 - two bars each
LIGHT = [(27, [55, 58, 62, 65, 70]), (34, [57, 58, 62, 65, 69]), (29, [57, 60, 65, 67, 69]), (31, [57, 58, 62, 65, 69])]
ROLL = [[0, 3, 4, 6, 10, 9, 7, 14], [0, 3, 4, 6, 13, 9, 15, 22]]
# THE REESE LINE (eight bars, beat, MIDI, length): low, brooding, gliding (overlaps slide)
LINE = [(0.0, 55, 3.2), (3.0, 58, 1.2), (4.0, 57, 2.2), (6.0, 55, 2.2), (8.0, 51, 3.2), (11.0, 53, 1.2), (12.0, 55, 4.0),
        (16.0, 60, 3.2), (19.0, 58, 1.2), (20.0, 57, 2.2), (22.0, 55, 2.2), (24.0, 54, 3.2), (27.0, 57, 1.2), (28.0, 55, 4.0)]

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

def legato(events, total):
    """the reese lead: notes may overlap (the overlap is the glide), so write them as explicit notes"""
    return [{'at': f'{at * SPB:.4f}s', 'len': f'{d * SPB:.4f}s', 'pitch': m, 'vel': round(v / 127, 3)} for at, m, d, v in events]

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 't': t}); t += 4.0
    total = t
    amen, piano, pad, sub, bass, lead, shep, crash, kick = [], [], [], [], [], [], [], [], []
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        light = s in DROPS or s == 'break' or (s == 'outro')
        root, ch = (LIGHT if light else DARK_ROOTS)[(k // 2) % 4]
        first = (k % 2 == 0)
        rolling = s in DROPS or s in ('verse', 'verse2') or (s == 'intro' and i >= 8) or (s == 'outro' and i < 8)
        if rolling:
            if s in DROPS:
                kick.append((t0, 'k', 0.25, 118)); kick.append((t0 + 2.5, 'k', 0.25, 108))
            for e, sl in enumerate(ROLL[k % 2]):
                v = (112 if sl in (0, 9, 13, 4, 7, 15, 22) else 82) - (10 if s in DARK else 0)
                amen.append((t0 + e * 0.5 + (0.03 if e % 2 else 0.0), nm(36 + sl), 0.5, v))
            if s in DROPS and i % 8 == 0:
                crash.append((t0, 'c', 3.5, 100))
        if s == 'build' or (s == 'break' and i >= 12):
            j = i if s == 'build' else i - 8
            st = 1.0 if j < 4 else (0.5 if j < 6 else 0.25)
            x = 0.0
            while x < 4.0 - 1e-6:
                amen.append((t0 + x, nm(36 + 4), min(0.5, st), 70 + 4 * j))
                x += st
        # THE LIGHT: the piano exists only in the light - stabs in the drops, held chords in the break and outro
        if s in DROPS:
            for q, d in ((0.0, 1.2), (1.5, 1.0), (3.0, 0.9)):
                piano.append((t0 + q, ','.join(nm(m) for m in [root + 24] + ch), d, 96))
        elif light and first:
            for j, m in enumerate(ch):
                piano.append((t0 + 0.04 * j, nm(m), 7.6 - 0.04 * j, 76))
        # the dark pad: the low minor chords under the verses
        if s in DARK and first:
            pad.append((t0, ','.join(nm(m - 12) for m in ch), 7.8, 72))
        # sub everywhere the floor is: the root
        if s in DROPS or s in ('verse', 'verse2', 'build'):
            sub.append((t0, nm(root + (12 if root < 28 else 0)), 3.6, 100))
        # THE REESE: the lead in the dark (and in the break), the bass in the drops
        if (s in ('intro', 'verse', 'verse2') and (s != 'intro' or i >= 8)) or s == 'break':
            if k % 8 == 0 or (s == 'verse2' and i == 0) or (s == 'intro' and i == 8) or (s == 'break' and i % 8 == 0):
                for at, m, d in LINE:
                    if t0 + at < total:
                        lead.append((t0 + at, 53 if (m == 54 and light) else m, d, 96 if s != 'intro' else 80))   # in the light the F# becomes F
        if s in DROPS:
            for q in (0.0, 1.5, 3.0):
                bass.append((t0 + q, nm(root + 12), 1.2, 90))
        if s == 'break' and i == 8:
            shep.append((t0, 'C4', 31.9, 88))
    # THE HANDOVER: the last two bars hold Ebmaj9 over a low G - into Hairline's Gm9
    tl = total - 8.0
    piano.append((tl, ','.join(nm(m) for m in [43, 55, 58, 62, 65, 70]), 7.9, 84))
    pad.append((total - 16.0, ','.join(nm(m) for m in [43, 55, 58, 62, 67]), 16.0, 96))   # the pad holds it to the last sample
    end_s = total * SPB
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'] * SPB)
    lv = {'intro': -8, 'verse': -3, 'build': -4, 'drop': 0, 'break': -5, 'verse2': -3, 'drop2': 0, 'outro': -6}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.3):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    op = [['0s', 1], [f"{secs['verse'] - 0.05:.3f}s", 0.4], [f"{secs['verse']:.3f}s", 0]]
    # (v5) THE DAWN BREAKS: the last beat before each drop is caught in a buffer and replayed rising (wM's stutter
    # pitch ramp, +3 semitones a repeat, sixteenths) - the dark winds itself up into the light
    wind = [['0s', 0]]
    for tg in (secs['drop'], secs['drop2']):
        a0 = tg - SPB
        wind += [[f'{a0 - 0.01:.3f}s', 0], [f'{a0:.3f}s', 1], [f'{tg - 0.01:.3f}s', 1], [f'{tg:.3f}s', 0]]
    return {
        'about': "Chirpers - Soft Concrete (Chirpers V), track 3 by chirper-one: REESE-LED, DARK TO LIGHT, Ring Road Sunrise. "
                 "Generated by compose/chirpers5/src/chirpers5-t3.py; see its docstring and compose/chirpers5/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 1.2:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'true_peak': True,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1', 'hp cutoff=250'], 'returns': []}},
        'master': {'fx': [{'type': 'filter', 'kind': 'lp', 'q': 0.7, 'cutoff': {'value': 18000, 'mod': [{'src': 'auto.op', 'amount': -4.9}]}},
                          {'type': 'eq', 'bands': ['highpass cutoff=28', 'lowshelf cutoff=160 gain=4dB', 'peak cutoff=1100 q=0.9 gain=-4dB', 'highshelf cutoff=8000 gain=-2dB']},
                          {'type': 'compressor', 'threshold': '-22dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'gain', 'gain': '+9.5dB'},
                          {'type': 'compressor', 'threshold': '-5dB', 'ratio': 10, 'attack': '0.3ms', 'release': '60ms', 'makeup': '0dB'},
                          {'type': 'stutter', 'slice': '1/16', 'repeats': 4, 'pitch': 3, 'chance': 1,
                           'mix': {'value': 0, 'mod': [{'src': 'auto.wind', 'amount': 1}]}},
                          'lp cutoff=15000',
                          {'type': 'clip', 'drive': '0dB', 'ceiling': '-1.8dB', 'knee': 0.55, 'link': True}],
                   'auto': {'dyn': {'points': dyn}, 'op': {'points': op}, 'wind': {'points': wind}}},
        'tracks': [
            {'name': 'amen', 'patch': 'amen-chops', 'gain': '-7dB',
             'fx': [{'type': 'compressor', 'threshold': '-20dB', 'ratio': 6, 'attack': '0.5ms', 'release': '50ms', 'makeup': '6dB'}],
             'score': line(amen, total)},
            {'name': 'kick', 'patch': 'machine-kit', 'gain': '-6dB', 'score': line(kick, total)},
            {'name': 'crash', 'patch': 'break-kit', 'gain': '-14dB', 'score': line(crash, total)},
            {'name': 'sub', 'patch': 'sub', 'gain': '+1dB', 'fx': [{'type': 'pump', 'on': 'amen', 'depth': '-4dB', 'release': '230ms', 'curve': 0.6}],
             'score': line(sub, total)},
            # THE REESE LEAD: overlapping notes glide; its low-pass breathes on an eight-bar LFO
            {'name': 'lead', 'patch': 'reese', 'gain': '-9dB', 'sends': {'hall': '-14dB'}, 'lfo': {'breath': 'sine rate=8/1 phase=0.75'},
             'fx': [{'type': 'filter', 'kind': 'lp', 'q': 1.2, 'cutoff': {'value': 1400, 'mod': [{'src': 'lfo.breath', 'amount': 1.0}]}},
                    {'type': 'pump', 'on': 'amen', 'depth': '-4dB', 'release': '230ms', 'curve': 0.6}],
             'notes': legato(lead, total)},
            {'name': 'bass', 'patch': 'reese', 'gain': '-7dB', 'fx': ['lp cutoff=900', {'type': 'pump', 'on': 'amen', 'depth': '-7dB', 'release': '230ms', 'curve': 0.6}],
             'score': line(bass, total)},
            {'name': 'pad', 'patch': 'juno-pad', 'gain': '-14dB', 'sends': {'hall': '-10dB'}, 'score': line(pad, total)},
            {'name': 'piano', 'patch': 'piano', 'gain': '-12dB', 'sends': {'hall': '-12dB'},
             'fx': [{'type': 'pump', 'on': 'amen', 'depth': '-4dB', 'release': '230ms', 'curve': 0.6}], 'score': line(piano, total)},
            {'name': 'shepard', 'patch': 'shepard-pad', 'gain': '-13dB', 'score': line(shep, total)},
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
