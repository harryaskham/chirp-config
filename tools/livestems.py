#!/usr/bin/env python3
"""livestems: stems for a LIVE record. The crowd (applause, cheering) is separated first, then the band from the
crowd-free mix, so the crowd doesn't land in the vocals and drums stems (Harry's S&M focus, 24 Oct).

  livestems.py ID [--crowd mdx|roformer|none] [--sw] [--threads 4] [--force]
  livestems.py --wav IN.wav --out DIR [same options]                 # any file, outside ref/stems

1. crowd (default mdx): UVR-MDX-NET Crowd HQ 1, ~1.6x realtime on 4 threads; --crowd roformer: Mel-RoFormer crowd
   (aufr33/viperx), ~25x realtime, whose crowd stem stays ~50 dB under the music during songs where MDX's carries
   10-15 dB of music bleed (use it when the crowd stem itself is the reference). -> ref/stems/crowd/ID/{crowd,nocrowd}.wav
2. band: htdemucs_6s on the crowd-free mix, ~0.8x realtime -> ref/stems/htdemucs_6s/ID/*.wav, the path every tool
   reads (an existing separation is kept unless --force; don't redo another climber's without asking).
3. --sw: BS-Roformer-SW (jarredou; the same 6 stems), ~13x realtime -> ref/stems/bs_roformer_sw/ID/*.wav.
Evidence, S&M Human 200-260 s (its applause tail 248-260 s, mean dB; the mix -24.5): demucs on the raw mix put the
applause into vocals (-25.7, the mix's own level) and drums (-42.9); on MDX's crowd-free mix vocals -76.4, drums
-76.0; BS-Roformer-SW -94.4 / -91.2. During the music the vocals stems agree within 1-4 dB (the crowd-free mix gives
2-4 dB of vocal to MDX's crowd stem). SW also keeps the orchestra in `other` (demucs scatters it: -22..-89 dB).
Slow: run it as a unit (systemd-run --user --collect …). Models cache: ~/.cache/chirp-sep/models.
Every step runs in a transient systemd scope with CPUQuota = 100 x --threads % (else taskset -c --cpus): ONNX
Runtime (the MDX crowd model) ignores OMP_NUM_THREADS and pins its own threads (taskset alone: 606%); it took 10
cores on 24 Oct and the groove underran while two climbers separated at once.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.expanduser("~/.cache/chirp-sep/models")
CROWD = {"mdx": "UVR-MDX-NET_Crowd_HQ_1.onnx", "roformer": "mel_band_roformer_crowd_aufr33_viperx_sdr_8.7144.ckpt"}
SW = "BS-Roformer-SW.ckpt"
STEMS6 = ("bass", "drums", "guitar", "other", "piano", "vocals")
UV = ["uv", "run", "--python", "3.11", "--index", "https://download.pytorch.org/whl/cpu", "--index-strategy",
      "unsafe-best-match", "--with", "torch==2.5.1"]


CPUS = ["0-3"]
QUOTA = [400]


def confine(cmd):
    """CMD in a transient systemd scope with CPUQuota (a cgroup limit the runtime can't lift: ONNX Runtime pins its
    own threads, so taskset alone still let it reach 606%), else under taskset -c CPUS."""
    if shutil.which("systemd-run") and os.environ.get("XDG_RUNTIME_DIR"):
        return ["systemd-run", "--user", "--scope", "--quiet", "-p", f"CPUQuota={QUOTA[0]}%", "--", *cmd]
    return ["taskset", "-c", CPUS[0], *cmd] if shutil.which("taskset") else cmd


def env(threads):
    e = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    e.update(OMP_NUM_THREADS=str(threads), MKL_NUM_THREADS=str(threads), OPENBLAS_NUM_THREADS="1",
             SSL_CERT_FILE=e.get("SSL_CERT_FILE", "/etc/ssl/certs/ca-certificates.crt"))
    return e


def pick(files, label):
    """The output whose `(label)` tag matches (audio-separator names stems `<in>_(Label)_<model>.wav`)."""
    want = f"({label.lower()})"
    hits = [f for f in files if want in os.path.basename(f).lower()]
    return hits[0] if hits else None


def separate(model, wav, outdir, threads, extra=()):
    os.makedirs(outdir, exist_ok=True)
    cmd = confine(["nice", "-n", "15", *UV, "--with", "audio-separator[cpu]", "audio-separator", wav, "-m", model,
                   "--model_file_dir", MODELS, "--output_dir", outdir, "--output_format", "WAV", *extra])
    r = subprocess.run(cmd, env=env(threads), capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode:
        raise SystemExit(f"livestems: {model} failed: {r.stderr.strip()[-400:]}")
    return glob.glob(os.path.join(outdir, "*.wav"))


def crowd_split(kind, wav, dest, threads):
    """dest/crowd.wav and dest/nocrowd.wav."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with tempfile.TemporaryDirectory(dir=os.path.dirname(dest)) as tmp:
        files = separate(CROWD[kind], wav, tmp, threads)
        crowd = pick(files, "crowd")
        rest = pick(files, "no crowd") or pick(files, "other")
        if not (crowd and rest):
            raise SystemExit(f"livestems: unexpected crowd outputs {[os.path.basename(f) for f in files]}")
        os.makedirs(dest, exist_ok=True)
        shutil.move(crowd, os.path.join(dest, "crowd.wav"))
        shutil.move(rest, os.path.join(dest, "nocrowd.wav"))


def demucs6(wav, name, out_root, threads):
    """htdemucs_6s on WAV -> out_root/htdemucs_6s/NAME/*.wav."""
    with tempfile.TemporaryDirectory(dir=out_root) as tmp:
        src = os.path.join(tmp, f"{name}.wav")
        shutil.copy(wav, src)
        cmd = confine(["nice", "-n", "15", *UV, "--with", "torchaudio==2.5.1", "--with", "demucs", "--with", "soundfile",
                       "python", "-m", "demucs", "-n", "htdemucs_6s", "-d", "cpu", "-j", "1", "--shifts", "0", "--float32",
                       "--clip-mode", "none", "--out", out_root, src])
        r = subprocess.run(cmd, env=env(threads), capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode:
            raise SystemExit(f"livestems: demucs failed: {r.stderr.strip()[-400:]}")


def sw6(wav, dest, threads):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with tempfile.TemporaryDirectory(dir=os.path.dirname(dest)) as tmp:
        files = separate(SW, wav, tmp, threads)
        os.makedirs(dest, exist_ok=True)
        for s in STEMS6:
            f = pick(files, s)
            if f:
                shutil.move(f, os.path.join(dest, f"{s}.wav"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--wav")
    ap.add_argument("--out")
    ap.add_argument("--crowd", choices=("mdx", "roformer", "none"), default="mdx")
    ap.add_argument("--sw", action="store_true")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--cpus", default="0-3", help="taskset CPU list every step is confined to")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    CPUS[0], QUOTA[0] = a.cpus, 100 * a.threads
    if bool(a.id) == bool(a.wav) or (a.wav and not a.out):
        ap.error("give ID, or --wav IN --out DIR")
    name = a.id or os.path.splitext(os.path.basename(a.wav))[0]
    src = a.wav or os.path.join(ROOT, "ref", f"{a.id}.wav")
    stems = a.out or os.path.join(ROOT, "ref", "stems")
    if not os.path.exists(src):
        raise SystemExit(f"livestems: no {src}")
    os.makedirs(stems, exist_ok=True)
    band_in = src
    if a.crowd != "none":
        cdir = os.path.join(stems, "crowd", name)
        if a.force or not os.path.exists(os.path.join(cdir, "nocrowd.wav")):
            crowd_split(a.crowd, src, cdir, a.threads)
            print(f"crowd ({a.crowd}): {cdir}/crowd.wav, nocrowd.wav")
        band_in = os.path.join(cdir, "nocrowd.wav")
    ddir = os.path.join(stems, "htdemucs_6s", name)
    if a.force or not os.path.exists(os.path.join(ddir, "vocals.wav")):
        demucs6(band_in, name, stems, a.threads)
        print(f"htdemucs_6s on the {'crowd-free mix' if a.crowd != 'none' else 'mix'}: {ddir}/")
    else:
        print(f"htdemucs_6s: {ddir}/ exists (kept; --force to redo)")
    if a.sw:
        sdir = os.path.join(stems, "bs_roformer_sw", name)
        if a.force or not os.path.exists(os.path.join(sdir, "vocals.wav")):
            sw6(band_in, sdir, a.threads)
            print(f"BS-Roformer-SW: {sdir}/")


if __name__ == "__main__":
    sys.exit(main())
