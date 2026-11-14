#!/usr/bin/env python3
"""stembal: where a mix's energy sits, band by band, beside reference records, and which instrument group to move.

Two measures, both in nine bands (20-60-120-250-500-1k-2k-4k-8k-16k Hz), both in dB relative to the whole mix:
  * THE WHOLE MIX: each band's share of the mix's energy. For a reference this is the sum of its separated stems over
    a window (default 0:30-2:30), so it does not lean on the separator. Eleven Meshuggah records agree with each other
    within about 1 dB per band (p25-p75), which makes their median a firm target.
  * EACH GROUP (drums, guitar, bass, vocals): its bands relative to the whole mix. For a reference these are the
    separator's stems (ref/stems/MODEL/SONG/STEM.wav), so they lean on it: use them to see WHICH instrument to move,
    and the whole-mix row to see how far.

  stembal.py refs --refs ID,ID,... [--from 30 --dur 120] [--model bs_roformer_sw]
        the references' medians, quartiles and each record (cached in ref/stembal/)
  stembal.py song SONG.yaml --refs ID,ID,... --windows 41-56:riffA 247-276:all [--groups drums=kick,snare bass=bass ...]
                  [--mix-only] [--seed 0] [--threads 2] [--out DIR]
        renders each window of SONG raw (loudness off) with the groove's pin (tools/groove-pin), once whole and once
        per group (--solo), and prints ours beside the references: per window, then the mean of the windows against
        the references' median, ours minus theirs, and the width of their middle half.
        --windows takes what `chirp render --from/--to` takes: bars (1-indexed) or seconds (30s-90s).
        --groups left out: drums, bass and guitar are guessed from track and patch names, and printed.
        --mix-only: only the whole-mix rows (for iterating on an equaliser).
        The song is rendered ONCE per group, to the end of the last window, and the windows are cut from that: a
        window render starts from the top anyway, so sixteen windows cost sixteen part-renders a group before (nine
        took 28 minutes on Common Time). The cut is the same samples a window render gives (checked bit for bit), so
        the numbers are the same. A song whose tempo changes, whose meter is not 4/4 or that embeds other songs is
        rendered window by window as before; --per-window forces that.

  --spread (on refs or song): the yardstick for "how far is too far". Each reference's own band shares are taken in
        consecutive --win second windows (default 20) of its loud passages (within --within dB, default 3, of its loud
        level), and the spread across them printed: per record and the median with `refs`, one row under OURS - REFS
        with `song`. Eleven Meshuggah records move 0.6-1.0 dB (std) between their own loud passages in most bands, but
        2.2 dB at 500 Hz-1 kHz (the voice coming and going) and 1.3 at 8-16 kHz: so "within 1 dB of the median" is too
        strict there and too loose at 2-8 kHz. Read a section's difference against this row, not against a flat 1 dB.
        (chirper-zero's refspread.py, Common Time v16.) It reads the record itself (ref/ID.wav), else the sum of its stems.

  --voice (on refs or song): the records' loud passages sorted by whether the VOICE is there (tools/vocsplit.py; the
        vocals stem only sorts the frames, the spectra are the mixes' own). With `refs` it prints vocsplit's table.
        With `song` it adds a block under OURS - REFS: what the records' passages without a voice, and with one, hold
        beside all their loud passages, and then EVERY window read both ways (ours minus the references' median
        shifted by that row). Eleven Meshuggah records hold 2.3 dB less at 500 Hz-1 kHz and 1.4 dB less at 8-16 kHz
        where nobody sings, so an instrumental section read against the one median looks 2 dB short of mids and
        level in the air when it is on target and too bright. Read an instrumental window's "no voice" row and a
        sung one's (or one with a tune on the lead) "voice" row. (chirper-zero's vocsplit.py, Common Time v30.)
  --voice-tracks T,T,... (with `song --voice`): the tracks that are the voice. They are rendered alone once more, and
        a third row is printed for each window, "label, blend 40%": ours against the median shifted by that share
        of the voice's row and the rest of the other. For a section a voice fills only part of, where neither row
        is right (chirper-zero's thought, v33: the bark sings part of the hardest stretch).
        The share is the voice's POWER against the mix in the window's 4 s frames, beside what the records' voices
        have in their frames with a voice (their median gap under the mix, about 8 dB on eleven Meshuggah
        records): a frame where ours is that loud counts whole, 3 dB less half, 6 dB less a quarter. So a voice as
        loud as theirs that sings a quarter of the time reads 25%, and one that sings throughout 100%.

  --parts NAME=T,T ... (with `song`): WHOSE BAND IS IT. Each part is rendered alone once more (as a group is), and
        under each window's row a table is printed: every part's nine bands in dB under the mix's OWN band (0 = the
        part is the whole band), the parts together, and for each band the part that holds most of it with its share
        of the mix's band. So a band that reads over the records comes with its owner: on Odd Sympathy v12, in step,
        2-4 kHz was the guitars' (-1.1 dB: 78% of it) and 8-16 kHz the cymbals' (-0.7: 85%), which ended a question
        carried for ten versions. Works with --mix-only (then only the mix and the parts are rendered).
        A part more than 30 dB under a band is shown as "-". A part alone still goes through its own bus and the
        master, so a clipped or compressed bus treats it differently alone than in the band, and parts that share a
        band add in power only when they are unrelated: read "the parts together" for how far the parts add up to
        the mix (near 0: they do; well under: a part is missing from the list; over: the bus holds them down
        together, or they cancel). The shares are of the MIX's band, so they need not add to 100%.
        (chirper-zero's six solo renders and a table, Odd Sympathy v13.)
        --parts guitars=gl,gr bass=bass kick=kick snare=snare cymbals=cym,hat,ride

  --refs all = every record that has stems. What Common Time used (chirpers10, v7):
  --refs bleed,combustion,dancers-to-a-discordant-system,electric-red,lethargica,obzen,pineal-gland-optics,pravus,
         the-abysmal-eye,the-faultless,this-spiteful-snake      (one argument, no spaces)
  --groups drums=kick,snare,cym,toms,hat,ride guitar=gl,gr,gl2,gr2,wl,wr,lead bass=bass
  --windows 41-56:riffA 247-276:all-three 282-309:hardest

EVERY ROW IS READ FROM THE MONO SUM (left + right) of the file, ours and the records' alike. A part that is wide and
decorrelated (a room, a hard-panned pair playing different things) counts up to 3 dB less than the same part in the
centre, so a part moved out of a room into the centre rises in its bands here while the stereo power spectrum
(tools/gspec.py sums the two channels' power) moves less or not at all. chirper-zero, Common Time v41, measured on
riff A: a snare taken out of the cymbals' room raised 8-16 kHz by 0.27 dB in the two channels' power and by 0.54 dB
in the mono sum (this table read +0.6). Half of the rise was real; half was the wide room counting short in mono.
Both readings are right; they answer different questions: read both before moving a band by less than a dB.

EVERY SAMPLE IS COUNTED ALIKE (since 14 Nov). Before, the spectrum was read in frames of 8192 samples (186 ms) that did
not overlap, each faded in and out, so a drum hit at a frame's edge hardly counted and one at its middle counted 2.7
times over. On a record, or a song whose beat does not sit on that grid, it evens out (the eleven records' median
moved by under 0.1 dB in every band; Common Time at 126 bpm by 0.5 dB at worst in its eight windows, under 0.3 in
seven of them). But at 108 bpm a beat is 2.99 frames: in Odd Sympathy every hit on the beat stayed at one place in
the frame through a whole short window. Its six windows had read up to 2.6 dB wrong at 8-16 kHz and 1.7 at 4-8 kHz
(the hold an eighth apart read that much too DULL, the hold three sixteenths apart 1.4 dB too bright and 1.3 dB
short under 60 Hz; the longest window, 23 bars, was within 0.2), and its snare alone read 12 dB under what it is.
Figures read before that date on a short window of a song near 65, 81, 108, 129, 161 or 215 bpm (a beat that is a
whole number of frames, or half of one) are worth reading again; whole songs and long windows were never far out.
(Found when --parts did not reproduce chirper-zero's own by-part table.)

Read it as: a band where the whole mix is more than about 1 dB from the references' median is worth a look; the group
rows say which instrument carries it. A compressed bass or a clipped drums bus changes level with what is played, so
re-run after every change (compose/chirpers10/sounds.md, "the mix against eleven records", has a worked case).
(chirper-zero, 12 Nov, for Common Time; promoted to tools/ by chirp-eco the same day. Tests: tools/tests/test_stembal.py.)"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vocsplit  # noqa: E402
from wincut import cut, position, window_seconds  # noqa: E402,F401  (position: for the tests and callers)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
while not os.path.isdir(os.path.join(ROOT, "ref")) and ROOT != "/":
    ROOT = os.path.dirname(ROOT)
EDGES = [20, 60, 120, 250, 500, 1000, 2000, 4000, 8000, 16000]
NAMES = ["<60", "-120", "-250", "-500", "-1k", "-2k", "-4k", "-8k", "-16k"]
STEMS = ("drums", "guitar", "bass", "vocals", "other", "piano")
GUESS = {"drums": r"kit|drum|hat|snare|kick|tom|cymbal|ride|crash|china|splash", "bass": r"bass",
         "guitar": r"gtr|guitar|chug|wall|rig|lead|m8"}


def load(path, ss=None, t=None):
    cmd = ["ffmpeg", "-loglevel", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-t", str(t)] if t else []) \
        + ["-i", path, "-ac", "1", "-ar", "44100", "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32).astype(np.float64)


def bands(x):
    """The power of x (44.1 kHz mono) in the nine bands, EVERY SAMPLE COUNTED ALIKE: Hann frames a quarter of a frame
    apart (their squares add to a constant; only the first and last 0.14 s of x fade). Until 14 Nov the frames did
    not overlap, so a hit at a frame's edge hardly counted and one at its middle counted 2.7 times: nothing on a
    record, but at 108 bpm a beat is 2.99 frames, so every hit ON the beat stayed at one place in the frame for a
    whole short window (see the notes at the top)."""
    n, hop = 8192, 2048
    if len(x) < n:
        return np.zeros(len(EDGES) - 1)
    sp = np.zeros(n // 2 + 1)
    w = np.hanning(n)
    k = 0
    for i in range(0, len(x) - n + 1, hop):
        sp += np.abs(np.fft.rfft(x[i:i + n] * w)) ** 2
        k += 1
    fr = np.fft.rfftfreq(n, 1 / 44100)
    return np.array([sp[(fr >= lo) & (fr < hi)].sum() for lo, hi in zip(EDGES[:-1], EDGES[1:])]) / k


def db(v):
    return 10 * np.log10(np.maximum(v, 1e-20))


def stem_dir(model):
    return os.path.join(ROOT, "ref", "stems", model)


def stem_file(model, song, part):
    """The stem's file in whatever format it is stored (WAV first; the htdemucs_6s stems are packed to Opus), or None."""
    for ext in (".wav", ".flac", ".opus", ".ogg", ".m4a", ".mp3"):
        p = os.path.join(stem_dir(model), song, part + ext)
        if os.path.isfile(p):
            return p
    return None


def ref_ids(a):
    have = sorted(d for d in os.listdir(stem_dir(a.model)) if stem_file(a.model, d, "drums"))
    if not a.refs:
        sys.exit("stembal: --refs ID,ID,... (or --refs all). Records with stems: " + ", ".join(have))
    ids = have if a.refs == "all" else a.refs.split(",")
    missing = [i for i in ids if i not in have]
    if missing:
        sys.exit(f"stembal: no stems for {', '.join(missing)} under {stem_dir(a.model)}")
    return ids


def refs(a):
    """{record: {stem: nine bands + whole, dB re the sum of stems}, "mix": nine bands} for every reference, cached."""
    ids = ref_ids(a)
    key = hashlib.sha1(json.dumps(["alike", ids, a.model, a.start, a.dur]).encode()).hexdigest()[:12]
    cache = os.path.join(ROOT, "ref", "stembal", key + ".json")
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    out = {}
    for s in ids:
        st = {n: bands(load(stem_file(a.model, s, n), a.start, a.dur)) for n in STEMS if stem_file(a.model, s, n)}
        tot = sum(v.sum() for v in st.values())
        out[s] = {n: db(v / tot).tolist() + [float(db(v.sum() / tot))] for n, v in st.items()}
        out[s]["mix"] = db(sum(st.values()) / tot).tolist()
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, "w") as f:
        json.dump(out, f)
    return out


def show(title, rows, whole=True):
    print(title)
    print(f"{'':22s}" + "".join(f"{n:>7s}" for n in NAMES) + ("   whole" if whole else ""))
    for name, v in rows:
        print(f"{name[:21]:22s}" + "".join(f"{x:7.1f}" for x in v[:9]) + (f"  {v[9]:6.1f}" if whole and len(v) > 9 else ""))


def stats(R, g):
    A = np.array([R[s][g] for s in R if g in R[s]])
    return np.median(A, 0), np.percentile(A, 25, 0), np.percentile(A, 75, 0)


def record_audio(model, song):
    """The record itself (ref/ID.wav, or another format), else the sum of its stems."""
    for ext in (".wav", ".flac", ".opus", ".ogg", ".m4a", ".mp3"):
        p = os.path.join(ROOT, "ref", song + ext)
        if os.path.isfile(p):
            return load(p)
    xs = [load(stem_file(model, song, n)) for n in STEMS if stem_file(model, song, n)]
    n = min(len(x) for x in xs)
    return sum(x[:n] for x in xs)


def spread(a):
    """{record: {"n": loud windows, "sd": nine bands, "range": nine bands (10th-90th percentile)}}, cached: how far each
    reference's band shares move between its own loud passages."""
    ids = ref_ids(a)
    key = hashlib.sha1(json.dumps(["spread", "alike", ids, a.model, a.win, a.within]).encode()).hexdigest()[:12]
    cache = os.path.join(ROOT, "ref", "stembal", f"spread-{key}.json")
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    out = {}
    win = int(a.win * 44100)
    for s in ids:
        x = record_audio(a.model, s)
        shares, level = [], []
        for i in range(0, len(x) - win + 1, win):
            b = bands(x[i:i + win])
            shares.append(db(b / max(b.sum(), 1e-30)))
            level.append(float(db((x[i:i + win] ** 2).mean())))
        shares, level = np.array(shares), np.array(level)
        keep = level > np.percentile(level, 90) - a.within if len(level) else np.array([], dtype=bool)
        if keep.sum() < 2:
            continue                                  # one loud window says nothing about a spread
        loud = shares[keep]
        out[s] = {"n": int(keep.sum()), "sd": loud.std(0).tolist(),
                  "range": (np.percentile(loud, 90, axis=0) - np.percentile(loud, 10, axis=0)).tolist()}
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, "w") as f:
        json.dump(out, f)
    return out


def spread_medians(S):
    return np.median([S[s]["sd"] for s in S], 0), np.median([S[s]["range"] for s in S], 0)


def voice(a):
    """What the records' loud passages without a voice, and with one, hold beside all of them: ({"without": nine bands,
    "with": nine bands}, records), or None when too few records have both kinds."""
    vocsplit.ROOT = ROOT
    V = vocsplit.cached(ref_ids(a), model=a.model)
    if not all(c in V for c in vocsplit.CLASSES):
        return None
    return {c: np.array(V[c]) - np.array(V["all"]) for c in ("without", "with")}, V["n"], V.get("gap")


def frame_levels(x, seconds=4.0):
    """The level in dB of each whole frame of x (44.1 kHz mono); one frame when x is shorter than a frame."""
    n = int(seconds * 44100)
    frames = [x[i:i + n] for i in range(0, len(x) - n + 1, n)] or [x]
    return np.array([float(db((f ** 2).mean() if len(f) else 0.0)) for f in frames])


def voice_share(mix, vox, gap):
    """How much of a window the voice fills, 0..1: the mean over its 4 s frames of the voice's power against the mix,
    as a fraction of what the records' voices have in their frames with a voice (`gap` dB under the mix), at most 1."""
    n = min(len(mix), len(vox))
    d = mix[:n] - vox[:n]
    return float(np.clip(10 ** ((gap - d) / 10), 0.0, 1.0).mean()) if n else 0.0


def cmd_refs(a):
    R = refs(a)
    med, lo, hi = stats(R, "mix")
    show(f"references, the whole mix (sum of stems, {a.start:g}-{a.start + a.dur:g} s; dB re its total): "
         "median, quartiles, each record",
         [("median", med), ("p25", lo), ("p75", hi)] + [(s, R[s]["mix"]) for s in R], whole=False)
    for g in ("drums", "guitar", "bass", "vocals"):
        if any(g in R[s] for s in R):
            med, lo, hi = stats(R, g)
            show(f"references, {g} stem (dB re the sum of stems)",
                 [("median", med), ("p25", lo), ("p75", hi)] + [(s, R[s][g]) for s in R if g in R[s]])
    if a.spread:
        S = spread(a)
        if not S:
            sys.exit("stembal: no reference has two loud windows of that length; try a shorter --win")
        sd, rng = spread_medians(S)
        show(f"references, each band's spread between a record's own loud passages ({a.win:g} s windows within "
             f"{a.within:g} dB of its loud level; std in dB; n = windows)",
             [("MEDIAN spread (std)", sd), ("MEDIAN 10-90% range", rng)] + [(f"{s[:16]} n={S[s]['n']}", S[s]["sd"]) for s in S],
             whole=False)
    if a.voice:
        vocsplit.ROOT = ROOT
        print("references, their loud passages with the voice and without it (4 s frames; tools/vocsplit.py)")
        vocsplit.report(ref_ids(a), model=a.model)


def whose(mix, parts, floor=30.0):
    """The lines of the "whose band is it" table. mix: the mix's nine band powers; parts: [(name, its nine band
    powers alone)]. Each part in dB under the mix's own band, the parts together, the part holding most of each
    band and that part's share of the mix's band. A band the mix has next to nothing in (60 dB under its total)
    is left out of every row."""
    live = mix > mix.sum() * 1e-6
    safe = np.where(live, mix, 1.0)

    def cells(v):
        d = db(v / safe)
        return "".join(f"{round(x, 1) + 0.0:7.1f}" if ok and x > -floor else f"{'-':>7s}" for x, ok in zip(d, live))
    out = [f"{'':22s}" + "".join(f"{n:>7s}" for n in NAMES)]
    out += [f"{name[:21]:22s}" + cells(v) for name, v in parts]
    out.append(f"{'the parts together':22s}" + cells(np.sum([v for _, v in parts], axis=0)))
    top = [max(parts, key=lambda p: p[1][b]) for b in range(len(NAMES))]
    out.append(f"{'most of it is':22s}" + "".join(f"{t[0][:6]:>7s}" if ok else f"{'-':>7s}" for t, ok in zip(top, live)))
    out.append(f"{'  its share':22s}" + "".join(f"{100 * t[1][b] / safe[b]:6.0f}%" if live[b] else f"{'-':>7s}"
                                               for b, t in enumerate(top)))
    return out


def canonical(pin, song, env):
    """The song as `chirp plan` resolves it, or {} when it cannot be read."""
    r = subprocess.run([pin, "--json", "plan", "-f", song, "--set", "seed=0"], capture_output=True, text=True, env=env)
    try:
        return json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        return {}


def guess_groups(pin, song, env):
    try:
        tracks = canonical(pin, song, env)["tracks"]
    except KeyError:
        sys.exit("stembal: could not read the song's tracks to guess groups; give --groups name=track,track ...")
    out = {}
    for t in tracks:
        hay = f"{t.get('name', '')} {t.get('patch', '') if isinstance(t.get('patch'), str) else ''}".lower()
        for g in ("drums", "bass", "guitar"):
            if re.search(GUESS[g], hay):
                out.setdefault(g, []).append(t["name"])
                break
    return out


def cmd_song(a):
    R = refs(a)
    with open(os.path.join(ROOT, "tools", "groove-pin")) as f:
        pin = f.read().split()[0]
    env = dict(os.environ)
    env.pop("LD_LIBRARY_PATH", None)
    if not a.windows:
        sys.exit("stembal: --windows FROM-TO[:label] ... (bars, 1-indexed, or seconds as 30s-90s): two or three heavy stretches")
    groups = {}
    if not a.mix_only:
        groups = dict((g.split("=")[0], g.split("=")[1].split(",")) for g in a.groups) if a.groups else guess_groups(pin, a.song, env)
        print("groups: " + "; ".join(f"{g} = {', '.join(t)}" for g, t in groups.items()))
    outdir = a.out or tempfile.mkdtemp(prefix="stembal-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    M = stats(R, "mix")[0]
    mixes, names, acc = [], [], {g: [] for g in groups}
    V = voice(a) if a.voice else None
    vt = [t for t in (a.voice_tracks or "").split(",") if t] if V and V[2] is not None else []
    if vt and "voice-tracks" in groups:
        sys.exit("stembal: a group may not be called voice-tracks when --voice-tracks is given")
    extra = [("voice-tracks", vt)] if vt else []
    parts = {}
    for p in a.parts or []:
        name, _, trs = p.partition("=")
        if not name or not [t for t in trs.split(",") if t]:
            sys.exit("stembal: --parts NAME=track,track ... (each part's tracks are rendered alone)")
        parts[name] = [t for t in trs.split(",") if t]
    if any("part-" + n in groups for n in parts):
        sys.exit("stembal: a group may not be called part-NAME when --parts has NAME")
    extra += [("part-" + n, trs) for n, trs in parts.items()]
    shares = []

    def render(g, trs, out, win, frm, to):
        cmd = ["nice", "-n", "7", pin, "--json", "render", "--threads", str(a.threads), "-f", a.song, "--seed", str(a.seed)] \
            + (["--from", frm] if frm else []) + ["--to", to, "--set", "loudness=null", "-o", out]
        for t in trs:
            cmd += ["--solo", t]
        r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=1800)
        if not os.path.exists(out):
            sys.exit(f"stembal: render failed for {g} {win}: {(r.stdout or r.stderr)[-300:]}")
        return out

    # One render a group, to the end of the last window; the windows are cut from it (see the notes above).
    secs = None if a.per_window else window_seconds(canonical(pin, a.song, env), a.windows)
    whole = {}
    if secs:
        last = max(range(len(secs)), key=lambda i: secs[i][1])
        to = a.windows[last].partition(":")[0].partition("-")[2]
        for g, trs in list(groups.items()) + [("mix", [])] + extra:
            whole[g] = render(g, trs, os.path.join(outdir, f"sb-{g}-whole.wav"), a.windows[last], None, to)
        try:
            with wave.open(whole["mix"], "rb"):
                pass
        except (wave.Error, EOFError):                # not a PCM file the cutter reads: window by window after all
            for f in whole.values():
                os.remove(f)
            secs, whole = None, {}
    for i, win in enumerate(a.windows):
        span, _, label = win.partition(":")
        b0, b1 = span.split("-")
        w = {}
        lv = {}
        for g, trs in list(groups.items()) + [("mix", [])] + extra:
            out = os.path.join(outdir, f"sb-{g}-{b0}.wav")
            if secs:
                cut(whole[g], out, *secs[i])
            else:
                render(g, trs, out, win, b0, b1)
            if g != "voice-tracks":
                w[g] = bands(load(out))
            if vt and g in ("mix", "voice-tracks"):
                lv[g] = frame_levels(load(out))
            os.remove(out)
        if vt:
            shares.append(voice_share(lv["mix"], lv["voice-tracks"], V[2]))
        tot = w["mix"].sum()
        mixes.append(db(w["mix"] / tot))
        names.append(label or span)
        print(f"mix, {(label or span)[:16]:16s}" + "".join(f"{x:7.1f}" for x in mixes[-1]) + "   | ours - refs: "
              + "".join(f"{x:6.1f}" for x in mixes[-1] - M))
        if groups:
            rows = []
            for g in groups:
                v = np.append(db(w[g] / tot), db(w[g].sum() / tot))
                acc[g].append(v)
                rows.append((g, v))
            show(f"== ours, {label or span} ({span}; dB re the whole mix)", rows)
        if parts:
            print(f"== whose band is it, {label or span} ({span}): each part alone, dB under the mix's OWN band (0 = it is the band)")
            print("\n".join(whose(w["mix"], [(n, w["part-" + n]) for n in parts])))
    for f in whole.values():
        os.remove(f)
    print(f"{'refs mix median':22s}" + "".join(f"{x:7.1f}" for x in M))
    print(f"{'OURS - REFS (mean)':22s}" + "".join(f"{x:7.1f}" for x in np.mean(mixes, axis=0) - M))
    if a.spread:
        S = spread(a)
        if S:
            print(f"{'refs own spread (std)':22s}" + "".join(f"{x:7.1f}" for x in spread_medians(S)[0])
                  + "   | what the records move between their own loud passages")
    if a.voice:
        if V:
            off, n, _ = V
            rows = [("no voice - all", off["without"]), ("voice - all", off["with"])]
            for i, (name, m) in enumerate(zip(names, mixes)):
                rows += [(f"{name[:11]}, no voice", m - (M + off["without"])), (f"{name[:11]}, voice", m - (M + off["with"]))]
                if vt:
                    sh = shares[i]
                    rows.append((f"{name[:8]}, blend {sh:.0%}", m - (M + sh * off["with"] + (1 - sh) * off["without"])))
            show(f"== each window against the records' passages WITHOUT a voice and WITH one (ours minus the median shifted by "
                 f"the first two rows; {n['without']} and {n['with']} records; tools/vocsplit.py)", rows, whole=False)
        else:
            print("stembal: --voice: too few of these records have loud passages both with and without a voice")
    for g in groups:
        if not any(g in R[s] for s in R):
            continue
        med, lo, hi = stats(R, g)
        ours = np.mean(acc[g], axis=0)
        show(f"== {g}: ours (mean of the windows), the references' median, ours minus theirs, their middle half's width",
             [("ours", ours), ("refs median", med), ("ours - refs", ours - med), ("refs p75 - p25", hi - lo)])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["refs", "song"])
    ap.add_argument("song", nargs="?")
    ap.add_argument("--refs")
    ap.add_argument("--model", default="bs_roformer_sw")
    ap.add_argument("--from", dest="start", type=float, default=30.0)
    ap.add_argument("--dur", type=float, default=120.0)
    ap.add_argument("--windows", nargs="+")
    ap.add_argument("--groups", nargs="+")
    ap.add_argument("--mix-only", action="store_true")
    ap.add_argument("--parts", nargs="+", help="NAME=track,track ...: each part alone against the mix's own band, and who holds it")
    ap.add_argument("--per-window", action="store_true", help="render every window by itself, as before 13 Nov")
    ap.add_argument("--spread", action="store_true")
    ap.add_argument("--voice", action="store_true", help="read every window against the records' passages without a voice and with one")
    ap.add_argument("--voice-tracks", help="with --voice: the voice's tracks; adds a row blended by the share of the window they fill")
    ap.add_argument("--win", type=float, default=20.0)
    ap.add_argument("--within", type=float, default=3.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.cmd == "refs":
        cmd_refs(a)
    else:
        if not a.song:
            ap.error("song SONG.yaml")
        cmd_song(a)


if __name__ == "__main__":
    main()
