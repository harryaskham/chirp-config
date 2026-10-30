#!/usr/bin/env python3
"""chirpers6-t7 (chirper-one): MATH-ROCK INTERPLAY, "Floor 31", for 'All the Lights Left On' (Chirpers VI).

An office tower at night with every light left on, in odd meters, 132 bpm (the beat a quarter note), D minor /
F major: the building's machinery as music. Interlocking clean guitars that disagree about where the bar is, a
lift that keeps announcing floors, a clock, a cleaner's long shift - and at the top, the roof and the city.
Nothing loops: THE FIGURE (a seven-note tapping line, D-F-A-C-A-F-E) is re-cut by every meter it passes through.
I.   LOBBY (5/4, 16 bars): a clock ticks; the lift chimes (two celesta notes) and its voice speaks ("going up. floor
     thirty one."); the first guitar taps THE FIGURE in 5/4 (it doesn't fit - seven notes against ten eighths).
II.  INTERLOCK (7/8, 64 bars): a second guitar enters in 4/4 phrases against the first's 7/8 - the two realign only
     every seven bars; bass and a drummer accenting the 2+2+3; the lift voice calls floors between phrases.
III. STAIRWELL (6/8, 32 bars, quiet): the drums leave; celesta and a cello play THE FIGURE slowed into compound time,
     the clock ticking under it; "doors closing."
IV.  ATRIUM (5/4, 32 bars): the lobby again, changed - both guitars, the bass, a soft ride, the celesta answering;
     the lift goes up again.
V.   MACHINE (7/8 -> 4/4, 64 bars): two chug rigs take the interlock riff in 7/8, the full kit, a fuzz bass; the last
     sixteen bars square into 4/4 and the tremolo guitars and strings lift it - the building's machinery at full load.
VI.  ROOF (4/4, 36 bars): the climb resolves to F major on the roof - the drums for 24 bars, then only wind, the guitars ringing open chords, THE FIGURE
     once more on the e-bow, slow; the lift's last word, far below: "ground floor."
(v3) The office at night: a photocopier's scan sweeps every 7/8 bar of the machine's drums-and-bass opening (and the
atrium's second half); a phone rings, unanswered, three times in the stairwell.
Levels: dynamic (album rms -21..-11, crest 9..18): light glue, soft clip under a -1 dB ceiling, true_peak on.
Emits songs/chirpers6-t7.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers6-t7.yaml")
BPM = 132
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

# (section, bars, beats per bar)
FORM = [('lobby', 16, 5.0), ('interlock', 64, 3.5), ('stair', 32, 3.0), ('atrium', 32, 5.0), ('machine', 64, 3.5), ('roof', 36, 4.0)]
FIGURE = [62, 65, 69, 72, 69, 65, 64]            # D F A C A F E
# chords per bar: Dm9, Bbmaj7, Fmaj7, Am7 (the roof resolves to F major)
CH = [(38, [62, 65, 69, 72]), (34, [62, 65, 69, 70]), (41, [60, 64, 65, 69]), (45, [60, 64, 67, 69])]
ROOF = [(41, [60, 65, 69, 72]), (34, [62, 65, 70, 74]), (36, [60, 64, 67, 72]), (41, [60, 65, 69, 77])]

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

def say(words, t0, pitch=57):
    out, t = [], t0
    for ph in words:
        out.append((t, f"{nm(pitch)}^ph={ph}", 0.55, 88)); t += 0.6
    return out

GOING_UP = ['g-ow1', 'ih0-ng', 'ah1-p', None, 'f-l-ao1-r', 'th-er1', 't-iy0', 'w-ah1-n']
DOORS = ['d-ao1-r-z', 'k-l-ow1', 'z-ih0-ng']
FLOORS = [['f-l-ao1-r', 'n-ay1-n'], ['f-l-ao1-r', 's-eh1-v', 'ah0-n', 't-iy1', 'n-ay1-n'], ['f-l-ao1-r', 'f-ih1-f', 't-iy1', 'n-ay1-n']]
GROUND = ['g-r-aw1-n-d', 'f-l-ao1-r']

def build():
    bars, t = [], 0.0
    for name, n, bl in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 'n': n, 't': t, 'bl': bl}); t += bl
    total = t
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'])
    T = {k: [] for k in ('clock', 'chime', 'lift', 'gtr1', 'gtr2', 'bass', 'kit', 'celesta', 'cello', 'chugl', 'chugr',
                         'fuzz', 'trem', 'strings', 'ebow', 'wind', 'sub', 'ring', 'copier', 'phone')}
    g2 = 0.0     # the second guitar's own 4/4 clock (it ignores the bar lines)
    for k, b in enumerate(bars):
        s, t0, i, bl = b['sec'], b['t'], b['i'], b['bl']
        root, ch = (ROOF if s == 'roof' else CH)[k % 4]
        eighths = int(round(bl * 2))
        # the clock: a tick every beat in the lobby and the stairwell
        if s in ('lobby', 'stair', 'atrium'):
            x = 0.0
            while x < bl - 1e-6:
                T['clock'].append((t0 + x, 'C6', 0.1, 70 if x == 0 else 54)); x += 1.0
        # THE FIGURE on guitar 1: tapped eighths, the seven notes re-cut by each bar's length
        # (the interlock's second half hands THE FIGURE to the celesta; the machine's first sixteen bars are drums and bass)
        if s in ('lobby', 'interlock', 'atrium', 'machine') and not (s == 'lobby' and i < 4) \
                and not (s == 'interlock' and 32 <= i < 48) and not (s == 'machine' and i < 16):
            for e in range(eighths):
                T['gtr1'].append((t0 + e * 0.5, nm(FIGURE[(k * eighths + e) % 7] + (0 if s != 'machine' else 12)), 0.45,
                                  86 if e == 0 else 72))
        # guitar 2: its own 4/4 phrase of chord tones in eighths, ignoring the 7/8 bar lines
        if s in ('interlock', 'atrium', 'machine') and not (s == 'interlock' and i < 8):
            while g2 < t0 + bl - 1e-6:
                if g2 >= t0:
                    q = int(round(g2 * 2)) % 8
                    _, c2 = CH[int(g2 // 4) % 4]
                    T['gtr2'].append((g2, nm(c2[[0, 2, 1, 3, 2, 0, 3, 1][q]] - 12), 0.45, 80 if q == 0 else 66))
                g2 += 0.5
        else:
            g2 = t0 + bl
        # drums: the 2+2+3 of 7/8 (kick, snare, kick-kick-snare) in interlock and machine; the roof plays a big 4/4
        if s in ('interlock', 'machine') and not (s == 'interlock' and i < 4):
            hard = s == 'machine'
            for q, p, v in ((0.0, 'k', 108), (1.0, 's', 100), (2.0, 'k', 96), (2.5, 'k', 90), (3.0, 's', 104)):
                if s == 'machine' and i >= 48:
                    continue
                T['kit'].append((t0 + q, p, 0.25, v + (8 if hard else 0)))
            x = 0.0
            while x < bl - 1e-6 and not (s == 'machine' and i >= 48):
                # the interlock's second half moves the hats to the ride; the machine's first sixteen bars are drums alone
                cym = 'rde' if hard else ('rd' if (s == 'interlock' and i >= 32) else 'h')
                T['kit'].append((t0 + x, cym, 0.25, 62 if x % 1 else 74)); x += 0.5
        if s == 'machine' and i >= 48:                       # squared into 4/4: the machine at full load
            for q in range(int(bl)):
                T['kit'].append((t0 + q, 'k', 0.25, 118))
                if q % 2 == 1:
                    T['kit'].append((t0 + q, 's', 0.25, 118))
                T['kit'].append((t0 + q + 0.5, 'rde', 0.25, 92))
            x = 0.0
            while x < bl - 1e-6:
                T['trem'].append((t0 + x, nm(ch[int(x * 4) % 4] + 12), 0.125, 96)); x += 0.125
        if s in ('machine',) and i % 8 == 0:
            T['kit'].append((t0, 'c', 0.25, 116))
        if s == 'roof' and i < 24:
            T['kit'].append((t0, 'k', 0.25, 104)); T['kit'].append((t0 + 2.0, 's', 0.25, 100))
            T['kit'].append((t0, 'c' if i % 4 == 0 else 'rde', 0.25, 96 if i % 4 == 0 else 78))
            T['kit'].append((t0 + 3.0, 'ft', 0.25, 80 + i))
        # bass: the root on the one and the bar's long beat
        if s == 'atrium':
            # IV: the atrium - the lobby's 5/4 again, changed: both guitars, the bass, a soft ride, celesta answering
            T['kit'].append((t0, 'rd', 0.25, 66)); T['kit'].append((t0 + 2.5, 'rd', 0.25, 58))
            if i % 2 == 1:
                T['celesta'].append((t0 + 3.0, nm(ch[-1] + 12), 1.8, 64))
        if s in ('interlock', 'atrium', 'machine', 'roof'):
            T['bass'].append((t0, nm(root), min(1.8, bl / 2), 92))
            T['bass'].append((t0 + (2.0 if bl >= 3.5 else 1.5), nm(root + 7), bl - 2.0 if bl >= 3.5 else 1.4, 84))
            T['sub'].append((t0, nm(root - 12 if root >= 40 else root), bl - 0.1, 90 if s != 'interlock' else 76))
        if s == 'interlock' and 32 <= i < 48:
            for e in range(eighths):
                if e % 2 == 0:
                    T['celesta'].append((t0 + e * 0.5, nm(FIGURE[(k * eighths + e) % 7] + 12), 0.9, 74))
        # III: celesta and cello play THE FIGURE in 6/8 (dotted quarters and eighths)
        if s == 'stair':
            for e, q in enumerate((0.0, 1.0, 1.5, 2.0, 2.5)):
                T['celesta'].append((t0 + q, nm(FIGURE[(i * 5 + e) % 7] + 12), 0.9, 70))
            if i % 2 == 0:
                T['cello'].append((t0, nm(root - 12), 5.9, 72))
        # IV: the chug rigs take the interlock riff (root and fifth on the 2+2+3)
        if s == 'machine' and i >= 16:
            five = f"{nm(root)},{nm(root + 7)},{nm(root + 12)}"
            for q in ((0.0, 0.5, 2.0, 2.5, 3.0) if i < 48 else (0.0, 0.5, 1.5, 2.0, 3.0, 3.5)):
                if q < bl:
                    T['chugl'].append((t0 + q, five, 0.4, 110)); T['chugr'].append((t0 + q + 0.01, five, 0.4, 108))
            T['fuzz'].append((t0, nm(root - 12 if root >= 40 else root), bl - 0.1, 108))
            if i >= 48 and i % 2 == 0:
                T['strings'].append((t0, ','.join(nm(m) for m in ch[:3]), bl * 2 - 0.2, 92))
        # V: the roof - open ringing chords, THE FIGURE on the e-bow, wind
        if s == 'roof' and i < 28:
            T['ring'].append((t0, ','.join(nm(m) for m in [root + 12] + ch), 3.9, 84))
            if i % 2 == 0 and i < 32:
                for e in range(4):
                    T['ebow'].append((t0 + e * 2, nm(FIGURE[(i // 2 * 4 + e) % 7] + 12), 1.9, 84))
            if i % 2 == 0:
                T['strings'].append((t0, ','.join(nm(m) for m in ch[:3]), 7.8, 78))
    # the lift: chime and voice
    T['chime'] += [(2.0, 'E6', 1.5, 80), (2.6, 'C6', 2.0, 76)]
    T['lift'] += say([w for w in GOING_UP if w], 4.0)
    for j, fl in enumerate(FLOORS):
        a = secs['interlock'] + (j + 1) * 7 * 3.5 + 1.0
        T['chime'] += [(a - 1.5, 'E6', 1.2, 70), (a - 0.9, 'C6', 1.6, 66)]
        T['lift'] += say(fl, a)
    T['lift'] += say(DOORS, secs['stair'] + 4 * 3.0)
    T['chime'] += [(secs['atrium'] + 2.0, 'E6', 1.5, 66), (secs['atrium'] + 2.6, 'C6', 2.0, 62)]
    T['lift'] += say(['g-ow1', 'ih0-ng', 'ah1-p'], secs['atrium'] + 4.0)
    T['chime'] += [(secs['roof'] + 31 * 4.0, 'E6', 1.5, 60), (secs['roof'] + 31 * 4.0 + 0.6, 'C6', 2.0, 56)]
    T['lift'] += say(GROUND, secs['roof'] + 31 * 4.0 + 2.0, 55)
    # (v3) THE OFFICE AT NIGHT: a photocopier scanning in the machine's opening bars - its sweep on every 7/8 bar, the
    # building's machinery literally keeping the meter - and a phone ringing, unanswered, in the stairwell
    for b in bars:
        if (b['sec'] == 'machine' and b['i'] < 16) or (b['sec'] == 'atrium' and b['i'] >= 16):
            T['copier'].append((b['t'], 'C4', min(2.0, b['bl'] - 0.1), 74))
    for rep in range(3):
        a0 = secs['stair'] + 8 * 3.0 + rep * 6.0
        x = 0.0
        while x < 2.0 - 1e-6:
            T['phone'].append((a0 + x, 'E6' if int(x * 8) % 2 == 0 else 'C6', 0.12, 62)); x += 0.125
    T['wind'].append((secs['roof'], 'C4', total - secs['roof'], 80))
    lv = {'lobby': -6, 'interlock': -2, 'stair': -7, 'atrium': -4, 'machine': 0, 'roof': -1}
    dyn = []
    for name, _, _ in FORM:
        t_ = secs[name] * SPB
        dyn += [[f'{max(0.0, t_ - 0.4):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    dyn.append([f'{total * SPB:.3f}s', -10])
    lift_fx = ['hp cutoff=300', 'lp cutoff=4500', {'type': 'delay', 'time': '1/8', 'feedback': 0.15, 'mix': 0.15}]
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(T[name], total)}, **kw)
    return {
        'about': "Chirpers - All the Lights Left On (Chirpers VI), track 7 by chirper-one: MATH-ROCK INTERPLAY, Floor 31. "
                 "Generated by compose/chirpers6/src/chirpers6-t7.py; see its docstring and compose/chirpers6/styles.md.",
        'feel': {'drift': '5ms', 'drift_bars': 2},
        'tempo': BPM, 'length': f'{total * SPB + 3:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'true_peak': True,
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.5s mix=1', 'hp cutoff=200'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.4, 'mix': 1}, 'lp cutoff=3500', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=34', 'peak cutoff=45 q=1 gain=-4dB', 'peak cutoff=115 q=0.6 gain=5dB', 'peak cutoff=170 q=0.8 gain=3dB', 'peak cutoff=1900 q=0.8 gain=-2dB', 'peak cutoff=4200 q=0.8 gain=-3dB', 'highshelf cutoff=7000 gain=-3dB']},
                          {'type': 'compressor', 'threshold': '-20dB', 'ratio': 2, 'attack': '20ms', 'release': '200ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'gain', 'gain': '+6dB'},
                          'lp cutoff=13000',
                          {'type': 'clip', 'drive': '0dB', 'ceiling': '-2dB', 'knee': 0.55, 'link': True}],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            tr('clock', 'metal-kit', '-20dB', score=line([(a, 'clv', d, v) for a, _, d, v in T['clock']], total)),
            tr('chime', 'celesta', '-10dB', sends={'hall': '-8dB'}),
            tr('lift', 'voice-tts', '-6dB', fx=lift_fx, sends={'hall': '-12dB'}),
            tr('gtr1', 'clean-hp', '-10dB', pan=-0.35, sends={'echo': '-10dB', 'hall': '-12dB'}),
            tr('gtr2', 'clean-chorus', '-11dB', pan=0.35, sends={'hall': '-12dB'}),
            tr('bass', 'bass-pick-di', '-5dB'),
            tr('sub', 'sub', '-15dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-4dB', 'release': '300ms', 'curve': 0.6}]),
            tr('kit', 'metal-kit', '-6dB', sends={'hall': '-16dB'}),
            tr('celesta', 'celesta', '-10dB', sends={'hall': '-6dB'}),
            tr('cello', 'cello', '-8dB', sends={'hall': '-8dB'}),
            tr('chugl', 'm8-chug-l', '-10dB', pan=-0.9),
            tr('chugr', 'm8-chug-r', '-10dB', pan=0.9),
            tr('fuzz', 'bass-fuzz', '-9dB'),
            tr('trem', 'clean-chorus', '-12dB', pan=0.2, sends={'echo': '-10dB'}),
            tr('strings', 'strings', '-10dB', sends={'hall': '-8dB'}),
            tr('ring', 'clean-chorus', '-11dB', sends={'hall': '-6dB', 'echo': '-12dB'}),
            tr('ebow', 'ebow', '-9dB', sends={'hall': '-6dB'}),
            tr('wind', 'fx-wind', '-14dB'),
            tr('copier', 'fx-sweep', '-18dB', fx=['hp cutoff=600', 'lp cutoff=5000'], sends={'hall': '-10dB'}),
            tr('phone', {'synth': {'layers': [{'type': 'osc', 'wave': 'sine'}, {'type': 'osc', 'wave': 'square', 'level': 0.15}],
                                   'amp': {'a': '2ms', 'd': '40ms', 's': 0.8, 'r': '20ms'}}}, '-22dB',
               fx=['hp cutoff=400', 'lp cutoff=3400'], sends={'hall': '-2dB'}),
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
