#!/usr/bin/env python3
"""chirpers4-t3 (chirper-one): PEAK-TIME WAREHOUSE / HARD TECHNO, "the one comes home", for 'Phantom Downbeat'.

The answer to Where Is the One (t9): there the one gets lost; here it is found.
- THE DISPLACED START: for the intro and the first groove the kick sits on the OFF-beats and the closed hats on the
  beats, so the ear takes the kick as the pulse and hears the whole grid shifted by an eighth.
- THE VOICE: in the break, with no kick, a giant synthesised voice (an octave down, formants pulled lower still with
  the new formant-preserving pitch) chants "one" on the true downbeats; a hoover swells under it.
- THE HOMECOMING: the drop puts the kick on the true beats, hoover stabs land on every one, and the grid the ear
  had been hearing snaps over by an eighth.
- In the second peak the voice comes back every four bars. In the outro the kick slips back to the off-beats: the
  one leaves again.
- THE FILTERED START: the intro plays through a master low-pass that opens from 400 Hz into the first groove; the
  beat before the drop is silence (v2).
- In the peak's second half a reese rolls off-beat sixteenths on A1; the peak's home stab and its answer a minor
  third up alternate bar by bar (v3: less piled up).
- The bass is RUMBLE: the kick fed through a dark hall, low-passed, driven and pumped (Berlin warehouse low end).

Form: intro, A (the displaced groove), break (the voice), drop (home), peak (voice and ride), outro (it slips).
Emits songs/chirpers4-t3.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers4-t3.yaml")
BPM = 140
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('A', 32), ('break', 16), ('drop', 32), ('peak', 32), ('outro', 16)]
HOOVER = [45, 52, 57, 60]                 # A minor (A2 E3 A3 C4): the home chord

def line(events, total):
    ev = sorted(events)
    toks, t = [], 0.0
    for k, (at, p, d, v) in enumerate(ev):
        if at < t - 1e-6: continue
        if at > t + 1e-4: toks.append(f"R/{at - t:.4f}b")
        nxt = ev[k + 1][0] if k + 1 < len(ev) else total
        d = max(0.02, min(d, nxt - at))
        base, _, attr = p.partition('^')         # per-note attributes (^ph=...) go after the velocity
        toks.append(f"{base}/{d:.4f}b@{v}" + (f"^{attr}" if attr else "")); t = at + d
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
    kit, hoov, voice, reese = [], [], [], []
    for b in bars:
        s, t0, i = b['sec'], b['t'], b['i']
        displaced = s in ('intro', 'A') or (s == 'outro' and i >= 4)
        for q in range(16):
            at = t0 + q * 0.25 + (0.02 if q % 2 else 0.0)
            on_beat, off_beat = q % 4 == 0, q % 4 == 2
            if s != 'break' and not (s == 'outro' and i >= 12):
                if (off_beat if displaced else on_beat):
                    kit.append((at, 'k', 0.25, 124))
                    if s == 'peak':
                        kit.append((at, 'kh', 0.25, 104))   # the peak layers the distorted kick on top (the pumps still key on k)
            # the hats: on the beats while the kick is displaced (they confirm the wrong grid), off-beat opens once home
            if displaced and on_beat:
                kit.append((at, 'h', 0.25, 96))
            if not displaced and s in ('drop', 'peak') and off_beat:
                kit.append((at, 'oh', 0.25, 92))
            if s in ('A', 'drop', 'peak') and q % 2 == 1:
                kit.append((at, 'h', 0.25, 60))
            if s in ('drop', 'peak') and q in (4, 12):
                kit.append((at, 'cp', 0.25, 108))
            if s == 'peak' and off_beat:
                kit.append((at, 'rd', 0.25, 74))
            if s == 'break' and i >= 12:
                st = 4 if i < 14 else 2                # a snare roll into the drop: quarters, then eighths, then 16ths
                if i == 15: st = 1
                if q % st == 0:
                    kit.append((at, 's', 0.25, 70 + 3 * (i - 12) + q))
        if s in ('drop', 'peak') and i % 8 == 0:
            kit.append((t0, 'c', 0.25, 110))
        # THE PEAK'S REESE: off-beat sixteenths rolling on A1, the octave on the and-of-4
        if s == 'peak' and i >= 16:          # (v3) the reese waits for the peak's second half
            for q in (2, 3, 6, 7, 10, 11, 14, 15):
                reese.append((t0 + q * 0.25, nm(45 if q == 14 else 33), 0.22, 100 if q % 4 == 2 else 84))
        # the voice: "one" on the true downbeats - every bar in the break, every four bars in the peak
        if (s == 'break') or (s == 'peak' and i % 4 == 0):
            voice.append((t0, 'A3^ph=w-ah1-n', 1.4, 112))
        # the hoover: a swell under the break, stabs on every one once home
        if s == 'break' and i % 4 == 0:
            hoov.append((t0, ','.join(nm(m) for m in HOOVER), 15.5, 70 + 4 * (i // 4)))
        if s == 'A' and i >= 8:
            # the displaced groove's stab: a short hoover on every and-of-1 and and-of-3, confirming the wrong grid
            for x in (0.5, 2.5):
                hoov.append((t0 + x, ','.join(nm(m) for m in HOOVER), 0.2, 84 + i))
        if s in ('drop', 'peak'):
            # (v3) in the peak the home stab and its answer alternate bar by bar instead of piling up
            if s == 'drop' or i % 2 == 0:
                hoov.append((t0, ','.join(nm(m) for m in HOOVER), 0.45, 118))
            if s == 'peak' and i % 2 == 1:
                hoov.append((t0 + 2.5, ','.join(nm(m + 3) for m in HOOVER), 0.4, 100))
    end_s = total * SPB
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'] * SPB)
    lv = {'intro': -7, 'A': -1, 'break': -8, 'drop': 0, 'peak': 0, 'outro': -5}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.3):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    dyn.append([f'{end_s:.3f}s', -12])
    # THE HELD BREATH (v2): the last beat before the drop is silence - after the voice's last "one", nothing,
    # then the kick lands home
    tg = secs['drop']; g0 = tg - SPB
    pts = [(float(p[0][:-1]), p[1]) for p in dyn]
    before = [p for p in pts if p[0] <= g0 - 0.02]; after = [p for p in pts if p[0] >= tg - 0.004]
    pts = before + [(g0 - 0.01, before[-1][1]), (g0, -40), (tg - 0.006, -40)] + after
    dyn = [['0s', pts[0][1]]] + [[f'{t_:.3f}s', v] for t_, v in pts if t_ > 0]
    return {
        'about': "Chirpers - Phantom Downbeat (Chirpers IV), track 3 by chirper-one: PEAK-TIME WAREHOUSE, the one comes home. "
                 "Generated by compose/chirpers4/src/chirpers4-t3.py; see its docstring and compose/chirpers4/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2:.2f}s', 'ceiling': '-1dB',
        'buses': {'rumble': {'fx': ['reverb kind=hall decay=2.8s mix=1', 'lp cutoff=160', 'drive drive=0.5 mix=1',
                                    {'type': 'pump', 'on': 'kit.k', 'depth': '-12dB', 'release': '280ms', 'curve': 0.6}], 'returns': []},
                  'hall': {'fx': ['reverb kind=hall decay=3.5s mix=1', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=32', 'peak cutoff=45 q=1 gain=-5dB', 'lowshelf cutoff=150 gain=-5dB', 'peak cutoff=44 q=1.2 gain=-3dB', 'peak cutoff=62 q=1.2 gain=-3dB', 'peak cutoff=180 q=0.8 gain=-5dB',
                                                   'peak cutoff=900 q=0.7 gain=3dB', 'peak cutoff=2200 q=0.7 gain=4dB', 'highshelf cutoff=4000 gain=7dB']},
                          {'type': 'filter', 'kind': 'lp', 'q': 0.9, 'cutoff': {'value': 18000, 'mod': [{'src': 'auto.op', 'amount': -5.5}]}},
                          {'type': 'gain', 'gain': '+16dB'},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 3, 'attack': '10ms', 'release': '120ms', 'makeup': '2dB'},
                          {'type': 'compressor', 'threshold': '-8dB', 'ratio': 6, 'attack': '1ms', 'release': '50ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'compressor', 'threshold': '-6dB', 'ratio': 4, 'attack': '3ms', 'release': '80ms', 'makeup': '5dB'}, 'lp cutoff=14000'],
                   'auto': {'dyn': {'points': dyn}, 'op': {'points': [['0s', 1], [f"{secs['A'] - 4 * 4 * SPB:.3f}s", 0.6], [f"{secs['A']:.3f}s", 0]]}}},
        'tracks': [
            {'name': 'kit', 'patch': '909', 'gain': '-2dB', 'sends': {'rumble': '-13dB'}, 'score': merge_kit(kit, total)},
            {'name': 'reese', 'patch': 'reese', 'gain': '-10dB', 'fx': [{'type': 'pump', 'on': 'kit.k', 'depth': '-9dB', 'release': '280ms', 'curve': 0.6}], 'score': line(reese, total)},
            {'name': 'hoover', 'patch': 'hoover', 'gain': '-11dB', 'sends': {'hall': '-14dB'},
             'fx': [{'type': 'pump', 'on': 'kit.k', 'depth': '-6dB', 'release': '280ms', 'curve': 0.6}], 'score': line(hoov, total)},
            # THE GIANT VOICE: an octave down with its formants pulled lower still (wM's formant-preserving pitch)
            {'name': 'voice', 'patch': 'voice', 'gain': '-6dB', 'sends': {'hall': '-6dB'},
             'fx': [{'type': 'pitch', 'semitones': -12, 'formant': {'value': -7, 'mod': [{'src': 'auto.giant', 'amount': 7}]}}, {'type': 'drive', 'drive': 0.3, 'mix': 0.4}],
             # (v5) THE GIANT WAKES: through the break the voice's formants climb from -7 (a giant) to 0 (a man) as the drop
             # nears, then fall back for the peak's calls - the voice seems to grow closer and smaller as the one comes home
             'auto': {'giant': {'points': [['0s', 0], [f"{secs['break']:.3f}s", 0], [f"{secs['drop'] - 2 * 4 * SPB:.3f}s", 0.55],
                                           [f"{secs['drop'] - 0.05:.3f}s", 1.0], [f"{secs['drop'] + 0.5:.3f}s", 0.3], [f"{secs['peak']:.3f}s", 0.3]]}},
             'score': line(voice, total)},
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
