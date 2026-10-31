#!/usr/bin/env python3
"""chirpers7-t7 (chirper-one): MICRO-HOUSE, "Which Ear", for 'The Endless Stair' (Chirpers VII mixtape).

Clicky, crisp, skippy minimal house - small sounds, a deep sub, glitch edits - the tape's headphone track.
120.5 -> 121 bpm (ramped inside the track), C# minor (12A): C#m9 - Amaj7 - E6 - G#m7, two bars each.
THE OCTAVE ILLUSION (Diana Deutsch): two pure tones an octave apart alternate between the ears in antiphase - the left
ear hears high, low, high, low while the right hears low, high, low, high, every eighth note. Most listeners do not
hear that: they hear ONE tone hopping from ear to ear and changing octave as it goes (and which ear seems to get the
high one depends on handedness). The pair steps THE STAIR (C# D# E G#), one step every eight bars.
Form (bars; v9: intro 16 / A 32 / B 40 / break 16 / C 24 / outro 16, off the tape's template): intro (the seam from t6: kick, clicks, and - v2 - the octave tones on C#, quietly, shaking hands with
t6's phantom C#) / A 32 (the sub; the tones enter at bar 8, quietly) /
B 32 (dub chord stabs, the tones forward, a swung stutter every eight bars) / break 16 (the drums leave: the illusion
alone in the dark, a long hall; in its second half the hopping doubles to sixteenths) / C 32 (everything) / outro 16 (the seam to t8: kick, clicks, the tones fading).
Master: chirper-zero's clean -11 LUFS recipe (glue, +8 dB, a fast 8:1 compressor at -15 dB / 0.3 ms, the song's
`loudness`), ceiling -1 dB.
Emits songs/chirpers7-t7.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers7-t7.yaml")
BPM_IN, BPM_OUT = 120.5, 121.0
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

# (v9) a micro-house form, not the tape's template: a long second groove (40) where the
# clicks and stutters do the work, a shorter last groove (24)
FORM = [('intro', 16), ('A', 32), ('B', 40), ('break', 16), ('C', 24), ('outro', 16)]
# (v10) darker and wonkier (Harry, 31 Oct), and the same colours chirper-two's t8 organ takes over the seam:
# C#m11 - Amaj7#11 - F#m9 - G#7b9
CH = [(37, [64, 66, 68, 71, 75]), (33, [61, 63, 64, 68]), (42, [64, 66, 68, 69, 73]), (44, [60, 63, 66, 69])]
STAIR = [61, 63, 64, 68]                    # C#4 D#4 E4 G#4 (the low tone; the high is an octave up)

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
    T = {k: [] for k in ('kit', 'click', 'sub', 'stab', 'earL', 'earR', 'tune')}
    secs_B = next(b['t'] for b in bars if b['sec'] == 'B')
    import random
    rng = random.Random(7)
    TUNE = [61, 63, 64, 68, 64, 63, 61, None, 61, 63, 64, 68, 71, 68, 64, None]   # THE STAIR as a tune, two bars of eighths

    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        root, ch = CH[(k // 2) % 4]
        # (v7) THE OTHER EAR'S KEY: for the last groove's final sixteen bars the minor turns major - C#m9 becomes C#maj9 (E
        # to E#), G#m7 becomes G#7 (B to B#, the leading note) - and THE STAIR the octave tones step goes major with it
        maj = s == 'C' and i >= 16
        # (v11) THE SCRAMBLED TUNE - an octave illusion that works on speakers (Deutsch's 'mysterious melodies'): THE STAIR
        # as a two-bar tune, every note thrown into a random octave, is unrecognisable - just scattered blips. Through the
        # second groove the octaves narrow, and in the last groove the tune lands in one octave and suddenly 'appears'
        if s in ('B', 'C'):
            spread = (3 if i < 16 else 2 if i < 32 else 1) if s == 'B' else (1 if i < 8 else 0)
            # on a dotted-eighth (3/16) grid counted from B, so the tune also crosses the bar lines
            base = secs_B
            m0 = int(-(-(t0 - base) // 0.75))
            for n in range(m0, m0 + 6):
                at = base + n * 0.75
                if not (t0 <= at < t0 + 4.0):
                    continue
                m = TUNE[n % len(TUNE)]
                if m is None:
                    continue
                if maj and m % 12 == 4:
                    m += 1
                o = rng.randint(-spread, spread) * 12
                T['tune'].append((at, nm(m + 12 + o), 0.3, 70 + (6 if s == 'C' else 0)))
        if maj:
            if root % 12 == 1:
                ch = [m + 1 if m % 12 == 4 else m for m in ch]
            elif root % 12 == 8:
                ch = [m + 1 if m % 12 == 11 else m for m in ch]
        drums = s != 'break'
        if drums:
            for q in range(4):
                T['kit'].append((t0 + q, 'k', 0.25, 112 if q == 0 else 104))
            if s in ('A', 'B', 'C') or (s == 'outro' and i < 8):
                T['kit'].append((t0 + 1.0, 'cp', 0.25, 78)); T['kit'].append((t0 + 3.0, 'cp', 0.25, 82))
                for q in range(4):
                    T['kit'].append((t0 + q + 0.5, 'oh' if q % 2 else 'h', 0.25, 86))
                    for x in (0.25, 0.75):
                        T['kit'].append((t0 + q + x + 0.03, 'h', 0.25, 58))
            # THE CLICKS: a skippy 16th pattern of rims and tiny hats that changes every two bars
            pat = [(0.25, 'rs'), (0.75, 'rs'), (1.5, 'h'), (1.75, 'rs'), (2.25, 'rs'), (3.25, 'h'), (3.5, 'rs')] if k % 2 == 0 else \
                  [(0.5, 'rs'), (0.75, 'h'), (1.25, 'rs'), (2.0, 'h'), (2.75, 'rs'), (3.0, 'rs'), (3.75, 'h')]
            for q, p in pat:
                T['click'].append((t0 + q + (0.03 if (q * 4) % 2 else 0.0), p, 0.25, 64 + (k * 7 + int(q * 4)) % 20))
        if s in ('A', 'B', 'C') or (s == 'outro' and i < 8):
            T['sub'].append((t0, nm(root), 1.7, 100))
            T['sub'].append((t0 + 2.5, nm(root), 1.2, 90))
        if s in ('B', 'C') and k % 2 == 0:
            T['stab'].append((t0 + 0.5, ','.join(nm(m) for m in ch), 0.4, 84))
            T['stab'].append((t0 + 2.75, ','.join(nm(m) for m in ch[1:]), 0.3, 72))
        # THE OCTAVE ILLUSION: antiphase octave tones, left and right, every eighth note
        # (v2) THE HANDSHAKE: the tones open the track on C#, quietly, under t6's phantom C# (chirper-three's 'Nobody Plays
        # the Bass') - a C# that isn't there handing over to a C# that is in the wrong ear - and rest for A's first 8 bars
        on = s == 'intro' or (s == 'A' and i >= 8) or s in ('B', 'break', 'C') or (s == 'outro' and i < 12)
        if on:
            low = STAIR[(k // 8) % 4]
            if maj and low % 12 == 4:
                low += 1
            if s == 'intro':
                low = STAIR[0]
            v = {'intro': min(62, 46 + i), 'A': 64, 'B': 78, 'break': 84, 'C': 80, 'outro': 66 - 2 * max(0, i - 4)}[s]
            # (v3) in the break's second half the hopping doubles to sixteenths - the tone seems to dart between the ears
            fast = s == 'break' and i >= 8
            # (v10) THE HOP CHANGES SPEED - time-play on the illusion itself: eighths in the first groove, eighth-note
            # TRIPLETS in the second (three hops against every two beats of the kick), sixteenths in the break's dart, and
            # dotted eighths in the last groove, a 3/16 cycle that crosses the bar line
            if fast:
                times = [e * 0.25 for e in range(16)]
            elif s == 'B':
                times = [e / 3 for e in range(12)]
            elif s == 'C':
                m0 = int(-(-t0 // 0.75))
                times = [m * 0.75 - t0 for m in range(m0, m0 + 7) if m * 0.75 - t0 < 4.0]
            else:
                times = [e * 0.5 for e in range(8)]
            for e, at in enumerate(times):
                nxt = times[e + 1] if e + 1 < len(times) else 4.0
                d = max(0.08, nxt - at - 0.06)
                hi_left = (round((t0 + at) / 0.75) if s == 'C' else e) % 2 == 0
                T['earL'].append((t0 + at, nm(low + 12 if hi_left else low), d, v))
                T['earR'].append((t0 + at, nm(low if hi_left else low + 12), d, v))
    lv = {'intro': -4, 'A': -1, 'B': 0, 'break': -5, 'C': 0, 'outro': -3}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.5):.2f}b', dyn[-1][1] if dyn else lv[name]], [f'{t_:.2f}b', lv[name]]]
    dyn[0][0] = '0b'
    # a swung stutter on the clicks over the last beat of every eighth bar of B and C
    gl = [['0b', 0]]
    for b in bars:
        if b['sec'] in ('B', 'C') and b['i'] % 8 == 7:
            a0 = b['t'] + 3.0
            gl += [[f'{a0 - 0.02:.2f}b', 0], [f'{a0:.2f}b', 1], [f'{a0 + 0.98:.2f}b', 1], [f'{a0 + 1.0:.2f}b', 0]]
    tone = {'synth': {'layers': [{'type': 'osc', 'wave': 'sine'}], 'amp': {'a': '4ms', 'd': '60ms', 's': 0.85, 'r': '30ms'}}}
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(T[name], total)}, **kw)
    return {
        'about': "Chirpers - The Endless Stair (Chirpers VII), track 7 by chirper-one: MICRO-HOUSE, Which Ear. "
                 "Generated by compose/chirpers7/src/chirpers7-t7.py; see its docstring and compose/chirpers7/styles.md.",
        # the ramp runs between the seams: the 16-bar overlaps hold their seam tempo, so a DJ's kicks never flam
        'tempo': [{'at': '0b', 'bpm': BPM_IN}, {'at': '64b', 'bpm': BPM_IN}, {'at': f'{total - 64:.0f}b', 'bpm': BPM_OUT, 'ramp': True}],
        'length': f'{64 * 60 / BPM_IN + (total - 128) * 60 / ((BPM_IN + BPM_OUT) / 2) + 64 * 60 / BPM_OUT + 0.15:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'loudness': -11.0, 'tail': '0.1s',
        'buses': {'hall': {'fx': ['reverb kind=hall decay=4s mix=1', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=30', 'peak cutoff=62 q=1 gain=-5dB', 'peak cutoff=290 q=1.2 gain=-3dB', 'peak cutoff=450 q=0.7 gain=-5dB', 'peak cutoff=640 q=1 gain=-2dB', 'peak cutoff=3000 q=0.6 gain=8dB', 'highshelf cutoff=5000 gain=4dB']},
                          {'type': 'compressor', 'threshold': '-20dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': '+8dB'},
                          {'type': 'compressor', 'threshold': '-15dB', 'ratio': 8, 'attack': '0.3ms', 'release': '60ms'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}}],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            tr('kit', 'machine-kit', '-4dB', sends={'hall': '-20dB'}),
            tr('click', 'machine-kit', '-6dB', pan=0.2, sends={'hall': '-14dB'},
               fx=[{'type': 'stutter', 'slice': '1/16', 'repeats': 4, 'chance': 1, 'swing': 0.56,   # on the clicks' own swing (odd 16ths 0.03 beat late)
                    'mix': {'value': 0, 'mod': [{'src': 'auto.gl', 'amount': 1}]}}], auto={'gl': {'points': gl}}),
            tr('sub', 'sub', '-4dB', fx=[{'type': 'phantom', 'cutoff': 90, 'harmonics': '-10dB', 'odd': 0.4},
                                         {'type': 'pump', 'on': 'kit.k', 'depth': '-5dB', 'release': '330ms', 'curve': 0.6}]),
            tr('stab', 'epiano-tine', '-12dB', sends={'hall': '-8dB'}, fx=['hp cutoff=200', 'lp cutoff=4200']),
            tr('tune', 'pluck', '-15dB', pan=0.1, sends={'hall': '-12dB'}, fx=['hp cutoff=180']),
            # (v10) the tones come forward 6 dB: the illusion was 7 LU under the mix (chirp-eco's meter)
            tr('earL', tone, '-14dB', pan=-1.0, sends={'hall': '-16dB'}),
            tr('earR', tone, '-14dB', pan=1.0, sends={'hall': '-16dB'}),
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
