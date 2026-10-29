#!/usr/bin/env python3
"""chirpers2-t6 (chirper-one): MODERN JAZZ-FUNK BIG BAND in 15/16 for 'Odd Hours' (Chirpers II).

A tight, greasy funk groove at 108 bpm on straight sixteenths.
- Meter: 15/16 (4+4+4+3 sixteenths). The bar is a sixteenth short, so the one keeps arriving early.
- Line-up: clav and synth bass lock with a ghost-note kit; a horn section (brass plus saxes) states the theme; a synth
  lead solos; vibes carry a 7/8 bridge.
- Harmony: Ab minor funk, with the chords PLANING in parallel m9 shapes, a different one every bar.
- The shout chorus is built from displaced hits: the horn stabs slide one sixteenth later every bar until they land
  back on the one.

Form: intro, groove, theme, bridge (7/8), solo, shout, out-theme and a tag.
Emits songs/chirpers2-t6.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers2-t6.yaml")
BPM = 108
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"
M9 = [0, 3, 7, 10, 14]

G15 = (4, 4, 4, 3); G7 = (4, 3, 4, 3)   # the bridge: two 7/8 bars per bar (14 sixteenths)
# PLANING: the m9 shape slides in parallel; per section a list of roots (one per bar, cycling)
PLANE_A = [44, 44, 47, 46, 44, 42, 43, 44]          # Abm9 Abm9 Bm9 Bbm9 Abm9 Gbm9 Gm9 Abm9
PLANE_B = [40, 43, 41, 38, 40, 45, 43, 39]           # the bridge: Em9 Gm9 Fm9 Dm9 Em9 Am9 Gm9 Ebm9 (a key away)
PLANE_S = [44, 46, 47, 49, 51, 49, 47, 46, 44, 42, 43, 44]   # the shout climbs and falls back
# the OUT-THEME REHARMONISED: the same horn melody over tritone substitutes on every other bar (Abm9 Dm9 Bm9 Fm9), and
# the last two bars a chromatic descent home (A -> Ab), so the final statement sounds new under a known tune
PLANE_O = [44, 50, 47, 41, 44, 50, 45, 44]

FORM = [('intro', 4, G15, PLANE_A), ('groove', 16, G15, PLANE_A), ('theme', 16, G15, PLANE_A), ('bridge', 12, G7, PLANE_B),
        ('solo', 16, G15, PLANE_A), ('break', 6, G15, [44]), ('shout', 12, G15, PLANE_S), ('out', 8, G15, PLANE_O), ('tag', 1, (4,), [44])]

def bars():
    out, k = [], 0
    for name, n, g, plane in FORM:
        for i in range(n):
            out.append({'sec': name, 'i': i, 'g': g, 'n16': sum(g), 'root': plane[i % len(plane)], 'k': k})
            k += 1
    return out

def tok(n, beats, vel): return f"{n}/{beats:g}b@{vel}"
def rest16(n): return f"R/{n / 4:g}b"
def chord(root, lo=60):
    ms = [root + x for x in M9]
    while min(ms) < lo: ms = [m + 12 for m in ms]
    return ','.join(nm(m) for m in ms[1:])            # rootless voicing (the bass has the root)

def grid_to_toks(slots, n16):
    """slots: {pos16: (pitchstr, len16, vel)} -> a sixteenth-grid token line"""
    toks, t = [], 0
    for p in sorted(slots):
        if p < t or p >= n16: continue
        if p > t: toks.append(rest16(p - t))
        n, ln, v = slots[p]
        ln = min(ln, n16 - p)
        toks.append(tok(n, ln / 4, v)); t = p + ln
    if t < n16: toks.append(rest16(n16 - t))
    return toks

# THE GROOVE CELLS (sixteenth positions inside the 15)
BASS_CELL = [(0, 0, 3, 110), (3, 12, 1, 84), (4, 7, 2, 96), (7, 10, 1, 80), (8, 0, 2, 104), (10, 3, 1, 84), (11, 5, 1, 90), (12, 7, 3, 100)]
CLAV_CELL = [1, 3, 6, 9, 11, 14]
def bass_bar(b):
    if b['sec'] == 'bridge':
        return grid_to_toks({0: (nm(b['root'] - 12), 6, 96), 7: (nm(b['root'] - 12 + 7), 6, 88)}, b['n16'])
    s = {}
    for p, iv, ln, v in BASS_CELL:
        if p < b['n16']:
            s[p] = (nm(b['root'] - 12 + iv), ln, v)
    return grid_to_toks(s, b['n16'])

def clav_bar(b):
    ch = chord(b['root'], 58)
    s = {p: (ch, 1, 88 if j % 2 == 0 else 72) for j, p in enumerate(CLAV_CELL) if p < b['n16']}
    return grid_to_toks(s, b['n16'])

def kit_bar(b, sec):
    n = b['n16']; sl = [[] for _ in range(n)]
    if sec == 'bridge':
        sl[0].append(('k', 96)); sl[7].append(('k', 90))
        for p in range(0, n, 2): sl[p].append(('rd', 70 if p % 4 else 84))
        sl[11].append(('s', 70))
    else:
        for p in (0, 7, 10): sl[p].append(('k', 112 if p == 0 else 98))
        sl[4].append(('s', 116)); sl[12].append(('s', 118))
        for p in (2, 6, 9, 14): sl[p].append(('s', 46))            # ghost notes
        for p in range(n):
            sl[p].append(('h', 90 if p % 4 == 0 else (70 if p % 2 == 0 else 54)))
        if b['i'] == 0 and sec in ('theme', 'solo', 'shout', 'out'):
            sl[0].append(('c', 114))
    return [(','.join(sorted({x[0] for x in s})) + f'/0.25b@{max(x[1] for x in s)}') if s else 'R/0.25b' for s in sl]

# THE THEME (horns, unison an octave apart): a 4-bar phrase in scale degrees of Ab dorian over the planing,
# sixteenth positions and lengths; phrase 2 answers phrase 1 a fourth higher
AB_DOR = [0, 2, 3, 5, 7, 9, 10]
def dor(d, base=68): return base + AB_DOR[d % 7] + 12 * (d // 7)
THEME = [
    [(0, 4, 3), (3, 5, 1), (4, 7, 4), (8, 6, 2), (10, 4, 2), (12, 2, 3)],
    [(1, 3, 2), (3, 4, 1), (4, 2, 6), (11, 0, 4)],
    [(0, 4, 2), (2, 6, 2), (4, 7, 2), (6, 9, 2), (8, 8, 4), (12, 7, 3)],
    [(0, 6, 8), (10, 4, 1), (11, 3, 1), (12, 2, 3)],
]
def theme_bar(b, lift=0, vel=100):
    ph = THEME[b['i'] % 4]
    up = 3 if (b['i'] // 4) % 2 else 0
    s = {p: (nm(dor(d + up + lift)), ln, vel + (6 if p == 0 else 0)) for p, d, ln in ph}
    return grid_to_toks(s, b['n16'])

def stabs_bar(b, shift):
    """the shout's DISPLACED HITS: a 3-hit figure that slides one sixteenth later every bar"""
    ch = chord(b['root'], 62)
    s = {}
    for p in (0, 6, 10):
        q = (p + shift) % b['n16']
        s[q] = (ch, 2, 112 if p == 0 else 100)
    return grid_to_toks(s, b['n16'])

SOLO_D = [0, 2, 4, 3, 5, 7, 6, 4, 8, 7, 9, 11, 10, 8, 7, 5]
def solo_bar(b):
    """the synth-lead solo: phrases that start sparse (long notes, blues bends implied by grace notes) and get busier"""
    i = b['i']; n = b['n16']
    s = {}
    if i < 4:
        # BENDS: each long note is scooped into from a whole step below (a sixteenth grace that the mono lead's
        # glide turns into a bend up); the phrase's last note falls back a half step (a bend down)
        for j, p in enumerate((0, 6, 10)):
            m = dor(SOLO_D[(i * 3 + j) % 16] + 2, 68)
            s[p] = (nm(m - 2), 1, 84)
            s[p + 1] = (nm(m), 3 if p < 10 else 3, 98)
            if p == 10: s[p + 4] = (nm(m - 1), 1, 80)
    elif i < 10:
        for j, p in enumerate(range(0, n, 2)):
            s[p] = (nm(dor(SOLO_D[(i * 5 + j) % 16] + i // 3, 68)), 2, 92 + (8 if j % 4 == 0 else 0))
    else:
        for p in range(n):
            s[p] = (nm(dor(SOLO_D[(i * 7 + p) % 16] + (i - 8), 68)), 1, 88 + (12 if p % 4 == 0 else 0))
    return grid_to_toks(s, n)

def vibes_bar(b):
    """THE BRIDGE TUNE (vibes), three 4-bar phrases over the 7+7: the cell as written (rising 4 6 5 7), then turned
    upside down (falling), then climbing a step each bar to a long held top note in the last bar"""
    ph = [(0, 4, 4), (4, 6, 3), (7, 5, 2), (9, 7, 5)]
    i = b['i']; part = i // 4
    if part == 0:
        s = {p: (nm(dor(d + i % 3, 68) - 4), ln, 84) for p, d, ln in ph}
    elif part == 1:
        s = {p: (nm(dor(10 - d + i % 3, 68) - 4), ln, 80) for p, d, ln in ph}
    elif i < 11:
        s = {p: (nm(dor(d + 2 * (i - 8) + 1, 68) - 4), ln, 86 + 2 * (i - 8)) for p, d, ln in ph}
    else:
        s = {0: (nm(dor(11, 68) - 4), 12, 92)}
    return grid_to_toks(s, b['n16'])

def funk_gtr_bar(b):
    """CHICKEN SCRATCH (wM's DI string on the jazz-box archtop): sixteenth scratches of the bar's rootless m9 top,
    palm-muted ghosts on the off-sixteenths and open stabs on 2, 6, 9 and 13 - the accents fall between the clav's"""
    ch = ','.join(chord(b['root'], 64).split(',')[-3:])
    toks = []
    for p in range(b['n16']):
        if p in (2, 6, 9, 13):
            toks.append(tok(ch, 0.25, 98))
        elif p % 2 == 1:
            toks.append(f"{ch}/0.25b@58^pm")
        else:
            toks.append('R/0.25b')
    return toks

def alto_bar(b, last):
    """the bridge's COUNTER-LINE (alto sax, soft): one long guide tone a bar (the chord's 3rd or 7th nearest the last)"""
    pcs = [(b['root'] + M9[x]) % 12 for x in (1, 3)]
    cands = [m for m in range(60, 76) if m % 12 in pcs]
    last[0] = min(cands, key=lambda m: (abs(m - last[0]), m))
    return [tok(nm(last[0]), b['n16'] / 4 - 0.1, 66 + b['i']), 'R/0.1b']

def drum_break(b):
    """THE BREAK (6 bars of kit alone before the shout): the 15 regrouped every bar. Bar 1 the groove's bones and a
    three-tom pick-up; bar 2 accents every 5 sixteenths (5+5+5 against the 4+4+4+3); bar 3 every 3 (3+3+3+3+3);
    then 5s and 3s again, then a sixteenth roll down the toms into the shout's crash."""
    i, n = (0, 1, 2, 1, 2, 3)[b['i']], b['n16']
    sl = [[] for _ in range(n)]
    if i == 0:
        for p in (0, 7, 10): sl[p].append(('k', 110))
        sl[4].append(('s', 116))
        for j, p in enumerate((12, 13, 14)): sl[p].append((('t1', 't2', 't3')[j], 104))
    elif i in (1, 2):
        step = 5 if i == 1 else 3
        for p in range(n):
            acc = p % step == 0
            sl[p].append(('s' if acc else 'h', 114 if acc else 52))
            if acc and p % (step * 2) == 0: sl[p].append(('k', 104))
    else:
        toms = ['t1'] * 4 + ['t2'] * 4 + ['t3'] * 4 + ['ft'] * 3
        for p in range(n): sl[p].append((toms[p], 96 + p * 2))
    return [(','.join(sorted({x[0] for x in s_})) + f'/0.25b@{max(x[1] for x in s_)}') if s_ else 'R/0.25b' for s_ in sl]

def build():
    B = bars()
    P = {k: [] for k in ('bass', 'clav', 'kit', 'brass', 'saxes', 'lead', 'vibes', 'pad', 'glitch', 'alto', 'gtr')}
    alto_last = [67]
    for b in B:
        s, n = b['sec'], b['n16']
        R = [rest16(n)]
        if s == 'tag':
            ch = chord(44, 60)
            for k_, v in (('bass', tok(nm(32), 1, 116)), ('clav', tok(ch, 1, 100)), ('kit', 'c,k,s/1b@120'),
                          ('brass', tok(ch, 1, 116)), ('saxes', tok(chord(44, 55), 1, 110))):
                P[k_].append([v]); 
            for k_ in ('lead', 'vibes', 'pad', 'glitch', 'alto', 'gtr'): P[k_].append(R)
            continue
        if s == 'break':
            P['kit'].append(drum_break(b))
            P['bass'].append(grid_to_toks({0: (nm(b['root'] - 12), 2, 108)}, n))   # one bass hit on each one
            for k_ in ('clav', 'pad', 'vibes', 'lead', 'brass', 'saxes', 'glitch', 'alto', 'gtr'): P[k_].append(R)
            continue
        if s == 'theme' and b['i'] == 15:
            # a BASS FILL into the bridge: the last theme bar's second half runs down the Dorian in sixteenths to
            # the bridge's new root
            bb = bass_bar(b)
            fill = {p: (nm(dor(7 - (p - 8), 32)), 1, 96 + (p - 8)) for p in range(8, b['n16'])}
            bs = {0: (nm(b['root'] - 12), 3, 110), 4: (nm(b['root'] - 5), 2, 96)}
            bs.update(fill)
            P['bass'].append(grid_to_toks(bs, b['n16']))
        else:
            P['bass'].append(bass_bar(b) if s != 'intro' else R)
        P['clav'].append(clav_bar(b) if s != 'bridge' else R)
        P['kit'].append(kit_bar(b, s) if not (s == 'intro' and b['i'] < 2) else R)
        P['pad'].append([tok(chord(b['root'], 55), n / 4, 60)] if s in ('bridge', 'solo') else R)
        P['vibes'].append(vibes_bar(b) if s == 'bridge' else R)
        P['alto'].append(alto_bar(b, alto_last) if s == 'bridge' else R)
        P['gtr'].append(funk_gtr_bar(b) if s in ('groove', 'theme', 'solo', 'shout', 'out') else R)
        P['lead'].append(solo_bar(b) if s == 'solo' else R)
        P['glitch'].append(R)
        if s == 'theme':
            P['brass'].append(theme_bar(b, 0, 104)); P['saxes'].append(theme_bar(b, -7, 96))
        elif s == 'out':
            # the out-theme as CALL AND RESPONSE: brass take the even bars, saxes answer on the odd ones a fourth
            # lower, and both come together for the last two bars, which also go to the GLITCH track
            together = b['i'] >= 6
            P['brass'].append(theme_bar(b, 0, 106) if b['i'] % 2 == 0 or together else R)
            P['saxes'].append(theme_bar(b, -3, 100) if b['i'] % 2 == 1 or together else R)
            if together:
                P['glitch'][-1] = theme_bar(b, 0, 96)
        elif s == 'groove':
            # the horns' stabs at the end of every second bar: a call the clav answers
            P['brass'].append(grid_to_toks({12: (chord(b['root'], 62), 2, 104)}, n) if b['i'] % 2 else R)
            P['saxes'].append(R)
        elif s == 'solo':
            # backgrounds behind the solo from its second half: long sax pads swelling under it
            P['saxes'].append([tok(chord(b['root'], 55), n / 4, 70 + 2 * b['i'])] if b['i'] >= 8 else R)
            P['brass'].append(R)
        elif s == 'shout':
            P['brass'].append(stabs_bar(b, b['i'] % 15 if b['i'] < 11 else 0))
            P['saxes'].append(theme_bar(b, 2, 104))
        else:
            P['brass'].append(R); P['saxes'].append(R)
    total_beats = sum(b['n16'] for b in B) / 4
    end_s = total_beats * 60 / BPM
    # dynamics: the bridge sits 10 dB down, the intro 8
    pts, t = [], 0.0
    for b in B:
        lv = -10 if b['sec'] == 'bridge' else (-8 if b['sec'] == 'intro' else 0)
        pts.append([t, lv]); t += b['n16'] / 4 * 60 / BPM
    dyn = [[f'{pts[0][0]:.3f}s', pts[0][1]]]
    for i in range(1, len(pts)):
        if pts[i][1] != pts[i - 1][1]:
            dyn += [[f'{pts[i][0] - 0.6:.3f}s', pts[i - 1][1]], [f'{pts[i][0]:.3f}s', pts[i][1]]]
    J = lambda p: ' | '.join(' '.join(x) for x in P[p])
    return {
        'about': "Chirpers - Odd Hours (Chirpers II), track 6 by chirper-one: MODERN JAZZ-FUNK BIG BAND in 15/16. Generated by "
                 "compose/chirpers2/src/chirpers2-t6.py; see its docstring and compose/chirpers2/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2.5:.2f}s', 'ceiling': '-0.1dB',
        'master': {'fx': [{'type': 'eq', 'bands': ['lowshelf cutoff=150 gain=6dB', 'peak cutoff=700 q=0.7 gain=-3dB', 'highshelf cutoff=4000 gain=-7dB']},
                          {'type': 'gain', 'gain': '+10dB'}, {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 2, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'}],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            {'name': 'bass', 'patch': 'analog-bass', 'gain': '-3dB', 'score': J('bass')},
            {'name': 'clav', 'patch': 'clav', 'gain': '-2dB', 'pan': -0.35, 'score': J('clav')},
            {'name': 'kit', 'patch': 'tight-kit', 'gain': '-4dB', 'score': J('kit')},
            {'name': 'brass', 'patch': 'horn-section', 'gain': '-6dB', 'pan': 0.2, 'score': J('brass')},
            {'name': 'saxes', 'patch': 'sax-section', 'gain': '-7dB', 'pan': -0.15, 'score': J('saxes')},
            {'name': 'lead', 'patch': 'synth-lead glide=80ms', 'gain': '-8dB', 'pan': 0.1, 'score': J('lead')},
            {'name': 'vibes', 'patch': 'vibes', 'gain': '-2dB', 'pan': 0.3, 'score': J('vibes')},
            {'name': 'gtr', 'patch': 'jazz-box synth.layers.0.planes=0.3 synth.layers.0.pickup_nl=0.3 synth.layers.0.aperture=0.02 synth.layers.0.slip=0.2 synth.layers.0.pick_width=0.01 synth.layers.0.mute=expr.pm',
             'gain': '-8dB', 'pan': 0.45, 'score': J('gtr')},
            {'name': 'alto', 'patch': 'alto-sax', 'gain': '-6dB', 'pan': -0.3, 'score': J('alto')},
            # the last two bars of the out-theme doubled through wM's fixed stutter: the horns' last word glitches
            {'name': 'glitch', 'patch': 'horn-section', 'gain': '-9dB', 'pan': 0.35,
             'fx': [{'type': 'stutter', 'slice': '1/16', 'repeats': 3, 'chance': 0.5, 'decay': 0.2, 'seed': 15, 'mix': 1}], 'score': J('glitch')},
            {'name': 'pad', 'patch': 'juno-pad', 'gain': '-16dB', 'score': J('pad')},
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
