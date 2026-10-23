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


def syllable_ph(syl, cmu):
    """ARPAbet strings per tab syllable (None where the dictionary has no word), and the words it missed."""
    words, out, miss = {}, [None] * len(syl), set()
    for j, x in enumerate(syl):
        words.setdefault(x[2], []).append(j)
    for js in words.values():
        x = syl[js[0]]
        wp = LV.word_ph(x[5], x[4], cmu)
        if wp is None and x[4] > 1:   # a hyphenated compound: its parts as words
            parts = [LV.word_ph(syl[j][0], 1, cmu) for j in js]
            wp = None if any(q is None for q in parts) else [q[0] for q in parts]
        if wp is None:
            miss.add(x[5])
            continue
        for k, j in enumerate(js):
            out[j] = " ".join(wp[k])
    return out, miss


def assign(notes, times, phs):
    """Indices of the notes that start each syllable's span, with that syllable's phonemes."""
    got = {}
    for i, n in enumerate(notes):
        if not n.get("pitch"):
            continue
        s = float(str(n["at"]).rstrip("s")) if str(n["at"]).endswith("s") else None
        if s is None:
            continue
        for k, t in enumerate(times):
            end = times[k + 1] - 0.05 if k + 1 < len(times) else float("inf")
            if t - 0.10 <= s < end:
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
    syl = LV.syllables(text)
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
    got = assign(tr["notes"], times, phs)
    print(f"tabvox {sid}: {len(syl)} syllables on {len(onsets_b)} sung beats; fit {bpm:.2f} BPM, {off:+.3f} s "
          f"(score {score:.3f}); {len(got)} of {len(tr['notes'])} {a.track} notes take a syllable's phonemes")
    if miss:
        print(f"  not in the dictionary (left on marks): {' '.join(sorted(miss))}")
    for k in sorted(got)[:6]:
        i, ph = got[k]
        print(f"  {times[k]:7.2f} s  {syl[k][0]:10s} -> note {i} at {tr['notes'][i]['at']}: {ph}")
    if a.dry_run:
        return
    for i, ph in got.values():
        tr["notes"][i]["ph"] = ph
    O.write_song(song, a.out)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
