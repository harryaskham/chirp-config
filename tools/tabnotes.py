#!/usr/bin/env python3
"""tabnotes: a Songsterr track as native notes on a map's performed timeline, with ties merged across bar lines and
(--hold-repeats) a bar's first chord merged into the previous bar's last when it repeats the same pitches right at the
bar line (tabs often split one held chord at the bar: Pyramid Song's 3+3+4+3+3 cycle is written 1.5+1.5+1 | 1+1.5+1.5).

  tabnotes.py MAP.json TRACK -o OUT.json [--hold-repeats] [--vel V]"""
import gzip, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tab2song as T  # noqa: E402
import songsterr as S  # noqa: E402

VEL = {'ppp': 0.2, 'pp': 0.3, 'p': 0.42, 'mp': 0.55, 'mf': 0.65, 'f': 0.78, 'ff': 0.9, 'fff': 1.0}


def main():
    a = sys.argv[1:]
    mp = json.load(open(a[0])); track = int(a[1]); out = a[a.index('-o') + 1]
    hold = '--hold-repeats' in a
    raw = open(f"{mp['cache']}/songsterr-{track}.json", 'rb').read()
    d = json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)
    tl = T.performed_timeline(mp['cache'], mp)
    open_notes = {}     # pitch -> note dict (for ties)
    notes = []
    vel = 0.65
    prev_chord = None   # (pitches, notes, end_time, ended_at_barline)
    for e in tl:
        if e.get('skip'): continue
        m = d['measures'][e['m'] - 1]
        spb = 60.0 / e['bpm']
        pos = 0.0
        voices = m.get('voices') or [{}]
        first = True
        for bt in voices[0].get('beats', []):
            ln = S.beats_of(bt)
            t0 = e['start'] + pos * spb; t1 = t0 + ln * spb
            if bt.get('velocity'): vel = VEL.get(bt['velocity'], vel)
            ns = [x for x in bt.get('notes', []) if not x.get('rest') and 'fret' in x]
            if bt.get('rest') or not ns:
                open_notes = {}; prev_chord = None
            else:
                pitches = sorted(d['tuning'][x['string']] + x['fret'] for x in ns)
                ties = {d['tuning'][x['string']] + x['fret'] for x in ns if x.get('tie')}
                merge = hold and first and prev_chord is not None and prev_chord[0] == pitches and abs(prev_chord[2] - t0) < 1e-6 and abs(ln - 1) < 1e-6 and abs(prev_chord[1] - 1) < 1e-6
                new = {}
                for p in pitches:
                    if (p in ties or merge) and p in open_notes:
                        open_notes[p]['end'] = t1; new[p] = open_notes[p]
                    else:
                        n = {'t': t0, 'end': t1, 'pitch': p, 'vel': vel}; notes.append(n); new[p] = n
                open_notes = new
                prev_chord = (pitches, ln, t1)
            pos += ln
            first = False
    res = [{'at': f"{n['t']:.6f}s", 'len': f"{n['end'] - n['t']:.6f}s", 'pitch': n['pitch'], 'vel': n['vel']} for n in notes]
    json.dump({'notes': res}, open(out, 'w'), indent=1)
    print(f'tabnotes: track {track}: {len(res)} notes', file=sys.stderr)


if __name__ == '__main__':
    main()
