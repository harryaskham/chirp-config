#!/usr/bin/env python3
"""wordread: can a sung or barked voice's words be read? A speech recogniser as the ear for words, with its control.

  wordread.py read VOICE.wav [VOICE.wav ...] --lyric "the words" | --lyric-file FILE [--models small.en,base.en] [--json]
      Each VOICE.wav is the voice ALONE (`chirp render --solo TRACK --set loudness=null`). It is brought to a standard
      loudness and recognised (tools/asr.py --norm, confined to its own CPUs). Per file and model: how many of the
      lyric's words were written, in order, and how many DIFFERENT words were written at all (a recogniser that loops
      one made-up sentence over a scream writes few), then what it wrote.
  wordread.py control ID[:START] ... [--model small.en] [--secs 53] [--json]
      THE CONTROL, on reference records: the record's vocal stem alone and the whole record over the same seconds (the
      --secs where the stem is busiest, or from START), each recognised; how many of the words written for the stem
      are also written, in order, for the record. It prints counts only, never the records' words.

Why both (chirper-zero, Common Time v17-v18, whose barktest.py and refread.py these are, made general):
  * It decides things a measurement cannot: a choir's "now" was heard as "no", the opposite word, three seeds in
    three; a spoken line read 9 words of 10 alone and 7 in the mix only with the band ducked under it.
  * A harsh voice is judged ALONE. In a full mix the recogniser read none of our bark; on five records it read 0, 9,
    12, 14 and 24 of the 49-65 words it read from their own vocal stems. So a mix reading of zero is no fault, and
    `control` gives the number to hold ours against.
  * small.en is the judge, not base.en: base.en gave 5 and 18 words of 35 for one scream at two levels 0.5 dB apart.
  * The stem's "words" are what the recogniser wrote, not checked against the record's lyric.
Tone and level against records' voices: tools/voxref.py. (chirp-eco, 13 Nov; tests: tools/tests/test_wordread.py.)"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import stemfile  # noqa: E402

ENV = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}


def words(text):
    return re.findall(r"[a-z']+", text.lower())


def in_order(want, got):
    """How many of `want`'s words appear in `got`, in order (the longest matching blocks, as difflib finds them)."""
    return sum(b.size for b in difflib.SequenceMatcher(None, want, got, autojunk=False).get_matching_blocks())


def recognise(path, model, t0=None, t1=None):
    """What the recogniser wrote for path (or its [t0, t1] seconds), loudness-normalised first."""
    with tempfile.TemporaryDirectory(prefix="wordread-") as d:
        out = os.path.join(d, "r.json")
        cmd = [sys.executable, os.path.join(HERE, "asr.py"), path, "--model", model, "--norm", "-o", out]
        if t0 is not None:
            cmd += ["--from", str(t0), "--to", str(t1)]
        r = subprocess.run(cmd, capture_output=True, text=True, env=ENV, stdin=subprocess.DEVNULL)
        if r.returncode or not os.path.exists(out):
            sys.exit(f"wordread: asr.py failed on {path}: {(r.stderr or r.stdout)[-300:]}")
        with open(out) as f:
            res = json.load(f)
    return res.get("text") or " ".join(s.get("text", "") for s in res.get("segments", []))


def busiest(path, secs):
    """The start (whole seconds) of the `secs` seconds where the file carries most energy."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", path, "-ar", "4000", "-ac", "1", "-f", "f32le", "-"],
                       capture_output=True, env=ENV)
    v = np.frombuffer(r.stdout, "<f4").astype(float)
    if len(v) < 4000:
        sys.exit(f"wordread: {path} could not be read")
    e = np.add.reduceat(v ** 2, np.arange(0, len(v), 4000))
    n = int(min(secs, len(e)))
    return float(np.argmax(np.convolve(e, np.ones(n), "valid")))


def record_file(rid):
    for ext in (".wav", ".flac", ".opus", ".ogg", ".m4a", ".mp3"):
        p = os.path.join(ROOT, "ref", rid + ext)
        if os.path.isfile(p):
            return p
    return None


def cmd_read(a):
    if a.lyric_file:
        with open(a.lyric_file) as f:
            lyric = words(f.read())
    else:
        lyric = words(a.lyric or "")
    if not lyric:
        sys.exit("wordread: give the words: --lyric \"...\" or --lyric-file FILE")
    models = a.models.split(",")
    rows = []
    for path in a.wavs:
        if not os.path.isfile(path):
            sys.exit(f"wordread: no file {path}")
        row = {"file": path, "lyric_words": len(lyric), "models": {}}
        for m in models:
            text = recognise(path, m)
            ws = words(text)
            row["models"][m] = {"read": in_order(lyric, ws), "different": len(set(ws)), "wrote": text.strip()}
        rows.append(row)
    if a.json:
        print(json.dumps(rows, ensure_ascii=False))
        return
    print(f"{'the voice alone':28s}" + "".join(f"  {m + ': read / of / different':>34s}" for m in models))
    for row in rows:
        name = os.path.basename(row["file"])
        print(f"{name[:27]:28s}" + "".join(f"  {r['read']:>22d} / {len(lyric):2d} / {r['different']:3d}" for r in row["models"].values()))
        for m, r in row["models"].items():
            print(f"      {m}: {r['wrote'][:230]}")


def cmd_control(a):
    rows = []
    for item in a.records:
        rid, _, start = item.partition(":")
        stem = stemfile.find(ROOT, rid, "vocals", a.stems.split(","))
        rec = record_file(rid)
        if not stem or not rec:
            print(f"wordread: skipped {rid}: no vocal stem or no record under ref/", file=sys.stderr)
            continue
        ss = float(start) if start else busiest(stem, a.secs)
        s = words(recognise(stem, a.model, ss, ss + a.secs))
        m = words(recognise(rec, a.model, ss, ss + a.secs))
        rows.append({"record": rid, "from": ss, "stem_words": len(s), "stem_different": len(set(s)),
                     "mix_words": len(m), "mix_different": len(set(m)), "in_common": in_order(s, m)})
    if not rows:
        sys.exit("wordread: no record could be read")
    if a.json:
        print(json.dumps(rows))
        return
    print(f"{'record (counts only)':34s} {'from s':>7s} {'stem words':>12s} {'mix words':>12s} {'of the stem, in the mix':>24s}")
    for r in rows:
        print(f"{r['record'][:33]:34s} {r['from']:7.0f} {r['stem_words']:6d} ({r['stem_different']:3d}) "
              f"{r['mix_words']:6d} ({r['mix_different']:3d}) {r['in_common']:24d}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("read")
    r.add_argument("wavs", nargs="+")
    r.add_argument("--lyric")
    r.add_argument("--lyric-file")
    r.add_argument("--models", default="small.en")
    r.add_argument("--json", action="store_true")
    c = sub.add_parser("control")
    c.add_argument("records", nargs="+")
    c.add_argument("--model", default="small.en")
    c.add_argument("--secs", type=float, default=53.0)
    c.add_argument("--stems", default="bs_roformer_sw,htdemucs_6s")
    c.add_argument("--json", action="store_true")
    a = ap.parse_args()
    (cmd_read if a.cmd == "read" else cmd_control)(a)


if __name__ == "__main__":
    main()
