#!/usr/bin/env python3
"""Per-section, per-band master stereo width fitted to the reference — the lever that moved Laid to Rest (+3.7),
Flim (+3.1), Raining Blood (+2.7) and The National Anthem (+2.6).

likeness' stereo term compares side/mid in seven bands (20-60-150-400-1.2k-3.5k-8k-16k) per section. This tool
puts ONE neutral width stage at the front of the master chain whose seven band widths are automation lanes
(wb0..wb6, one value per section, 50 ms ramps at the cuts; band lanes need chirp >= f4b9563) and sets each value
to the record's side/mid over the render's. Run it again on a new render to refine (it multiplies the existing
lanes by the residual): the clip/limiter after the stage and the bands' crossovers re-create or leak side, so a
first pass under-corrects and 2-4 passes converge (stop when a pass ties).

  widthfit.py IN OUT RENDER.wav[,RENDER2.wav,...] REF.wav SECTIONS.txt [--bass-width 0.5] [--clip LO,HI] [--min-sec 5] [--strength 1] [--only 4,6,7] [--joint]

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
Several seed renders pool their side/mid POWER spectra per section (not their waveforms), fitting the seed-average
image. One input keeps the original path. A literal filename containing a comma is accepted if that file exists.
Prints each section's ratios. Measure the result with likeness; keep it only if it scores higher.

The bands are coupled (bd-33c6c3; tools/widthresp.py): wb_k scales the side from FREQS[k] up (lower edge), but the
stage's crossovers are 12 dB/oct Butterworth splits ~3x apart, so a measured band answers its own width and the next
one up about equally (and the one below slightly negatively, through phase); with uneven widths a band follows its
widest neighbour (MM tail: 1.2-3.5k measured x4.08 with wb4 1.95, wb5 4.2). The per-band ratio above assumes each
band answers only its own width. --joint (opt-in) instead solves a section's seven widths together on the exact
stage model, weighted by the render's own side spectrum, for the likeness stereo residuals (same --clip bounds per
pass, --strength scales the step); each section prints the model's predicted stereo term now / per-band / joint.
The model covers the stage only: anything after it that reacts to the side (clip, limiter) is why passes repeat."""
import json, os, re, sys

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


def lane_points(points):
    """[(seconds, value)] of an automation lane whose times are "N.NNNs" (widthfit's lanes); anything else is refused
    (before anything is written) rather than misread."""
    out = []
    for t, v in points:
        ts = str(t)
        if not ts.endswith("s") or ts.endswith("ms"):
            sys.exit(f"widthfit: lane point time {t!r} is not in seconds; refusing to rewrite this lane")
        out.append((float(ts[:-1]), float(v)))
    return out


def section_mean(points, a, b, ramp=0.05):
    """The time-weighted mean of a piecewise-linear lane over the section's interior [a + ramp, b - ramp] (the 50 ms
    lane ramps at the cuts belong to both neighbours) — by actual time, not knot order (custom knots shift the
    ordinals: Imprint v10's 32.15/63.85 s ramps, bd-3a56c6). On widthfit's regular grid this is the section's value."""
    if b - a > 4 * ramp:
        a, b = a + ramp, b - ramp
    pts = lane_points(points)
    ts, vs = [p[0] for p in pts], [p[1] for p in pts]
    grid = sorted({a, b, *[t for t in ts if a < t < b]})
    val = lambda t: float(np.interp(t, ts, vs))  # noqa: E731
    area = sum((t1 - t0) * (val(t0) + val(t1)) / 2 for t0, t1 in zip(grid, grid[1:]))
    return area / (b - a) if b > a else val(a)


def varies(points, a, b, mean, tol=0.10, share=0.10):
    """Whether a lane strays more than tol from its section mean for more than share of the section (a shape the
    one-width-per-section model does not describe)."""
    pts = lane_points(points)
    ts, vs = [p[0] for p in pts], [p[1] for p in pts]
    grid = np.linspace(a, b, 401)
    dev = np.abs(np.interp(grid, ts, vs) - mean) > tol * max(abs(mean), 1e-9)
    return dev.mean() > share


def scale_section(points, a, b, r, absolute=None, now=None, new=None):
    """The lane with every knot in [a, b) scaled by r (clipped 0..6, rounded) — or set to `absolute` where the
    current width is 0; a knot at exactly the section's current value `now` takes `new` (so a regular grid rounds as
    before); knots elsewhere keep their exact time strings and values. A section without knots of its own gets a
    pair just inside its edges."""
    inside = [i for i, (t, _) in enumerate(points) if a <= float(str(t)[:-1]) < b]
    pts = [list(p) for p in points]
    if not inside:
        v = section_mean(points, a, b)
        added = [[f"{a + 0.05:.3f}s", v], [f"{b - 0.05:.3f}s", v]]
        pts = sorted(pts + added, key=lambda p: float(str(p[0])[:-1]))
        inside = [i for i, (t, _) in enumerate(pts) if a <= float(str(t)[:-1]) < b]
    for i in inside:
        if absolute is not None:
            nv = absolute
        elif now is not None and float(pts[i][1]) == now:
            nv = new
        else:
            nv = pts[i][1] * r
        pts[i][1] = round(float(np.clip(nv, 0, 6)), 3)
    return pts


def lanes(cuts, W):
    out = {}
    for k in range(W.shape[1]):
        pts = [["0s", round(float(W[0, k]), 3)]]
        for i in range(1, len(W)):
            pts += [[f"{cuts[i] - 0.05:.3f}s", round(float(W[i - 1, k]), 3)], [f"{cuts[i] + 0.05:.3f}s", round(float(W[i, k]), 3)]]
        out[f"wb{k}"] = {"points": pts}
    return out


def pooled_spectra(segments):
    """Mean side/mid PSDs on the common sample window; phase-opposed renders must not cancel."""
    import widthresp as WR
    spectra = [WR.spectra(st) for st in segments]
    f = spectra[0][0]
    if not all(np.array_equal(f, v[0]) for v in spectra[1:]):
        raise ValueError("widthfit: seed renders have incompatible frequency grids")
    return f, np.mean([v[1] for v in spectra], axis=0), np.mean([v[2] for v in spectra], axis=0)


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
        # the current width of each section, by time (bd-3a56c6: custom knots shifted the old points[2*i] read)
        cur = np.array([[section_mean(auto[f"wb{k}"]["points"], cuts[i], cuts[i + 1]) for k in range(7)] for i in range(nsec)])
        if "--bass-width" in a:
            for f in master["fx"]:
                if isinstance(f, dict) and f.get("type") == "width" and any(isinstance(b[1], dict) and "auto.wb" in json.dumps(b[1]) for b in f.get("bands", [])):
                    f["bass_width"] = float(opt("--bass-width", 1.0))   # only the lane stage, not other (static) width stages
    paths = [wav] if os.path.isfile(wav) else wav.split(",")
    if any(not p for p in paths):
        sys.exit("widthfit: render list contains an empty path")
    R, renders = L.load(ref), [L.load(p) for p in paths]
    O = renders[0]
    minsec = float(opt("--min-sec", 5))
    strength = float(opt("--strength", 1.0))
    only = {int(v) for v in opt("--only", "").split(",") if v.strip()} if "--only" in a else None
    joint = "--joint" in a
    if joint or len(renders) > 1:
        import widthresp as WR
        bass = next((float(f.get("bass_width", 1.0)) for f in master["fx"] if isinstance(f, dict) and f.get("type") == "width"
                     and any(isinstance(b[1], dict) and "auto.wb" in json.dumps(b[1]) for b in f.get("bands", []))), 1.0)
    now = cur.copy()   # the current widths; cur becomes the new ones, and only `fitted` sections are rewritten
    fitted = []
    for i in range(nsec):
        if only is not None and i + 1 not in only:
            continue
        if not first and "--scale-shapes" not in a:
            shaped = [k for k in range(7) if varies(auto[f"wb{k}"]["points"], cuts[i], cuts[i + 1], now[i, k])]
            if shaped:
                sys.exit(f"widthfit: section {i + 1}: lanes " + ", ".join(f"wb{k}" for k in shaped) + " vary within the "
                         "section (more than 10% off their mean for over 10% of it); widthfit fits one width per section. "
                         "Leave the section out (--only), or --scale-shapes to scale the shape by the fitted factor. "
                         "Nothing written.")
        s0, s1 = int(cuts[i] * 48000), min(int(cuts[i + 1] * 48000), len(R), *(len(o) for o in renders))
        if s1 - s0 < minsec * 48000:
            if i:
                cur[i] = cur[i - 1]
                fitted.append(i)
            continue
        if len(renders) > 1:
            f_, ps, pm = pooled_spectra([o[s0:s1] for o in renders])
            current = WR.band_ratios(f_, ps, pm)
        else:
            current = L.stereo_bands(O[s0:s1])
        r = np.clip(L.stereo_bands(R[s0:s1]) / np.maximum(current, 1e-3), lo, hi) ** strength
        if joint:
            if len(renders) == 1:
                f_, ps, pm = WR.spectra(O[s0:s1])
            target = L.stereo_bands(R[s0:s1])
            naive = np.clip(cur[i] * r, 0, 6)
            new = WR.fit_joint(f_, ps, pm, cur[i], target, lo, hi, cap=6.0, strength=strength, bass_width=bass)
            term = lambda w: WR.stereo_term(WR.predict_ratios(f_, ps, pm, cur[i], w, bass_width=bass), target)  # noqa: E731
            print(f"section {i + 1:2d} joint x " + " ".join(f"{v:.2f}" for v in new / np.maximum(cur[i], 1e-9))
                  + f"  | predicted stereo term {term(cur[i]):.1f} now, {term(naive):.1f} per-band, {term(new):.1f} joint")
            cur[i] = new
            fitted.append(i)
            continue
        cur[i] = np.clip(cur[i] * r, 0, 6)
        fitted.append(i)
        print(f"section {i + 1:2d} ratio " + " ".join(f"{v:.2f}" for v in r))
    if first:
        auto.update(lanes(cuts, cur))
    else:
        # rewrite only the fitted sections, scaling their own knots (shapes and unselected sections survive; a
        # factor of exactly 1 changes nothing)
        for i in fitted:
            for k in range(7):
                lane = auto[f"wb{k}"]
                if now[i, k] > 0:
                    r = cur[i, k] / now[i, k]
                    if r != 1.0:
                        lane["points"] = scale_section(lane["points"], cuts[i], cuts[i + 1], r, now=now[i, k], new=cur[i, k])
                elif cur[i, k] != now[i, k]:
                    lane["points"] = scale_section(lane["points"], cuts[i], cuts[i + 1], 1.0, absolute=cur[i, k])
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
