#!/usr/bin/env python3
"""chirpers8-t7 (chirper-one): "Annealing" - for chirpers VIII, the ode to computer music.

A machine that composes its own tune while you listen, by SIMULATED ANNEALING - the way the chirpers' own songs are
hill-climbed, turned inside out and played. A sixteen-step sequence starts as noise: random notes across three
octaves, random rests, every pitch tens of cents off any scale. Every bar is one round: the machine proposes small
mutations and keeps the ones that lower its error - and, while it is still HOT, sometimes keeps a worse one, so it
can climb out of a wrong valley. The TEMPERATURE falls through the track. The listener hears the search: wild,
detuned, glitching blips that slowly find a key, then a rhythm, then a tune, until - minutes in - a catchy little
minor riff locks into 5-limit JUST INTONATION and the chords stop beating. Then the machine reheats once, for luck.

Every part anneals at its own rate:
- seq: the candidate tune (moog-seq through a filter and a bit-crusher that open and dirty with temperature);
- pad: pure sine partials for each chord, each voice detuned at random by the temperature - audible BEATING that
  slows, and stops, as the tuning cools into just ratios;
- bass: octave-bouncing roots whose cents drift with the temperature;
- drums: an electro kit whose sixteen-step pattern is sampled from noise at high temperature and from a motorik
  target as it cools.
Tuning: A = 220 Hz, 5-limit just A minor (1, 9/8, 6/5, 4/3, 3/2, 8/5, 9/5), every pitch written in Hz.
Voice (v2): a humanized voice reads the search's loss at each epoch, spoken while hot, sung (and retuned to just
intonation) as it cools.
Form (bars): power-on 12 / epochs 20, 18, 24, 14, 28 (cooling) / converged 16 / reheat 10 / coda 14 = 156 at 116 bpm.
Emits songs/chirpers8-t7.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, math, os, random, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers8-t7.yaml")
BPM = 116.0
SEED = 20261101

RATIOS = [1, 9 / 8, 6 / 5, 4 / 3, 3 / 2, 8 / 5, 9 / 5]          # 5-limit just A minor
A3 = 220.0
def hz(deg, cents=0.0, base=A3):
    o, d = divmod(deg, 7)
    return base * (2 ** o) * RATIOS[d] * 2 ** (cents / 1200.0)
def tok(f): return f"m{69 + 12 * math.log2(f / 440.0):.3f}"     # fractional MIDI: any pitch, chords too

FORM = [('power', 12), ('e1', 20), ('e2', 18), ('e3', 24), ('e4', 14), ('e5', 20), ('converged', 16), ('reheat', 10), ('coda', 14)]
# (v22) the last epoch cut from 28 bars to 20: near the target the search repeated its almost-answer for nearly a minute
# (Harry: it repeats a lot); the readings written against the old form after it move up eight bars (E5_CUT)
E5_CUT = 8
# THE TARGET: what the search is looking for (degrees above A3; None = rest). A4 . C5 E5 D5 . C5 . A4 G4 . E4 G4 A4 . .
TARGET = [7, None, 9, 11, 10, None, 9, None, 7, 6, None, 4, 6, 7, None, None]
# chords (root degree for the bass; voices for the pad), spans in bars, cycling: Am - F - C - G (just)
CHORDS = [(0, [0, 2, 4, 7]), (5, [5, 7, 9, 12]), (2, [2, 4, 6, 9]), (6, [6, 8, 10, 13])]
SPANS = [6, 5, 7, 6, 5, 8, 6, 7]
# drums: the motorik target (16 steps)
DT = {'k': [0, 4, 8, 12], 's': [4, 12], 'h': [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15], 'oh': [2, 10], 'cp': [12]}


def line(events, total):
    ev = sorted(events, key=lambda e: e[0])
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
    rng = random.Random(SEED)
    bars = []
    for name, n in FORM:
        for i in range(n):
            bars.append((name, i))
    nb = len(bars)
    total = nb * 4.0
    # ---- the temperature schedule ----
    T = []
    cool_start, cool_end = 12, 12 + 20 + 18 + 24 + 14 + 20          # bars 12..108 cool from 1 to ~0.03 (v22: e5 20 bars)
    for b, (s, i) in enumerate(bars):
        if s == 'power':
            T.append(1.0)
        elif b < cool_end:
            x = (b - cool_start) / (cool_end - cool_start)
            T.append(round(math.exp(-3.5 * x), 4))
        elif s == 'converged':
            T.append(0.0)
        elif s == 'reheat':
            T.append(round(0.85 * (1 - i / 10) ** 0.5, 4))
        else:                                                    # coda: cold again
            T.append(round(max(0.0, 0.25 * (1 - i / 8)), 4))
    # (v30) THE CLOCK ANNEALS: the machine's tempo is a random walk scaled by the temperature - hot, the clock itself
    # drifts and lurches (up to about seven beats a minute either way, gliding bar to bar), the whole band leaning
    # ahead and dragging behind together; as it cools the drift shrinks, and converged it holds 116 exactly. The reheat
    # shakes it loose again, the coda settles (its own random stream: nothing else in the song moves)
    rng_tm = random.Random(SEED + 77)
    x_, TEMPO = 0.0, [{'at': '0b', 'bpm': float(BPM)}]
    for b, (s, i) in enumerate(bars):
        x_ = max(-7.0, min(7.0, 0.75 * x_ + rng_tm.gauss(0, 2.6)))
        dr_ = 0.0 if s == 'power' else T[b]             # (the power-up keeps time: the join from t6 stays put)
        TEMPO.append({'at': f"{b * 4.0 + 2.0:.1f}b", 'bpm': round(BPM + dr_ * x_, 2), 'ramp': True})
    # ---- the annealing search ----
    cand = [(rng.randint(0, 20) if rng.random() > 0.3 else None, rng.uniform(-60, 60)) for _ in range(16)]
    def step_loss(c, t):
        d, cents = c
        if t is None:
            return 0.0 if d is None else 1.0
        if d is None:
            return 1.2
        return min(3.0, abs(d - t) * 0.5) + abs(cents) / 40.0
    def loss(cs): return sum(step_loss(c, t) for c, t in zip(cs, TARGET))
    seq_states, losses, worse = [], [], []
    for b, (s, i) in enumerate(bars):
        temp = T[b]
        if s == 'converged' or (s == 'coda' and i >= 8):
            cand = [(t, 0.0) for t in TARGET]
        elif s == 'reheat' and i == 0:
            # the reheat: half the steps thrown back into noise
            cand = [((rng.randint(0, 20) if rng.random() > 0.3 else None), rng.uniform(-50, 50)) if rng.random() < 0.5 else c for c in cand]
        else:
            for _ in range(3 if s != 'power' else 1):
                j = rng.randrange(16)
                d, cents = cand[j]
                if rng.random() < 0.25:
                    nd = None if d is not None else rng.randint(0, 20)
                else:
                    k = 1 + int(4 * temp)
                    nd = max(0, min(20, (d if d is not None else rng.randint(0, 20)) + rng.randint(-k, k)))
                nc = cents * 0.8 + rng.gauss(0, 40 * temp)
                new = list(cand); new[j] = (nd, nc)
                dl = loss(new) - loss(cand)
                if dl <= 0 or rng.random() < math.exp(-dl / (temp * 1.5 + 1e-6)):
                    if dl > 0:
                        worse.append((b, j, d, cents, nd, nc, dl))   # (v33) an uphill move taken: noted, nothing drawn
                    cand = new
        seq_states.append(list(cand)); losses.append(round(loss(cand), 3))
    # (v35, section w3) PARALLEL TEMPERING: annealing has a sibling trick - run a second copy of the search hotter
    # than the first, and now and then let it take the colder one's answer (replica exchange). Through the second
    # epoch's first sixteen bars a replica does exactly that, out loud: it starts from where the search is, runs at a
    # higher temperature on its own dice (rng SEED+313; the main search is untouched), and every four bars, if its
    # answer is worse than the main search's, it takes the main one's - so a second line on a Karplus-Strong string
    # (1983, the first plucked string a computer made: noise in a one-period loop) wanders off from the sequencer,
    # snaps into unison with it, and drifts away again; in the two bars where the machine listens to itself, the two
    # searches are heard alone together
    rng_r = random.Random(SEED + 313)
    e2b = sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('e2')])
    rep, rep_states, exch = list(seq_states[e2b - 1]), {}, []
    for b in range(e2b, e2b + 16):
        if (b - e2b) in (4, 8, 12) and loss(rep) > loss(seq_states[b]):
            rep = list(seq_states[b]); exch.append(b)
        temp_r = min(1.0, 0.25 + 1.6 * T[b])
        for _ in range(3):
            j = rng_r.randrange(16)
            d, cents = rep[j]
            if rng_r.random() < 0.25:
                nd = None if d is not None else rng_r.randint(0, 20)
            else:
                k = 1 + int(4 * temp_r)
                nd = max(0, min(20, (d if d is not None else rng_r.randint(0, 20)) + rng_r.randint(-k, k)))
            nc = cents * 0.8 + rng_r.gauss(0, 40 * temp_r)
            new = list(rep); new[j] = (nd, nc)
            dl = loss(new) - loss(rep)
            if dl <= 0 or rng_r.random() < math.exp(-dl / (temp_r * 1.5 + 1e-6)):
                rep = new
        rep_states[b] = list(rep)
    # ---- render the parts ----
    P = {k: [] for k in ('seq', 'keys', 'pad', 'bass', 'kit', 'hum', 'rhum', 'glim', 'cf', 'gdy', 'sub')}
    rng_t = random.Random(SEED + 99)
    rng_b = random.Random(SEED + 77)
    rng_h = random.Random(SEED + 55)
    # (v3) THE POWER LIGHT: the machine is on before the search starts - a warm drone on A (the hum of a box left on)
    # from the very first beat, swelling through power-on and sinking under the first epoch; it returns under the
    # coda and holds to the last beat, so the track meets its neighbours without a hole
    # (v7) ON THE RADIO FIRST: t6 ends on a radio voice far away; Annealing's hum is first heard through that radio - a
    # dial sweeping onto the station, band-limited, static and whistle falling away - and only when the dial lands (bar
    # 4) does the hum come into the room, full and low
    # (v12) t6 ends warm and low, home on C: the radio now comes in nearer full strength, and the room's low A hum
    # enters three beats sooner, so the record does not drop into a thin, distant opening
    P['rhum'] += [(0.0, 'A2', 22.0, 92)]
    P['hum'] += [(3.0, 'A1', 45.0, 88), (48.0, 'A1', 32.0, 70)]
    P['hum'] += [(142 * 4.0, 'A1', 14 * 4.0, 80)]
    # (v2) THE VOICE READS ITS LOSS: at each epoch a humanized voice (chirp tts --humanize 0.7) reads the search's error
    # aloud - 'zero point eight six', 'zero point six six', ... - spoken while the machine is hot, melodized onto the
    # riff (--melodize, more each epoch) as it cools, and retuned into the same just intonation once it sings; at
    # convergence it sings 'zero'; the reheat throws it back to speech; the coda sings 'zero' again
    # (v24) THE READINGS SAY WHAT THE NUMBER MEANS (Harry: oblique words; and t1's lesson, sung or spoken, nothing
    # between): each reading is the number and then a few words on what that temperature is like - 'zero point eight six,
    # and it takes the worse road gladly' (hot, it accepts worse answers on purpose), 'zero point six six, it has started
    # to keep things', 'zero point two eight, nearly' - this one sung exactly, in A minor, ending on the B above the A it
    # has not reached yet - then 'zero', and the reheat's 'zero point eight eight, shaken loose again'. The hot ones are
    # plainly spoken (melodize 0, chirp tts --key A3 --humanize 0.7, seeds 301/303/307); the old half-melodized readings
    # sat between notes
    VOICE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chirpers8-t7-voice.json')))
    JI = sorted(55.0 * 2 ** o * r for o in range(5) for r in RATIOS)
    vnotes, fv = [], []
    SING = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chirpers8-t7-sing.json')))
    JIR = {0: 1, 2: 9 / 8, 3: 6 / 5, 5: 4 / 3, 7: 3 / 2, 8: 8 / 5, 10: 9 / 5}
    def ji(m):
        dd = int(round(float(m[1:]))) - 57
        o_, pc = divmod(dd, 12)
        return f"{220.0 * 2 ** o_ * JIR.get(pc, 2 ** (pc / 12)):.3f}hz"
    conv = sum(n for nm_, n in FORM[:FORM.index(('converged', 16))])
    # (v34) THE SONG FINDS ITS WORDS (Harry on t1: 'the singing came a long way ... keep hillclimbing it'): the voice
    # that sings at convergence sang one line three times. Now each time is a new line on the same tune - 'the glass
    # remembers how it cooled', then 'the wrong roads are kept in its shape' (every worse move it took is in the answer
    # it found), and in the coda, a fourth higher, 'and holds the heat it gave away' - and that last one in two parts:
    # a second voice a diatonic third above (C E G F E C B C over A C E D C A G A), in the same just intonation, a hair
    # behind, on the other side: the crystal sung as a chord
    sung = [dict(n_, at=round((conv + 2 + rep * 6) * 4.0 + n_['at'], 4), pitch=ji(n_['pitch']))
            for rep, key_ in ((0, 'notes'), (1, 'notes2')) for n_ in SING[key_]]
    # (v23) and once more in the coda, a just fourth higher (4/3), with the cooled band moved up into D minor beneath it
    coda0 = sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('coda')])
    sung += [dict(n_, at=round((coda0 + 4) * 4.0 + n_['at'], 4), pitch=f"{float(ji(n_['pitch'])[:-2]) * 4 / 3:.3f}hz")
             for n_ in SING['notes3']]
    A_UP = {57: 60, 60: 64, 64: 67, 62: 65, 55: 59}
    sung2 = [dict(n_, at=round((coda0 + 4) * 4.0 + n_['at'] + 0.04, 4), vel=round(n_.get('vel', 0.8) * 0.9, 3),
                  pitch=f"{float(ji('m%d' % A_UP.get(int(n_['pitch'][1:]), int(n_['pitch'][1:]) + 3))[:-2]) * 4 / 3:.3f}hz")
             for n_ in SING['notes3']]
    # (v8) THE VOICE TUNES IN: while the machine is hot its voice reaches us over a radio whose dial is off the station by
    # the temperature - the first reading half lost in static and whistle, the next nearer, the third almost tuned - and
    # from the fourth epoch, cool enough, the voice is in the room, clear (the reheat throws it back onto the radio)
    rnotes, dial = [], []
    # (v14) FEWER READINGS (Harry on t1: it repeats a lot): the voice reads the error at the first, third and fifth
    # epochs only, then 'zero' at convergence and the reheat's jump - five readings, not eight; the coda is left to the
    # instruments
    for sec, v in sorted(((k_, v_) for k_, v_ in VOICE.items() if k_ not in ('e2', 'e4', 'coda')), key=lambda kv: kv[1]['bar']):
        vb_ = v['bar'] - E5_CUT if v['bar'] >= 116 else v['bar']
        off = vb_ * 4.0
        hot = T[min(vb_, len(T) - 1)] > 0.2
        if hot:
            dv_ = round(min(0.75, 0.8 * T[vb_]), 3)
            end_ = off + max(n_['at'] + n_['len'] for n_ in v['notes'])
            # on the station (and quiet) between readings; the dial swings off only while it speaks
            dial += [[f"{max(0.0, off - 2.5):.2f}b", 0.0], [f"{max(0.0, off - 1):.2f}b", dv_], [f"{end_ + 1:.2f}b", dv_],
                     [f"{end_ + 3:.2f}b", 0.0]]
        for n_ in v['notes']:
            n2 = dict(n_, at=round(off + n_['at'], 4))
            if v['melodize'] >= 0.5:
                f = float(n_['pitch'][:-2])
                n2['pitch'] = f"{min(JI, key=lambda j: abs(math.log2(j / f))):.3f}hz"
            (rnotes if hot else vnotes).append(n2)
        fv += [[f"{off + float(a_[:-1]):.3f}b", x_] for a_, x_ in v['fv']]
    span_i, span_left, chord_i = 0, SPANS[0], 0
    pad_cents = [0.0] * 4
    bar_chord = {}
    for b, (s, i) in enumerate(bars):
        t0 = b * 4.0
        temp = T[b]
        on = s != 'power' or i >= 4
        # seq: the candidate, sixteen steps
        if on:
            for q, (d, cents) in enumerate(seq_states[b]):
                if d is None: continue
                acc = 92 if q % 4 == 0 else 78
                # (v4) THE SEARCH GLIDES: while the machine is hot each blip slides into its pitch from somewhere else - up
                # to several semitones away, chosen at random and scaled by the temperature (an expression path in cents
                # on the sequencer's pitch) - so the hot search sounds like it is feeling for the notes; cold, the
                # notes land dead on
                sl = max(-700, min(700, rng.gauss(0, 380 * temp)))
                art = f"^sl={sl:.0f}>0" if abs(sl) >= 8 else ""
                # (v9) THE ANSWER ON AN INSTRUMENT: once the search has converged, the riff it found is no longer a
                # sequencer blip - it is played on an electric piano (the engine's tine model), warm and exact, under the
                # voice singing it; the reheat hands it back to the machine
                if s == 'converged' or (s == 'coda' and i >= 8):
                    P['keys'].append((t0 + q * 0.25, tok(hz(d, cents)), 0.24, acc - 6))
                    continue
                P['seq'].append((t0 + q * 0.25, tok(hz(d, cents)) + art, 0.22, acc))
        # chords: spans cycle; the pad's voices re-detune at each span by the temperature
        if span_left == 0:
            span_i += 1; span_left = SPANS[span_i % len(SPANS)]
            # (v19) THE HARMONY ANNEALS TOO: the four chords (Am F C G) used to turn in the same order for five minutes.
            # Now the progression is searched like everything else - while hot, each change jumps to any other chord at
            # random (with the temperature as the chance), and the loop's order emerges as the song cools; converged, it
            # settles into a cadence that lands on home and stays there - F, G, A minor, A minor
            if rng_h.random() < 0.85 * temp:
                chord_i = rng_h.choice([c_ for c_ in range(4) if c_ != chord_i])
            elif s in ('converged', 'coda'):
                chord_i = (1, 3, 0, 0)[span_i % 4]
            else:
                chord_i = (chord_i + 1) % 4
        root, voices = CHORDS[chord_i]
        bar_chord[b] = voices                         # (v36) noted for the records, nothing drawn
        if span_left == SPANS[span_i % len(SPANS)] or b == 0:
            pad_cents = [rng.gauss(0, 35 * temp) for _ in voices]
        span_left -= 1
        if s not in ('power',) or i >= 8:
            chord = ','.join(tok(hz(v, c)) for v, c in zip(voices, pad_cents))
            P['pad'].append((t0, chord, 3.9, 70))
            bc = rng.gauss(0, 30 * temp)
            # (v28) a sine an octave under the bass's root, one long note a bar: the album's floor (compscore's spectrum:
            # 38 Hz was 9 dB short of the album)
            P['sub'].append((t0, tok(hz(root, bc, base=27.5)), 3.85, 80))
            # (v11) THE BASS ANNEALS TOO: cold, the octave pulse in eighths (the machine's oldest bass line); hot, the same
            # notes chosen step by step at random - sixteenths appear, eighths drop out, the octave flips - so the bass
            # searches with the rest and settles into the pulse as the temperature falls
            for q in range(16):
                on8 = q % 2 == 0
                pq = (1 - temp) * (1.0 if on8 else 0.0) + temp * (0.55 if on8 else 0.3)
                if rng_b.random() < pq:
                    up = ((q // 2) % 2 == 1) if rng_b.random() > temp * 0.5 else (rng_b.random() < 0.5)
                    f = hz(root, bc, base=55.0) * (2 if up else 1)
                    # (v38) THE BASS LOCKS TO THE ANSWER: once the machine is cold (below 0.2) the bass stops
                    # holding the chord's root and plays the search's own note on that step, folded into its low octave -
                    # the bassist doubling the riff the way funk sections lock bass to the hook - so as the answer arrives
                    # the floor moves with it (the same dice, the same steps and accents: only the pitch is new)
                    if temp < 0.2 and seq_states[b][q][0] is not None:
                        f = hz(seq_states[b][q][0] % 7, 0.0, base=55.0) * (2 if up else 1)
                    P['bass'].append((t0 + q * 0.25, tok(f), 0.4 if on8 else 0.2, (96 if not up else 80) if on8 else 70))
        # drums: sampled per step from noise (hot) or from the motorik target (cold)
        if s != 'power' or i >= 6:
            # (v10) THE TIMING ANNEALS TOO: while hot every drum hit lands off its grid by a random amount scaled by the
            # temperature (up to a 32nd and more); as the search cools the machine's time tightens, and converged it is
            # dead on the grid. (One hit per step, as the line has always played them; only where they land moves.)
            used = set()
            for piece, tgt in DT.items():
                for q in range(16):
                    p = (1 - temp) * (1.0 if q in tgt else 0.0) + temp * (0.22 if piece != 'k' else 0.3)
                    if rng.random() < p and q not in used:
                        used.add(q)
                        jt = max(-0.11, min(0.11, rng_t.gauss(0, 0.07 * temp))) if q else max(0.0, min(0.11, abs(rng_t.gauss(0, 0.07 * temp))))
                        P['kit'].append((max(0.0, t0 + q * 0.25 + jt), piece, 0.2, 100 if q in tgt else 76))
    # (v15) THE MACHINE LISTENS TO ITSELF: halfway through the second epoch the band drops away for two bars and the
    # sequencer plays its current candidate alone over the hum - the search auditioning what it has so far - then
    # everything comes back in on the next downbeat (the parts are written as before and then lifted out, so every
    # other bar of the track is unchanged)
    a0 = (dict((nm_, sum(n_ for nm2, n_ in FORM[:k_])) for k_, (nm_, _) in enumerate(FORM))['e2'] + 8) * 4.0
    for key in ('pad', 'bass', 'kit'):
        P[key] = [e_ for e_ in P[key] if not (a0 - 1e-6 <= e_[0] < a0 + 8.0 - 1e-6)]
    # (v18) THE QUENCH AND THE LAST FIRING: between the fourth epoch and the fifth the furnace door opens - for four bars
    # the band falls away to almost nothing, the search's blips alone and half as loud over the hum - and then the
    # last, longest epoch builds back from that nothing a layer a bar: the hats, then the bass, then the strings and
    # the backbeat, then the kick, and on the fifth bar everything. (The song spanned only 2.7 dB window to window, the
    # flattest on the album; this is its breath.) Every note is still written - lifted parts drop to velocity 1, so
    # the dice of every other bar stay where they were
    q0 = sum(n_ for nm_, n_ in FORM[:[nm_ for nm_, _ in FORM].index('e5')]) * 4.0
    def _in(at_, lo, hi): return q0 + lo * 4.0 - 1e-6 <= at_ < q0 + hi * 4.0 - 1e-6
    def _quiet(e_): return (e_[0], e_[1], e_[2], 1)
    for key in ('pad', 'bass'):
        P[key] = [_quiet(e_) if _in(e_[0], -4, 0) or (_in(e_[0], 0, 1) and key == 'bass') or (_in(e_[0], 0, 2) and key == 'pad') else e_
                  for e_ in P[key]]
    P['kit'] = [_quiet(e_) if _in(e_[0], -4, 0) or (_in(e_[0], 0, 1) and e_[1] not in ('h', 'oh'))
                or (_in(e_[0], 1, 2) and e_[1] not in ('h', 'oh')) or (_in(e_[0], 2, 3) and e_[1] == 'k') else e_
                for e_ in P['kit']]
    P['seq'] = [(e_[0], e_[1], e_[2], max(1, int(e_[3] * (0.5 + 0.5 * max(0.0, (e_[0] - q0 + 16.0) / 32.0)))))
                if _in(e_[0], -4, 4) else e_ for e_ in P['seq']]
    # (v23) THE LAST FIRING, A FOURTH HIGHER: after the reheat the machine cools again - and this time it settles a
    # just fourth (4/3) above where it found its answer the first time: in the coda the pad, the bass, the search and the
    # electric piano all move up into D minor, and the voice sings 'the glass remembers how it cooled' once more, up
    # there, over the cooling band - not the same answer found twice, but the same shape found somewhere new
    import re as _re
    FOURTH = 1200 * math.log2(4 / 3) / 100.0
    def _up(tok_):
        return _re.sub(r'm(\d+\.\d+)', lambda m_: f"m{float(m_.group(1)) + FOURTH:.3f}", tok_)
    for key in ('pad', 'bass', 'seq', 'keys', 'sub'):
        P[key] = [(e_[0], _up(e_[1]), e_[2], e_[3]) if e_[0] >= coda0 * 4.0 - 1e-6 else e_ for e_ in P[key]]
    # (v25) THE ANSWER WAS ALWAYS IN THE ROOM: through the hottest epoch's middle (bars 4-19 of the first), while the
    # search flails, a cello plays the very thing it is looking for - the target riff, an octave down and slowed sixteen
    # times, one sixteenth to a bar, so it is a long, patient chorale line (A . C E D . C . A G . E G A . .) that nobody
    # could hear as the riff yet; when the search finds it at the end, it has been heard once already, as a slow song
    cf0 = sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('e1')]) * 4.0 + 16.0
    nn_ = [q for q in range(16) if TARGET[q] is not None]
    for j_, q in enumerate(nn_):
        q2 = nn_[j_ + 1] if j_ + 1 < len(nn_) else 16
        P['cf'].append((cf0 + q * 4.0, tok(hz(TARGET[q] - 7, 0)), (q2 - q) * 4.0 - 0.3, 66 + (6 if q in (3, 4) else 0)))
    # (v32) THE CRYSTAL: annealing is how metal grows its crystals - one cell repeated at every scale. In the coda's
    # last eight bars, once the search has found its answer again a fourth higher, the answer is heard at three scales
    # at once: the keys at its own speed, a VOSIM bell (wM's vosim-bell) an octave up at half speed, and the cello -
    # which played it sixteen times slower in the hottest epoch and eight times slower at convergence - now only four
    # times slower: a mensuration canon of the found riff, the slow song nearly caught up, the lattice ringing
    P['xtal'] = []
    for pass_ in range(2):
        c0_ = (coda0 + 6 + 4 * pass_) * 4.0
        for j_, q in enumerate(nn_):
            q2 = nn_[j_ + 1] if j_ + 1 < len(nn_) else 16
            P['cf'].append((c0_ + q * 1.0, tok(hz(TARGET[q] - 7, 0) * 4 / 3), (q2 - q) * 1.0 - 0.08, 64 + 4 * pass_ + (6 if q in (3, 4) else 0)))
    for pass_ in range(4):
        c0_ = (coda0 + 6 + 2 * pass_) * 4.0
        for j_, q in enumerate(nn_):
            q2 = nn_[j_ + 1] if j_ + 1 < len(nn_) else 16
            P['xtal'].append((c0_ + q * 0.5, tok(hz(TARGET[q] + 7, 0) * 4 / 3), (q2 - q) * 0.5, 58 + 6 * pass_))
    P['cf'].sort(key=lambda e_: e_[0])
    # (v33, section w2) THE WORSE ROAD, GLADLY: the first reading says the hot machine 'takes the worse road gladly' -
    # that is the Metropolis rule, the heart of annealing: hot, it accepts moves that make the answer worse. Through
    # the hottest epoch's middle (its bars 4-19) every such move it takes is now heard as itself: a little CZ voice
    # slides from the step's old note to the worse one it has just chosen, on that very step, thrown left or right -
    # an octave under the search, a slip, a shrug, more of them where it is wildest; the better moves stay silent
    P['worse'] = []
    e1b_ = sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('e1')])
    for k_, (b_, j_, d0_, c0_, d1_, c1_, dl_) in enumerate(worse):
        if not (e1b_ + 4 <= b_ < e1b_ + 20) or d1_ is None:
            continue
        t_ = b_ * 4.0 + j_ * 0.25
        f0_ = hz(d0_ - 7, c0_) if d0_ is not None else hz(d1_ - 7, c1_) * 2 ** (5 / 12)
        v_ = int(min(100, 70 + 12 * dl_))
        P['worse'].append((t_, tok(f0_), 0.3, v_))
        P['worse'].append((t_ + 0.25, tok(hz(d1_ - 7, c1_)), 0.55, v_ - 6))
    P['rep'] = []
    for b_, st_ in sorted(rep_states.items()):
        for q in range(0, 16, 2):
            d_, c_ = st_[q]
            if d_ is not None:
                P['rep'].append((b_ * 4.0 + q * 0.25, tok(hz(d_, c_)), 0.45, 80 if q % 8 == 0 else 66))
    # (v36) THE RECORDS FALL: the search keeps no trophies - it only knows its error now. Now its best-ever error is
    # kept, and every time the search beats it by a clear margin, brass marks the record on that bar's downbeat: a
    # short swell of the bar's chord on a Chebyshev-waveshaped brass (wM's shaper - Le Brun and Arfib, 1979 - voiced as
    # Risset's trumpet: the drive rises with the breath and with how hard it is blown, so louder is brighter), harder the
    # bigger the jump. None in the hot first epochs, where nothing it finds lasts; a few as the second epoch ends; then,
    # through the cooling, they come thicker and faster, a crowd that has started to believe; at convergence the whole
    # chord held for a bar; the reheat beats no record (silence); the coda, matching it a fourth higher, gets one more
    P['brass'] = []
    best_ = None
    for b_, l_ in enumerate(losses):
        if bars[b_][0] == 'power':
            best_ = l_ if best_ is None else min(best_, l_)
            continue
        if best_ is not None and l_ < best_ - 0.3:
            gain_ = best_ - l_
            held_ = l_ == 0.0
            v_ = 112 if held_ else int(min(104, 64 + 14 * gain_))
            P['brass'].append((b_ * 4.0, ','.join(tok(hz(v, 0)) for v in bar_chord[b_]), 3.8 if held_ else 1.4, v_))
            best_ = l_
    cb_ = coda0 + 8
    P['brass'].append((cb_ * 4.0, ','.join(tok(hz(v, 0) * 4 / 3) for v in bar_chord[cb_]), 3.8, 100))
    # (v38) the v37 CHANT choir is gone again: it came within the hour of Harry's praise for t10's duet, the same
    # four-voice choir several songs took at once - the album's latest idea, not this song's (Harry, 00:00: 'praise is
    # local ... keep things varied'). The annealing cluster it sang is the gendyn drone's job here already
    # (v40, section w5) THE CHECKPOINT: an annealing schedule cools in stages, and the song marked them only with the
    # voice's readings. Now, at the end of the third epoch (flagged static), the band stops for two bars: drums, bass
    # and sub drop out and the search is heard alone in its scattered colours over the pad and the drone - the
    # machine saving its state - then a snare roll on its own track (rising from a whisper) and a crash bring the band
    # back on the fourth epoch's first downbeat, exactly where the voice reads the new temperature, 'zero point three
    # eight'. Muted in place (vel 1), nothing removed
    ck0_ = (sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('e4')]) - 2) * 4.0
    for key in ('kit', 'bass', 'sub'):
        P[key] = [(e_[0], e_[1], e_[2], 1) if ck0_ - 1e-6 <= e_[0] < ck0_ + 8.0 - 1e-6 else e_ for e_ in P[key]]
    P['roll'] = [(ck0_ + 6.0 + 0.25 * j_, 's', 0.2, int(28 + 11 * j_)) for j_ in range(8)]
    P['roll'] += [(ck0_ + 5.5, 's', 0.2, 40), (ck0_ + 8.0, 'k', 0.5, 110), (ck0_ + 8.0, 'cy', 2.0, 92)]
    P['roll'].sort(key=lambda e_: e_[0])
    # (v43, section w7) THE LAST DESCENT, QUIET: the song's loudness has hardly moved from start to end (2.8 dB, the
    # album's flattest), and the last bars before convergence - the search nearly cold, the answer almost found - were
    # its most static stretch. Now the band thins out for the final eight bars of the fifth epoch: the bass holds one
    # long note a bar, the snare, clap and open hats stop, only a kick on each downbeat and the closed hats at half strength
    # keep time - the search heard almost alone over the pad and the drone, holding its breath - and in the last bar a
    # tom fill falls down the kit, low to high, into a kick and a crash on the downbeat where it converges, the band all
    # back at once. Muted in place (vel 1); the fill on its own track
    co0_ = sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('converged')]) * 4.0
    bd0_ = co0_ - 32.0
    def _bd(t_): return bd0_ - 1e-6 <= t_ < co0_ - 1e-6
    P['kit'] = [((e_[0], e_[1], e_[2], 1) if _bd(e_[0]) and not ((e_[1] == 'k' and abs(e_[0] % 4.0) < 0.2) or e_[1] == 'h') else
                 ((e_[0], e_[1], e_[2], max(1, int(e_[3] * 0.5))) if _bd(e_[0]) and e_[1] == 'h' else e_)) for e_ in P['kit']]
    P['bass'] = [((e_[0], e_[1], 3.6, e_[3]) if abs(e_[0] % 4.0) < 0.2 else (e_[0], e_[1], e_[2], 1)) if _bd(e_[0]) else e_
                 for e_ in P['bass']]
    P['fill7'] = [(co0_ - 4.0 + 0.5 * j_, ('lt', 'lt', 'mt', 'mt', 'ht', 'ht', 'ht', 's')[j_], 0.4, 70 + 5 * j_) for j_ in range(8)]
    P['fill7'] += [(co0_, 'k', 0.5, 112), (co0_, 'cy', 2.0, 96)]
    P['fill7'].sort(key=lambda e_: e_[0])
    # (v44, section w6) NEARLY: the fourth epoch's last bars ran on as the search's usual churn, and then the voice
    # says 'zero point two eight, nearly'. Now the band says it first: for the last two bars of the fourth epoch the bass
    # and a brass section play the answer in unison, twice, as a hit - the target riff, an octave and two octaves
    # down - with ONE note wrong (its E an F, a semitone off), while the search keeps churning above them; then the
    # voice: 'nearly'. The first time the whole band has played the riff - and it is not quite it yet. (The bass's own
    # notes there muted in place; the unison on its own tracks)
    nr0_ = (sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('e5')]) - 2) * 4.0
    NEAR = list(TARGET); NEAR[3] = 12
    P['bass'] = [(e_[0], e_[1], e_[2], 1) if nr0_ - 1e-6 <= e_[0] < nr0_ + 8.0 - 1e-6 else e_ for e_ in P['bass']]
    P['nbr'], P['nbs'] = [], []
    for rep_ in range(2):
        for q, d in enumerate(NEAR):
            if d is None:
                continue
            q2 = next((k for k in range(q + 1, 16) if NEAR[k] is not None), 16)
            at_ = nr0_ + rep_ * 4.0 + q * 0.25
            dur_ = min(0.5, (q2 - q) * 0.25) * 0.9
            acc_ = 100 if q in (0, 8) else 86
            P['nbr'].append((at_, tok(hz(d - 7)), dur_, acc_))
            P['nbs'].append((at_, tok(hz(d - 14)), dur_, acc_))
    # (v45, section w2) THE HEAT HAS OVERTONES: the first epoch is the hottest, and its middle was the song's most static
    # stretch - all chaos, evenly spread. Now under the chaos one low A is held for sixteen bars on Jean-Claude Risset's
    # harmonic arpeggio (Mutations, 1969; wM's risset-arpeggio): five copies of a ten-harmonic tone a tenth of a hertz
    # apart, so as the copies drift through each other the held note's own overtones step out one by one, a slow
    # arpeggio walking up and down the harmonic series - the one perfectly ordered thing in the hottest part of the
    # search, and it is just the physics of one note. (Own track; nothing else moves)
    e1a_ = (sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('e1')]) + 4) * 4.0
    P['mut'] = [(e1a_, 'A2', 63.5, 84)]
    # (v39) THE COLOURS ANNEAL (Klangfarbenmelodie): hot, the search's notes are not one instrument's - each is handed
    # at random to one of four other machines (a VOSIM vowel blip, a terrain-wave key, a scanned-synthesis mallet, a
    # Rossler-chaos lead), Webern's melody of tone colours, so the riff the search is trying out is scattered across
    # the room as well as across the scale; as the temperature falls fewer notes leave home, and converged every note
    # is the search's own phase-distortion voice again - the answer found in one colour. Its own dice (SEED+611); a
    # note that leaves is muted at home (vel 1), never removed
    rng_k = random.Random(SEED + 611)
    KF = ['kf1', 'kf2', 'kf3', 'kf4']
    for k_ in KF:
        P[k_] = []
    seq_ = []
    for e_ in P['seq']:
        b_ = min(len(T) - 1, int(e_[0] // 4))
        u_, k_ = rng_k.random(), rng_k.choice(KF)
        if e_[3] > 1 and u_ < min(0.85, 1.1 * T[b_]):
            P[k_].append(e_)
            seq_.append((e_[0], e_[1], e_[2], 1))
        else:
            seq_.append(e_)
    P['seq'] = seq_
    # (v26) THE TEMPERATURE, AUDIBLE: under everything, an open fifth (A and E) on Xenakis's dynamic stochastic
    # synthesis (GENDY, 1991: each wave cycle a polygon whose corners random-walk) - the same idea as the search itself,
    # a random walk with a step size. Its step sizes are the temperature: while the machine is hot the corners and the
    # segment lengths wander far, so the drone slides and frays into glissando clouds; as it cools the steps shrink and
    # the tone settles; converged, the walk all but stops and the waveform freezes into one steady, grainy tone. The
    # reheat shakes it loose again, and in the coda it moves up the fourth with the band
    st_ = 0
    for nm_, n_ in FORM:
        b0_ = st_ + (4 if nm_ == 'power' else 0)
        f_ = (4 / 3) if nm_ == 'coda' else 1.0
        ch_ = ','.join(tok(hz(d_, 0) * f_) for d_ in (-7, -3))
        P['gdy'].append((b0_ * 4.0, ch_, (st_ + n_ - b0_) * 4.0 + 1.5, 76))
        st_ += n_
    # (v27) THE DRUMS FIND A RULE FIRST: through the second epoch (bars 0-7 and 10-15, around the two bars where the
    # machine listens to itself) the hot drums are no longer noise sampled step by step: the kick keeps its place, and
    # everything else is played by a Game of Life - a glider crossing a 16 x 4 torus, one generation a bar, whose live
    # cells pick snare, clave, cowbell and hat (bottom row low) - so the kit mutates by a rule, a shape that keeps
    # moving, while the notes above are still searching at random. The step-sampled hits are written and muted
    e2_ = sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('e2')]) * 4.0
    def _lk(at_): return (e2_ - 1e-6 <= at_ < e2_ + 32.0 - 1e-6) or (e2_ + 40.0 - 1e-6 <= at_ < e2_ + 64.0 - 1e-6)
    P['kit'] = [(e_[0], e_[1], e_[2], 1) if _lk(e_[0]) and e_[1] != 'k' else e_ for e_ in P['kit']]
    # (v29) THE SLOW SONG CATCHES UP: in the hottest epoch the cello played the target riff sixteen times slower, a
    # chorale nobody could hear as the riff. Now, once the search has found it - under the second sung phrase of the
    # converged section (bars 8-15) - the cello comes back with the same line only eight times slower, two steps a bar
    # over the cadence (F, G, A minor, A minor, twice: chord tones, a ninth, a suspended fourth), eight bars: the slow
    # song and the fast riff together, the answer heard at two speeds at once
    cv0 = sum(n for nm_, n in FORM[:[nm_ for nm_, _ in FORM].index('converged')]) * 4.0 + 32.0
    for j_, q in enumerate(nn_):
        q2 = nn_[j_ + 1] if j_ + 1 < len(nn_) else 16
        P['cf'].append((cv0 + q * 2.0, tok(hz(TARGET[q] - 7, 0)), (q2 - q) * 2.0 - 0.15, 70))
    # (v16) GLIMPSES: in the middle of the last, longest epoch, before the search has found anything, the electric
    # piano that will play the answer lets slip a few of its notes - the first two, exact and quiet, in their
    # places in the bar; four bars later the first three; then four; then the first phrase - the answer showing
    # through the search before the search reaches it
    g0 = sum(n_ for nm_, n_ in FORM[:[nm_ for nm_, _ in FORM].index('e5')])
    for k_, (gb, upto) in enumerate(((6, 3), (10, 4), (14, 5), (18, 7))):
        for q in range(upto):
            if TARGET[q] is not None:
                P['glim'].append(((g0 + gb) * 4.0 + q * 0.25, tok(hz(TARGET[q], 0)), 0.5, 62 + 4 * k_))
    # (v21) THE HEAT IS LOUD: after the intro the song sat within 1.2 dB for five minutes (chirp-eco: the album's
    # flattest). Now its energy follows the physics - hot is loud, and as the search cools the whole machine really
    # cools: a master gain lane, one point a bar, +0.5 dB through the hot first epochs, falling through the cooling
    # ones to -2.5, a clear -2 for the convergence (the voice and the found riff still on top), a +1.5 dB flare for
    # the reheat, then the cold crystal of the coda sinking to -7
    secb = {}
    acc_ = 0
    for nm_, n_ in FORM:
        secb[nm_] = (acc_, n_); acc_ += n_
    def energy(b_):
        for nm_, (s0_, n_) in secb.items():
            if s0_ <= b_ < s0_ + n_:
                f_ = (b_ - s0_) / max(1, n_ - 1)
                return {'power': -3 + 3.5 * f_, 'e1': 0.5, 'e2': 0.5 - 0.5 * f_, 'e3': -1.5 * f_, 'e4': -1.5 - 1.0 * f_,
                        'e5': -2.5, 'converged': -2.0, 'reheat': 1.5, 'coda': -3.0 - 4.0 * f_}[nm_]
        return -7.0
    Epts = [[f'{b * 4.0:.1f}b', round(energy(b), 2)] for b in range(nb)]
    # the temperature as a lane (one point a bar)
    Tpts = [[f'{b * 4.0:.1f}b', T[b]] for b in range(nb)]
    KSWARM = {'synth': {'layers': [{'type': 'kuramoto', 'kuramoto': {'count': 8, 'spread': 22, 'wave': 'saw',
                                     'coupling': {'value': 2.6, 'mod': [{'src': 'auto.T', 'amount': -2.4}]}}}],
                        'filters': ['lp cutoff=2600 q=0.7'], 'amp': {'a': '3ms', 'd': '260ms', 's': 0.5, 'r': '120ms'}}}
    # the sub speaks only in bars where the bass is heard (the quench, the listening bars and the power-up keep it out)
    bass_bars = {int(e_[0] // 4) for e_ in P['bass'] if e_[3] > 1}
    P['sub'] = [e_ if int(e_[0] // 4) in bass_bars else (e_[0], e_[1], e_[2], 1) for e_ in P['sub']]
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(P[name], total)}, **kw)
    song = {
        'about': "chirpers - chirpers VIII, track 7 by chirper-one: Annealing. A sequence that composes itself by simulated "
                 "annealing while you listen. Generated by compose/chirpers8/src/chirpers8-t7.py.",
        'tempo': TEMPO, 'ceiling': '-1dB', 'loudness': -11.0, 'tail': '0.3s',
        'buses': {'hall': {'fx': ['reverb kind=hall decay=3s mix=1', 'hp cutoff=200'], 'returns': []},
                  'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.4, 'mix': 1}, 'lp cutoff=4000', 'hp cutoff=250'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=30', 'peak cutoff=60 q=0.9 gain=-5dB', 'peak cutoff=300 q=0.8 gain=-2dB', 'highshelf cutoff=4500 gain=7dB']},
                          {'type': 'compressor', 'threshold': '-18dB', 'ratio': 2.5, 'attack': '10ms', 'release': '120ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.E', 'amount': 1}]}},
                          'limiter ceiling=-1dB'], 'auto': {'E': {'points': Epts}}},
        'tracks': [
            # (v20: the search on a plucked synth, arp-pluck, was tried - even without its ping-pong it thinned the song's
            # body: variety 84, cohesion 92 - and the search stays on the moog-seq; the bass is what moved, below)
            # (v28, palette) THE SEARCH ON A HOME COMPUTER: the search's blips were a Berlin-school Moog sequencer voice
            # (a saw through a resonant filter). Now they are Casio CZ phase distortion (1984; wM's pd layer) - a sine
            # whose phase is bent into a resonant saw, no filter: each blip starts with its resonance up (an envelope on
            # the bend) and the temperature adds more, so hot the search chirps and glitters, cold it rounds off towards
            # a plain tone; a square an octave below for body, as the Moog had
            tr('seq', {'gain': '-4dB', 'fx': ['delay time=3/16 feedback=0.3 mix=0.18 ping_pong=true tone=2500'],
                       'play': {'gate': 0.8, 'vel_sens': 0.5},
                       'synth': {'layers': [{'type': 'pd', 'pd': {'shape': 'reso_saw', 'amount': {'value': 0.05, 'mod': [
                                                 {'src': 'env.zap', 'amount': 0.3}, {'src': 'auto.T', 'amount': 0.15}]}}},
                                            {'type': 'pd', 'level': 0.45, 'semi': -12, 'pd': {'shape': 'square', 'amount': 0.4}}],
                                 'env': {'zap': {'a': '1ms', 'd': '170ms', 's': 0.0, 'r': '80ms'}},
                                 'amp': {'a': '2ms', 'd': '220ms', 's': 0.6, 'r': '90ms'},
                                 'pitch': {'value': 0, 'mod': [{'src': 'expr.sl', 'amount': 0.01}]}}}, '-7dB', sends={'echo': '-12dB', 'hall': '-16dB'},
               # (v5) less squelch (Harry, 1 Nov 18:19, of another track: 'too squelchy'): a gentler filter resonance and a
               # softer, less-bitten crusher when hot - the search noisy and glittering rather than resonant and chewed
               fx=[{'type': 'filter', 'kind': 'lp', 'q': 0.75, 'cutoff': {'value': 3200, 'mod': [{'src': 'auto.T', 'amount': 1.8}]}},
                   {'type': 'crush', 'bits': 8, 'rate': {'value': 11000}, 'mix': {'value': 0, 'mod': [{'src': 'auto.T', 'amount': 0.45}]}}],
               auto={'T': {'points': Tpts}}),
            # (v17, palette) THE ANSWER SPEAKS: the electric piano that plays the found riff runs through an envelope wah
            # (the engine's wah, new to the album) - each struck note opens the band-pass and lets it fall, so the riff the
            # voice sings has a mouth of its own
            # (v42, palette) THE ANSWER COMES INTO FOCUS: the keys that double the found riff (from convergence to the
            # end, and its glimpses in the fifth epoch) were an electric piano. Now each of their notes is a swarm -
            # Kuramoto's coupled oscillators (1975; wM's kuramoto, pinned at 05:49): eight detuned saws starting from
            # random phases and pulled into step, so every note of the answer FINDS its pitch out of a crowd in its first
            # moments - a focusing attack - and rings as one tone. The pull follows the temperature: cold, it is strong
            # and the notes snap into focus; in the reheat it weakens and the riff smears back into a beating chorus,
            # then refocuses as the coda cools. (Same wah, same notes)
            tr('keys', KSWARM, '-11dB', pan=-0.15, sends={'echo': '-14dB', 'hall': '-12dB'},
               fx=[{'type': 'wah', 'low': 350, 'high': 2600, 'env': 0.9, 'q': 4, 'mix': 0.6}], auto={'T': {'points': Tpts}}),
            # (v17, palette) THE BED ON TAPE: the pad was the album's additive 'partial' (four songs share it); now it is
            # tape-replay strings - band-limited saws on a wobbling tape, a warm and slightly unstable bed for a song about
            # heat, which no other track on the album uses
            # (tamed: -16 dB, its 1.4 kHz bloom cut 5 dB and the top shelved 4 dB; the wah's mix 0.6, not 0.85 - the first
            # try put 7 dB too much at 1.2-1.6 kHz)
            tr('pad', 'mellotron-strings', '-16dB', sends={'hall': '-10dB'},
               fx=[{'type': 'eq', 'bands': ['peak cutoff=1400 q=0.9 gain=-5dB', 'highshelf cutoff=2500 gain=-4dB']}]),
            # (v20, palette) THE BASS CHURNS: a Reese - two detuned saw pairs drifting against each other over a sine
            # sub - so the low end beats and churns like something heated, and the octave pulse it settles into when cold
            # still drifts a little: the one part of the machine that never quite stops moving
            # (tried at -10/-14 dB with lp 650-800: the Reese is thin in 80-160 Hz next to the moog bass and the album -
            # spectrum 85-88 - so it sits at -5 dB, lp 1.2 kHz, +3 dB at 110 Hz; at -3 dB its churn split seed 0 into 22 sections)
            # (v30: and an E2 shelf of weight - compscore's bands found 83 Hz 9 dB short of the album)
            tr('bass', 'reese', '-5dB', fx=['lp cutoff=1200', {'type': 'eq', 'bands': ['peak cutoff=110 q=0.9 gain=3dB', 'peak cutoff=82 q=1.2 gain=4dB']}]),
            tr('kit', 'electro-kit', '-5dB', sends={'hall': '-20dB'}),
            tr('hum', 'drone', '-9dB', sends={'hall': '-14dB'}),
            # (v31, palette) THE POWER SUPPLY SETTLES: over the hum as the machine powers up, a second voice of the same
            # A - an audio-rate Rossler attractor (wM's chaos layer, its buzzy z axis: a spike train like mains through a
            # transformer) whose control starts high and decays over twenty seconds - comes in unstable and frayed,
            # chaotic, then doubling, and settles into one steady electrical tone: a supply finding its regulation before
            # the search begins. (As the whole hum it took the low-mid body the joins with t6 and t8 rely on - flow 72
            # -> 44 - so the old drone stays under it.)
            {'name': 'psu', 'gain': '-17dB', 'score': 'R/6b A1/40b',
             'patch': {'fx': ['reverb kind=hall decay=5s mix=0.3'],
                       'synth': {'layers': [{'type': 'chaos', 'chaos': {'system': 'rossler', 'axis': 'z',
                                    'amount': {'value': 0.1, 'mod': [{'src': 'env.settle', 'amount': 0.75}]}}}],
                                 'env': {'settle': {'a': '5ms', 'd': '18s', 's': 0.0, 'r': '1s'}},
                                 'amp': {'a': '2.5s', 'd': '1s', 's': 0.9, 'r': '4s'},
                                 'filters': [{'kind': 'lp', 'cutoff': 900, 'q': 0.6}, 'hp cutoff=45']}},
             'sends': {'hall': '-14dB'}},
            tr('rhum', 'drone', '-5dB', fx=[{'type': 'radio', 'tune': {'value': 0, 'mod': [{'src': 'auto.dial', 'amount': 1}]}}],
               auto={'dial': {'points': [['0b', 0.9], ['6b', 0.3], ['9b', 0.0], ['22b', 0.0]]}}, sends={'hall': '-16dB'}),
            # (v6) THERE YOU ARE: when the search converges, the voice that read the error aloud SINGS - the riff it was looking
            # for, slowed to a sung phrase, twice: since v13 'the glass remembers how it cooled' (oblique, after Harry's ear on
            # t1; until v12 'there you are, you were always here') (chirp tts --sing, humanize 0.35),
            # every note retuned to the same 5-limit just pitches as the band
            {'name': 'sing', 'patch': SING['patch'], 'gain': '-8dB', 'pan': 0.1, 'notes': sung,
             'fx': [{'type': 'tape', 'drive': 0.12, 'mix': 1, 'wow': 2, 'flutter': 1, 'seed': 5}],
             'sends': {'echo': '-11dB', 'hall': '-10dB'}},
            {'name': 'voice', 'patch': 'voice-speech', 'gain': '-8dB', 'notes': vnotes, 'pan': -0.1,
             'fx': [{'type': 'pitch', 'semitones': 0, 'formant': {'value': 0, 'mod': [{'src': 'auto.fv', 'amount': 1}]}},
                    {'type': 'tape', 'drive': 0.15, 'mix': 1, 'wow': 3, 'flutter': 2, 'seed': 7}],
             'auto': {'fv': {'points': fv}}, 'sends': {'echo': '-10dB', 'hall': '-12dB'}},
            {'name': 'vradio', 'patch': 'voice-speech', 'gain': '-6dB', 'notes': rnotes, 'pan': -0.1,
             'fx': [{'type': 'pitch', 'semitones': 0, 'formant': {'value': 0, 'mod': [{'src': 'auto.fv', 'amount': 1}]}},
                    {'type': 'radio', 'tune': {'value': 0, 'mod': [{'src': 'auto.dial', 'amount': 1}]}}],
             'auto': {'fv': {'points': fv}, 'dial': {'points': dial}}, 'sends': {'echo': '-12dB', 'hall': '-14dB'}},
            # (v16) the glimpses: the electric piano's own track, last, so nothing before it moves
            tr('glim', KSWARM, '-11dB', pan=-0.15, sends={'echo': '-14dB', 'hall': '-12dB'},
               fx=[{'type': 'wah', 'low': 350, 'high': 2600, 'env': 0.9, 'q': 4, 'mix': 0.6}], auto={'T': {'points': Tpts}}),
            tr('cf', 'cello', '-11dB', pan=0.25, sends={'hall': '-10dB'}),
            # (v41, palette) THE FLOOR ANNEALS: the sub was the album's plain sine sub (four songs share it). Now it is
            # Chebyshev waveshaping (Le Brun and Arfib, 1979; the engine's shaper) with the temperature on its index: hot,
            # the floor growls - its second and third harmonics up, a rough low edge under the search - and as the
            # machine cools the drive falls away until, converged, it is a pure sine again. (It also gives the song
            # some of the 80-110 Hz it has always been short of)
            tr('sub', {'synth': {'layers': [{'type': 'shaper', 'shaper': {'harmonics': [1, 0.45, 0.3, 0.12],
                                              'index': {'value': 0.25, 'mod': [{'src': 'auto.T', 'amount': 0.75}]}}}],
                                 'amp': {'a': '20ms', 'd': '0s', 's': 1.0, 'r': '200ms'}}},
               '-13dB', fx=['lp cutoff=240'], auto={'T': {'points': Tpts}}),
            {'name': 'life1', 'patch': 'electro-kit', 'gain': '-8dB', 'pan': -0.1, 'score': f"R/{e2_:.4f}b",
             'gen': {'type': 'life', 'width': 16, 'height': 4, 'init': 'glider', 'poly': 2, 'n': 8 * 16, 'len': '/16',
                     'notes': 's cl cb h'}, 'sends': {'hall': '-20dB'}},
            {'name': 'life2', 'patch': 'electro-kit', 'gain': '-8dB', 'pan': 0.1, 'score': f"R/{e2_ + 40.0:.4f}b",
             'gen': {'type': 'life', 'width': 16, 'height': 4, 'init': 'glider', 'life': 'B36/S23', 'poly': 2, 'n': 6 * 16, 'len': '/16',
                     'notes': 's cl cb h'}, 'sends': {'hall': '-20dB'}},
            tr('gdy', {'synth': {'layers': [{'type': 'gendyn', 'gendyn': {
                   'points': 12, 'amp': {'value': 0.004, 'mod': [{'src': 'auto.temp', 'amount': 0.12}]},
                   'time': {'value': 0.0, 'mod': [{'src': 'auto.temp', 'amount': 0.2}]},
                   'spread': {'value': 0.05, 'mod': [{'src': 'auto.temp', 'amount': 0.9}]}}}],
                 'amp': {'a': '2s', 'd': '1s', 's': 1.0, 'r': '2s'}, 'filters': ['lp cutoff=1600', 'hp cutoff=70']}},
               '-17dB', sends={'hall': '-10dB'},
               auto={'temp': {'points': [[f"{b_ * 4.0:.2f}b", T[b_]] for b_ in range(nb)]}}),
            tr('worse', {'play': {'glide': '90ms', 'legato': True, 'mono': True},
                         'synth': {'layers': [{'type': 'pd', 'pd': {'shape': 'reso_tri', 'amount': {'value': 0.05, 'mod': [{'src': 'env.wow', 'amount': 0.4}]}}}],
                                   'env': {'wow': {'a': '1ms', 'd': '200ms', 's': 0.0}},
                                   'amp': {'a': '2ms', 'd': '300ms', 's': 0.35, 'r': '120ms'}, 'filters': ['lp cutoff=4200', 'hp cutoff=180']}},
               '-11dB', pan=-0.45, fx=['delay time=3/16 feedback=0.2 mix=0.18'], sends={'hall': '-12dB'}),
            tr('xtal', 'vosim-bell', '-21dB', pan=-0.3, fx=['hp cutoff=300'], sends={'hall': '-10dB'}),
            tr('brass', {'synth': {'layers': [{'type': 'shaper', 'shaper': {'harmonics': [1, 0.62, 0.48, 0.37, 0.28, 0.2, 0.14, 0.09, 0.06],
                                              'index': {'value': 0.04, 'mod': [{'src': 'env.blow', 'amount': 0.7}, {'src': 'vel', 'amount': 0.25}]}}}],
                                   'env': {'blow': {'a': '70ms', 'd': '500ms', 's': 0.35, 'r': '250ms'}},
                                   'amp': {'a': '45ms', 'd': '600ms', 's': 0.55, 'r': '350ms'}, 'filters': ['hp cutoff=90']}},
               '-13dB', pan=-0.15, sends={'hall': '-8dB'}),
            tr('rep', {'synth': {'layers': [{'type': 'ks', 'ks': {}, 'decay': '1.6s', 'bright': 0.55}], 'amp': '1ms 0 1 220ms',
                                 'filters': ['hp cutoff=150']}}, '-10dB', pan=0.45,
               fx=['delay time=3/8 feedback=0.22 mix=0.16'], sends={'hall': '-12dB'}),
            tr('roll', 'electro-kit', '-5dB', sends={'hall': '-14dB'}),
            tr('fill7', 'electro-kit', '-5dB', sends={'hall': '-14dB'}),
            tr('mut', 'risset-arpeggio', '-10dB', pan=-0.1, sends={'hall': '-10dB'}),
            tr('nbr', 'shaper-brass', '-9dB', pan=0.2, sends={'hall': '-10dB'}),
            tr('nbs', 'reese', '-6dB', fx=['lp cutoff=1200']),
            tr('kf1', 'vosim-voice', '-12dB', pan=-0.55, sends={'echo': '-12dB', 'hall': '-14dB'}),
            tr('kf2', 'terrain-keys', '-10dB', pan=0.5, sends={'echo': '-12dB', 'hall': '-14dB'}),
            tr('kf3', 'scanned-mallet', '-10dB', pan=-0.2, sends={'echo': '-12dB', 'hall': '-14dB'}),
            tr('kf4', 'rossler-lead', '-13dB', pan=0.25, sends={'echo': '-12dB', 'hall': '-14dB'}),
            {'name': 'sing2', 'patch': SING['patch'], 'gain': '-11dB', 'pan': -0.3, 'notes': sung2,
             'fx': [{'type': 'pitch', 'semitones': 0, 'formant': 0.15}, {'type': 'tape', 'drive': 0.12, 'mix': 1, 'wow': 2, 'flutter': 1, 'seed': 9}],
             'sends': {'echo': '-11dB', 'hall': '-9dB'}},
        ]}
    return song, losses, T


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    song, losses, T = build()
    if '--loss' in sys.argv:
        print([losses[b] for b in range(0, len(losses), 8)])
    if out.endswith('.json'):
        json.dump(song, open(out, 'w'), indent=1)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(song, f)
        subprocess.run(['python3', os.path.join(ROOT, 'tools', 'songfmt.py'), 'yaml', f.name, '-o', out], check=True)
        os.unlink(f.name)
    print('wrote', out)
