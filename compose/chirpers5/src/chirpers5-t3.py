#!/usr/bin/env python3
"""chirpers5-t3 (chirper-one): EUPHORIC ANTHEM, "Ring Road Sunrise", for 'Soft Concrete' (Chirpers V).

Piano-led, hands-in-the-air liquid drum & bass at 174 bpm in A major: the night's last tune as the sky goes pale
over the ring road. The euphoria half of the album's euphoria-and-melancholy.
- THE PIANO: a concert grand plays house-piano stabs (the one, the and-of-2, the four) on Dmaj9 - E6 - C#m7 - F#m9
  (IV - V - iii - vi), two bars each: lift, lift, ache, home-that-isn't.
- THE ROLL: wM's amen-chops in a straight roll (no garage skip - that is Last Night Bus), a crash on every
  phrase, the sub and a low reese pumping against it.
- THE VOICE: a soaring wordless "ah" line, four bars, on the chord tones, into a long hall; in the second drop
  strings double it an octave down.
- THE SUNRISE: the break ends on wM's endless Shepard rise (shepard-pad) under a snare roll, so the climb into the
  last drop never seems to arrive - until it does.
Form: intro 16 (piano alone, opening up) / build 8 / drop 32 / break 24 (piano, strings, voice; the endless rise in
its last 8) / drop2 32 / outro 16.
Levels (the album standard, -12.5 LUFS +-1.5, true peak <= -1 dBTP, no pinned runs): drums compressed on their
track; master glue, +12 dB into a fast 10:1 compressor, a 15 kHz low-pass, then a soft-knee clip (chirper-zero's
ending) under a -1 dB ceiling, song volume 0 dB.
Emits songs/chirpers5-t3.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers5-t3.yaml")
BPM = 174
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('build', 8), ('drop', 32), ('break', 24), ('drop2', 32), ('outro', 16)]
DROPS = ('drop', 'drop2')
# (root, voicing): Dmaj9, E6, C#m7, F#m9
CHORDS = [(26, [57, 61, 64, 66, 69]), (28, [56, 61, 64, 68, 71]), (25, [56, 59, 64, 68]), (30, [57, 61, 64, 68, 69])]
ROLL = [[0, 3, 4, 6, 10, 9, 7, 14], [0, 3, 4, 6, 13, 9, 15, 22]]
# the voice: (beat within the 4-bar phrase, MIDI, length)
MELODY = [(0.0, 76, 2.5), (3.0, 78, 1.0), (4.0, 76, 3.0), (7.0, 73, 1.0), (8.0, 73, 2.5), (11.0, 71, 1.0), (12.0, 73, 3.5)]

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
    amen, piano, strings, sub, reese, voice, shep, crash, kick = [], [], [], [], [], [], [], [], []
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        root, ch = CHORDS[(k // 2) % 4]
        # (v2) THE LIFT: the last sixteen bars of the second drop (and the outro) go up a semitone - the anthem's
        # truck-driver key change, A major to Bb major, every pitched part together
        up = 0   # (v3) the lift is withdrawn: a last-drop semitone rise is Streetlights Off's (chirper-zero's closer)
        root, ch = root + up, [m + up for m in ch]
        first = (k % 2 == 0)
        if s in DROPS or (s == 'outro' and i < 8):
            # (v2) a punchy kick under the amen's own kicks (the one and the and-of-3): the anthem's chest
            kick.append((t0, 'k', 0.25, 118))
            kick.append((t0 + 2.5 + 0.03, 'k', 0.25, 108))
            for e, sl in enumerate(ROLL[k % 2]):
                v = 112 if sl in (0, 9, 13, 4, 7, 15, 22) else 82
                amen.append((t0 + e * 0.5 + (0.03 if e % 2 else 0.0), nm(36 + sl), 0.5, v))
            if i % 8 == 0:
                crash.append((t0, 'C4', 3.5, 100))
        if s == 'build':
            st = 1.0 if i < 4 else (0.5 if i < 6 else 0.25)
            x = 0.0
            while x < 4.0 - 1e-6:
                amen.append((t0 + x, nm(36 + 4), min(0.5, st), 70 + 5 * i))
                x += st
        if s == 'break' and i >= 20:
            st = 0.5 if i < 22 else 0.25
            x = 0.0
            while x < 4.0 - 1e-6:
                amen.append((t0 + x, nm(36 + 4), min(0.5, st), 72 + 6 * (i - 20)))
                x += st
        # THE PIANO: house stabs on the one, the and-of-2 and the four
        vel = {'intro': 70 + i, 'build': 88, 'break': 74, 'outro': 72}.get(s, 96)
        if s in DROPS or s == 'build':
            for q, d in ((0.0, 1.2), (1.5, 1.0), (3.0, 0.9)):
                piano.append((t0 + q, ','.join(nm(m) for m in [root + 24, root + 36] + ch), d, vel))   # (v2) the left hand's octave
        elif first:
            # outside the drops the piano holds each chord, rolled, so the stabs are the drop's reward
            for j, m in enumerate(ch):
                piano.append((t0 + 0.04 * j, nm(m), 7.6 - 0.04 * j, vel))
        if s in ('break', 'drop2') and first:
            strings.append((t0, ','.join(nm(m) for m in ch[:3]), 7.8, 74 if s == 'break' else 64))
        if s in DROPS or s == 'build':
            if first:
                sub.append((t0, nm(root + (12 if root < 28 else 0)), 3.4, 100))
            else:
                sub.append((t0 + 1.5, nm(root + (12 if root < 28 else 0)), 2.3, 96))
        if s in DROPS:
            for q in (0.0, 1.5, 3.0):
                reese.append((t0 + q, nm(root + 12), 1.2, 86 if s == 'drop' else 94))
        # the voice: the four-bar phrase over every other phrase in the drops, every phrase in the break
        ph = (k % 4 == 0)
        if ph and ((s in DROPS and (k // 4) % 2 == 0) or s == 'break' or (s == 'intro' and i >= 8)):
            for at, m, ln in MELODY:
                voice.append((t0 + at, nm(m + up), ln, 94 if s != 'intro' else 76))
                if s == 'drop2':
                    strings.append((t0 + at, nm(m + up - 12), ln, 70))
        if s == 'break' and i == 16:
            shep.append((t0, 'C4', 31.9, 90))
    end_s = total * SPB
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'] * SPB)
    lv = {'intro': -7, 'build': -4, 'drop': 0, 'break': -5, 'drop2': 0, 'outro': -6}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.3):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    dyn.append([f'{end_s:.3f}s', -14])
    # the intro opens up: a low-pass over the whole mix from 600 Hz to open across the intro and build
    op = [['0s', 1], [f"{secs['build']:.3f}s", 0.45], [f"{secs['drop'] - 0.05:.3f}s", 0.15], [f"{secs['drop']:.3f}s", 0]]
    return {
        'about': "Chirpers - Soft Concrete (Chirpers V), track 3 by chirper-one: EUPHORIC ANTHEM, Ring Road Sunrise. Generated by "
                 "compose/chirpers5/src/chirpers5-t3.py; see its docstring and compose/chirpers5/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'true_peak': True,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.6s mix=1', 'hp cutoff=250'], 'returns': []}},
        'master': {'fx': [{'type': 'filter', 'kind': 'lp', 'q': 0.7, 'cutoff': {'value': 18000, 'mod': [{'src': 'auto.op', 'amount': -4.9}]}},
                          {'type': 'eq', 'bands': ['highpass cutoff=28', 'lowshelf cutoff=160 gain=4dB', 'peak cutoff=1100 q=0.9 gain=-5dB', 'highshelf cutoff=8000 gain=-2dB']},
                          {'type': 'compressor', 'threshold': '-22dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'gain', 'gain': '+8dB'},
                          {'type': 'compressor', 'threshold': '-5dB', 'ratio': 10, 'attack': '0.3ms', 'release': '60ms', 'makeup': '0dB'},
                          'lp cutoff=15000',
                          {'type': 'clip', 'drive': '0dB', 'ceiling': '-1.5dB', 'knee': 0.8, 'link': True}],
                   'auto': {'dyn': {'points': dyn}, 'op': {'points': op}}},
        'tracks': [
            {'name': 'amen', 'patch': 'amen-chops', 'gain': '-7dB',
             'fx': [{'type': 'compressor', 'threshold': '-20dB', 'ratio': 6, 'attack': '0.5ms', 'release': '50ms', 'makeup': '6dB'}],
             'score': line(amen, total)},
            {'name': 'kick', 'patch': 'machine-kit', 'gain': '-6dB', 'score': line(kick, total)},
            {'name': 'crash', 'patch': {'extends': 'break-kit'}, 'gain': '-14dB', 'score': line([(a, 'c', d, v) for a, _, d, v in crash], total)},
            {'name': 'sub', 'patch': 'sub', 'gain': '+1dB', 'fx': [{'type': 'pump', 'on': 'amen', 'depth': '-4dB', 'release': '230ms', 'curve': 0.6}],
             'score': line(sub, total)},
            {'name': 'reese', 'patch': 'reese', 'gain': '-7dB', 'fx': ['lp cutoff=900', {'type': 'pump', 'on': 'amen', 'depth': '-7dB', 'release': '230ms', 'curve': 0.6}],
             'score': line(reese, total)},
            {'name': 'piano', 'patch': 'piano', 'gain': '-12dB', 'sends': {'hall': '-12dB'},
             'fx': [{'type': 'pump', 'on': 'amen', 'depth': '-4dB', 'release': '230ms', 'curve': 0.6}], 'score': line(piano, total)},
            {'name': 'strings', 'patch': 'strings-saw', 'gain': '-13dB', 'sends': {'hall': '-6dB'}, 'score': line(strings, total)},
            {'name': 'voice', 'patch': 'voice', 'gain': '-11dB', 'sends': {'hall': '-6dB'}, 'score': line(voice, total)},
            {'name': 'shepard', 'patch': 'shepard-pad', 'gain': '-12dB', 'score': line(shep, total)},
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
