#!/usr/bin/env python3
"""refread.py ID[:START] ...: THE CONTROL for barktest. On a reference record, find the 53 s where the vocal stem is busiest
(or START seconds), give the vocal stem alone and the full record over the same seconds to the recogniser (small.en), and count
how many of the words it wrote for the stem it also wrote, in order, for the record. If a recogniser cannot read the record's
own singer through the record's own band, it cannot be the judge of ours in the mix. Prints counts only, never the words.
What it found (v18), stem words -> of those, in the record: bleed 52 -> 24, pravus 54 -> 14, the-faultless 54 -> 12,
obzen 49 -> 0, combustion 65 -> 9. So: judge a harsh voice's words ALONE, and its level and tone with voxref.py.
(The stem's "words" are what the recogniser wrote, not checked against the lyric. chirper-zero, 13 Nov, Common Time.)"""
import difflib, json, os, re, subprocess, sys, wave
import numpy as np
import tempfile
ROOT = os.path.expanduser("~/.config/chirp"); W = os.environ.get("VOX_TMP") or tempfile.mkdtemp(prefix="voxread-")   # VOX_TMP keeps the renders
env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
LEN = 53.3
def words(t): return re.findall(r"[a-z']+", t.lower())
def asr(src, ss, model="small.en"):
    x = f"{W}/rr16.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(ss), "-t", str(LEN), "-i", src, "-af", "loudnorm=I=-20:TP=-3", "-ar", "16000", "-ac", "1", x], env=env)
    subprocess.run(["python3", "tools/asr.py", x, "--model", model, "--cores", "0-1", "-o", f"{W}/rr.json"], capture_output=True, env=env, cwd=ROOT)
    d = json.load(open(f"{W}/rr.json")); return words(d.get("text") or " ".join(s.get("text", "") for s in d.get("segments", [])))
print("%-34s %8s %12s %12s %10s" % ("record", "from s", "stem words", "mix words", "in common"))
for a in sys.argv[1:]:
    rid, _, st = a.partition(":"); stem = f"{ROOT}/ref/stems/bs_roformer_sw/{rid}/vocals.wav"; mix = f"{ROOT}/ref/{rid}.wav"
    if st: ss = float(st)
    else:
        x = f"{W}/rr-env.wav"; subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", stem, "-ar", "4000", "-ac", "1", x], env=env)
        w = wave.open(x); v = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
        e = np.add.reduceat(v ** 2, np.arange(0, len(v), 4000)); n = int(LEN); c = np.convolve(e, np.ones(n), "valid"); ss = float(np.argmax(c))
    s = asr(stem, ss); m = asr(mix, ss)
    got = sum(b.size for b in difflib.SequenceMatcher(None, s, m, autojunk=False).get_matching_blocks())
    print("%-34s %8.0f %6d (%2d) %6d (%2d) %10d" % (rid, ss, len(s), len(set(s)), len(m), len(set(m)), got), flush=True)
