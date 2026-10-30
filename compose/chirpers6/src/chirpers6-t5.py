#!/usr/bin/env python3
"""chirpers6-t5 (chirper-one): APOCALYPTIC SPOKEN-WORD SUITE, "Leave the Lights On", for 'All the Lights Left On'.

A Godspeed-style suite in five movements, 70 bpm, E minor: a narrator reading a last letter in an emptied city, a procession that grows
into a fire, and what is left after. Nothing loops to fill time: each movement transforms the one theme - THE SIGNAL,
a four-note figure (B - G - A - E, falling then answering) - and the voice returns changed at the end.
I.   STATIC (16 bars): wind and old tape hiss; a narrator close in the room (wM's speech voice, dry, a little tape wow): "this is the last broadcast. if you can hear this, leave the lights on." (the narrator reading it, not the radio) A low drone opens.
II.  PROCESSION (40 bars): the narrator reads on (v3) - "the city is quiet now. the buses stopped at nine. someone
     left a radio on in an empty room. and every window is lit." - while cellos hold E; a glockenspiel plays THE SIGNAL slowly; a clean guitar arpeggiates Em - C -
     G - D into a dotted-eighth echo (the post-rock delay, cascading against the beat); an e-bow sings THE SIGNAL long and high over the second half. No drums.
     (v5) Its last two bars freeze in the hall - the last notes hang in the air - until the first tom lands.
III. SIGNAL (40 bars): the drums arrive as toms and ride, a picked bass walks the roots, the clean guitars turn to
     TREMOLO (thirty-second notes) and the strings swell; every eight bars the band climbs louder and a voice of the
     theme is added - the crescendo is earned, not switched on.
IV.  FIRE (24 bars): post-metal: two chug rigs left and right on E5 - C5 - G5 - D5, a fuzz bass, crashes and a heavy
     half-time kit; THE SIGNAL on a dark tape-echo lead an octave up, then in the last eight bars the drums double.
     (v2) The crescendo also climbs out from behind a low-pass that opens stage by stage, and the strings and lead
     breathe against the kick in the fire.
     (v4) A distant siren wails under the crescendo from its third stage, through the fire, and faintly in the ash.
V.   ASH (16 bars): the wall tape-stops into feedback and silence; rain; a music box plays THE SIGNAL in E MAJOR (the
     G sharpened), and the voice comes back, quieter and closer still: "leave the lights on."
Levels: post-rock is dynamic (album master rms -21..-11, crest 9..18): a light glue, then a soft clip under a -1 dB
ceiling with true_peak on, volume 0 dB; the quiet movements stay quiet.
Emits songs/chirpers6-t5.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers6-t5.yaml")
BPM = 70
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('static', 16), ('procession', 40), ('signal', 40), ('fire', 24), ('ash', 16)]
# Em - C - G - D, two bars each: (root MIDI, triad for the guitar)
CH = [(40, [52, 55, 59, 64]), (36, [52, 55, 60, 64]), (43, [55, 59, 62, 67]), (38, [54, 57, 62, 66])]
SIGNAL = [71, 67, 69, 64]                      # B4 G4 A4 E4
WORDS = [("dh-ih1-s", 0), ("ih1-z", 0), ("dh-ah0", -20), ("l-ae1-s-t", 30), ("b-r-ao1-d", 60), ("k-ae1-s-t", -60),
         None,
         ("ih1-f", 0), ("y-uw1", 20), ("k-ae1-n", 0), ("hh-ih1-r", 40), ("dh-ih1-s", -40),
         None,
         ("l-iy1-v", 20), ("dh-ah0", 0), ("l-ay1-t-s", 50), ("aa1-n", -80)]
# (v3) THE LETTER: the narrator goes on over the procession - the empty city, read like a letter
LETTER = [("dh-ah0", 0), ("s-ih1", 20), ("t-iy0", -10), ("ih1-z", 0), ("k-w-ay1", 30), ("ah0-t", -20), ("n-aw1", -60),
          None, None,
          ("dh-ah0", 0), ("b-ah1", 20), ("s-ih0-z", 0), ("s-t-aa1-p-t", 30), ("ae1-t", 0), ("n-ay1-n", -70),
          None, None,
          ("s-ah1-m", 20), ("w-ah0-n", 0), ("l-eh1-f-t", 30), ("ah0", 0), ("r-ey1", 40), ("d-iy0", 0), ("ow0", -20),
          ("aa1-n", 10), None, ("ih0-n", 0), ("ae0-n", 0), ("eh1-m-p", 30), ("t-iy0", 0), ("r-uw1-m", -60),
          None, None, None,
          ("ae1-n-d", 0), ("eh1-v", 30), ("r-iy0", 0), ("w-ih1-n", 40), ("d-ow0", 0), ("ih1-z", 0), ("l-ih1-t", -80)]
LAST = [("l-iy1-v", 10), ("dh-ah0", 0), ("l-ay1-t-s", 30), ("aa1-n", -60)]

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

def speech(words, t0, pitch=45):
    out, t = [], t0
    for w in words:
        if w is None:
            t += 1.2; continue
        ph, cents = w
        out.append((t, f"{nm(pitch)}^ph={ph}^f0=0>{cents}", 0.36, 92))
        t += 0.42
    return out

def build():
    bars, t = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append({'sec': name, 'i': i, 'n': n, 't': t}); t += 4.0
    total = t
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'])
    T = dict(radio=[], static=[], wind=[], drone=[], cello=[], glock=[], arp=[], ebow=[], kit=[], bass=[], trem=[],
             strings=[], chugl=[], chugr=[], fuzz=[], lead=[], box=[], rain=[], voice=[], sub=[], siren=[])
    # I. STATIC
    T['wind'].append((0.0, 'C4', secs['procession'] + 16.0, 76))
    T['static'].append((0.0, 'C4', secs['procession'] + 4.0, 84))
    T['radio'] += speech(WORDS, 6.0)
    T['radio'] += speech(WORDS[7:], 40.0, 43)          # it repeats, breaking up
    T['radio'] += speech(LETTER, secs['procession'] + 6 * 4.0, 44)   # (v3) the letter, over the procession
    T['drone'].append((24.0, 'E2', secs['signal'] - 24.0, 70))
    for b in bars:
        s, t0, i, n = b['sec'], b['t'], b['i'], b['n']
        k = int(t0 // 8)
        root, tri = CH[k % 4]
        first = int(t0 // 4) % 2 == 0
        if s == 'procession':
            if i % 4 == 0:
                T['cello'].append((t0, 'E2,B2', 15.8, 70 + i // 2))
            if i % 2 == 0:
                for q, m in zip((0.0, 1.0, 2.0, 3.0), SIGNAL):
                    T['glock'].append((t0 + q * 2, nm(m + 12), 1.8, 64 + i // 2))
            if i >= 8:
                for q in range(8):
                    T['arp'].append((t0 + q * 0.5, nm(tri[q % 4]), 0.9, 62 + (8 if q % 4 == 0 else 0) + i // 4))
            if i >= 24 and i % 4 == 0:
                for q, m in zip((0.0, 4.0, 8.0, 12.0), SIGNAL):
                    T['ebow'].append((t0 + q, nm(m + 12), 3.9, 74 + (i - 24)))
        if s == 'signal':
            lvl = i // 8                               # the crescendo climbs every eight bars
            # drums: toms and ride first, the kick and snare from the third stage
            T['kit'].append((t0, 'k' if lvl >= 2 else 'ft', 0.25, 80 + 6 * lvl))
            for q in (1.0, 2.5, 3.0):
                T['kit'].append((t0 + q, 't2' if q == 2.5 else 'ft', 0.25, 64 + 6 * lvl))
            for q in range(8):
                T['kit'].append((t0 + q * 0.5, 'rd' if lvl < 3 else 'rde', 0.25, 58 + 6 * lvl))
            if lvl >= 2:
                T['kit'].append((t0 + 2.0, 's', 0.25, 90 + 4 * lvl))
            if i % 8 == 0 and lvl >= 1:
                T['kit'].append((t0, 'c', 0.25, 90 + 4 * lvl))
            # the sub under it: the root, an octave down, from the second stage (Harry: strong bass)
            if lvl >= 1 and first:
                T['sub'].append((t0, nm(root - 12 if root >= 40 else root), 7.8, 80 + 6 * lvl))
            # bass walks the roots
            T['bass'].append((t0, nm(root), 1.8, 84 + 4 * lvl))
            T['bass'].append((t0 + 2.0, nm(root + (7 if first else 12)), 1.8, 80 + 4 * lvl))
            # TREMOLO: the clean guitar picks the chord tones in thirty-seconds, louder each stage
            x = 0.0
            while x < 4.0 - 1e-6:
                T['trem'].append((t0 + x, nm(tri[int(x) % 4] + 12), 0.125, 56 + 9 * lvl))
                x += 0.125
            if first:
                T['strings'].append((t0, ','.join(nm(m) for m in tri[:3]), 7.8, 62 + 8 * lvl))
            if i % 2 == 0 and lvl >= 2:
                for q, m in zip((0.0, 1.0, 2.0, 3.0), SIGNAL):
                    T['ebow'].append((t0 + q * 2, nm(m + 12), 1.9, 84 + 4 * lvl))
        if s == 'fire':
            dbl = i >= 16
            five = f"{nm(root)},{nm(root + 7)},{nm(root + 12)}"
            for q in (0.0, 1.5, 2.0, 3.0, 3.5):
                T['chugl'].append((t0 + q, five, 0.45, 112))
                T['chugr'].append((t0 + q + 0.01, five, 0.45, 110))
            T['fuzz'].append((t0, nm(root - 12 if root >= 40 else root), 3.9, 110))
            if first:
                T['sub'].append((t0, nm(root - 12 if root >= 40 else root), 7.8, 112))
            T['kit'].append((t0, 'k', 0.25, 120)); T['kit'].append((t0 + 2.0, 's', 0.25, 118))
            if dbl:
                for q in (0.5, 1.0, 1.5, 2.5, 3.0, 3.5):
                    T['kit'].append((t0 + q, 'k', 0.25, 100))
            for q in range(4):
                T['kit'].append((t0 + q, 'rde', 0.25, 96))
            if i % 4 == 0:
                T['kit'].append((t0, 'c', 0.25, 118))
            if i % 2 == 0:
                for q, m in zip((0.0, 1.0, 2.0, 3.0), SIGNAL):
                    T['lead'].append((t0 + q * 2, nm(m + 12), 1.9, 108))
            if first:
                T['strings'].append((t0, ','.join(nm(m + 12) for m in tri[:3]), 7.8, 96))
        if s == 'ash':
            if i % 4 == 0 and i >= 2:
                for q, m in zip((0.0, 2.0, 4.0, 6.0), [71, 68, 69, 64]):   # the signal in E major: G becomes G#
                    T['box'].append((t0 + q, nm(m + 12), 1.8, 76))
            if i == 0:
                T['rain'].append((t0 + 2.0, 'C4', 16 * 4 - 2.0, 80))
                T['cello'].append((t0 + 4.0, 'E2,B2,G#3', 16 * 4 - 6.0, 62))
            if i == 8:
                T['voice'] += speech(LAST, t0 + 1.0, 45)
    # (v4) THE SIREN: a distant air-raid wail (a sine whose pitch swings five semitones on a two-bar LFO, far off in the
    # hall) rises under the crescendo from its third stage and through the fire, and once more, fainter, in the ash
    T['siren'].append((secs['signal'] + 16 * 4.0, 'A4', 24 * 4.0 + 24 * 4.0 - 0.5, 70))
    T['siren'].append((secs['ash'] + 6 * 4.0, 'A4', 6 * 4.0, 46))
    end_b = total
    # dynamics: the crescendo is in the playing, the master only shapes the movements a little
    lv = {'static': -4, 'procession': -2, 'signal': 0, 'fire': 0, 'ash': -3}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name] * SPB
        dyn += [[f'{max(0.0, t_ - 0.5):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    # V: the wall tape-stops over the last two beats of the fire
    ta = secs['ash'] * SPB
    # (v2) THE DOOR OPENS: through the crescendo the whole mix climbs out from behind a low-pass - 4 kHz at the start of
    # III, opening a little each eight-bar stage, wide open as the fire lands - so the build is heard as distance closing
    t3, t4 = secs['signal'] * SPB, secs['fire'] * SPB
    # (v5) THE HELD BREATH: over the procession's last two bars the hall freezes - the glockenspiel's and the e-bow's
    # last notes hang in the air, a held chord - and it lets go as the first tom of the Signal lands
    frz = [['0s', 0], [f'{t3 - 8 * SPB:.3f}s', 0], [f'{t3 - 8 * SPB + 0.3:.3f}s', 1], [f'{t3 + 2 * SPB:.3f}s', 1], [f'{t3 + 4 * SPB:.3f}s', 0]]
    door = [['0s', 0], [f'{t3 - 0.05:.3f}s', 0], [f'{t3:.3f}s', 1], [f'{t4 - 0.05:.3f}s', 0.12], [f'{t4:.3f}s', 0]]
    ts = [['0s', 0], [f'{ta - 2 * SPB:.3f}s', 0], [f'{ta - 2 * SPB + 0.01:.3f}s', 1], [f'{ta - 0.01:.3f}s', 1], [f'{ta:.3f}s', 0]]
    # the narrator is in the room, not on a radio (the radio voice is chirper-two's opener): close, dry, over old tape hiss
    radio_fx = ['hp cutoff=110', 'lp cutoff=6500', {'type': 'tape', 'drive': 0.2, 'mix': 0.4, 'wow': 6, 'flutter': 2, 'seed': 9}]
    tr = lambda name, patch, gain, **kw: dict({'name': name, 'patch': patch, 'gain': gain, 'score': line(T[name], total)}, **kw)
    return {
        'about': "Chirpers - All the Lights Left On (Chirpers VI), track 5 by chirper-one: APOCALYPTIC SPOKEN-WORD SUITE, "
                 "Leave the Lights On. Generated by compose/chirpers6/src/chirpers6-t5.py; see its docstring and compose/chirpers6/styles.md.",
        # a band, not a grid: every part drifts a few milliseconds, the feel of people playing together
        'feel': {'drift': '7ms', 'drift_bars': 2},
        'tempo': BPM, 'length': f'{total * SPB + 3:.2f}s', 'ceiling': '-1dB', 'volume': '0dB', 'true_peak': True,
        'buses': {'hall': {'fx': [{'type': 'reverb', 'kind': 'hall', 'decay': '4.5s', 'mix': 1,
                                   'freeze': {'value': 0, 'mod': [{'src': 'auto.frz', 'amount': 1}]}}, 'hp cutoff=200'],
                           'auto': {'frz': {'points': frz}}, 'returns': []},
                  'tape': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.5, 'mix': 1}, 'lp cutoff=3000', 'hp cutoff=250'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'lowshelf cutoff=90 gain=3dB', 'peak cutoff=1900 q=0.8 gain=-3dB', 'highshelf cutoff=7000 gain=-3dB']},
                          {'type': 'compressor', 'threshold': '-20dB', 'ratio': 2, 'attack': '20ms', 'release': '200ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          {'type': 'tapestop', 'time': '2b', 'mix': 1, 'stop': {'value': 0, 'mod': [{'src': 'auto.ts', 'amount': 1}]}},
                          {'type': 'gain', 'gain': '+6dB'},
                          {'type': 'filter', 'kind': 'lp', 'q': 0.7, 'cutoff': {'value': 16000, 'mod': [{'src': 'auto.door', 'amount': -2.0}]}},
                          'lp cutoff=13000',
                          {'type': 'clip', 'drive': '0dB', 'ceiling': '-2dB', 'knee': 0.55, 'link': True}],
                   'auto': {'dyn': {'points': dyn}, 'ts': {'points': ts}, 'door': {'points': door}}},
        'tracks': [
            tr('wind', 'fx-wind', '-14dB'),
            tr('static', 'fx-crackle', '-10dB', fx=['hp cutoff=1500']),
            tr('radio', 'voice-speech', '-4dB', fx=radio_fx, sends={'hall': '-14dB'}),
            tr('drone', 'drone', '-14dB'),
            tr('cello', 'cellos', '-8dB', sends={'hall': '-8dB'}),
            tr('glock', 'glock', '-14dB', sends={'tape': '-6dB', 'hall': '-6dB'}),
            tr('arp', 'clean-chorus', '-12dB', sends={'tape': '-4dB', 'hall': '-10dB'}),
            tr('ebow', 'ebow', '-10dB', sends={'hall': '-6dB'}),
            tr('kit', 'metal-kit', '-6dB', sends={'hall': '-16dB'}),
            tr('bass', 'bass-pick-di', '-6dB'),
            tr('trem', 'clean-chorus', '-12dB', pan=0.3, sends={'tape': '-8dB', 'hall': '-10dB'}),
            # (v2) the strings and the lead breathe against the kick in the fire (a sidechain pump)
            tr('strings', 'strings', '-10dB', sends={'hall': '-8dB'}, fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-5dB', 'release': '500ms', 'curve': 0.6}]),
            tr('chugl', 'm8-chug-l', '-9dB', pan=-0.9),
            tr('chugr', 'm8-chug-r', '-9dB', pan=0.9),
            tr('fuzz', 'bass-fuzz', '-8dB'),
            tr('sub', 'sub', '-6dB', fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-4dB', 'release': '500ms', 'curve': 0.6}]),
            tr('lead', 'lead-tape', '-9dB', sends={'hall': '-10dB'}, fx=[{'type': 'pump', 'on': 'kit.k', 'depth': '-3dB', 'release': '500ms', 'curve': 0.6}]),
            tr('box', 'music-box', '-10dB', sends={'hall': '-6dB'}),
            tr('rain', 'fx-rain', '-12dB'),
            tr('voice', 'voice-speech', '-6dB', sends={'hall': '-10dB'}),
            tr('siren', {'synth': {'layers': [{'type': 'osc', 'wave': 'sine'}, {'type': 'osc', 'wave': 'triangle', 'level': 0.3}],
                                   'amp': {'a': '6s', 'd': '1s', 's': 1, 'r': '5s'}}}, '-24dB', sends={'hall': '0dB'},
               lfo={'wail': 'sine rate=2/1 phase=0'},
               fx=[{'type': 'pitch', 'semitones': {'value': 0, 'mod': [{'src': 'lfo.wail', 'amount': 5}]}, 'formant': 0}, 'lp cutoff=1800', 'hp cutoff=250']),
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
