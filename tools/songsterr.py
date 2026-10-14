#!/usr/bin/env python3
"""Songsterr tab → explicit chirp score notation (one line per measure, durations exact in beats).

  songsterr.py SONG_ID [TRACK…]        fetch the tab's meta + tracks (cached under ref/), print scores
  songsterr.py --cached DIR [TRACK…]   use already-fetched DIR/songsterr-N.json files

Pitched tracks: note = string tuning + fret; ties merge into the previous note; dynamics (ppp…fff)
become velocities; palm mute → ^pm, dead → ^dead, harmonics → ^ph; slides into a note become a
short bend from 2 semitones below, slides out a bend down at the end. Drums: General MIDI numbers →
metal-kit pieces. Output is plain notation to paste into a song — the tab is a transcription aid,
not a runtime dependency."""
import gzip
import json
import os
import sys
import urllib.request

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
VEL = {"ppp": 40, "pp": 52, "p": 64, "mp": 76, "mf": 88, "f": 100, "ff": 112, "fff": 124}
GM = {35: "k", 36: "k", 37: "rc", 38: "s", 39: "cp", 40: "s", 41: "ft", 42: "h1", 43: "ft", 44: "hf", 45: "t3", 46: "oh",
      47: "t2", 48: "t1", 49: "c", 50: "t1", 51: "rd", 52: "cch", 53: "rbs", 55: "spl", 56: "cow", 57: "c2", 59: "rd"}
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
    if b.get("tuplet"):
        t *= {3: 2 / 3, 5: 4 / 5, 6: 4 / 6, 7: 4 / 7}.get(b["tuplet"], 1)
    return t


def fmt_len(t):
    s = f"{t:.4f}".rstrip("0").rstrip(".")
    return f"/{s}b"


def measure_tokens(track, m, drums):
    out = []  # list of [token_body, beats, suffix]
    vel = None
    for b in m["voices"][0]["beats"]:
        t = beats_of(b)
        if b.get("velocity"):
            vel = VEL.get(b["velocity"], vel)
        notes = [n for n in b.get("notes", []) if not n.get("rest")]
        if not notes or b.get("rest"):
            out.append(["R", t, ""]); continue
        if drums:
            pcs = sorted({GM.get(int(n["fret"]), f"m{int(n['fret'])}") for n in notes})
            acc = any(n.get("accentuated") for n in notes)
            v = min(127, (vel or 100) + (12 if acc else 0))
            out.append([",".join(pcs), t, f"@{v}"]); continue
        tun = track["tuning"]
        if all(n.get("tie") for n in notes) and out and out[-1][0] != "R":
            out[-1][1] += t  # tie: extend the previous note
            if any(n.get("slide") in ("downwards", "outDownwards", "shift") for n in notes):
                out[-1][2] += "^slidedown"
            continue
        pitches = sorted(tun[int(n["string"])] + int(n["fret"]) for n in notes)
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
        out.append([",".join(nm(p) for p in pitches), t, v + arts])
    toks = []
    for body, t, suf in out:
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
    return " ".join(toks)


def score(cache, i):
    tr = load(cache, i)
    drums = not tr.get("tuning")
    lines = [measure_tokens(tr, m, drums) for m in tr["measures"]]
    return tr.get("name") or tr.get("instrument"), drums, lines


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--cached":
        cache = args[1]; args = args[2:]
    else:
        cache = os.path.expanduser("~/.config/chirp/ref"); fetch(args[0], cache); args = args[1:]
    meta = json.load(open(f"{cache}/songsterr-meta.json"))
    idx = [int(a) for a in args] or list(range(len(meta.get("tracks", []))))
    for i in idx:
        name, drums, lines = score(cache, i)
        print(f"# track {i}: {name}{' (drums → metal-kit)' if drums else ''}")
        for mi, l in enumerate(lines):
            print(f"m{mi + 1:<3d} {l}")
