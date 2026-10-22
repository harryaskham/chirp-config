#!/usr/bin/env python3
"""vocalscore: how close our vocal is to the record's, from the vocal stems (opt-in; Harry 2026-10-22: the vocal climbs
— Pyramid Song, I Never Learnt to Share, I Feel Love, Do It Now — need vocal metrics; a Demucs stem is noisy, so the
terms are ordered by how much noise they survive).

  vocalscore.py REF_VOCALS.wav OURS.wav [b0,b1,…] [--from A --to B] [--asr] [--asr-model base.en] [--json]
  vocalscore.py REF_VOCALS.wav --render SONG TRACK[,TRACK…] [b0,b1,…] [--seed S] [--keep OUT.wav] …
      (renders TRACK(s) soloed, the whole span, with the groove pin)

  activity     when the voice sings: frames whose vocal-band level is within 30 dB of the recording's loud frames
               and above -60 dBFS,
               F1 of ours against the record's (phrasing; survives stem noise best)
  cadence      syllable onsets (rises of the 200 Hz-4 kHz level while active) matched one-to-one within ±70 ms, F
               rescaled against chance (the onsets slid along the song) — the rhythm of the words
  pitch        where both sing: harmonic-sum f0 (MIDI 36-84, 10 cents), share of frames within 50 cents (and within
               50 cents of an octave, for doubled or octave-sung lines)
  vowels       where both sing: the MFCC shape (coefficients 2-13, 25 ms) cosine, rescaled against chance — vowel and
               voice colour; the noisiest term on a separated stem
  words        (--asr) Whisper's transcripts of both, word similarity (1 - word edit distance / reference words);
               also reports what Whisper heard in the record's stem: if that is not the lyrics, the stem caps the term

--from/--to scores one window (both signals cropped; section bounds then ignored). Whisper on CPU is slow (base.en
read 30 s of a stem in ~3 min under load): give --asr a window of a verse or a chorus. It read You Can't Hurry Love's
separated vocal stem close to the lyrics in places ("You gotta trust, give it time"), so the stem caps but does not
void the term.

Scores run 0 (chance) to 100 (identical) except activity and words (0-100 as shares). Compare like with like: our
vocal separated the same way as the reference (vocaltest.py --keep) carries the same artifacts; our clean solo render
does not, so a perfect reproduction scores below 100 on it. Nothing here changes the default metric.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
from scipy import ndimage, signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import noteacc  # noqa: E402
from likeness import SR, load  # noqa: E402

HOP = 480                       # 10 ms
ACTIVE_DB = 30.0
TOL = 0.07
SHIFTS = noteacc.SHIFTS


def band_level(x, lo=200, hi=4000):
    """Vocal-band level (dB) per 10 ms (25 ms windows)."""
    sos = signal.butter(4, [lo, hi], "bandpass", fs=SR, output="sos")
    h = signal.sosfilt(sos, x)
    cs = np.concatenate([[0.0], np.cumsum(h.astype(np.float64) ** 2)])
    w = 1200
    e = (cs[w:] - cs[:-w])[::HOP] / w
    return 10 * np.log10(np.maximum(e, e.max() * 1e-9 + 1e-20))


ABS_DB = -60.0                  # and above this absolute vocal-band level: a near-silent track does not sing


def active(lv):
    return (lv > np.percentile(lv, 95) - ACTIVE_DB) & (lv > ABS_DB)


def syllables(lv, act):
    """Syllable onset times (s): peaks of the smoothed level's rise where active."""
    sm = ndimage.uniform_filter1d(lv, 3)
    rise = np.maximum(np.diff(sm, prepend=sm[0]), 0) * act
    if rise.max() <= 0:
        return np.zeros(0)
    pk, _ = signal.find_peaks(rise, height=max(1.0, np.percentile(rise[act], 90) if act.any() else 1.0),
                              distance=int(0.08 * SR / HOP))
    return pk * HOP / SR


def f0(x, act, lo=36, hi=84):
    """MIDI f0 per 10 ms frame where active (NaN elsewhere): monotrans' harmonic sum, 2048-sample windows."""
    n, nf = 2048, 1 << 14
    f = np.fft.rfftfreq(nf, 1 / SR)
    cands = 440 * 2 ** ((np.arange(lo * 10, hi * 10) / 10 - 69) / 12)
    idx = [np.clip(np.round(cands * h / f[1]).astype(int), 0, len(f) - 1) for h in range(1, 6)]
    win = np.hanning(n)
    out = np.full(len(act), np.nan)
    for i in np.nonzero(act)[0]:
        a = i * HOP
        z = x[a:a + n]
        if len(z) < n:
            break
        X = np.abs(np.fft.rfft(z * win, nf))
        sal = sum(0.8 ** (h - 1) * X[ix] for h, ix in enumerate(idx, 1))
        out[i] = 69 + 12 * np.log2(cands[int(np.argmax(sal))] / 440)
    return out


def mfcc(x, nfft=1200):
    """MFCC 2-13 (no c0, c1) per 10 ms frame (25 ms windows), unit length."""
    f, _, Z = signal.stft(x, SR, nperseg=nfft, noverlap=nfft - HOP, boundary=None, padded=False)
    P = np.abs(Z) ** 2
    mel = lambda hz: 2595 * np.log10(1 + hz / 700)  # noqa: E731
    pts = 700 * (10 ** (np.linspace(mel(80), mel(8000), 42) / 2595) - 1)
    fb = np.zeros((40, len(f)))
    for m in range(40):
        a, b, c = pts[m:m + 3]
        fb[m] = np.clip(np.minimum((f - a) / (b - a), (c - f) / (c - b)), 0, None)
    L = np.log(fb @ P + 1e-12)
    C = _dct(L)[2:14]
    return C / (np.linalg.norm(C, axis=0) + 1e-12)


def _dct(L):
    n = L.shape[0]
    k = np.arange(n)
    basis = np.cos(np.pi / n * (k[:, None] + 0.5) * k[None, :])        # DCT-II
    return basis.T @ L


def words(path, model):
    """Whisper's words for path (lowercase, no punctuation), or None when whisper is unavailable."""
    d = tempfile.mkdtemp(prefix="vocalscore-asr-")
    wav = os.path.join(d, "v.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", wav], check=True,
                   stdin=subprocess.DEVNULL)
    subprocess.run(["nice", "-n", "10", "whisper", wav, "--model", model, "--language", "en", "--output_dir", d,
                        "--output_format", "json", "--fp16", "False", "--verbose", "False",
                        # bounded and loop-free: a separated stem's silences sent tiny.en into temperature-fallback
                        # re-decoding (4.3 CPU-hours on 25 threads, still at its first window)
                        "--threads", "4", "--condition_on_previous_text", "False",
                        "--temperature_increment_on_fallback", "None"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL,
                       env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    try:
        text = json.load(open(os.path.join(d, "v.json")))["text"]
    except (OSError, ValueError, KeyError):
        return None
    return re.findall(r"[a-z']+", text.lower())


def word_similarity(ref, ours):
    """1 - word edit distance / len(ref) (0..1, floored at 0)."""
    if not ref:
        return None
    prev = list(range(len(ours) + 1))
    for i, a in enumerate(ref, 1):
        cur = [i]
        for j, b in enumerate(ours, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a != b)))
        prev = cur
    return max(0.0, 1 - prev[-1] / len(ref))


def rescale(v, chance):
    return round(100 * (v - chance) / (1 - chance), 2) if chance < 1 else None


def score(rx, ox, a=0, b=None):
    """Terms over frames [a, b) (10 ms frames) of two mono signals already on the same timeline."""
    lr, lo = band_level(rx), band_level(ox)
    n = min(len(lr), len(lo))
    lr, lo = lr[:n], lo[:n]
    ar, ao = active(lr), active(lo)
    b = n if b is None else min(b, n)
    sl = slice(a, b)
    out = {}
    inter = (ar[sl] & ao[sl]).sum()
    denom = ar[sl].sum() + ao[sl].sum()
    out["activity"] = round(100 * 2 * inter / denom, 2) if denom else None
    sr_, so = syllables(lr, ar), syllables(lo, ao)
    t0, t1 = a * HOP / SR, b * HOP / SR
    sr_, so = sr_[(sr_ >= t0) & (sr_ < t1)], so[(so >= t0) & (so < t1)]
    if len(sr_) >= 4:
        m, offs = _match(sr_, so)
        fv = 2 * m / (len(sr_) + len(so))
        dur = max(t1 - t0, 1e-9)
        ch = np.mean([2 * _match(sr_, np.sort(t0 + (so - t0 + s * dur) % dur))[0] / (len(sr_) + len(so)) for s in SHIFTS])
        out["cadence"] = rescale(fv, ch)
        out["syllables"] = {"ref": int(len(sr_)), "ours": int(len(so)), "matched": int(m),
                            "offset_ms": round(1000 * float(np.median(offs)), 1) if len(offs) else None}
    else:
        out["cadence"], out["syllables"] = None, {"ref": int(len(sr_)), "ours": int(len(so))}
    both = np.zeros(n, bool)
    both[sl] = ar[sl] & ao[sl]
    if both.sum() >= 20:
        pr, po = f0(rx, both), f0(ox, both)
        d = np.abs(pr - po)[both]
        out["pitch"] = round(100 * float(np.mean(d < 0.5)), 2)
        out["pitch_octave_free"] = round(100 * float(np.mean(np.minimum(d % 12, 12 - d % 12) < 0.5)), 2)
        mr, mo = mfcc(rx), mfcc(ox)
        k = min(mr.shape[1], mo.shape[1], n)
        bk = both[:k]
        cos = (mr[:, :k] * mo[:, :k]).sum(0)
        real = float(cos[bk].mean())
        chance = float(np.mean([(mr[:, :k] * np.roll(mo[:, :k], int(s * k), axis=1)).sum(0)[bk].mean() for s in SHIFTS]))
        out["vowels"] = rescale(real, chance)
    else:
        out["pitch"] = out["pitch_octave_free"] = out["vowels"] = None
    out["frames_both_singing"] = int(both.sum())
    return out


def _match(r, c, tol=TOL):
    if not len(r) or not len(c):
        return 0, np.zeros(0)
    pairs = []
    for i, t in enumerate(r):
        lo_, hi_ = np.searchsorted(c, t - tol), np.searchsorted(c, t + tol, side="right")
        pairs += [(abs(c[j] - t), i, j) for j in range(lo_, hi_)]
    pairs.sort()
    ur, uc, offs = set(), set(), []
    for _, i, j in pairs:
        if i not in ur and j not in uc:
            ur.add(i), uc.add(j), offs.append(c[j] - r[i])
    return len(offs), np.array(offs)


def render(song, tracks, seed, out):
    cmd = [chirpbin.resolve("chirp"), "render", "-f", song, "-o", out]
    for t in tracks:
        cmd += ["--solo", t]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    r = subprocess.run(["nice", "-n", "12", *cmd], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode or not os.path.exists(out):
        raise SystemExit(f"vocalscore: render failed: {r.stderr.strip()[-300:]}")


def main(argv):
    a = list(argv)

    def opt(k, d=None):
        if k in a:
            i = a.index(k)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return d

    asr, as_json = "--asr" in a, "--json" in a
    a = [x for x in a if x not in ("--asr", "--json")]
    model, seed, keep = opt("--asr-model", "base.en"), opt("--seed"), opt("--keep")
    w0, w1 = opt("--from"), opt("--to")
    rend = None
    if "--render" in a:
        i = a.index("--render")
        rend = (a[i + 1], a[i + 2].split(","))
        del a[i:i + 3]
    if not a:
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    ref = a[0]
    rest = a[1:]
    tmp = None
    if rend:
        ours = keep or tempfile.mktemp(suffix=".wav", prefix="vocalscore-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
        tmp = None if keep else ours
        render(rend[0], rend[1], seed, ours)
    else:
        if not rest:
            raise SystemExit(__doc__.strip().split("\n\n")[1])
        ours, rest = rest[0], rest[1:]
    bounds = [float(v) for v in rest[0].split(",")] if rest else None
    try:
        rx, ox = load(ref).mean(1), load(ours).mean(1)
        if len(ox) < len(rx):
            ox = np.concatenate([ox, np.zeros(len(rx) - len(ox), ox.dtype)])
        ox = ox[:len(rx)]
        if w0 is not None or w1 is not None:
            i0 = int(float(w0 or 0) * SR)
            i1 = int(float(w1) * SR) if w1 is not None else len(rx)
            rx, ox, bounds = rx[i0:i1], ox[i0:i1], None
            if asr:
                d = tempfile.mkdtemp(prefix="vocalscore-win-")
                import wave
                for name, x in (("ref", rx), ("ours", ox)):
                    with wave.open(os.path.join(d, name + ".wav"), "wb") as f:
                        f.setnchannels(1), f.setsampwidth(2), f.setframerate(SR)
                        f.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
                ref, ours = os.path.join(d, "ref.wav"), os.path.join(d, "ours.wav")
        fa, fb = (int(bounds[0] * SR / HOP), int(bounds[-1] * SR / HOP)) if bounds else (0, None)
        res = {"whole": score(rx, ox, fa, fb)}
        if bounds:
            res["sections"] = [{"start": s0, "end": s1, **score(rx, ox, int(s0 * SR / HOP), int(s1 * SR / HOP))}
                               for s0, s1 in zip(bounds[:-1], bounds[1:])]
        if asr:
            wr, wo = words(ref, model), words(ours, model)
            res["words"] = {"score": None if wr is None or wo is None else round(100 * word_similarity(wr, wo), 2),
                            "ref_heard": " ".join(wr or [])[:400], "ours_heard": " ".join(wo or [])[:400],
                            "model": model}
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    if as_json:
        print(json.dumps(res))
        return
    w = res["whole"]
    print(f"activity {w['activity']}  cadence {w['cadence']}  pitch {w['pitch']} (octave-free {w['pitch_octave_free']})  "
          f"vowels {w['vowels']}   syllables {w['syllables']}  frames both singing {w['frames_both_singing']}")
    for s in res.get("sections", []):
        print(f"  {s['start']:7.1f}-{s['end']:7.1f} s  activity {s['activity']}  cadence {s['cadence']}  pitch {s['pitch']}  "
              f"vowels {s['vowels']}")
    if "words" in res:
        print(f"words {res['words']['score']}  ({res['words']['model']})\n  record: {res['words']['ref_heard']}\n"
              f"  ours:   {res['words']['ours_heard']}")


if __name__ == "__main__":
    main(sys.argv[1:])
