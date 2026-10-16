#!/usr/bin/env python3
"""Hats (or any missing high percussion) from the drum stem: the record's onsets in a band that NO existing drum hit
of the song covers become a new track — the hats/shaker/ride taps a drum transcription left out. Saturnine +1.95
held-out (874 uncovered 6-12 kHz onsets on tight-kit h at -6 dB, kept between the intro and the ending).

  stemhats.py SONG.yaml DRUM_STEM.wav OUT.yaml [--band 6000-12000] [--k 1.5] [--cover 0.03] [--gap 0.06]
              [--piece h] [--patch PATCH] [--gain -6dB] [--name drums-hats] [--tracks REGEX] [--from S] [--to S]
              [--vel 15-90] [--len 0.125] [--map MAP.json --raw tools/maps/SONG-hats.json]

Onsets: spectral flux of the band (log magnitude, hop 256), local maxima within +-30 ms above median + K * std of a
2 s neighbourhood, at least --gap s apart. Covered: within --cover s of any note start of the tracks whose name
matches --tracks (default drum|kit|perc|hat|cym|tom|snare|kick). Velocity from the band level around its median
(2 per dB, clipped to --vel). --from/--to keep hits only inside that time range (the intro/ending may not want them).
The new one-line track goes after the last matching track; its patch (first word) and sends come from the matching
track that already plays --piece most, else the first kit-like one (piece names, not pitches) — a pitched
'low-perc' on modal-tom cannot play `h` (chirper-two's Daydreaming catch); --patch overrides.
Tempo: a number or a tempo map (`tempo: [{at, bpm}, ...]`, as tab2song writes) — times go through it both ways.
Map-built songs (tab2song): pass --map MAP.json --raw RAW.json — the hats go into RAW.json (key "hats") and OUT is
a copy of the map with a part {"name", "raw": "RAW.json#hats", "patch", "gain", "extra": {"sends"}} appended;
regenerate the song with tab2song. Measure on held-out seeds and try --gain -12dB / 0dB."""
import re
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import likeness as L  # noqa: E402
import drumtrans as D  # noqa: E402


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    song, stem, out_path = a[:3]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    b0, b1 = (float(v) for v in opt("--band", "6000-12000").split("-"))
    K, cover, gap = opt("--k", 1.5), opt("--cover", 0.03), opt("--gap", 0.06)
    v0, v1 = (int(v) for v in opt("--vel", "15-90").split("-"))
    t_from, t_to = opt("--from", 0.0), opt("--to", 1e9)
    rx = re.compile(opt("--tracks", r"drum|kit|perc|hat|cym|tom|snare|kick"))
    y = open(song).read()
    pts = D.tempo_points(song); t2b = D.time_to_beat(pts)
    pb = np.array([b for b, _ in pts]); pv = np.array([v for _, v in pts])
    psec = np.concatenate([[0.0], np.cumsum(np.diff(pb) * 60 / pv[:-1])])
    def b2t(b):
        i = max(0, np.searchsorted(pb, b, side="right") - 1)
        return psec[i] + (b - pb[i]) * 60 / pv[i]
    x = L.load(stem).mean(1); sr = 48000
    hop, n = 256, 1024
    fr = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * np.hanning(n)
    F = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(n, 1 / sr); band = (f > b0) & (f < b1)
    E = np.log(F[:, band] + 1e-6)
    flux = np.concatenate([[0], np.maximum(np.diff(E, axis=0), 0).sum(1)])
    lvl = 10 * np.log10((F[:, band] ** 2).sum(1) + 1e-12)
    t = np.arange(len(flux)) * hop / sr + n / 2 / sr
    w = int(0.03 * sr / hop); k = int(1.0 * sr / hop); on = []
    for i in range(w, len(flux) - w):
        if flux[i] == flux[i - w:i + w + 1].max():
            loc = flux[max(0, i - k):i + k]
            if flux[i] > np.median(loc) + K * loc.std() and (not on or t[i] - on[-1][0] > gap):
                on.append((t[i], lvl[i]))
    hits, last, src, src_n, kitlike = [], None, None, 0, None
    piece = opt("--piece", "h")
    note = re.compile(r"^[A-Ga-g][#b]?-?\d+$")
    for m in re.finditer(r'^\s*- \{name: "?([^",]+)"?,[^\n]*?score: "([^"]*)"', y, re.M):
        if not rx.search(m.group(1)):
            continue
        last = m
        pos, n_piece, n_notes, n_hits = 0.0, 0, 0, 0
        for tk in m.group(2).split():
            mm = re.match(r"^([^/]+)/([0-9.]+)b", tk)
            if not mm:
                continue
            if mm.group(1) not in ("R", "r", "_"):
                hits.append(b2t(pos)); n_hits += 1
                heads = mm.group(1).split(",")
                n_piece += piece in heads; n_notes += any(note.match(h) for h in heads)
            pos += float(mm.group(2))
        if n_piece > src_n:   # the patch/sends come from a track that already plays --piece
            src, src_n = m, n_piece
        if kitlike is None and n_hits and n_notes < 0.5 * n_hits:   # else a kit (pieces, not pitches)
            kitlike = m
    if last is None:
        sys.exit("no drum tracks matched --tracks")
    src = src or kitlike
    if src is None and "--patch" not in a:
        sys.exit(f"no drum track plays '{piece}' or looks like a kit (pitched tracks only): pass --patch KIT")
    hits = np.sort(np.array(hits))
    keep = [(s, l) for s, l in on if t_from <= s < t_to and (hits.size == 0 or np.min(np.abs(hits - s)) > cover)]
    print(f"{len(on)} band onsets, {len(keep)} uncovered{' in range' if '--from' in a or '--to' in a else ''}")
    if not keep:
        sys.exit("nothing to add")
    med = float(np.median([l for _, l in keep])); ln = opt("--len", 0.125)
    toks, cur = [], 0.0
    for s, l in keep:
        b = float(t2b(s))
        if b > cur + 1e-3:
            toks.append(f"R/{b - cur:.4f}b"); cur = b
        toks.append(f"{opt('--piece', 'h')}/{ln:g}b@{int(np.clip((v0 + v1) / 2 + 2.0 * (l - med), v0, v1))}"); cur += ln
    line = (src or last).group(0)   # patch and sends from the source track; the new track goes after the last one
    patch = opt("--patch", "") or (re.search(r'patch: "([^"]*)"', line) or re.search(r"patch: ([^,}]+)", line)).group(1)
    sends = re.search(r"sends: (\{[^}]*\})", line)
    indent = re.match(r"^(\s*)", line).group(1)
    new = (f'{indent}- {{name: "{opt("--name", "drums-hats")}", patch: "{patch.split()[0] if "--patch" not in a else patch}", '
           f'gain: "{opt("--gain", "-6dB")}"' + (f", sends: {sends.group(1)}" if sends else "") + f', score: "{" ".join(toks)}"}}')
    if "--map" in a:   # a tab2song map: the hats as a raw part
        import json, os
        raw = opt("--raw", "")
        if not raw:
            sys.exit("--map needs --raw RAW.json (relative to the config root, e.g. tools/maps/SONG-hats.json)")
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json.dump({"hats": {"score": " ".join(toks)}}, open(raw if os.path.isabs(raw) else os.path.join(root, raw), "w"))
        mraw = open(opt("--map", "")).read(); mp = json.loads(mraw)
        part = {"name": opt("--name", "drums-hats"), "raw": f"{raw}#hats",
                "patch": patch.split()[0] if "--patch" not in a else patch, "gain": opt("--gain", "-6dB")}
        if sends:
            part["extra"] = {"sends": json.loads(sends.group(1))}
        mp["parts"].append(part)
        ind = (len(mraw.splitlines()[1]) - len(mraw.splitlines()[1].lstrip())) if mraw.count("\n") > 1 else 2
        open(out_path, "w").write(json.dumps(mp, indent=ind or 2, ensure_ascii=False) + "\n")
        print(f"raw {raw} ({len(keep)} hits); map part appended -> {out_path} (regenerate with tab2song.py)")
        return
    j = y.index("\n", last.end()) + 1 if "\n" in y[last.end():] else len(y)
    open(out_path, "w").write(y[:j] + new + "\n" + y[j:])
    print(f"added {opt('--name', 'drums-hats')} ({len(keep)} hits) -> {out_path}")


if __name__ == "__main__":
    main()
