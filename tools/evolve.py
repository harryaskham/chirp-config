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
  "prog-clean": dict(form="rock", tempo=(104, 126), off=1, riff=["riff-thump", "riff-taps"], riff_off=0,
                     low=["beat-sparse"], mid=["beat-ghost", "beat-ride", "beat-euclid"], high=["beat-djent", "beat-ghost"],
                     half=["beat-halftime"], brk=["beat-sparse"], hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "poly":       dict(form="rock", tempo=(88, 100), off=-1, riff=["riff-nylon", "riff-funk"], riff_off=0,
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
  "thrash":     dict(form="thrash", tempo=(170, 210), off=0, riff=["riff-gallop"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-blast"], high=["beat-blast"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "tool":       dict(form="tool", tempo=(90, 126), off=0, riff=["riff-chug7"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-poly7"], high=["beat-doom"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "brostep":    dict(form="brostep", tempo=(140, 150), off=0, riff=["bass-acid"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-halftime"], high=["beat-halftime"], half=["beat-halftime"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "hardcore-kl": dict(form="hardcore-kl", tempo=(140, 180), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "blackgaze":  dict(form="blackgaze", tempo=(150, 190), off=0, riff=["riff-chug7"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-blast"], high=["beat-blast"], half=["beat-halftime"], brk=["beat-sparse"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "darksynth":  dict(form="darksynth", tempo=(104, 124), off=0, riff=["bass-acid"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-house"], high=["beat-house"], half=["beat-halftime"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "numetal":    dict(form="numetal", tempo=(92, 112), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "industrial": dict(form="industrial", tempo=(112, 128), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "dnb":        dict(form="dnb", tempo=(170, 176), off=0, riff=["bass-acid"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "deathcore":  dict(form="deathcore", tempo=(130, 170), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "postrock":   dict(form="postrock", tempo=(100, 130), off=0, riff=["riff-taps"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "groovemetal": dict(form="groovemetal", tempo=(100, 140), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "power":      dict(form="power", tempo=(170, 210), off=0, riff=["riff-gallop"], riff_off=0, lift=2,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "sludge":     dict(form="sludge", tempo=(60, 84), off=0, riff=["riff-hold"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "breakcore":  dict(form="breakcore", tempo=(170, 190), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "mathcore":   dict(form="mathcore", tempo=(150, 190), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "gojira":     dict(form="gojira", tempo=(100, 140), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "djazz":      dict(form="djazz", tempo=(120, 150), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "raga":       dict(form="raga", tempo=(96, 132), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "gamelan":    dict(form="gamelan", tempo=(100, 136), off=0, riff=["riff-chug5"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "koto":       dict(form="koto", tempo=(120, 160), off=0, riff=["riff-chug5"], riff_off=0, lift=2,
                     low=["beat-sparse"], mid=["beat-djent"], high=["beat-djent"], half=["beat-halftime"], brk=["beat-doom"],
                     hook=["lead-solo"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["riff-hold"]),
  "tech-death": dict(form="tech-death", tempo=(170, 220), off=0, riff=["riff-chug7"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-blast"], high=["beat-blast"], half=["beat-halftime"], brk=["beat-doom"],
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
                ("heavy", ["riffB"], "impact"), ("heavy", ["riffB", "hook"], None),
                ("blast", ["riffBl"], "impact"), ("blast", ["riffBl", "pad"], None), ("shuffle", ["riffS"], "impact"),
                ("shuffle", ["riffS", "pad"], None), ("toms", ["riffT"], "impact"), ("toms", ["riffT", "soft"], None),
                ("space", ["riffX"], "impact"), ("space", ["riffX", "drone", "hookE"], None),
                ("verse2", ["riff", "hook"], "revcym"), ("break", ["riffBrk"], "impact"),
                ("break", ["riffBrk", "soft"], None), ("C", ["riffC"], "impact"), ("C", ["riffC", "hook", "pad"], None),
                ("final", ["riff", "hook", "pad"], "impact"), ("outro", ["soft", "hold"], "revcym")],
  "thrash": [("intro", ["riffH"], "revcym"), ("intro2", ["riffG"], "impact"), ("verse", ["riff"], "impact"),
             ("verse", ["riff", "pad"], None), ("pre", ["riffC"], "riser"), ("chorus", ["riffH", "hook"], "impact"),
             ("chorus", ["riffG", "hook"], None), ("verse2", ["riffC"], "impact"), ("solo", ["riffG", "solo"], "impact"),
             ("solo", ["riff", "solo"], None), ("break", ["riffBrk"], "impact"), ("chorus", ["riffH", "hook"], "impact"),
             ("final", ["riffG", "hook", "pad"], None), ("outro", ["riffH"], "revcym")],
  # Tool-style journey: the band plays odd meters (sections take their parts' lengths).
  "tool": [("intro", ["riffClean"], None), ("intro2", ["riffCleanB"], None), ("A", ["riffSoft"], "impact"),
           ("A", ["riff"], None), ("A2", ["riff", "hookA"], None), ("B", ["riffB"], "impact"), ("B2", ["riffB", "hookB"], None),
           ("C", ["riffT"], None), ("C2", ["riffP"], "impact"), ("build", ["riffUp"], "riser"), ("climax", ["riffB", "hookB"], "impact"),
           ("break", ["riffClean"], "revcym"), ("final", ["riff", "hookA"], "impact"), ("outro", ["riffCleanB"], "revcym")],
  "brostep": [("intro", ["riffIntro", "pad"], None), ("build", ["riffUp", "pad"], "riser"), ("drop", ["riff"], "impact"),
              ("drop", ["riffB"], None), ("break", ["riffIntro", "soft", "hookE"], "revcym"), ("build", ["riffUp", "arp"], "riser"),
              ("drop", ["riffM"], "impact"), ("drop", ["riffM2"], None), ("outro", ["soft"], "revcym")],
  "hardcore-kl": [("intro", ["riffSq"], "revcym"), ("verse", ["riffSoft"], "impact"), ("verse", ["riff"], None),
                  ("fast", ["riffD"], "impact"), ("fast", ["riffD"], None), ("break", ["riffBd"], "impact"), ("break", ["riffBd2"], None),
                  ("verse2", ["riff"], "impact"), ("fast", ["riffD"], None), ("stop", ["riffStop"], "tapestop"),
                  ("break", ["riffSlow"], "impact"), ("final", ["riffBd"], "impact"), ("outro", ["riffSq"], "revcym")],
  "blackgaze": [("intro", ["riffClean"], None), ("intro2", ["riffClean", "hookE"], None), ("build", ["riffUp"], "riser"),
                ("blast", ["riff"], "impact"), ("blast", ["riffB", "hook"], None), ("half", ["riffH", "hookE"], "revcym"),
                ("build", ["riffUp"], "riser"), ("climax", ["riff", "hook"], "impact"), ("final", ["riffB", "hookE"], None),
                ("outro", ["riffClean"], "revcym")],
  "darksynth": [("intro", ["riffIntro"], None), ("verse", ["riff"], "impact"), ("verse", ["riff", "pad"], None),
                ("build", ["riffUp", "pad"], "riser"), ("drop", ["riffD", "hook"], "impact"), ("drop", ["riffD2", "hook"], None),
                ("break", ["riffIntro"], "revcym"), ("build", ["riffUp"], "riser"), ("final", ["riffD", "hook", "pad"], "impact"),
                ("outro", ["riffIntro"], "revcym")],
  "numetal": [("intro", ["riffV"], None), ("verse", ["riffV"], None), ("verse", ["riffSoft"], "impact"), ("chorus", ["riffH", "hook"], "impact"),
              ("verse2", ["riff"], "impact"), ("verse2", ["riffB"], None), ("chorus", ["riffH", "hook"], "impact"), ("break", ["riffBrk"], "impact"),
              ("bridge", ["riffV", "pad"], "revcym"), ("final", ["riffB", "hook"], "impact"), ("outro", ["riffV"], "revcym")],
  "industrial": [("intro", ["riffV"], None), ("verse", ["riffSoft"], "impact"), ("verse", ["riff"], None), ("build", ["riffUp", "pad"], "riser"),
                 ("chorus", ["riffS", "hook"], "impact"), ("chorus", ["riff", "hook"], None), ("break", ["riffV", "pad"], "revcym"),
                 ("final", ["riffS", "hook", "pad"], "impact"), ("final", ["riff", "hook"], None), ("outro", ["riffV"], "revcym")],
  "dnb": [("intro", ["riffIntro"], None), ("build", ["riffUp", "pad"], "riser"), ("drop", ["riff"], "impact"), ("drop", ["riffB"], None),
          ("break", ["riffIntro", "soft", "hookE"], "revcym"), ("build", ["riffUp", "arp"], "riser"), ("drop", ["riffM"], "impact"),
          ("drop", ["riffM2"], None), ("outro", ["soft"], "revcym")],
  "deathcore": [("intro", ["soft", "drone"], "riser"), ("blast", ["riff", "pad"], "impact"), ("blast", ["riffB"], None),
                ("groove", ["riffG"], "impact"), ("groove", ["riffG", "pad"], None), ("break", ["riffBd"], "impact"), ("slam", ["riffSlam"], None),
                ("blast", ["riff", "pad"], "impact"), ("break", ["riffBd", "pad"], "impact"), ("final", ["riffSlam", "pad"], "impact"),
                ("outro", ["soft", "drone"], "revcym")],
  "postrock": [("intro", ["riffClean"], None), ("intro2", ["riffClean", "hookE"], None), ("A", ["riffSoft"], None), ("A2", ["riffH", "hookE"], None),
               ("build", ["riffUp"], "riser"), ("climax", ["riff", "hook"], "impact"), ("climax", ["riff", "hookE"], None),
               ("break", ["riffClean"], "revcym"), ("build", ["riffUp"], "riser"), ("final", ["riff", "hook"], "impact"), ("outro", ["riffClean"], "revcym")],
  "groovemetal": [("intro", ["riffH"], "revcym"), ("verse", ["riffSoft"], "impact"), ("verse", ["riff"], None), ("chorus", ["riffG", "hook"], "impact"),
                  ("verse2", ["riffB"], "impact"), ("chorus", ["riffG", "hook"], "impact"), ("solo", ["riff", "solo"], "impact"),
                  ("break", ["riffH"], "impact"), ("final", ["riffB", "hook"], "impact"), ("outro", ["riffH"], "revcym")],
  "power": [("intro", ["riffC", "pad"], "impact"), ("verse", ["riffSoft"], "impact"), ("verse", ["riff"], None),
            ("chorus", ["riffC", "hook", "pad"], "impact"), ("chorus", ["riffC", "hook", "pad"], None), ("verse2", ["riff"], "impact"),
            ("solo", ["riff", "solo"], "impact"), ("solo", ["riffC", "solo"], None), ("break", ["riffBrk"], "impact"),
            ("final", ["riffC", "hook", "pad"], "impact"), ("final", ["riffC", "hook", "pad"], None), ("outro", ["riffC", "pad"], "revcym")],
  "sludge": [("intro", ["riffD"], "revcym"), ("verse", ["riffSoft"], "impact"), ("verse", ["riff"], None), ("chorus", ["riffG", "hook"], "impact"),
             ("break", ["riffD"], None), ("verse2", ["riffB"], "impact"), ("solo", ["riff", "solo"], "impact"), ("climax", ["riffG", "hook"], "impact"),
             ("outro", ["riffD"], "revcym")],
  "breakcore": [("intro", ["riffP"], None), ("chaos", ["riff"], "impact"), ("chaos", ["riffB"], None), ("break", ["riffP", "pad"], "revcym"),
                ("build", ["riffUp"], "riser"), ("chaos", ["riffM"], "impact"), ("chaos", ["riff"], None), ("outro", ["riffP"], "revcym")],
  "mathcore": [("intro", ["riffJ"], None), ("chaos", ["riff"], "impact"), ("chaos", ["riffB"], None), ("break", ["riffJ"], "revcym"),
               ("chaos", ["riffC"], "impact"), ("slam", ["riffSlam"], None), ("chaos", ["riff"], "impact"), ("outro", ["riffJ"], "revcym")],
  "gojira": [("intro", ["riffN"], "revcym"), ("verse", ["riffSoft"], "impact"), ("verse", ["riff"], None), ("chorus", ["riffW", "hook"], "impact"),
             ("toms", ["riffT"], "impact"), ("verse2", ["riffB"], "impact"), ("chorus", ["riffW", "hook"], "impact"),
             ("break", ["riffN", "drone"], "revcym"), ("final", ["riffT"], "impact"), ("final", ["riffW", "hook"], None), ("outro", ["riffN"], "revcym")],
  "djazz": [("intro", ["riffJ"], None), ("verse", ["riffSoft"], "impact"), ("verse", ["riff", "hook"], None), ("break", ["riffJ2"], "revcym"),
            ("chaos", ["riffC"], "impact"), ("heavy", ["riffB"], "impact"), ("heavy", ["riffB", "hook"], None), ("break", ["riffJ"], "revcym"),
            ("chaos", ["riffC"], "impact"), ("final", ["riff", "hook", "pad"], "impact"), ("outro", ["riffJ2"], "revcym")],
  "raga": [("intro", ["riffA"], None), ("intro2", ["riffG"], None), ("verse", ["riffSoft"], "impact"), ("verse", ["riff", "hook"], None),
           ("break", ["riffG"], "revcym"), ("heavy", ["riffB"], "impact"), ("heavy", ["riffB", "hook"], None), ("break", ["riffBrk"], "impact"),
           ("final", ["riff", "hook"], "impact"), ("outro", ["riffA"], "revcym")],
  "gamelan": [("intro", ["riffK", "drone"], None), ("verse", ["riffSoft"], "impact"), ("verse", ["riff"], None), ("toms", ["riffT"], "impact"),
              ("heavy", ["riffB"], "impact"), ("break", ["riffK", "hook"], "revcym"), ("heavy", ["riff", "hook"], "impact"), ("toms", ["riffT"], None),
              ("final", ["riff", "hook"], "impact"), ("outro", ["riffK", "drone"], "revcym")],
  "koto": [("intro", ["riffK"], None), ("verse", ["riffSoft"], "impact"), ("verse", ["riff"], None), ("chorus", ["riffC", "hook", "pad"], "impact"),
           ("break", ["riffT"], "impact"), ("verse2", ["riff"], "impact"), ("chorus", ["riffC", "hook", "pad"], "impact"), ("break", ["riffK"], "revcym"),
           ("final", ["riffC", "hook", "pad"], "impact"), ("outro", ["riffK"], "revcym")],
  "tech-death": [("blast", ["riff"], "impact"), ("blast", ["riffB", "pad"], None), ("dbeat", ["riffD"], "impact"),
                 ("dbeat", ["riffD", "hook"], None), ("groove", ["riffSoft"], "impact"), ("groove", ["riffG", "pad"], None),
                 ("blast", ["riff", "hook"], "impact"), ("break", ["riffBrk"], "impact"), ("break", ["riffBrk", "drone"], None),
                 ("toms", ["riffT"], "impact"), ("solo", ["riffD", "solo"], "impact"), ("solo", ["riffB", "solo"], None),
                 ("final", ["riff", "hook", "pad"], "impact"), ("outro", ["riffBrk", "soft"], "revcym")],
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
                fv=random.choice(FORM_VARIANTS),
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
# Section energy (0 calm … 1 full) → one automation curve per chapter that drives the riff
# track's level, room, saturation and OTT together. Ramp sections glide into the next.
ENERGY = {"intro": 0.3, "intro2": 0.45, "verse": 0.6, "verse2": 0.65, "pre": 0.7, "build": 0.7, "chorus": 0.85,
          "drop": 0.95, "heavy": 0.85, "blast": 1.0, "dbeat": 0.85, "groove": 0.7, "shuffle": 0.7, "toms": 0.75,
          "space": 0.4, "break": 0.9, "C": 0.8, "C2": 0.8, "solo": 0.85, "final": 1.0, "outro": 0.35, "coda": 0.3,
          "A": 0.6, "A2": 0.7, "B": 0.8, "B2": 0.85, "climax": 1.0, "fast": 1.0, "stop": 0.9, "half": 0.75, "bridge": 0.5, "slam": 0.95, "chaos": 1.0}
RAMPS = {"pre", "build", "intro2"}


def energy_lane(meta):
    """Breakpoints for a chapter from [(section, beats)]: hold each section's energy, 1-beat moves,
    ramps across build sections."""
    pts, t = [], 0.0
    es = [ENERGY.get(sec, 0.7) for sec, _ in meta]
    for i, (sec, ln) in enumerate(meta):
        e = es[i]
        nxt = es[i + 1] if i + 1 < len(es) else e
        pts.append([f"{t:g}b", e])
        if sec in RAMPS:
            pts.append([f"{t + ln - 0.5:g}b", nxt])
        else:
            pts.append([f"{max(t, t + ln - 1):g}b", e])
        t += ln
    pts.append([f"{t:g}b", es[-1]])
    return pts


FILTERED = {"intro": 0.2, "intro2": 0.4}


def filter_lane(meta):
    """0..1 openness per chapter: intros muffled (≈1.4 kHz), builds open up, everything else open."""
    pts, t = [], 0.0
    vals = [FILTERED.get(sec, 1.0) for sec, _ in meta]
    for i, (sec, ln) in enumerate(meta):
        v = vals[i]
        nxt = vals[i + 1] if i + 1 < len(vals) else v
        pts.append([f"{t:g}b", v])
        pts.append([f"{t + ln - 0.5:g}b", nxt if sec in RAMPS else v])
        t += ln
    pts.append([f"{t:g}b", vals[-1]])
    return pts


def energy_fx(style=None):
    wet = {"blackgaze": (0.38, -0.22, "3.5s")}.get(style, (0.28, -0.26, "2.4s"))
    return {"gain": {"value": "-5dB", "mod": [{"src": "auto.energy", "amount": 6}]},
            "fx": [{"type": "drive", "drive": 0.3, "mix": {"value": 0, "mod": [{"src": "auto.energy", "amount": 0.25}]}},
                   {"type": "ott", "time": 0.3, "depth": {"value": 0, "mod": [{"src": "auto.energy", "amount": 0.3}]}},
                   {"type": "reverb", "kind": "hall", "decay": wet[2], "predelay": "25ms", "low_cut": 250,
                    "mix": {"value": wet[0], "mod": [{"src": "auto.energy", "amount": wet[1]}]}}]}
FAVORITES = f"{TOOLS}/favorites.json" if "TOOLS" in globals() else "/home/harry/.config/chirp/tools/favorites.json"

def favorite_for(role, ident):
    """A saved favourite part for `role`, transposed into the song's key (kits don't transpose)."""
    try:
        favs = [f for f in json.load(open("/home/harry/.config/chirp/tools/favorites.json")) if f.get("role") == role]
    except Exception:
        return None
    if not favs or not ident.get("gen") or random.random() > 0.35:
        return None
    f = random.choice(favs)
    tr = (ident["gen"]["pc"] - f["pc"] + 6) % 12 - 6
    return f["part"], tr

FORM_VARIANTS = ["base", "base", "extended", "short", "breakheavy", "shuffle"]
MOD_STEPS = [1, -1, 2, 3, -3, 5, 6, -6]  # half/whole steps, minor thirds, fourth, tritone


def modulation(ident, nsec):
    """Within-chapter modulation (deterministic per song and chapter): half of chapters shift every
    pitched part from a section past the first by a brutal interval. Returns (from_index, semitones)."""
    rng = random.Random(((ident.get("gen") or {}).get("seed", 0)) * 31 + ident.get("chapter", 0) * 7 + 11)
    if nsec < 3 or rng.random() < 0.5:
        return None, 0
    return rng.randrange(1, nsec), rng.choice(MOD_STEPS)
KEEP_END = {"final", "outro", "coda", "climax"}


def form_for(ident):
    """The song's form: the style's base form, varied per song (deterministic from its seed):
    extended (the most intense middle section repeats), short (some middle sections dropped),
    breakheavy (an extra breakdown before the finale), shuffle (middle sections reordered)."""
    base = list(FORMS[STYLES[ident["style"]]["form"]])
    v = ident.get("fv", "base")
    rng = random.Random(((ident.get("gen") or {}).get("seed", 0)) ^ 0x5F3759DF)
    if v == "base" or len(base) < 5:
        return base
    head, tail = base[:1], []
    while len(base) > 2 and base[-1][0] in KEEP_END | {"outro"}:
        tail.insert(0, base.pop())
    mid = base[1:]
    if v == "extended" and mid:
        peak = max(range(len(mid)), key=lambda i: ENERGY.get(mid[i][0], 0.7))
        mid.insert(peak + 1, mid[peak])
    elif v == "short" and len(mid) > 4:
        drop = set(rng.sample(range(len(mid)), max(1, len(mid) // 4)))
        mid = [m for i, m in enumerate(mid) if i not in drop]
    elif v == "breakheavy":
        brks = [m for m in mid if m[0] in ("break", "slam", "stop")]
        if brks:
            mid.append(rng.choice(brks))
        else:
            peak = max(range(len(mid)), key=lambda i: ENERGY.get(mid[i][0], 0.7))
            mid.insert(peak + 1, mid[peak])
    elif v == "shuffle" and len(mid) > 3:
        rng.shuffle(mid)
    return head + mid + tail


def chapters(ident):
    """Split the song's form into consecutive chapters of about PASS_MINUTES each."""
    form = form_for(ident)
    n = max(4, round(ident.get("base_tempo", ident["tempo"]) * PASS_MINUTES / 16))
    chs = [form[i:i + n] for i in range(0, len(form), n)]
    if len(chs) > 1 and len(chs[-1]) < n / 2:
        last = chs.pop()
        chs[-1] = chs[-1] + last
    return chs

COMP_STYLES = ["glue", "pump", "smash", "parallel", "opto", "tape"]
# Loudness-matched to glue (measured RMS over the same 48 beats through each master chain).
FLAVOR_HOOK = {"vintage": ["rack:tape-echo"], "industrial": ["rack:radio"], "space": ["rack:shimmer-hall"], "wide": ["rack:chorus-wide"]}
STYLE_TRIM = {"tool": 2.0, "numetal": 1.0, "industrial": -1.5, "power": -1.0, "sludge": 2.0, "mathcore": 1.5, "gojira": 1.0, "raga": -2.0}  # sparse styles sit lower (QA loudness)
COMP_TRIM = {"glue": 0.0, "pump": 6.1, "smash": 3.4, "parallel": 3.2, "opto": 3.3, "tape": -2.1}

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
    trim = COMP_TRIM.get(comp, 0.0) + STYLE_TRIM.get(ident.get("style"), 0.0)
    eq = [json.loads(MASTER_BASE[0])]
    air = {"brostep": 2.5, "darksynth": 3.0, "tool": 1.5, "industrial": 3.0, "dnb": 2.0, "power": 2.0, "raga": 2.5, "koto": 2.0}.get(ident.get("style"))
    if air:  # QA: these styles measure dark at the top
        eq.append({"type": "eq", "bands": ["peak cutoff=3500 q=0.8 gain=1.5dB", f"highshelf cutoff=8000 gain={air}dB"]
                   + (["peak cutoff=500 q=0.9 gain=-2dB"] if ident.get("style") == "industrial" else [])})
    flavor = (ident.get("gen") or {}).get("flavor", "modern")
    dyn = dyn + (["tape drive=0.45 warmth=0.65"] if flavor == "vintage" else [])
    width = "width width=1.35 mono_below=140" if flavor == "wide" else "width width=1.2 mono_below=140"
    fx = eq + [verb] + dyn + ([f"gain gain={trim:+.1f}dB"] if trim else []) + [width]
    return json.dumps(fx)

def choir_notes(ident):
    """The vocoder choir's carrier chord: the song's tonic with its mode's fifth, octave and third."""
    g = ident.get("gen")
    if not g:
        return None
    k = composer.Key(g["pc"], g["mode"])
    return ",".join(composer.mname(m + ident.get("key", 0)) for m in (k.deg(0, 48), k.deg(4, 48), k.deg(len(k.iv), 48), k.deg(2, 60)))


def set_choir(ident, when="loop"):
    notes = choir_notes(ident)
    if notes:  # best effort: a live song without the choir just rejects this edit
        subprocess.run([C, "live", "set", "--id", "groove", "--when", when, f"tracks.voxchoir.fx.0.notes={notes}"], capture_output=True)


def write_form(name, ident):
    s = STYLES[ident["style"]]
    if ident.get("gen"):
        # Freshly composed melodic parts in their own key: no F-based offsets.
        names, gdesc = composer.compose(ident["style"], name, ident["gen"])
        lens = {role: composer.LENGTHS.get(n, 16) for role, n in names.items()}
        ident = dict(ident, **names)
        ident["solo"] = names.get("solo", names.get("hook"))
        s = dict(s, off=0, riff_off=0, hook_off=0)
    else:
        gdesc, lens = "library parts", {}
    roles = ["drums", "riff", "hook", "pad", "arp", "hold", "drone", "fx"]
    tracks = {t: [] for t in roles}
    flavor = (ident.get("gen") or {}).get("flavor", "modern")
    chs = chapters(ident)
    chapter = chs[min(ident.get("chapter", 0), len(chs) - 1)]
    form_secs = [sec for sec, _, _ in chapter]
    def rest(beats):
        return REST if beats == 16 else f"[ R/8 ]x{int(round(beats * 2))}"
    meta = []
    mod_at, mod_tr = modulation(ident, len(chapter)) if ident.get("gen") else (None, 0)
    for idx, (sec, layers, fx) in enumerate(chapter):
        sec_len = max([lens[l] for l in layers if l in lens] or [16])
        meta.append((sec, sec_len))
        mod = mod_tr if mod_at is not None and idx >= mod_at else 0
        lift = s.get("lift", 2) if sec == "final" else 0
        def put(track, part, off, xf=""):
            if not part:
                tracks[track].append(rest(sec_len))
                return
            t = ident["key"] + off + lift + mod
            tracks[track].append(f"tr={t} @{part}{xf} tr=0" if t else f"@{part}{xf}")
        # Generated riffs carry their own locked drums: library beats only where no riff plays.
        has_riff = any(l.startswith("riff") for l in layers) and ident.get("gen") and ident["style"] in ("djent", "djent-breakdown")
        drum = None if has_riff else next((ident[r] for r in ["high", "mid", "half", "brk", "low"] if r in layers and ident.get(r)), None)
        tracks["drums"].append(f"@{drum}" if drum else rest(sec_len))
        # The motif develops when it returns: rotated/thinned in verse 2, thinned under the solo.
        riff_xf = {"verse2": random.choice(["^rot=0.5", "^rot=1", "^thin=0.2"]), "solo": "^thin=0.35"}.get(sec, "")
        rx = ident.get("xf", {})
        riff_role = next((l for l in layers if l.startswith("riff")), None)
        part = (ident.get(riff_role) or ident.get("riff")) if riff_role else None
        fav = favorite_for(riff_role, ident) if riff_role else None
        if fav:
            t = ident["key"] + fav[1] + mod
            tracks["riff"].append(f"tr={t} @{fav[0]} tr=0" if t else f"@{fav[0]}")
        else:
            put("riff", part, s["riff_off"], riff_xf + rx.get("riff", ""))
        hook_role = next((l for l in layers if l.startswith("hook")), None)
        hook = ident.get("solo", "lead-solo") if "solo" in layers else (ident.get(hook_role) if hook_role else None)
        put("hook", hook, s.get("hook_off", s["off"]), ("^rot=1" if "solo" in layers and ident.get("gen") else "") + rx.get("hook", ""))
        pad = ident["pad"] if "pad" in layers else (ident["soft"] if "soft" in layers else None)
        put("pad", pad, s["off"], rx.get("pad", ""))
        put("arp", ident["arp"] if "arp" in layers else None, s["off"], ("^rev" if sec == "break" else "") + rx.get("arp", ""))
        put("hold", ident["hold"] if "hold" in layers else None, s["off"], rx.get("hold", ""))
        calm = sec in ("intro", "intro2", "break", "outro", "coda", "space")
        put("drone", ident.get("drone") if sec_len == 16 and ("drone" in layers or (calm and ident.get("drone"))) and BUILTIN_FX["drone"] else None, 0)
        nxt_sec = form_secs[idx + 1] if idx + 1 < len(form_secs) else None
        if nxt_sec == "break" and BUILTIN_FX["fx-tapestop"] and random.random() < 0.6:
            fx = "tapestop"
        risers = ["fx-riser"] + [p for p in ["fx-riser-shepard", "fx-riser-noise"] if BUILTIN_FX[p]]
        revs = ["fx-revcym"] + (["fx-reverse"] if BUILTIN_FX["fx-reverse"] else [])
        tracks["fx"].append({"riser": f"{rest(sec_len - 4)} patch={random.choice(risers)} C4/1@90",
                             "impact": f"patch=fx-impact F1/4@104 {rest(sec_len - 1)}",
                             "revcym": f"{rest(sec_len - 2)} patch={random.choice(revs)} C5/2@88",
                             "tapestop": f"{rest(sec_len - 4)} patch=fx-tapestop C4/1@100"}.get(fx, rest(sec_len)))
    modn = f", modulates {mod_tr:+d} at section {mod_at + 1}" if mod_at is not None else ""
    lines = [f"about: Generated {s['form']}-form song ({ident.get('fv', 'base')}) — {ident['style']} at {ident['tempo']} BPM, {gdesc}, shift {ident['key']:+d}{modn}, chapter {ident.get('chapter', 0) + 1}/{len(chs)}, comp {ident.get('comp', 'glue')}.",
             f"tempo: {ident['tempo']}", "tracks:"]
    for t, items in tracks.items():
        if t == "hook" and FLAVOR_HOOK.get(flavor):
            lines.append("  - " + json.dumps({"name": t, "score": " ".join(items), "fx": composer.expand(FLAVOR_HOOK[flavor])}))
        elif t == "riff":
            efx = energy_fx(ident["style"])
            efx["fx"] = [{"type": "filter", "kind": "lp", "cutoff": {"value": 700, "mod": [{"src": "auto.filt", "amount": 5}]}}] + efx["fx"]
            lines.append("  - " + json.dumps(dict({"name": t, "score": " ".join(items), "auto": {"energy": {"points": energy_lane(meta)}, "filt": {"points": filter_lane(meta)}}}, **efx)))
        else:
            lines.append(f"  - {{name: {t}, score: \"{' '.join(items)}\"}}")
    open(f"{SONGS}/{name}.yaml", "w").write("\n".join(lines) + "\n")

TOOLS = "/home/harry/.config/chirp/tools"
JOURNEY = f"{TOOLS}/journey.json"
# How heavy each style is (0 lofi … 1 djent).
HEAVY = {"raga": 0.9, "gamelan": 0.9, "koto": 0.9, "djazz": 0.9, "gojira": 1.0, "mathcore": 1.0, "sludge": 0.95, "breakcore": 0.9, "power": 0.9, "groovemetal": 0.95, "deathcore": 1.0, "postrock": 0.6, "numetal": 0.9, "industrial": 0.85, "dnb": 0.8, "blackgaze": 0.95, "darksynth": 0.8, "hardcore-kl": 1.0, "brostep": 0.8, "thrash": 0.9, "tool": 0.9, "tech-death": 1.0, "meshuggah": 1.0, "lofi": 0.0, "classical": 0.05, "house": 0.2, "garage": 0.25, "poly": 0.35, "prog-clean": 0.4, "acid": 0.45,
         "idm": 0.55, "doom-ambient": 0.6, "hardcore": 0.7, "djent-breakdown": 0.85, "djent": 1.0}

STYLE_QUEUE = []

def journey_load():
    try:
        return json.load(open(JOURNEY))
    except Exception:
        return {"on": False, "h": 0.0, "rate": 0.09, "passes_per_song": 2}

def journey_style(h, current):
    """Pick a style near heaviness h; at full heaviness: mostly djent, sometimes breakdown/clean/excursion."""
    r = random.random()
    if h >= 0.95:  # full heaviness: mostly meshuggah, then djent; breakdowns; rare clean/excursions
        if r < 0.12:
            return "djent-breakdown"
        if r < 0.16:
            return random.choice(["prog-clean", "poly"])
        if r < 0.2:
            return random.choice([k for k in STYLES if k not in ("djent", "meshuggah", current)])
        x = random.random()
        mix = [("meshuggah", 0.26), ("hardcore-kl", 0.1), ("tech-death", 0.09), ("thrash", 0.09), ("tool", 0.09), ("djent", 0.07),
               ("brostep", 0.07), ("blackgaze", 0.06), ("darksynth", 0.04), ("numetal", 0.05), ("industrial", 0.05), ("dnb", 0.03),
               ("deathcore", 0.06), ("postrock", 0.03), ("groovemetal", 0.05), ("power", 0.04), ("sludge", 0.04), ("breakcore", 0.03), ("mathcore", 0.04), ("gojira", 0.06), ("djazz", 0.05), ("raga", 0.04), ("gamelan", 0.03), ("koto", 0.03)]
        for name, w in mix:
            x -= w
            if x <= 0:
                return name
        return "meshuggah"
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
    elif op == "then":
        STYLE_QUEUE.extend(args)
        return ident, f"then {' '.join(STYLE_QUEUE)}"
    elif op == "mutate":
        ident, k = mutate(ident)
        return ident, f"mutate {k}"
    else:
        raise ValueError(f"unknown steer command {cmd!r}")
    return ident, cmd

ARCHIVE = os.path.expanduser("~/.cache/chirp/played")

def archive(name, ident):
    """Keep a copy of every chapter that starts playing (form + its generated parts), so a
    "this slaps" can be saved later by time with tools/fav.py."""
    if not name or not ident:
        return
    try:
        import glob, shutil
        d = os.path.join(ARCHIVE, time.strftime("%Y%m%d-%H%M%S") + f"-{name}")
        os.makedirs(d, exist_ok=True)
        for f in [f"{SONGS}/{name}.yaml"] + glob.glob(f"{SONGS}/gen-{name}-*.yaml"):
            shutil.copy(f, d)
        open(os.path.join(d, "ident.json"), "w").write(json.dumps(ident, indent=1))
        for old in sorted(glob.glob(os.path.join(ARCHIVE, "*")))[:-200]:
            shutil.rmtree(old, ignore_errors=True)
    except Exception as e:
        print(time.strftime("%T"), f"archive failed: {e}", flush=True)

def save_state(**kw):
    kw["queue"] = list(STYLE_QUEUE)
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
            seen = -1  # the first status is a real pass change: continue the song's chapters
            print(time.strftime("%T"), f"resumed: playing {playing} {ident['style']}", flush=True)
        except Exception as e:
            print(time.strftime("%T"), f"resume failed: {e}", flush=True)
    try:
        STYLE_QUEUE.extend(json.load(open(STATE)).get("queue", []))
    except Exception:
        pass
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
            archive(playing, playing_ident)
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
                x = random.random()
                if x < 0.35:  # key change at the chapter boundary
                    ident["key"] = max(-6, min(6, ident.get("key", 0) + random.choice(MOD_STEPS)))
                    change += f", key {ident['key']:+d}"
                elif x < 0.6 and ident.get("gen"):  # scale change: same motifs, new mode
                    modes = [m for m in composer.STYLE_MODES.get(ident["style"], []) if m != ident["gen"]["mode"]]
                    if modes:
                        m = random.choice(modes)
                        ident["gen"] = dict(ident["gen"], mode=m, prog=random.choice(composer.PROGS[m]))
                        change += f", mode {m}"
            elif not first or passes > 1:
                queued = bool(STYLE_QUEUE)
                style = STYLE_QUEUE.pop(0) if STYLE_QUEUE else (journey_style(j.get("h", 0), ident["style"]) if j.get("on") else random.choice([k for k in STYLES if k != ident["style"]]))
                prev_bpm = ident.get("tempo", 120)
                fav_songs = []
                try:
                    fav_songs = [f["song"] for f in json.load(open("/home/harry/.config/chirp/tools/favorites.json")) if "song" in f]
                except Exception:
                    pass
                for _ in range(8):  # keep tempos moving: at least 14 BPM from the last song
                    cand = identity(style)
                    if fav_songs and not queued and random.random() < 0.15:  # a favourite returns, moved
                        fs = dict(random.choice(fav_songs))
                        bpm = max(90, min(150, fs["base_tempo"] + random.choice([-16, -10, 10, 16])))
                        cand = dict(fs, tempo=bpm, base_tempo=bpm, chapter=0, key=random.choice([-2, -1, 1, 2]), comp=random.choice(COMP_STYLES))
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
            set_choir(ident)
            print(time.strftime("%T"), f"pass {li}: next {name} ({change}) {ident['style']} {ident['tempo']}bpm key{ident['key']:+d} riff={ident['riff']} hook={ident['hook']}" + ("" if ok is not None else "  (rejected)"), flush=True)
            save_state(playing=playing, playing_ident=playing_ident, next=nxt, next_ident=nxt_ident, loop_index=li)
        # Steering: apply to the song playing now (cut at the next bar, same position),
        # then carry the change into the queued next song and re-queue it.
        cmds = [l.strip() for l in open(STEER).read().splitlines() if l.strip() and not l.startswith("#")]
        if cmds:
            open(STEER, "w").close()
            for cmd in cmds:
                try:
                    if cmd.split()[0] == "then":
                        _, desc = steer(ident, cmd)
                        print(time.strftime("%T"), f"steer: {desc}", flush=True)
                        continue
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
                        set_choir(playing_ident, "bar")
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
