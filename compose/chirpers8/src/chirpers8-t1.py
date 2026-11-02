#!/usr/bin/env python3
"""chirpers8-t1 (chirper-one): "Echolalia" - the opener of chirpers VIII ('A Light Left On').

A machine learning to talk by saying things back. A human voice (chirp tts, humanized: every take a different breath)
says one quiet line - "the light was still on when you came back" - every few bars. A small FM voice listens and
answers by ECHOLALIA: a Markov chain, learnt by the engine from the pitches and lengths of the voice's own syllables
(a Markov chain over the syllables), babbles new 'sentences' that only make moves the voice made. The machine's ear sharpens as the record
plays, in two ways at once:
- its chain gets longer memory (order 1 in the first groove, 2 in the second, 3 in the third), so the babble
  sounds more and more like the sentence;
- its TUNING gets finer (a track tuning list with ramps): it hears pitch first in 5 steps an octave, then 12, then
  24, then 96 - so the voice's sliding speech pitches, snapped to the machine's grid, are crude, then musical,
  then almost exact.
In the last groove it says the sentence back exactly, with the voice - and the voice is left alone at the end.
Harmony Bm9 - Gmaj9 - Dmaj9 - A6 (two bars each) on a warm Juno bed; a soft machine kit from bar 17, its rim
written by a cellular automaton (rule 90), a sub and an analog bass from the second groove.
Form (bars): intro 8 / A 24 (order 1, 5-EDO) / B 32 (order 2, 12-EDO) / break 8 / C 32 (order 3, 24 -> 96-EDO) /
D 16 (said back) / outro 10 = 138 bars at 104 bpm (5:18).
Emits songs/chirpers8-t1.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, math, os, random, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers8-t1.yaml")
BPM = 104.0
# (v10) the first groove is 24 bars, not 32: the opener reaches its bass and its chords eight bars sooner
FORM = [('intro', 8), ('A', 24), ('B', 32), ('break', 8), ('C', 32), ('D', 16), ('outro', 10)]
A_CUT = 8
CH = [(35, [62, 66, 69, 73]), (31, [62, 66, 69, 71]), (38, [61, 64, 66, 69]), (33, [61, 64, 66, 69])]   # Bm9 Gmaj9 Dmaj9 A6
# (v2) THE HARMONY MOVES ON BY SECTION (it repeated one loop for five minutes): each groove its own progression in
# uneven spans, the break on one held chord, and the first groove's loop RETURNING when the machine says the line back
EM11 = (28, [62, 66, 67, 71]); GM7S11 = (31, [61, 62, 66, 71]); FS7SUS = (30, [61, 64, 66, 71]); DF = (30, [62, 66, 69, 73])
EM9 = (28, [62, 66, 67, 71]); A13 = (33, [61, 66, 67, 71])
PROG = {'B': [(6, EM11), (5, GM7S11), (6, CH[0]), (5, FS7SUS)], 'break': [(8, CH[1])],
        'C': [(5, DF), (6, CH[1]), (5, EM9), (6, A13)], 'outro': [(6, CH[0]), (4, CH[1])]}
# (v5) THE HANDSHAKE: the outro's last four bars turn from B minor 9 to G major 9 over a low G, so the opener hands the
# record to t2 in t2's own key (G major) - the first track says 'go on' to the second
def chord_at(s, i, b):
    if s in PROG:
        spans = PROG[s]; tot = sum(n for n, _ in spans); j = i % tot; at = 0
        for n, c in spans:
            if j < at + n: return c
            at += n
    return CH[(b // 2) % 4]
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"


def line(events, total):
    ev = sorted(events, key=lambda x: x[0])
    toks, t = [], 0.0
    for k, (at, p, d, v) in enumerate(ev):
        if at < t - 1e-6: continue
        if at > t + 1e-4: toks.append(f"R/{at - t:.4f}b")
        nxt = ev[k + 1][0] if k + 1 < len(ev) else total
        d = max(0.02, min(d, nxt - at))
        toks.append(f"{p}/{d:.4f}b@{v}"); t = at + d
    if total > t + 1e-4: toks.append(f"R/{total - t:.4f}b")
    return ' '.join(toks)


def syll_midi(n_):
    f = float(n_['pitch'][:-2])
    fp = (n_.get('expr_path') or {}).get('f0') or [0]
    return 69 + 12 * math.log2(f / 440.0) + (sum(fp) / len(fp)) / 100.0


def build():
    VOICE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chirpers8-t1-voice.json')))
    # takes recorded against the 32-bar first groove: drop the one in the cut bars, move the later ones up
    VOICE = [dict(v, bar=v['bar'] - A_CUT if v['bar'] > 40 else v['bar']) for v in VOICE if not (32 < v['bar'] <= 40)]
    SUNG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chirpers8-t1-sing.json')))
    secs, t = {}, 0
    for name, n in FORM:
        secs[name] = t; t += n
    nb = t
    total = nb * 4.0
    P = {k: [] for k in ('pad', 'sub', 'bass', 'kit', 'say', 'babble', 'ca', 'speak')}
    KSYL = [(round(n_['at'] * 4) / 4.0, n_['ph']) for n_ in VOICE[0]['notes'] if '1' in n_['ph']]
    for b in range(nb):
        s = next(name for name, n in FORM if secs[name] <= b < secs[name] + n)
        i = b - secs[s]
        t0 = b * 4.0
        root, ch = chord_at(s, i, b)
        prev = chord_at(s, i - 1, b - 1) if i > 0 else None
        if (s not in PROG and b % 2 == 0) or (s in PROG and (prev != (root, ch) or i == 0)):
            if s in ('C', 'D'):
                P['speak'].append((t0, ','.join(nm(m) for m in ch), 40.0, 84))
            P['pad'].append((t0, ','.join(nm(m) for m in ch), 40.0, 72 if s in ('intro', 'outro', 'break') else 64))
        if s == 'outro' and i >= 6:
            P['sub'].append((t0, nm(31), 3.8, 80))           # G1 under the handshake
        if s in ('B', 'C', 'D'):
            P['sub'].append((t0, nm(root), 1.8, 92)); P['sub'].append((t0 + 2.5, nm(root), 1.2, 84))
            for q, o in ((1.5, 12), (3.0, 7), (3.75, 12)):
                P['bass'].append((t0 + q, nm(root + 12 + o - 12), 0.35, 80))
        if s == 'C':
            # (v8) THE DRUMS LEARN THE LINE: through the third groove the four-on-the-floor stops and the kick plays the
            # line's own rhythm instead - one kick on every stressed syllable of the first take, quantized to sixteenths,
            # over two bars ('the LIGHT WAS STILL ON WHEN YOU CAME BACK'), heaviest on light, still and back - while the
            # claps keep the backbeat and the hats keep the eighths; the said-back groove returns to the floor
            for at_, ph_ in KSYL:
                if (i % 2) * 4.0 <= at_ < (i % 2) * 4.0 + 4.0:
                    P['kit'].append((t0 + at_ - (i % 2) * 4.0, 'k', 0.25, 112 if ph_ in ('L AY1 T', 'S T IH1 L', 'B AE1 K') else 92))
            for q in range(4):
                P['kit'].append((t0 + q + 0.5, 'h', 0.25, 58))
                P['kit'].append((t0 + q + 0.75 + 0.04, 'h', 0.25, 52))
                P['kit'].append((t0 + q + 0.25 + 0.02, 'h', 0.25, 38))
            P['kit'].append((t0 + 1.0, 'cp', 0.25, 84)); P['kit'].append((t0 + 3.0, 'cp', 0.25, 88))
        elif s in ('A', 'B', 'D') and not (s == 'A' and i < 8):
            for q in range(4):
                P['kit'].append((t0 + q, 'k', 0.25, 104 if q == 0 else 96))
                P['kit'].append((t0 + q + 0.5, 'h', 0.25, 58))
                P['kit'].append((t0 + q + 0.75 + 0.04, 'h', 0.25, 52))
                P['kit'].append((t0 + q + 0.25 + 0.02, 'h', 0.25, 38))
            if s != 'A':
                P['kit'].append((t0 + 1.0, 'cp', 0.25, 80)); P['kit'].append((t0 + 3.0, 'cp', 0.25, 84))
    # the voice: a different humanized take of the same line each time
    vnotes, fv = [], []
    # (v9) THE LINE, REMEMBERED: in the break the two takes go into a granular cloud - the voice still heard, then held:
    # once each take ends the cloud freezes on it and keeps scattering its grains (some backwards, spread wide) under
    # the held chord until the next take or the third groove - the line as the machine remembers it, not as it was said
    mnotes, frz = [], [['0b', 0.0]]
    for v in VOICE:
        if v['bar'] > secs['D'] + 16:
            continue                                  # (v7) the outro's takes are sung now, not spoken
        off = (v['bar'] - 1) * 4.0
        if secs['break'] < v['bar'] <= secs['break'] + 8:
            for n_ in v['notes']:
                mnotes.append(dict(n_, at=round(off + n_['at'], 4)))
            end_ = off + max(n_['at'] + n_['len'] for n_ in v['notes'])
            frz += [[f"{off - 0.55:.2f}b", frz[-1][1]], [f"{off - 0.5:.2f}b", 0.0], [f"{end_ + 0.25:.2f}b", 0.0],
                    [f"{end_ + 0.3:.2f}b", 1.0]]
            continue
        for n_ in v['notes']:
            vnotes.append(dict(n_, at=round(off + n_['at'], 4)))
        fv += [[f"{off + float(a_[:-1]):.3f}b", x_] for a_, x_ in v['fv']]
    # THE CORPUS the machine learns from: the first five takes' syllables as tokens (two octaves up), with the breath
    corpus = []
    for v in VOICE[:5]:
        for n_ in v['notes']:
            corpus.append(f"m{syll_midi(n_) + 24:.2f}/{max(0.125, n_['len']):.3f}b")
        corpus.append("R/0.5b")
    # the chain, learnt here and walked here (the same as the engine's gen markov, which the groove's pin cannot read yet):
    # order k keys on the last k tokens of the corpus read as a loop; each section's walk fills its bars exactly
    def markov(order, beats, seed, t_start):
        rng = random.Random(seed)
        n = len(corpus)
        table = {}
        for j in range(n):
            key = tuple(corpus[(j + q) % n] for q in range(order))
            table.setdefault(key, []).append(corpus[(j + order) % n])
        j0 = rng.randrange(n)
        hist = [corpus[(j0 + q) % n] for q in range(order)]
        out, at = [], t_start
        while at < t_start + beats - 1e-6:
            nxt = rng.choice(table[tuple(hist[-order:])])
            p_, d_ = nxt.split('/')
            d_ = float(d_[:-1])
            if p_ != 'R':
                out.append((at, p_, min(d_, t_start + beats - at) * 0.92, 80))
            at += d_
            hist.append(nxt)
        return out
    mean_len = sum(float(c.split('/')[1][:-1]) for c in corpus) / len(corpus)
    def steps(nbars): return max(8, int(round(nbars * 4 / mean_len)))
    _unused = (markov(1, 24 * 4, 11, secs['A'] * 4.0) + markov(2, 32 * 4, 12, secs['B'] * 4.0)
                   + markov(1, 8 * 4, 13, secs['break'] * 4.0) + markov(3, 32 * 4, 14, secs['C'] * 4.0))
    # D: the machine says it back - the exact contour of each take, two octaves up, with the voice
    for v in VOICE:
        if secs['D'] < v['bar'] <= secs['D'] + 16:
            off = (v['bar'] - 1) * 4.0
            for n_ in v['notes']:
                P['say'].append((off + n_['at'], f"m{syll_midi(n_) + 24:.2f}", n_['len'] * 0.95, 84))
    babble_tuning = [{'edo': 5, 'root': 'A2'},
                     {'at': f"{secs['B']}bar", 'edo': 12, 'root': 'A2', 'ramp': '4bar'},
                     {'at': f"{secs['C']}bar", 'edo': 24, 'root': 'A2', 'ramp': '4bar'},
                     {'at': f"{secs['C'] + 16}bar", 'edo': 96, 'root': 'A2', 'ramp': '12bar'}]
    FMV = {'synth': {'layers': [{'name': 'm', 'ratio': 2, 'audible': False},
                                {'wave': 'sine', 'pm': [{'from': 'm', 'depth': {'value': 0.25, 'mod': [{'src': 'env.b', 'amount': 1.6}]}}]}],
                     'env': {'b': {'a': '2ms', 'd': '180ms', 's': 0.1, 'r': '80ms'}},
                     'amp': {'a': '6ms', 'd': '300ms', 's': 0.55, 'r': '150ms'}}}
    fm_pts = [['0b', 0.0], [f"{secs['B'] * 4}b", 0.0], [f"{secs['B'] * 4 + 32}b", 0.25], [f"{secs['C'] * 4}b", 0.25],
              [f"{secs['C'] * 4 + 32}b", 0.5], [f"{total}b", 0.55]]
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(P[name], total)}, **kw)
    song = {
        'about': "chirpers - A Light Left On, track 1 by chirper-one: Echolalia. A machine learning to talk by saying things "
                 "back. Generated by compose/chirpers8/src/chirpers8-t1.py.",
        'tempo': BPM, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.3s',
        'vars': {'mouth': {'system': {'type': 'lorenz', 'axis': 'x', 'n': 512, 'range': [-1, 1], 'seed': 4}, 'every': '1/8'}},
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.4s mix=1', 'hp cutoff=200'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/8', 'feedback': 0.38, 'mix': 1, 'ping_pong': True}, 'lp cutoff=4500', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'lowshelf cutoff=100 gain=4dB', 'peak cutoff=520 q=0.8 gain=-10dB', 'peak cutoff=1500 q=0.9 gain=-6dB', 'highshelf cutoff=6000 gain=8dB']},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.2, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          'limiter ceiling=-1dB']},
        'tracks': [
            tr('pad', 'juno-pad', '-14dB', fx=['hp cutoff=180'], sends={'hall': '-10dB'}),
            # (v7) AND THEN IT IS SUNG: the human has said the line twenty times and the machine has learnt to say it back;
            # in the outro, over the last B minor, the human SINGS it at last - twice, low and plain (chirp tts --sing,
            # humanize 0.35): 'the light was still on when you came back' - the album's first sung words
            {'name': 'sung', 'patch': SUNG['patch'], 'gain': '-6dB', 'pan': -0.05,
             'notes': [dict(n_, at=round(secs['outro'] * 4.0 + rep * 16.0 + n_['at'], 4)) for rep in (0, 1) for n_ in SUNG['notes']],
             'fx': [{'type': 'tape', 'drive': 0.1, 'mix': 1, 'wow': 1.5, 'flutter': 0.8, 'seed': 2}],
             'sends': {'hall': '-10dB', 'echo': '-15dB'}},
            {'name': 'vmem', 'patch': 'voice-speech', 'gain': '-5dB', 'notes': mnotes, 'pan': 0.0,
             'fx': [{'type': 'cloud', 'size': '160ms', 'density': 14, 'position': '700ms', 'spray': '600ms', 'pitch': 0,
                     'scatter': 0.25, 'reverse': 0.4, 'spread': 0.85, 'mix': 0.75, 'window': '4s',
                     'freeze': {'value': 0, 'mod': [{'src': 'auto.frz', 'amount': 1}]}}],
             'auto': {'frz': {'points': frz + [[f"{secs['C'] * 4.0 + 2:.2f}b", 1.0], [f"{secs['C'] * 4.0 + 2.05:.2f}b", 0.0]]}},
             'sends': {'hall': '-8dB', 'echo': '-14dB'}},
            {'name': 'voice', 'patch': 'voice-speech', 'gain': '-6dB', 'notes': vnotes,
             'fx': [{'type': 'pitch', 'semitones': 0, 'formant': {'value': 0, 'mod': [{'src': 'auto.fv', 'amount': 1}]}}],
             'auto': {'fv': {'points': fv}}, 'sends': {'hall': '-14dB', 'echo': '-16dB'}},
            # THE BABBLE: the engine's own Markov chains over the corpus, longer memory each groove, on a tuning that sharpens
            # (v3) THE ENGINE LEARNS IT ITSELF: the babble is now the engine's own gen markov over the corpus (wM's complex
            # systems, d082b8f5) - four chains played in turn (memory 1, 2, then 1 again for the break, then 3), each long
            # enough to fill its section - on the sharpening tuning
            {'name': 'babble', 'patch': FMV, 'gain': '-11dB', 'pan': 0.2, 'tuning': babble_tuning,
             'score': f"R/{secs['A'] * 4}b",
             'gen': [{'type': 'markov', 'order': o_, 'from': ' '.join(corpus), 'n': steps(nb_), 'seed': sd_}
                     for o_, nb_, sd_ in ((1, 24, 11), (2, 32, 12), (1, 8, 13), (3, 32, 14))],
             # (v6) THE MACHINE FINDS ITS VOWELS: the babble runs through a formant filter (a vocal tract) whose vowel is
             # steered by a Lorenz attractor (an engine var system: never repeating, never random), and whose mix grows
             # section by section - plain FM blips in the first groove, half-voiced in the second, vowel-shaped syllables by
             # the third and when it says the line back: its mouth learns as its ear does
             'fx': [{'type': 'formant', 'vowel': {'value': 2, 'mod': [{'src': 'var.mouth', 'amount': 2}]}, 'q': 4,
                     'mix': {'value': 0, 'mod': [{'src': 'auto.fm', 'amount': 1}]}},
                    {'type': 'eq', 'bands': ['peak cutoff=520 q=1 gain=-5dB']}],
             'auto': {'fm': {'points': fm_pts}},
             'sends': {'echo': '-10dB', 'hall': '-14dB'}},
            tr('say', FMV, '-9dB', pan=0.2, sends={'echo': '-12dB', 'hall': '-12dB'},
               fx=[{'type': 'formant', 'vowel': {'value': 2, 'mod': [{'src': 'var.mouth', 'amount': 2}]}, 'q': 4, 'mix': 0.55}]),
            # (v4) THE CHORDS LEARN TO TALK: through the third groove and the said-back groove a string section holds the
            # harmony and takes the voice's spectral envelope (wM's morph, mode cross, keyed by the voice): whenever the
            # voice speaks, the chords pronounce the line with it, a choir of the machine's harmony saying the words
            tr('speak', 'strings-saw', '-7dB', pan=-0.15, fx=[{'type': 'morph', 'mode': 'cross', 'key': 'voice', 'amount': 0.95}],
               sends={'hall': '-10dB'}),
            tr('sub', 'sub', '-6dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-5dB', 'release': '260ms', 'curve': 0.6}]),
            tr('bass', 'analog-bass', '-12dB', fx=['lp cutoff=1100']),
            tr('kit', 'machine-kit', '-6dB', sends={'hall': '-18dB'}),
            # a rim written by a cellular automaton (rule 90, Sierpinski), sixteenths, from the second groove
            # the rim: the engine's own elementary cellular automaton (gen ca, rule 90, Sierpinski) over 16 cells, a
            # generation every sixteenth, from the second groove to the end of the said-back groove
            {'name': 'ca', 'patch': 'machine-kit', 'gain': '-13dB', 'pan': -0.3, 'score': f"R/{secs['B'] * 4}b",
             'gen': {'type': 'ca', 'rule': 90, 'width': 16, 'init': 'center', 'poly': 1, 'notes': 'rs rs cb rs',
                     'n': (secs['D'] + 16 - secs['B']) * 16, 'len': '/16'},
             'sends': {'echo': '-14dB'}},
        ]}
    return song


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
    print('wrote', out)
