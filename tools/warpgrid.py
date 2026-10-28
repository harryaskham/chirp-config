#!/usr/bin/env python3
"""warpgrid (wM; promoted 28 Oct): a timing-warp candidate for a constant-tempo song whose record drifts (a live drummer: obZen).

  warpgrid.py ID --out DIR [--stems DIR] [--pin vox] [--scale 1.0] [--tag warp] [--reuse]

Our song plays every bar on one tempo; the record's drummer drifts (Pravus: 0 ms in the middle, -60 ms at 100 s,
+80 ms at the end), so likeness's rhythm term (onset envelopes smoothed +-50 ms, correlated per 4 s, +-1 frame) sees
whole sections out of step. This measures, every 4 beats, the lag of OUR drums (solo render) against the record's
drums stem and of our full mix against the record, on likeness's own onset envelope (8-beat windows, +-170 ms,
parabolic sub-frame peak), keeps the drums' lag where it is confident (r >= 0.6, or >= 0.5 and >= 0.05 over lag 0)
unless a confident mix (r >= 0.6) disagrees by more than 60 ms (a fill or an entry), else the mix's, smooths
(median of 3, gaps interpolated) and writes DIR/ID-TAG.json: the song with a tempo map putting every 4-beat knot
where the record plays it. Tracks given by --pin (default vox: stem-derived timing, already in record time) become
seconds-based notes at their old times; notes tracks written in seconds ('oth') and every seconds-based lane (the
guitars' envl, the master's) stay put. Renders with the groove pin, seed 0. Read-only on songs/.

--song F starts from F instead of songs/ID.yaml (a tempo-map song works: a second, residual pass on an earlier warp;
--lags names its cache). Results, 28 Oct (pin 85b3881): Pravus drifts (bars 26-41 +45 ms, 57-66 -58, 148-170 up to
+86): its tempo map won +1.2..+2.2 on all four seeds after one ride pass (masterstack: the old ride lane was fitted on
the old timing, loudness dips ~3 until it is refitted), adopted as v14. A second, residual pass on the warped Pravus
found nothing real (-0.28/-0.18). The other eight obZen songs do not drift (lags 0 +- 20 ms); their raw readings
are aliases (a 16th or an 8th: Bleed +140 ms at 115 BPM, Combustion +144 at 220) and warping on them LOST 0.6-0.9,
hence the rules here: a lag counts only if it beats lag 0 by >= 0.05 correlation and persists >= 12 beats within
30 ms. Pin stem-timed tracks (--pin vox: +0.07 on Pravus); a song whose drums don't drift needs nothing.
"""
import argparse
import copy
import json
import os
import subprocess
import sys

import numpy as np

CFG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # ~/.config/chirp (promoted from ref/evidence/wM-rhythm)
sys.path.insert(0, os.path.join(CFG, 'tools'))
import likeness as L  # noqa: E402
from partrhythm import onset_env  # noqa: E402

MAX = 8


def render(song, out, solo=(), seed=0):
    b = open(os.path.join(CFG, 'tools/groove-pin')).read().strip()
    env = dict(os.environ, RAYON_NUM_THREADS='2')
    env.pop('LD_LIBRARY_PATH', None)
    cmd = ['nice', '-n', '15', b, 'render', '-f', song, '--seed', str(seed), '-o', out]
    for t in solo:
        cmd += ['--solo', t]
    subprocess.run(cmd, env=env, cwd=os.path.join(CFG, 'songs'), check=True, capture_output=True)


def beat_clock(tempo):
    """beat -> seconds for a tempo number or a tempo map list ({at: 'Nb', bpm})."""
    if isinstance(tempo, (int, float)):
        return lambda b: b * 60 / tempo
    bt = [float(str(e['at']).rstrip('b')) for e in tempo]
    bpm = [e['bpm'] for e in tempo]
    tt = [0.0]
    for i in range(1, len(bt)):
        tt.append(tt[-1] + (bt[i] - bt[i - 1]) * 60 / bpm[i - 1])

    def f(b):
        i = max(0, int(np.searchsorted(bt, b, side='right')) - 1)
        return tt[i] + (b - bt[i]) * 60 / bpm[i]
    return f


def lags(ref, ours, knots, b2t):
    es, eo = onset_env(L.load(ref)), onset_env(L.load(ours))
    n, fps, out = min(len(es), len(eo)), L.FPS, []
    for b in knots:
        i0, i1 = int(b2t(max(b - 4, 0)) * fps), int(b2t(b + 4) * fps)
        if i0 - MAX < 0 or i1 + MAX > n or es[i0:i1].std() == 0 or eo[i0:i1].std() == 0:
            out.append((None, 0.0, 0.0))
            continue
        a = es[i0:i1]
        r = np.array([np.corrcoef(a, eo[i0 + k:i1 + k])[0, 1] if eo[i0 + k:i1 + k].std() > 0 else -1
                      for k in range(-MAX, MAX + 1)])
        k = int(np.argmax(r))
        d = 0.0
        if 0 < k < len(r) - 1:
            y0, y1, y2 = r[k - 1], r[k], r[k + 1]
            den = y0 - 2 * y1 + y2
            d = 0.5 * (y0 - y2) / den if den else 0.0
        out.append((1000 * (k - MAX + d) / fps, float(r[k]), float(r[MAX])))
    return out


def pick(dr, mx):
    """A window's lag: the drums' where confident, else the mix's; a lag that gains under 0.05 correlation over lag 0
    is read as 0 (no evidence of drift: Spiteful Snake's +-10 ms noise warped cost 0.9)."""
    def use(x):
        return 0.0 if x[1] - x[2] < 0.05 else x[0]
    if mx[0] is not None and mx[1] >= 0.6 and dr[0] is not None and abs(use(dr) - use(mx)) > 60:
        return use(mx), 'm'
    if dr[0] is not None and abs(dr[0]) <= 150 and dr[1] >= 0.5:
        return use(dr), 'd'
    if mx[0] is not None and abs(mx[0]) <= 150 and mx[1] >= 0.6:
        return use(mx), 'm'
    return None, '-'


def pin_tracks(d, names, spb, tmp):
    """Score tracks in NAMES become seconds-based notes at their old (constant-tempo) times."""
    for name in names:
        t = next((x for x in d['tracks'] if x['name'] == name), None)
        if t is None:
            continue
        if 'score' in t:
            src = os.path.join(tmp, 'pin-src.json')
            json.dump(d, open(src, 'w'))
            y = os.path.join(tmp, 'pin.yaml')
            subprocess.run(['python3', 'tools/songfmt.py', 'notes', src, name, '-o', y], cwd=CFG, check=True,
                           capture_output=True)
            subprocess.run(['python3', 'tools/songfmt.py', 'json', y, '-o', src, '--no-check'], cwd=CFG, check=True,
                           capture_output=True)
            notes = next(x for x in json.load(open(src))['tracks'] if x['name'] == name)['notes']
        else:
            notes = t['notes']

        def sec(v):
            v = str(v)
            if v.endswith('s'):
                return v
            return f"{float(v.rstrip('b')) * spb:.5f}s"
        t.pop('score', None)
        t['notes'] = [dict(x, at=sec(x['at']), len=sec(x.get('len', '0.25b'))) for x in notes]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('id')
    ap.add_argument('--out', required=True)
    ap.add_argument('--stems')
    ap.add_argument('--pin', default='vox')
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--tag', default='warp')
    ap.add_argument('--reuse', action='store_true', help='reuse DIR/lags.json')
    ap.add_argument('--song', help='start from this song JSON (e.g. an earlier warp: a second, residual pass)')
    ap.add_argument('--lags', default='lags.json', help='lag cache file name in DIR')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cur = a.song or os.path.join(a.out, 'cur.json')
    if not os.path.exists(cur):
        subprocess.run(['python3', 'tools/songfmt.py', 'json', f'songs/{a.id}.yaml', '-o', cur, '--no-check'],
                       cwd=CFG, check=True, capture_output=True)
    d0 = json.load(open(cur))
    tempo = d0['tempo']
    b2t = beat_clock(tempo)
    spb = 60 / tempo if isinstance(tempo, (int, float)) else None   # pinning needs the old constant tempo
    stems = a.stems or next(p for p in (f'{CFG}/ref/stems/bs_roformer_sw/{a.id}', f'{CFG}/ref/stems/htdemucs_6s/{a.id}')
                            if os.path.exists(f'{p}/drums.wav'))
    lj = os.path.join(a.out, a.lags)
    if a.reuse and os.path.exists(lj):
        res = json.load(open(lj))
    else:
        drums = [t['name'] for t in d0['tracks'] if 'kit' in str(t.get('patch', '')) or t['name'].startswith('drum')]
        dw, mw = f'/tmp/warpgrid-{a.id}-drums.wav', f'/tmp/warpgrid-{a.id}-mix.wav'
        render(cur, dw, drums)
        render(cur, mw)
        length = len(L.load(mw)) / 48000
        nb = 0
        while b2t(nb + 4) < length:
            nb += 4
        knots = [float(k) for k in range(0, nb + 1, 4)]
        res = {'stems': stems, 'drums_tracks': drums, 'knots': knots,
               'drums': lags(f'{stems}/drums.wav', dw, knots, b2t),
               'mix': lags(f'{CFG}/ref/{a.id}.wav', mw, knots, b2t)}
        json.dump(res, open(lj, 'w'))
        for f in (dw, mw):
            os.remove(f)
    knots = np.array(res['knots'])
    raw, src = [], []
    for dr, mx in zip(res['drums'], res['mix']):
        lag, s = pick(dr, mx)
        raw.append(np.nan if lag is None else lag)
        src.append(s)
    raw = np.array(raw)
    nk = len(raw)
    # a drift persists: a non-zero lag counts only inside a run of >= 3 knots (12 beats) agreeing within 30 ms;
    # isolated jumps of a 16th or an 8th are onset aliases (Bleed +140 ms, Combustion +144 ms: both lost)
    keep = np.zeros(nk, bool)
    for i in range(nk):
        if np.isnan(raw[i]) or raw[i] == 0:
            continue
        run = [j for j in range(max(0, i - 2), min(nk, i + 3)) if not np.isnan(raw[j]) and abs(raw[j] - raw[i]) <= 30]
        keep[i] = len(run) >= 3
    raw = np.where(np.isnan(raw) | keep, raw, 0.0)
    sm = np.array([np.nanmedian(raw[max(0, i - 1):i + 2]) if np.sum(~np.isnan(raw[max(0, i - 1):i + 2])) >= 2
                   else np.nan for i in range(nk)])
    ok = ~np.isnan(sm)
    idx = np.arange(nk)
    sm = np.interp(idx, idx[ok], sm[ok]) if ok.any() else np.zeros(nk)
    newt = np.array([b2t(k) for k in knots]) - sm * a.scale / 1000
    newt[0] = max(newt[0], 0.0)
    tm = [{'at': f'{knots[i]:.3f}b', 'bpm': round(4 * 60 / (newt[i + 1] - newt[i]), 4)} for i in range(nk - 1)]
    tm.append({'at': f'{knots[-1]:.3f}b', 'bpm': tm[-1]['bpm']})
    if knots[0] > 0 or newt[0] > 0:
        # the song's first knot is beat 0; a positive start is impossible, so beat 0 stays at 0 s
        pass
    d = copy.deepcopy(d0)
    d['tempo'] = tm
    pins = [p for p in a.pin.split(',') if p] if spb else []
    pin_tracks(d, pins, spb, a.out)
    outf = os.path.join(a.out, f'{a.id}-{a.tag}.json')
    json.dump(d, open(outf, 'w'))
    json.dump({'raw_ms': [None if np.isnan(x) else round(float(x), 1) for x in raw], 'src': src,
               'smooth_ms': [round(float(x), 1) for x in sm], 'scale': a.scale, 'pins': pins, 'tempo': tm},
              open(os.path.join(a.out, f'{a.tag}-lags.json'), 'w'))
    bp = [e['bpm'] for e in tm]
    gain0 = np.nanmean([x[1] - x[2] for x in res['drums'] if x[0] is not None])
    print(f"{a.id} {a.tag}: {outf}; knots {nk}, bpm {min(bp):.2f}..{max(bp):.2f}; lag ms "
          f"{np.min(sm):+.0f}..{np.max(sm):+.0f}; drums r gain at best lag {gain0:+.2f}; "
          f"sources d {src.count('d')} m {src.count('m')} - {src.count('-')}")
    print(' '.join(f'{int(k)}:{v:+.0f}{s}' for k, v, s in zip(knots, sm, src)))


if __name__ == '__main__':
    main()
