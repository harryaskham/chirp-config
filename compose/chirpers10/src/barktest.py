#!/usr/bin/env python3
"""barktest.py NAME=PATCH ... | wav:NAME=FILE ...: can the bark's words be read? Each PATCH (a patch string, e.g. "kidman synth.layers.0.diction=2")
replaces the vox track's patch in Common Time; the voice alone over its 28 bars is rendered raw and given to two speech
recognisers (tools/asr.py, base.en and small.en; input levelled with loudnorm, never a fixed gain). Score: the lyric's words
found, in order, in what the recogniser wrote (of 35), and how many different words it wrote at all (a looped sentence scores
few). --mix reads the voice in the raw mix instead (bars 281-309). --sub="K AW1 N T=>K AA1 UH0 N T" respells a syllable.
What it found (v18): the larger model is the judge. It read 16 of 35 from `kidman` as it stands and 26-28 with diction 2 and
speech 1; the smaller one loops a made-up sentence on a scream and gave 5 and 18 for the same sound at two levels. In the mix
neither reads anything, and refread.py shows that is true of the records too. (chirper-zero, 13 Nov, Common Time.)"""
import difflib, json, os, re, subprocess, sys
import tempfile
ROOT = os.path.expanduser("~/.config/chirp"); W = os.environ.get("VOX_TMP") or tempfile.mkdtemp(prefix="voxread-")   # VOX_TMP keeps the renders
PIN = open(f"{ROOT}/tools/groove-pin").read().split()[0]
env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
LYRIC = ("wait not yet each one keeps its own count none of them wrong wait not yet they do not know each other "
         "somewhere ahead one hour holds them all keep count keep count keep count").split()
mix = "--mix" in sys.argv
SUBS = dict(a[6:].split("=>") for a in sys.argv[1:] if a.startswith("--sub="))      # --sub="K AW1 N T=>K AE1 UH0 N T": respell a syllable
args = [a for a in sys.argv[1:] if a != "--mix" and not a.startswith("--sub=")]
src = open(f"{ROOT}/songs/chirpers10-t1.yaml").read()
def words(t): return re.findall(r"[a-z']+", t.lower())
def asr(wav, model):
    x = f"{W}/bt16.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-af", "loudnorm=I=-20:TP=-3", "-ar", "16000", "-ac", "1", x], env=env)
    subprocess.run(["python3", "tools/asr.py", x, "--model", model, "--cores", "0-1", "-o", f"{W}/bt.json"], capture_output=True, env=env, cwd=ROOT)
    d = json.load(open(f"{W}/bt.json")); return d.get("text") or " ".join(s.get("text", "") for s in d.get("segments", []))
print("%-22s %s" % ("", "base.en: lyric words / different words | small.en: lyric words / different words"))
def score(name, w):
    row = []; texts = []
    for model in ("base.en", "small.en"):
        t = asr(w, model); ws = words(t); texts.append(t)
        got = sum(b.size for b in difflib.SequenceMatcher(None, LYRIC, ws, autojunk=False).get_matching_blocks())
        row.append("%2d / %2d" % (got, len(set(ws))))
    print("%-22s %s   |   %s" % (name, row[0], row[1]), flush=True)
    for t in texts: print("      " + t.strip()[:230], flush=True)
for a in [a for a in args if a.startswith("wav:")]:        # wav:NAME=FILE scores a render that already exists
    name, w = a[4:].split("=", 1); score(name, w)
args = [a for a in args if not a.startswith("wav:")]
for a in args:
    name, patch = a.split("=", 1); out = []
    for l in src.split("\n"):
        m = re.match(r'\s*- (\{"name": "vox".*)$', l)
        if m:
            t = json.loads(m.group(1))
            t["patch"] = json.loads(patch) if patch.startswith("{") else patch
            for n in t["notes"]:
                n["ph"] = SUBS.get(n["ph"], n["ph"])
            l = "  - " + json.dumps(t)
        out.append(l)
    y = f"{W}/bt-{name}.yaml"; open(y, "w").write("\n".join(out)); w = f"{W}/bt-{name}.wav"
    r = subprocess.run(["nice", "-n", "7", PIN, "render", "--threads", "2", "-f", y, "--seed", "0", *([] if mix else ["--solo", "vox"]), "--from", "281", "--to", "309",
                        "--set", "loudness=null", "-o", w], capture_output=True, text=True, env=env, cwd=ROOT)
    if r.returncode: print(name, "RENDER FAILED", r.stderr[-300:]); continue
    row = []; texts = []
    for model in ("base.en", "small.en"):
        t = asr(w, model); ws = words(t); texts.append(t)
        got = sum(b.size for b in difflib.SequenceMatcher(None, LYRIC, ws, autojunk=False).get_matching_blocks())
        row.append("%2d / %2d" % (got, len(set(ws))))
    print("%-22s %s   |   %s" % (name, row[0], row[1]), flush=True)
    for t in texts: print("      " + t.strip()[:230], flush=True)
