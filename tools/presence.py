#!/usr/bin/env python3
"""presence: how audible each of a song's tracks is inside its own mix (chirp-eco, 5 Nov; chirper-three found layers
30-50 dB under the mix in two Accretion songs by soloing them one at a time: parts nobody can hear).

  presence.py ID [--from POS --to POS] [--seed 0] [-j 3] [--buried -25] [--rms] [--json]
  presence.py ID --windows 3-10:wait 41-56:riffA 309-311 ...    (several windows in ONE run: a table for each)
  presence.py --song FILE ...                       (any song file; default songs/ID.yaml)
  presence.py ... --preroll 8                       (a late window of a long song, several times faster: see below)
  presence.py ... --stereo                          (both channels' power, not the mono sum: see below)

Renders the mix and every top-level track solo over the window (whole song by default; POS as chirp render takes it:
bars 49, beats 12b, seconds 30s), all unmastered (loudness=null) with the groove pin at nice 12, and prints per track:
  vs mix   its level against the mix while it SOUNDS (0.4 s frames where the solo is within 50 dB of its own peak
           frame), so a part that plays briefly is judged on when it plays, not diluted by its silence
  near     the share of those frames where it is within 10 dB of the mix (how often it can be followed)
  active   the share of the window it sounds at all
and flags BURIED (vs mix below --buried, default -25 dB) and LOUDEST. Levels are K-weighted (BS.1770, as LUFS:
the sub does not swamp the measure and hats are judged as heard); --rms for plain RMS. Tracks silent in the window
are listed as such, not as buried. Muted tracks are skipped. Read-only.

--windows FROM-TO[:label] ... is for auditing a song section by section. A window render starts from the top, so a
window by itself costs a part-render of every track; with --windows the mix and every track are rendered ONCE, to the
end of the last window, and each window is cut from that (the same samples: tools/wincut.py), so twenty sections cost
what one costs. A song wincut cannot place (a tempo that changes, a meter other than 4/4) is rendered window by window.

--preroll SECS: start each render SECS seconds before the (first) window instead of at the top of the song
(`chirp render --preroll`: the engine warms its effects over those seconds). For a window late in a long song that is
the difference between rendering thirteen minutes of every track and rendering twenty seconds: on Common Time's bars
390-397 a drum alone took 4.6 s for 18.9, the bass 4.6 s for 36.3, and the samples were the SAME (kick, bass, a
guitar: bit for bit at 8 s; the whole mix within -105 dB). A part on a bus with a `rotary` still renders from the top
(bd-e11da9), so the mix of such a song gains less (180 s for 256). Tails longer than SECS are cut short: 8 is plenty
for levels. With --windows the renders start SECS before the EARLIEST window, so it pays when the windows sit
together late in the song and costs nothing otherwise. (chirper-zero, Common Time v46: 49 tracks to bar 397 took
about ten minutes.) --preroll 0 is the same as leaving it out.

--stereo: EVERY LEVEL HERE IS READ FROM THE MONO SUM (left + right) unless you ask for --stereo, which reads both
channels' power as a loudness meter does. In the mono sum a hard-panned part reads about 1.5 dB lower than the same
part at pan 0.75, and 3 dB lower than at the centre, though alone it is as loud by LUFS: two takes a side at pans 1
and 0.75 look unequal here when they are not (chirper-zero, Common Time v46). Use --stereo to compare parts at
different pans; the yardstick below and every figure quoted before 14 Nov are mono-sum readings.

A yardstick for a VOICE (14 Nov, for chirper-zero's question on Odd Sympathy v5, "what does `near` predict for an
ear"): the same measure taken on eleven Meshuggah records, the vocals stem against the record, reads vs mix -9.1 dB
(-6.8 to -9.9) and near 69% (52% to 82%). Those are voices a listener follows through a full band. A voice at -11 to
-12 dB and near 14-37% sits under every one of them; a recogniser read 5 of its 24 words in the mix and 14 alone.
Brought to -6.0 dB and near 70% (v7) it read 10 and 8 on two seeds. So this measure ranks what was tried and the
recogniser does not: in a full metal mix it is a floor, not a scale (tools/wordread.py says how far it can be trusted).

What it cannot see (chirper-zero, Common Time v22): a pure tone has all its energy in one band. A sine-like part read
-12 to -14 dB here ("buried", 5 dB under the lead) while it put its section's 250-500 Hz 3.8 dB further over the
reference records (tools/stembal.py). Both readings were right. A level under the mix is not a share of a band: for a
part with a narrow spectrum run stembal on the section as well.

SHORT STROKES (16 Nov, chirper-zero, Running Total v8: a woodblock knock at ONE velocity read -11.2 dB where it struck
every bar or so and -3.6 where it struck eight times in two bars). `vs mix` is the part's power while it SOUNDS, and a
short stroke with a tail (a room, a reverb, a ringing bar) sounds for the whole window: active 1.00. So `vs mix`
averages each stroke with its tail and follows how OFTEN the part strikes, not how loud a stroke is. Under the table,
from the same renders: the parts made of strokes whose strokes `vs mix` reads 3 dB or more low, each with THE STROKE
ITSELF against the mix: every stroke's own tenth of a second against the mix's same tenth (the median, low to high, how
many). A stroke is a tenth of a second 10 dB over what the part was doing 0.1 to 0.2 s before, at a local peak, within
30 dB of the part's loudest. Read that figure to set one level for a part that strikes at different rates: on Running
Total v8, with velocity set by the gap so that `vs mix` read -10 to -13 everywhere, the knock's strokes were -2.5 to
-3.2 dB under the mix where it is sparse and -6.2 to -7.3 where it is dense (the kick's strokes: -2.8 to -4.8).
What it is not: how loud a stroke SOUNDS (a tenth of a second of K-weighted power is not loudness, and a stroke
masked by a cymbal on the same beat reads the same as one in a gap); a held or fast-repeating part has no strokes
here (nothing falls 10 dB between them) and `vs mix` is the figure for it.

WHOSE BAND IS IT (16 Nov, chirper-zero, three times in one day: a synth riser that was most of a climax's 500 Hz to
1 kHz for five versions, a bass's lift, a held lead 3.7 dB under the whole mix at 500 Hz-1 kHz; each found only when
the part alone was put under the mix by band, by hand). Under each table, from the same renders (nothing more is
rendered): for each of the nine bands tools/stembal.py reads, the tracks that ALONE are within 6 dB of the mix's own
band there, nearest first (0 = the track is the band; -3 = about half of it). A band nobody holds that closely is
shared and is left out. The same caution as stembal's --parts: a track alone still goes through its bus and the
master, and tracks that share a band add in power only when they are unrelated. Always the mono sum, whatever
--stereo says of the levels. When a band reads over the records (stembal), look here for its owner before mending.
LEFT AND RIGHT TOGETHER (16 Nov, chirper-zero, Odd Sympathy v24: two music boxes, el and er, one of them alone 5.3 dB
under the mix's 500 Hz-1 kHz and so listed; "summed, the pair was 2.6 dB under", by hand. Had each been 6.5 under,
nothing would have been listed). Tracks that are the left and the right of one part by name (gl/gr, gl2/gr2,
v0l/v0r, el/er) are also read as a pair, their band powers added, and listed under the single tracks when the pair
is within 6 dB of the mix's band. Added powers are right for a left and a right that do not sound the same thing at
the same instant (two takes, an echo); a pair in unison could read up to 3 dB higher still. A PURE-TONED PART (a
music box, a bell, a marimba, a sine) holds its fundamental's band at a `vs mix` a guitar would not: read this
block, not the level, for such a part.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import levels  # noqa: E402
import likeness as L  # noqa: E402
import wincut  # noqa: E402
from keybench import EDGES, LABELS  # noqa: E402

ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
FRAME = 0.4          # seconds
SOUNDS_DB = 50.0     # a frame "sounds" within this many dB of the track's loudest frame
NEAR_DB = 10.0
STROKE_S, STROKE_HOP_S = 0.1, 0.05   # a stroke is read in a tenth of a second, looked for every twentieth
STROKE_RISE_DB = 10.0   # a stroke: the part this far over what it was doing 0.1 to 0.2 s before, at a local peak ...
STROKE_FLOOR_DB = 30.0  # ... and within this of the part's loudest tenth of a second in the window
STROKE_LOW_DB = 3.0     # listed when the strokes' median is this far over `vs mix`
HOLDS_DB = -6.0      # a track alone within this of the mix's own band HOLDS the band
BAND_FLOOR_DB = -40.0   # a band this far under the mix's whole is not read: next to nothing is in it


def band_power(x, sr):
    """The power of the mono sum in the nine bands tools/stembal.py reads, every sample counted alike (Hann frames a
    quarter of a frame apart). Zeros for a stretch shorter than one frame."""
    m = (x.mean(axis=1) if x.ndim > 1 else x).astype(np.float64)
    n, hop = 8192, 2048
    if len(m) < n:
        return np.zeros(len(LABELS))
    sp, w, k = np.zeros(n // 2 + 1), np.hanning(n), 0
    for i in range(0, len(m) - n + 1, hop):
        sp += np.abs(np.fft.rfft(m[i:i + n] * w)) ** 2
        k += 1
    fr = np.fft.rfftfreq(n, 1.0 / sr)
    return np.array([sp[(fr >= lo) & (fr < hi)].sum() for lo, hi in zip(EDGES, EDGES[1:])]) / k


def holds(mix, solo):
    """{band label: dB against the mix's own band} for the bands a track alone HOLDS: within HOLDS_DB of the mix's
    band, in a band the mix has something in (BAND_FLOOR_DB of its whole)."""
    out = {}
    whole = float(mix.sum())
    for lb, m, s in zip(LABELS, mix, solo):
        if whole > 0 and m > whole * 10 ** (BAND_FLOOR_DB / 10) and s > 0:
            d = 10 * np.log10(s / m)
            if d >= HOLDS_DB:
                out[lb] = round(float(d), 1)
    return out


def frames_db(x, sr, frame=FRAME, kweight=False, stereo=False):
    """Per-frame level in dB: RMS, or K-weighted (BS.1770's filter, LUFS-like) with KWEIGHT. Of the mono sum; with
    STEREO, of both channels' power (the sum of each channel's mean square, as a loudness meter counts)."""
    chans = [x[:, c] for c in range(x.shape[1])] if stereo and x.ndim > 1 else [x.mean(axis=1) if x.ndim > 1 else x]
    n = max(1, int(frame * sr))
    k = len(chans[0]) // n
    if k == 0:
        return np.array([-120.0])
    power = np.zeros(k)
    for m in chans:
        if kweight:
            m = levels.k_weight(m.astype(np.float64), sr)
        power += (m[:k * n].astype(np.float64).reshape(k, n) ** 2).mean(1)
    return 20 * np.log10(np.sqrt(power) + 1e-9)


def fine_db(x, sr, kweight=False, stereo=False):
    """Levels in dB a tenth of a second long, one every twentieth; weighted and summed as frames_db does."""
    chans = [x[:, c] for c in range(x.shape[1])] if stereo and x.ndim > 1 else [x.mean(axis=1) if x.ndim > 1 else x]
    n, hop = max(1, int(STROKE_S * sr)), max(1, int(STROKE_HOP_S * sr))
    if len(chans[0]) < n:
        return np.array([-120.0])
    starts = np.arange(0, len(chans[0]) - n + 1, hop)
    power = np.zeros(len(starts))
    for m in chans:
        m = levels.k_weight(m.astype(np.float64), sr) if kweight else m.astype(np.float64)
        c = np.concatenate([[0.0], np.cumsum(m ** 2)])
        power += (c[starts + n] - c[starts]) / n
    return 20 * np.log10(np.sqrt(np.maximum(power, 0.0)) + 1e-9)


def strokes(mix_f, solo_f):
    """A part's strokes against the mix, from fine_db levels of both: {n, vs_mix_db (the median of each stroke's own
    tenth of a second against the mix's same tenth), lo, hi (the 10th and 90th percentiles)}; None when the part has
    fewer than two strokes in the window (a held part, a fast-repeating one, one hit)."""
    k = min(len(mix_f), len(solo_f))
    s, m = solo_f[:k], mix_f[:k]
    if k < 5:
        return None
    top, idx = float(s.max()), []
    for i in range(2, k):                             # the first tenth of a second has no "before" to rise from
        if s[i] < top - STROKE_FLOOR_DB or s[i] < s[i - 1] or (i + 1 < k and s[i] <= s[i + 1]):
            continue
        if s[i] < s[max(0, i - 4):i - 1].min() + STROKE_RISE_DB:
            continue
        if idx and i - idx[-1] < 2:                   # one stroke seen twice: keep the louder reading
            if s[i] > s[idx[-1]]:
                idx[-1] = i
            continue
        idx.append(i)
    if len(idx) < 2:
        return None
    d = s[idx] - m[idx]
    return {"n": len(idx), "vs_mix_db": round(float(np.median(d)), 1), "lo": round(float(np.percentile(d, 10)), 1),
            "hi": round(float(np.percentile(d, 90)), 1)}


def sides(names):
    """[(left, right)] of the tracks that are the left and the right of one part by name: gl/gr, gl2/gr2, v0l/v0r."""
    by = {}
    for n in names:
        m = re.fullmatch(r"(.+?)([lr])(\d*)", n, re.I)
        if m:
            by.setdefault((m.group(1).lower(), m.group(3)), {})[m.group(2).lower()] = n
    return [(v["l"], v["r"]) for v in by.values() if len(v) == 2]


def pair_holds(rows, mix, power):
    """Adds rows[left]["pair"] = {with: right, holds: {...}} for each left and right that both sound: the bands the two
    hold TOGETHER (their band powers added), as holds() reads one track."""
    for left, right in sides(list(rows)):
        if not rows[left]["silent"] and not rows[right]["silent"]:
            rows[left]["pair"] = {"with": right, "holds": holds(mix, power[left] + power[right])}


def presence(mix_db, solo_db, buried=-25.0):
    """{vs_mix_db, near, active, buried} for one track's frame levels against the mix's (same frame grid)."""
    k = min(len(mix_db), len(solo_db))
    mix_db, solo_db = mix_db[:k], solo_db[:k]
    peak = float(solo_db.max()) if k else -120.0
    on = solo_db > max(peak - SOUNDS_DB, -100.0)
    if peak < -100.0 or not on.any():
        return {"vs_mix_db": None, "near": 0.0, "active": 0.0, "buried": True, "silent": True}
    # power means over the sounding frames
    p = lambda v: 10 * np.log10(np.mean(10 ** (v / 10)) + 1e-12)  # noqa: E731
    vs = p(solo_db[on]) - p(mix_db[on])
    near = float(np.mean(solo_db[on] >= mix_db[on] - NEAR_DB))
    return {"vs_mix_db": round(float(vs), 1), "near": round(near, 2), "active": round(float(on.mean()), 2),
            "buried": bool(vs < buried), "silent": False}


def plan_canonical(pin, song):
    """The song as chirp plan --json resolves it."""
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True)
    d = json.loads(r.stdout)
    d = d.get("data") or d
    return d.get("canonical") or {}


def plan_tracks(pin, song, canon=None):
    """[(name, muted)] of the song's top-level tracks, from chirp plan --json."""
    out = []
    for t in (plan_canonical(pin, song) if canon is None else canon).get("tracks") or []:
        if t.get("name"):
            out.append((t["name"], bool(t.get("mute"))))
    return out


def render(pin, song, out, seed, win, solo=None, preroll=None):
    cmd = ["nice", "-n", "12", pin, "render", "-f", song, "--seed", str(seed), "--set", "loudness=null", "-o", out]
    if win[0]:
        cmd += ["--from", win[0]] + (["--preroll", f"{preroll:g}"] if preroll else [])
    if win[1]:
        cmd += ["--to", win[1]]
    if solo:
        cmd += ["--solo", solo]
    env = dict(os.environ, RAYON_NUM_THREADS="2")
    env.pop("LD_LIBRARY_PATH", None)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode:
        raise RuntimeError(f"render failed ({solo or 'mix'}): {r.stderr.strip()[-300:]}")
    return out


def one_window(pin, song, live, win, a, work):
    """{track: presence} for one window: the mix and every live track rendered over it."""
    jobs = [("__mix__", None)] + [(n, n) for n in live]
    with ThreadPoolExecutor(max(1, a.j)) as ex:
        wavs = dict(zip([j[0] for j in jobs], ex.map(
            lambda j: render(pin, song, os.path.join(work, f"{len(j[0])}-{abs(hash(j[0]))}.wav"), a.seed, win, j[1],
                             a.preroll),
            jobs)))
    kw = not a.rms
    x = L.load(wavs["__mix__"])
    mix, mixb, rows = frames_db(x, L.SR, kweight=kw, stereo=a.stereo), band_power(x, L.SR), {}
    mixf, power = fine_db(x, L.SR, kweight=kw, stereo=a.stereo), {}
    for n in live:
        x = L.load(wavs[n])
        rows[n] = presence(mix, frames_db(x, L.SR, kweight=kw, stereo=a.stereo), a.buried)
        power[n] = band_power(x, L.SR)
        rows[n]["holds"] = {} if rows[n]["silent"] else holds(mixb, power[n])
        rows[n]["strokes"] = None if rows[n]["silent"] else strokes(mixf, fine_db(x, L.SR, kweight=kw, stereo=a.stereo))
    pair_holds(rows, mixb, power)
    for f in wavs.values():
        os.remove(f)
    return rows


def many_windows(pin, song, live, windows, secs, a, work):
    """[{track: presence}] a window: the mix and every live track rendered ONCE, to the end of the last window, and
    each window cut from that (tools/wincut.py: the same samples a window render gives). With --preroll the one
    render starts that many seconds before the earliest window instead of at the top."""
    last = max(range(len(secs)), key=lambda i: secs[i][1])
    to = windows[last].partition(":")[0].partition("-")[2]
    kw = not a.rms
    frm, base = None, 0
    if a.preroll:
        first = min(range(len(secs)), key=lambda i: secs[i][0])
        frm = windows[first].partition(":")[0].partition("-")[0]
        base = wincut.frames(secs[first][0], secs[first][0], L.SR)[0]      # the render's first frame, counted from the top

    def one(job):
        name, solo = job
        wav = render(pin, song, os.path.join(work, f"{len(name)}-{abs(hash(name))}.wav"), a.seed, (frm, to), solo, a.preroll)
        x = L.load(wav)
        os.remove(wav)
        out = []
        for s0, s1 in secs:
            f0, f1 = wincut.frames(s0, s1, L.SR)
            seg = x[f0 - base:f1 - base]
            out.append((frames_db(seg, L.SR, kweight=kw, stereo=a.stereo), band_power(seg, L.SR),
                        fine_db(seg, L.SR, kweight=kw, stereo=a.stereo)))
        return out

    jobs = [("__mix__", None)] + [(n, n) for n in live]
    with ThreadPoolExecutor(max(1, a.j)) as ex:
        db = dict(zip([j[0] for j in jobs], ex.map(one, jobs)))
    many = []
    for i in range(len(secs)):
        rows = {n: presence(db["__mix__"][i][0], db[n][i][0], a.buried) for n in live}
        for n in live:
            rows[n]["holds"] = {} if rows[n]["silent"] else holds(db["__mix__"][i][1], db[n][i][1])
            rows[n]["strokes"] = None if rows[n]["silent"] else strokes(db["__mix__"][i][2], db[n][i][2])
        pair_holds(rows, db["__mix__"][i][1], {n: db[n][i][1] for n in live})
        many.append(rows)
    return many


def stroke_lines(rows):
    """The lines of SHORT STROKES under a table: the parts whose strokes `vs mix` reads STROKE_LOW_DB or more low."""
    low = sorted(((r["strokes"]["vs_mix_db"] - r["vs_mix_db"], n) for n, r in rows.items()
                  if r.get("strokes") and r.get("vs_mix_db") is not None
                  and r["strokes"]["vs_mix_db"] - r["vs_mix_db"] >= STROKE_LOW_DB), reverse=True)
    if not low:
        return []
    out = ["  short strokes (`vs mix` averages a stroke with its tail, so it follows how OFTEN a part strikes; here each stroke's own "
           "tenth of a second against the mix's same tenth: the median, low to high, how many):"]
    for _, n in low:
        st = rows[n]["strokes"]
        out.append(f"    {n:16s} {st['vs_mix_db']:+7.1f}  ({st['lo']:+.1f} to {st['hi']:+.1f}; {st['n']} strokes)"
                   f"   where vs mix says {rows[n]['vs_mix_db']:+.1f}")
    return out


EQ_DB = 2.0               # WHAT AN EQ ON IT WOULD MOVE: the turn-up it is worked out for


def moves(d, gain=EQ_DB):
    """(the part's share of the mix's band, how far the mix's band moves in dB) when a part that alone reads d dB against
    the band is turned up by `gain` dB there: powers added, as if the parts were unrelated."""
    share = min(1.0, 10 ** (d / 10))
    return share, 10 * np.log10(1 - share + share * 10 ** (gain / 10))


def eq_lines(rows):
    """The lines of WHAT AN EQ ON IT WOULD MOVE, under WHOSE BAND IS IT: for each holder of a band (alone, or a left and
    a right together), its share of the band and how far the mix's own band moves when it alone is turned up EQ_DB there.
    chirper-zero, 16 Nov (Plain Hunt, a round not made): "BEFORE AN EQ, ASK WHAT SHARE OF THE BAND THE PART HAS (WHOSE
    BAND pairs at -5 mean a third each: 2 dB on them is 0.7 on the mix)": he benched two tilts on four guitars to learn
    that 4.5 dB on them moved the song by under 1 dB."""
    by = {}
    for n, r in rows.items():
        for lb, d in (r.get("holds") or {}).items():
            by.setdefault(lb, []).append((d, n))
        for lb, d in ((r.get("pair") or {}).get("holds") or {}).items():
            by.setdefault(lb, []).append((d, f"{n}+{r['pair']['with']}"))
    if not by:
        return []
    out = [f"  what an eq on it would move (its share of the band's power; the mix's own band when that part alone is turned up "
           f"{EQ_DB:g} dB across it; powers added, a guide: a peak gives less than its gain across a whole band):"]
    for lb in LABELS:
        if lb in by:
            got = sorted(by[lb], reverse=True)
            out.append(f"    {lb:8s} " + ", ".join("{} {:.0%} {:+.1f}".format(n, *moves(d)) for d, n in got[:4])
                       + (f" +{len(got) - 4}" if len(got) > 4 else ""))
    return out


def whose_lines(rows):
    """The lines of WHOSE BAND IS IT under a table: for each band, the tracks that alone hold it, nearest first."""
    by = {lb: sorted(((r["holds"][lb], n) for n, r in rows.items() if lb in (r.get("holds") or {})), reverse=True) for lb in LABELS}
    two = {lb: sorted(((r["pair"]["holds"][lb], f"{n}+{r['pair']['with']}") for n, r in rows.items()
                       if lb in (r.get("pair") or {}).get("holds", {})), reverse=True) for lb in LABELS}
    if not any(by.values()) and not any(two.values()):
        return []
    out = [f"  whose band is it (a track ALONE within {-HOLDS_DB:g} dB of the mix's own band; 0 = it is the band, -3 about half):"]
    for lb in LABELS:
        if by[lb]:
            out.append(f"    {lb:8s} " + ", ".join(f"{n} {d:+.1f}" for d, n in by[lb][:4])
                       + (f" +{len(by[lb]) - 4}" if len(by[lb]) > 4 else ""))
    if any(two.values()):
        out.append("    a left and a right TOGETHER (their powers added: a pair can hold a band neither holds alone):")
        for lb in LABELS:
            if two[lb]:
                out.append(f"    {lb:8s} " + ", ".join(f"{n} {d:+.1f}" for d, n in two[lb][:4])
                           + (f" +{len(two[lb]) - 4}" if len(two[lb]) > 4 else ""))
    return out


def report(song, span, a, tracks, live, rows):
    order = sorted(rows, key=lambda n: (rows[n]["vs_mix_db"] is None, -(rows[n]["vs_mix_db"] or -999)))
    print(f"{os.path.basename(song)} ({span}; seed {a.seed}; unmastered, {'RMS' if a.rms else 'K-weighted'}"
          f"{', both channels' if a.stereo else ''}): {len(live)} tracks"
          + (f", {len(tracks) - len(live)} muted skipped" if len(tracks) > len(live) else ""))
    print(f"  {'track':16s} {'vs mix':>8s} {'near':>6s} {'active':>7s}")
    loud = order[0] if order else None
    for n in order:
        r = rows[n]
        if r["silent"]:
            print(f"  {n:16s} {'silent':>8s}  (not in this window)")
            continue
        flag = "BURIED" if r["buried"] else ("LOUDEST" if n == loud else "")
        print(f"  {n:16s} {r['vs_mix_db']:+7.1f}  {r['near']:6.2f} {r['active']:7.2f}  {flag}")
    nb = sum(1 for r in rows.values() if r["buried"] and not r["silent"])
    if nb:
        print(f"  {nb} track(s) under {a.buried:g} dB while they sound: inaudible in the mix (raise, cut, or let them go)")
    for ln in stroke_lines(rows) + whose_lines(rows) + eq_lines(rows):
        print(ln)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--song")
    ap.add_argument("--from", dest="frm")
    ap.add_argument("--to")
    ap.add_argument("--windows", nargs="+", help="FROM-TO[:label] ...: several windows in one run, every track rendered once")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--buried", type=float, default=-25.0)
    ap.add_argument("--pin")
    ap.add_argument("--rms", action="store_true", help="plain RMS instead of K-weighted levels")
    ap.add_argument("--preroll", type=float, help="start each render this many seconds before the (first) window, not at the top")
    ap.add_argument("--stereo", action="store_true", help="read both channels' power (as a loudness meter), not the mono sum")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    song = a.song or (os.path.join(ROOT, "songs", f"{a.id}.yaml") if a.id else None)
    if not song or not os.path.exists(song):
        raise SystemExit("presence: give a climb ID (songs/ID.yaml) or --song FILE")
    if a.windows and (a.frm or a.to):
        raise SystemExit("presence: --windows or --from/--to, not both")
    if a.preroll is not None and a.preroll < 0:
        raise SystemExit("presence: --preroll takes seconds")
    if a.preroll == 0:
        a.preroll = None                           # --preroll 0: from the top, as without it (a window at the song's start)
    for w in a.windows or []:
        if "-" not in w.partition(":")[0]:
            raise SystemExit(f"presence: --windows takes FROM-TO[:label], not {w!r}")
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    canon = plan_canonical(pin, song)
    tempo = canon.get("tempo", 120.0)
    if isinstance(tempo, (int, float)) and not isinstance(tempo, bool) and tempo > 0:
        # a window's TO is where it STOPS: one bar is 28-29, and 28-28 is no window (it printed a header and no rows)
        for w in (a.windows or []) + ([f"{a.frm}-{a.to}"] if a.frm and a.to else []):
            lo, _, hi = w.partition(":")[0].partition("-")
            s0, s1 = wincut.position(lo, tempo), wincut.position(hi, tempo)
            if s0 is not None and s1 is not None and s1 < s0:
                raise SystemExit(f"presence: {lo}-{hi} runs backwards (TO is where it stops)")
            if s0 is not None and s1 == s0:
                one = f", so bar {lo} alone is {lo}-{int(lo) + 1}" if lo.isdigit() else ""
                raise SystemExit(f"presence: {lo}-{hi} is an empty window: TO is where it stops{one}")
    tracks = plan_tracks(pin, song, canon)
    live = [n for n, muted in tracks if not muted]
    win = (a.frm, a.to)
    work = tempfile.mkdtemp(prefix="presence-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    try:
        if a.windows:
            spans = [tuple(w.partition(":")[0].split("-", 1)) for w in a.windows]
            secs = wincut.window_seconds(canon, a.windows)
            many = many_windows(pin, song, live, a.windows, secs, a, work) if secs \
                else [one_window(pin, song, live, sp, a, work) for sp in spans]
        else:
            rows = one_window(pin, song, live, win, a, work)
    finally:
        for f in os.listdir(work):
            os.remove(os.path.join(work, f))
        os.rmdir(work)
    if a.windows:
        labels = [w.partition(":")[2] for w in a.windows]
        if a.json:
            print(json.dumps({"song": song, "muted": [n for n, m in tracks if m], "windows": [
                {"window": list(sp), "label": lb, "tracks": r} for sp, lb, r in zip(spans, labels, many)]}))
            return
        for sp, lb, r in zip(spans, labels, many):
            report(song, (f"{lb}: " if lb else "") + f"{sp[0]} -> {sp[1]}", a, tracks, live, r)
        return
    if a.json:
        print(json.dumps({"song": song, "window": win, "muted": [n for n, m in tracks if m], "tracks": rows}))
        return
    report(song, f"{a.frm or 'start'} -> {a.to or 'end'}", a, tracks, live, rows)


if __name__ == "__main__":
    main()
