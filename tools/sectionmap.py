#!/usr/bin/env python3
"""sectionmap: a composed song as ~30 s windows, for SECTION rounds (Harry, 2 Nov: "a climber focuses really closely on
say a 30s segment (knowing its context) and makes that section stand out or blend well and keep variety moving; whole
song improvements might miss the smaller changes that make a song feel handcrafted and unique").

  sectionmap.py ID [--wav W] [--window 30] [--json]      the map: per window level, brightness, density, motion,
                                                          change from the window before, the earlier window it is most
                                                          like, flags, the ledger's last focus; then the windows to
                                                          focus on next and the commands that render them
  sectionmap.py ID --wav NEW --against OLD               per-window deltas: did the round stay in its window, and how
                                                          did that window move against its neighbours
  sectionmap.py ID --mark N --note TEXT                  record a section round on window N in the song's ledger
                                                          (compose/<album>/sections/<id>.jsonl; committed)

Windows are whole bars on the song's own tempo map (beats, so they stay put when the audio changes), about WINDOW
seconds each; a short last window joins the one before. Without --wav the song is rendered with the groove's pin
(seed 0, idle CPU priority). The numbers are a flashlight for where to look, not a score to climb.

A MARK STAYS WITH ITS MUSIC (14 Nov): a mark records the window's beats and the song's tempo and length, so when the
map is drawn on other windows (--window) it sits on the window that holds most of those beats, and when the song is
RESHAPED (a new tempo, a longer form: Plain Hunt v5 went from 96 bpm and 483 beats to 120 and 648 in one round) it is
put where that music is now, scaled along the song, and shown as "about here: marked on vN as wM". Marks made before
then carry no beats and stay with their window number, right or not: after a reshape read those by their notes.

Reading the flags: "static" and "little new vs wN" are relative to the song's own quartiles, so about a quarter of
every song's windows carry them, however good it is. The map prints the two lines under its table. "static" keys on
MOTION: the scorer's novelty curve inside the window (compscore.novelty: frames of spectral shape, chroma and level,
half a second each, against their neighbours eight seconds either way), so it is change WITHIN the window, not
onsets: a harmony that joins near the window's start and stays (Plain Hunt v7, w8) is one change and then none, and
the window is still static. "little new" keys on CHANGE: the window's mean frame against the window before's.
"little new vs wN" only says the window continues the one before.
THE MAP'S BLIND SIDE WAS RHYTHM THAT KEEPS ITS INSTRUMENTS (15 Nov, chirper-zero, Plain Hunt v9: a snare moved in
time, the same strokes on the same drum, changed no tone, harmony or level, and the window's motion went 0.0321 to
0.0315). The `rhythm` column is how far the attacks' places in the BAR change from one bar to the next inside the
window (0 = every bar alike; that window went 0.087 to 0.230). A static window whose rhythm is in the song's top
quarter (and at least 0.15) is flagged "static in tone"; the line under the map says which way each static window's
rhythm reads. It is still a flag: whether a rhythm that moves is tension or the floor going is for an ear.
WHAT ENTERS IN A STATIC WINDOW (14 Nov, chirper-zero, Common Time v48): the map's most static window had a new
wheel arriving in the middle of it, 3 to 4 dB under guitars that never stopped: "static" was "the arrival is
masked". Under the map, each static window now lists the parts that ENTER in it (from the plan: a part silent for
two bars or more before its note) and the command that says how loud they are against what was already playing.
WHERE IN A WINDOW ITS CHANGE SITS (--against; 16 Nov, chirper-zero, False Summit v11). A window is half a minute and
its residual is one number, so a change in its last five seconds reads as the whole window's. Under the table, for
each changed window whose change sits in part of it (the shortest run of seconds holding nine tenths of the
residual is no more than half the window): "w7's change sits in 3:16-3:21 (5 s of its 29): the rest of the window
reads -50.1 dB, untouched". (There a fader came down two bars before the window's end; the passage the window is
named for was untouched, and had been taken for an engine effect.)

WHAT THE NOTES DO IN A STATIC WINDOW (16 Nov, chirper-zero, False Summit v8 and Plain Hunt v13: a harmony written
on one side of a stair for ten bars, and a bell struck in a new place every row, left their windows "static": the
same instruments at the same level, so the flag cannot hear which notes). Under each static window the map now reads
the PLAN, part by part and bar by bar (a part is a pitched track or one piece of a kit; a note is its place in the
bar and its pitch class, so a line passed between octaves is the same notes): how many parts LOOP (the same every
1, 2 or 4 bars while they play), which CHANGE inside the window (a loop, then other notes from one bar on: where),
and which NEVER SETTLE (half their bars or more repeat nothing near them). A window whose parts change or never
settle is static in its SOUND, not in its notes: listen before rewriting it. A part that only enters or leaves is
the ENTERS line's, not a change.
A sung return (the chorus or hook coming back, a crest's later lines) is MEANT to repeat; hear it before rewriting.
chirper-three, t4 v24 (6 Nov): rewriting a flagged chorus return cost recurrence 96.2 -> 91.7 and the round was refused.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compscore as CS  # noqa: E402

L = CS.L
ROOT = CS.ROOT
BAND_HZ = [30 * 533.33 ** ((i + 0.5) / 40) for i in range(40)]
REPEAT_NOTES = 0.6      # a near-repeat: an earlier window whose note sequence is this close (seq_dist; a literal
REPEAT_AVG = 0.97       # repeat reads 0.0-0.3, a new melody 2.6+), whose texture and harmony are this alike, at a
                        # similar level (calibrated on P P' P P, 2 Nov)


def song_path(cid):
    c = CS.climb_of(cid)
    return os.path.join(ROOT, c.get("song") or f"songs/{cid}.yaml"), c


def meter_beats(song):
    """Beats per bar of the song's starting meter (its top-level `meter`, else 4/4)."""
    try:
        with open(song) as f:
            text = f.read()
        if text.lstrip().startswith("{"):
            m = json.loads(text).get("meter")
        else:
            import re
            mm = re.search(r"^meter:\s*[\"']?(\d+)\s*/\s*(\d+)", text, re.M)
            m = f"{mm.group(1)}/{mm.group(2)}" if mm else None
        n, d = (m or "4/4").split("/")
        return float(n) * 4.0 / float(d)
    except (OSError, ValueError, AttributeError):
        return 4.0


def beat_clock(song):
    """(beats -> seconds for an array of beats, beats per minute of reference) on the song's tempo map, or (None, None)
    when it declares no tempo."""
    pts = CS.tempo_points(song)
    bpm = CS.declared_tempo(song)
    if pts:
        segs = CS.tempo_segments(pts)
        return (lambda b: CS.map_secs(segs, np.atleast_1d(np.asarray(b, float)))), bpm
    if bpm:
        return (lambda b: np.atleast_1d(np.asarray(b, float)) * 60.0 / bpm), bpm
    return None, None


def window_beats(song, bpm, window_s=30.0):
    """How many beats a window is: whole bars of the song's meter about WINDOW_S long, whole 4-bar phrases when the
    window holds at least one."""
    bpb = meter_beats(song)
    w = round(window_s * float(bpm or 120) / 60.0 / bpb) * bpb
    phrase = 4 * bpb
    return max(2 * bpb, round(w / phrase) * phrase if w >= phrase else w)


def declared_beats(song):
    """The song's own `length` in beats ("648b"), or None when it declares none in beats."""
    try:
        with open(song) as f:
            text = f.read()
        if text.lstrip().startswith("{"):
            v = str(json.loads(text).get("length") or "")
        else:
            import re
            m = re.search(r"^length:\s*[\"']?([0-9.]+b)\b", text, re.M)
            v = m.group(1) if m else ""
        return float(v[:-1]) if v.endswith("b") else None
    except (OSError, ValueError, AttributeError):
        return None


def shape(song, n=None, window_s=30.0):
    """What lets a ledger mark be found again after the song is reshaped (a new tempo, a longer form: Plain Hunt v5
    went from 96 bpm and 483 beats to 120 and 648 in one round, and every window moved): {"tempo", "of" (its declared
    length in beats, when it has one), "beats" ([a, b] of window N on today's grid, when N is given)}. {} for a song
    with no fixed tempo, whose marks stay with their window number."""
    bpm = CS.declared_tempo(song)
    if not bpm or CS.tempo_points(song):
        return {}
    out = {"tempo": float(bpm)}
    of = declared_beats(song)
    if of:
        out["of"] = of
    if n:
        w = window_beats(song, bpm, window_s)
        out["beats"] = [float((n - 1) * w), float(min(n * w, of) if of and (n - 1) * w < of else n * w)]
    return out


def place(e, rows, now):
    """(the window of today's map a ledger entry belongs to, whether that is a guess). An entry that carries its beats
    is placed by them: on the window that holds most of them while the song has the tempo and length it had; when the
    song has been reshaped since, by its place along the song (its beats scaled to today's length), as a guess. An
    entry without them (marked before 14 Nov), or one that cannot be scaled, stays with its window number."""
    b = e.get("beats")
    if not b or not rows or rows[0]["beats"][0] is None:
        return e.get("window"), False
    same = e.get("tempo") == now.get("tempo") and e.get("of") == now.get("of")
    if not same:
        if not e.get("of") or not now.get("of"):
            return e.get("window"), True
        k = now["of"] / e["of"]
        b = [b[0] * k, b[1] * k]
    held = [(min(b[1], r["beats"][1]) - max(b[0], r["beats"][0]), -r["n"]) for r in rows]
    best = max(held)
    return (-best[1] if best[0] > 0 else e.get("window")), not same


def placed_ledger(ledger, rows, song):
    """The ledger with every entry on the window it belongs to TODAY (place): `window` is today's, `marked_as` the
    number it was marked with when that differs, `reshaped` set when the song has changed tempo or length since."""
    now = shape(song)
    out = []
    for e in ledger:
        n, guess = place(e, rows, now)
        e2 = dict(e, window=n)
        if n != e.get("window"):
            e2["marked_as"] = e.get("window")
        if guess:
            e2["reshaped"] = True
        out.append(e2)
    return out


def windows(song, dur, window_s=30.0):
    """[(beat_a, beat_b, t_a, t_b)] covering 0..DUR seconds: whole bars of the song's tempo (its map's segments when it
    has one) about WINDOW_S long. Beats are None when the song declares no tempo (plain WINDOW_S time windows)."""
    clock, bpm = beat_clock(song)
    if clock is None:
        n = max(1, int(round(dur / window_s)))
        edges = list(np.linspace(0, dur, n + 1))
        return [(None, None, a, b) for a, b in zip(edges[:-1], edges[1:])]
    pts = CS.tempo_points(song)
    total = CS.map_beats(CS.tempo_segments(pts), dur) if pts else dur * bpm / 60.0
    to_s = lambda b: float(clock(b)[0])  # noqa: E731
    w = window_beats(song, bpm, window_s)
    edges = list(np.arange(0, total, w)) + [total]
    if len(edges) > 2 and edges[-1] - edges[-2] < w / 2:
        edges.pop(-2)
    return [(float(a), float(b), to_s(a), min(dur, to_s(b))) for a, b in zip(edges[:-1], edges[1:])]


def _cos(u, v):
    u, v = np.asarray(u, float), np.asarray(v, float)
    return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-12))


def _sim(p, q):
    """How alike two windows are, 0..1: half their texture and average harmony, half their note sequence step by step
    (pitch with register, twice a beat), so a melody moved, reordered or leapt an octave reads as different
    (chirper-zero, 2 Nov: t8's octave leaps changed the window by -22 dB but the averages by 0.0025)."""
    avg = 0.5 * _cos(p["vec"], q["vec"]) + 0.5 * _cos(p["chroma"], q["chroma"])
    if p.get("seq") is None or q.get("seq") is None:
        return avg
    return 0.5 * avg + 0.5 * seq_sim(p["seq"], q["seq"])


SEMI_LO, SEMI_HI = 36, 96                          # C2 .. B6: the notes, with their register

# Groove: where in the beat the attacks fall. A 24-bin onset-phase histogram per window on the song's beat clock; 1 - its
# cosine with the previous window's is the groove change. Straight 8ths/16ths and a triplet shuffle land in different bins
# (chirper-three, 3 Nov: t4 v36's swing moved nothing in `change`, which hears texture, harmony and notes, not feel).
# Steady grooves read under ~0.06 on chirpers8; drums entering or leaving, and t4's shuffle (0.149), read 0.08 or more.
GROOVE_BINS = 24
GROOVE_NEW = 0.08


def onset_env(x, sr, hop=256, n=1024):
    """Attack strength (log-magnitude flux above its running median) at ~5 ms, with the attack times: finer than
    likeness's 21 ms frames, since a 16th and a triplet 8th differ by a 12th of a beat (~40 ms at 120 bpm)."""
    from scipy import signal
    mono = x.mean(1) if x.ndim == 2 else x
    _, t, Z = signal.stft(mono, sr, nperseg=n, noverlap=n - hop, boundary=None, padded=False)
    mag = np.log1p(100 * np.abs(Z))
    flux = np.maximum(np.diff(mag, axis=1), 0).sum(0)
    k = 2 * int(0.25 * sr / hop) + 1
    base = signal.medfilt(flux, k) if len(flux) > k else np.median(flux)
    return np.maximum(flux - base, 0), t[1:] + n / (2 * sr)        # a frame's flux leads its attack by half a window


def groove_hist(env, times, clock, ba, bb):
    """Onset strength by position within the beat (GROOVE_BINS bins, one-bin circular smear), normalised."""
    grid = np.arange(ba, bb + 1e-9, 1 / 96)
    secs = clock(grid)
    sel = (times >= secs[0]) & (times < secs[-1])
    beats = np.interp(times[sel], secs, grid)
    h = np.bincount(((beats % 1.0) * GROOVE_BINS).astype(int) % GROOVE_BINS, weights=env[sel], minlength=GROOVE_BINS)
    h = h + 0.5 * (np.roll(h, 1) + np.roll(h, -1))
    return h / (h.sum() + 1e-12)


# Rhythm inside a window: where in the BAR the attacks fall, bar by bar. The mean of 1 - cosine between consecutive
# bars' onset histograms. Steady grooves read 0.02 to 0.09 on Common Time's three songs; a riff of ten sixteenths
# sliding against the bar 0.12 to 0.19; Plain Hunt v9's snare following the riff's long note 0.230 (0.087 before).
RHYTHM_BINS = 48            # places in a bar: a sixteenth is three of them in 4/4, a triplet eighth four
RHYTHM_MOVES = 0.15


def rhythm_motion(env, times, clock, ba, bb, bpb=4.0):
    """How far the attacks' places in the bar change from one bar to the next between beats ba and bb: the mean, over
    consecutive bars, of 1 - cosine of their onset histograms (RHYTHM_BINS places, a one-bin smear). 0 = every bar
    alike. Bars with next to no attacks (under a fiftieth of the busiest bar's) are left out, so a rest is not a
    change of rhythm. None when fewer than two bars can be compared."""
    hs, tot = [], []
    half = bpb / (2.0 * RHYTHM_BINS)                # places are centred on the grid, so an attack on a sixteenth is in ONE
    for b0 in np.arange(ba, bb - bpb + 1e-9, bpb):  # place, and a bar owns the attacks from half a place before its line
        grid = np.linspace(b0 - half, b0 + bpb - half, int(round(bpb * 96)) + 1)
        secs = clock(grid)
        sel = (times >= secs[0]) & (times < secs[-1])
        beats = np.interp(times[sel], secs, grid)
        h = np.bincount(np.clip(np.floor((beats - b0) / bpb * RHYTHM_BINS + 0.5).astype(int), 0, RHYTHM_BINS - 1),
                        weights=env[sel], minlength=RHYTHM_BINS)
        tot.append(float(h.sum()))
        hs.append(h + 0.5 * (np.roll(h, 1) + np.roll(h, -1)))
    floor = max(tot, default=0.0) / 50.0
    steps = [1 - _cos(hs[i], hs[i + 1]) for i in range(len(hs) - 1) if tot[i] > floor and tot[i + 1] > floor]
    return float(np.mean(steps)) if steps else None


def is_static(r):
    """Whether a window carries the static flag, in either wording ("static", "static in tone")."""
    return any(f.startswith("static") for f in r.get("flags") or [])


def semitones(x, sr, hop_s=0.1, ref=None, info=None):
    """(frames x 60 semitone energies C2..B6, log-compressed; frame times in s) of the mono mix, at 12 kHz. The scale is
    the render's own loudest semitone frame, or REF (another render's, so an A/B shares one scale); INFO gets 'sref'."""
    from scipy import signal
    m = x.astype(np.float32).mean(1) if x.ndim > 1 else x.astype(np.float32)
    m = signal.resample_poly(m, 1, 4) if sr == 48000 else signal.resample_poly(m, 12000, sr)
    fs, nfft, hop = 12000, 4096, int(hop_s * 12000)
    if len(m) < nfft:
        return np.zeros((0, SEMI_HI - SEMI_LO)), np.zeros(0)
    n = 1 + (len(m) - nfft) // hop
    win = np.hanning(nfft).astype(np.float32)
    idx = np.round(69 + 12 * np.log2(np.maximum(np.fft.rfftfreq(nfft, 1 / fs), 1e-6) / 440.0)).astype(int)
    S = np.zeros((n, SEMI_HI - SEMI_LO), dtype=np.float32)
    for c0 in range(0, n, 512):
        c1 = min(n, c0 + 512)
        fr = np.stack([m[i * hop:i * hop + nfft] * win for i in range(c0, c1)])
        mag = np.abs(np.fft.rfft(fr, axis=1))
        for k in range(SEMI_LO, SEMI_HI):
            sel = idx == k
            if sel.any():
                S[c0:c1, k - SEMI_LO] = mag[:, sel].sum(1)
    ref = float(S.max()) if ref is None else ref
    if info is not None:
        info["sref"] = ref
    S = np.log1p(S / (ref + 1e-12) * 1000.0)
    return S, (np.arange(n) * hop + nfft / 2) / fs


def match_gain(xn, xo, spans, sr):
    """The gain that best maps the OLD render onto the NEW one, taken from the window the edit touched least (the
    highest correlation between old and new), so reworked windows cannot pull it. Renders are loudness-normalised, so
    new energy in one window turns the whole song down a little (chirper-three, t11 v21: ~0.3 dB put every untouched
    window at -25 dB residual). A median of per-window gains failed when most windows changed: an edit that moves a
    line's pitch decorrelates it, which shrinks a window's least-squares gain (chirper-zero, t5 overshoot: -2.05 dB
    instead of -0.001, so an untouched w1 read -13.5 dB). No window above 0.99 correlation: no gain match."""
    best = None
    for ta, tb in spans:
        a, b = int(ta * sr), int(tb * sr)
        n, o = xn[a:b].astype(np.float64), xo[a:b].astype(np.float64)
        k = min(len(n), len(o))
        n, o = n[:k], o[:k]
        nn, oo = float((n ** 2).sum()), float((o ** 2).sum())
        if k and nn > 1e-9 and oo > 1e-9:
            no = float((n * o).sum())
            rho = no / np.sqrt(nn * oo)
            if best is None or rho > best[0]:
                best = (rho, no / oo)
    return best[1] if best and best[0] > 0.99 else 1.0


def seq_of(S, times, clock, ba, bb, ta, tb):
    """A window's note sequence: semitone frames twice a beat (on the tempo map), or every 0.25 s without a tempo."""
    if not len(times):
        return np.zeros((0, SEMI_HI - SEMI_LO))
    ts = clock(np.arange(ba, bb, 0.5)) if clock is not None and ba is not None else np.arange(ta, tb, 0.25)
    i = np.clip(np.searchsorted(times, ts), 0, len(times) - 1)
    return S[i]


def seq_dist(A, B):
    """How far apart two note sequences are: the mean over aligned steps of the largest change in any semitone's
    (log) energy, so one new, moved or octave-leapt note counts even under a loud pad. About 0.002 for an untouched
    window between two renders, 0.36 for t8 v26's octave leaps (the mean cosine read 0.0007 there)."""
    n = min(len(A), len(B))
    if n == 0:
        return 0.0
    return float(np.abs(np.asarray(A[:n], float) - np.asarray(B[:n], float)).max(1).mean())


def seq_sim(A, B):
    """Likeness of two note sequences, 0..1: exp(-seq_dist)."""
    return float(np.exp(-seq_dist(A, B)))


def analyse(wav, song, window_s=30.0, x=None, sref=None, info=None):
    """Map WAV (or the audio X) in windows. SREF puts the note sequence on another render's semitone scale (A/B);
    INFO, a dict, receives this render's scale as 'sref'."""
    x = L.load(wav) if x is None else x
    F = L.Feat(x)
    dur = CS.music_end(x, L.SR)
    X = CS.frames(F)
    wins = windows(song, dur, window_s)
    feats = CS.section_feats(F, x, [(ta, tb) for _, _, ta, tb in wins], X)
    nov = CS.novelty(X)
    S, st = semitones(x, L.SR, ref=sref, info=info)
    clock, _ = beat_clock(song)
    env, etimes = onset_env(x, L.SR) if clock is not None else (None, None)
    bpb = meter_beats(song)
    rows = []
    for i, ((ba, bb, ta, tb), f) in enumerate(zip(wins, feats)):
        prof = np.asarray(f["profile"], float)
        wgt = np.maximum(prof - (prof.max() - 60.0), 0.0)   # dB above a 60 dB floor: the bands you hear, not the bass's power
        bright = float(np.exp((wgt * np.log(BAND_HZ)).sum() / (wgt.sum() + 1e-12)))
        lo, hi = CS.frame_at(ta), max(CS.frame_at(ta) + 1, CS.frame_at(tb))
        motion = float(np.mean(nov[lo:hi])) if hi <= len(nov) and hi > lo else 0.0
        r = {"n": i + 1, "beats": [ba, bb], "time": [round(ta, 2), round(tb, 2)], "level": round(f["level"], 1),
             "bright_hz": round(bright), "density": round(f["density"], 2), "motion": round(motion, 4),
             "vec": f["vec"], "chroma": f["chroma"], "seq": seq_of(S, st, clock, ba, bb, ta, tb)}
        if env is not None and ba is not None:
            r["ghist"] = groove_hist(env, etimes, clock, ba, bb)
            rm = rhythm_motion(env, etimes, clock, ba, bb, bpb)
            r["rhythm"] = None if rm is None else round(rm, 3)
        if i:
            prev = rows[-1]
            r["change"] = round(1 - _sim(prev, r) + abs(r["level"] - prev["level"]) / 20.0, 4)
            if r.get("ghist") is not None and prev.get("ghist") is not None:
                r["groove"] = round(1 - _cos(prev["ghist"], r["ghist"]), 3)
        best = max(((j, _sim(rows[j], r)) for j in range(i)), key=lambda t: t[1], default=None)
        if best:
            j = best[0]
            avg = 0.5 * _cos(rows[j]["vec"], r["vec"]) + 0.5 * _cos(rows[j]["chroma"], r["chroma"])
            r["like"] = {"n": j + 1, "sim": round(best[1], 4), "dlevel": round(r["level"] - rows[j]["level"], 1),
                         "notes": round(seq_dist(rows[j]["seq"], r["seq"]), 3), "avg": round(avg, 4)}
        rows.append(r)
    flag(rows)
    return rows, dur


def rhythm_line(rows):
    """(lowest quarter, median, the "rhythm moves" line) of the windows' rhythm figures: the last is the song's top
    quarter, and at least RHYTHM_MOVES. (None, None, None) when fewer than three windows have one."""
    rhy = [r["rhythm"] for r in rows if r.get("rhythm") is not None]
    if len(rhy) < 3:
        return None, None, None
    return float(np.percentile(rhy, 25)), float(np.median(rhy)), max(float(np.percentile(rhy, 75)), RHYTHM_MOVES)


def flag(rows):
    """Flags relative to the song itself (its own quartiles) plus a few absolute ones."""
    if len(rows) < 3:
        return
    mot = np.array([r["motion"] for r in rows])
    chg = np.array([r.get("change", np.nan) for r in rows])
    m25 = float(np.percentile(mot, 25))
    c25 = float(np.nanpercentile(chg, 25))
    moves = rhythm_line(rows)[2]
    for r in rows:
        f = []
        lk = r.get("like")
        if (lk and lk.get("notes", 9.0) <= REPEAT_NOTES and lk.get("avg", 0.0) >= REPEAT_AVG
                and abs(lk["dlevel"]) <= 1.5):
            f.append(f"near-repeat of w{lk['n']}")
        if r["motion"] <= m25:                                    # static in tone, harmony and level: the rhythm may still move
            f.append("static in tone" if moves is not None and (r.get("rhythm") or 0.0) >= moves else "static")
        if (r.get("change") is not None and r["change"] <= c25
                and r.get("groove", 0.0) < GROOVE_NEW):           # a new groove is new, whatever texture says
            f.append("little new vs w{}".format(r["n"] - 1))
        if r.get("change") is not None and r["n"] > 1 and abs(r["level"] - rows[r["n"] - 2]["level"]) >= 6:
            f.append("level jump")
        r["flags"] = f


ENTER_QUIET = 8.0          # beats a part must have been silent for its next note to be an entry (two bars of four)


def plan_of(song, pin):
    """The song as chirp plans it (canonical), or None when it cannot be asked."""
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    try:
        r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, env=env, cwd=ROOT)
        return json.loads(r.stdout)["data"]["canonical"]
    except (OSError, ValueError, KeyError, TypeError):
        return None


def entries(canon, rows, quiet=ENTER_QUIET):
    """{window n: [(track, beat)]}: the parts that ENTER in each window, with where: a note of a track that had been
    silent for `quiet` beats or more (or had not played yet). From the plan's notes where they SOUND (a warped track,
    a risset track's copies, a track that starts late: tools/notechk.py); one entry a track a window (its first).
    Windows without beats (a song with no tempo) have none."""
    out = {}
    if not canon or not rows or rows[0]["beats"][0] is None:
        return out
    stack = list(canon.get("tracks") or [])
    while stack:
        t = stack.pop(0)
        stack.extend(t.get("tracks") or [])
        notes = t.get("notes") or []
        if t.get("name") and (t.get("warp") or t.get("risset") or t.get("at")):
            import notechk
            try:
                notes = notechk.track_notes(canon, t["name"]) or notes
            except SystemExit:
                pass
        spans = sorted((float(n.get("at") or 0), float(n.get("at") or 0) + float(n.get("len") or 0))
                       for n in notes if isinstance(n, dict))
        end = None
        for a, b in spans:
            if end is None or a - end >= quiet:
                r = next((r for r in rows if r["beats"][0] <= a < r["beats"][1]), None)
                if r and not any(name == t.get("name") for name, _ in out.get(r["n"], [])):
                    out.setdefault(r["n"], []).append((t.get("name"), a))
            end = b if end is None else max(end, b)
    return {n: sorted(v, key=lambda e: e[1]) for n, v in out.items()}


NOTE_PERIODS = (1, 2, 4)    # bars LOOP when they repeat this many bars on, throughout a run
NOTE_GRID = 12              # places are read to a twelfth of a beat (sixteenths and triplets)
NOTE_SAME = 0.8             # two bars are the same notes when this share of them is shared ...
NOTE_SHORT = 0.5            # ... or when one is the other with notes left out, down to this share of it (a figure cut
#                             short at the edge of a part's range is still the figure: a stair's guitar drops two notes
#                             of six where its register ends)
NOTE_MOVES = 0.5            # NEVER SETTLES: at least this share of a part's bars belong to no looping run


def _same(a, b):
    if a == b:
        return True
    lo, hi = sorted((a, b), key=len)
    return bool(lo) and (len(a & b) >= NOTE_SAME * len(a | b) or (lo <= hi and len(lo) >= NOTE_SHORT * len(hi)))


def _loops(sigs):
    """The shortest of NOTE_PERIODS at which a run of bars repeats throughout (two bars or more of evidence), or None."""
    for p in NOTE_PERIODS:
        if len(sigs) >= max(2, 2 * p) and all(_same(a, b) for a, b in zip(sigs, sigs[p:])):
            return p
    return None


def _runs(sigs):
    """Bars as the longest looping runs, left to right: [(start, end, period)], period None for a bar that loops with
    nothing after it."""
    out, i = [], 0
    while i < len(sigs):
        end = next((e for e in range(len(sigs), i + 1, -1) if _loops(sigs[i:e])), None)
        if end is None:
            out.append((i, i + 1, None))
            i += 1
        else:
            out.append((i, end, _loops(sigs[i:end])))
            i = end
    return out


def note_motion(canon, rows, bpb=4.0):
    """{window n: {"loops": [part], "changes": [(part, beat)], "moves": [part], "mixed": [part]}} from the plan's
    notes where they sound, part by part. A part is a pitched track, or ONE PIECE of a kit's track (kit:t1); a note is
    its place in the bar and its pitch class, so a line passed between octaves is the same notes. Over the bars a part
    plays in the window (two or more):
      loops    its bars repeat every 1, 2 or 4 bars throughout (rests between are not a change)
      changes  it loops, then loops on OTHER notes: the beat of each such bar
      moves    at least NOTE_MOVES of its bars belong to no looping run: it never settles
      mixed    a loop with breaks"""
    import pitchbench
    out = {}
    if not canon or not rows or rows[0]["beats"][0] is None:
        return out
    parts, order = {}, []                               # part -> bar -> {(place, class)}
    stack = list(canon.get("tracks") or [])
    while stack:
        t = stack.pop(0)
        stack.extend(t.get("tracks") or [])
        notes = t.get("notes") or []
        if not t.get("name") or not notes:
            continue
        if t.get("warp") or t.get("risset") or t.get("at"):
            import notechk
            try:
                notes = notechk.track_notes(canon, t["name"]) or notes
            except SystemExit:
                pass
        for n in notes:
            if not isinstance(n, dict):
                continue
            at = float(n.get("at") or 0)
            k = int(np.floor(at / bpb + 1e-9))
            place, pitch = int(round((at - k * bpb) * NOTE_GRID)), n.get("pitch")
            try:
                if isinstance(pitch, (int, float)) and not isinstance(pitch, bool):
                    name, classes = t["name"], {int(round(pitch)) % 12}
                else:
                    name, classes = t["name"], {pitchbench.midi(x.strip()) % 12 for x in str(pitch).split(",")}
            except (ValueError, KeyError, IndexError):
                name, classes = f"{t['name']}:{pitch}", {0}          # a kit's piece is a part of its own
            if name not in parts:
                order.append(name)
            parts.setdefault(name, {}).setdefault(k, set()).update((place, c) for c in classes)
    for r in rows:
        k0, k1 = int(np.ceil(r["beats"][0] / bpb - 1e-9)), int(np.floor(r["beats"][1] / bpb + 1e-9))
        for name in order:
            sigs = [frozenset(parts[name].get(k, ())) for k in range(k0, k1)]
            played = [i for i, x in enumerate(sigs) if x]
            if len(played) < 2:
                continue
            first, sigs = played[0], sigs[played[0]:played[-1] + 1]
            runs = _runs(sigs)
            sounding = [(a, b, p) for a, b, p in runs if any(sigs[a:b])]
            got = out.setdefault(r["n"], {"loops": [], "changes": [], "moves": [], "mixed": []})
            new = sum(1 for a, b, p in sounding if p is None)
            cuts = [(k0 + first + b0) * bpb for (_, a1, _), (b0, _, _) in zip(sounding, sounding[1:]) if a1 == b0]
            if new >= NOTE_MOVES * len(played):
                got["moves"].append(name)
            elif new:
                got["mixed"].append(name)
            elif cuts:
                got["changes"].extend((name, b) for b in cuts)
            else:
                got["loops"].append(name)
    return out


def note_lines(rows, motion, clock, bpb=4.0):
    """The lines under the map: for each window flagged static, what its parts' NOTES do there (from the plan)."""
    def names(v):
        return ", ".join(v[:8]) + (f" +{len(v) - 8}" if len(v) > 8 else "")
    lines = []
    for r in rows:
        got = motion.get(r["n"])
        if not is_static(r) or not got:
            continue
        n = len(got["loops"]) + len(got["mixed"])
        said = [f"{n} part{'s' if n != 1 else ''} loop{'s' if n == 1 else ''}"
                + (f" ({len(got['mixed'])} with breaks)" if got["mixed"] else "")]
        if got["changes"]:
            by = {}
            for name, beat in got["changes"]:
                by.setdefault(beat, []).append(name)
            said.append("these CHANGE in it (a loop, then other notes): " + "; ".join(
                f"{names(v)} at {fmt_t(float(clock(b)[0]))} (bar {int(b // bpb) + 1})" for b, v in sorted(by.items())[:4]))
        if got["moves"]:
            said.append(f"these NEVER SETTLE (most of their bars repeat nothing near them): {names(got['moves'])}")
        lines.append(f"  w{r['n']} by the plan's notes (part by part; a note is its place in the bar and its pitch class): "
                     + "; ".join(said) + (". Static in its SOUND, not in its notes: the flag cannot hear which notes; listen before "
                                          "rewriting it" if got["changes"] or got["moves"] else ""))
    return lines


def entry_lines(cid, rows, enters, clock):
    """The lines under the map: for each window flagged static, what enters in it and the presence command."""
    lines = []
    low, mid, moves = rhythm_line(rows)
    for r in rows:
        if not is_static(r):
            continue
        said = "static"
        if moves is not None and r.get("rhythm") is not None:    # which way its rhythm reads: the map's motion cannot hear it
            if r["rhythm"] >= moves:
                said = f"static in tone (its rhythm MOVES: {r['rhythm']:.3f} bar to bar, this song's median {mid:.3f})"
            elif r["rhythm"] <= low:
                said = f"static (and its rhythm repeats: {r['rhythm']:.3f} bar to bar, this song's median {mid:.3f})"
            else:
                said = f"static (rhythm {r['rhythm']:.3f} bar to bar, this song's median {mid:.3f})"
        got = enters.get(r["n"]) or []
        if not got:
            lines.append(f"  w{r['n']} {said}: nothing enters in it (the same parts throughout, or parts that never rested two bars)")
            continue
        by = {}
        for name, beat in got:
            by.setdefault(round(beat, 3), []).append(name)
        what = "; ".join(f"{', '.join(v[:6])}{' +' + str(len(v) - 6) if len(v) > 6 else ''} at {fmt_t(float(clock(b)[0]))}"
                         for b, v in list(by.items())[:4])
        first = got[0][1]
        lines.append(f"  w{r['n']} {said}, and these ENTER in it: {what}. How loud against what was already playing: "
                     f"presence.py {cid} --windows {first:g}b-{first + 16:g}b --preroll 8")
    return lines


def focus_order(rows, ledger, recent=3):
    """Windows to focus on next: flagged ones first (most flags, then the most repeat-like), least recently focused
    first; a window focused in the last RECENT marks waits."""
    last = {}
    for k, e in enumerate(ledger):
        last[e.get("window")] = k
    n = len(ledger)
    cand = []
    for r in rows:
        if r["n"] in last and n - last[r["n"]] <= recent:
            continue
        score = 2.0 * len(r.get("flags") or []) + (r.get("like") or {}).get("sim", 0) - r["motion"] * 10
        cand.append((-(score), last.get(r["n"], -1), r["n"]))
    cand.sort()
    return [c[2] for c in cand]


def ledger_path(cid):
    c = CS.climb_of(cid)
    album = c.get("album") or (c.get("compose") or {}).get("album")
    return os.path.join(ROOT, "compose", album, "sections", f"{cid}.jsonl")


def read_ledger(cid):
    try:
        with open(ledger_path(cid)) as f:
            return [json.loads(x) for x in f if x.strip()]
    except (OSError, ValueError):
        return []


def residual_db(xn, xo, ta, tb, sr):
    """How much of a window is new, in dB: the energy of (new - old) against the new render's, sample-aligned (the
    renders are deterministic). About -60 or lower: untouched; around -20: clearly changed."""
    a, b = int(ta * sr), int(tb * sr)
    n = xn[a:b].astype(np.float64)
    o = xo[a:b].astype(np.float64)
    k = min(len(n), len(o))
    if k == 0:
        return 0.0
    n, o = n[:k], o[:k]
    e = float(((n - o) ** 2).sum())
    return round(max(-99.0, 10 * np.log10(e / (float((n ** 2).sum()) + 1e-20) + 1e-20)), 1)


SPAN_SLICE_S = 1.0          # WHERE IN THE WINDOW: the residual is read a second at a time ...
SPAN_SHARE = 0.9            # ... and the change SITS in the shortest run of seconds that holds this share of it ...
SPAN_MOST = 0.5             # ... when that run is no more than this share of the window


def residual_span(xn, xo, ta, tb, sr):
    """Where in a window its residual sits: (from s, to s, the residual of the REST of the window in dB), or None when
    the change is spread through the window (the shortest run of seconds holding SPAN_SHARE of the residual energy is
    more than SPAN_MOST of the window) or there is none. A window is half a minute: a change in its last five seconds
    reads as the whole window's (chirper-zero, False Summit v11: a fader brought down two bars before a window's end
    read -15.6 dB "at the pole", which itself was untouched at -52)."""
    a, b = int(ta * sr), int(tb * sr)
    n, o = xn[a:b].astype(np.float64), xo[a:b].astype(np.float64)
    k = min(len(n), len(o))
    step = int(SPAN_SLICE_S * sr)
    if k < 2 * step:
        return None
    d = (n[:k] - o[:k]) ** 2
    d = d.sum(axis=1) if d.ndim > 1 else d
    p = (n[:k] ** 2).sum(axis=1) if n.ndim > 1 else n[:k] ** 2
    cuts = list(range(0, k, step))
    if k - cuts[-1] < step // 2 and len(cuts) > 1:           # a last sliver joins the slice before it
        cuts.pop()
    cuts.append(k)
    e = np.array([d[i:j].sum() for i, j in zip(cuts, cuts[1:])])
    total = float(e.sum())
    if total <= 0:
        return None
    best, i, run = None, 0, 0.0
    for j in range(len(e)):                                   # the shortest run of slices holding SPAN_SHARE of it
        run += e[j]
        while run - e[i] >= SPAN_SHARE * total:
            run -= e[i]
            i += 1
        if run >= SPAN_SHARE * total and (best is None or j - i < best[1] - best[0]):
            best = (i, j)
    if best is None or (cuts[best[1] + 1] - cuts[best[0]]) > SPAN_MOST * k:
        return None
    lo, hi = cuts[best[0]], cuts[best[1] + 1]
    rest_e = total - float(e[best[0]:best[1] + 1].sum())
    rest_p = float(p.sum() - p[lo:hi].sum())
    rest = max(-99.0, 10 * np.log10(rest_e / (rest_p + 1e-20) + 1e-20))
    return round(ta + lo / sr, 1), round(ta + hi / sr, 1), round(rest, 1)


def span_lines(cmp_, rows, cut):
    """One line for each CHANGED window whose change sits in part of it."""
    out = []
    for c, r in zip(cmp_, rows):
        sp = c.get("residual_span")
        if sp and c.get("residual_db") is not None and c["residual_db"] > cut:
            t0, t1, rest = sp
            out.append(f"  w{c['n']}'s change sits in {fmt_t(t0)}-{fmt_t(t1)} ({t1 - t0:.0f} s of its {r['time'][1] - r['time'][0]:.0f}): "
                       f"the rest of the window reads {rest:.1f} dB" + (", untouched" if rest <= -45.0 else ""))
    return out


def residual_floor(cmp_, levels=None):
    """(the median window residual, the level above which a window counts as changed): -40 dB, or 10 dB over the
    floor when the whole song moved (chirper-three, t11 v21: the mastering gain into the master compressors moved
    0.37 dB and put every window near -29 dB). With LEVELS (each window's level in dB), a song in which some audible
    window still reads untouched (<= -45 dB) did not move as a whole, however many windows were edited: the line stays
    at -40 (chirper-zero, t5 overshoot: 6 of 8 windows edited put the median at -15, which would have hidden them).
    Silent windows read -99 whatever happened, so they never count as untouched."""
    rs = [c["residual_db"] for c in cmp_ if c.get("residual_db") is not None]
    if not rs:
        return -99.0, -40.0
    floor = float(np.median(rs))
    if levels is not None and anchored(cmp_, levels):
        return round(floor, 1), -40.0
    return round(floor, 1), round(max(-40.0, floor + 10.0), 1)


def anchored(cmp_, levels, quiet_db=-60.0):
    """Whether an audible window (level above QUIET_DB) still reads untouched (residual <= -45 dB)."""
    return any(c.get("residual_db") is not None and c["residual_db"] <= -45.0 and lv is not None and lv > quiet_db
               for c, lv in zip(cmp_, levels))


def compare(new, old, xn=None, xo=None, sr=None):
    """Per window: how the NEW render's window differs from the OLD's (same windows): the residual in dB when both
    renders' audio is given, the note-sequence change, and the feature deltas."""
    out = []
    for a, b in zip(new, old):
        c = {"n": a["n"], "change": round(1 - _sim(a, b) + abs(a["level"] - b["level"]) / 20.0, 4),
             "melody": round(seq_dist(a["seq"], b["seq"]), 3) if a.get("seq") is not None and b.get("seq") is not None
             else None,
             "dlevel": round(a["level"] - b["level"], 1), "dbright_hz": a["bright_hz"] - b["bright_hz"],
             "ddensity": round(a["density"] - b["density"], 2), "dmotion": round(a["motion"] - b["motion"], 4),
             "change_vs_prev": [b.get("change"), a.get("change")]}
        if a.get("ghist") is not None and b.get("ghist") is not None:
            c["groove"] = round(1 - _cos(a["ghist"], b["ghist"]), 3)        # the window's feel, new vs old
        if a.get("rhythm") is not None and b.get("rhythm") is not None:
            c["rhythm"] = [b["rhythm"], a["rhythm"]]                        # bar-to-bar change inside the window, was -> now
        if xn is not None and xo is not None:
            c["residual_db"] = residual_db(xn, xo, a["time"][0], a["time"][1], sr or L.SR)
            span = residual_span(xn, xo, a["time"][0], a["time"][1], sr or L.SR)
            if span:
                c["residual_span"] = list(span)
        out.append(c)
    return out


def fmt_t(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def render(song, pin, out):
    def idle():
        try:
            os.sched_setscheduler(0, os.SCHED_IDLE, os.sched_param(0))
        except (AttributeError, OSError):
            os.nice(15)
    r = subprocess.run([pin, "render", "-f", song, "--seed", "0", "-o", out], cwd=ROOT, capture_output=True, text=True,
                       preexec_fn=idle)
    if r.returncode:
        raise SystemExit(f"sectionmap: render failed: {r.stderr.strip()[-400:]}")


def print_map(cid, song, rows, dur, ledger, canon=None):
    rel = os.path.relpath(song, ROOT)
    w0 = rows[0]
    span = (w0["beats"][1] - w0["beats"][0]) if w0["beats"][0] is not None else None
    print(f"{cid}: {len(rows)} windows" + (f" of {span:g} beats" if span else "") + f", music {fmt_t(dur)}"
          f" — a flashlight, not a score")
    last = {e.get("window"): e for e in ledger}
    print(f"{'w':>3} {'time':>11} {'beats':>11} {'lvl dB':>7} {'bright':>7} {'dens':>5} {'motion':>7} {'change':>7} "
          f"{'groove':>6} {'rhythm':>6}  {'most like':<14} flags / last focus")
    for r in rows:
        b = f"{r['beats'][0]:g}-{r['beats'][1]:.0f}" if r["beats"][0] is not None else "-"
        lk = r.get("like")
        like = f"w{lk['n']} {lk['sim']:.3f}" if lk else "-"
        ch = f"{r['change']:.3f}" if r.get("change") is not None else "-"
        gv = f"{r['groove']:.3f}" if r.get("groove") is not None else "-"
        rv = f"{r['rhythm']:.3f}" if r.get("rhythm") is not None else "-"
        lf = last.get(r["n"])
        tail = ", ".join(r.get("flags") or [])
        if r.get("groove", 0.0) >= GROOVE_NEW:
            tail += ("; " if tail else "") + "(new groove)"
        if lf:
            tail += (" | " if tail else "") + f"focused {lf.get('at', '')[:16]} by {lf.get('who')}"
            if lf.get("reshaped"):
                tail += (f" (about here: marked on {lf.get('version') or 'an older version'} as w{lf.get('marked_as', r['n'])}, "
                         "and the song's tempo or length has changed since)")
            elif lf.get("marked_as"):
                tail += f" (marked as w{lf['marked_as']} on another window length)"
        print(f"{r['n']:>3} {fmt_t(r['time'][0]):>5}-{fmt_t(r['time'][1]):<5} {b:>11} {r['level']:>7.1f} "
              f"{r['bright_hz']:>7} {r['density']:>5.2f} {r['motion']:>7.4f} {ch:>7} {gv:>6} {rv:>6}  {like:<14} {tail}")
    if len(rows) >= 3:                                   # what the two commonest flags key on, with this song's own lines
        m25 = float(np.percentile([r["motion"] for r in rows], 25))
        c25 = float(np.nanpercentile([r.get("change", np.nan) for r in rows], 25))
        print(f"  static = motion at or under {m25:.4f}, this song's lowest quarter: how much the texture (spectral shape, harmony, "
              "level, half a second at a time) changes WITHIN the window. A part that joins and stays is one change, then none.")
        print(f"  little new = change at or under {c25:.3f}, its lowest quarter: 1 - likeness to the window before, + the level "
              "step / 20. A quarter of the windows carry each flag, however good the song.")
        moves = rhythm_line(rows)[2]
        if moves is not None:
            print(f"  rhythm = how far the attacks' places in the bar change from one bar to the next WITHIN the window (0 = every "
                  "bar alike). Motion hears tone, harmony and level; a part moved in time, the same strokes on the same drum, shows "
                  f"only here. static in tone = static, with rhythm at or over {moves:.3f} (this song's top quarter, and at least "
                  f"{RHYTHM_MOVES}).")
    if canon:                                            # a static window with an arrival in it: the arrival may be masked
        clock, _ = beat_clock(song)
        for ln in entry_lines(cid, rows, entries(canon, rows), clock) if clock else []:
            print(ln)
        for ln in note_lines(rows, note_motion(canon, rows, meter_beats(song)), clock, meter_beats(song)) if clock else []:
            print(ln)
    order = focus_order(rows, ledger)[:3]
    if order:
        print("focus next (flagged and least recently focused first):")
        for n in order:
            r = rows[n - 1]
            why = ", ".join(r.get("flags") or []) or "no flags: polish"
            print(f"  w{n} {fmt_t(r['time'][0])}-{fmt_t(r['time'][1])}: {why}")
            if r["beats"][0] is not None:
                a, b = r["beats"]
                ctx_a = max(0.0, a - (b - a) / 2)
                print(f"     chirp render -f {rel} --from {a:g}b --to {b:g}b --preroll 4 -o /tmp/{cid}-w{n}.wav"
                      f"   (in context: --from {ctx_a:g}b --to {b + (b - a) / 2:g}b)")
        print("  (--preroll 4, engine 5cffa033+: starts 4 s before the window instead of from the top, 1.5-10x faster, "
              "-100 dB or better on t6 and wM's cases; for listening and trying ideas. Keep exact renders for scoring "
              "and --against.)")
    print(f"after the round: chirpers.py sections {cid} --mark N --note '…'  (and --against OLD.wav to check it stayed local)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id")
    ap.add_argument("--wav", help="the render to map (default: render the song with the groove pin, seed 0)")
    ap.add_argument("--against", help="an earlier render of the same song: per-window deltas")
    ap.add_argument("--window", type=float, default=30.0, help="window length in seconds (whole bars; default 30)")
    ap.add_argument("--mark", type=int, help="record a section round on window N in the ledger")
    ap.add_argument("--note", help="with --mark: what the round did")
    ap.add_argument("--pin", help="chirp binary (default: tools/groove-pin)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--as", dest="as_", metavar="NAME", help="who you are, as climb.py's --as (default: CLIMB_AS or the "
                                                                "session, else the song's owner)")
    ap.add_argument("--no-git", action="store_true", help="with --mark: write the ledger without committing")
    a = ap.parse_args(argv)
    song, climb = song_path(a.id)
    if a.mark is not None:
        return mark(a, song, climb, list(sys.argv[1:] if argv is None else argv))
    tmp = None
    wav = a.wav
    if not wav:
        tmp = tempfile.mkdtemp(prefix="chirp-sections-")
        wav = os.path.join(tmp, f"{a.id}.wav")
        render(song, a.pin or open(os.path.join(HERE, "groove-pin")).read().strip(), wav)
    try:
        xn = L.load(wav) if a.against else None
        info = {}
        rows, dur = analyse(wav, song, a.window, x=xn, info=info)
        ledger = placed_ledger(read_ledger(a.id), rows, song)
        if a.against:
            xo = L.load(a.against)
            g = match_gain(xn, xo, [r["time"] for r in rows], L.SR)
            xo = xo * g
            # the old render, gain-matched and on the new render's semitone scale, on the NEW render's windows (same
            # song file, so the same beats)
            old, _ = analyse(a.against, song, a.window, x=xo, sref=info.get("sref"))
            old = old[:len(rows)]
            cmp_ = compare(rows, old, xn, xo, L.SR)
            gain_db = round(20 * np.log10(max(g, 1e-9)), 2)
            levels = [r["level"] for r in rows]
            floor, cut = residual_floor(cmp_, levels)
            if a.json:
                print(json.dumps({"id": a.id, "gain_db": gain_db, "floor_db": floor, "changed_above_db": cut,
                                  "compare": cmp_}))
                return
            print(f"{a.id}: {os.path.basename(wav)} against {os.path.basename(a.against)} (per window, the old render "
                  f"matched by {gain_db:+.2f} dB first; residual: the energy "
                  f"of new - old against new, about -60 untouched, -20 clearly changed; melody: note-sequence change)")
            if floor > -45 and anchored(cmp_, levels):
                k = sum(1 for c in cmp_ if c["residual_db"] > cut)
                print(f"  most windows changed ({k} of {len(cmp_)} above {cut:.1f} dB), but an audible window still reads "
                      f"untouched, so these are edits, not a whole-song shift (the gain is anchored on the least-touched "
                      f"window). Pitch edits (overshoot, scoop, fall) decorrelate the waveform and overstate residuals: "
                      f"read the melody column and listen.")
            elif floor > -45:
                print(f"  every window moved (median residual {floor:.1f} dB): a whole-song shift, most often the mastering "
                      f"gain into the master's compressors moving because the edit changed the song's loudness, not edits "
                      f"there. '<' marks windows above {cut:.1f} dB, well clear of that floor.")
            print(f"{'w':>3} {'time':>11} {'resid dB':>8} {'melody':>7} {'groove':>6} {'change':>7} {'dB':>6} {'bright':>7} "
                  f"{'dens':>6}  change vs prev (was -> now)   rhythm in the window (was -> now)")
            for c, r in zip(cmp_, rows):
                mark_ = " <" if c["residual_db"] > cut else ""
                cv = c["change_vs_prev"]
                cvs = f"{cv[0]:.3f} -> {cv[1]:.3f}" if cv[0] is not None and cv[1] is not None else "-"
                mel = f"{c['melody']:.3f}" if c["melody"] is not None else "-"
                gv = f"{c['groove']:.3f}" if c.get("groove") is not None else "-"
                rh = c.get("rhythm")
                rhs = f"{rh[0]:.3f} -> {rh[1]:.3f}" + ("  moved" if abs(rh[1] - rh[0]) >= 0.05 else "") if rh else "-"
                print(f"{c['n']:>3} {fmt_t(r['time'][0]):>5}-{fmt_t(r['time'][1]):<5} {c['residual_db']:>8.1f} {mel:>7} {gv:>6} "
                      f"{c['change']:>7.4f} {c['dlevel']:>6.1f} {c['dbright_hz']:>7} {c['ddensity']:>6.2f}  {cvs:<27s}   {rhs}{mark_}")
            for ln in span_lines(cmp_, rows, cut):
                print(ln)
            return
        if a.json:
            print(json.dumps({"id": a.id, "dur": dur, "windows": [{k: v for k, v in r.items()
                                                                   if k not in ("vec", "chroma", "seq", "ghist")} for r in rows],
                              "focus": focus_order(rows, ledger)}))
            return
        print_map(a.id, song, rows, dur, ledger, plan_of(song, a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()))
    finally:
        if tmp:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)


def mark(a, song, climb, argv):
    import chirpers as CH
    C = CH.C
    if not a.note:
        raise SystemExit("sectionmap: --mark N needs --note '…' (what the round did to that window)")
    path = ledger_path(a.id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    who = a.as_ or C.whoami(argv)
    fallback = f"{os.environ.get('USER', '?')}@{os.uname().nodename}"
    if who == fallback and climb.get("owner"):
        who = str(climb["owner"]).split()[0]           # no identity set: the song's owner (section rounds are theirs)
    e = {"id": a.id, "window": a.mark, "at": C.now_iso(), "who": who,
         "version": (climb.get("best") or {}).get("version"), "note": a.note}
    e.update(shape(song, a.mark, a.window))            # its beats, the tempo and the length: found again after a reshape
    with open(path, "a") as f:
        f.write(json.dumps(e) + "\n")
    print(f"{a.id}: section round on w{a.mark} recorded ({e['who']})")
    if not a.no_git:
        rel = os.path.relpath(path, ROOT)
        subprocess.run(["git", "-C", ROOT, "add", rel], check=False)
        C.commit_or_die([rel], f"compose: {e['who']} section round on {a.id} w{a.mark}: {a.note[:80]}",
                        argv + (["--as", who] if "--as" not in argv else []))


if __name__ == "__main__":
    main()
