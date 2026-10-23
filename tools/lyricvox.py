#!/usr/bin/env python3
"""lyricvox: sing a Songsterr vocal track's lyrics on chirp's voice layer.

  lyricvox.py MAP.json TRACK -o OUT.json [--words] [--ph CMUDICT]

--ph CMUDICT (a cmudict.dict file): sing ARPAbet phoneme strings (native notes[].ph, groove pin 9a9fad3+) instead
of the onset/vowel/coda marks: each tab word looked up in CMUdict, split into its syllables (one consonant between
vowels starts the next syllable, more split first-to-coda), a syllable sung over several notes gets its onset+vowel on
the first, the vowel held on the middle ones and vowel+coda on the last; syllables merged onto one note are joined
with '.'; 'Ooh' melismas sing UW. Words missing from the dictionary keep the marks.

Reads the map's Songsterr cache (track TRACK: notes, ties, and the tab's own `newLyrics` syllables, which Songsterr
lays onto the track's non-tied notes in order), places every note on the map's performed timeline (offset, bpm
corrections, skips, repeats: tab2song.performed_timeline) and gives each sung onset its syllable as voice marks:
`expr.on` (onset consonant), `expr.vow` (+ `expr_end.vow` for a diphthong), `expr.off` (coda consonant) — the
voice patch must bind `onset: expr.on`, `coda: expr.off` and `vowel: {value: 0, mod: [{src: expr.vow, amount: 1}]}`.
Ties merge into the sung note; extra notes past the lyric run out sing 'ah'. Prints {"notes": [...]} (native notes,
`at`/`len` in seconds) and a syllable/note count check on stderr. Spelling → sound is a small English heuristic
(first consonant cluster's most audible member, the vowel letters' quality, the last consonant), not a dictionary:
it gives the right *kind* of syllable (closures, hiss, nasals, the vowel line), not exact phonemes."""
import gzip, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tab2song as T  # noqa: E402

CODES = dict(p=1, b=2, t=3, d=4, k=5, g=6, f=7, v=8, th=9, dh=10, s=11, z=12, sh=13, zh=14, h=15, m=16, n=17, ng=18,
             l=19, r=20, w=21, y=22)
# vowel line u 0 · o .25 · a .5 · e .75 · i 1
V = {'u': 0.0, 'o': 0.25, 'a': 0.5, 'e': 0.75, 'i': 1.0}


def onset(w):
    w = w.lower()
    if not w or w[0] in 'aeiou': return 0
    for cl, c in (('sch', 's'), ('sh', 'sh'), ('ch', 'sh'), ('th', 'dh' if w in ('the', 'there', 'they', 'this', 'that', 'then', 'their', 'them', 'these', 'those', 'than', 'thee', 'thy') else 'th'),
                  ('wh', 'w'), ('ph', 'f'), ('kn', 'n'), ('wr', 'r'), ('qu', 'k'), ('gh', 'g'), ('ck', 'k')):
        if w.startswith(cl): return CODES[c]
    c = w[0]
    if c == 'j': return CODES['d']
    if c == 'c': return CODES['s'] if len(w) > 1 and w[1] in 'eiy' else CODES['k']
    if c == 'x': return CODES['z']
    if c == 'y': return CODES['y'] if len(w) > 1 and w[1] in 'aeiou' else 0
    # clusters: s+stop sounds as s first; stop+l/r keeps the stop
    return CODES.get(c, 0)


def coda(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 0
    for cl, c in (('ng', 'ng'), ('nk', 'k'), ('sh', 'sh'), ('ch', 'sh'), ('th', 'th'), ('ck', 'k'), ('ts', 's'), ('ds', 'z'),
                  ('gh', None), ('ll', 'l'), ('ss', 's'), ('ve', 'v'), ('se', 'z'), ('ce', 's'), ('ne', 'n'), ('me', 'm'),
                  ('le', 'l'), ('re', 'r'), ('de', 'd'), ('te', 't'), ('ke', 'k'), ('pe', 'p'), ('be', 'b'), ('ge', 'zh')):
        if w.endswith(cl) and len(w) > len(cl): return CODES[c] if c else 0
    c = w[-1]
    if c in 'aeiouwy' or c == 'h': return 0
    if c == 's': return CODES['z'] if len(w) > 1 and w[-2] in 'aeioubdglmnrvw' else CODES['s']
    if c == 'x': return CODES['s']
    if c == 'r': return 0           # non-rhotic sung r: colours the vowel instead
    return CODES.get(c, 0)


def vowel(w):
    """(start, end) on the u-o-a-e-i line."""
    s = re.sub(r"[^a-z]", "", w.lower())
    for pat, a, b in (('igh', 0.5, 1.0), ('ee', 1.0, 1.0), ('ea', 1.0, 1.0), ('ie', 1.0, 1.0), ('oo', 0.0, 0.0),
                      ('ou', 0.4, 0.05), ('ow', 0.3, 0.05), ('oa', 0.25, 0.05), ('oy', 0.25, 1.0), ('oi', 0.25, 1.0),
                      ('ay', 0.75, 1.0), ('ai', 0.75, 1.0), ('ey', 0.75, 1.0), ('ar', 0.5, 0.5), ('or', 0.25, 0.25),
                      ('er', 0.6, 0.6), ('ir', 0.6, 0.6), ('ur', 0.6, 0.6), ('aw', 0.3, 0.3), ('au', 0.3, 0.3),
                      ('ue', 0.0, 0.0), ('ew', 0.9, 0.0)):
        if pat in s: return a, b
    vs = [c for c in s if c in 'aeiouy']
    if not vs: return 0.5, 0.5
    if s in ('i',) or s.endswith('y') and len(vs) == 1 and len(s) <= 3: return 0.5, 1.0    # I, my, by, fly
    c = vs[0] if vs[0] != 'y' else 'i'
    # a final silent e makes the vowel 'long' (diphthongs)
    if len(vs) >= 2 and s.endswith('e') and c != 'e':
        return {'a': (0.75, 1.0), 'i': (0.5, 1.0), 'o': (0.25, 0.05), 'u': (0.0, 0.0)}.get(c, (V[c], V[c]))
    if c == 'o' and s.endswith('o'): return 0.25, 0.05
    return {'a': (0.55, 0.55), 'e': (0.72, 0.72), 'i': (0.92, 0.92), 'o': (0.35, 0.35), 'u': (0.45, 0.45)}[c]


def syllables(text):
    """[(syllable, starts_a_line)]"""
    out = []
    wid = 0
    for line in text.split('\n'):
        first = True
        line = re.sub(r'\[[^\]]*\]', ' ', line)    # section labels such as [Verse 1] are not sung
        for word in line.split():
            parts = [re.sub(r"[^A-Za-z']", "", p) for p in word.split('-')]
            parts = [p for p in parts if p]
            for k, p in enumerate(parts):
                out.append((p, first, wid, k, len(parts), ''.join(parts))); first = False
            wid += 1
    return out


def align(notes, syl, gap=0.45):
    """DP: each note sings a new syllable, or continues the previous one (melisma); a syllable with no note of its
    own merges into the previous note. Line starts prefer phrase starts (a rest before the note)."""
    INF = 1e9
    N, M = len(notes), len(syl)
    ps = [i == 0 or notes[i]['t'] - notes[i - 1]['end'] > gap for i in range(N)]
    D = [[INF] * (M + 1) for _ in range(N + 1)]; B = [[None] * (M + 1) for _ in range(N + 1)]
    D[0][0] = 0
    for i in range(N + 1):
        for j in range(M + 1):
            c = D[i][j]
            if c >= INF: continue
            if i < N and j < M:   # note i sings syllable j
                k = c + (0 if ps[i] == syl[j][1] else (2 if syl[j][1] else 1))
                if k < D[i + 1][j + 1]: D[i + 1][j + 1] = k; B[i + 1][j + 1] = (i, j, 'new')
            if i < N and j > 0:   # note i continues syllable j-1
                k = c + 1 + (3 if ps[i] else 0)
                if k < D[i + 1][j]: D[i + 1][j] = k; B[i + 1][j] = (i, j, 'cont')
            if j < M and i > 0:   # syllable j merged into note i-1
                k = c + 2 + (3 if syl[j][1] else 0)
                if k < D[i][j + 1]: D[i][j + 1] = k; B[i][j + 1] = (i, j, 'merge')
    # end: all notes consumed; leftover syllables unsung (cheap) 
    best = min(range(M + 1), key=lambda j: D[N][j] + (M - j) * 0.5)
    lab = [None] * N; i, j = N, best
    while i > 0 or j > 0:
        pi, pj, kind = B[i][j]
        if kind == 'new': lab[pi] = ('new', pj)
        elif kind == 'cont': lab[pi] = ('cont', pj - 1)
        i, j = pi, pj
    return lab


def _unused_words(text):
    out = []
    for word in text.split():
        parts = [p for p in word.split('-') if p]
        for k, p in enumerate(parts):
            clean = re.sub(r"[^A-Za-z']", "", p)
            if not clean: continue
            out.append(clean)
    return out


ARPA_V = {'AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW'}


def load_cmu(path):
    d = {}
    for line in open(path, encoding='utf-8', errors='replace'):
        p = line.split('#')[0].split()
        if len(p) < 2: continue
        w = p[0].lower()
        if '(' in w: continue          # keep the first pronunciation
        d[w] = p[1:]
    return d


def cmu_syllables(ph):
    """split an ARPAbet word into syllables: one consonant between nuclei starts the next syllable, more split
    first-to-coda / rest-to-onset."""
    vi = [i for i, x in enumerate(ph) if x.rstrip('012') in ARPA_V]
    if not vi: return [ph]
    bounds = [0]
    for a, b in zip(vi, vi[1:]):
        n = b - a - 1
        bounds.append(b - (1 if n == 1 else (n - 1 if n >= 2 else 0)))
    bounds.append(len(ph))
    return [ph[bounds[i]:bounds[i + 1]] for i in range(len(vi))]


def word_ph(word, nsyl, cmu):
    """the word's tab syllables as phoneme lists (melisma syllables repeat the vowel), or None"""
    w = word.lower().strip("'")
    if re.fullmatch(r"o+h?", w) or w in ('ooh', 'oooh'):
        return [['UW1']] * nsyl
    ph = cmu.get(w) or cmu.get(w.rstrip("'s")) or None
    if ph is None: return None
    sy = cmu_syllables(ph)
    if len(sy) == nsyl: return sy
    if len(sy) > nsyl:                 # fewer tab syllables: merge the rest into the last
        return sy[:nsyl - 1] + [sum(sy[nsyl - 1:], [])]
    vowel = [x for x in sy[-1] if x.rstrip('012') in ARPA_V][0]
    return sy + [[vowel]] * (nsyl - len(sy))   # melisma ('se-e'): hold the vowel


def split_ovc(ph):
    vi = [i for i, x in enumerate(ph) if x.rstrip('012') in ARPA_V]
    if not vi: return ph, [], []
    return ph[:vi[0]], ph[vi[0]:vi[-1] + 1], ph[vi[-1] + 1:]


def marks(syl, prev=None):
    """onset/vowel/coda codes for one written syllable; a repeated vowel melisma ('o', 'h') sustains."""
    s = syl.lower().strip("'")
    if re.fullmatch(r"o+h?|h", s): return dict(on=0, va=0.05, vb=0.05, off=0)
    if re.fullmatch(r"e+\??", s) or (prev and re.fullmatch(r"[aeiou]+", s)):   # held vowel continuation ('se-e')
        return dict(on=0, va=prev['vb'] if prev else 0.75, vb=prev['vb'] if prev else 0.75, off=0)
    a, b = vowel(s)
    return dict(on=onset(s), va=a, vb=b, off=coda(s))


def main():
    a = sys.argv[1:]
    mp = json.load(open(a[0])); track = int(a[1]); out = a[a.index('-o') + 1]
    cache = mp['cache']
    raw = open(f'{cache}/songsterr-{track}.json', 'rb').read()
    d = json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)
    text = (d.get('newLyrics') or [{}])[0].get('text', '')
    syl = syllables(text)
    tl = T.performed_timeline(cache, mp)
    import songsterr as S
    notes = []
    for e in tl:
        if e.get('skip'): continue
        m = d['measures'][e['m'] - 1]
        spb = 60.0 / e['bpm']
        voices = m.get('voices') or [{}]
        pos = 0.0
        for bt in voices[0].get('beats', []):
            ln = S.beats_of(bt)
            ns = [x for x in bt.get('notes', []) if not x.get('rest')]
            if not bt.get('rest') and ns:
                x = ns[0]
                tie = bool(x.get('tie'))
                pitch = d['tuning'][x['string']] + x['fret'] if 'string' in x else x.get('fret')
                t0 = e['start'] + pos * spb
                if tie and notes:
                    notes[-1]['end'] = t0 + ln * spb
                else:
                    notes.append({'t': t0, 'end': t0 + ln * spb, 'pitch': pitch, 'vel': (bt.get('velocity') or 'mf')})
            pos += ln
    n_sung = len(notes)
    res = []
    prev = None
    lab = align(notes, syl)
    cmu = load_cmu(a[a.index('--ph') + 1]) if '--ph' in a else None
    if cmu is not None:
        sylph = {}
        words = {}
        for j, x in enumerate(syl): words.setdefault(x[2], []).append(j)
        miss = set()
        for wid, js in words.items():
            x = syl[js[0]]
            wp = word_ph(x[5], x[4], cmu)
            if wp is None and x[4] > 1:      # a hyphenated compound ('Black-eyed', 'past-and'): its parts as words
                parts = [word_ph(syl[j][0], 1, cmu) for j in js]
                wp = None if any(q is None for q in parts) else [q[0] for q in parts]
            if wp is None: miss.add(x[5]); continue
            for k, j in enumerate(js): sylph[j] = wp[k]
        if miss: print('lyricvox: not in the dictionary (marks instead):', ' '.join(sorted(miss)), file=sys.stderr)
        # syllables per note: a 'new' note sings its syllable plus any merged (skipped) ones up to the next new note
        news = [(i, lab[i][1]) for i in range(len(notes)) if lab[i] and lab[i][0] == 'new']
        own = {}
        for (i, j), nxt in zip(news, news[1:] + [(None, len(syl))]):
            own[i] = list(range(j, nxt[1]))
        groups = {}                    # syllable index -> its notes (new + continuations)
        for i in range(len(notes)):
            if lab[i]: groups.setdefault(lab[i][1], []).append(i)
        phs = {}
        for i, js in own.items():
            if not all(j in sylph for j in js): continue
            tail = groups.get(js[0], [i])
            o, v, c = split_ovc(sylph[js[0]])
            if len(tail) == 1:
                body = [sylph[j] for j in js]
                phs[i] = ' . '.join(' '.join(b) for b in body)
                continue
            phs[tail[0]] = ' '.join(o + v)
            for m in tail[1:-1]: phs[m] = ' '.join(v[-1:])
            rest = [sylph[j] for j in js[1:]]
            phs[tail[-1]] = ' . '.join([' '.join(v[-1:] + c)] + [' '.join(b) for b in rest])
    for i, n in enumerate(notes):
        kind, j = lab[i] if lab[i] else ('new', None)
        s = syl[j][0] if j is not None else 'ah'
        if kind == 'cont' and prev:
            mk = dict(on=0, va=prev['vb'], vb=prev['vb'], off=prev['off']); prev['off'] = 0
            if res and 'expr' in res[-1]: res[-1]['expr'].pop('off', None)
        else:
            mk = marks(s, prev)
        prev = mk
        e = {'vow': round(mk['va'], 3)}
        if mk['on']: e['on'] = mk['on']
        if mk['off']: e['off'] = mk['off']
        note = {'at': f"{n['t']:.6f}s", 'len': f"{n['end'] - n['t']:.6f}s", 'pitch': int(n['pitch']), 'vel': 0.75, 'expr': e}
        if mk['vb'] != mk['va']: note['expr_end'] = {'vow': round(mk['vb'], 3)}
        note['syl'] = s
        if cmu is not None and i in phs:
            note.pop('expr', None); note.pop('expr_end', None); note['ph'] = phs[i]
        res.append(note)
    print(f'lyricvox: {n_sung} sung notes, {len(syl)} syllables', file=sys.stderr)
    if '--words' in a:
        for n in res: print(f"{float(n['at'][:-1]):8.2f} {n['pitch']:3d} {n['syl']:10s} {n.get('ph') or n.get('expr')} {n.get('expr_end', '')}", file=sys.stderr)
    for n in res: n.pop('syl')
    json.dump({'notes': res}, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
