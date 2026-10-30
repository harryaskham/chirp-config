#!/usr/bin/env python3
"""chirpers5-t5 (chirper-one): AMBIENT / HALF-TIME INTERLUDE, "Underpass", for 'Soft Concrete' (Chirpers V).

The album's breath between Hairline (t4, G minor glitchstep) and Overpass Rain (t6, F minor roller): walking through
an underpass at night, the city's roll heard through concrete. Patient, sparse, half-time at 174 (the 87 feel).
- THE TUNNEL: a dark wobbly grand (piano-wash) and a stretched-voice pad move from G minor down to F minor -
  Gm9 - Ebmaj7 - Cm9 - Dbmaj7, four bars each, ending on a held Fm9 for Overpass Rain to begin on.
- THE HALF-TIME: in the middle sections the amen plays half-time - its kick on the one, its snare on the three, a
  ghost or two - with a deep sub on the roots; no roll, no garage skip, no glitch fracture.
- THE ECHOES: the whole amen is also sent, quietly, through a granular cloud (wM's cloud: small grains, scattered,
  some reversed) and a long hall - the drum & bass from the next room, smeared into the walls - but only where the
  beat is NOT: the intro's second half and the drift, where only these echoes, the stretched-voice pad and a low voice
  remain (the piano rests there). The second half-time adds a glass bell on the chords' top notes.
- (v3, Harry's Soft Concrete notes) the sub gains weight (phantom harmonics, drive, pumped); a tapestop winds the first
  half-time down into the drift; the piano is darker and pumps with the kick, and a notch turns the voice pad on a 5-bar LFO; a touch darker; and the last eight bars fade the tunnel out under rising rain - out of the underpass into
  Overpass Rain's weather.
Form: intro 16 / half 32 / drift 24 / half2 24 / outro 16 (Dbmaj7 -> Fm9, fading into rain for t6).
Levels on the album standard: -12.5 LUFS +-1.5 target (an interlude may sit at its quiet edge), true peak <= -1 dBTP,
no pinned runs; volume 0 dB, true_peak on, a low-knee soft clip ending the master.
Emits songs/chirpers5-t5.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers5-t5.yaml")
BPM = 174
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('half', 32), ('drift', 24), ('half2', 24), ('outro', 16)]
CHORDS = [(31, [53, 58, 62, 65, 69]), (27, [55, 58, 62, 67]), (24, [51, 55, 58, 62]), (25, [53, 56, 60, 65])]
END = (29, [51, 56, 60, 63, 67])       # Fm9, the handover to Overpass Rain
# half-time amen: (beat, slice, vel): the kick on 1, the snare on 3, ghosts
HALF = [(0.0, 0, 112), (1.5, 3, 66), (2.0, 4, 110), (3.25, 10, 60), (3.5, 6, 72)]

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
    amen, ghost, piano, pad, sub, voice, glass = [], [], [], [], [], [], []
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        if s == 'outro' and i >= 8:
            root, ch = END
        elif s == 'outro':
            root, ch = CHORDS[3]
        else:
            root, ch = CHORDS[(k // 4) % 4]
        if s in ('half', 'half2'):
            for q, sl, v in HALF:
                amen.append((t0 + q, nm(36 + sl), 0.5, v - (8 if s == 'half2' else 0)))
            if k % 4 == 0:
                sub.append((t0, nm(root), 7.5, 100))
                sub.append((t0 + 8.0, nm(root), 7.5, 92))
        # THE ECHOES: the whole amen in order, very quiet, only to feed the cloud and the frozen hall
        if s == 'drift' or (s == 'intro' and i >= 8):
            for e in range(8):
                ghost.append((t0 + e * 0.5, nm(36 + (k % 4) * 8 + e), 0.5, 70))
        # the tunnel: piano-wash holds each chord (rolled) every four bars; the voice pad under it
        if (k % 4 == 0 or (s == 'outro' and i == 8)) and s != 'drift':
            for j, m in enumerate(ch):
                piano.append((t0 + 0.06 * j, nm(m), 15.5 - 0.06 * j, 70))
        if k % 4 == 0 and s in ('intro', 'drift', 'outro'):
            pad.append((t0, ','.join(nm(m - 12) for m in ch[:3]), 15.8, 74))
        # (v2) the second half-time adds glass: a high bell on the chord's top notes, the streetlight through the grating
        if s == 'half2' and k % 2 == 0:
            for q, m in ((0.0, ch[-1] + 12), (1.5, ch[-2] + 12), (3.0, ch[-1] + 24)):
                glass.append((t0 + q, nm(m), 1.4, 70))
        if s == 'drift' and k % 4 == 0:
            voice.append((t0 + 2.0, nm(ch[-1] - 12) + '^u', 10.0, 80))
    end_s = total * SPB
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'] * SPB)
    lv = {'intro': -6, 'half': 0, 'drift': -4, 'half2': -1, 'outro': -4}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.6):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    # (v3) INTO THE RAIN: the last eight bars fade the tunnel out under a rising rain - we walk out of the underpass
    # into Overpass Rain's weather (its intro is rain), the music sinking to the rain's level by the last bar
    t_out = secs['outro'] + 8 * 4 * SPB
    dyn += [[f'{t_out:.3f}s', lv['outro']], [f'{end_s:.3f}s', -16]]
    rainlane = [['0s', -30], [f'{t_out:.3f}s', -30], [f'{end_s - 2.0:.3f}s', 0]]
    # (v3) THE TUNNEL WINDS DOWN: a tapestop on the master over the last beat of the first half-time, into the drift
    td = secs['drift']
    ts = [['0s', 0], [f'{td - 2 * SPB - 0.01:.3f}s', 0], [f'{td - 2 * SPB:.3f}s', 1], [f'{td - 0.01:.3f}s', 1], [f'{td:.3f}s', 0]]
    return {
        'about': "Chirpers - Soft Concrete (Chirpers V), track 5 by chirper-one: AMBIENT / HALF-TIME INTERLUDE, Underpass. Generated by "
                 "compose/chirpers5/src/chirpers5-t5.py; see its docstring and compose/chirpers5/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 1.2:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'true_peak': True,
        'buses': {'walls': {'fx': [{'type': 'cloud', 'size': '60ms', 'density': 14, 'position': 0.5, 'spray': 0.6, 'pitch': 0,
                                    'scatter': 0.4, 'reverse': 0.35, 'spread': 0.8, 'mix': 1, 'seed': 5},
                                   'reverb kind=hall decay=5s mix=1', 'lp cutoff=3000', 'hp cutoff=200'], 'returns': []},
                  'hall': {'fx': ['reverb kind=hall decay=4.5s mix=1', 'hp cutoff=200'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'peak cutoff=45 q=1 gain=-4dB', 'peak cutoff=110 q=0.8 gain=4dB', 'peak cutoff=220 q=1 gain=-3dB', 'peak cutoff=450 q=0.8 gain=-6dB', 'highshelf cutoff=7000 gain=-2dB']},
                          {'type': 'compressor', 'threshold': '-22dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'gain', 'gain': '+13dB'},
                          {'type': 'compressor', 'threshold': '-5dB', 'ratio': 10, 'attack': '0.3ms', 'release': '60ms', 'makeup': '1.5dB'},
                          {'type': 'tapestop', 'time': '2b', 'mix': 1, 'stop': {'value': 0, 'mod': [{'src': 'auto.ts', 'amount': 1}]}},
                          'lp cutoff=14000',
                          {'type': 'clip', 'drive': '0dB', 'ceiling': '-1.8dB', 'knee': 0.55, 'link': True}],
                   'auto': {'dyn': {'points': dyn}, 'ts': {'points': ts}}},
        'tracks': [
            {'name': 'amen', 'patch': 'amen-chops', 'gain': '-6dB', 'sends': {'hall': '-14dB'},
             'fx': [{'type': 'compressor', 'threshold': '-20dB', 'ratio': 6, 'attack': '0.5ms', 'release': '50ms', 'makeup': '6dB'}, 'lp cutoff=7000'],
             'score': line(amen, total)},
            {'name': 'ghost', 'patch': 'amen-chops', 'gain': '-40dB', 'sends': {'walls': '+22dB'}, 'score': line(ghost, total)},
            # (v3) THE BASS WITH WEIGHT: the sine sub stays mono and deep, and wM's phantom fx adds its harmonics above
            # 100 Hz (so it reads on small speakers), lightly driven, pumped by the half-time kick
            {'name': 'sub', 'patch': 'sub', 'gain': '-2dB', 'fx': [{'type': 'phantom', 'cutoff': 100, 'harmonics': '-10dB', 'odd': 0.4},
                                                                   {'type': 'drive', 'drive': 0.15, 'mix': 0.3},
                                                                   {'type': 'pump', 'on': 'amen', 'depth': '-5dB', 'release': '300ms', 'curve': 0.6}],
             'score': line(sub, total)},
            # (v3) the piano darker (a 2.4 kHz low-pass) and pumped by the half-time kick, so it breathes with the beat
            {'name': 'piano', 'patch': 'piano-wash', 'gain': '-7dB',
             'fx': ['lp cutoff=2400', {'type': 'pump', 'on': 'amen', 'depth': '-3dB', 'release': '300ms', 'curve': 0.6}], 'score': line(piano, total)},
            # (v3) a notch sweeps the voice pad on a five-bar LFO, so the stretched voices seem to turn in the dark
            {'name': 'pad', 'patch': 'vox-pad', 'gain': '-12dB', 'sends': {'hall': '-10dB'}, 'lfo': {'turn': 'sine rate=5/1 phase=0'},
             'fx': [{'type': 'filter', 'kind': 'notch', 'q': 2, 'cutoff': {'value': 700, 'mod': [{'src': 'lfo.turn', 'amount': 1.5}]}}], 'score': line(pad, total)},
            {'name': 'glass', 'patch': 'pad-glass', 'gain': '-17dB', 'sends': {'hall': '-8dB'}, 'score': line(glass, total)},
            {'name': 'rain', 'patch': 'fx-rain', 'gain': {'value': '-12dB', 'mod': [{'src': 'auto.rn', 'amount': 1}]}, 'auto': {'rn': {'points': rainlane}},
             'score': f"C4/{8 * 4 - 0.2:.4f}b@80" if False else line([(total - 32.0, 'C4', 32.0, 84)], total)},
            {'name': 'voice', 'patch': 'voice', 'gain': '-12dB', 'sends': {'hall': '-4dB'},
             'fx': [{'type': 'pitch', 'semitones': 0, 'formant': -4}], 'score': line(voice, total)},
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
