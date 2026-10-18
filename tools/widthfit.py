#!/usr/bin/env python3
"""Per-section, per-band master stereo width fitted to the reference — the lever that moved Laid to Rest (+3.7),
Flim (+3.1), Raining Blood (+2.7) and The National Anthem (+2.6).

likeness' stereo term compares side/mid in seven bands (20-60-150-400-1.2k-3.5k-8k-16k) per section. This tool
puts ONE neutral width stage at the front of the master chain whose seven band widths are automation lanes
(wb0..wb6, one value per section, 50 ms ramps at the cuts; band lanes need chirp >= f4b9563) and sets each value
to the record's side/mid over the render's. Run it again on a new render to refine (it multiplies the existing
lanes by the residual): the clip/limiter after the stage and the bands' crossovers re-create or leak side, so a
first pass under-corrects and 2-4 passes converge (stop when a pass ties).

  widthfit.py IN OUT RENDER.wav REF.wav SECTIONS.txt [--bass-width 0.5] [--clip LO,HI] [--min-sec 5] [--strength 1] [--only 4,6,7] [--joint]

IN/OUT: a tab2song map (.json; edits head.master) or a song (.yaml; replaces its `master:` line). First pass
(no wb lanes yet): ratios clipped to 0.2..2.5; later passes 0.5..2.0 (--clip overrides). --bass-width sets the
stage's width below its 120 Hz corner, where the band lanes do not reach (0.3-0.5 when the record's lows are
narrower than ours). --strength S applies ratio**S (0.5 = half the correction in dB: quiet acoustic records whose width is room
sound responded better to half — Daydreaming). --only N,M (1-based, as printed) fits just those sections; the others keep their lanes (1.0 on a first pass) — on a
mature mix fit only sections whose stereo term is below ~80: Bleed's full pass lost where the image was already right
(near-1 ratios add noise), the selective one gained +0.5. Sections shorter than --min-sec seconds of render keep the previous section's values.
Recipe for a mature mix (chirper-zero's 'stale width'): print the per-section stereo term; run 2 passes with --only the
sections below ~65 and --clip 0.5,4; score per section; then REFIT from the base on the winners only (2 passes).
Raining Blood +0.58, Come Down +0.4, 2 Minutes to Midnight +0.12, The National Anthem +0.1 held-out. Sections whose
stereo is content (an intro's mono voice, a squall ending, a part's pan) lose — leave them out.
Prints each section's ratios. Measure the result with likeness; keep it only if it scores higher.

The bands are coupled (bd-33c6c3; tools/widthresp.py): wb_k scales the side from FREQS[k] up (lower edge), but the
stage's crossovers are 12 dB/oct Butterworth splits ~3x apart, so a measured band answers its own width and the next
one up about equally (and the one below slightly negatively, through phase); with uneven widths a band follows its
widest neighbour (MM tail: 1.2-3.5k measured x4.08 with wb4 1.95, wb5 4.2). The per-band ratio above assumes each
band answers only its own width. --joint (opt-in) instead solves a section's seven widths together on the exact
stage model, weighted by the render's own side spectrum, for the likeness stereo residuals (same --clip bounds per
pass, --strength scales the step); each section prints the model's predicted stereo term now / per-band / joint.
The model covers the stage only: anything after it that reacts to the side (clip, limiter) is why passes repeat."""
import json, re, sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import likeness as L  # noqa: E402

FREQS = [20, 60, 150, 400, 1200, 3500, 8000]


def flow_to_json(s):
    """Minimal YAML-flow → JSON for master lines such as ["glue …", {type: gain, gain: 3dB}, "clip …"]."""
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    s = re.sub(r'([{,]\s*)([A-Za-z_][\w.]*)\s*:', r'\1"\2":', s)                       # bare keys
    s = re.sub(r':\s*([A-Za-z_+\-.\d][^,"{}\[\]]*?)\s*(?=[,}\]])',
               lambda m: ": " + (m.group(1) if re.fullmatch(r"-?\d+(\.\d+)?", m.group(1)) else json.dumps(m.group(1))), s)
    return json.loads(s)


def lanes(cuts, W):
    out = {}
    for k in range(W.shape[1]):
        pts = [["0s", round(float(W[0, k]), 3)]]
        for i in range(1, len(W)):
            pts += [[f"{cuts[i] - 0.05:.3f}s", round(float(W[i - 1, k]), 3)], [f"{cuts[i] + 0.05:.3f}s", round(float(W[i, k]), 3)]]
        out[f"wb{k}"] = {"points": pts}
    return out


def main():
    a = sys.argv[1:]
    if len(a) < 5:
        sys.exit(__doc__)
    src, dst, wav, ref, secf = a[:5]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    cuts = [float(x) for x in open(secf).read().replace("\n", ",").split(",") if x.strip()]
    nsec = len(cuts) - 1
    is_map = src.endswith(".json")
    if is_map:
        doc = json.load(open(src))
        master = doc.setdefault("head", {}).get("master")
    else:
        lines = open(src).read().splitlines()
        mi = next((k for k, l in enumerate(lines) if l.startswith("master:")), None)
        master = flow_to_json(lines[mi][len("master:"):].strip()) if mi is not None else None
    if master is None:
        master = {"fx": []}
    elif isinstance(master, list):
        master = {"fx": master}
    master.setdefault("fx", [])
    auto = master.setdefault("auto", {})
    first = "wb0" not in auto
    lo, hi = (float(x) for x in opt("--clip", "0.2,2.5" if first else "0.5,2.0").split(","))
    if first:
        cur = np.ones((nsec, 7))
        master["fx"].insert(0, {"type": "width", "width": 1.0, "bass_width": float(opt("--bass-width", 1.0)),
                                "bands": [[f, {"value": 0.0, "mod": [{"src": f"auto.wb{k}", "amount": 1}]}] for k, f in enumerate(FREQS)]})
    else:
        cur = np.array([[auto[f"wb{k}"]["points"][0 if i == 0 else 2 * i][1] for k in range(7)] for i in range(nsec)])
        if "--bass-width" in a:
            for f in master["fx"]:
                if isinstance(f, dict) and f.get("type") == "width" and any(isinstance(b[1], dict) and "auto.wb" in json.dumps(b[1]) for b in f.get("bands", [])):
                    f["bass_width"] = float(opt("--bass-width", 1.0))   # only the lane stage, not other (static) width stages
    R, O = L.load(ref), L.load(wav)
    minsec = float(opt("--min-sec", 5))
    strength = float(opt("--strength", 1.0))
    only = {int(v) for v in opt("--only", "").split(",") if v.strip()} if "--only" in a else None
    joint = "--joint" in a
    if joint:
        import widthresp as WR
        bass = next((float(f.get("bass_width", 1.0)) for f in master["fx"] if isinstance(f, dict) and f.get("type") == "width"
                     and any(isinstance(b[1], dict) and "auto.wb" in json.dumps(b[1]) for b in f.get("bands", []))), 1.0)
    for i in range(nsec):
        if only is not None and i + 1 not in only:
            continue
        s0, s1 = int(cuts[i] * 48000), min(int(cuts[i + 1] * 48000), len(O), len(R))
        if s1 - s0 < minsec * 48000:
            if i:
                cur[i] = cur[i - 1]
            continue
        r = np.clip(L.stereo_bands(R[s0:s1]) / np.maximum(L.stereo_bands(O[s0:s1]), 1e-3), lo, hi) ** strength
        if joint:
            f_, ps, pm = WR.spectra(O[s0:s1])
            target = L.stereo_bands(R[s0:s1])
            naive = np.clip(cur[i] * r, 0, 6)
            new = WR.fit_joint(f_, ps, pm, cur[i], target, lo, hi, cap=6.0, strength=strength, bass_width=bass)
            term = lambda w: WR.stereo_term(WR.predict_ratios(f_, ps, pm, cur[i], w, bass_width=bass), target)  # noqa: E731
            print(f"section {i + 1:2d} joint x " + " ".join(f"{v:.2f}" for v in new / np.maximum(cur[i], 1e-9))
                  + f"  | predicted stereo term {term(cur[i]):.1f} now, {term(naive):.1f} per-band, {term(new):.1f} joint")
            cur[i] = new
            continue
        cur[i] = np.clip(cur[i] * r, 0, 6)
        print(f"section {i + 1:2d} ratio " + " ".join(f"{v:.2f}" for v in r))
    auto.update(lanes(cuts, cur))
    if is_map:
        doc["head"]["master"] = master
        json.dump(doc, open(dst, "w"), indent=1)
    else:
        line = "master: " + json.dumps(master)
        if mi is None:
            ci = next((k for k, l in enumerate(lines) if l.startswith(("ceiling:", "tempo:"))), 0)
            lines.insert(ci + 1, line)
        else:
            lines[mi] = line
        open(dst, "w").write("\n".join(lines) + "\n")
    print(f"{'inserted' if first else 'refined'} master band lanes ({lo}..{hi}) -> {dst}")


if __name__ == "__main__":
    main()
