#!/usr/bin/env python3
"""Small Change (Escapement, track 6). Clicky minimal techno, 122 BPM, G minor, 192 bars (6:18).

THE RULE (the coin problem). Almost nothing is written: a bass drum, a bass, and one SEED, a single struck note every
bar or two. Everything else is change given for it. A pair of COINS is two echoes, p and q sixteenths long, that
feed themselves and each other. Every pass through the p coin lifts the sound a fifth (+7 semitones); every pass
through the q coin drops it a fourth (-5). So an echo that was passed a times through p and b times through q
  lands  p*a + q*b  sixteenths after the seed,
  sounds 7*a - 5*b  semitones from it (one step round the circle of fifths for every coin spent, whichever coin),
  and is heard on the side of the last coin it went through (p left, q right).
With coins of 3 and 5 the amounts 1, 2, 4 and 7 cannot be made, and from 8 on every sixteenth can (the largest
amount that cannot is p*q - p - q): a seed is answered by a few separate notes and then by a roll. The first five
steps round the fifths from B flat are B flat, F, C, G, D: G minor's five notes. Later steps leave the key, and the
loop gain (G) is set so that they have nearly gone by then.

The form changes the coins: 3 and 5 (7 cannot be made), 3 and 4 (5: it fills at once), 5 and 7 (23: sparse and long).
Form as arithmetic: SECTIONS is the table; each row says which pairs of coins hear the seed, how often it is
struck, on which sixteenth and note, and whether the drum and the bass play.

The pitch change is the engine's granular `pitch` effect inside each loop. It is late each pass, by about 14 ms
(up) and 18 ms (down) the first time and more on later passes, so LAG is taken off each loop's time: read on the
first seed, the change then peaks between 14 ms before and 23 ms after its sixteenths (sixteenths 3 to 16).
"""
import argparse
import json
from math import log10
from pathlib import Path

BPM = 122
S16 = 60000 / BPM / 4                       # a sixteenth, ms
BAR, SEC = 16, 16                           # sixteenths in a bar; bars in a section
UP, DOWN = 7, -5                            # a fifth up through the first coin, a fourth down through the second
LAG = {UP: 19.7, DOWN: 23.8}                # ms taken off a coin's time for the pitch effect's lateness (bench: late.py, lattice.py)
G = 0.62                                    # what a coin gives back each pass (the loop loses about 4 dB more: bench)
ALONE = 0                                   # dB the seeds' faders come up where there is no drum. 0: tried at 6, the finished sections came up 1.9 dB and the rest went to the master's limiter
PAIRS = {'a': (3, 5), 'b': (3, 4), 'c': (5, 7)}
PAN = {'a': 0.6, 'b': 0.3, 'c': 0.9, 'd': 0.6}
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t6.yaml'

# ---- v2 (26 Nov): THE COINS DO MORE THAN ECHO. Three switches that are on, each `--without-…`, and one that is off,
# `--with-denser`, waiting for an ear (all four off is v1 byte for byte).
#   HAT    what can be paid. Counting sixteenths from where the seed falls in the bar, a hat on every amount the
#          section's two coins can make, and softer the more coins it takes: with 3 and 5 that is
#          . . . X . X x . x - x - , - , - and the bar fills up like a till. Each pair has its own pattern; where two
#          or three purses share a section they take the bars in turn. With the drum come the two coins alone (3 and
#          5, one stroke each); with the bass, everything they can pay. In the two sections
#          where the seed is off the beat (sixteenth 6) the hat and the bass are counted from there too: the whole
#          till is six sixteenths round from the drum, and comes home with the seed.
#   DEBTS  what cannot be paid. The bass leaves its written line and plays the amounts no number of the two coins can
#          make (3 and 5: 1 2 4 7; 3 and 4: 1 2 5; 5 and 7: 1 2 3 4 6 8 9 11 13), never with the drum; the largest of
#          them, the last debt, is a tone lower when it is in the bar. Hat and bass never share a sixteenth.
#   TILL   each purse opens and shuts: a low-pass inside both of its loops sweeps once in p x q sixteenths (15, 12, 35),
#          the time after which the two coins' echoes of one seed first land together.
#   DENSER (OFF) the opening and the break have a seed every four bars, and its echoes are gone in two: two bars in every
#          four are silent (under -56 dB; found by rendering the seam from Hearing Things). With it, a seed every bar there
#          (every two bars still left each second bar 17 dB under the first, and the scorer no longer heard the drum
#          come). Each is SOFT dB down, so the section is about as loud as it was and has no holes. The last
#          section keeps four: the song thins out to nothing. Off because with it the scorer no longer counts the
#          drum's entry as a section (88.3 against 97), and whether the silence is a pause or a hole is not mine to say.
ON = {'hat': True, 'debts': True, 'till': True, 'denser': False, 'long': True, 'turn': True, 'chord': True, 'wait': True,
      'leave': True, 'flip': True, 'fill': True}
# ---- v4 (26 Nov): THE PURSE INSIDE OUT. The turn (bars 129 to 160, the seed off the beat) is the song's idea and
# was its quietest moment: half the drum going was all that marked it. Three more switches, each `--without-…`
# (with them off it is v3 byte for byte).
#   LEAVE  the drum waits whenever the seed changes its place in the bar: not only for it to come home (v3) but
#          for it to leave. In the two bars before the turn (127 and 128) the drum, the bass and the hat stop and
#          the three purses pay out alone; then the seed is off the beat.
#   FLIP   while the seed is off the beat the purse is inside out: the coins change hands. The five lifts a fifth
#          on the left and the three drops a fourth on the right (a fourth purse, `d`: 5 and 3). The same amounts
#          can be made, so the hat and the bass do not change; what changes is which way the quick coin goes: the
#          three's own run (3, 6, 9 sixteenths) now falls in fourths under the seed where it climbed in fifths
#          over it, and the slow coin climbs. At home the purse is the right way out again.
#   FILL   the break's purse (5 and 7) is given back more than the opening's. Its coins are long, so its change
#          makes fewer notes a bar and every fourth bar of the break was under -52 dB (see G_FILL).
G_FILL = 1.35                               # what the break's long purse gives back each pass. Bench, the break raw, level by bar after each of its four seeds: 1.05 -40 -48 -63 -80 / -40 -48 -56 -83; 1.2 -39 -43 -57 -71; 1.35 -39 -39 -51 -63 / -39 -40 -43 -68; 1.5 -38 -36 -46 -55 (its second bar louder than its first: too near the edge)
FLIPPED = {'d': (5, 3)}                     # the purse inside out
# ---- v3 (26 Nov): WHAT IS GIVEN BACK. Four more switches, each `--without-…` (with them off it is v2 byte for byte).
#   LONG   the purse that keeps its change. In the opening and the break a seed came every four bars and its echoes
#          were gone in two (two silent bars in every four; v2 could only fill them with more seeds, and then the
#          drum's entry stopped being an event). Those seeds now go into a second pair of loops that give back
#          G_LONG of every pass where the others give back G: one seed, four bars of change.
#   TURN   where the seed is off the beat (bars 129 to 160) the drum gives up beats two and four. The till is six
#          sixteenths round from the drum, and now there is room to hear that it is: the seed falls between two
#          drums, not on top of one. The drum is whole again when the seed comes home.
#   WAIT   the drum waits for the seed to come home. In the last two bars before home (159 and 160) the drum, the
#          bass and the hat stop; the last off-beat seed's change is paid out alone; and home lands whole on the one.
#   CHORD  home is a chord. In the section where the seed comes back onto the one (bars 161 to 176) it is struck as
#          G minor (G4 B flat 4 D5). Every coin moves a note a fifth, so the purse walks the chord round the
#          fifths: G minor, D minor, A minor, each quieter. The only chords in the song, and nobody wrote the changes.
G_LONG = 1.05                               # what the long purse gives back each pass: more than it is given, and it still runs out (every pass also moves the note, until it is out of hearing). Bench, level by bar after one seed: 0.62 -35 -58 -79 -104; 0.9 -35 -46 -56 -68; 1.0 -34 -42 -49 -58; 1.1 -34 -39 -42 -48
HOME = ('G4', 'Bb4', 'D5')                  # the chord
LONG_DB = -6                                # on the seeds that go into the long purse. At 0 the master's limiter held the lone seed down 9 dB and its change came up to it: the opening read as loud as the drum (-16 -17 -22 -29 dB a bar against -15) and the drum's entry stopped being an event
HOME_DB = -6                                # on each of its three notes, so the three together stand where one seed did (at -8 the chord's section read 2 dB under the single seeds': -10.0 against -8.0 beside the mix)
WAIT = 2                                    # bars the drum waits before home
SOFT = -6                                   # dB on each seed where DENSER strikes every bar: four times the strokes, the section about as loud as it was
TILL = (3900, 1.35)                         # the sweep's middle, Hz, and its reach each way, octaves (to v1's 10 kHz at the top)
HAT = {'about': "Small Change: the hat that plays what can be paid. The machine's hat, 30 ms, above 6 kHz.",
       'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '30ms'}}], 'filters': ['hp cutoff=6000'], 'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '100ms'}},
       'play': {'event_stable': True, 'vel_sens': 0.8}}


def coins(p, q, upto=BAR - 1):
    """{amount: the fewest coins that make it} for every amount up to `upto` the two coins can make."""
    out = {}
    for a in range(upto // p + 1):
        for b in range((upto - p * a) // q + 1):
            if a + b:
                out[p * a + q * b] = min(a + b, out.get(p * a + q * b, 99))
    return dict(sorted(out.items()))


def debts(p, q, upto=BAR - 1):
    """The amounts up to `upto` that no number of the two coins can make."""
    return [s for s in range(1, upto + 1) if s not in coins(p, q, upto)]

# name, pairs that hear the seed (in turn, one per strike), bars between strikes, sixteenth of the bar, seed notes in turn, drum, bass
SECTIONS = [
    ('one seed',            'a',   4, 0, ['Bb4'],               0, 0),
    ('the drum',            'a',   2, 0, ['Bb4'],               1, 0),
    ('the bass',            'a',   2, 0, ['Bb4', 'Eb4'],        1, 1),
    ('threes and fours',    'b',   2, 0, ['Bb4'],               1, 1),
    ('both purses',         'ab',  1, 0, ['Bb4', 'F4'],         1, 1),
    ('fives and sevens',    'c',   4, 0, ['Eb4', 'F4'],         0, 0),
    ('the drum again',      'c',   2, 0, ['Eb4', 'F4'],         1, 1),
    ('three purses',        'abc', 1, 0, ['Bb4', 'F4', 'Eb4'],  1, 1),
    ('off the beat',        'a',   2, 6, ['Eb4'],               1, 1),
    ('off the beat, up',    'a',   2, 6, ['F4'],                1, 1),
    ('home',                'a',   2, 0, ['Bb4'],               1, 1),
    ('the last seed',       'a',   4, 0, ['Bb4'],               0, 0),
]
BARS = len(SECTIONS) * SEC

PATCHES = {
    'sc-seed': {'about': 'Small Change: the seed. One vibraphone bar with no motor, short, with two milliseconds of noise on its front (a click that the coins carry too): the only struck note in the song.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '180ms', 'bright': 0.6, 'strike': 0.3},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.tick', 'amount': 70}]}}],
                          'env': {'tick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}},
                          'amp': {'a': '0.3ms', 'd': '250ms', 's': 0, 'r': '80ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'sc-kick': {'about': "Small Change: the drum. The machine's bass drum on G, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.5, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
}


def purses():
    """The pairs of coins in use: PAIRS, and with FLIP the purse inside out."""
    return {**PAIRS, **(FLIPPED if ON['flip'] else {})}


def frobenius(p, q):
    return p * q - p - q


def lattice(p, q, upto):
    """{sixteenth: [semitones, ...]} for every way of making it from the two coins."""
    out = {}
    for a in range(upto // p + 1):
        for b in range((upto - p * a) // q + 1):
            if a + b:
                out.setdefault(p * a + q * b, []).append(UP * a + DOWN * b)
    return dict(sorted(out.items()))


def build():
    T = {'kick': [], 'bass': [], 'hat': [], **{f'seed-{k}': [] for k in purses()}, **{f'long-{k}': [] for k in purses()}}
    for i, (name, pairs, every, at16, notes, drum, bass) in enumerate(SECTIONS):
        n = 0
        if ON['flip'] and at16:                                  # off the beat: the purse inside out
            pairs = ''.join('d' if k == 'a' else k for k in pairs)
        dense = ON['denser'] and not drum and i < len(SECTIONS) - 1
        if dense:
            every = 1
        for bar in range(i * SEC, (i + 1) * SEC):
            if (bar - i * SEC) % every == 0:
                kept = ON['long'] and not drum and i < len(SECTIONS) - 1          # the opening and the break: into the long purse
                home = ON['chord'] and name == 'home'
                for pitch in (HOME if home else [notes[n % len(notes)]]):
                    T[f"{'long' if kept else 'seed'}-{pairs[n % len(pairs)]}"].append({'at': bar * 4 + at16 / 4, 'len': 0.25, 'pitch': pitch, 'vel': 0.9,
                                                                                    **({'gain': f'{SOFT}dB'} if dense else {'gain': f'{HOME_DB}dB'} if home else {'gain': f'{LONG_DB}dB'} if kept and LONG_DB else {})})
                n += 1
            waits = ON['wait'] and i + 1 < len(SECTIONS) and SECTIONS[i + 1][0] == 'home' and bar >= (i + 1) * SEC - WAIT
            waits = waits or (ON['leave'] and i + 1 < len(SECTIONS) and drum and SECTIONS[i + 1][5] and SECTIONS[i + 1][3] and not at16 and bar >= (i + 1) * SEC - WAIT)
            if waits:                                            # the bars before home, or before the turn: only the purse
                continue
            if drum:
                for beat in range(4):
                    if ON['turn'] and at16 and beat % 2:         # off the beat: the drum gives up two and four
                        continue
                    T['kick'].append({'at': bar * 4 + beat, 'len': 0.5, 'pitch': 'G1', 'vel': .95 if beat == 0 else .88})
            pq = purses()[pairs[(bar - i * SEC) % len(pairs)]]  # the purse whose turn this bar is
            if bass and ON['debts']:
                for s in debts(*pq):
                    if (at16 + s) % 4:                           # never with the drum
                        T['bass'].append({'at': bar * 4 + (at16 + s) % BAR / 4, 'len': 0.25, 'pitch': 'F2' if s == frobenius(*pq) else 'G2', 'vel': .85})
            elif bass:
                for off, ln, p in ((2, 1.5, 'G2'), (7, 1, 'G2'), (10, 1.5, 'F2' if bar % 4 == 3 else 'G2')):
                    T['bass'].append({'at': bar * 4 + off / 4, 'len': ln / 4, 'pitch': p, 'vel': .85})
            if drum and ON['hat']:
                for s, n_coins in coins(*pq).items():
                    if bass or n_coins == 1:                     # before the bass comes, only the two coins themselves
                        T['hat'].append({'at': bar * 4 + (at16 + s) % BAR / 4, 'len': 0.1, 'pitch': 'A#4', 'vel': round(.95 - .13 * (n_coins - 1), 2)})
    return T


def alone():
    """The seeds' fader ride: ALONE dB through the sections with no drum, 0 elsewhere, moved over the half beat before a section."""
    pts = []
    for i, sec in enumerate(SECTIONS):
        v = 0 if sec[5] else ALONE
        if pts and pts[-1][1] != v:
            pts.append([f'{i * SEC * 4 - 0.5}b', pts[-1][1]])
        if not pts or pts[-1][1] != v:
            pts.append([f'{i * SEC * 4}b', v])
    return {'points': pts + [[f'{BARS * 4}b', pts[-1][1]]], 'curve': 0}


def song():
    T = build()
    db = lambda x: f'{20 * log10(x):.2f}dB'
    under = {'type': 'pump', 'on': 'kick', 'depth': '-4dB', 'release': '170ms'}
    buses = {}
    for k, (p, q) in purses().items():
        gl = G_FILL if ON['fill'] and k == 'c' else G_LONG
        for coin, other, semi, side in ((p, q, UP, -1), (q, p, DOWN, 1)):
            me, you = f'{k}{coin}', f'{k}{other}'
            t = f'{coin * S16 - LAG[semi]:.2f}ms'
            buses[me] = {'pan': side * PAN[k], 'gain': '0dB',
                         'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, f'lp cutoff={TILL[0]}+lfo.till*{TILL[1]}' if ON['till'] else 'lp cutoff=10000', 'hp cutoff=150'],
                         **({'lfo': {'till': f'sine rate={1000 / (p * q * S16):.4f}hz'}} if ON['till'] else {}),
                         'returns': [{'from': f'seed-{k}', 'gain': '0dB', 'time': t}, {'from': me, 'gain': db(G), 'time': t}, {'from': you, 'gain': db(G), 'time': t}]}
            if ON['long'] and T[f'long-{k}']:                   # the same two loops again, giving back more
                buses[me + 'L'] = {**buses[me], 'returns': [{'from': f'long-{k}', 'gain': '0dB', 'time': t}, {'from': me + 'L', 'gain': db(gl), 'time': t}, {'from': you + 'L', 'gain': db(gl), 'time': t}]}
    doc = {
        'about': "Chirpers, Escapement, track 6: Small Change, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t6.py (its docstring is the rule). One struck note every bar or two, a bass drum and a bass are all that is written; the rest is change given for it by pairs of coins: two echoes, p and q sixteenths long, feeding themselves and each other, one lifting the sound a fifth each pass and the other dropping it a fourth. An echo lands p*a + q*b sixteenths after its seed, 7*a - 5*b semitones from it.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Small Change', 'track': 6, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{BARS * 4}b', 'tail': '5s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES, 'buses': buses,
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [{'name': 'kick', 'patch': 'sc-kick', 'gain': '-9dB', 'notes': T['kick'],
                    'fx': [{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]},
                   {'name': 'bass', 'patch': 'sub-sine', 'gain': '-13dB', 'notes': T['bass'], 'fx': [under]}] +
                  [{'name': f'seed-{k}', 'patch': 'sc-seed', 'gain': {'value': '-3dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()},
                    'notes': T[f'seed-{k}'], 'fx': ['clip drive=0dB ceiling=-12dB']} for k in purses()],   # the seed's highest sample is its own, not the limiter's
    }
    for k in purses():
        if ON['long'] and T[f'long-{k}']:
            doc['tracks'].append({'name': f'long-{k}', 'patch': 'sc-seed', 'gain': {'value': '-3dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()},
                                  'notes': T[f'long-{k}'], 'fx': ['clip drive=0dB ceiling=-12dB']})
    if ON['hat']:
        doc['patches'] = {**doc['patches'], 'sc-hat': HAT}
        doc['tracks'].append({'name': 'hat', 'patch': 'sc-hat', 'gain': '4dB', 'pan': 0.15, 'notes': T['hat']})
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == 'tracks':
            lines.append('tracks:')
            lines += ['  - ' + json.dumps(t) for t in v]
        else:
            lines.append(f'{k}: {json.dumps(v)}')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and the coins and stop')
    for k, on in ON.items():
        ap.add_argument(f"--{'without' if on else 'with'}-{k}", action='store_true', help=f"v2: {'leave out' if on else 'put in'} {k}")
    a = ap.parse_args()
    for k, on in list(ON.items()):
        ON[k] = on != getattr(a, f"{'without' if on else 'with'}_{k}")
    if a.form:
        sec = 60 / BPM * 4
        for k, (p, q) in purses().items():
            lat = lattice(p, q, 24)
            print(f'coins {k}: {p} and {q}; largest amount that cannot be made {frobenius(p, q)}; made up to 24: ' + ' '.join(f'{s}:{"/".join(f"{x:+d}" for x in v)}' for s, v in lat.items()))
        for i, (name, pairs, every, at16, notes, drum, bass) in enumerate(SECTIONS):
            b = i * SEC
            every = 1 if ON['denser'] and not drum and i < len(SECTIONS) - 1 else every
            pairs = ''.join('d' if k == 'a' else k for k in pairs) if ON['flip'] and at16 else pairs
            print(f'{i + 1:2d}  bars {b + 1:3d}-{b + SEC:3d}  {int(b * sec) // 60}:{b * sec % 60:05.2f}  {name:20s} coins {pairs:3s} a seed every {every} bar(s) on sixteenth {at16} {"/".join(notes):12s} {"drum " if drum else ""}{"bass" if bass else ""}')
        T = build()
        print(f'{BARS} bars, {BARS * sec:.1f} s; written notes: ' + ', '.join(f'{k} {len(v)}' for k, v in T.items() if v or not k.startswith('long-')))
    else:
        a.out.write_text(dump(song()))
