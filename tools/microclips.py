#!/usr/bin/env python3
"""microclips: the micro benchmark's clip set (micro/clips.json): moments where one instrument is exposed, 1-10 s, from
records we have stems for (Harry, 25 Oct; scored by tools/microscore.py).

  microclips.py propose [ID …] [--all] [--min 1.5] [--max 8] [--share 0.7] [--per-song 3] [--kit-std 6]
                        [--sum riff=guitar+bass] [--json]
  microclips.py add SONG --from A --to B --family F [--holdout] [--note TEXT] [--ref-stems guitar+bass]
  microclips.py list

propose: every 0.5 s frame of the song's htdemucs_6s stems (and ref/stems/crowd/ID/crowd.wav when tools/livestems.py
made one) gets each stem's share of their summed energy; a run of frames where one stem holds >= --share while the mix
is within 20 dB of the song's loud level is a candidate (trimmed to --max s, the most dominant stretch). Ranked by
mean share x duration, at most --per-song per song, family = the stem (bass, drums, guitar, piano, vocals, other,
crowd). Curate with `add` (the same clip id = SONG-FAMILY-START); mark about a third of each family --holdout: those
are never tuned on, and a library change must improve them too.
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "micro", "clips.json")
STEMS = ("bass", "drums", "guitar", "piano", "vocals", "other")
HOP = 0.5


def frame_energy(path):
    x = L.load(path)
    x = x.mean(1) if x.ndim > 1 else x
    h = int(HOP * L.SR)
    n = len(x) // h
    return (x[:n * h].reshape(n, h) ** 2).mean(1)


def shares(cid):
    """(names, [stems, frames] energy shares, mix level dB per frame) or None without stems."""
    d = os.path.join(ROOT, "ref", "stems", "htdemucs_6s", cid)
    if not os.path.exists(os.path.join(d, "vocals.wav")):
        return None
    names, rows = [], []
    for s in STEMS:
        p = os.path.join(d, f"{s}.wav")
        if os.path.exists(p):
            names.append(s)
            rows.append(frame_energy(p))
    crowd = os.path.join(ROOT, "ref", "stems", "crowd", cid, "crowd.wav")
    if os.path.exists(crowd):
        names.append("crowd")
        rows.append(frame_energy(crowd))
    n = min(len(r) for r in rows)
    e = np.stack([r[:n] for r in rows])      # (with a crowd stem the band stems are of the crowd-free mix: they add up)
    tot = e.sum(0) + 1e-14
    return names, e / tot, 10 * np.log10(tot)


def envelope_std(cid, a, b, stem="drums"):
    """Std (dB) of a stem's 20 ms frame level over a..b s: a kit swings 8-25 dB between hits; a sustained roll
    (S&M's timpani under 'one-drums-46', chirper-three: 3 dB) barely moves."""
    x = L.load(os.path.join(ROOT, "ref", "stems", "htdemucs_6s", cid, f"{stem}.wav"))
    x = x.mean(1) if x.ndim > 1 else x
    seg = x[int(a * L.SR):int(b * L.SR)]
    h = int(0.02 * L.SR)
    n = len(seg) // h
    if n < 2:
        return 0.0
    return float((10 * np.log10((seg[:n * h].reshape(n, h) ** 2).mean(1) + 1e-14)).std())


def candidates(cid, mn=1.5, mx=8.0, share=0.7, kit_std=None, sums=()):
    got = shares(cid)
    if got is None:
        return []
    names, sh, lev = got
    extra = [(fam, parts) for fam, parts in sums if all(x in names for x in parts)]
    if extra:                                  # opt-in summed families (e.g. riff = guitar + bass): their shares add
        names = names + [fam for fam, _ in extra]
        sh = np.vstack([sh] + [sum(sh[names.index(x)] for x in parts)[None] for _, parts in extra])
    loud = np.percentile(lev, 95)
    out = []
    for i, name in enumerate(names):
        ok = (sh[i] >= share) & (lev >= loud - 20)
        k = 0
        while k < len(ok):
            if not ok[k]:
                k += 1
                continue
            s = k
            while k < len(ok) and ok[k]:
                k += 1
            if (k - s) * HOP >= mn:
                w = int(mx / HOP)
                if k - s > w:                  # the most dominant window of --max s
                    best = max(range(s, k - w + 1), key=lambda j: sh[i, j:j + w].mean())
                    a, b = best, best + w
                else:
                    a, b = s, k
                out.append({"song": cid, "family": name, "from": round(a * HOP, 1), "to": round(b * HOP, 1),
                            "share": round(float(sh[i, a:b].mean()), 3), "rank": float(sh[i, a:b].mean() * (b - a) * HOP)})
    if kit_std is not None:                    # opt-in: drums candidates must be a kit, not a sustained roll
        out = [c for c in out if c["family"] != "drums" or envelope_std(cid, c["from"], c["to"]) >= kit_std]
    return sorted(out, key=lambda c: -c["rank"])


def parse_sums(specs):
    """['riff=guitar+bass', …] -> [('riff', ['guitar', 'bass']), …]."""
    out = []
    for sp in specs or ():
        fam, _, parts = sp.partition("=")
        ps = [x for x in parts.split("+") if x]
        if not fam or len(ps) < 2 or any(x not in STEMS + ("crowd",) for x in ps):
            raise SystemExit(f"microclips: --sum wants FAMILY=STEM+STEM from {', '.join(STEMS)} (got {sp!r})")
        out.append((fam, ps))
    return out


def load_manifest():
    if os.path.exists(MANIFEST):
        return json.load(open(MANIFEST))
    return {"about": "Micro benchmark clips (tools/microclips.py, scored by tools/microscore.py). holdout clips are never "
                     "tuned on: a library change must improve them too.", "clips": []}


def save_manifest(m):
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    with open(MANIFEST, "w") as f:
        json.dump(m, f, indent=1)
        f.write("\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("propose", "add", "list"))
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--min", type=float, default=1.5)
    ap.add_argument("--max", type=float, default=8.0)
    ap.add_argument("--share", type=float, default=0.7)
    ap.add_argument("--per-song", type=int, default=3)
    ap.add_argument("--sum", action="append", default=[], metavar="FAMILY=STEM+STEM",
                    help="propose a summed family too, e.g. riff=guitar+bass (Immutable: the 8-string's low register lands "
                         "in demucs' bass stem, so no guitar stem is ever exposed)")
    ap.add_argument("--ref-stems", metavar="STEM+STEM", help="add: score the clip against these stems summed, not the mix")
    ap.add_argument("--kit-std", type=float, help="drums candidates need this much 20 ms level swing (dB; ~6): drops "
                                                  "sustained rolls (timpani) the stem share alone mistakes for a kit")
    ap.add_argument("--from", dest="t0", type=float)
    ap.add_argument("--to", dest="t1", type=float)
    ap.add_argument("--family")
    ap.add_argument("--holdout", action="store_true")
    ap.add_argument("--note", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "list":
        for c in load_manifest()["clips"]:
            hold = "HOLDOUT " if c.get("holdout") else ""
            print(f"{c['id']:44s} {c['family']:8s} {c['from']:6.1f}-{c['to']:<6.1f} {hold}{c.get('note', '')}")
        return
    if a.cmd == "add":
        if len(a.ids) != 1 or a.t0 is None or a.t1 is None or not a.family:
            ap.error("add SONG --from A --to B --family F")
        if not 1.0 <= a.t1 - a.t0 <= 10.0:
            ap.error("a clip is 1-10 s")
        song = a.ids[0]
        if not os.path.exists(os.path.join(ROOT, "ref", f"{song}.wav")):
            ap.error(f"no ref/{song}.wav")
        m = load_manifest()
        cid = f"{song}-{a.family}-{int(a.t0)}"
        m["clips"] = [c for c in m["clips"] if c["id"] != cid] + [
            {"id": cid, "song": song, "from": a.t0, "to": a.t1, "family": a.family, "holdout": a.holdout, "note": a.note,
             **({"ref": f"stems:{a.ref_stems}"} if a.ref_stems else {})}]
        save_manifest(m)
        print(f"added {cid}")
        return
    reg = json.load(open(os.path.join(ROOT, "climbs.json")))["climbs"]
    ids = a.ids or [c["id"] for c in reg if c.get("song") and (a.all or c.get("enabled"))]
    res = []
    for cid in ids:
        res.extend(candidates(cid, a.min, a.max, a.share, a.kit_std, parse_sums(a.sum))[:a.per_song])
    if a.json:
        print(json.dumps(res, indent=1))
        return
    for c in sorted(res, key=lambda c: (c["family"], -c["rank"])):
        print(f"{c['family']:8s} {c['song']:40s} {c['from']:6.1f}-{c['to']:<6.1f} share {c['share']:.2f}")


if __name__ == "__main__":
    main()
