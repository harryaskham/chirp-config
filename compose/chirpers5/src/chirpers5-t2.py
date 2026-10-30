#!/usr/bin/env python3
"""chirpers5-t2 (chirper-one): 2-STEP LIQUID, "Last Night Bus", for 'Soft Concrete' (Chirpers V).

Liquid drum & bass with a UK-garage 2-step shuffle, 174 bpm, G minor: the night bus home, euphoria and melancholy
together. (chirper-two's Overpass Rain is the album's straight soulful roller; this one skips.)
- THE SHUFFLE: the amen roll's off-eighths lean late (0.04 beat) and two garage skips are added - a ghost before
  the snare on 2 and a kick on the e-of-4.
- THE GARAGE CHOPS: a second voice pitched up a fifth with its formants kept, cut to sixteenth stabs on the
  off-beats of every chord's second bar.
- THE ROLL: wM's amen-chops re-sequenced into a two-step (kick on 1, snare on 2, kick on the and-of-3, snare on 4),
  ghosts between, two alternating bars so it rolls rather than loops; a light swing on the off-eighths.
- THE CHORDS: a Rhodes (physical tine + damper release) on Gm9 - Ebmaj9 - Bbmaj7 - F6/9, two bars each, held and
  re-struck on the and-of-2; strings swell under the break.
- THE LOW END: a warm sine sub on the roots and a reese an octave up, pumped against the kick, both following the
  chords.
- THE VOICE: a wordless synthesised voice sings a short hook on the chord tones (oh-oh-ooh), pitched up with its
  formants kept (no chipmunk), into a dotted-eighth echo.
- The break drops the roll and the bass: Rhodes, strings, the voice alone; the second drop adds a glitch
  stutter roll (wM's stutter roll) at the end of every eight bars.
Form: intro 16 (keys, the roll filtered in from bar 9) / drop 32 / break 16 / drop2 32 / outro 16.
Levels (Harry's clipped-bass note): the amen has its own fast compressor, the master gets loud on two compressors (no
gain into a limiter), a 15 kHz low-pass and a -1.5 dB ceiling: true peak -1.1 dBTP, about -12 LUFS.
Final round (v5, Harry's Soft Concrete notes): the shuffle straightens for each bar whose last beat stutters into a
roll, so the roll's straight repeats grow out of a straight bar; the sub gains phantom harmonics and drive and pumps
harder; darker (the top -1.5 dB more, a 12 kHz low-pass).
Levels (Harry's clipped-bass note; v2 after chirper-two's recipe): the amen has its own fast compressor; the master
glues, then +12 dB into a fast 10:1 compressor (-5 dB, 0.3 ms attack, 60 ms release, +2.5 makeup) that catches the
transients softly; (v3) then a 13.5 kHz low-pass, -4 dB, and a low-knee soft clip (-2.3 dB, knee 0.55) under a -1 dB
ceiling with the song volume at 0 dB: true peak -1.3 to -1.6 dBTP, -12.8 LUFS, longest pinned run 1.
Emits songs/chirpers5-t2.yaml (JSON through tools/songfmt.py). Edit the music here, not the YAML.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers5-t2.yaml")
BPM = 174
SPB = 60 / BPM
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(m): return f"{NN[m % 12]}{m // 12 - 1}"

FORM = [('intro', 16), ('drop', 32), ('break', 16), ('drop2', 32), ('outro', 16)]
# (root, voicing) two bars each: Gm9, Ebmaj9, Bbmaj7, F6/9
CHORDS = [(31, [55, 58, 62, 65, 69]), (27, [55, 58, 62, 63, 67]), (34, [53, 57, 58, 62, 65]), (29, [57, 60, 62, 65, 67])]
# the roll: amen slices on the eighth grid (slice numbers; C2 = slice 0)
ROLL = [[0, 3, 4, 6, 10, 9, 7, 14], [0, 3, 4, 11, 13, 9, 15, 22]]
HOOK = [(0.0, 0, 0.5), (0.75, 1, 0.5), (1.5, 2, 1.25), (3.0, 1, 0.75)]   # (beat, chord-tone index from the top, length)

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
    amen, keys, strings, sub, reese, voice, rain, chops = [], [], [], [], [], [], [], []
    for k, b in enumerate(bars):
        s, t0, i = b['sec'], b['t'], b['i']
        root, ch = CHORDS[(k // 2) % 4]
        first = (k % 2 == 0)
        drums = s in ('drop', 'drop2') or (s == 'intro' and i >= 8) or (s == 'outro' and i < 8)
        # (v5) THE SHUFFLE GIVES WAY: in the bars whose last beat stutters into a roll, the swing straightens for the whole
        # bar, so the roll's straight repeats grow out of a straight bar instead of fighting the shuffle (Harry's note)
        sw = 0.0 if (s == 'drop2' and i % 8 == 7) else 0.04
        if drums:
            pat = ROLL[k % 2]
            # (2-step shuffle) the off-eighths lean late, and two skippy sixteenths are added - a ghost before the
            # snare on 2 and a kick on the e-of-4 - UK garage's skip under a D&B roll
            for q, sl, v in ((1.75, 2, 70), (3.25, 1, 92)):
                amen.append((t0 + q + sw, nm(36 + sl), 0.25, v))
            for e, sl in enumerate(pat):
                at = t0 + e * 0.5 + (sw if e % 2 else 0.0)
                v = 112 if sl in (0, 9, 13, 4, 7, 15, 22) else 84
                amen.append((at, nm(36 + sl), 0.5, v))
        # keys: the chord on the one of each chord's first bar, re-struck on the and-of-2 of the second
        if first:
            keys.append((t0, ','.join(nm(m) for m in ch), 3.8, 86 if s != 'break' else 76))
        else:
            keys.append((t0 + 1.5, ','.join(nm(m) for m in ch[1:]), 2.3, 70))
        if s in ('break', 'drop2', 'outro') and first:
            strings.append((t0, ','.join(nm(m - 12) for m in ch[:3]), 7.8, 70 if s == 'break' else 58))
        if s in ('drop', 'drop2'):
            if first:
                sub.append((t0, nm(root), 3.4, 100))
                reese.append((t0, nm(root + 12), 3.4, 90))
            else:
                sub.append((t0 + 1.5, nm(root), 2.3, 96))
                reese.append((t0 + 1.5, nm(root + 12), 1.0, 86))
                reese.append((t0 + 3.0, nm(root + 24), 0.9, 80))
        # the garage chops: in the drops, short pitched vocal stabs on the off-beats of the chord's second bar
        if s in ('drop', 'drop2') and not first:
            # (v4) THE WORDS: the chops now sing the title in garage fragments - 'night', 'bus', 'night', 'home' -
            # the vocal sample a garage producer would have chopped, synthesised
            for (q, idx), ph in zip(((0.5, 0), (1.25, 1), (2.5, 0), (3.25, 2)), ('n-ay1-t', 'b-ah1-s', 'n-ay1-t', 'hh-ow1-m')):
                chops.append((t0 + q + sw, f"{nm(ch[-1 - idx] + 12)}^ph={ph}", 0.3 if ph == 'hh-ow1-m' else 0.22, 96))
        # the hook: every other chord in the drops, every chord in the break
        if (s in ('drop', 'drop2') and first and (k // 2) % 2 == 0) or (s == 'break' and first):
            for at, idx, ln in HOOK:
                voice.append((t0 + at, f"{nm(ch[-1 - idx])}^o", ln, 92))
    end_s = total * SPB
    secs = {}
    for b in bars:
        secs.setdefault(b['sec'], b['t'] * SPB)
    lv = {'intro': -6, 'drop': 0, 'break': -6, 'drop2': 0, 'outro': -6}
    dyn = []
    for name, _ in FORM:
        t_ = secs[name]
        dyn += [[f'{max(0.0, t_ - 0.3):.3f}s', dyn[-1][1] if dyn else lv[name]], [f'{t_:.3f}s', lv[name]]]
    dyn[0][0] = '0s'
    dyn.append([f'{end_s:.3f}s', -14])
    # the roll is filtered in through the intro's second half
    filt = [['0s', 1], [f"{secs['intro'] + 8 * 4 * SPB:.3f}s", 1], [f"{secs['drop'] - 0.05:.3f}s", 0.25], [f"{secs['drop']:.3f}s", 0]]
    # glitch: stutter rolls on the last beat of every eighth bar of drop2
    gl = [['0s', 0]]
    for b in bars:
        if b['sec'] == 'drop2' and b['i'] % 8 == 7:
            a0 = (b['t'] + 3.0) * SPB
            gl += [[f'{a0 - 0.01:.3f}s', 0], [f'{a0:.3f}s', 1], [f'{(b["t"] + 4.0) * SPB - 0.01:.3f}s', 1], [f'{(b["t"] + 4.0) * SPB:.3f}s', 0]]
    return {
        'about': "Chirpers - Soft Concrete (Chirpers V), track 2 by chirper-one: 2-STEP LIQUID, Last Night Bus. Generated by "
                 "compose/chirpers5/src/chirpers5-t2.py; see its docstring and compose/chirpers5/styles.md.",
        'tempo': BPM, 'length': f'{end_s + 2:.2f}s', 'ceiling': '-1dB', 'volume': '0dB',
        'buses': {'echo': {'fx': [{'type': 'delay', 'time': '3/16', 'feedback': 0.35, 'mix': 1}, 'lp cutoff=4000', 'hp cutoff=300'], 'returns': []},
                  'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1', 'hp cutoff=250'], 'returns': []}},
        'master': {'fx': [{'type': 'eq', 'bands': ['highpass cutoff=28', 'lowshelf cutoff=120 gain=3dB', 'peak cutoff=250 q=0.8 gain=-2dB', 'highshelf cutoff=6000 gain=-5.5dB']},
                          {'type': 'gain', 'gain': '+14dB'},
                          {'type': 'compressor', 'threshold': '-16dB', 'ratio': 2.5, 'attack': '15ms', 'release': '150ms', 'makeup': '2dB'},
                          {'type': 'gain', 'gain': '+12dB'}, {'type': 'compressor', 'threshold': '-5dB', 'ratio': 10, 'attack': '0.3ms', 'release': '60ms', 'makeup': '2.5dB'},
                          {'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.dyn', 'amount': 1}]}},
                          'lp cutoff=12000', {'type': 'gain', 'gain': '-4dB'}, {'type': 'clip', 'drive': '0dB', 'ceiling': '-2.3dB', 'knee': 0.55, 'link': True}],
                   'auto': {'dyn': {'points': dyn}}},
        'tracks': [
            {'name': 'amen', 'patch': 'amen-chops', 'gain': '-7dB',
             'fx': [{'type': 'filter', 'kind': 'lp', 'q': 0.9, 'cutoff': {'value': 18000, 'mod': [{'src': 'auto.op', 'amount': -4.5}]}},
                    {'type': 'compressor', 'threshold': '-20dB', 'ratio': 6, 'attack': '0.5ms', 'release': '50ms', 'makeup': '6dB'},
                    {'type': 'stutter', 'slice': '1/16', 'repeats': 4, 'roll': 0.5, 'floor': '1/64', 'chance': 1,
                     'mix': {'value': 0, 'mod': [{'src': 'auto.gl', 'amount': 1}]}}],
             'auto': {'op': {'points': filt}, 'gl': {'points': gl}}, 'score': line(amen, total)},
            # (v5) the sub with weight that reads on small speakers: phantom harmonics above 90 Hz, a little drive
            {'name': 'sub', 'patch': 'sub', 'gain': '-1dB', 'fx': [{'type': 'phantom', 'cutoff': 90, 'harmonics': '-10dB', 'odd': 0.4},
                                                                 {'type': 'drive', 'drive': 0.2, 'mix': 0.3},
                                                                 {'type': 'pump', 'on': 'amen', 'depth': '-5dB', 'release': '230ms', 'curve': 0.6}],
             'score': line(sub, total)},
            {'name': 'reese', 'patch': 'reese', 'gain': '-10dB', 'fx': ['lp cutoff=1400', {'type': 'pump', 'on': 'amen', 'depth': '-7dB', 'release': '230ms', 'curve': 0.6}],
             'score': line(reese, total)},
            {'name': 'keys', 'patch': {'extends': 'epiano-tine', 'play': {'release': {'patch': 'epiano-damper', 'decay': '2s'}}},
             'gain': '-9dB', 'sends': {'hall': '-12dB'}, 'score': line(keys, total)},
            {'name': 'strings', 'patch': 'strings-saw', 'gain': '-14dB', 'sends': {'hall': '-8dB'}, 'score': line(strings, total)},
            {'name': 'voice', 'patch': 'voice', 'gain': '-9dB', 'sends': {'echo': '-8dB', 'hall': '-10dB'},
             'fx': [{'type': 'pitch', 'semitones': 0, 'formant': 2}], 'score': line(voice, total)},
            # THE GARAGE CHOPS: a second voice, pitched up a fifth with its formants kept, cut to sixteenth stabs
            {'name': 'chops', 'patch': 'voice', 'gain': '-12dB', 'pan': 0.25, 'sends': {'echo': '-10dB'},
             'fx': [{'type': 'pitch', 'semitones': 7, 'formant': 0}], 'score': line(chops, total)},
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
