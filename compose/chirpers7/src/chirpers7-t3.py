#!/usr/bin/env python3
"""chirpers7-t3 (chirper-one): SOULFUL DEEP HOUSE, "One More Step", for 'The Endless Stair' (Chirpers VII mixtape).

A warm, deep groove with Rhodes and a voice, 118.5 -> 119 bpm (ramped inside the track), E minor (9A):
Em9 - Cmaj9 - Am9 - Bm7, two bars each.
THE SPEECH-TO-SONG ILLUSION: a spoken phrase - "one more step up" - repeats every two bars. At first it is plainly
speech (a falling, conversational contour). With each repetition its contour is pulled toward THE STAIR, the tape's
thread (E F# G B, degrees 1 2 3 5), until the four syllables land on those notes and the sentence SINGS; a sung double
surfaces under it; in the break the song is heard alone; and when the plain speech comes back at the end, the ear
keeps hearing the melody in it.
Form (bars): intro 16 (the seam from t2: kick, hats, pad) / A 32 (groove, bass, Rhodes; the phrase enters at bar 8
as speech) / B 32 (the contour quantises; the sung double fades in) / break 16 (drums out: the song alone with the
Rhodes) / C 32 (full groove, the stair sung, the Rhodes quoting it) / outro 16 (the seam to t4: kick, hats and the
plain spoken phrase).
Emits songs/chirpers7-t3.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers7-t3.yaml")
BPM_IN, BPM_OUT = 118.5, 119.0
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('A', 32), ('B', 32), ('break', 16), ('C', 32), ('outro', 16)]
CH = [(28, [52, 55, 59, 62, 66]), (24, [52, 55, 59, 62, 64]), (33, [55, 59, 60, 64, 67]), (35, [54, 57, 59, 62, 66])]
WORDS = ['w-ah1-n', 'm-ao1-r', 's-t-eh1-p', 'ah1-p']
SPEECH = [(52, 150, -60), (52, 90, -40), (52, 40, -160), (52, -60, -320)]   # pitch, cents at onset, cents at end
STAIR = [52, 54, 55, 59]                                                    # E3 F#3 G3 B3
STEP_AT = [0.0, 0.5, 1.0, 1.75]                                             # beat offsets of the four syllables

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

def phrase(at, w, vel=90):
    """the spoken phrase at blend w (0 = speech, 1 = song): pitches move to THE STAIR, the glides flatten"""
    out = []
    for k, (ph, (p, c0, c1), tgt, off) in enumerate(zip(WORDS, SPEECH, STAIR, STEP_AT)):
        m = round(p + (tgt - p) * w)
        a, b = round(c0 * (1 - w)), round(c1 * (1 - w))
        out.append((at + off, f"{nm(m)}^ph={ph}^f0={a}>{b}", 0.45 if k < 3 else 0.9, vel))
    return out

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 't': t}); t += 4.0
    total = t
    T = {k: [] for k in ('kit', 'sub', 'bass', 'keys', 'pad', 'speech', 'sung', 'stair')}
    n_rep = 0
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        root, ch = CH[(k // 2) % 4]
        first = k % 2 == 0
        drums = s not in ('break',) and not (s == 'intro' and i < 4)
        if drums:
            full = s in ('A', 'B', 'C')
            for q in range(4):
                T['kit'].append((t0 + q, 'k', 0.25, 118 if q == 0 else 110))
                T['kit'].append((t0 + q + 0.5, 'oh' if (full or i >= 8) else 'h', 0.25, 84))
                for x in (0.25, 0.75):
                    T['kit'].append((t0 + q + x + 0.02, 'h', 0.25, 64 + (10 if x == 0.75 else 0)))
            if full or (s == 'outro' and i < 8):
                T['kit'].append((t0 + 1.0, 'cp', 0.25, 96)); T['kit'].append((t0 + 3.0, 'cp', 0.25, 100))
            if s in ('B', 'C') and i % 2 == 1:
                T['kit'].append((t0 + 3.75 + 0.02, 'rs', 0.25, 70))
        # bass: the root on the one, an octave answer on the and-of-2 and the four's offbeat
        if s in ('A', 'B', 'C') or (s == 'outro' and i < 8):
            T['sub'].append((t0, nm(root), 1.6, 100))
            T['sub'].append((t0 + 2.0, nm(root), 1.0, 92))
            for q, o in ((1.5, 12), (3.5, 7)):
                T['bass'].append((t0 + q + 0.02, nm(root + o), 0.4, 84))
        # Rhodes: soulful stabs (the one held, the and-of-2 answered without the root)
        if (s in ('B', 'C', 'break') or (s == 'A' and i >= 8)):
            if first:
                T['keys'].append((t0, ','.join(nm(m) for m in ch), 1.8, 84))
            else:
                T['keys'].append((t0 + 1.5, ','.join(nm(m) for m in ch[1:]), 1.2, 76))
        if (s in ('intro', 'break', 'outro') or s == 'A') and k % 4 == 0:
            T['pad'].append((t0, ','.join(nm(m - 12) for m in ch[:3]), 15.8, 70))
        # THE PHRASE: every two bars from A's bar 8; the blend toward song grows through B
        on = (s == 'A' and i >= 8) or s in ('B', 'C') or (s == 'outro' and i < 12)
        if on and first:
            if s == 'A':
                w = 0.0
            elif s == 'B':
                w = min(1.0, i / 24)
            elif s == 'C':
                w = 1.0
            else:
                w = 0.0                                # the plain speech returns at the end
            T['speech'] += phrase(t0, w)
            n_rep += 1
            if (s == 'B' and i >= 12) or s == 'C':
                T['sung'] += [(a, p.split('^f0')[0], d, 70 + (10 if s == 'C' else 0)) for a, p, d, _ in phrase(t0, 1.0)]
        if s == 'break' and first:
            T['sung'] += [(a, p.split('^f0')[0], d, 86) for a, p, d, _ in phrase(t0, 1.0)]
        # the Rhodes quotes THE STAIR in C, an octave up, answering the phrase
        if s == 'C' and not first:
            for off, m in zip(STEP_AT, STAIR):
                T['stair'].append((t0 + 2.0 + off, nm(m + 24), 0.45, 76))
    beats_total = total
    lv = {'intro': -4, 'A': -1, 'B': 0, 'break': -5, 'C': 0, 'outro': -3}
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'])
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.5):.2f}b', dyn[-1][1] if dyn else lv[name]], [f'{t_:.2f}b', lv[name]]]
    dyn[0][0] = '0b'
    # the break's filter: the Rhodes and the song through a low-pass that opens back up into C
    tb, tc = secs['break'], secs['C']
    op = [['0b', 0], [f'{tb:.2f}b', 0], [f'{tb + 0.1:.2f}b', 1], [f'{tc - 8:.2f}b', 1], [f'{tc:.2f}b', 0]]
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(T[name], total)}, **kw)
    return {
        'about': "Chirpers - The Endless Stair (Chirpers VII), track 3 by chirper-one: SOULFUL DEEP HOUSE, One More Step. "
                 "Generated by compose/chirpers7/src/chirpers7-t3.py; see its docstring and compose/chirpers7/styles.md.",
        'tempo': [{'at': '0b', 'bpm': BPM_IN}, {'at': f'{beats_total:.0f}b', 'bpm': BPM_OUT, 'ramp': True}],
        'length': f'{beats_total * 60 / ((BPM_IN + BPM_OUT) / 2) + 0.15:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'loudness': -11.0, 'tail': '0.1s',
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1', 'hp cutoff=250'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.35, 'mix': 1}, 'lp cutoff=3500', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=30', 'peak cutoff=55 q=1 gain=-4dB', 'peak cutoff=300 q=0.8 gain=-2dB', 'highshelf cutoff=5000 gain=4dB']},
                          {'type': 'filter', 'kind': 'lp', 'q': 0.8, 'cutoff': {'value': 18000, 'mod': [{'src': 'auto.op', 'amount': -3.2}]}},
                          {'type': 'compressor', 'threshold': '-20dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'gain', 'gain': '+10.5dB'},
                          {'type': 'compressor', 'threshold': '-5dB', 'ratio': 10, 'attack': '0.3ms', 'release': '60ms', 'makeup': '1dB'},
                          'limiter ceiling=-1dB'],
                   'auto': {'dyn': {'points': dyn}, 'op': {'points': op}}},
        'tracks': [
            tr('kit', 'machine-kit', '-4dB', sends={'hall': '-18dB'}),
            tr('sub', 'sub', '-6dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-5dB', 'release': '330ms', 'curve': 0.6}]),
            tr('bass', 'bass', '-10dB', fx=['lp cutoff=1200', {'type': 'pump', 'on': 'kit.k', 'depth': '-5dB', 'release': '330ms', 'curve': 0.6}]),
            tr('keys', {'extends': 'epiano-tine', 'play': {'release': {'patch': 'epiano-damper', 'decay': '2s'}}}, '-9dB',
               sends={'echo': '-12dB', 'hall': '-12dB'}, fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-3dB', 'release': '330ms', 'curve': 0.6}]),
            tr('pad', 'juno-pad', '-14dB', sends={'hall': '-10dB'}),
            tr('speech', 'voice-speech', '-5dB', sends={'hall': '-14dB', 'echo': '-14dB'}),
            tr('sung', 'voice', '-10dB', fx=[{'type': 'pitch', 'semitones': 12, 'formant': 0}], sends={'hall': '-6dB', 'echo': '-10dB'}),
            tr('stair', {'extends': 'epiano-tine', 'play': {'release': {'patch': 'epiano-damper', 'decay': '2s'}}}, '-10dB', pan=0.3, sends={'echo': '-8dB'}),
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
