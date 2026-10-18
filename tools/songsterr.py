#!/usr/bin/env python3
"""Songsterr tab → explicit chirp score notation (one line per measure, durations exact in beats).

  songsterr.py SONG_ID [TRACK…]        fetch the tab's meta + tracks (cached under ref/songsterr-SONG_ID/), print scores
  songsterr.py --cached DIR [TRACK…]   use already-fetched DIR/songsterr-N.json files
  … [--bends peak|curve|mean] [--bend-step 0.125]   how a bent note's curve becomes bend= (see below)
  … [--voice N]                        read the tab's Nth voice (default 0, the first; see below)
  … [--gm-map 39=cp,…]                 drums: General-MIDI note -> piece overrides, applied before a beat's pieces
                                       merge (see below)

Pitched tracks: note = string tuning + fret; ties merge into the previous note; dynamics (ppp…fff)
become velocities; palm mute → ^pm, dead → ^dead, harmonics → ^ph; slides into a note become a
short bend from 2 semitones below, slides out a bend down at the end. Drums: General MIDI numbers →
metal-kit pieces. Output is plain notation to paste into a song — the tab is a transcription aid,
not a runtime dependency.

Bends (a tab note's curve: points of (position 0-60 across the note, tone 25 = one semitone)):
  peak   one bend= for the whole note, read at the curve's middle — a bend-and-release (0 -> 3 -> 0) holds its
         peak throughout (the default: every existing song was built this way)
  curve  the curve itself: stepped bend= over holds every ~--bend-step beats, each step at the curve's mean over
         it (a tied continuation carries its own curve on); the time-averaged pitch follows the record (bd-954470)
  mean   one bend= at the curve's time-average
tab2song maps choose per part or map-wide ("bends", "bend_step").

Voices: a staff can carry independent voices (e.g. a drum tab's cymbals in voice 0, kick and snare in voice 1). One
voice is read — voice 0 unless chosen (`--voice N`, a tab2song part's "voice": N; bd-72f61a); voices are never
merged. A measure without the chosen voice is a rest of the bar's length (its time signature), never another voice.

Drum pieces: each General-MIDI note maps to a metal-kit piece (GM below), and a beat's pieces merge — a clap (39) and a
snare (38) struck together are one `s`. `--gm-map 39=cp` (a tab2song part's or map's "gm_map": {"39": "cp"}; bd-a725c6)
overrides notes BEFORE that merge, so they stay distinct (`cp,s`); tab2song's per-part remap/drop still apply after.
Overrides must be MIDI 0..127 -> a piece name ([a-z][a-z0-9]*); the target kit has to define the piece."""
import gzip
import json
import os
import sys
import urllib.request

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
VEL = {"ppp": 40, "pp": 52, "p": 64, "mp": 76, "mf": 88, "f": 100, "ff": 112, "fff": 124}
GM = {35: "k", 36: "k", 37: "rc", 38: "s", 39: "s", 40: "s", 41: "ft", 42: "h1", 43: "ft", 44: "hf", 45: "t3", 46: "oh",
      47: "t2", 48: "t1", 49: "c", 50: "t1", 51: "rd", 52: "x", 53: "rbs", 55: "sp", 56: "cow", 57: "c", 59: "rd"}
UA = {"User-Agent": "Mozilla/5.0"}


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def fetch(song_id, cache):
    os.makedirs(cache, exist_ok=True)
    meta = json.load(urllib.request.urlopen(urllib.request.Request(f"https://www.songsterr.com/api/meta/{song_id}", headers=UA)))
    json.dump(meta, open(f"{cache}/songsterr-meta.json", "w"))
    for i in range(len(meta.get("tracks", []))):
        url = f"https://dqsljvtekg760.cloudfront.net/{song_id}/{meta['revisionId']}/{meta['image']}/{i}.json"
        raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()
        open(f"{cache}/songsterr-{i}.json", "wb").write(raw)
    return meta


def load(cache, i):
    raw = open(f"{cache}/songsterr-{i}.json", "rb").read()
    try:
        return json.loads(gzip.decompress(raw))
    except OSError:
        return json.loads(raw)


def beats_of(b):
    n, d = b.get("duration", [1, 4])
    t = 4 * n / d
    # Songsterr usually stores tuplets already reduced ([1, 24] = a sixteenth triplet); scale only
    # durations that are still plain note values (power-of-two denominators).
    if b.get("tuplet") and d & (d - 1) == 0:
        t *= {3: 2 / 3, 5: 4 / 5, 6: 4 / 6, 7: 4 / 7}.get(b["tuplet"], 1)
    return t


def fmt_len(t):
    s = f"{t:.4f}".rstrip("0").rstrip(".")
    return f"/{s}b"


def fmt_num(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def gm_map_of(spec):
    """{GM note: piece} from {"39": "cp"} or "39=cp,40=s"; None for none. Raises ValueError on a bad entry."""
    import re
    if spec is None or spec == {} or spec == "":
        return None
    items = spec.items() if isinstance(spec, dict) else (kv.partition("=")[::2] for kv in str(spec).split(","))
    out = {}
    for k, v in items:
        try:
            note = int(str(k).strip())
        except ValueError:
            raise ValueError(f"gm_map: {k!r} is not a General-MIDI note number") from None
        if not 0 <= note <= 127:
            raise ValueError(f"gm_map: note {note} is outside 0..127")
        if not isinstance(v, str) or not re.fullmatch(r"[a-z][a-z0-9]*", v.strip()):
            raise ValueError(f"gm_map: {note} -> {v!r} is not a piece name ([a-z][a-z0-9]*)")
        out[note] = v.strip()
    return out


def measure_tokens(track, m, drums, bends="peak", step=0.125, voice=0, bar_beats=4.0, gm_map=None):
    voices = m.get("voices") or []
    if voice >= len(voices):   # the chosen voice is absent here: the bar rests (bd-72f61a)
        return f"R{fmt_len(bar_beats)}"
    out = []  # list of [token_body, beats, suffix, bend]: bend semitones, or {"pieces": [(curve|None, beats)]}
    vel = None
    for b in voices[voice]["beats"]:
        t = beats_of(b)
        if b.get("velocity"):
            vel = VEL.get(b["velocity"], vel)
        notes = [n for n in b.get("notes", []) if not n.get("rest")]
        if not notes or b.get("rest"):
            out.append(["R", t, ""]); continue
        if drums:
            gm = {**GM, **gm_map} if gm_map else GM   # overrides map before the beat's pieces merge (bd-a725c6)
            pcs = sorted({gm.get(int(n["fret"]), f"m{int(n['fret'])}") for n in notes})
            acc = any(n.get("accentuated") for n in notes)
            v = min(127, (vel or 100) + (12 if acc else 0))
            out.append([",".join(pcs), t, f"@{v}"]); continue
        tun = track["tuning"]
        if all(n.get("tie") for n in notes) and out and out[-1][0] != "R":
            if bends == "curve" and len(out[-1]) > 3:   # the tied part bends on (its own curve, or holds)
                tie_pts = widest_curve(notes)
                prev = out[-1][3]
                if tie_pts or isinstance(prev, dict):
                    if not isinstance(prev, dict):
                        prev = out[-1][3] = {"pieces": [([(0, prev)], out[-1][1])]}
                    prev["pieces"].append((tie_pts, t))
            out[-1][1] += t  # tie: extend the previous note
            if any(n.get("slide") in ("downwards", "outDownwards", "shift") for n in notes):
                out[-1][2] += "^slidedown"
            continue
        pitches = sorted(tun[int(n["string"])] + int(n["fret"]) for n in notes if "fret" in n)
        if not pitches:  # only fretless notes (e.g. a dead/ghost note without a fret): a rest of that length
            out.append(["R", t, ""]); continue
        if bends == "peak":
            bend = max((bend_semis(n) for n in notes), key=abs, default=0.0)
        else:   # a chord follows its widest curve (one bend per track)
            pts = widest_curve(notes)
            if pts is None:
                bend = 0.0
            elif bends == "mean":
                bend = round(curve_mean(pts), 2)
            else:
                bend = {"pieces": [(pts, t)]}
        arts = ""
        if b.get("palmMute") or any(n.get("palmMute") for n in notes):
            arts += "^pm"
        if any(n.get("dead") for n in notes):
            arts += "^dead"
        if any(n.get("harmonic") for n in notes):
            arts += "^ph"
        if any(n.get("slide") == "below" for n in notes):
            arts += "^slidein"
        if any(n.get("slide") in ("downwards", "outDownwards") for n in notes):
            arts += "^slidedown"
        v = f"@{vel}" if vel else ""
        out.append([",".join(nm(p) for p in pitches), t, v + arts, bend])
    toks = []
    state = 0.0   # the track's current bend (semitones): a bend= token holds until the next one
    for item in out:
        body, t, suf = item[:3]
        bend = item[3] if len(item) > 3 else 0.0
        if isinstance(bend, dict):
            segs = curve_segments(bend["pieces"], step)
            if any(abs(v) > 1e-6 for _, v in segs):
                # the curve: the note at its first step's bend, then holds at each next step's
                suf = suf.replace("^slidein", "").replace("^slidedown", "")
                parts, done = [], 0.0
                for k, (ln, v) in enumerate(segs):
                    ln = round(t - done, 4) if k == len(segs) - 1 else round(ln, 4)
                    done += ln
                    if abs(v - state) > 1e-6:
                        parts.append(f"bend={fmt_num(v)}" if abs(v) > 1e-6 else "bend=")
                        state = v
                    parts.append(f"{body}{fmt_len(ln)}{suf}" if k == 0 else f"_{fmt_len(ln)}")
                toks.append(" ".join(parts))
                continue
            bend = 0.0
        if body != "R" and abs(bend - state) > 1e-6:
            toks.append(f"bend={fmt_num(bend)}" if abs(bend) > 1e-6 else "bend=")
            state = bend
        # slides become stepped bends across short holds (bends act on the holds that follow them):
        # in = from 2 semitones below over the first 1/8 beat; out = falling 2 then 5 over the last 1/4
        sin, sout = "^slidein" in suf, "^slidedown" in suf
        suf = suf.replace("^slidein", "").replace("^slidedown", "")
        if not (sin or sout) or t <= 0.5:
            toks.append(f"{body}{fmt_len(t)}{suf}"); continue
        parts = []
        core = t
        if sin:
            parts.append(f"bend=-2 {body}{fmt_len(0.125)}{suf} bend=")
            core -= 0.125
        if sout:
            core -= 0.25
        if sin:
            if core > 0:
                parts.append(f"_{fmt_len(core)}")
        else:
            parts.append(f"{body}{fmt_len(core)}{suf}")
        if sout:
            parts.append("bend=-2 _/0.125b bend=-5 _/0.125b bend=")
        toks.append(" ".join(parts))
        state = 0.0   # the slide's stepped bends end reset
    if abs(state) > 1e-6:
        toks.append("bend=")
    return " ".join(toks)


def bend_curve(n):
    """A bent note's curve as [(position 0-60, semitones)], or None."""
    b = n.get("bend")
    if not b:
        return None
    return sorted((p.get("position", 0), p.get("tone", 0) / 25.0) for p in b.get("points", [])) \
        or [(0, b.get("tone", 0) / 25.0)]


def widest_curve(notes):
    """The curve of the most-bent note (a chord bends as one), or None."""
    curves = [c for c in (bend_curve(n) for n in notes) if c]
    return max(curves, key=lambda c: max(abs(v) for _, v in c)) if curves else None


def curve_at(pts, pos):
    if pos <= pts[0][0]:
        return pts[0][1]
    for (p0, v0), (p1, v1) in zip(pts, pts[1:]):
        if p0 <= pos <= p1:
            return v0 + (v1 - v0) * ((pos - p0) / (p1 - p0) if p1 > p0 else 0)
    return pts[-1][1]


def curve_mean(pts, a=0.0, b=60.0, n=24):
    """The curve's mean (semitones) over positions a..b."""
    return sum(curve_at(pts, a + (b - a) * (i + 0.5) / n) for i in range(n)) / n


def curve_segments(pieces, step):
    """[(curve or None, beats)] → [(beats, semitones)]: each piece in ~step-beat steps at the curve's mean over the
    step (None holds the last value), equal neighbours merged."""
    out, last = [], 0.0
    for pts, beats in pieces:
        if pts is None:
            vals = [(beats, last)]
        else:
            k = max(1, int(round(beats / step)))
            vals = [(beats / k, round(curve_mean(pts, 60 * i / k, 60 * (i + 1) / k), 2)) for i in range(k)]
        for ln, v in vals:
            if out and abs(out[-1][1] - v) < 1e-9:
                out[-1][0] += ln
            else:
                out.append([ln, v])
            last = v
    return [(ln, v) for ln, v in out]


def bend_semis(n):
    """A bent note's pitch offset in semitones, read at the middle of its bend curve (Songsterr `tone` 25 =
    one semitone: Bleed's B25/B50 pedal bends sound E/F over the open D#, as the stems confirm). Notes
    bending through a transition (0 → 25) take the value they mostly sound at."""
    b = n.get("bend")
    if not b:
        return 0.0
    pts = sorted((p.get("position", 0), p.get("tone", 0)) for p in b.get("points", [])) or [(0, b.get("tone", 0))]
    mid = 30
    for (p0, v0), (p1, v1) in zip(pts, pts[1:]):
        if p0 <= mid <= p1:
            tone = v0 + (v1 - v0) * ((mid - p0) / (p1 - p0) if p1 > p0 else 0)
            break
    else:
        tone = pts[-1][1] if mid >= pts[-1][0] else pts[0][1]
    return round(tone / 25.0, 2)


def score(cache, i, bends="peak", step=0.125, voice=0, gm_map=None):
    tr = load(cache, i)
    drums = not tr.get("tuning")
    lines, sig = [], [4, 4]
    for m in tr["measures"]:
        sig = m.get("signature", sig)   # as tabtime.timeline: a signature holds until the next one
        lines.append(measure_tokens(tr, m, drums, bends, step, voice, 4 * sig[0] / sig[1], gm_map))
    return tr.get("name") or tr.get("instrument"), drums, lines


if __name__ == "__main__":
    args = sys.argv[1:]
    bends, step, voice, gm_map = "peak", 0.125, 0, None
    if "--bends" in args:
        i = args.index("--bends"); bends = args[i + 1]; del args[i:i + 2]
    if "--bend-step" in args:
        i = args.index("--bend-step"); step = float(args[i + 1]); del args[i:i + 2]
    if "--voice" in args:
        i = args.index("--voice"); voice = int(args[i + 1]); del args[i:i + 2]
    if "--gm-map" in args:
        i = args.index("--gm-map")
        try:
            gm_map = gm_map_of(args[i + 1])
        except ValueError as e:
            sys.exit(f"songsterr: {e}")
        del args[i:i + 2]
    if args and args[0] == "--cached":
        cache = args[1]; args = args[2:]
    else:
        cache = os.path.expanduser(f"~/.config/chirp/ref/songsterr-{args[0]}"); fetch(args[0], cache); args = args[1:]
    meta = json.load(open(f"{cache}/songsterr-meta.json"))
    idx = [int(a) for a in args] or list(range(len(meta.get("tracks", []))))
    for i in idx:
        name, drums, lines = score(cache, i, bends, step, voice, gm_map)
        print(f"# track {i}: {name}{' (drums → metal-kit)' if drums else ''}{f' voice {voice}' if voice else ''}")
        for mi, l in enumerate(lines):
            print(f"m{mi + 1:<3d} {l}")
