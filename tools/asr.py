#!/usr/bin/env python3
"""asr: windowed Whisper transcription that cannot take over the host.

  asr.py AUDIO [--from S] [--to S] [--window 30] [--model base.en] [--words] [--cores 0-3] [-o OUT.json] [--work DIR]

Splits [--from, --to] (default: all of AUDIO) into --window second pieces, transcribes each with openai-whisper and
merges them into one JSON: {"text", "segments": [{"start", "end", "text", "words"?}]}, times on AUDIO's timeline.
Every call is confined: `taskset -c CORES` (a hard CPU limit: OpenBLAS ignored --threads and OMP/MKL caps and spread
whisper over every core — three host-wide runaways on 2026-10-21/22, all with --word_timestamps on rap stems), nice
15, OMP/MKL 4 and OPENBLAS 1 threads, no conditioning on previous text, no temperature fallback, and a timeout of 15 s
per audio second (at least 5 min). --words adds word timestamps (the heavy part; safe under taskset, just slower).
Finished windows are kept in --work (default: a temp dir, removed unless given) and reused, so an interrupted run
resumes. Prints the JSON to stdout unless -o.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return float(r.stdout.strip())


def whisper_cmd(wav, outdir, model, words, cores):
    cmd = ["taskset", "-c", cores, "nice", "-n", "15", "whisper", wav, "--model", model, "--language", "en",
           "--threads", "4", "--condition_on_previous_text", "False", "--temperature_increment_on_fallback", "None",
           "--fp16", "False", "--output_dir", outdir, "--output_format", "json", "--verbose", "False"]
    if words:
        cmd += ["--word_timestamps", "True"]
    return cmd


def env():
    e = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    e.update(OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", OPENBLAS_NUM_THREADS="1")
    return e


def window(audio, start, length, work, model, words, cores):
    """One window's segments shifted to AUDIO's timeline ([] on failure, with a note on stderr)."""
    tag = f"w{start:09.3f}-{length:g}{'-words' if words else ''}-{model}"
    done = os.path.join(work, tag + ".json")
    if not os.path.exists(done):
        wav = os.path.join(work, tag + ".wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(length), "-i", audio, "-ac", "1",
                        "-ar", "16000", wav], check=True, stdin=subprocess.DEVNULL)
        try:
            r = subprocess.run(whisper_cmd(wav, work, model, words, os.environ.get("ASR_CORES") or "0-3"),
                               capture_output=True, text=True, stdin=subprocess.DEVNULL, env=env(),
                               timeout=max(300, 15 * length))
        except subprocess.TimeoutExpired:
            print(f"asr: window {start:g}+{length:g} s timed out", file=sys.stderr)
            return []
        out = os.path.join(work, tag + ".json")       # whisper names its output after the input
        if r.returncode or not os.path.exists(out):
            print(f"asr: window {start:g}+{length:g} s failed: {r.stderr[-300:]}", file=sys.stderr)
            return []
        os.remove(wav)
    with open(done) as f:
        d = json.load(f)
    segs = []
    for s in d.get("segments", []):
        seg = {"start": round(s["start"] + start, 3), "end": round(s["end"] + start, 3), "text": s["text"].strip()}
        if words and s.get("words"):
            seg["words"] = [{"word": w["word"].strip(), "start": round(w["start"] + start, 3),
                             "end": round(w["end"] + start, 3)} for w in s["words"]]
        segs.append(seg)
    return segs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("audio")
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float)
    ap.add_argument("--window", type=float, default=30.0)
    ap.add_argument("--model", default="base.en")
    ap.add_argument("--words", action="store_true")
    ap.add_argument("--cores", default="0-3", help="CPU list for taskset (default 0-3)")
    ap.add_argument("-o", dest="out")
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    if a.window <= 0:
        ap.error("--window must be positive")
    t1 = a.t1 if a.t1 is not None else duration(a.audio)
    work = a.work or tempfile.mkdtemp(prefix="asr-")
    os.makedirs(work, exist_ok=True)
    os.environ["ASR_CORES"] = a.cores
    try:
        segs = []
        t = a.t0
        while t < t1 - 0.05:
            n = min(a.window, t1 - t)
            segs += window(a.audio, round(t, 3), round(n, 3), work, a.model, a.words, a.cores)
            t += a.window
        res = {"audio": os.path.abspath(a.audio), "from": a.t0, "to": t1, "model": a.model,
               "text": " ".join(s["text"] for s in segs), "segments": segs}
        if a.out:
            with open(a.out, "w") as f:
                json.dump(res, f, indent=1)
        else:
            print(json.dumps(res, indent=1))
    finally:
        if not a.work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
