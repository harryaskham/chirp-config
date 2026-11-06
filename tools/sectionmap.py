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
    bpb = meter_beats(song)
    w = round(window_s * float(bpm or 120) / 60.0 / bpb) * bpb
    phrase = 4 * bpb                                    # whole 4-bar phrases when the window holds at least one
    w = max(2 * bpb, round(w / phrase) * phrase if w >= phrase else w)
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
    rows = []
    for i, ((ba, bb, ta, tb), f) in enumerate(zip(wins, feats)):
        prof = np.asarray(f["profile"], float)
        wgt = np.maximum(prof - (prof.max() - 60.0), 0.0)   # dB above a 60 dB floor: the bands you hear, not the bass's power
        bright = float(np.exp((wgt * np.log(BAND_HZ)).sum() / (wgt.sum() + 1e-12)))
        lo, hi = int(ta * 2), max(int(ta * 2) + 1, int(tb * 2))
        motion = float(np.mean(nov[lo:hi])) if hi <= len(nov) and hi > lo else 0.0
        r = {"n": i + 1, "beats": [ba, bb], "time": [round(ta, 2), round(tb, 2)], "level": round(f["level"], 1),
             "bright_hz": round(bright), "density": round(f["density"], 2), "motion": round(motion, 4),
             "vec": f["vec"], "chroma": f["chroma"], "seq": seq_of(S, st, clock, ba, bb, ta, tb)}
        if env is not None and ba is not None:
            r["ghist"] = groove_hist(env, etimes, clock, ba, bb)
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


def flag(rows):
    """Flags relative to the song itself (its own quartiles) plus a few absolute ones."""
    if len(rows) < 3:
        return
    mot = np.array([r["motion"] for r in rows])
    chg = np.array([r.get("change", np.nan) for r in rows])
    m25 = float(np.percentile(mot, 25))
    c25 = float(np.nanpercentile(chg, 25))
    for r in rows:
        f = []
        lk = r.get("like")
        if (lk and lk.get("notes", 9.0) <= REPEAT_NOTES and lk.get("avg", 0.0) >= REPEAT_AVG
                and abs(lk["dlevel"]) <= 1.5):
            f.append(f"near-repeat of w{lk['n']}")
        if r["motion"] <= m25:
            f.append("static")
        if (r.get("change") is not None and r["change"] <= c25
                and r.get("groove", 0.0) < GROOVE_NEW):           # a new groove is new, whatever texture says
            f.append("little new vs w{}".format(r["n"] - 1))
        if r.get("change") is not None and r["n"] > 1 and abs(r["level"] - rows[r["n"] - 2]["level"]) >= 6:
            f.append("level jump")
        r["flags"] = f


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
        if xn is not None and xo is not None:
            c["residual_db"] = residual_db(xn, xo, a["time"][0], a["time"][1], sr or L.SR)
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


def print_map(cid, song, rows, dur, ledger):
    rel = os.path.relpath(song, ROOT)
    w0 = rows[0]
    span = (w0["beats"][1] - w0["beats"][0]) if w0["beats"][0] is not None else None
    print(f"{cid}: {len(rows)} windows" + (f" of {span:g} beats" if span else "") + f", music {fmt_t(dur)}"
          f" — a flashlight, not a score")
    last = {e.get("window"): e for e in ledger}
    print(f"{'w':>3} {'time':>11} {'beats':>11} {'lvl dB':>7} {'bright':>7} {'dens':>5} {'motion':>7} {'change':>7} "
          f"{'groove':>6}  {'most like':<14} flags / last focus")
    for r in rows:
        b = f"{r['beats'][0]:g}-{r['beats'][1]:.0f}" if r["beats"][0] is not None else "-"
        lk = r.get("like")
        like = f"w{lk['n']} {lk['sim']:.3f}" if lk else "-"
        ch = f"{r['change']:.3f}" if r.get("change") is not None else "-"
        gv = f"{r['groove']:.3f}" if r.get("groove") is not None else "-"
        lf = last.get(r["n"])
        tail = ", ".join(r.get("flags") or [])
        if r.get("groove", 0.0) >= GROOVE_NEW:
            tail += ("; " if tail else "") + "(new groove)"
        if lf:
            tail += (" | " if tail else "") + f"focused {lf.get('at', '')[:16]} by {lf.get('who')}"
        print(f"{r['n']:>3} {fmt_t(r['time'][0]):>5}-{fmt_t(r['time'][1]):<5} {b:>11} {r['level']:>7.1f} "
              f"{r['bright_hz']:>7} {r['density']:>5.2f} {r['motion']:>7.4f} {ch:>7} {gv:>6}  {like:<14} {tail}")
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
        ledger = read_ledger(a.id)
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
                  f"{'dens':>6}  change vs prev (was -> now)")
            for c, r in zip(cmp_, rows):
                mark_ = " <" if c["residual_db"] > cut else ""
                cv = c["change_vs_prev"]
                cvs = f"{cv[0]:.3f} -> {cv[1]:.3f}" if cv[0] is not None and cv[1] is not None else "-"
                mel = f"{c['melody']:.3f}" if c["melody"] is not None else "-"
                gv = f"{c['groove']:.3f}" if c.get("groove") is not None else "-"
                print(f"{c['n']:>3} {fmt_t(r['time'][0]):>5}-{fmt_t(r['time'][1]):<5} {c['residual_db']:>8.1f} {mel:>7} {gv:>6} "
                      f"{c['change']:>7.4f} {c['dlevel']:>6.1f} {c['dbright_hz']:>7} {c['ddensity']:>6.2f}  {cvs}{mark_}")
            return
        if a.json:
            print(json.dumps({"id": a.id, "dur": dur, "windows": [{k: v for k, v in r.items()
                                                                   if k not in ("vec", "chroma", "seq", "ghist")} for r in rows],
                              "focus": focus_order(rows, ledger)}))
            return
        print_map(a.id, song, rows, dur, ledger)
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
