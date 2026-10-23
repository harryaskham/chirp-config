#!/usr/bin/env python3
"""tabvox: sing a tab's lyrics on a stem-built vocal (chirper-zero's Knives Out r7, as a tool).

  tabvox.py SONG TRACK SONGSTERR_ID VOX_TRACK -o OUT [--stem VOCALS.wav] [--bpm LO-HI] [--lag 0-40]
            [--cmu ref/cmudict.dict] [--tab TRACK.json] [--dry-run]

For a vocal TRACK whose notes come from the stem (monotrans/stemvox: real timing and pitch), with a Songsterr tab
whose vocal track VOX_TRACK carries lyrics (`newLyrics`; cache it first with tools/songsterr.py SONGSTERR_ID):
  1. the tab's syllables (lyricvox.syllables) lie 1:1 on the vocal track's non-rest, non-tied beats, in beats;
  2. their timeline t = t0 + b*60/bpm is fitted to the vocal stem by FFT cross-correlating an impulse train of those
     onsets with the stem's onset envelope (likeness's flux), over BPM LO-HI (default: the song's tempo +-10%) and
     lags 0..40 s, then refined;
  3. each word's CMUdict phonemes are split into its tab syllables (lyricvox.word_ph);
  4. each TRACK note takes the syllable whose span [t_k - 0.10, t_k+1 - 0.05) holds its start; the FIRST note of
     each syllable gets notes[].ph (ARPAbet, groove pin 9a9fad3+), the rest keep their vowel marks.
Knives Out: 137.27 BPM, +0.149 s; words on the stem notes +0.07 (every-seed mean up) at v4 68.04. Pair it with the
voice's ph settings (ph_vowels:false keeps the marks' vowels; consonant_level about -2 dB, ph_early 0: the mark-voice
match wM measured). The tab is read linearly (no repeat expansion): a tab whose sung part repeats via repeat signs
needs its lyric spans checked (--dry-run prints the fit and the first syllables). OUT keeps the song's structure
(songfmt) and is written by extension like onsetsnap: .json JSON, else song YAML.
"""
import argparse
import gzip
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402,F401  (the adopted pin for anything that renders)
import likeness as L  # noqa: E402
import lyricvox as LV  # noqa: E402
import songsterr as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_tab(sid, track):
    p = os.path.join(ROOT, "ref", f"songsterr-{sid}", f"songsterr-{track}.json")
    if not os.path.exists(p):
        raise SystemExit(f"tabvox: no cached tab at {p}: run tools/songsterr.py {sid} first")
    raw = open(p, "rb").read()
    return json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)


def tab_onsets(d):
    """Beat positions (quarter beats from the tab's start) of the vocal track's sung, non-tied beats, linearly."""
    out, pos, sig = [], 0.0, None
    for m in d.get("measures", []):
        voices = m.get("voices") or [{}]
        mpos = 0.0
        for bt in voices[0].get("beats", []):
            ns = [x for x in bt.get("notes", []) if not x.get("rest")]
            if not bt.get("rest") and ns and not ns[0].get("tie"):
                out.append(pos + mpos)
            mpos += S.beats_of(bt)
        sig = m.get("signature") or sig        # Songsterr stores the signature only where it changes
        pos += 4 * sig[0] / sig[1] if sig else mpos
    return out


def fit(onsets_b, env, fps, bpm_lo, bpm_hi, max_lag_s=40.0):
    """(bpm, t0, score): the impulse train t0 + b*60/bpm best aligned (FFT cross-correlation) with the envelope."""
    n = len(env)
    e = env - env.mean()
    E = np.fft.rfft(e, 2 * n)
    M = int(max_lag_s * fps)

    def best(bpm):
        imp = np.zeros(n)
        idx = (np.asarray(onsets_b) * 60.0 / bpm * fps).astype(int)
        idx = idx[(idx >= 0) & (idx < n)]
        imp[idx] = 1.0
        c = np.fft.irfft(E * np.conj(np.fft.rfft(imp, 2 * n)))[: M + 1]    # c[lag] = sum e[t + lag] * imp[t]
        k = int(np.argmax(c))
        return float(c[k]) / max(1, len(idx)), k

    coarse = [(best(b), b) for b in np.arange(bpm_lo, bpm_hi + 1e-9, 0.25)]
    (sc, lag), bpm = max(coarse, key=lambda x: x[0][0])
    for b in np.arange(bpm - 0.5, bpm + 0.5 + 1e-9, 0.02):
        (s2, l2) = best(b)
        if s2 > sc:
            sc, lag, bpm = s2, l2, b
    return float(bpm), lag / fps, sc


HOLD = re.compile(r"[._\-\u2026]+")
CONT = (".", "-", "\u2026")


def lyric_tokens(text):
    """One token per sung beat (Songsterr lays lyric tokens 1:1 on the track's sung, non-tied beats):
    {'kind': 'syl', 'piece', 'wid'} or {'kind': 'hold'}. Words split over beats are joined back, whichever way the tab
    writes it: in-word hyphens ('pret-ty'), a trailing hyphen ('pret- ty'), or ellipses ('pret... ..ty'; Songsterr
    51263). A token that is only dots/underscores/hyphens ('...', '_') is a HELD beat: it continues the previous
    syllable and starts none (dropping those, as lyricvox.syllables does, shifted every later syllable a beat early)."""
    out, wid, cont = [], -1, False
    for line in text.split("\n"):
        line = re.sub(r"\[[^\]]*\]", " ", line)       # section labels are not sung
        for tok in line.split():
            if HOLD.fullmatch(tok):
                out.append({"kind": "hold"})
                continue
            lead = tok.startswith(CONT)
            core = tok.strip("".join(CONT))
            parts = [re.sub(r"[^A-Za-z']", "", q) for q in core.split("-")]
            parts = [q for q in parts if q]
            if not parts:
                out.append({"kind": "hold"})
                continue
            if not (cont or lead):
                wid += 1
            for q in parts:
                out.append({"kind": "syl", "piece": q, "wid": wid})
            cont = tok.endswith(CONT)
    return out


def syllable_ph(tokens, cmu):
    """ARPAbet per token (None for holds and dictionary misses), and the words missed."""
    words, out, miss = {}, [None] * len(tokens), set()
    for j, x in enumerate(tokens):
        if x["kind"] == "syl":
            words.setdefault(x["wid"], []).append(j)
    for js in words.values():
        word = "".join(tokens[j]["piece"] for j in js)
        wp = LV.word_ph(word, len(js), cmu)
        if wp is None and len(js) > 1:   # a compound: its pieces as words
            parts = [LV.word_ph(tokens[j]["piece"], 1, cmu) for j in js]
            wp = None if any(q is None for q in parts) else [q[0] for q in parts]
        if wp is None:
            miss.add(word)
            continue
        for k, j in enumerate(js):
            out[j] = " ".join(wp[k])
    return out, miss


def assign(notes, times, phs, kinds=None):
    """Indices of the notes that start each syllable's span, with that syllable's phonemes. A syllable's span runs
    to the next SYLLABLE (held beats in between belong to it)."""
    kinds = kinds or ["syl"] * len(times)
    syl = [k for k in range(len(times)) if kinds[k] == "syl"]
    spans = [(k, times[k] - 0.10, (times[syl[m + 1]] - 0.05) if m + 1 < len(syl) else float("inf"))
             for m, k in enumerate(syl)]
    got = {}
    for i, n in enumerate(notes):
        if not n.get("pitch") or not str(n.get("at", "")).endswith("s"):
            continue
        s = float(str(n["at"]).rstrip("s"))
        for k, lo, hi in spans:
            if lo <= s < hi:
                if k not in got and phs[k]:
                    got[k] = (i, phs[k])
                break
    return got


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("song")
    ap.add_argument("track")
    ap.add_argument("songsterr_id")
    ap.add_argument("vox_track", type=int)
    ap.add_argument("-o", dest="out")
    ap.add_argument("--stem")
    ap.add_argument("--bpm", help="LO-HI (default: the song's tempo +-10%%)")
    ap.add_argument("--lag", type=float, default=40.0, help="largest lead-in, s")
    ap.add_argument("--cmu", default=os.path.join(ROOT, "ref", "cmudict.dict"))
    ap.add_argument("--tab", help="a Songsterr track JSON to read instead of the cache")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if not a.dry_run and not a.out:
        ap.error("-o OUT (or --dry-run)")
    import onsetsnap as O      # song loading/writing (songfmt structure, canonical tempo)
    song, canon = O.load_song(a.song)
    tr = next((t for t in song.get("tracks", []) if t.get("name") == a.track), None)
    if tr is None or not isinstance(tr.get("notes"), list):
        raise SystemExit(f"tabvox: {a.track} is not a notes track in {a.song}")
    if a.tab:
        with open(a.tab) as f:
            d = json.load(f)
    else:
        d = load_tab(a.songsterr_id, a.vox_track)
    text = (d.get("newLyrics") or [{}])[0].get("text", "")
    syl = lyric_tokens(text)
    onsets_b = tab_onsets(d)
    if not syl or not onsets_b:
        raise SystemExit(f"tabvox: track {a.vox_track} of {a.songsterr_id} has no lyrics or no sung beats")
    n = min(len(syl), len(onsets_b))
    sid = os.path.splitext(os.path.basename(a.song))[0]
    stem = a.stem or os.path.join(ROOT, "ref", "stems", "htdemucs_6s", sid, "vocals.wav")
    env = np.convolve(L.Feat(L.load(stem)).onset, np.ones(5) / 5, "same")
    tempo = canon.get("tempo") or 120
    t0 = float(tempo if isinstance(tempo, (int, float)) else tempo[0]["bpm"])
    lo, hi = (float(x) for x in a.bpm.split("-")) if a.bpm else (t0 * 0.9, t0 * 1.1)
    bpm, off, score = fit(onsets_b[:n], env, L.FPS, lo, hi, a.lag)
    times = [off + b * 60.0 / bpm for b in onsets_b[:n]]
    phs, miss = syllable_ph(syl[:n], LV.load_cmu(a.cmu))
    got = assign(tr["notes"], times, phs, [x["kind"] for x in syl[:n]])
    holds = sum(1 for x in syl if x["kind"] == "hold")
    print(f"tabvox {sid}: {len(syl)} lyric tokens ({holds} held) on {len(onsets_b)} sung beats; fit {bpm:.2f} BPM, {off:+.3f} s "
          f"(score {score:.3f}); {len(got)} of {len(tr['notes'])} {a.track} notes take a syllable's phonemes")
    n_syl = sum(1 for x in syl[:n] if x["kind"] == "syl")
    cover = len(got) / max(1, n_syl)
    print(f"  coverage: {len(got)} of {n_syl} syllables found a stem note ({cover:.0%})")
    if cover < 0.5:
        print("  WARNING: under half the syllables found a stem note: the tab's timeline does not fit this record "
              "(a live or edited tab, repeats the tab does not spell out, or a wrong vocal track). Check --dry-run's "
              "first syllables against the record before keeping it (Like Spinning Plates' live tab 51263: 16%; Knives Out 79%).")
    if miss:
        print(f"  not in the dictionary (left on marks): {' '.join(sorted(miss))}")
    for k in sorted(got)[:6]:
        i, ph = got[k]
        print(f"  {times[k]:7.2f} s  {syl[k]['piece']:10s} -> note {i} at {tr['notes'][i]['at']}: {ph}")
    if a.dry_run:
        return
    for i, ph in got.values():
        tr["notes"][i]["ph"] = ph
    O.write_song(song, a.out)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
