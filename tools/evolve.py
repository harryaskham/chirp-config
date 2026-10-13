#!/usr/bin/env python3
"""Evolve the live `groove` as songs with form across styles (metal/prog/poly/house/garage/
hardcore/acid/IDM/lofi/classical/doom-ambient). Each pass is a generated song built from
tempo-inheriting parts on parallel role tracks, with a form suited to the style (rock / edm /
classical), a main motif and hook that return, transitions, and a lifted final section.
A song identity persists for 2–3 passes, mutating one element per pass."""
import json, math, os, random, subprocess, sys, time
sys.path.insert(0, "/home/harry/.config/chirp/tools")
import compose as composer

# The binary that talks to the groove: $CHIRP_BIN, the pinned copy restart-groove.sh made, or PATH.
C = os.environ.get("CHIRP_BIN") or next((p for p in [os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "chirp-groove"), "/tmp/lt/chirp-groove"] if os.path.exists(p)), "chirp")
SONGS = "/home/harry/.config/chirp/songs"
REST = "R/1 R/1 R/1 R/1"

# off: transposition applied to F-based layers (pads, hooks, arps, holds, F-minor parts).
STYLES = {
  "djent":      dict(form="rock", tempo=(110, 150), off=0, riff=["riff-chug7", "riff-chug5", "riff-332", "riff-gallop"], riff_off=0,
                     low=["beat-sparse"], mid=["beat-poly7", "beat-euclid", "beat-ghost"], high=["beat-djent", "beat-blast", "beat-doom"],
                     half=["beat-halftime"], brk=["beat-doom"], hook=["lead-hook", "lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "prog-clean": dict(form="rock", tempo=(104, 126), off=1, riff=["riff-thump", "riff-taps"], riff_off=-1,
                     low=["beat-sparse"], mid=["beat-ghost", "beat-ride", "beat-euclid"], high=["beat-djent", "beat-ghost"],
                     half=["beat-halftime"], brk=["beat-sparse"], hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "poly":       dict(form="rock", tempo=(88, 100), off=-1, riff=["riff-nylon", "riff-funk"], riff_off=1,
                     low=["beat-sparse"], mid=["beat-trap", "beat-ghost"], high=["beat-trap", "beat-euclid"],
                     half=["beat-halftime"], brk=["beat-lofi"], hook=["lead-hook"], pad=["pad-dark", "bass-808"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "house":      dict(form="edm", tempo=(120, 126), off=0, riff=["bass-house"], riff_off=0,
                     low=["beat-house"], mid=["beat-house"], high=["beat-house"], half=["beat-lofi"], brk=["beat-sparse"],
                     hook=["chords-house"], pad=["pad-dark", "strings-chorale"], soft=["pad-swell", "strings-chorale"], arp=["arp-16th", "keys-rhodes"], hold=["chords-house"]),
  "garage":     dict(form="edm", tempo=(130, 136), off=0, riff=["bass-house", "bass-808"], riff_off=0,
                     low=["beat-garage"], mid=["beat-garage"], high=["beat-garage"], half=["beat-lofi"], brk=["beat-sparse"],
                     hook=["keys-rhodes"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["chords-house"]),
  "hardcore":   dict(form="edm", tempo=(170, 182), off=0, riff=["bass-acid"], riff_off=0,
                     low=["beat-sparse"], mid=["beat-hardcore"], high=["beat-hardcore"], half=["beat-halftime"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["strings-chorale"], arp=["arp-16th"], hold=["riff-hold"]),
  "acid":       dict(form="edm", tempo=(128, 138), off=0, riff=["bass-acid"], riff_off=0,
                     low=["beat-house"], mid=["beat-house"], high=["beat-house", "beat-euclid"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["chords-house"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["chords-house"]),
  "idm":        dict(form="edm", tempo=(150, 174), off=0, riff=["bass-acid", "arp-16th"], riff_off=0,
                     low=["beat-euclid"], mid=["beat-breaks"], high=["beat-breaks"], half=["beat-euclid"], brk=["beat-sparse"],
                     hook=["lead-hook", "keys-rhodes"], pad=["pad-dark", "strings-chorale"], soft=["pad-swell"], arp=["piano-alberti", "arp-16th"], hold=["strings-chorale"]),
  "lofi":       dict(form="edm", tempo=(72, 86), off=0, riff=["keys-lofi"], riff_off=0,
                     low=["beat-lofi"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["riff-nylon"], hook_off=1, pad=["tex-vinyl"], soft=["tex-vinyl"], arp=["keys-rhodes"], hold=["pad-swell"]),
  "classical":  dict(form="classical", tempo=(66, 90), off=0, riff=["piano-alberti"], riff_off=0,
                     low=[], mid=[], high=["beat-sparse"], half=[], brk=[],
                     hook=["lead-hook"], pad=["strings-chorale"], soft=["strings-chorale"], arp=["arp-16th"], hold=["pad-swell"]),
  "meshuggah":  dict(form="meshuggah", tempo=(96, 140), off=0, riff=["riff-chug7"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-poly7"], high=["beat-doom"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "djent-breakdown": dict(form="breakdown", tempo=(100, 140), off=0, riff=["riff-hold", "riff-chug5", "riff-chug7"], riff_off=0,
                     low=["beat-sparse"], mid=["beat-halftime"], high=["beat-doom"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "doom-ambient": dict(form="rock", tempo=(60, 72), off=0, riff=["riff-hold"], riff_off=0,
                     low=["beat-sparse"], mid=["beat-halftime"], high=["beat-doom"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
}
# Forms: (section, roles, fx). Roles: low/mid/high/half/brk (drums), riff, hook, pad, soft, arp, hold.
FORMS = {
  "rock": [("intro", ["soft"], None), ("intro2", ["soft", "low", "hold"], "riser"), ("verse", ["mid", "riffSoft"], "impact"),
           ("verse", ["mid", "riff", "arp"], None), ("pre", ["half", "hold", "pad"], "riser"), ("chorus", ["high", "riff", "hook", "pad"], "impact"),
           ("chorus", ["high", "riff", "hook", "pad"], None), ("verse2", ["mid", "riff", "arp"], "impact"), ("chorus", ["high", "riff", "hook", "pad"], "impact"),
           ("break", ["brk", "hold"], "revcym"), ("solo", ["high", "riff", "solo"], "impact"), ("pre", ["half", "hold", "pad", "arp"], "riser"),
           ("final", ["high", "riff", "hook", "pad", "arp"], "impact"), ("final", ["high", "riff", "hook", "pad", "arp"], None), ("outro", ["soft", "hold", "low"], "revcym")],
  "edm":  [("intro", ["low"], None), ("intro2", ["low", "soft"], None), ("build", ["mid", "riffSoft"], "riser"), ("drop", ["high", "riff", "hook", "pad"], "impact"),
           ("drop", ["high", "riff", "hook", "pad", "arp"], None), ("break", ["soft", "arp"], "revcym"), ("break", ["soft", "arp", "hold"], None),
           ("build", ["mid", "riff", "arp"], "riser"), ("final", ["high", "riff", "hook", "pad", "arp"], "impact"), ("final", ["high", "riff", "hook", "pad"], None),
           ("outro", ["low", "soft"], "revcym")],
  # Polymetric riffs carry their own locked drums (kick follows the guitar; 4/4 cymbals, snare on 3).
  "meshuggah": [("intro", ["soft", "hold"], "revcym"), ("verse", ["riffSoft"], "impact"), ("verse", ["riff", "pad"], None),
                ("heavy", ["riffB"], "impact"), ("heavy", ["riffB", "hook"], None), ("shuffle", ["riffS"], "impact"),
                ("shuffle", ["riffS", "pad"], None), ("toms", ["riffT"], "impact"), ("toms", ["riffT", "soft"], None),
                ("space", ["riffX"], "impact"), ("space", ["riffX", "drone"], None),
                ("verse2", ["riff", "hook"], "revcym"), ("break", ["riffBrk"], "impact"),
                ("break", ["riffBrk", "soft"], None), ("C", ["riffC"], "impact"), ("C", ["riffC", "hook", "pad"], None),
                ("final", ["riff", "hook", "pad"], "impact"), ("outro", ["soft", "hold"], "revcym")],
  "breakdown": [("intro", ["brk", "hold"], "revcym"), ("break", ["half", "riff"], "impact"), ("break", ["half", "riff", "pad"], None),
                ("build", ["mid", "riffSoft", "arp"], "riser"), ("drop", ["high", "riff", "hook"], "impact"), ("drop", ["high", "riff", "hook", "pad"], None),
                ("break", ["brk", "hold", "pad"], "revcym"), ("final", ["high", "riff", "hook", "pad"], "impact"), ("outro", ["brk", "hold"], "revcym")],
  "classical": [("A", ["pad", "riff"], None), ("A", ["pad", "riff", "hook"], None), ("B", ["soft", "arp"], None), ("B", ["soft", "arp", "hook"], "riser"),
                ("final", ["pad", "riff", "hook", "high"], "impact"), ("coda", ["soft"], "revcym")],
}

def live(*a):
    r = subprocess.run([C, "--json", "live", *a, "--id", "groove"], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)["data"]
    except Exception:
        return {}

def pick(s, role):
    return random.choice(s[role]) if s.get(role) else None

def identity(style=None):
    style = style or random.choice(list(STYLES))
    s = STYLES[style]
    bpm = random.randrange(s["tempo"][0], s["tempo"][1] + 1, 2)
    return dict(style=style, tempo=bpm, base_tempo=bpm, chapter=0, key=0, gen=composer.params(style), comp=random.choice(COMP_STYLES),
                **{r: pick(s, r) for r in ["riff", "low", "mid", "high", "half", "brk", "hook", "pad", "soft", "arp", "hold"]})

def mutate(ident):
    s = STYLES[ident["style"]]
    k = random.choice(["tempo", "key", "mid", "high", "hook", "arp", "pad"])
    ident = dict(ident)
    if k == "tempo":
        ident["tempo"] = max(s["tempo"][0] - 6, min(s["tempo"][1] + 6, ident["tempo"] + random.choice([-4, -2, 2, 4])))
    elif k == "key":
        ident["key"] = random.choice([-2, -1, 0, 1, 2])
    else:
        ident[k] = pick(s, k) or ident[k]
    return ident, k

PASS_MINUTES = 1.0

def chapters(ident):
    """Split the style's form into consecutive chapters of about PASS_MINUTES each."""
    form = FORMS[STYLES[ident["style"]]["form"]]
    n = max(4, round(ident.get("base_tempo", ident["tempo"]) * PASS_MINUTES / 16))
    chs = [form[i:i + n] for i in range(0, len(form), n)]
    if len(chs) > 1 and len(chs[-1]) < n / 2:
        last = chs.pop()
        chs[-1] = chs[-1] + last
    return chs

COMP_STYLES = ["glue", "pump", "smash", "parallel", "opto", "tape"]

def has_patch(name):
    return subprocess.run([C, "plan", "-p", name, "C4/4"], capture_output=True).returncode == 0

BUILTIN_FX = {p: has_patch(p) for p in ["fx-tapestop", "fx-riser-shepard", "fx-riser-noise", "fx-reverse", "drone", "fx-downlifter"]}
BUILTIN_FX["fx-reverse"] = False  # sample-song layer: rejected by live sessions (resample path), see bead

MASTER_BASE = ['{"type": "eq", "bands": ["hp cutoff=28", "peak cutoff=320 q=0.8 gain=-1dB", "highshelf cutoff=9000 gain=1.5dB"]}']

def master_for(ident):
    """Master chain for the chapter about to play: the room and glue follow its content."""
    chs = chapters(ident)
    secs = [sec for sec, _, _ in chs[min(ident.get("chapter", 0), len(chs) - 1)]]
    calm = sum(sec in ("intro", "intro2", "break", "outro", "coda", "B") for sec in secs) / len(secs)
    shuffle = "shuffle" in secs
    toms = "toms" in secs
    if calm >= 0.4:
        verb, ott, makeup = "reverb kind=hall decay=3.6s size=1 mix=0.2 predelay=35ms low_cut=220 high_cut=7500 width=1.4 modulation=0.5", 0.1, 3
    elif shuffle:
        verb, ott, makeup = "reverb kind=plate decay=2s mix=0.14 predelay=20ms low_cut=250 width=1.3 modulation=0.3", 0.15, 3.5
    else:
        verb, ott, makeup = "reverb kind=room decay=1.6s size=0.8 mix=0.1 predelay=15ms low_cut=280 high_cut=8000 width=1.25 modulation=0.3", 0.2, 4
    if toms:  # the tom grooves love the compressor
        ott, makeup = 0.25, makeup + 0.5
    comp = ident.get("comp", "glue")
    dyn = {
        "glue": [f"ott depth={ott} time=0.3", f"glue threshold=-16dB ratio=2 attack=10ms release=150ms makeup={makeup}dB", "tape drive=0.25 warmth=0.4"],
        "pump": [f"ott depth={ott} time=0.2", f"compressor threshold=-22dB ratio=6 attack=1ms release=70ms makeup={makeup + 2}dB", "tape drive=0.2 warmth=0.4"],
        "smash": [f"ott depth={min(0.55, ott + 0.3)} time=0.2", f"glue threshold=-14dB ratio=2 attack=10ms release=120ms makeup={makeup - 1}dB", "tape drive=0.3 warmth=0.45"],
        "parallel": [f"ott depth={ott} time=0.3", f"glue threshold=-30dB ratio=8 attack=3ms release=90ms makeup={makeup + 6}dB mix=0.45", "tape drive=0.25 warmth=0.4"],
        "opto": [f"ott depth={ott * 0.5} time=0.6", f"compressor threshold=-18dB ratio=3 attack=30ms release=450ms makeup={makeup}dB", "glue threshold=-14dB ratio=1.5 makeup=1dB"],
        "tape": [f"ott depth={ott * 0.5} time=0.4", f"glue threshold=-16dB ratio=2 makeup={makeup - 1}dB", "tape drive=0.6 warmth=0.7"],
    }[comp]
    fx = [json.loads(MASTER_BASE[0]), verb] + dyn + ["width width=1.2 mono_below=140"]
    return json.dumps(fx)

def write_form(name, ident):
    s = STYLES[ident["style"]]
    if ident.get("gen"):
        # Freshly composed melodic parts in their own key: no F-based offsets.
        names, gdesc = composer.compose(ident["style"], name, ident["gen"])
        ident = dict(ident, **names, solo=names["hook"])
        s = dict(s, off=0, riff_off=0, hook_off=0)
    else:
        gdesc = "library parts"
    roles = ["drums", "riff", "hook", "pad", "arp", "hold", "drone", "fx"]
    tracks = {t: [] for t in roles}
    chs = chapters(ident)
    chapter = chs[min(ident.get("chapter", 0), len(chs) - 1)]
    form_secs = [sec for sec, _, _ in chapter]
    for idx, (sec, layers, fx) in enumerate(chapter):
        lift = s.get("lift", 2) if sec == "final" else 0
        def put(track, part, off, xf=""):
            if not part:
                tracks[track].append(REST)
                return
            t = ident["key"] + off + lift
            tracks[track].append(f"tr={t} @{part}{xf} tr=0" if t else f"@{part}{xf}")
        drum = next((ident[r] for r in ["high", "mid", "half", "brk", "low"] if r in layers and ident.get(r)), None)
        tracks["drums"].append(f"@{drum}" if drum else REST)
        # The motif develops when it returns: rotated/thinned in verse 2, thinned under the solo.
        riff_xf = {"verse2": random.choice(["^rot=0.5", "^rot=1", "^thin=0.2"]), "solo": "^thin=0.35"}.get(sec, "")
        rx = ident.get("xf", {})
        riff_role = next((l for l in layers if l.startswith("riff")), None)
        part = (ident.get(riff_role) or ident.get("riff")) if riff_role else None
        put("riff", part, s["riff_off"], riff_xf + rx.get("riff", ""))
        hook = ident.get("solo", "lead-solo") if "solo" in layers else (ident["hook"] if "hook" in layers else None)
        put("hook", hook, s.get("hook_off", s["off"]), ("^rot=1" if "solo" in layers and ident.get("gen") else "") + rx.get("hook", ""))
        pad = ident["pad"] if "pad" in layers else (ident["soft"] if "soft" in layers else None)
        put("pad", pad, s["off"], rx.get("pad", ""))
        put("arp", ident["arp"] if "arp" in layers else None, s["off"], ("^rev" if sec == "break" else "") + rx.get("arp", ""))
        put("hold", ident["hold"] if "hold" in layers else None, s["off"], rx.get("hold", ""))
        calm = sec in ("intro", "intro2", "break", "outro", "coda", "space")
        put("drone", ident.get("drone") if ("drone" in layers or (calm and ident.get("drone"))) and BUILTIN_FX["drone"] else None, 0)
        nxt_sec = form_secs[idx + 1] if idx + 1 < len(form_secs) else None
        if nxt_sec == "break" and BUILTIN_FX["fx-tapestop"] and random.random() < 0.6:
            fx = "tapestop"
        risers = ["fx-riser"] + [p for p in ["fx-riser-shepard", "fx-riser-noise"] if BUILTIN_FX[p]]
        revs = ["fx-revcym"] + (["fx-reverse"] if BUILTIN_FX["fx-reverse"] else [])
        tracks["fx"].append({"riser": f"R/1 R/1 R/1 patch={random.choice(risers)} C4/1@90",
                             "impact": "patch=fx-impact F1/4@104 R/4 R/2 R/1 R/1 R/1",
                             "revcym": f"R/1 R/1 R/1 R/2 patch={random.choice(revs)} C5/2@88",
                             "tapestop": "R/1 R/1 R/1 patch=fx-tapestop C4/1@100"}.get(fx, REST))
    lines = [f"about: Generated {s['form']}-form song — {ident['style']} at {ident['tempo']} BPM, {gdesc}, shift {ident['key']:+d}, chapter {ident.get('chapter', 0) + 1}/{len(chs)}, comp {ident.get('comp', 'glue')}.",
             f"tempo: {ident['tempo']}", "tracks:"]
    for t, items in tracks.items():
        lines.append(f"  - {{name: {t}, score: \"{' '.join(items)}\"}}")
    open(f"{SONGS}/{name}.yaml", "w").write("\n".join(lines) + "\n")

TOOLS = "/home/harry/.config/chirp/tools"
JOURNEY = f"{TOOLS}/journey.json"
# How heavy each style is (0 lofi … 1 djent).
HEAVY = {"meshuggah": 1.0, "lofi": 0.0, "classical": 0.05, "house": 0.2, "garage": 0.25, "poly": 0.35, "prog-clean": 0.4, "acid": 0.45,
         "idm": 0.55, "doom-ambient": 0.6, "hardcore": 0.7, "djent-breakdown": 0.85, "djent": 1.0}

def journey_load():
    try:
        return json.load(open(JOURNEY))
    except Exception:
        return {"on": False, "h": 0.0, "rate": 0.09, "passes_per_song": 2}

def journey_style(h, current):
    """Pick a style near heaviness h; at full heaviness: mostly djent, sometimes breakdown/clean/excursion."""
    r = random.random()
    if h >= 0.95:
        if r < 0.12:
            return "djent-breakdown"
        if r < 0.24:
            return random.choice(["prog-clean", "poly"])
        if r < 0.34:
            return random.choice([k for k in STYLES if k not in ("djent", "meshuggah", current)])
        return "meshuggah" if r < 0.79 else "djent"
    if r < 0.1:
        return random.choice([k for k in STYLES if k != current])
    w = {k: math.exp(-((HEAVY.get(k, 0.5) - h) / 0.15) ** 2) for k in STYLES}
    if current in w and len(w) > 1:
        w[current] *= 0.3  # prefer moving on
    tot = sum(w.values())
    x = random.random() * tot
    for k, v in w.items():
        x -= v
        if x <= 0:
            return k
    return "djent"

STEER = f"{TOOLS}/steer.txt"
STATE = f"{TOOLS}/state.json"

def steer(ident, cmd):
    """Apply one steering command to an identity; returns (ident, description)."""
    s = STYLES[ident["style"]]
    words = cmd.split()
    op, args = words[0], words[1:]
    ident = json.loads(json.dumps(ident))
    if op == "key":
        ident["key"] = max(-5, min(6, ident["key"] + int(args[0]) if args[0][0] in "+-" else int(args[0])))
    elif op == "tempo":
        ident["tempo"] = max(50, min(200, ident["tempo"] + int(args[0]) if args[0][0] in "+-" else int(args[0])))
    elif op == "swap":
        role = args[0]
        if args[1:]:
            ident[role] = args[1]
        else:
            opts = [p for p in s.get(role, []) if p != ident.get(role)] or s.get(role, [])
            ident[role] = random.choice(opts) if opts else ident.get(role)
    elif op == "xf":
        ident.setdefault("xf", {})[args[0]] = args[1] if len(args) > 1 else ""
    elif op == "style":
        new = identity(args[0] if args else random.choice([k for k in STYLES if k != ident["style"]]))
        new["key"] = ident["key"]  # keep the key so the cut is smooth
        ident = new
    elif op == "journey":
        j = journey_load()
        for a in args:
            if a in ("on", "off"):
                j["on"] = a == "on"
            elif "=" in a:
                k, v = a.split("=", 1)
                j[k] = float(v)
        open(JOURNEY, "w").write(json.dumps(j) + "\n")
        return ident, f"journey {j}"
    elif op in ("compose", "melody", "rekey"):
        g = composer.params(ident["style"])
        old = ident.get("gen") or g
        ident["gen"] = g if op == "compose" else (dict(old, seed=g["seed"]) if op == "melody" else dict(g, seed=old["seed"]))
        ident["key"] = 0
        return ident, f"{op}: {composer.NAMES[ident['gen']['pc']]} {ident['gen']['mode']} prog {'-'.join(str(d + 1) for d in ident['gen']['prog'])}"
    elif op == "comp":
        ident["comp"] = args[0] if args else random.choice(COMP_STYLES)
        if ident["comp"] not in COMP_STYLES:
            raise ValueError(f"comp: one of {COMP_STYLES}")
    elif op == "mutate":
        ident, k = mutate(ident)
        return ident, f"mutate {k}"
    else:
        raise ValueError(f"unknown steer command {cmd!r}")
    return ident, cmd

def save_state(**kw):
    open(STATE, "w").write(json.dumps(kw, indent=1, default=str) + "\n")

def wait_generation(after, timeout=8.0):
    t = time.time()
    while time.time() - t < timeout:
        st = live("status") or {}
        if st.get("generation", after) > after:
            return True
        time.sleep(0.25)
    return False

if __name__ == "__main__":
    ident, passes, flip = identity(os.environ.get("EVOLVE_STYLE")), 0, 0
    seen, next_var = None, time.time() + 20
    playing, playing_ident, nxt, nxt_ident = None, None, None, None
    if os.environ.get("EVOLVE_RESUME") == "keep":
        # Evolver-only restart: the groove keeps playing what it was playing.
        try:
            prev = json.load(open(STATE))
            playing, playing_ident, nxt, nxt_ident = prev["playing"], prev["playing_ident"], prev["next"], prev["next_ident"]
            ident, passes = dict(playing_ident), 1
            seen = prev.get("loop_index")
            flip = 0 if nxt == "form-1" else 1
            print(time.strftime("%T"), f"resumed (keep): playing {playing}, next {nxt}", flush=True)
        except Exception as e:
            print(time.strftime("%T"), f"resume failed: {e}", flush=True)
    elif os.environ.get("EVOLVE_RESUME"):
        # The queued song is (about to be) playing: adopt it so steering works immediately.
        try:
            prev = json.load(open(STATE))
            playing, playing_ident = prev["next"], prev["next_ident"]
            ident, passes = dict(playing_ident), 1
            print(time.strftime("%T"), f"resumed: playing {playing} {ident['style']}", flush=True)
        except Exception as e:
            print(time.strftime("%T"), f"resume failed: {e}", flush=True)
    open(STEER, "a").close()
    while True:
        st = live("status")
        gap = time.time()
        while st is None and time.time() - gap < 20:
            time.sleep(1)
            st = live("status")
        if st is None:
            print(time.strftime("%T"), "groove ended", flush=True)
            break
        li = st.get("loop_index")
        if li != seen:
            first = seen is None
            seen = li
            if not first and nxt:
                playing, playing_ident = nxt, nxt_ident
            passes += 1
            j = journey_load()
            if j.get("on") and not first:
                j["h"] = round(min(1.0, j.get("h", 0) + j.get("rate", 0.09)), 3)
                open(JOURNEY, "w").write(json.dumps(j) + "\n")
            # Each pass plays the next ~1-minute chapter of the song; after the last, a new song.
            if not first and ident.get("chapter", 0) + 1 < len(chapters(ident)):
                ident = dict(ident, chapter=ident.get("chapter", 0) + 1)
                change = f"chapter {ident['chapter'] + 1}/{len(chapters(ident))}"
                if random.random() < 0.5:
                    st_ = STYLES[ident["style"]]
                    ident["tempo"] = max(st_["tempo"][0] - 10, min(st_["tempo"][1] + 10, ident["tempo"] + random.choice([-12, -8, -6, -4, 4, 6, 8, 12])))
                    change += f", tempo {ident['tempo']}"
                if random.random() < 0.3:
                    ident, k = mutate(ident)
                    change += f", {k}"
            elif not first or passes > 1:
                style = journey_style(j.get("h", 0), ident["style"]) if j.get("on") else random.choice([k for k in STYLES if k != ident["style"]])
                prev_bpm = ident.get("tempo", 120)
                for _ in range(8):  # keep tempos moving: at least 14 BPM from the last song
                    cand = identity(style)
                    if abs(cand["tempo"] - prev_bpm) >= 14:
                        break
                ident, passes, change = cand, 1, f"new song h={j.get('h', 0):.2f}" if j.get("on") else "new song"
            else:
                change = "first pass"
            flip = 1 - flip
            name = f"form-{flip + 1}"
            if name == playing:
                flip = 1 - flip
                name = f"form-{flip + 1}"
            write_form(name, ident)
            nxt, nxt_ident = name, dict(ident)
            ok = live("set", f"tracks.arrangement.score=@{name}", f"master.fx={master_for(ident)}")
            print(time.strftime("%T"), f"pass {li}: next {name} ({change}) {ident['style']} {ident['tempo']}bpm key{ident['key']:+d} riff={ident['riff']} hook={ident['hook']}" + ("" if ok is not None else "  (rejected)"), flush=True)
            save_state(playing=playing, playing_ident=playing_ident, next=nxt, next_ident=nxt_ident, loop_index=li)
        # Steering: apply to the song playing now (cut at the next bar, same position),
        # then carry the change into the queued next song and re-queue it.
        cmds = [l.strip() for l in open(STEER).read().splitlines() if l.strip() and not l.startswith("#")]
        if cmds:
            open(STEER, "w").close()
            for cmd in cmds:
                try:
                    if cmd.split()[0] == "next":
                        # Replace only the queued song with a fresh one in STYLE (playing untouched).
                        words = cmd.split()
                        nxt_ident = identity(words[1] if len(words) > 1 else None)
                        write_form(nxt, nxt_ident)
                        ident, passes = dict(nxt_ident), 0
                        live("set", f"tracks.arrangement.score=@{nxt}")
                        print(time.strftime("%T"), f"steer: next → {nxt} {nxt_ident['style']} {nxt_ident['tempo']}bpm {nxt_ident.get('gen')}", flush=True)
                        continue
                    if playing and playing_ident:
                        # Only carry the change into the queued pass if it continues the same song.
                        same = bool(nxt_ident) and nxt_ident.get("gen") == playing_ident.get("gen") and nxt_ident.get("style") == playing_ident.get("style")
                        playing_ident, desc = steer(playing_ident, cmd)
                        write_form(playing, playing_ident)
                        gen = (live("status") or {}).get("generation", 0)
                        ok = subprocess.run([C, "live", "set", "--id", "groove", "--when", "bar", "--xfade", "250ms", f"tracks.arrangement.score=@{playing}", f"master.fx={master_for(playing_ident)}"], capture_output=True, text=True).returncode == 0
                        applied = ok and wait_generation(gen)
                        if cmd.split()[0] == "style":
                            nxt_ident = dict(playing_ident)
                        elif not same:
                            pass
                        elif cmd.split()[0] in ("compose", "melody", "rekey"):
                            nxt_ident = dict(nxt_ident, gen=playing_ident["gen"], key=playing_ident["key"])
                        else:
                            nxt_ident, _ = steer(nxt_ident, cmd)
                        write_form(nxt, nxt_ident)
                        ident = dict(nxt_ident)
                        live("set", f"tracks.arrangement.score=@{nxt}")
                        print(time.strftime("%T"), f"steer: {desc} → {playing} now ({'applied' if applied else 'NOT applied'}), {nxt} next", flush=True)
                    else:
                        nxt_ident, desc = steer(nxt_ident or ident, cmd)
                        write_form(nxt, nxt_ident)
                        ident = dict(nxt_ident)
                        live("set", f"tracks.arrangement.score=@{nxt}")
                        print(time.strftime("%T"), f"steer: {desc} → queued in {nxt} (current song not ours yet)", flush=True)
                except Exception as e:
                    print(time.strftime("%T"), f"steer failed: {cmd!r}: {e}", flush=True)
            save_state(playing=playing, playing_ident=playing_ident, next=nxt, next_ident=nxt_ident, loop_index=li)
        time.sleep(1)
