#!/usr/bin/env python3
"""riffpunch: our guitar chugs against the record's guitar stem, per picked note (the tone push, micro/TONE.md).
It separates the two reasons microscore's riff `transients` (an onset-envelope correlation) can read near zero:
our notes are off the record's timing, or our attacks are the wrong shape.

  riffpunch.py --song ID [--from S --to S] [--song-file F] [--tracks a,b] [--set PATH=V …] [--seed N]
               [--stems guitar|guitar+bass] [--ours WAV] [--json]
  riffpunch.py --clip CLIP_ID [same options]
  riffpunch.py --strokes --song-file F --from S --to S [--tracks a,b] [--set PATH=V …] [--ours WAV] [--json]
      an ORIGINAL song's strokes (no record of its own) beside the RECORDS' strokes: see "--strokes" below

Events: our guitar tracks' notes (patches/tracks matching m8|guitar|gtr|emg|rig|chug, or --tracks), doubled parts
merged; a CLEAN onset has no other guitar onset within 40 ms before it and 60 ms after. Ours: those tracks rendered
solo (groove pin). Ref: the record's guitar stem (bs_roformer_sw, else htdemucs_6s; --stems guitar+bass adds the bass
stem, where demucs puts the 8-string's low register).

Per clean onset, on both sides (the ref's peak searched within +-30 ms of ours after a global lag):
  offset_ms   where the record's attack is against ours (+ = the record is later): timing, not tone
  rise_ms     10% -> 90% of the attack peak, 150 Hz-8 kHz
  punch_db    the attack peak vs 30-60 ms later (150 Hz-8 kHz)
  tight_db    100-250 Hz: the first 20 ms vs 40-80 ms (a tight chug's low end dies fast: larger = tighter)
  fizz_db     6-10 kHz vs 1-4 kHz over 20-120 ms
  scoop_db    400 Hz-1 kHz vs 1-4 kHz over 20-120 ms
  grain       spectral flatness 1-4 kHz over 20-120 ms (noise between the harmonics; a clean synth series is low)
Reported: each side's medians, the median paired difference, and the offset's median and spread. Score as drumpunch
(100 * exp(-mean(|diff| / tolerance) / 2)) over the tone measures; timing is reported, not scored.

Timing caveat (chirper-one, 28 Oct): in sustained distortion the record's per-note attack peak is not resolvable;
a peak picked at random in the +-30 ms window gives IQR 30 ms and 67% off by >10 ms, which is what our songs read.
So the offset line is shown with that baseline and is NOT evidence of drift unless it is far below it; the tone
measures are taken at the same moment on both sides (no per-note re-alignment), after a global lag capped at +-20 ms.

Separator floor (28 Oct; htdemucs vs bs_roformer guitar stems of one song, 30 s each of Bleed, Faultless, Pineal):
total 67-86. grain agrees within 0.02 and scoop within ~1 dB, so trust those. fizz differs by 3-11 dB (htdemucs
loses the top), so judge fizz only against bs_roformer refs. Timing is noisy on sustained distortion (IQR up to 20 ms
and 27-50% "off by >10 ms" between two stems of identical timing): compare it against that floor, never alone.

--strokes (19 Nov, from chirper-zero's bench on Extreme and Mean v23): a song we wrote has no record to pair its notes
with, but its strokes can be read by the same measures and set beside what six records' guitar stems read at their own
chugs (tools/riffpunch-records.json: their medians, and the lowest and highest record). It renders the song's guitar
tracks solo over the window (--tracks to name the rig you are judging; without it, every track whose name or patch
says guitar, or whose resolved patch is a plucked string through an amp, less the bass) and prints ours, the records,
their range and the difference. What it found on the album: through a stroke the records' guitars carry 11.3 dB more
at 1-4 kHz than at 400 Hz-1 kHz (scoop_db -11.3; -12.7 to -6.5), and a `ct-twin` chug written at a full palm
(pm 1.0, which closes the string's filter to 1 kHz before the amp) read -4.4: no teeth. Nothing is scored: it is a
read. fizz_db is to be trusted only as far as the separator (see below). What the records CANNOT give: how empty the
rest after a stroke should be. A stroke "followed by a rest" in our transcriptions is not followed by a rest on the
records' guitar stems (-4 to 0 dB under the stroke on obZen, Pravus, Lethargica, This Spiteful Snake).
"""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import drumpunch as D  # noqa: E402
import likeness as L  # noqa: E402
import stemfile  # noqa: E402

SR = L.SR
GTR = re.compile(r"m8|guitar|gtr|emg|rig|chug|thrash|les-paul|fluence|bkp|obzen-l|obzen-r", re.I)
TOL = {"rise_ms": 2.0, "punch_db": 2.5, "tight_db": 3.0, "fizz_db": 3.0, "scoop_db": 3.0, "grain": 0.05}


def strung_and_amped(patch):
    """A resolved patch that is a plucked string through an amp: a guitar, whatever it is called (as stembal's)."""
    try:
        layers = [x.get("type") for x in patch["synth"]["layers"] if isinstance(x, dict)]
        fx = [x.get("type") if isinstance(x, dict) else str(x).split()[0] for x in patch.get("fx") or []]
    except (KeyError, TypeError, AttributeError):
        return False
    return "pluck" in layers and "amp" in fx


def guitar_events(song_file, names=None, by_chain=False):
    """Onset times (s) of the song's guitar notes, doubles merged; and the track names."""
    import chirpbin
    r = subprocess.run([chirpbin.resolve("chirp"), "plan", "-f", os.path.abspath(song_file), "--json"], capture_output=True,
                       text=True, cwd=os.path.dirname(os.path.abspath(song_file)))
    try:
        can = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"riffpunch: chirp plan failed for {song_file}: {r.stderr.strip()[-200:]}")
    return events_from(can, names, by_chain)


def events_from(can, names=None, by_chain=False):
    """guitar_events on a canonical plan. by_chain (only --strokes asks for it, so a reproduction's tracks and score are
    as they were): a track no name places is a guitar when its resolved patch is a plucked string through an amp; the
    album's rhythm rig is `ct-twin` on tracks called gl, gr, left, and no word in those says guitar."""
    to_s = D.beats_to_seconds(can.get("tempo"))
    patches = can.get("patches") if isinstance(can.get("patches"), dict) else {}
    times, tracks = [], []
    for t in can.get("tracks", []):
        p = t.get("patch")
        pname = p if isinstance(p, str) else ""
        nm = t.get("name") or ""
        if names is not None:
            if nm not in names:
                continue
        elif "bass" in nm.lower() or "bass" in pname.lower():
            continue
        elif not (GTR.search(pname) or GTR.search(nm)) and not (by_chain and strung_and_amped(patches.get(pname))):
            continue
        tracks.append(nm)
        times += [to_s(float(n["at"])) for n in t.get("notes") or [] if n.get("at") is not None]
    times = sorted(times)
    merged = []
    for x in times:                                   # doubled guitars hit together: one event
        if not merged or x - merged[-1] > 0.012:
            merged.append(x)
    return merged, tracks


def clean(ts, before=0.04, after=0.06):
    return [t for i, t in enumerate(ts) if (i == 0 or t - ts[i - 1] >= before) and (i + 1 == len(ts) or ts[i + 1] - t >= after)]


def flatness(seg):
    if len(seg) < 256:
        return 0.0
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 8192)) ** 2
    f = np.fft.rfftfreq(8192, 1 / SR)
    b = sp[(f >= 1000) & (f < 4000)] + 1e-20
    return float(np.exp(np.mean(np.log(b))) / np.mean(b))


def at_peak(yb, t, search=0.03):
    """The attack peak time (s) of band signal YB near T, or None."""
    i0, i1 = int(max(0, t - search) * SR), int(min(len(yb) / SR, t + search) * SR)
    if i1 - i0 < 96:
        return None
    tt, e = D.envelope(yb[i0:i1])
    return (tt[int(np.argmax(e))] + i0 / SR) if e.max() > 1e-5 else None


def measure_note(y, yb, t, nxt):
    m = D.measure(y, yb, t, nxt)
    if not m:
        return None
    s0 = int(t * SR)
    lo = D.bandpass(y[max(0, s0 - int(0.005 * SR)):s0 + int(0.09 * SR)], 100, 250)
    e = lambda a, b: float(np.sqrt(np.mean(lo[int(a * SR):int(b * SR)] ** 2)) + 1e-12)  # noqa: E731
    sus = y[s0 + int(0.02 * SR):s0 + int(min(0.12, max(0.04, nxt - t)) * SR)]
    mid = D.band_db(sus, 1000, 4000)
    return {"rise_ms": m["rise_ms"], "punch_db": m["punch_db"],
            "tight_db": 20 * np.log10(e(0.005, 0.025) / e(0.045, 0.085)) if len(lo) > int(0.085 * SR) else np.nan,
            "fizz_db": D.band_db(sus, 6000, 10000) - mid, "scoop_db": D.band_db(sus, 400, 1000) - mid, "grain": flatness(sus)}


def strokes_read(ours, ts, t0, t1):
    """--strokes: the medians of riffpunch's measures over the clean onsets of `ts` (seconds in the song) that fall in
    the window t0-t1, on `ours` (the window's audio, starting at t0). {"n": strokes read, "of": onsets in the window,
    "ours": {measure: median}}; a stroke in the window's first 30 ms or last 200 ms is not read."""
    y = D.mono(ours)
    yb = D.bandpass(y, 150, 8000)
    cl, rows, inside = set(clean(ts)), [], 0
    for i, t in enumerate(ts):
        if not t0 <= t < t1:
            continue
        inside += 1
        nxt = ts[i + 1] if i + 1 < len(ts) else t + 0.5
        if t in cl and 0.03 < t - t0 < (t1 - t0) - 0.2:
            m = measure_note(y, yb, t - t0, nxt - t0)
            if m:
                rows.append(m)
    med = {k: (round(float(np.nanmedian([r[k] for r in rows])), 3) if rows else None) for k in TOL}
    return {"n": len(rows), "of": inside, "ours": med}


def records_table(path=None):
    """{record id: {measure: its guitar stem's median, "n": onsets}} from tools/riffpunch-records.json."""
    with open(path or os.path.join(HERE, "riffpunch-records.json")) as f:
        return json.load(f)["records"]


def records_stats(recs):
    """{measure: (median, lowest, highest)} over the records."""
    return {k: (float(np.median([r[k] for r in recs.values()])), min(r[k] for r in recs.values()),
                max(r[k] for r in recs.values())) for k in TOL}


def strokes_lines(res, stats, nrec):
    row = lambda name, f: f"  {name:14s}" + "".join(f"{f(k):>14s}" for k in TOL)   # noqa: E731
    o = res["ours"]
    return [row("", lambda k: k),
            row("ours", lambda k: f"{o[k]:.2f}"),
            row("records", lambda k: f"{stats[k][0]:.2f}") + f"   (median of {nrec} records' guitar stems at their own chugs)",
            row("  low..high", lambda k: f"{stats[k][1]:.1f}..{stats[k][2]:.1f}"),
            row("ours - records", lambda k: f"{o[k] - stats[k][0]:+.2f}"),
            "  scoop_db is 400 Hz-1 kHz less 1-4 kHz through a stroke: MORE negative is more teeth. rise_ms and punch_db are "
            "the attack; tight_db the low end's fall; grain the noise between the harmonics. A read, not a score; fizz_db only "
            "as far as the separator. The records give no figure for the rest after a stroke."]


def compare(ref, ours, ts, shift):
    yr, yo = D.mono(ref), D.mono(ours)
    rb, ob = D.bandpass(yr, 150, 8000), D.bandpass(yo, 150, 8000)
    rows, offs = [], []
    for i, t in enumerate(ts):
        nxt = ts[i + 1] if i + 1 < len(ts) else t + 0.3
        if t < 0.05 or t > len(yo) / SR - 0.15:
            continue
        po, pr = at_peak(ob, t), at_peak(rb, t - shift)
        if po is None or pr is None:
            continue
        offs.append((pr + shift - po) * 1000)
        # both sides at the same moment: per-note attack peaks are not resolvable in sustained distortion (chirper-one:
        # a random pick in the +-30 ms window gives the same IQR), so no per-note re-alignment
        mo, mr = measure_note(yo, ob, t, nxt), measure_note(yr, rb, t - shift, nxt - shift)
        if mo and mr and not any(np.isnan(v) for v in (*mo.values(), *mr.values())):
            rows.append((mr, mo))
    if not rows:
        return {"total": None, "n": 0}
    med = lambda side, k: round(float(np.median([r[side][k] for r in rows])), 3)  # noqa: E731
    diffs = {k: round(float(np.median([r[1][k] - r[0][k] for r in rows])), 3) for k in TOL}
    score = float(100 * np.exp(-np.mean([abs(v) / TOL[k] for k, v in diffs.items()]) / 2))
    return {"total": round(score, 2), "n": len(rows), "ref": {k: med(0, k) for k in TOL}, "ours": {k: med(1, k) for k in TOL},
            "diff": diffs,
            "offset_ms": {"median": round(float(np.median(offs)), 1),
                          "iqr": round(float(np.subtract(*np.percentile(offs, [75, 25]))), 1),
                          "abs_over_10ms": round(float(np.mean(np.abs(np.array(offs) - np.median(offs)) > 10)), 2)}}


def ref_audio(song, stems):
    xs = []
    for part in stems.split("+"):
        # a WAV under either separator first (as before), else a packed stem (stemfile.py: the htdemucs_6s stems are Opus)
        p = stemfile.find(ROOT, song, part, ("bs_roformer_sw", "htdemucs_6s"))
        if p is None:
            raise SystemExit(f"riffpunch: no {part} stem for {song}")
        xs.append(stemfile.load(p))
    n = min(len(x) for x in xs)
    return sum(x[:n] for x in xs)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--song")
    ap.add_argument("--clip")
    ap.add_argument("--from", dest="t0", type=float)
    ap.add_argument("--to", dest="t1", type=float)
    ap.add_argument("--song-file")
    ap.add_argument("--tracks")
    ap.add_argument("--set", action="append", default=[])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--stems", default="guitar")
    ap.add_argument("--ours")
    ap.add_argument("--max-lag", type=float, default=20.0, help="global lag search, +-ms (default 20: songs are map-aligned; "
                    "a wider search found -100 ms on Pineal, chirper-one)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strokes", action="store_true", help="an original song's strokes beside the records' (no pairing, no score)")
    a = ap.parse_args(argv)
    song, t0, t1 = a.song, a.t0, a.t1
    if a.strokes:
        song_file = a.song_file or (os.path.join(ROOT, "songs", f"{song}.yaml") if song else None)
        if not song_file or t1 is None:
            raise SystemExit("riffpunch --strokes: --song-file F (or --song ID) and --from S --to S (seconds)")
        t0 = t0 or 0.0
        ts, tracks = guitar_events(song_file, a.tracks.split(",") if a.tracks else None, by_chain=True)
        if not tracks:
            raise SystemExit("riffpunch: no guitar tracks found; pass --tracks")
        ours_x = L.load(a.ours) if a.ours else D.render_ours(song_file, t0, t1, tracks, a.seed, a.set)
        res = strokes_read(ours_x, ts, t0, t1)
        if not res["n"]:
            raise SystemExit(f"riffpunch --strokes: no clean stroke of {','.join(tracks)} in {t0:g}-{t1:g} s ({res['of']} onsets)")
        recs = records_table()
        stats = records_stats(recs)
        res.update(label=f"{os.path.basename(song_file)} {t0:g}-{t1:g} s", tracks=tracks,
                   records={k: round(v[0], 3) for k, v in stats.items()}, low={k: v[1] for k, v in stats.items()},
                   high={k: v[2] for k, v in stats.items()})
        if a.json:
            print(json.dumps(res))
            return
        print(f"riffpunch strokes {res['label']} (tracks {','.join(tracks)}): {res['n']} clean strokes read of {res['of']} onsets")
        print("\n".join(strokes_lines(res, stats, len(recs))))
        return
    if a.clip:
        cl = next((c for c in json.load(open(os.path.join(ROOT, "micro", "clips.json")))["clips"] if c["id"] == a.clip), None)
        if not cl:
            raise SystemExit(f"riffpunch: no clip {a.clip}")
        song, t0, t1 = cl["song"], cl["from"], cl["to"]
    if not song:
        raise SystemExit("riffpunch: --song ID or --clip ID")
    song_file = a.song_file or os.path.join(ROOT, "songs", f"{song}.yaml")
    ts, tracks = guitar_events(song_file, a.tracks.split(",") if a.tracks else None)
    if not tracks:
        raise SystemExit("riffpunch: no guitar tracks found; pass --tracks")
    full = ref_audio(song, a.stems)
    t0 = t0 or 0.0
    t1 = t1 or len(full) / SR
    ref_x = full[int(t0 * SR):int(t1 * SR)]
    ours_x = L.load(a.ours) if a.ours else D.render_ours(song_file, t0, t1, tracks, a.seed, a.set)
    cts = [t - t0 for t in clean(ts) if t0 <= t < t1]
    shift = D.lag(D.bandpass(D.mono(ref_x), 150, 8000), D.bandpass(D.mono(ours_x), 150, 8000), max_s=a.max_lag / 1000)
    res = compare(ref_x, ours_x, cts, shift)
    res.update(label=f"{song} {t0:g}-{t1:g} s", tracks=tracks, lag_ms=round(shift * 1000, 1), stems=a.stems)
    if a.json:
        print(json.dumps(res))
        return
    print(f"riffpunch {res['label']} (tracks {','.join(tracks)}; stems {a.stems}; global lag {res['lag_ms']} ms): "
          f"total {res['total']} over {res['n']} clean onsets")
    if res.get("offset_ms"):
        o = res["offset_ms"]
        print(f"  timing: record vs ours median {o['median']:+.1f} ms, IQR {o['iqr']:.1f} ms, "
              f"{o['abs_over_10ms'] * 100:.0f}% off by >10 ms  (random peaks in the +-30 ms window: IQR 30, 67%: "
              f"at or near that, the stem's attacks are unresolvable, not our timing)")
    if res.get("diff"):
        print("  " + "  ".join(f"{k} {res['ref'][k]:.2f}->{res['ours'][k]:.2f}" for k in TOL))


if __name__ == "__main__":
    main()
