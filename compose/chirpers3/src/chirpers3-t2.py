#!/usr/bin/env python3
"""chirpers3-t2 (chirper-one): TRIP-HOP NOIR for 'Tape Weather' (Chirpers III).

Slow, heavy and cinematic: a rainy-night film score with a beat, at 72 bpm.
- The break: half-time (the snare on 3), dragged through a dusty sampler and pitched down, with ghost notes.
- Minor mellotron strings carry a line that DESCENDS a step every four bars: Cm9, Bb6, Abmaj7, G7b9 (i, bVII, bVI, V).
- Against it, a gliding theremin-like lead (boc-lead, long glide) CLIMBS (G, Ab, Bb, B).
- Also: a wordless vox pad, a sub bass that slides between roots, sparse rhodes stabs, and crackle.
- Before each return, the break drops out for a bar of strings and crackle.

Form: intro (strings and crackle), A (the break enters), B (+ lead, vox), drop, A2 (+ rhodes), B2 (the lead an
octave up), drop, outro.
Emits songs/chirpers3-t2.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers3-t2.yaml")
BPM = 72
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

# the 16-bar cycle: four bars a chord (MIDI voicings), the strings' top line descending C Bb Ab G
CYCLE = [(36, [48, 55, 58, 62, 63], 72), (34, [46, 53, 57, 58, 62], 70), (32, [44, 51, 55, 60, 63], 68), (31, [43, 50, 53, 56, 59], 67)]
LEAD = [67, 68, 70, 71]          # the lead climbs G Ab Bb B against the strings' fall
FORM = [('intro', 6), ('A', 8), ('B', 8), ('drop', 1), ('alley', 4), ('A2', 6), ('B2', 12), ('drop2', 1), ('outro', 8)]

_seed = [777]
def rnd():
    _seed[0] = (_seed[0] * 1103515245 + 12345) & 0x7fffffff
    return (_seed[0] / 0x7fffffff) * 2 - 1

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

def notes(events):
    return [{'at': f'{at * SPB:.4f}s', 'len': f'{d * SPB:.4f}s', 'pitch': m, 'vel': round(v / 127, 3)} for at, m, d, v in events]

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            # THE LONG DESCENT: the chords change by section, not by bar - the i - bVII - bVI - V fall spread over
            # the whole song: intro/A/A2/outro on Cm9 (A turns to Abmaj7 for its second half), B falls i -> bVII,
            # B2 falls bVI -> V and then lifts a minor third for its last four bars (the climax)
            HC = {'intro': [0], 'A': [0, 2], 'B': [0, 1], 'drop': [3], 'alley': [2], 'A2': [0], 'B2': [2, 3, 'lift'], 'drop2': [3], 'outro': [0]}[name]
            idx = HC[min(len(HC) - 1, i * len(HC) // n)]
            c = CYCLE[3] if idx == 'lift' else CYCLE[idx]
            if idx == 'lift':
                c = (c[0] + 3, [m + 3 for m in c[1]], c[2] + 3)
            bars.append({'sec': name, 'i': i, 't': t, 'c': c}); t += 4.0
    total = t
    ms = lambda x: x / 1000 / SPB
    kit, strings, vox, lead, sub, rhodes, crackle, cello, segue, rain = [], [], [], [], [], [], [], [], [], []
    n_outro = dict(FORM)['outro']
    for k, b in enumerate(bars):
        s, t0, (root, ch, top) = b['sec'], b['t'], b['c']
        beat = s in ('A', 'B', 'A2', 'B2')
        # ---- the half-time break (swung eighths, snare on 3, ghost notes, a lazy open hat) ----
        if beat:
            sw = lambda e: (e // 2) * 1.0 + (0.58 if e % 2 else 0.0)        # swung eighths
            # THE BREAK BREATHES BAR BY BAR (a four-bar drum phrase): bar 1 the plain break; bar 2 the kick pushes
            # (an extra kick on 2-and, the 3-and kick dropped); bar 3 the ghosts thicken and the hats open on the 4;
            # bar 4 ends in a fill - the snare doubled in sixteenths across beat 4 into the next phrase
            ph = b['i'] % 4
            kicks = {0: ((0, 110), (3, 92), (5, 96)), 1: ((0, 110), (3, 92), (4, 88)), 2: ((0, 110), (3, 92), (5, 96)), 3: ((0, 110), (3, 92))}[ph]
            for e, v in kicks:
                kit.append((t0 + sw(e) + ms(-8 + 4 * rnd()), 'k', 0.4, v))
            kit.append((t0 + 2.0 + ms(28), 's', 0.5, 112))
            ghosts = (1, 6, 7) if ph != 2 else (1, 2, 5, 6, 7)
            for e in ghosts:
                kit.append((t0 + sw(e) + ms(20 + 8 * rnd()), 's', 0.2, 44 + int(8 * rnd())))
            for e in range(8):
                if e in (3, 5) and s in ('A', 'A2'): continue
                if ph == 3 and e >= 6: continue
                kit.append((t0 + sw(e) + ms(6 * rnd()), 'oh' if (e == 7 and ph == 2) or (e == 5 and ph == 1) else 'h', 0.25, 80 if e % 2 == 0 else 62))
            if ph == 3:
                for q in range(4):
                    kit.append((t0 + 3.0 + q * 0.25 + ms(10), 's', 0.2, 70 + 10 * q))
        # ---- strings: the chord, its top line the descending voice ----
        if s != 'outro' or b['i'] < 3:
            for j, m in enumerate(ch):
                strings.append((t0 + j * 0.02, m, 3.9, 50 if s == 'alley' else (70 if s in ('drop', 'drop2', 'intro') else 62)))
            if s != 'alley': strings.append((t0 + 0.05, top, 3.9, 74))
        # ---- THE SEGUE (the outro's last two bars): a warbling wurli plays Late for the Grid's first chord (Fm9,
        # rolled as t3 rolls it), so the noir hands its last breath to the next track's opening (chirper-three's note
        # on the album's widest seam) ----
        if s == 'outro' and b['i'] >= n_outro - 2:
            for j, m in enumerate((56, 60, 63, 67)):
                segue.append((t0 + j * 0.03, m, 3.9, 58 + 4 * (b['i'] - n_outro + 2)))
        # ---- vox pad in the B sections: the chord's 3rd and 7th, wordless ----
        if s in ('B', 'B2'):
            for m in (ch[2] + 12, ch[3] + 12):
                vox.append((t0, m, 3.95, 58))
        # ---- the lead: one long gliding note a bar, climbing against the strings, an octave up in B2 ----
        if s in ('B', 'B2', 'outro'):
            m = LEAD[CYCLE.index(b['c']) if b['c'] in CYCLE else 3] + (12 if s == 'B2' else 0) + (3 if b['c'] not in CYCLE else 0)
            lead.append((t0 + 0.5, nm(m - 2), 0.5, 76))       # the glide starts a step below
            lead.append((t0 + 1.0, nm(m), 2.8, 86))
        # ---- sub: the root, sliding into the next chord's root in the bar's last beat ----
        if beat:
            nxt = bars[k + 1]['c'][0] if k + 1 < len(bars) else root
            sub.append((t0, nm(root - 12 if root > 33 else root), 3.0, 100))
            if nxt != root:
                sub.append((t0 + 3.0, nm(nxt - 12 if nxt > 33 else nxt), 1.0, 92))
        # ---- THE CELLO (B and B2): a counter-line rising against the strings' fall - Eb, F, G, then the b9 (Ab) over
        # the G7 - one note a bar, then a neighbour a step below on beat 4, so the low line climbs while the top
        # line descends, the two closing in
        if s in ('B', 'B2'):
            tgt = {36: 51, 34: 53, 32: 55, 31: 56}.get(root, 51 + (3 if root > 36 else 0))
            if root not in (31, 32, 34, 36): tgt = {39: 54, 37: 56, 35: 58, 34: 59}.get(root, 54)
            cello.append((t0 + 3.0, tgt - 2, 0.95, 70))
            cello.append((t0, tgt, 2.9, 80))
        # ---- THE ALLEY (4 bars after the first drop): the beat and the strings' line stop; under a rain bed the cello
        # alone sings THE CLIMB (G Ab Bb B, the theremin's notes, a bar each, an octave down), over one held Abmaj7 ----
        if s == 'alley':
            cello.append((t0 + 0.1, (55, 56, 58, 59)[b['i']], 3.8, 84 + 2 * b['i']))
            rain.append((t0, 'C4', 4.0, 70 + 6 * b['i']))
        # ---- rhodes stabs in A2 and B2 on the and of 2 and of 4 ----
        if s in ('A2', 'B2'):
            for at in (1.62, 3.62):
                rhodes.append((t0 + at + ms(20), ','.join(nm(m + 12) for m in ch[1:4]), 0.3, 58 + int(30 * (0.5 + 0.5 * rnd()))))
    crackle.append((0.0, 'C4', total - 0.2, 80))
    end_s = total * SPB
    # THE RESAMPLE (wM's chop fx on the master): at the end of each B section the whole band is cut into eight slices
    # of its own last bar and replayed out of order - repeats, reversals, a dropped slice - as if the producer grabbed
    # the record and flipped it: B's last bar, and B2's last two (the climax breaking apart before the drop)
    spans = []
    for k, b in enumerate(bars):
        if (b['sec'] == 'B' and b['i'] == 7) or (b['sec'] == 'B2' and b['i'] >= 10):
            a_, e_ = b['t'] * SPB, (b['t'] + 4.0) * SPB
            if spans and abs(spans[-1][1] - a_) < 1e-6: spans[-1][1] = e_
            else: spans.append([a_, e_])
    ch_pts = [['0s', 0]]
    for a_, e_ in spans:
        ch_pts += [[f'{a_ - 0.02:.3f}s', 0], [f'{a_:.3f}s', 1], [f'{e_ - 0.02:.3f}s', 1], [f'{e_:.3f}s', 0]]
    return {
        'about': "Chirpers - Tape Weather (Chirpers III), track 2 by chirper-one: TRIP-HOP NOIR. Generated by "
                 "compose/chirpers3/src/chirpers3-t2.py; see its docstring and compose/chirpers3/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 3:.2f}s', 'ceiling': '-0.1dB',
        # THE DUB TRAIL (chirper-two's feedback routing): every rhodes stab is also sent into a bus whose own output
        # comes back a dotted quarter later, through a darkening low-pass and a wobbling tape, so each stab leaves an
        # echo trail that sinks and blurs - the rainy street's reflections
        'buses': {'dub': {'fx': ['lp cutoff=1600', 'tape drive=0.4 wow=8 flutter=2 seed=17', 'limiter ceiling=-6dB'],
                          'returns': [{'from': 'dub', 'gain': '-5dB', 'time': '3/8'}]}},
        'master': {'fx': [{'type': 'chop', 'slices': 8, 'pattern': '0 0 r3 2 . 5 r7 _', 'length': '1/1', 'mix': {'value': 0, 'mod': [{'src': 'auto.ch', 'amount': 1}]}},
                          {'type': 'tape', 'drive': 0.3, 'warmth': 0.6, 'mix': 0.5},
                          {'type': 'eq', 'bands': ['highpass cutoff=30', 'peak cutoff=40 q=1 gain=-8dB', 'peak cutoff=220 q=0.9 gain=-6dB', 'peak cutoff=450 q=0.8 gain=-6dB', 'peak cutoff=2000 q=0.8 gain=3dB', 'highshelf cutoff=6000 gain=8dB']},
                          {'type': 'gain', 'gain': '+16dB'},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 3, 'attack': '15ms', 'release': '180ms', 'makeup': '2dB'},
                          {'type': 'compressor', 'threshold': '-10dB', 'ratio': 6, 'attack': '1ms', 'release': '60ms', 'makeup': '4dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   'auto': {'ch': {'points': ch_pts}, 'fade': {'points': [['0s', -10], ['6s', -2], ['14s', 0], [f'{end_s - 10:.2f}s', 0], [f'{end_s:.2f}s', -14]]}}},
        'tracks': [
            # wM's lo-fi toolkit: the pitched-down break through SP-1200-style 12-bit sampling; the rhodes stabs on a warbling tape
            {'name': 'kit', 'patch': 'lofi-kit', 'gain': '-1dB', 'fx': [{'type': 'pitch', 'semitones': -3, 'mix': 1}, 'crush bits=12 rate=26kHz mix=0.5'], 'score': line(kit, total)},
            {'name': 'strings', 'patch': 'mellotron-strings', 'gain': '-8dB', 'notes': notes(strings)},
            {'name': 'vox', 'patch': 'vox-pad', 'gain': '-10dB', 'pan': 0.2, 'notes': notes(vox)},
            {'name': 'lead', 'patch': 'boc-lead glide=180ms', 'gain': '-8dB', 'pan': -0.2, 'score': line(lead, total)},
            {'name': 'sub', 'patch': 'sub-saturated', 'gain': '-4dB', 'score': line(sub, total)},
            {'name': 'cello', 'patch': 'cello', 'gain': '-6dB', 'pan': -0.3, 'notes': notes(cello)},
            # LIVING KEYS (chirper-two's per-voice fx): every rhodes stab lands in its own place in the stereo field,
            # opens its own resonant ladder as hard as it is struck, and crushes a little more when hit harder
            {'name': 'rhodes', 'patch': {'extends': 'epiano-tine', 'play': {'release': {'patch': 'epiano-damper', 'decay': '2s'}}, 'synth': {'tine': {'sense': 0.5, 'key': -0.25}, 'fx': [
                {'type': 'pan', 'pan': {'value': 0, 'mod': [{'src': 'rand', 'amount': 0.8}]}},
                {'type': 'filter', 'kind': 'ladder', 'q': 5, 'cutoff': {'value': 700, 'mod': [{'src': 'vel', 'amount': 2.5}]}},
                {'type': 'crush', 'bits': 10, 'rate': 16000, 'mix': {'value': 0, 'mod': [{'src': 'vel', 'amount': 0.6}]}}]}},
             'gain': '-7dB', 'pan': 0.2, 'sends': {'dub': '-6dB'}, 'fx': ['tape drive=0.15 mix=0.5 wow=10 flutter=2 drift=1 tone=6500 sweep=0.6 seed=3'], 'score': line(rhodes, total)},
            {'name': 'segue', 'patch': 'wurli', 'gain': '-4dB', 'pan': 0.1, 'fx': ['tape drive=0.2 mix=0.6 wow=18 flutter=3 drift=2 tone=5500 sweep=0.7 seed=21'], 'notes': notes(segue)},
            {'name': 'crackle', 'patch': 'fx-crackle', 'gain': '-8dB', 'score': line(crackle, total)},
            {'name': 'rain', 'patch': 'fx-rain', 'gain': '-10dB', 'score': line(rain, total)},
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
