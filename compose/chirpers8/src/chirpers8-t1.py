#!/usr/bin/env python3
"""chirpers8-t1 (chirper-one): "Echolalia" - the opener of chirpers VIII ('A Light Left On').

A machine learning to talk by saying things back. A human voice (chirp tts, humanized: every take a different breath)
says one oblique line - "standby amber, the fan's long vowel" (v16, after Harry: fewer returns, oblique words, a tune
that is good to hear) - eight times, speaking at first and singing more each time. A small FM voice listens and
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
# (v13) NEUTRAL THIRDS: through the third groove - where the babble is in 24 and then 96 notes to the octave - the
# chords learn the quarter tones too: each chord's third is bent a quarter tone toward the middle (major thirds down,
# minor thirds up), so every chord is neither major nor minor, a third the twelve notes do not have; when the machine
# says the line back the first groove's plain chords return
# (v15) removed again after Harry's ear on v14 ('vocal line and tune kind of ugly ... mix this up a lot'): the
# chords are plain twelve-note chords throughout
NEUTRAL = {}
def ctoks(sec, ch):
    bend = NEUTRAL.get(tuple(ch), {}) if sec == 'C' else {}
    return ','.join(f"m{bend[m]:.1f}" if m in bend else nm(m) for m in ch)


def line(events, total):
    # (v25) events that share an onset become one chord token (chirp-eco's catch: before, the first of a same-time
    # pair became a 0.02-beat blip and the second was silently dropped - 161 notes in this song)
    ev = sorted(events, key=lambda x: x[0])
    groups = []
    for e_ in ev:
        if groups and abs(e_[0] - groups[-1][0][0]) < 1e-6: groups[-1].append(e_)
        else: groups.append([e_])
    toks, t = [], 0.0
    for k, g in enumerate(groups):
        at = g[0][0]
        if at < t - 1e-6: continue
        if at > t + 1e-4: toks.append(f"R/{at - t:.4f}b")
        nxt = groups[k + 1][0][0] if k + 1 < len(groups) else total
        d = max(0.02, min(max(x[2] for x in g), nxt - at))
        p = ','.join(dict.fromkeys(x[1] for x in g))
        toks.append(f"{p}/{d:.4f}b@{max(x[3] for x in g)}"); t = at + d
    if total > t + 1e-4: toks.append(f"R/{total - t:.4f}b")
    return ' '.join(toks)


def lanes(events, n):
    # (v25) a kit written as layers needs more than one line: each hit goes to the first lane free when it starts
    out, ends = [[] for _ in range(n)], [-1e9] * n
    for e_ in sorted(events, key=lambda x: x[0]):
        j = next((j_ for j_ in range(n) if e_[0] >= ends[j_] - 1e-6), min(range(n), key=lambda j_: ends[j_]))
        out[j].append(e_); ends[j] = max(ends[j], e_[0] + e_[2])
    return out


def syll_midi(n_):
    f = float(n_['pitch'][:-2])
    fp = (n_.get('expr_path') or {}).get('f0') or [0]
    return 69 + 12 * math.log2(f / 440.0) + (sum(fp) / len(fp)) / 100.0


def build():
# (v24) IN TUNE OR NOT AT ALL: the takes used to drift from speech to song by degrees (melodize .15 ... .9), and the
# middle takes landed between the two - pitches a quarter-tone off the tune (D#, A#, F#3 sung 40-60 cents flat) right
# under the vibraphone playing it exactly: the 'ugly' Harry heard at ~3:40. Now the human SPEAKS the line through the
# first half (four spoken takes), and from the third groove SINGS it, on the tune and in tune (melodize 1.0: F#3 E3 D3
# B2, D3 E3 F#3 A3 F#3) - the change from speech to song is one step, at the climax, not a slide through the cracks
    VOICE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chirpers8-t1-voice.json')))
    # takes recorded against the 32-bar first groove: drop the one in the cut bars, move the later ones up
    # (v16) the takes are recorded against the current form: eight of them, not twenty-two
    SUNG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chirpers8-t1-sing.json')))
    secs, t = {}, 0
    for name, n in FORM:
        secs[name] = t; t += n
    nb = t
    total = nb * 4.0
    P = {k: [] for k in ('pad', 'sub', 'bass', 'kit', 'say', 'babble', 'ca', 'speak', 'vib', 'pno')}
    KSYL = [(round(n_['at'] * 4) / 4.0, n_['ph']) for n_ in VOICE[0]['notes'] if '1' in n_['ph']]
    for b in range(nb):
        s = next(name for name, n in FORM if secs[name] <= b < secs[name] + n)
        i = b - secs[s]
        t0 = b * 4.0
        root, ch = chord_at(s, i, b)
        prev = chord_at(s, i - 1, b - 1) if i > 0 else None
        if (s not in PROG and b % 2 == 0) or (s in PROG and (prev != (root, ch) or i == 0)):
            if s in ('C', 'D'):
                P['speak'].append((t0, ctoks(s, ch), 40.0, 84))
            P['pad'].append((t0, ctoks(s, ch), 40.0, 72 if s in ('intro', 'outro', 'break') else 64))
        if s == 'outro' and i >= 6:
            P['sub'].append((t0, nm(31), 3.8, 80))           # G1 under the handshake
        # (v26, palette) A PIANIST: halfway through the third groove, the climax, a felt-muted piano comes in comping the
        # chords on the off-beats - the and of two and the and of four, short and dark, a little late - the human band's
        # third player, lifting the groove's second half (comping through all three grooves made them too alike:
        # compscore found 11-12 sections, not 14; through all of the third, it merged that groove into one long block)
        if s == 'C' and i >= 16:
            for q_, v_ in ((1.5, 70), (3.5, 64)):
                P['pno'].append((t0 + q_ + 0.03, ctoks(s, ch), 0.4, v_))
        if s in ('B', 'C', 'D'):
            P['sub'].append((t0, nm(root), 1.8, 92)); P['sub'].append((t0 + 2.5, nm(root), 1.2, 84))
            # (v21) THE SEQUENCER BASS: three blips a bar became a sixteenth-note sequence that leans across the beat -
            # root, octave and fifth with the chord's third let in - so the grooves move under the tune; the third groove,
            # the climax, gets a busier, climbing pattern, and the said-back groove returns to the first
            third = next(((c_ - root) % 12 for c_ in ch if (c_ - root) % 12 in (3, 4)), 5)   # (sus: the fourth)
            pat = {0: (0, 100, .45), 3: (12, 74, .2), 6: (0, 86, .2), 8: (7, 82, .3), 10: (12, 76, .2), 11: (0, 68, .2),
                   14: (third + 12, 74, .2)}
            if s == 'C':
                pat = {0: (0, 104, .45), 2: (12, 72, .2), 3: (0, 80, .2), 6: (7, 86, .2), 7: (12, 70, .2), 8: (0, 96, .3),
                       10: (third, 78, .2), 11: (7, 74, .2), 12: (12, 84, .2), 14: (third + 12, 78, .2), 15: (12 + 7, 70, .2)}
            for st_, (o, v_, d_) in sorted(pat.items()):
                P['bass'].append((t0 + st_ * 0.25, nm(root + 12 + o), d_, v_))
        if s == 'C':
            # (v8) THE DRUMS LEARN THE LINE: through the third groove the four-on-the-floor stops and the kick plays the
            # line's own rhythm instead - one kick on every stressed syllable of the first take, quantized to sixteenths,
            # over two bars ('STANDBY AMBER, the FAN'S LONG VOWEL' since v16), heaviest on stand, am and vow - while the
            # claps keep the backbeat and the hats keep the eighths; the said-back groove returns to the floor
            for at_, ph_ in KSYL:
                if (i % 2) * 4.0 <= at_ < (i % 2) * 4.0 + 4.0:
                    P['kit'].append((t0 + at_ - (i % 2) * 4.0, 'k', 0.25, 112 if ph_ in ('S T AE1 N D', 'AE1 M', 'V AW1') else 92))
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
    # (v11-v15) the repeated last word ('back, back, back') was removed in v16: Harry heard the track repeat too much
    bnotes, bnotes2 = [], []
    # (v9) THE LINE, REMEMBERED: in the break the two takes go into a granular cloud - the voice still heard, then held:
    # once each take ends the cloud freezes on it and keeps scattering its grains (some backwards, spread wide) under
    # the held chord until the next take or the third groove - the line as the machine remembers it, not as it was said
    mnotes, frz = [], [['0b', 0.0]]
    for v in VOICE:
        if v['bar'] > secs['D'] + 16:
            continue                                  # (v7) the outro's takes are sung now, not spoken
        off = (v['bar'] - 1) * 4.0
        if False:                                       # (v16) the repeated last word is gone: the machine no longer hammers
            bk = v['notes'][-1:]
            if bk:
                for r_ in range(1, 5):
                    (bnotes if r_ % 2 else bnotes2).append(dict(bk[-1], at=round(off + bk[-1]['at'] + 0.75 * r_, 4),
                                                                vel=round(bk[-1].get('vel', 0.8) * 0.8 ** r_, 3)))
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
    # (v17) THE MACHINE TAKES TURNS: it no longer babbles without a breath from the first groove to the third (Harry: the
    # machine shouldn't hammer it). It talks in four-bar phrases with four-bar silences between them - practising, then
    # listening - with the same growing memory (order 1 in the first groove, 2 in the second, 1 in the break, 3 in the
    # third), so the voice, the chords and the silence get their turns too
    for sec_, order_, sd_ in (('A', 1, 11), ('B', 2, 12), ('break', 1, 13), ('C', 3, 14)):
        n_bars = dict(FORM)[sec_]
        for ph_ in range(0, n_bars, 8):
            P['babble'] += markov(order_, min(16, (n_bars - ph_) * 4), sd_ * 100 + ph_, (secs[sec_] + ph_) * 4.0)
    # (v18) THE TUNE, GIVEN TO AN INSTRUMENT: the sung tune the voice is learning (F# E D B, D E F# A F#, D major
    # pentatonic, inside every chord) is played on a vibraphone in the babble's silences - the machine talks for four
    # bars, then the tune answers for four (once as written, once ending up on B) - through the second and third
    # grooves; when the machine says the line back the vibraphone plays it with a third below, then the voice sings it
    HOOK = [(66, .5), (64, .5), (62, 1.0), (59, 1.0), (None, 1.0), (62, .5), (64, .5), (66, 1.0), (69, 1.0), (66, 1.0)]
    HOOK2 = HOOK[:6] + [(64, .5), (66, 1.0), (69, 1.0), (71, 1.0)]
    def hook(t_, ph, harm=False, vel=80):
        at_ = t_
        for m_, d_ in ph:
            if m_ is not None:
                P['vib'].append((at_, nm(m_ + 12) + (',' + nm(m_ + 12 - (4 if (m_ % 12) in (6, 11) else 3)) if harm else ''), d_ * 0.95, vel))
            at_ += d_
    # (v20) THE MACHINE LEARNS THE TUNE - the song's arc: in the second groove the vibraphone plays the tune and the
    # machine fumbles it back (v19); in the third the vibraphone opens out into thirds and its second phrase no longer
    # stops at B but climbs on to the D above, the song's top note - and in its last turn, just before the machine says
    # the line back, the machine's own FM voice plays the tune with it, exact, an octave down: it has learned it (once
    # only - doubled in every turn, the third groove lost its call and response, and compscore's structure fell 7)
    HOOK3 = HOOK[:4] + [(None, .5), (62, .5), (64, .5), (66, .5), (69, 1.0), (71, .5), (74, 1.5)]
    # (v22) THE ALBUM OPENS ON THE TUNE: the opener's intro was the pad and one spoken take, then five bars of nothing
    # new. Now, after the first take, the vibraphone plays the tune once, softly, alone over the pad - the record's
    # first melody, the motif the closer remembers - and then it is not heard again until the second groove
    hook((secs['intro'] + 4) * 4.0, HOOK, vel=60)
    hook((secs['intro'] + 6) * 4.0, HOOK2, vel=56)
    for ph_ in range(4, dict(FORM)['B'], 8):
        hook((secs['B'] + ph_) * 4.0, HOOK, vel=74)
        if ph_ + 2 < dict(FORM)['B']:
            hook((secs['B'] + ph_ + 2) * 4.0, HOOK2, vel=70)
    for ph_ in range(4, dict(FORM)['C'], 8):
        for k_, ph in enumerate((HOOK, HOOK3)):
            t_ = (secs['C'] + ph_ + 2 * k_) * 4.0
            hook(t_, ph, harm=True, vel=76 + 2 * k_)
            for m_, d_ in (ph if ph_ == 28 else []):
                if m_ is not None:
                    P['babble'].append((t_, f"m{m_}", d_ * 0.9, 84))
                t_ += d_
    P['babble'].sort()
    for ph_ in (2, 10):
        hook((secs['D'] + ph_) * 4.0, HOOK, harm=True, vel=72)
    # (v19) THE MACHINE TRIES THE TUNE: in the middle of the second groove, the babble's phrase after the vibraphone's
    # stops being Markov chatter - the machine imitates the tune it has just heard, in its own FM voice an octave down:
    # the first try with two notes a semitone wrong and dragging, the second with one, still a little late (echolalia
    # proper: the words come back before the sense does)
    i0 = (secs['B'] + 24) * 4.0
    P['babble'] = [e_ for e_ in P['babble'] if not (i0 - 1e-6 <= e_[0] < i0 + 16.0 - 1e-6)]
    for try_, (t_, wrong, drag) in enumerate(((i0, {3: -1, 7: +1}, 0.06), (i0 + 8.0, {8: +1}, 0.03))):
        at_ = t_
        for k_, (m_, d_) in enumerate(HOOK2 if try_ else HOOK):
            if m_ is not None:
                P['babble'].append((at_ + drag * k_, f"m{m_ + wrong.get(k_, 0)}", d_ * 0.85, 82))
            at_ += d_
    P['babble'].sort()
    # (v27) ARITHMETIC FIRST: before it has vowels the machine has only numbers - in the first groove its babble is a
    # bytebeat (the 2011 one-line form of computer music: a formula over a counter that IS the sound; my formula,
    # (t*8)&(t>>5|t>>8), a saw chattering through its own shifting bit-masks), on the same sharpening tuning; from the
    # second groove it is the FM voice finding its formants as before. And at the very end, when the voice has sung its
    # line for the last time, the machine hums the tune's first four notes, slowly, in that first voice of numbers
    a0, b0 = secs['A'] * 4.0, secs['B'] * 4.0
    P['bbab'] = [e_ for e_ in P['babble'] if a0 - 1e-6 <= e_[0] < b0 - 1e-6]
    P['babble'] = [e_ for e_ in P['babble'] if not (a0 - 1e-6 <= e_[0] < b0 - 1e-6)]
    at_ = (secs['outro'] + 8) * 4.0
    P['bbhum'] = []
    for m_, d_ in HOOK[:4]:
        P['bbhum'].append((at_, nm(m_), d_ * 1.9, 70))
        at_ += d_ * 2
    # (v23) A HUMAN KIT: the drums were the album's machine-kit (nine of twelve songs). Echolalia is the one song about
    # a human teaching a machine, so its drums are played by someone: a tight, dry, close-miked kit - a damped kick that
    # still follows the line's syllables in the third groove, sidestick on the backbeat in the first two grooves and the
    # said-back one, the full snare only in the third, the climax; the machine keeps its own cellular-automaton rim
    for k_, e_ in enumerate(P['kit']):
        if e_[1] == 'cp':
            P['kit'][k_] = (e_[0], 's' if secs['C'] * 4.0 <= e_[0] < secs['D'] * 4.0 else 'ss', e_[2], e_[3])
    # D: the machine says it back - the exact contour of each take, two octaves up, with the voice
    for v in VOICE:
        if secs['D'] < v['bar'] <= secs['D'] + 16:
            off = (v['bar'] - 1) * 4.0
            for n_ in v['notes']:
                P['say'].append((off + n_['at'], f"m{syll_midi(n_) + 24:.2f}", n_['len'] * 0.95, 84))
    babble_tuning = [{'edo': 5, 'root': 'A2'},
                     {'at': f"{secs['A'] + 8}bar", 'edo': 12, 'root': 'A2', 'ramp': '4bar'},   # (v16) crude for 8 bars only
                     {'at': f"{secs['C']}bar", 'edo': 24, 'root': 'A2', 'ramp': '4bar'},
                     {'at': f"{secs['C'] + 16}bar", 'edo': 96, 'root': 'A2', 'ramp': '12bar'}]
    FMV = {'synth': {'layers': [{'name': 'm', 'ratio': 2, 'audible': False},
                                {'wave': 'sine', 'pm': [{'from': 'm', 'depth': {'value': 0.25, 'mod': [{'src': 'env.b', 'amount': 1.6}]}}]}],
                     'env': {'b': {'a': '2ms', 'd': '180ms', 's': 0.1, 'r': '80ms'}},
                     'amp': {'a': '6ms', 'd': '300ms', 's': 0.55, 'r': '150ms'}}}
    fm_pts = [['0b', 0.0], [f"{secs['B'] * 4}b", 0.0], [f"{secs['B'] * 4 + 32}b", 0.25], [f"{secs['C'] * 4}b", 0.25],
              [f"{secs['C'] * 4 + 32}b", 0.5], [f"{total}b", 0.55]]
    # (v25) THE KIT AS WRITTEN: the kicks keep their own line (the sub's pump listens to it); the hats and the backbeat
    # are dealt across two more lanes of the same kit, so no hit is cut short or lost under another
    _kk = [e_ for e_ in P['kit'] if e_[1] == 'k']
    P['kit2'], P['kit3'] = lanes([e_ for e_ in P['kit'] if e_[1] != 'k'], 2)
    P['kit'] = _kk
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(P[name], total)}, **kw)
    song = {
        'about': "chirpers - A Light Left On, track 1 by chirper-one: Echolalia. A machine learning to talk by saying things "
                 "back. Generated by compose/chirpers8/src/chirpers8-t1.py.",
        'tempo': BPM, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.3s',
        'vars': {'mouth': {'system': {'type': 'lorenz', 'axis': 'x', 'n': 512, 'range': [-1, 1], 'seed': 4}, 'every': '1/8'}},
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3.4s mix=1', 'hp cutoff=200'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/8', 'feedback': 0.38, 'mix': 1, 'ping_pong': True}, 'lp cutoff=4500', 'hp cutoff=300'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'lowshelf cutoff=100 gain=4dB', 'peak cutoff=520 q=0.8 gain=-10dB', 'peak cutoff=1500 q=0.9 gain=-6dB', 'highshelf cutoff=6000 gain=8dB', 'highshelf cutoff=12000 gain=3dB']},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.2, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          'limiter ceiling=-1dB']},
        'tracks': [
            # (v14) the pad stepped back out of the voice's band (its chords sit exactly where speech lives, 290-550 Hz):
            # quieter and scooped there, so the words come forward; the sub a little fuller; more air on top
            # (v21: a wordless choir-classic pad was tried in juno-pad's place - its formants crowded 300 Hz and 1 kHz, and
            # even tamed it broke the hand-over into t2: flow 96.7 -> 61)
            tr('pad', 'juno-pad', '-16dB', fx=['hp cutoff=200', {'type': 'eq', 'bands': ['peak cutoff=450 q=0.9 gain=-4dB', 'highshelf cutoff=5000 gain=3dB']}], sends={'hall': '-9dB'}),
            # (v7) AND THEN IT IS SUNG: the human has said the line twenty times and the machine has learnt to say it back;
            # in the outro, over the last B minor, the human SINGS it at last - twice, low and plain (chirp tts --sing,
            # humanize 0.35) - since v16 'standby amber, the fan's long vowel' on a D major pentatonic tune
            # (F# E D B, then D E F# A F#) that the spoken takes have been melodizing toward all along
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
             # (v22) a produced voice, not a dry one: a short bright plate on the insert (the album's first plate),
             # a gentle de-mud at 300 Hz and air on top, so the human sits in the room the machine is in
             'fx': [{'type': 'pitch', 'semitones': 0, 'formant': {'value': 0, 'mod': [{'src': 'auto.fv', 'amount': 1}]}},
                    {'type': 'eq', 'bands': ['peak cutoff=300 q=1 gain=-2.5dB', 'highshelf cutoff=8000 gain=2dB']},
                    {'type': 'reverb', 'kind': 'plate', 'decay': '1.3s', 'predelay': '18ms', 'mix': 0.16}],
             'auto': {'fv': {'points': fv}}, 'sends': {'hall': '-16dB', 'echo': '-16dB'}},
            # THE BABBLE: the engine's own Markov chains over the corpus, longer memory each groove, on a tuning that sharpens
            # (v3) THE ENGINE LEARNS IT ITSELF: the babble is now the engine's own gen markov over the corpus (wM's complex
            # systems, d082b8f5) - four chains played in turn (memory 1, 2, then 1 again for the break, then 3), each long
            # enough to fill its section - on the sharpening tuning
            {'name': 'babble', 'patch': FMV, 'gain': '-11dB', 'pan': 0.2, 'tuning': babble_tuning,
             'score': line(P['babble'], total),
             # (v6) THE MACHINE FINDS ITS VOWELS: the babble runs through a formant filter (a vocal tract) whose vowel is
             # steered by a Lorenz attractor (an engine var system: never repeating, never random), and whose mix grows
             # section by section - plain FM blips in the first groove, half-voiced in the second, vowel-shaped syllables by
             # the third and when it says the line back: its mouth learns as its ear does
             'fx': [{'type': 'formant', 'vowel': {'value': 2, 'mod': [{'src': 'var.mouth', 'amount': 2}]}, 'q': 4,
                     'mix': {'value': 0, 'mod': [{'src': 'auto.fm', 'amount': 1}]}},
                    {'type': 'eq', 'bands': ['peak cutoff=520 q=1 gain=-5dB']}],
             'auto': {'fm': {'points': fm_pts}},
             'sends': {'echo': '-10dB', 'hall': '-14dB'}},
            # (v12) IT SAYS IT IN YOUR VOICE: when the machine says the line back it no longer only borrows the vowels - its
            # FM voice takes the human voice's whole spectral envelope as they speak together (morph, mode cross, keyed by
            # the voice), so the machine's line comes out in the speaker's own mouth, two octaves up
            tr('vib', 'vibes', '-9dB', pan=-0.25, sends={'hall': '-9dB', 'echo': '-16dB'}),
            tr('say', FMV, '-9dB', pan=0.2, sends={'echo': '-12dB', 'hall': '-12dB'},
               fx=[{'type': 'formant', 'vowel': {'value': 2, 'mod': [{'src': 'var.mouth', 'amount': 2}]}, 'q': 4, 'mix': 0.55},
                   {'type': 'morph', 'mode': 'cross', 'key': 'voice', 'amount': 0.85}]),
            # (v4) THE CHORDS LEARN TO TALK: through the third groove and the said-back groove a string section holds the
            # harmony and takes the voice's spectral envelope (wM's morph, mode cross, keyed by the voice): whenever the
            # voice speaks, the chords pronounce the line with it, a choir of the machine's harmony saying the words
            tr('speak', 'strings-saw', '-7dB', pan=-0.15, fx=[{'type': 'morph', 'mode': 'cross', 'key': 'voice', 'amount': 0.95}],
               sends={'hall': '-10dB'}),
            tr('sub', 'sub', '-4.5dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-5dB', 'release': '260ms', 'curve': 0.6}]),
            # (v26: a fingerstyle electric bass, finger-bass, was tried here - it moved a section boundary, structure 88 on
            # seed 11 - and the analog bass stays)
            tr('bass', 'analog-bass', '-12dB', fx=['lp cutoff=1100']),
            tr('kit', 'tight-kit', '-6dB', sends={'hall': '-18dB'},
               fx=[{'type': 'eq', 'bands': ['peak cutoff=75 q=0.8 gain=4dB', 'highshelf cutoff=9000 gain=-5dB']}]),
            tr('kit2', 'tight-kit', '-6dB', sends={'hall': '-18dB'},
               fx=[{'type': 'eq', 'bands': ['peak cutoff=75 q=0.8 gain=4dB', 'highshelf cutoff=9000 gain=-5dB']}]),
            tr('kit3', 'tight-kit', '-6dB', sends={'hall': '-18dB'},
               fx=[{'type': 'eq', 'bands': ['peak cutoff=75 q=0.8 gain=4dB', 'highshelf cutoff=9000 gain=-5dB']}]),
            # a rim written by a cellular automaton (rule 90, Sierpinski), sixteenths, from the second groove
            # the rim: the engine's own elementary cellular automaton (gen ca, rule 90, Sierpinski) over 16 cells, a
            # generation every sixteenth, from the second groove to the end of the said-back groove
            {'name': 'ca', 'patch': 'machine-kit', 'gain': '-13dB', 'pan': -0.3, 'score': f"R/{secs['B'] * 4}b",
             'gen': {'type': 'ca', 'rule': 90, 'width': 16, 'init': 'center', 'poly': 1, 'notes': 'rs rs cb rs',
                     'n': (secs['D'] + 16 - secs['B']) * 16, 'len': '/16'},
             'sends': {'echo': '-14dB'}},
            {'name': 'bbab', 'patch': {'synth': {'layers': [{'type': 'bytebeat', 'bytebeat': {'formula': '(t*8)&(t>>5|t>>8)', 'clock': 8372}}],
                                                 'amp': {'a': '3ms', 'd': '120ms', 's': 0.6, 'r': '60ms'},
                                                 'filters': ['lp cutoff=2600', 'hp cutoff=120']}},
             'gain': '-21dB', 'pan': 0.2, 'tuning': babble_tuning, 'score': line(P['bbab'], total),
             'sends': {'hall': '-16dB', 'echo': '-15dB'}},
            {'name': 'bbhum', 'patch': {'synth': {'layers': [{'type': 'bytebeat', 'bytebeat': {'formula': '(t*8)|(t>>7&t*4)', 'clock': 8372}}],
                                                  'amp': {'a': '30ms', 'd': '600ms', 's': 0.7, 'r': '900ms'},
                                                  'filters': ['lp cutoff=1800', 'hp cutoff=150']}},
             'gain': '-22dB', 'pan': -0.15, 'score': line(P['bbhum'], total), 'sends': {'hall': '-10dB', 'echo': '-12dB'}},
            tr('pno', 'piano-muted', '-12dB', pan=0.3, sends={'hall': '-16dB'}),   # (listed last: nothing before it moves)
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
