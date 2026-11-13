#!/usr/bin/env python3
"""asr: windowed Whisper transcription that cannot take over the host.

  asr.py AUDIO [--from S] [--to S] [--window 30] [--model base.en] [--words] [--norm] [--cores LIST] [-o OUT.json]
         [--work DIR]

Splits [--from, --to] (default: all of AUDIO) into --window second pieces, transcribes each with openai-whisper and
merges them into one JSON: {"text", "segments": [{"start", "end", "text", "words"?}]}, times on AUDIO's timeline.
Every call is confined: `taskset -c CORES` (a hard CPU limit: OpenBLAS ignored --threads and OMP/MKL caps and spread
whisper over every core — three host-wide runaways on 2026-10-21/22, all with --word_timestamps on rap stems), nice
15, OMP/MKL 4 and OPENBLAS 1 threads, no conditioning on previous text, no temperature fallback, and a timeout of 15 s
per audio second (at least 5 min). --words adds word timestamps (the heavy part; safe under taskset, just slower).
Finished windows are kept in --work (default: a temp dir, removed unless given) and reused, so an interrupted run
resumes. Prints the JSON to stdout unless -o.

--cores (or $ASR_CORES): the CPUs whisper is held to. The default is the machine's LAST four (20-23 on pocket4), not
0-3 as it was until 13 Nov: CPUs 0-3 are the groove's render threads' (chirp-eco's cpu-reserve), which moved whisper
off them and, until the same day, onto all twenty others, so the hard limit was not one.

--norm: bring each window to a standard loudness (ffmpeg loudnorm, -16 LUFS) before it is recognised. USE THIS, OR
LOUDNORM OF YOUR OWN, WHEN THE VOICE IS QUIET; NEVER A FIXED GAIN. A fixed +12 dB clipped the input, and the damage
read as the voice's own fault (chirper-zero, Common Time v17, where this tool decided a choir's word: small.en heard
"no" for a sung "now" three seeds in three). Off by default: the output without it is what it always was. Compare
models and seeds before trusting one reading; a recogniser is an ear for words, not for tone.
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


def default_cores():
    """The machine's last four CPUs ("20-23" of 24; all of them on a machine with four or fewer): away from 0-3, which
    are kept for the groove's render threads."""
    n = os.cpu_count() or 4
    return f"{max(0, n - 4)}-{n - 1}"


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


def window(audio, start, length, work, model, words, cores, norm=False):
    """One window's segments shifted to AUDIO's timeline ([] on failure, with a note on stderr)."""
    tag = f"w{start:09.3f}-{length:g}{'-words' if words else ''}{'-norm' if norm else ''}-{model}"
    done = os.path.join(work, tag + ".json")
    if not os.path.exists(done):
        wav = os.path.join(work, tag + ".wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(length), "-i", audio, "-ac", "1"]
                       + (["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"] if norm else [])
                       + ["-ar", "16000", wav], check=True, stdin=subprocess.DEVNULL)
        try:
            r = subprocess.run(whisper_cmd(wav, work, model, words, cores),
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
    ap.add_argument("--norm", action="store_true", help="loudness-normalise each window first (never use a fixed gain)")
    ap.add_argument("--cores", default=os.environ.get("ASR_CORES") or default_cores(),
                    help="CPU list for taskset (default: $ASR_CORES, else the machine's last four)")
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
            segs += window(a.audio, round(t, 3), round(n, 3), work, a.model, a.words, a.cores, a.norm)
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
