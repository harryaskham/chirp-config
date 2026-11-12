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
        --mix-only: only the whole-mix rows (one render per window: for iterating on an equaliser).

  --refs all = every record that has stems. What Common Time used (chirpers10, v7):
  --refs bleed,combustion,dancers-to-a-discordant-system,electric-red,lethargica,obzen,pineal-gland-optics,pravus,
         the-abysmal-eye,the-faultless,this-spiteful-snake      (one argument, no spaces)
  --groups drums=kick,snare,cym,toms,hat,ride guitar=gl,gr,gl2,gr2,wl,wr,lead bass=bass
  --windows 41-56:riffA 247-276:all-three 282-309:hardest

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

import numpy as np

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
    n = 8192
    k = max(1, len(x) // n)
    sp = np.zeros(n // 2 + 1)
    w = np.hanning(n)
    for i in range(k):
        seg = x[i * n:(i + 1) * n]
        if len(seg) == n:
            sp += np.abs(np.fft.rfft(seg * w)) ** 2
    fr = np.fft.rfftfreq(n, 1 / 44100)
    return np.array([sp[(fr >= lo) & (fr < hi)].sum() for lo, hi in zip(EDGES[:-1], EDGES[1:])]) / k


def db(v):
    return 10 * np.log10(np.maximum(v, 1e-20))


def stem_dir(model):
    return os.path.join(ROOT, "ref", "stems", model)


def ref_ids(a):
    have = sorted(d for d in os.listdir(stem_dir(a.model)) if os.path.exists(os.path.join(stem_dir(a.model), d, "drums.wav")))
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
    key = hashlib.sha1(json.dumps([ids, a.model, a.start, a.dur]).encode()).hexdigest()[:12]
    cache = os.path.join(ROOT, "ref", "stembal", key + ".json")
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    out = {}
    for s in ids:
        d = os.path.join(stem_dir(a.model), s)
        st = {n: bands(load(os.path.join(d, n + ".wav"), a.start, a.dur)) for n in STEMS if os.path.exists(os.path.join(d, n + ".wav"))}
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


def guess_groups(pin, song, env):
    r = subprocess.run([pin, "--json", "plan", "-f", song, "--set", "seed=0"], capture_output=True, text=True, env=env)
    try:
        tracks = json.loads(r.stdout)["data"]["canonical"]["tracks"]
    except (ValueError, KeyError):
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
    mixes, acc = [], {g: [] for g in groups}
    for win in a.windows:
        span, _, label = win.partition(":")
        b0, b1 = span.split("-")
        w = {}
        for g, trs in list(groups.items()) + [("mix", [])]:
            out = os.path.join(outdir, f"sb-{g}-{b0}.wav")
            cmd = ["nice", "-n", "7", pin, "--json", "render", "--threads", str(a.threads), "-f", a.song, "--seed", str(a.seed),
                   "--from", b0, "--to", b1, "--set", "loudness=null", "-o", out]
            for t in trs:
                cmd += ["--solo", t]
            r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=1800)
            if not os.path.exists(out):
                sys.exit(f"stembal: render failed for {g} {win}: {(r.stdout or r.stderr)[-300:]}")
            w[g] = bands(load(out))
            os.remove(out)
        tot = w["mix"].sum()
        mixes.append(db(w["mix"] / tot))
        print(f"mix, {(label or span)[:16]:16s}" + "".join(f"{x:7.1f}" for x in mixes[-1]) + "   | ours - refs: "
              + "".join(f"{x:6.1f}" for x in mixes[-1] - M))
        if groups:
            rows = []
            for g in groups:
                v = np.append(db(w[g] / tot), db(w[g].sum() / tot))
                acc[g].append(v)
                rows.append((g, v))
            show(f"== ours, {label or span} ({span}; dB re the whole mix)", rows)
    print(f"{'refs mix median':22s}" + "".join(f"{x:7.1f}" for x in M))
    print(f"{'OURS - REFS (mean)':22s}" + "".join(f"{x:7.1f}" for x in np.mean(mixes, axis=0) - M))
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
