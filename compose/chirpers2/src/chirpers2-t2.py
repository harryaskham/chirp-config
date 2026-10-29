#!/usr/bin/env python3
"""chirpers2-t2 (chirper-one): ELECTRIC NIGHT-GROOVE for 'Odd Hours' (Chirpers II).

Dark electric-Miles-ish modal funk. The band is the groove, and the soloists ride it.
- METER WHEEL: bar lengths turn 4/4, 7/8, 5/4, 9/8, 3/4 (8, 7, 10, 9, 6 eighths) and never stop; phrases are 4 bars, so
  phrase and meter realign every 20 bars. The climax stretches the wheel to 11/8, 13/8.
- Roots by section: D Dorian (A), Eb Lydian (B), F# Phrygian dominant (trades), back to D.
- Every bar another voice carries the vamp's cell (bass always; then rhodes, wah, trumpet, tenor in rotation).
Emits songs/chirpers2-t2.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers2-t2.yaml")
BPM = 100
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"
WHEEL = [8, 7, 10, 9, 6]                 # eighths per bar
STRETCH = [11, 13, 11, 13, 9]
# the orchestration wheel's doublings (intro/break/outro): on since v5 (with v3's sub and no harmonic wheel they broke
# the returns, recurrence 100 -> 31; with the harmonic wheel the returns hold)
WHEEL_DOUBLES = True
# HARMONIC RHYTHM (bar by bar): the vamp's chord moves every bar inside the mode, an 7-bar cycle against the 5-bar wheel
# and the 4-bar phrases (scale degrees from the section's root; the bass cell, the rhodes and the sub follow it)
PROG = {'dorian': [0, 3, 0, 6, 4, 3, 1], 'lydian': [0, 1, 0, 4, 2, 1, 5], 'phrygdom': [0, 1, 0, 6, 5, 1, 3]}
# chirper-two's tom choir from Palindrome for Brushes and Toms (t4): physical toms (drum layer, tune_sounding)
TOM_CHOIR = {'synth': {'layers': [{'type': 'drum', 'beater': 'stick', 'contact': 1.5, 'decay': '1.1s', 'sharp': 35, 'reso': 1.0, 'cavity': 0.25, 'tune_sounding': True, 'reso_level': 0.5, 'air': 0.45, 'strike': 0.3, 'shell': 0.25, 'slap': 0.5, 'stereo': 0.5}], 'filters': ['hp cutoff=60'], 'amp': {'a': '0.3ms', 'd': '1.4s', 's': 0, 'r': '120ms', 'curve': 3}}, 'play': {'vel_sens': 0.6}}

MODES = {'dorian': [0, 2, 3, 5, 7, 9, 10], 'lydian': [0, 2, 4, 6, 7, 9, 11], 'phrygdom': [0, 1, 4, 5, 7, 8, 10]}

# form: (name, bars, root midi (bass octave), mode, wheel)
FORM = [('intro', 10, 38, 'dorian', WHEEL), ('A', 20, 38, 'dorian', WHEEL), ('B', 20, 39, 'lydian', WHEEL),
        ('trades', 20, 42, 'phrygdom', WHEEL), ('break', 10, 38, 'dorian', WHEEL), ('climax', 15, 38, 'dorian', STRETCH),
        ('outro', 10, 38, 'dorian', WHEEL)]

def bars():
    out = []
    for name, n, root, mode, wheel in FORM:
        for i in range(n):
            out.append({'sec': name, 'i': i, 'n': n, 'root': root, 'mode': MODES[mode], 'e8': wheel[i % len(wheel)],
                        'cd': PROG[mode][i % len(PROG[mode])] if name != 'break' else 0})
    return out

def deg(b, d, octv=0):
    sc = b['mode']; return b['root'] + sc[d % 7] + 12 * (d // 7 + octv)

def tok(n, beats, vel, art=''):
    return f"{n}/{beats:g}b@{vel}{art}"

# ---- the parts ----
BASSCELL = [0, None, 4, 0, 6, None, 3, 4, 0, None, 2, 4, 6]   # degrees on eighths (None = rest), cut to the bar
def bass(b, k):
    toks = []
    for e in range(b['e8']):
        d = BASSCELL[(e + k) % len(BASSCELL)] if e else 0
        if d is None:
            toks.append('R/0.5b')
        else:
            toks.append(tok(nm(deg(b, d + b['cd'])), 0.5, 100 if e == 0 else 84))
    return toks

def kit(b, k, sec):
    sl = []
    for e in range(b['e8']):
        for half in (0, 1):
            p = []
            if half == 0 and (e == 0 or (e % 3 == 2 and sec not in ('intro',))):
                p.append(('k', 110 if e == 0 else 92))
            if half == 0 and e in (b['e8'] // 2, b['e8'] - 2) and sec != 'intro':
                p.append(('s', 104))
            if sec == 'B':          # the hats drop back to a whisper on the off-sixteenths: the rhodes solo floats
                p.append(('h', 48 if half else 80))
            elif sec == 'break':    # bass and kit alone: kick on one, hats on quarters
                p = [x for x in p if x[0] == 'k' and e == 0]
                if half == 0 and e % 2 == 0: p.append(('h', 76))
            else:
                p.append(('h', 70 if half else 84))
            if sec in ('climax',) and e == 0 and half == 0:
                p.append(('c', 110))
            sl.append(p)
    return [(','.join(sorted({x[0] for x in s})) + f'/0.25b@{max(x[1] for x in s)}') if s else 'R/0.25b' for s in sl]

def chord(b, top=0):
    return ','.join(nm(deg(b, d + b['cd'], 1) + 12) for d in (0, 2, 4, 6, 8)[top:top + 4])

def rhodes(b, k):
    e8 = b['e8']; toks = []
    hits = {1: 0, 4: 1, e8 - 2: 2}
    for e in range(e8):
        if e in hits:
            toks.append(tok(chord(b, hits[e] % 2), 0.5, 74))
        else:
            toks.append('R/0.5b')
    return toks

def wah(b, k):
    toks = []
    for e in range(b['e8'] * 2):
        if e % 4 in (1, 3) or e % 7 == 0:
            toks.append(tok(f"{nm(deg(b, 2, 1) + 12)},{nm(deg(b, 6, 1) + 12)}", 0.25, 64, '^pm' if e % 4 == 1 else ''))
        else:
            toks.append('R/0.25b')
    return toks

THEME = [4, 6, 7, 8, 7, 6, 4, 3, 2, 4]   # degrees, a rising-falling modal line
def rhodes_solo(b, vel):
    """THE RHODES SOLO (B, Eb Lydian over the harmonic wheel): 4-bar phrases that grow over the 20 bars.
    Bar 1 states a 3-note cell from the chord (with a chromatic approach from below), bar 2 sequences it a step up,
    bar 3 runs sixteenths up the mode, bar 4 lands on a long note (the #4, the Lydian colour, on the last phrase).
    Each phrase starts a third higher and the runs get longer: a solo that climbs and opens out."""
    i = b['i']; ph, pos = i // 4, i % 4
    base = 2 + 2 * ph + b['cd']              # degree the phrase starts on (a third higher each phrase)
    while base > 7: base -= 7                # kept in the solo's octave (G4-D6)
    e16 = b['e8'] * 2
    toks, t = [], 0
    def add(d, ln, v, chrom=0):
        nonlocal t
        ln = min(ln, e16 - t)
        if ln <= 0: return
        toks.append(tok(nm(deg(b, d, 2) + chrom), ln / 4, v)); t += ln
    if pos in (0, 1):
        c = base + pos                       # the sequence: a step up
        add(c, 1, vel - 10, chrom=-1)        # chromatic approach from below
        add(c, 2, vel + 6); add(c + 2, 2, vel); add(c + 4, 3, vel + 4)
        while t < e16:
            add(c + 2 if (t // 2) % 2 else c + 1, 2, vel - 8)
    elif pos == 2:
        d = base - 7 - (e16 // 2 - 4)        # start low enough that the run lands near where the phrase began
        while t < e16:                       # the run: sixteenths up the mode, longer each phrase
            add(d, 1, vel + (6 if t % 4 == 0 else -4)); d += 1
    else:
        land = 3 if ph == 4 else base + 4    # #4 (degree 3 in Lydian) on the last phrase
        add(land, max(4, e16 - 4), vel + 8)
        while t < e16:
            add(land - 1, 2, vel - 12)
    if t < e16:
        toks.append(f"R/{(e16 - t) / 4:g}b")
    return toks

def trade_call(b, n):
    """a trade: a 4-note chord cell (root 3rd 5th 7th order turned by n), entered from a semitone below, sequenced a
    step higher each trade; later trades fragment it (repeat its first two notes, rests between)"""
    e16 = b['e8'] * 2; toks, t = [], 0
    cell = [(0, 2, 4, 6), (2, 4, 6, 7), (4, 2, 0, 1), (6, 4, 2, 4), (1, 3, 5, 7)][n % 5]
    base = n
    frag = n >= 5
    seq = [cell[0], cell[1], cell[0], cell[1], cell[2]] if frag else list(cell)
    toks.append(tok(nm(deg(b, base + seq[0], 2) - 1), 0.25, 82)); t += 1
    for j, d in enumerate(seq):
        ln = 2 if j < len(seq) - 1 else 4
        if frag and j % 2 == 1: ln = 1
        if t + ln > e16: break
        toks.append(tok(nm(deg(b, base + d, 2)), ln / 4, 104 if j == 0 else 94)); t += ln
        if frag and j % 2 == 1 and t < e16:
            toks.append('R/0.25b'); t += 1
    if t < e16: toks.append(f"R/{(e16 - t) / 4:g}b")
    return toks

def trade_answer(b, call):
    """the answer: the call's notes mirrored around its first note, same rhythm, in the tenor's octave"""
    if not call: return rest(b)
    first = None; out = []; t = 0; e16 = b['e8'] * 2
    for x in call:
        n_, r_ = x.split('/', 1)
        ln = float(r_.split('b')[0])
        if n_ == 'R':
            out.append(f"R/{ln:g}b"); t += ln * 4; continue
        m_ = NN.index(n_[:-1]) + 12 * (int(n_[-1]) + 1)
        if first is None: first = m_
        if t + ln * 4 > e16: break
        out.append(f"{nm(2 * first - m_ - 12)}/{ln:g}b@{int(r_.split('@')[1]) - 6}"); t += ln * 4
    if t < e16: out.append(f"R/{(e16 - t) / 4:g}b")
    return out

def turnstile_head(b):
    """THE TURNSTILE HEAD (A): a composed 4-bar phrase that every bar of the meter wheel bends. The trumpet CLICKS
    three eighths and then HOLDS for whatever the bar has left - so in 7/8 the hold is short, in 5/4 it is long, and
    the same click lands differently every time the wheel turns. Bar 1 clicks up into the 9th, bar 2 answers down,
    bar 3 is bar 1 a third higher, bar 4 the tenor answers with the click inverted; under the trumpet's holds the
    tenor echoes the click's last two notes. Every second phrase the click sticks: it starts an eighth late."""
    i, e8 = b['i'], b['e8']
    pos, n = i % 4, i // 4
    late = 1 if n % 2 else 0
    c = b['cd']
    def notes(degs, hold, octv, vel, start):
        toks = []
        if start: toks.append(f"R/{start / 2:g}b")
        t = start
        for d in degs:
            toks.append(tok(nm(deg(b, c + d, octv)), 0.5, vel + (6 if d == degs[0] else 0))); t += 1
        if e8 - t > 0:
            toks.append(tok(nm(deg(b, c + hold, octv)), (e8 - t) / 2 - 0.1, vel - 4)); toks.append('R/0.1b')
        return toks
    if pos == 3:
        return rest(b), notes([4, 3, 1], 0, 1, 90, late)
    degs, hold = {0: ([4, 5, 7], 8), 1: ([7, 5, 4], 2), 2: ([6, 7, 9], 10)}[pos]
    tpt = notes(degs, hold, 2, 98, late)
    # the tenor's echo of the click's last two notes, in the hold's last two eighths, an octave down
    ten = [f"R/{(e8 - 2) / 2:g}b"] + [tok(nm(deg(b, c + d, 1)), 0.5, 78) for d in degs[1:]] if e8 - late - 3 >= 3 else rest(b)
    return tpt, ten

def horn_line(b, k, start_deg, vel):
    """a phrase across the bar: quarter-ish notes, the last one held"""
    toks, e8, j = [], b['e8'], 0
    t = 0
    while t < e8:
        ln = 3 if (t + 3 >= e8) else (2 if (k + j) % 3 else 1)
        ln = min(ln, e8 - t)
        d = THEME[(start_deg + j) % len(THEME)]
        toks.append(tok(nm(deg(b, d, 2)), ln / 2, vel))
        t += ln; j += 1
    return toks

def rest(b): return [f"R/{b['e8'] / 2:g}b"]

def build():
    B = bars()
    parts = {k: [] for k in ('bass', 'kit', 'rhodes', 'wah', 'tpt', 'ten', 'sub')}
    last_call = [None]
    for k, b in enumerate(B):
        sec = b['sec']; lead = k % 5   # who carries the cell this bar (beyond the bass)
        parts['bass'].append(bass(b, k) if sec != 'break' or b['i'] < 8 else bass(b, k))
        parts['kit'].append(kit(b, k, sec) if not (sec == 'intro' and b['i'] < 2) else rest(b))
        parts['rhodes'].append(rhodes(b, k) if (sec != 'intro' or b['i'] >= 5) and sec != 'break' else (rhodes(b, k) if sec == 'break' and b['i'] >= 6 else rest(b)))
        parts['wah'].append(wah(b, k) if sec in ('A', 'B', 'climax') or (sec == 'trades' and lead in (2, 4)) else rest(b))
        # SUB: the bar's root an octave under the fretless on the downbeat (the low end jazz-rock records keep under the bass)
        parts['sub'].append([tok(nm(deg(b, b['cd']) - 12 - (12 if deg(b, b['cd']) - b['root'] > 6 else 0)), min(1.5, b['e8'] / 2), 96), f"R/{b['e8'] / 2 - min(1.5, b['e8'] / 2):g}b"]
                            if sec != 'intro' or b['i'] >= 5 else rest(b))
        # ORCHESTRATION WHEEL: in the intro, the break and the outro the NIGHT CELL is doubled two octaves up by a
        # different voice every bar (none, rhodes, wah, tenor, trumpet), so no two consecutive bars sound alike
        if sec == 'A':
            t_, n_ = turnstile_head(b)
            parts['tpt'].append(t_); parts['ten'].append(n_)
        elif sec == 'B':   # the rhodes 'solos' (the cell climbs), horns lay out but for stabs
            parts['tpt'].append(rest(b)); parts['ten'].append(rest(b))
            parts['rhodes'][-1] = rhodes_solo(b, 86)
        elif sec == 'trades':   # trading bars: trumpet / tenor alternate
            if b['i'] < 2:
                # THE ANSWER: the trades open with the trumpet and tenor quoting the rhodes solo's last phrase
                # (its cell and the cell a step up), re-heard in F# Phrygian dominant, before trading their own bars
                q = dict(b, i=16 + b['i'])
                parts['tpt'].append(rhodes_solo(q, 100) if b['i'] == 0 else rest(b))
                parts['ten'].append(rhodes_solo(q, 94) if b['i'] == 1 else rest(b))
            else:
                # THE TRADES ARGUE: each trumpet bar takes the last idea and develops it (a 4-note cell from the
                # chord, sequenced a step higher each time and fragmented as the trades go on); each tenor bar answers
                # the trumpet's bar UPSIDE DOWN (mirrored around its first note), a bar of conversation each
                if b['i'] % 2 == 0:
                    line = trade_call(b, b['i'] // 2)
                    last_call[0] = line
                    parts['tpt'].append(line); parts['ten'].append(rest(b))
                else:
                    parts['tpt'].append(rest(b)); parts['ten'].append(trade_answer(b, last_call[0]))
        elif sec == 'climax':
            # THE CELL COMES HOME: over the stretched wheel the horns stop soloing and join the bass on the NIGHT
            # CELL in octaves (trumpet two octaves up, tenor one), every third bar breaking back out into the line,
            # so the climax is the whole band hammering the song's first idea
            if b['i'] % 3 == 2:
                parts['tpt'].append(horn_line(b, k, b['i'] + 2, 112))
                parts['ten'].append(horn_line(b, k, b['i'] + 6, 100))
            else:
                def up(cell, octs, v):
                    o_ = []
                    for x in cell:
                        if x.startswith('R'): o_.append(x); continue
                        n_, r_ = x.split('/', 1)
                        m_ = NN.index(n_[:-1]) + 12 * (int(n_[-1]) + 1) + 12 * octs
                        o_.append(f"{nm(m_)}/{r_.split('@')[0]}@{v}")
                    return o_
                parts['tpt'].append(up(bass(b, k), 2, 108))
                parts['ten'].append(up(bass(b, k), 1, 100))
        elif sec == 'outro':
            # HEAD OUT: the turnstile head's first phrase comes back over the unravelling band (trumpet and the
            # tenor's echoes), then the trumpet leaves with the others
            if b['i'] < 4:
                t_, n_ = turnstile_head(dict(b, i=b['i']))
                parts['tpt'].append(t_); parts['ten'].append(n_)
            else:
                parts['tpt'].append(rest(b)); parts['ten'].append(rest(b))
        else:
            parts['tpt'].append(rest(b)); parts['ten'].append(rest(b))
    total_beats = sum(b['e8'] for b in B) / 2
    # the doubling voices (built after, per voice, so each has its own track)
    for v in ('dr', 'dw', 'dt', 'dp'):
        parts[v] = []
    for k, b in enumerate(B):
        who = {1: 'dr', 2: 'dw', 3: 'dt', 4: 'dp'}.get(k % 5) if b['sec'] in ('intro', 'break', 'outro') else None
        cell = bass(b, k)
        up = []
        for x in cell:
            if x.startswith('R'):
                up.append(x)
            else:
                n_, rest_ = x.split('/', 1)
                m_ = NN.index(n_[:-1]) + 12 * (int(n_[-1]) + 1)
                up.append(f"{nm(m_ + 24)}/{rest_.split('@')[0]}@70")
        for v in ('dr', 'dw', 'dt', 'dp'):
            parts[v].append(up if v == who else rest(b))
    # THE UNRAVELLING (outro): the band leaves the vamp one voice every two bars - the wah, then the rhodes, then the
    # trumpet's line and the doublings, then the kit - until the fretless and the sub play the NIGHT CELL alone,
    # as the song began
    leave = [('wah',), ('rhodes',), ('tpt', 'ten', 'dr', 'dw', 'dt', 'dp'), ('kit',)]
    for k, b in enumerate(B):
        if b['sec'] == 'outro':
            for step, voices in enumerate(leave):
                if b['i'] >= 2 * (step + 1):
                    for v in voices:
                        parts[v][k] = rest(b)
    # THE TOM CHOIR ANSWERS (the break): chirper-two's Palindrome for Brushes and Toms (t4) plays this song's NIGHT
    # CELL through its bridge; here its tom choir (t4's singing physical toms, borrowed) sings t4's MIRROR MELODY
    # back over the bass and kit - its 3/4 cell (A G F E) and 5/8 cell (D E F), then both retrograde, the
    # palindrome's way - and in the break's second half the same a fourth up, as the rhodes comes back in
    parts['toms'] = []
    CELL_A = [('A3', 2), ('G3', 1), ('F3', 1), ('E3', 2)]; CELL_B = [('D4', 1), ('E4', 1), ('F4', 3)]
    def fit(notes, e8, up=0):
        o_, t_ = [], 0
        for n_, ln in notes:
            if t_ + ln > e8: break
            m_ = NN.index(n_[:-1]) + 12 * (int(n_[-1]) + 1) + up
            o_.append(f"{nm(m_)}/{ln / 2 - 0.05:g}b@84"); o_.append('R/0.05b'); t_ += ln
        if t_ < e8: o_.append(f"R/{(e8 - t_) / 2:g}b")
        return o_
    PLAN = [CELL_A, CELL_B, CELL_B[::-1], CELL_A[::-1], None]
    for k, b in enumerate(B):
        if b['sec'] == 'break':
            ph = PLAN[b['i'] % 5]
            parts['toms'].append(fit(ph, b['e8'], 5 if b['i'] >= 5 else 0) if ph else rest(b))
        else:
            parts['toms'].append(rest(b))
    end_s = total_beats * 60 / BPM
    J = lambda p: ' | '.join(' '.join(x) for x in parts[p])
    return {
        'about': "Chirpers - Odd Hours (Chirpers II), track 2 by chirper-one: ELECTRIC NIGHT-GROOVE. Generated by "
                 "compose/chirpers2/src/chirpers2-t2.py; see its docstring and compose/chirpers2/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 3:.2f}s', 'ceiling': '-0.1dB',
        'master': {'fx': [{'type': 'eq', 'bands': ['lowshelf cutoff=120 gain=6dB', 'peak cutoff=650 q=0.7 gain=-4dB', 'highshelf cutoff=8000 gain=-5dB']}, {'type': 'gain', 'gain': '+8dB'},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 2, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.fade', 'amount': 1}]}}],
                   'auto': {'fade': {'points': [['0s', 0], [f'{end_s - 14:.1f}s', 0], [f'{end_s:.1f}s', -40]]}}},
        'tracks': [
            {'name': 'bass', 'patch': 'fretless', 'gain': '0dB', 'score': J('bass')},
            {'name': 'kit', 'patch': 'tight-kit', 'gain': '-4dB', 'score': J('kit')},
            {'name': 'rhodes', 'patch': 'rhodes-rotary', 'gain': '-6dB', 'pan': -0.3,
             'fx': [{'type': 'amp', 'model': 'clean', 'stack': 'bassman', 'gain': 0.35, 'mix': 0.6}], 'score': J('rhodes')},
            {'name': 'wah', 'patch': 'lead-wah', 'gain': '-14dB', 'pan': 0.45, 'score': J('wah')},
            {'name': 'sub', 'patch': 'sub-saturated', 'gain': '-15dB', 'score': J('sub')},
            *([{'name': 'dr', 'patch': 'rhodes', 'gain': '-10dB', 'pan': -0.4, 'score': J('dr')},
               {'name': 'dw', 'patch': 'starcaster-clean', 'gain': '-12dB', 'pan': 0.5, 'score': J('dw')},
               {'name': 'dt', 'patch': 'tenor-sax-synth', 'gain': '-12dB', 'pan': -0.15, 'score': J('dt')},
               {'name': 'dp', 'patch': 'trumpet-mute', 'gain': '-12dB', 'pan': 0.2, 'score': J('dp')}] if WHEEL_DOUBLES else []),
            {'name': 'toms', 'patch': TOM_CHOIR, 'gain': '+8dB', 'pan': -0.05, 'fx': ['reverb kind=room decay=0.9s mix=0.15'], 'score': J('toms')},
            {'name': 'tpt', 'patch': 'trumpet-mute', 'gain': '-6dB', 'pan': 0.15, 'score': J('tpt')},
            {'name': 'ten', 'patch': 'tenor-sax-synth', 'gain': '-7dB', 'pan': -0.2, 'score': J('ten')},
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
