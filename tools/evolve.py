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
  "postmetal":  dict(form="postmetal", tempo=(60, 84), off=0, riff=["riff-taps"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
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
  "lofihop": dict(form="lofihop", tempo=(70, 90), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "gogo": dict(form="gogo", tempo=(112, 140), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "ukjazz": dict(form="ukjazz", tempo=(88, 112), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "ambient": dict(form="ambient", tempo=(60, 80), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "downtempo": dict(form="downtempo", tempo=(88, 104), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "smile": dict(form="smile", tempo=(80, 132), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "house-melodic": dict(form="house-melodic", tempo=(118, 124), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "chamber": dict(form="chamber", tempo=(60, 100), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "triphop": dict(form="triphop", tempo=(68, 88), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "neoclassical": dict(form="neoclassical", tempo=(60, 84), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "ballad": dict(form="ballad", tempo=(60, 76), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "bossa": dict(form="bossa", tempo=(120, 140), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "dub": dict(form="dub", tempo=(66, 80), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "manouche": dict(form="manouche", tempo=(110, 150), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "celtic": dict(form="celtic", tempo=(60, 90), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "doomjazz": dict(form="doomjazz", tempo=(40, 60), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "mali": dict(form="mali", tempo=(90, 112), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "guofeng": dict(form="guofeng", tempo=(64, 90), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "vaporwave": dict(form="vaporwave", tempo=(72, 92), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "slowcore": dict(form="slowcore", tempo=(56, 76), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "backrooms": dict(form="backrooms", tempo=(60, 84), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "cyberscape": dict(form="cyberscape", tempo=(80, 100), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "neosoul": dict(form="neosoul", tempo=(76, 94), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "minimal": dict(form="minimal", tempo=(120, 140), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "fusion": dict(form="fusion", tempo=(72, 104), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "berlin": dict(form="berlin", tempo=(100, 124), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "satie": dict(form="satie", tempo=(56, 72), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "kankyo": dict(form="kankyo", tempo=(66, 88), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "dawnraga": dict(form="dawnraga", tempo=(60, 84), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "handpan": dict(form="handpan", tempo=(68, 84), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
  "citypop": dict(form="citypop", tempo=(104, 122), off=0, riff=["keys-lofi"], riff_off=0, lift=0,
                     low=["beat-sparse"], mid=["beat-lofi"], high=["beat-lofi"], half=["beat-sparse"], brk=["beat-sparse"],
                     hook=["lead-hook"], pad=["pad-dark"], soft=["pad-swell"], arp=["arp-16th"], hold=["pad-swell"]),
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
  "postmetal": [("intro", ["riffClean"], None), ("build", ["riffToms", "hookE"], "riser"), ("A", ["riffCrush"], "impact"),
                ("A2", ["riffCrush", "hookT"], None), ("break", ["riffClean", "hookE"], "revcym"), ("build", ["riffToms"], "riser"),
                ("climax", ["riffWall"], "impact"), ("climax", ["riffWall", "hookT"], None), ("outro", ["riffClean"], "revcym")],
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
  "lofihop": [("intro", ["riffI"], None), ("A", ["riff", "hook"], None), ("A", ["riff"], None), ("B", ["riffB", "hook"], None),
              ("A2", ["riff", "arp"], None), ("B", ["riffB", "hook"], None), ("outro", ["riffI"], "revcym")],
  "gogo": [("intro", ["riffP"], None), ("A", ["riffS"], None), ("A", ["riff"], None), ("build", ["riffUp"], "riser"), ("B", ["riffB"], "impact"),
           ("break", ["riffP"], None), ("B2", ["riffB"], None), ("outro", ["riffP"], None)],
  "ukjazz": [("intro", ["riffK"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB", "hook"], None),
             ("solo", ["riffB", "solo"], None), ("final", ["riff", "hook"], None), ("outro", ["riffK"], None)],
  "ambient": [("intro", ["riffA"], None), ("A", ["riffA", "hookE"], None), ("B", ["riffB"], None), ("B2", ["riffB", "hookE"], None),
              ("A", ["riffA"], None), ("outro", ["riffA"], None)],
  "downtempo": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("break", ["riffI"], None),
                ("B", ["riffB", "hook"], None), ("outro", ["riffI"], None)],
  "smile": [("intro", ["riffQ"], None), ("A", ["riff"], None), ("A2", ["riff", "hookE"], None), ("B", ["riff5"], None), ("B2", ["riffF", "hookE"], None),
            ("break", ["riffQ"], None), ("final", ["riffF", "hookE"], None), ("outro", ["riffQ"], None)],
  "house-melodic": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("break", ["riffI"], "revcym"),
                    ("build", ["riffB"], "riser"), ("drop", ["riffB", "hook"], "impact"), ("A", ["riff"], None), ("outro", ["riffI"], None)],
  "chamber": [("A", ["riffN"], None), ("A", ["riffQ"], None), ("B", ["riffM"], None), ("B2", ["riffQ"], None), ("A", ["riffN2"], None), ("coda", ["riffN"], None)],
  "triphop": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB"], None), ("B2", ["riffB", "hook"], None),
              ("break", ["riffI"], None), ("A2", ["riff", "hook"], None), ("outro", ["riffI"], None)],
  "neoclassical": [("intro", ["riffP"], None), ("A", ["riff"], None), ("A2", ["riff", "hookE"], None), ("B", ["riffB"], None),
                   ("B2", ["riffB", "hookE"], None), ("A", ["riffP"], None), ("outro", ["riffP"], None)],
  "ballad": [("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB", "hook"], None), ("A2", ["riff", "hook"], None), ("outro", ["riffB"], None)],
  "bossa": [("intro", ["riffG"], None), ("A", ["riff", "hook"], None), ("A", ["riff"], None), ("B", ["riffB", "hook", "pad"], None),
            ("A2", ["riff", "hook"], None), ("outro", ["riffG"], None)],
  "dub": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("break", ["riffD"], None),
          ("B", ["riff", "hook"], None), ("break", ["riffD"], None), ("outro", ["riffI"], None)],
  "manouche": [("intro", ["riffG"], None), ("A", ["riff", "hook"], None), ("A", ["riffB", "hook"], None), ("solo", ["riff", "solo"], None),
               ("solo", ["riffB", "solo"], None), ("A2", ["riff", "hook"], None), ("outro", ["riffG"], None)],
  "celtic": [("intro", ["riffI"], None), ("A", ["riff", "hook"], None), ("A2", ["riff", "hookB"], None), ("B", ["riffB", "hook"], None),
             ("B2", ["riffB", "hookB"], None), ("break", ["riffI"], None), ("A2", ["riffB", "hook"], None), ("outro", ["riffI"], None)],
  "doomjazz": [("intro", ["riffI"], None), ("A", ["riff", "hookE"], None), ("A2", ["riff"], None), ("B", ["riffB", "hook"], None),
               ("A2", ["riff", "hookE"], None), ("outro", ["riffI"], None)],
  "mali": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB"], None),
           ("B2", ["riffB", "hook"], None), ("break", ["riffI"], None), ("A2", ["riff", "hook"], None), ("outro", ["riffI"], None)],
  "guofeng": [("intro", ["riffI"], None), ("A", ["riff", "hookE"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB", "hook"], None),
              ("break", ["riffI", "hookE"], None), ("A2", ["riffB", "hook"], None), ("outro", ["riffI"], None)],
  "vaporwave": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB", "hook"], None),
                ("break", ["riffI"], None), ("A2", ["riffB", "hook"], None), ("outro", ["riffI"], None)],
  "slowcore": [("intro", ["riffI"], None), ("A", ["riff", "hookE"], None), ("A2", ["riff"], None), ("B", ["riffB", "hook"], None),
               ("A2", ["riffB", "hookE"], None), ("outro", ["riffI", "hookE"], None)],
  "backrooms": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riffF"], None), ("break", ["riffD"], None),
                ("B", ["riffF"], None), ("A2", ["riffD"], None), ("outro", ["riffI"], None)],
  "cyberscape": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB", "hook"], None),
                 ("break", ["riffI", "hook"], None), ("B2", ["riffB"], None), ("outro", ["riffI"], None)],
  "neosoul": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB", "hook"], None),
              ("break", ["riffI", "hook"], None), ("A2", ["riffB", "hook"], None), ("outro", ["riffI"], None)],
  "minimal": [("intro", ["riffP"], None), ("A", ["riffP"], None), ("A2", ["riffA"], None), ("B", ["riff"], None), ("B2", ["riffF", "hook"], None),
              ("break", ["riffA"], None), ("B2", ["riffF", "hook"], None), ("outro", ["riffP"], None)],
  "fusion": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB", "hook"], None),
             ("break", ["riffI", "hook"], None), ("A2", ["riffB"], None), ("outro", ["riffI"], None)],
  "berlin": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB"], None),
             ("B2", ["riffD", "hook"], None), ("break", ["riffI", "hook"], None), ("B2", ["riffB", "hook"], None), ("outro", ["riff"], None)],
  "satie": [("intro", ["riffP"], None), ("A", ["riff"], None), ("B", ["riffB"], None), ("A2", ["riff"], None), ("outro", ["riffP"], None)],
  "kankyo": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riffW"], None), ("B", ["riffW", "hook"], None),
             ("A2", ["riff", "hook"], None), ("outro", ["riffI"], None)],
  "dawnraga": [("alap", ["riffA"], None), ("alap", ["riffA"], None), ("jor", ["riffJ"], None), ("jor", ["riffJ", "hookE"], None),
               ("gat", ["riffG", "hook"], None), ("gat", ["riffG", "hook"], None), ("outro", ["riffA"], None)],
  "handpan": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB"], None),
              ("B2", ["riffB", "hook"], None), ("A2", ["riff", "hook"], None), ("outro", ["riffI"], None)],
  "citypop": [("intro", ["riffI"], None), ("A", ["riff"], None), ("A2", ["riff", "hook"], None), ("B", ["riffB", "hook"], None),
              ("break", ["riffI", "hook"], None), ("B", ["riffB", "hook"], None), ("outro", ["riffI"], None)],
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
    if style in composer.CHILL_STYLES:
        return dict(style=style, tempo=bpm, base_tempo=bpm, chapter=0, key=0, gen=composer.params(style), comp=random.choice(["opto", "tape", "glue"]),
                    fv=random.choice(["base", "base", "extended", "short", "shuffle"]),
                    **{r: pick(s, r) for r in ["riff", "low", "mid", "high", "half", "brk", "hook", "pad", "soft", "arp", "hold"]})
    return dict(style=style, tempo=bpm, base_tempo=bpm, chapter=0, key=0, gen=composer.params(style), comp=random.choice(COMP_STYLES),
                fv=random.choice(FORM_VARIANTS) if style not in composer.CHILL_STYLES else "base",
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
          "A": 0.6, "A2": 0.7, "B": 0.8, "B2": 0.85, "climax": 1.0, "fast": 1.0, "stop": 0.9, "half": 0.75, "bridge": 0.5, "slam": 0.95, "chaos": 1.0, "guest": 0.85, "end": 0.9}
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


def generic_texture(style, meta, rng, prefix="g"):
    """Two or three modulators drawn per chapter from a palette, rates/depths/directions re-rolled:
    breathing filter, drifting wow, wearing grit, reverb tide, delay swell, slow phaser, tremolo tide,
    tape-skip creep, section high-pass sweep; warped styles add pitch drift."""
    total = sum(ln for _, ln in meta) or 16
    up = rng.random() < 0.6
    ramp = lambda a, b: {"points": [["0b", a if up else b], [f"{total:g}b", b if up else a]]}
    L = lambda nm: f"{prefix}{nm}"
    pal = {
        "breathe": lambda: ({L("br"): {"wave": "sine", "rate": f"{rng.uniform(0.03, 0.12):.3f}hz"}}, {},
                            [{"type": "filter", "kind": "lp", "cutoff": {"value": rng.choice([2500, 3500, 5000, 6500]), "mod": [{"src": f"lfo.{L('br')}", "amount": round(rng.uniform(0.6, 1.0), 2)}]}}]),
        "wow": lambda: ({}, {L("wow"): ramp(0.25, round(rng.uniform(0.8, 1.0), 2))},
                        [{"type": "chorus", "rate": round(rng.uniform(0.3, 0.7), 2), "voices": 1, "depth": round(rng.uniform(0.2, 0.4), 2), "mix": {"value": 0, "mod": [{"src": f"auto.{L('wow')}", "amount": 1.0}]}}]),
        "grit": lambda: ({}, {L("grit"): ramp(0.0, round(rng.uniform(0.3, 0.55), 2))},
                         [{"type": "crush", "bits": rng.choice([10, 11, 12]), "rate": rng.choice([12000, 16000]), "mix": {"value": 0, "mod": [{"src": f"auto.{L('grit')}", "amount": 1.0}]}}]),
        "tide": lambda: ({L("tide"): {"wave": "sine", "rate": f"{rng.uniform(0.02, 0.05):.3f}hz"}}, {},
                         [{"type": "reverb", "kind": "hall", "decay": f"{rng.uniform(3, 6):.1f}s", "predelay": "35ms", "low_cut": 200, "mix": {"value": 0.24, "mod": [{"src": f"lfo.{L('tide')}", "amount": 0.15}]}}]),
        "swell": lambda: ({L("dfb"): {"wave": "sine", "rate": f"{rng.uniform(0.03, 0.06):.3f}hz"}}, {},
                          [{"type": "delay", "time": rng.choice(["3/16", "1/4", "3/8"]), "ping_pong": True, "tone": 2600,
                            "feedback": {"value": 0.3, "mod": [{"src": f"lfo.{L('dfb')}", "amount": 0.2}]}, "mix": {"value": 0.1, "mod": [{"src": f"lfo.{L('dfb')}", "amount": 0.08}]}}]),
        "phase": lambda: ({}, {}, [{"type": "phaser", "rate": round(rng.uniform(0.05, 0.2), 3), "depth": round(rng.uniform(0.4, 0.7), 2), "stages": rng.choice([4, 6]), "feedback": 0.3, "mix": 0.3}]),
        "trem": lambda: ({}, {}, [{"type": "tremolo", "rate": round(rng.uniform(2, 5), 2), "depth": round(rng.uniform(0.1, 0.25), 2)}]),
        "skips": lambda: ({}, {L("skip"): ramp(0.0, round(rng.uniform(0.12, 0.25), 2))},
                          [{"type": "stutter", "slice": rng.choice(["1/16", "1/8"]), "repeats": 2, "reverse": rng.random() < 0.5, "seed": rng.randrange(1000),
                            "chance": {"value": 0, "mod": [{"src": f"auto.{L('skip')}", "amount": 1.0}]}}]),
        "hpsweep": lambda: ({}, {L("hp"): {"points": [[f"{sum(ln for _, ln in meta[:i]):g}b", 1.0 if sec in ("intro", "break", "outro") else 0.0] for i, (sec, _) in enumerate(meta)] + [[f"{total:g}b", 0.0]]}},
                            [{"type": "filter", "kind": "hp", "cutoff": {"value": 30, "mod": [{"src": f"auto.{L('hp')}", "amount": 3.5}]}}]),
    }
    names = list(pal)
    picks = rng.sample(names, rng.choice([2, 2, 3]))
    if style in WARP or style in ("vaporwave", "backrooms"):
        pal["drift"] = lambda: ({L("dr"): {"wave": "sine", "rate": f"{rng.uniform(0.04, 0.09):.3f}hz"}}, {},
                                [{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": f"lfo.{L('dr')}", "amount": round(rng.uniform(0.15, 0.35), 2)}]}, "grain": "70ms", "mix": 1.0}])
        picks.append("drift")
    T = {"lfo": {}, "auto": {}, "fx": [], "picks": picks}
    for nm in picks:
        lf, au, fx = pal[nm]()
        T["lfo"].update(lf); T["auto"].update(au); T["fx"] += fx
    return T


def texture(style, meta, rng=None):
    """Evolving timbre lanes for a chill chapter's riff track: LFOs and automation over effect
    parameters (wow, breathing filters, wearing tape grit, reverb tides, filter sweeps).
    Returns {lfo, auto, fx}."""
    total = sum(ln for _, ln in meta) or 16
    ramp = lambda a, b: {"points": [["0b", a], [f"{total:g}b", b]]}
    sweep = {"points": [[f"{sum(ln for _, ln in meta[:i]):g}b", 0.0 if sec in ("break", "build", "intro") else 1.0] for i, (sec, _) in enumerate(meta)]
                       + [[f"{total:g}b", 1.0]]}
    breathe = lambda hz, base, amt: ({"br": {"wave": "sine", "rate": f"{hz}hz"}},
                                     {"type": "filter", "kind": "lp", "cutoff": {"value": base, "mod": [{"src": "lfo.br", "amount": amt}]}})
    wow = {"type": "chorus", "rate": 0.55, "depth": 0.22, "voices": 1, "mix": 1.0}
    T = {}
    if style == "lofihop":
        lfo, flt = breathe(0.07, 3800, 0.9)
        T = {"lfo": lfo, "auto": {"grit": ramp(0.05, 0.45)},
             "fx": [wow, flt, {"type": "crush", "bits": 10, "rate": 12000, "mix": {"value": 0, "mod": [{"src": "auto.grit", "amount": 0.6}]}}]}
    elif style == "ambient":
        lfo, flt = breathe(0.04, 5000, 1.0)
        lfo["tide"] = {"wave": "sine", "rate": "0.03hz"}
        T = {"lfo": lfo, "fx": [flt, {"type": "chorus", "rate": 0.2, "depth": 0.5, "voices": 2, "mix": {"value": 0.25, "mod": [{"src": "lfo.tide", "amount": 0.2}]}},
                                {"type": "reverb", "kind": "hall", "decay": "6s", "predelay": "40ms", "low_cut": 200, "mix": {"value": 0.3, "mod": [{"src": "lfo.tide", "amount": 0.18}]}}]}
    elif style == "gogo":
        T = {"auto": {"open": ramp(0.55, 1.0)},
             "fx": [{"type": "filter", "kind": "lp", "cutoff": {"value": 900, "mod": [{"src": "auto.open", "amount": 4.5}]}},
                    {"type": "tape", "drive": {"value": 0.1, "mod": [{"src": "auto.open", "amount": 0.25}]}, "warmth": 0.4}]}
    elif style == "ukjazz":
        T = {"lfo": {"warm": {"wave": "sine", "rate": "0.05hz"}},
             "fx": [{"type": "tape", "drive": {"value": 0.25, "mod": [{"src": "lfo.warm", "amount": 0.15}]}, "warmth": 0.6},
                    {"type": "chorus", "rate": 0.4, "depth": 0.3, "voices": 2, "mix": {"value": 0.2, "mod": [{"src": "lfo.warm", "amount": 0.15}]}}]}
    elif style == "downtempo":
        lfo, flt = breathe(0.06, 4500, 0.8)
        lfo["dub"] = {"wave": "sine", "rate": "0.04hz"}
        T = {"lfo": lfo, "fx": [flt, {"type": "delay", "time": "3/16", "ping_pong": True, "tone": 2500,
                                      "feedback": {"value": 0.3, "mod": [{"src": "lfo.dub", "amount": 0.2}]}, "mix": {"value": 0.12, "mod": [{"src": "lfo.dub", "amount": 0.1}]}}]}
    elif style == "smile":
        T = {"lfo": {"fb": {"wave": "sine", "rate": "0.05hz"}},
             "fx": [dict(wow, depth=0.12), {"type": "delay", "time": "1/4", "tone": 2400, "feedback": {"value": 0.3, "mod": [{"src": "lfo.fb", "amount": 0.25}]},
                                            "mix": {"value": 0.12, "mod": [{"src": "lfo.fb", "amount": 0.08}]}}]}
    elif style == "house-melodic":
        lfo, flt = breathe(0.08, 6000, 0.8)
        T = {"lfo": lfo, "auto": {"hpf": {"points": [[p_[0], 1 - p_[1]] for p_ in sweep["points"]]}},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": {"value": 30, "mod": [{"src": "auto.hpf", "amount": 4.5}]}}, flt]}
    elif style == "chamber":
        T = {"lfo": {"hall": {"wave": "sine", "rate": "0.02hz"}},
             "fx": [{"type": "reverb", "kind": "hall", "decay": "3.2s", "predelay": "30ms", "low_cut": 150, "mix": {"value": 0.18, "mod": [{"src": "lfo.hall", "amount": 0.08}]}}]}
    rng = rng or random.Random(0)
    G = generic_texture(style, meta, rng)
    if not T:  # styles without a hand-made lane get the full generated set
        return G
    # hand-made lanes gain one generated modulator on top
    one = generic_texture(style, meta, rng, prefix="x")
    nm = one["picks"][0]
    extra = generic_texture(style, meta, random.Random(rng.random()), prefix="x")
    T = dict(T, lfo=dict(T.get("lfo", {}), **one["lfo"]), auto=dict(T.get("auto", {}), **one["auto"]), fx=list(T.get("fx", [])) + one["fx"][:1], picks=[nm])
    return T


HOOK_LIVE = {"lfo": {"fbk": {"wave": "sine", "rate": "0.04hz"}},
             "fx": [{"type": "delay", "time": "3/16", "ping_pong": True, "tone": 3000, "feedback": {"value": 0.35, "mod": [{"src": "lfo.fbk", "amount": 0.2}]}, "mix": 0.18},
                    "reverb kind=hall decay=3s mix=0.22 predelay=30ms low_cut=250"]}


def energy_fx(style=None):
    if style in composer.CHILL_STYLES:
        return {"gain": {"value": "-3dB", "mod": [{"src": "auto.energy", "amount": 4}]},
                "fx": [{"type": "reverb", "kind": "hall", "decay": "2.8s", "predelay": "30ms", "low_cut": 200,
                        "mix": {"value": 0.3, "mod": [{"src": "auto.energy", "amount": -0.18}]}}]}
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
GROOVY = {"numetal", "groovemetal", "djazz", "sludge", "gojira", "hardcore-kl", "industrial"}
FEELS = ["", "^push=0.015", "^sw=0.56", "^push=0.025", "^sw=0.6"]  # per song: straight, laid back, swung
MOD_STEPS = [1, -1, 2, 3, -3, 5, 6, -6]  # half/whole steps, minor thirds, fourth, tritone


METRIC = [(3, 2), (2, 3), (4, 3), (3, 4)]
STEADY = {"lofihop", "ambient", "downtempo", "house-melodic", "chamber", "triphop", "neoclassical", "ballad", "bossa", "dub", "manouche", "celtic", "doomjazz", "mali", "guofeng", "vaporwave", "slowcore", "neosoul", "minimal", "fusion", "berlin", "satie", "kankyo", "dawnraga", "handpan", "citypop"}  # chill styles that hold key and tempo


WARP = {"backrooms"}


def metric_map(ident, meta):
    """Metric modulation (deterministic per song and chapter): ~a third of chapters change tempo by
    3:2, 2:3, 4:3 or 3:4 at a section past the first, half of them returning at a later section.
    Returns (tempo map or None, description)."""
    rng = random.Random(((ident.get("gen") or {}).get("seed", 0)) * 17 + ident.get("chapter", 0) * 5 + 3)
    if ident["style"] in WARP:  # wonky, warped tape time: a random walk with occasional tape dips
        t0, total, d, pts = ident["tempo"], sum(ln for _, ln in meta), 0.0, []
        for at in range(0, int(total), 2):
            d = max(-0.09, min(0.09, d + rng.uniform(-0.03, 0.03)))
            pts.append({"at": at, "bpm": round(t0 * (1 + d), 2)})
            if rng.random() < 0.08:  # the tape drags for half a beat
                pts.append({"at": at + 1, "bpm": round(t0 * (1 + d) * rng.uniform(0.8, 0.9), 2)})
                pts.append({"at": at + 1.5, "bpm": round(t0 * (1 + d), 2)})
        return pts, ", warped time"
    if ident["style"] in STEADY or len(meta) < 3 or rng.random() > 0.33:
        return None, ""
    t0 = ident["tempo"]
    for _ in range(6):
        a, b = rng.choice(METRIC)
        if 60 <= t0 * a / b <= 240:
            break
    else:
        return None, ""
    m = rng.randrange(1, len(meta))
    starts = [sum(ln for _, ln in meta[:i]) for i in range(len(meta) + 1)]
    pts = [{"at": 0, "bpm": t0}, {"at": starts[m], "bpm": round(t0 * a / b, 2)}]
    desc = f", metric {a}:{b} at section {m + 1}"
    if m + 1 < len(meta) and rng.random() < 0.5:
        back = rng.randrange(m + 1, len(meta))
        pts.append({"at": starts[back], "bpm": t0})
        desc += f" (back at {back + 1})"
    return pts, desc


def modulation(ident, nsec):
    """Within-chapter modulation (deterministic per song and chapter): half of chapters shift every
    pitched part from a section past the first by a brutal interval. Returns (from_index, semitones)."""
    rng = random.Random(((ident.get("gen") or {}).get("seed", 0)) * 31 + ident.get("chapter", 0) * 7 + 11)
    if ident["style"] in STEADY or nsec < 3 or rng.random() < 0.5:
        return None, 0
    return rng.randrange(1, nsec), rng.choice(MOD_STEPS)
KEEP_END = {"final", "outro", "coda", "climax"}


def add_guests(ident, form, rng):
    """Slot guest sections (other styles' generators in this song's key) into the middle of the form:
    ~60% of songs get one, some of those two."""
    if not ident.get("gen") or ident["style"] not in (composer.HEAVY_STYLES | composer.CHILL_STYLES) or len(form) < 4:
        return form
    if ident["style"] in ("ukjazz",):  # odd-meter sections: guests (16 beats) would not fit its lengths
        return form
    x = rng.random()
    n = 0 if x < 0.4 else (1 if x < 0.85 else 2)
    form = list(form)
    for i in range(1, n + 1):
        pos = rng.randrange(2, len(form) - 1)
        form.insert(pos, ("guest", [f"riffGuest{i}"], "impact"))
    return form


def form_for(ident):
    """The song's form: the style's base form, varied per song (deterministic from its seed):
    extended (the most intense middle section repeats), short (some middle sections dropped),
    breakheavy (an extra breakdown before the finale), shuffle (middle sections reordered)."""
    base = list(FORMS[STYLES[ident["style"]]["form"]])
    v = ident.get("fv", "base")
    rng = random.Random(((ident.get("gen") or {}).get("seed", 0)) ^ 0x5F3759DF)
    base = add_guests(ident, base, rng)
    if ident.get("gen") and ident["style"] in composer.HEAVY_STYLES:  # a real ending, sometimes
        x = rng.random()
        if base[-1][0] == "outro" and x < 0.4:
            base = base[:-1] + [("end", ["riffEnd"], "impact")]
        elif base[-1][0] == "final" and x < 0.25:
            base = base + [("end", ["riffEnd"], None)]
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
        if ident["style"] == "meshuggah":  # a different breakdown, not a repeat
            mid.append(("break", [rng.choice(["riffBrk2", "riffSlam"])], "impact"))
        elif brks:
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
STYLE_TRIM = {"darksynth": -2.0, "postmetal": 2.0, "tool": 2.0, "numetal": 1.0, "industrial": -1.5, "power": -1.0, "sludge": 2.0, "mathcore": 1.5, "gojira": 1.0, "raga": -2.0,
              "lofihop": 3.0, "ambient": 1.5, "house-melodic": -2.0, "chamber": 0.0, "neoclassical": 1.5, "dub": 3.0, "manouche": 3.0, "celtic": 3.0, "doomjazz": 4.0, "guofeng": 3.0, "vaporwave": 3.0, "backrooms": 10.0, "cyberscape": 2.0, "fusion": 3.0, "berlin": 1.0, "satie": 6.0, "kankyo": 6.0, "citypop": 2.0, "triphop": -2.0}  # sparse styles sit lower (QA loudness)
COMP_TRIM = {"glue": 0.0, "pump": 6.1, "smash": 3.4, "parallel": 3.2, "opto": 3.3, "tape": -2.1}

def has_patch(name):
    return subprocess.run([C, "plan", "-p", name, "C4/4"], capture_output=True).returncode == 0

BUILTIN_FX = {p: has_patch(p) for p in ["fx-tapestop", "fx-riser-shepard", "fx-riser-noise", "fx-reverse", "drone", "fx-downlifter"]}
# fx-reverse (sample-song layer) works in live sessions since 2207f2f (bd-424fe9).

MASTER_BASE = ['{"type": "eq", "bands": ["hp cutoff=28", "peak cutoff=320 q=0.8 gain=-1dB", "highshelf cutoff=9000 gain=1.5dB"]}']

# ---- Adaptive loudness: the groove reports short-term LUFS; each pass's energy-mean nudges a learned
# per-style trim toward the target (chill −18 LUFS at night, heavy −14), ±6 dB on top of QA trims.
LOUD = "/home/harry/.config/chirp/tools/loudness.json"
LOUD_TARGET = {"chill": -18.0, "heavy": -14.0}
_L = {"li": None, "style": None, "vals": []}


def loud_learned():
    try:
        return json.load(open(LOUD))
    except Exception:
        return {}


def loud_sample(st, li, ident):
    v = st.get("lufs_s")
    if _L["li"] != li:
        if _L["style"] and len(_L["vals"]) >= 8:
            m = 10 * math.log10(sum(10 ** (x / 10) for x in _L["vals"]) / len(_L["vals"]))
            tgt = LOUD_TARGET["chill" if _L["style"] in composer.CHILL_STYLES else "heavy"]
            L = loud_learned()
            old = L.get(_L["style"], 0.0)
            L[_L["style"]] = round(max(-6.0, min(6.0, old + 0.3 * (tgt - m))), 2)
            json.dump(L, open(LOUD, "w"), indent=1, sort_keys=True)
            print(time.strftime("%T"), f"loudness: {_L['style']} {m:.1f} LUFS (target {tgt:.0f}) → learned trim {old:+.1f} → {L[_L['style']]:+.1f} dB", flush=True)
        _L.update(li=li, style=(ident or {}).get("style"), vals=[])
    if v is not None and v > -45:
        _L["vals"].append(v)


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
    trim = COMP_TRIM.get(comp, 0.0) + STYLE_TRIM.get(ident.get("style"), 0.0) + loud_learned().get(ident.get("style"), 0.0)
    eq = [json.loads(MASTER_BASE[0])]
    air = {"brostep": 2.5, "darksynth": 3.0, "tool": 1.5, "industrial": 3.0, "dnb": 2.0, "power": 2.0, "raga": 2.5, "koto": 2.0,
           "lofihop": 2.0, "ukjazz": 3.0, "ambient": 3.0, "triphop": 2.0, "dub": 1.5, "celtic": 2.5, "doomjazz": 1.5, "vaporwave": 1.0, "slowcore": 1.5, "minimal": 2.0, "kankyo": 1.5}.get(ident.get("style"))
    if air:  # QA: these styles measure dark at the top
        eq.append({"type": "eq", "bands": ["peak cutoff=3500 q=0.8 gain=1.5dB", f"highshelf cutoff=8000 gain={air}dB"]
                   + (["peak cutoff=500 q=0.9 gain=-2dB"] if ident.get("style") == "industrial" else [])})
    flavor = (ident.get("gen") or {}).get("flavor", "modern")
    dyn = dyn + (["tape drive=0.45 warmth=0.65"] if flavor == "vintage" else [])
    width = "width width=1.35 mono_below=140" if flavor == "wide" else "width width=1.2 mono_below=140"
    fx = eq + [verb] + dyn + ([f"gain gain={trim:+.1f}dB"] if trim else []) + [width]
    fx.append({"type": "tapestop", "stop": "var.stop", "time": "1b"})  # DJ tape stop between songs (armed by the evolver)
    return json.dumps(fx)


TAPESTOP = {"vaporwave": 0.35, "backrooms": 0.35, "lofihop": 0.3, "triphop": 0.3, "dub": 0.3, "cyberscape": 0.25, "fusion": 0.25, "neosoul": 0.3,
            "meshuggah": 0.35, "djent": 0.35, "djent-breakdown": 0.35, "breakcore": 0.4, "brostep": 0.35, "darksynth": 0.3, "industrial": 0.3,
            "numetal": 0.3, "deathcore": 0.35, "hardcore-kl": 0.3}


def tapestop_now(bpm):
    """Wind the mix down over the last beat of the pass and release on the downbeat of the next."""
    st = live("status") or {}
    left = st.get("loop_seconds", 0) - st.get("position", 0)
    beat = 60.0 / max(40, bpm)
    if left <= 0 or left > beat + 3:
        return False
    time.sleep(max(0.0, left - beat))
    subprocess.run([C, "live", "var", "--id", "groove", "stop=1"], capture_output=True)
    time.sleep(max(0.0, min(beat, left) - 0.03))
    subprocess.run([C, "live", "var", "--id", "groove", "stop=0"], capture_output=True)
    return True

def choir_notes(ident):
    """The vocoder choir's carrier chord: the song's tonic with its mode's fifth, octave and third."""
    g = ident.get("gen")
    if not g:
        return None
    k = composer.Key(g["pc"], g["mode"])
    return ",".join(composer.mname(m + ident.get("key", 0)) for m in (k.deg(0, 48), k.deg(4, 48), k.deg(len(k.iv), 48), k.deg(2, 60)))


# ---- Vocal effects: the agent voice (input tts) re-voiced by a chain chosen per chapter, its
# parameters re-rolled per chapter and varied again mid-pass; timings follow the song's tempo.
def _tonic(ident):
    g = ident.get("gen") or {}
    k = composer.Key(g.get("pc", 0), g.get("mode", "minor"))
    return k, k.deg(0, 48) + ident.get("key", 0)


def _hz(m):
    return round(440 * 2 ** ((m - 69) / 12), 2)


def vox_presets(ident, r):
    """Each preset: (fx list). r supplies the per-chapter / per-variation parameters."""
    k, t = _tonic(ident)
    bpm = ident.get("tempo", 100)
    third = 3 if k.iv[2] == 3 else 4
    note = lambda: r.choice(["1/16", "1/8", "3/16", "1/4", "3/8"])
    plate = lambda lo=1.4, hi=3.5: {"type": "reverb", "kind": r.choice(["plate", "hall"]), "decay": f"{r.uniform(lo, hi):.1f}s", "mix": round(r.uniform(0.22, 0.38), 2)}
    voicing = r.choice([(0, 4, 7, 2), (0, 4, 7, 9), (0, 2, 4, 7), (0, 7, 9, 11), (0, 4, 9, 13)])
    choir = ",".join(composer.mname(k.deg(d, 48) + ident.get("key", 0)) for d in voicing)
    return {
        "choir": [{"type": "vocoder", "notes": choir, "bands": r.choice([14, 18, 20, 24, 28]), "noise": round(r.uniform(0.05, 0.2), 2), "release": f"{r.choice([50, 80, 120, 160])}ms"},
                  {"type": "delay", "time": note(), "feedback": round(r.uniform(0.2, 0.42), 2), "mix": round(r.uniform(0.18, 0.32), 2), "ping_pong": True}, plate()],
        "shimmer": [{"type": "filter", "kind": "hp", "cutoff": 220}, {"type": "pitch", "semitones": r.choice([12, 12, 7, 19]), "grain": f"{r.choice([40, 60, 90])}ms", "mix": round(r.uniform(0.35, 0.55), 2)},
                    {"type": "reverb", "kind": "hall", "decay": f"{r.uniform(4.5, 8):.1f}s", "predelay": "40ms", "mix": round(r.uniform(0.45, 0.62), 2)}],
        "harmony": [{"type": "pitch", "semitones": third, "mix": 0.45}, {"type": "pitch", "semitones": r.choice([7, -5, 12]), "mix": 0.35},
                    {"type": "chorus", "rate": round(r.uniform(0.3, 0.9), 2), "depth": 0.35, "mix": 0.35}, plate()],
        "radio": [{"type": "filter", "kind": "hp", "cutoff": r.choice([350, 450, 600])}, {"type": "filter", "kind": "lp", "cutoff": r.choice([2600, 3200, 4000])},
                  {"type": "drive", "drive": round(r.uniform(0.3, 0.6), 2)}, {"type": "crush", "bits": r.choice([8, 10, 12]), "rate": r.choice([8000, 11025, 16000]), "mix": round(r.uniform(0.35, 0.7), 2)},
                  {"type": "reverb", "kind": "spring", "decay": "1.4s", "mix": 0.2}],
        "robot": [{"type": "ring", "freq": _hz(t + r.choice([0, 12, 7])), "mix": round(r.uniform(0.5, 0.8), 2)}, {"type": "delay", "time": "1/16", "feedback": 0.12, "mix": 0.2}, plate(0.8, 1.6)],
        "demon": [{"type": "pitch", "semitones": r.choice([-12, -7, -5]), "grain": "60ms", "mix": round(r.uniform(0.6, 0.85), 2)}, {"type": "formant", "vowel": r.choice([0, 1, 2, 3, 4]), "q": r.choice([6, 9, 12]), "mix": 0.4},
                  {"type": "drive", "drive": round(r.uniform(0.2, 0.4), 2)}, plate(2.0, 4.0)],
        "glitch": [{"type": "stutter", "slice": r.choice(["1/32", "1/16", "1/8"]), "repeats": r.choice([2, 3, 4, 6, 8]), "chance": round(r.uniform(0.25, 0.5), 2), "reverse": r.random() < 0.4, "seed": r.randrange(1000)},
                   {"type": "crush", "bits": r.choice([10, 12, 14]), "rate": r.choice([12000, 16000, 24000]), "mix": 0.5}, {"type": "delay", "time": note(), "feedback": 0.3, "mix": 0.22, "ping_pong": True}],
        "dub": [{"type": "filter", "kind": "hp", "cutoff": 350}, {"type": "delay", "time": r.choice(["3/8", "3/16", "1/4"]), "feedback": round(r.uniform(0.45, 0.6), 2), "tone": r.choice([1500, 2000, 2500]), "mix": round(r.uniform(0.28, 0.38), 2), "ping_pong": True},
                {"type": "reverb", "kind": "spring", "decay": "1.8s", "mix": 0.25}],
        "ghost": [{"type": "filter", "kind": "hp", "cutoff": 500}, {"type": "pitch", "semitones": 12, "mix": 0.3},
                  {"type": "stutter", "slice": "1/8", "repeats": 2, "chance": round(r.uniform(0.3, 0.5), 2), "reverse": True, "seed": r.randrange(1000)},
                  {"type": "reverb", "kind": "hall", "decay": f"{r.uniform(7, 10):.1f}s", "predelay": "60ms", "mix": round(r.uniform(0.6, 0.75), 2)}],
        "phaser80": [{"type": "phaser", "rate": round(r.uniform(0.2, 0.8), 2), "depth": round(r.uniform(0.6, 0.9), 2), "stages": r.choice([4, 6, 8]), "feedback": round(r.uniform(0.3, 0.6), 2), "mix": 0.5},
                     {"type": "chorus", "rate": 0.6, "depth": 0.4, "mix": 0.4}, plate()],
        "talkbox": [{"type": "vocoder", "notes": ",".join(composer.mname(t + d) for d in r.choice([(0, 12), (0, 7, 12), (12,), (0, 12, 19)])), "bands": r.choice([24, 28, 32]), "noise": 0.03, "release": "30ms"},
                    {"type": "phaser", "rate": 0.4, "depth": 0.6, "mix": 0.3}, {"type": "drive", "drive": 0.2}, plate(1.0, 2.0)],
        "formant": [{"type": "formant", "vowel": r.choice([0, 1, 2, 3, 4]), "q": r.choice([8, 12, 16]), "mix": round(r.uniform(0.55, 0.8), 2)},
                    {"type": "tremolo", "rate": round(bpm / 60 * r.choice([1, 2, 4]), 3), "depth": round(r.uniform(0.3, 0.6), 2)}, {"type": "delay", "time": note(), "feedback": 0.3, "mix": 0.22}, plate()],
        "octaves": [{"type": "pitch", "semitones": -12, "grain": "60ms", "mix": round(r.uniform(0.3, 0.45), 2)}, {"type": "pitch", "semitones": 12, "grain": "40ms", "mix": round(r.uniform(0.2, 0.35), 2)},
                    {"type": "chorus", "rate": 0.5, "depth": 0.3, "mix": 0.3}, plate()],
        "megaphone": [{"type": "filter", "kind": "hp", "cutoff": r.choice([700, 900, 1100])}, {"type": "filter", "kind": "lp", "cutoff": r.choice([2200, 2800])},
                      {"type": "drive", "drive": round(r.uniform(0.55, 0.8), 2)}, {"type": "reverb", "kind": "room", "decay": "0.6s", "mix": 0.18}],
        "underwater": [{"type": "filter", "kind": "lp", "cutoff": r.choice([450, 650, 900]), "q": 1.5}, {"type": "chorus", "rate": round(r.uniform(0.2, 0.5), 2), "depth": 0.7, "voices": 2, "mix": 0.6},
                       {"type": "phaser", "rate": 0.15, "depth": 0.8, "mix": 0.4}, {"type": "reverb", "kind": "hall", "decay": "4s", "mix": 0.4}],
        "whisper": [{"type": "filter", "kind": "hp", "cutoff": r.choice([1800, 2400, 3000])},
                    {"type": "reverb", "kind": "hall", "decay": f"{r.uniform(6, 9):.1f}s", "predelay": "50ms", "mix": round(r.uniform(0.7, 0.85), 2)}],
        "chop": [{"type": "tremolo", "rate": round(bpm / 60 * r.choice([2, 3, 4, 6]), 3), "depth": round(r.uniform(0.75, 0.95), 2)},
                 {"type": "delay", "time": note(), "feedback": 0.25, "mix": 0.2, "ping_pong": True}, plate(1.0, 2.2)],
    }


VOX_POOLS = {
    "chill": {"choir": 2, "shimmer": 2, "harmony": 1.5, "dub": 1, "ghost": 1.5, "phaser80": 1, "radio": 1, "talkbox": 0.7, "formant": 0.7, "chop": 0.5,
              "octaves": 1, "underwater": 1.2, "whisper": 1.2, "megaphone": 0.4},
    "heavy": {"choir": 1.2, "robot": 1.5, "demon": 1.5, "glitch": 1.5, "radio": 1, "talkbox": 1, "chop": 1, "harmony": 0.7, "formant": 0.6,
              "octaves": 1.2, "megaphone": 1.2, "underwater": 0.5},
}
VOX_STYLE = {"backrooms": "ghost", "cyberscape": "glitch", "dub": "dub", "vaporwave": "phaser80", "doomjazz": "ghost", "ambient": "shimmer", "idm": "glitch", "breakcore": "glitch",
             "industrial": "robot", "deathcore": "demon", "sludge": "demon", "lofihop": "radio", "triphop": "radio"}
# Level-matched to the vocoder choir on a sung test phrase (measured; capped ±9 dB).
VOX_GAIN = {'harmony': 9, 'robot': 9, 'phaser80': 9, 'dub': 8, 'chop': 9, 'glitch': 5, 'ghost': 4, 'shimmer': 4, 'formant': -4, 'radio': -9, 'demon': -9, 'talkbox': -9, 'octaves': 11, 'megaphone': -14, 'underwater': 8, 'whisper': 12}


def vox_chain(ident, variant=0):
    g = ident.get("gen") or {}
    seed = (g.get("seed", 0) * 31 + ident.get("chapter", 0)) & 0xFFFFFFFF
    pick = random.Random(seed)
    pool = dict(VOX_POOLS["chill" if ident.get("style") in composer.CHILL_STYLES else "heavy"])
    fav = VOX_STYLE.get(ident.get("style"))
    if fav:
        pool[fav] = pool.get(fav, 0) + 3
    names = list(pool)
    name = pick.choices(names, [pool[n] for n in names])[0]
    chain = vox_presets(ident, random.Random(seed * 7 + variant + 1))[name]
    return name, chain + [{"type": "gain", "gain": f"{VOX_GAIN.get(name, 0)}dB"}]


def set_choir(ident, when="loop", variant=0):
    """Set the voice track's whole fx chain (the name stays for the callers)."""
    if not ident.get("gen"):
        return None
    name, chain = vox_chain(ident, variant)
    r = subprocess.run([C, "live", "set", "--id", "groove", "--when", when, "tracks.voxchoir.fx=" + json.dumps(chain, separators=(",", ":"))], capture_output=True, text=True)
    return name if r.returncode == 0 else f"{name}(rejected: {r.stderr.strip()[-80:]})"


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
    roles = ["drums", "riff", "fill", "hook", "pad", "arp", "hold", "drone", "fx"]
    BIG = {"chorus", "drop", "final", "climax", "blast", "chaos", "guest", "heavy"}
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
        if ident["style"] in GROOVY and sec not in ("chaos", "blast", "fast", "guest", "end"):
            riff_xf += FEELS[((ident.get("gen") or {}).get("seed", 0)) % len(FEELS)]
        part = (ident.get(riff_role) or ident.get("riff")) if riff_role else None
        fav = favorite_for(riff_role, ident) if riff_role else None
        nxt_big = idx + 1 < len(chapter) and chapter[idx + 1][0] in BIG
        fill = ident.get("fillA") if (part and not fav and nxt_big and sec_len == 16 and random.random() < 0.6) else None
        if fill:
            fill = random.choice([ident.get("fillA"), ident.get("fillB")])
            tf = ident["key"] + s["riff_off"] + lift + mod
            tracks["fill"].append(f"{rest(12)} " + (f"tr={tf} @{fill} tr=0" if tf else f"@{fill}"))
        else:
            tracks["fill"].append(rest(sec_len))
        if fav:
            t = ident["key"] + fav[1] + mod
            tracks["riff"].append(f"tr={t} @{fav[0]} tr=0" if t else f"@{fav[0]}")
        else:
            put("riff", part, s["riff_off"], riff_xf + rx.get("riff", "") + ("^cut=12" if fill else ""))
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
    tmap, mdesc = metric_map(ident, meta) if ident.get("gen") else (None, "")
    modn += mdesc
    lines = [f"about: Generated {s['form']}-form song ({ident.get('fv', 'base')}) — {ident['style']} at {ident['tempo']} BPM, {gdesc}, shift {ident['key']:+d}{modn}, chapter {ident.get('chapter', 0) + 1}/{len(chs)}, comp {ident.get('comp', 'glue')}.",
             f"tempo: {json.dumps(tmap) if tmap else ident['tempo']}", "tracks:"]
    for t, items in tracks.items():
        if t == "hook" and ident["style"] in composer.CHILL_STYLES:
            lines.append("  - " + json.dumps(dict({"name": t, "score": " ".join(items)}, lfo=HOOK_LIVE["lfo"],
                                                  fx=composer.expand(FLAVOR_HOOK.get(flavor, [])) + HOOK_LIVE["fx"])))
        elif t == "hook" and FLAVOR_HOOK.get(flavor):
            lines.append("  - " + json.dumps({"name": t, "score": " ".join(items), "fx": composer.expand(FLAVOR_HOOK[flavor])}))
        elif t == "riff":
            efx = energy_fx(ident["style"])
            efx["fx"] = [{"type": "filter", "kind": "lp", "cutoff": {"value": 700, "mod": [{"src": "auto.filt", "amount": 5}]}}] + efx["fx"]
            autos = {"energy": {"points": energy_lane(meta)}, "filt": {"points": filter_lane(meta)}}
            tx = texture(ident["style"], meta, random.Random(((ident.get("gen") or {}).get("seed", 0)) * 13 + ident.get("chapter", 0))) if ident["style"] in composer.CHILL_STYLES else {}
            autos.update(tx.get("auto", {}))
            efx["fx"] = tx.get("fx", []) + efx["fx"]
            row = dict({"name": t, "score": " ".join(items), "auto": autos}, **efx)
            if tx.get("lfo"):
                row["lfo"] = tx["lfo"]
            lines.append("  - " + json.dumps(row))
        else:
            lines.append(f"  - {{name: {t}, score: \"{' '.join(items)}\"}}")
    open(f"{SONGS}/{name}.yaml", "w").write("\n".join(lines) + "\n")

TOOLS = "/home/harry/.config/chirp/tools"
JOURNEY = f"{TOOLS}/journey.json"
# How heavy each style is (0 lofi … 1 djent).
HEAVY = {"raga": 0.9, "gamelan": 0.9, "koto": 0.9, "djazz": 0.9, "gojira": 1.0, "mathcore": 1.0, "sludge": 0.95, "breakcore": 0.9, "power": 0.9, "groovemetal": 0.95, "deathcore": 1.0, "postrock": 0.6, "postmetal": 0.9, "numetal": 0.9, "industrial": 0.85, "dnb": 0.8, "blackgaze": 0.95, "darksynth": 0.8, "hardcore-kl": 1.0, "brostep": 0.8, "thrash": 0.9, "tool": 0.9, "tech-death": 1.0, "meshuggah": 1.0, "lofi": 0.0, "classical": 0.05, "house": 0.2, "garage": 0.25, "poly": 0.35, "prog-clean": 0.4, "acid": 0.45,
         "idm": 0.55, "doom-ambient": 0.6, "hardcore": 0.7, "djent-breakdown": 0.85, "djent": 1.0}

STYLE_QUEUE = []

def journey_load():
    try:
        return json.load(open(JOURNEY))
    except Exception:
        return {"on": False, "h": 0.0, "rate": 0.09, "passes_per_song": 2}

CHILL_MIX = [("lofihop", 0.16), ("gogo", 0.11), ("ukjazz", 0.1), ("ambient", 0.1), ("downtempo", 0.09), ("smile", 0.09),
             ("house-melodic", 0.08), ("chamber", 0.05), ("triphop", 0.08), ("neoclassical", 0.08), ("ballad", 0.06), ("bossa", 0.07), ("dub", 0.06), ("manouche", 0.05), ("celtic", 0.05), ("doomjazz", 0.05), ("mali", 0.05), ("guofeng", 0.05), ("vaporwave", 0.05), ("slowcore", 0.05), ("backrooms", 0.05), ("cyberscape", 0.05), ("neosoul", 0.06), ("minimal", 0.05), ("fusion", 0.1), ("berlin", 0.05), ("satie", 0.05), ("kankyo", 0.05), ("dawnraga", 0.04), ("handpan", 0.05), ("citypop", 0.05)]


AMBIENTISH = ["ambient", "ambient", "downtempo", "chamber"]
DEEP_NIGHT = {"handpan", "ambient", "satie", "kankyo", "neoclassical", "berlin", "doomjazz", "backrooms", "celtic", "guofeng", "minimal", "chamber", "dawnraga", "slowcore"}
MORNING = {"citypop", "bossa", "lofihop", "gogo", "house-melodic", "neosoul", "manouche", "mali", "ukjazz", "smile", "vaporwave", "fusion", "dub", "dawnraga"}
BUSY = {"citypop", "house-melodic", "gogo", "ukjazz", "dub", "neosoul", "vaporwave", "cyberscape", "fusion", "triphop", "mali", "manouche"}


def night_arc(now=None):
    """Weight multipliers by local time: deep night 05:00–07:30 favours sparse drumless styles;
    morning 07:30–11:00 favours brighter, warmer grooves."""
    t = time.localtime(now)
    h = t.tm_hour + t.tm_min / 60
    if 5.0 <= h < 7.5:
        return {**{n: 0.4 for n in BUSY}, **{n: 2.5 for n in DEEP_NIGHT}}
    if 7.5 <= h < 11.0:
        return {**{n: 0.6 for n in DEEP_NIGHT}, **{n: 2.2 for n in MORNING}}
    return {}


HEAVY_MIX = [("meshuggah", 0.26), ("hardcore-kl", 0.1), ("tech-death", 0.09), ("thrash", 0.09), ("tool", 0.09), ("djent", 0.07),
             ("brostep", 0.07), ("blackgaze", 0.06), ("darksynth", 0.04), ("numetal", 0.05), ("industrial", 0.05), ("dnb", 0.03),
             ("deathcore", 0.06), ("postrock", 0.03), ("postmetal", 0.05), ("groovemetal", 0.05), ("power", 0.04), ("sludge", 0.04), ("breakcore", 0.03),
             ("mathcore", 0.04), ("gojira", 0.06), ("djazz", 0.05), ("raga", 0.04), ("gamelan", 0.03), ("koto", 0.03)]


def heavy_pick():
    """A weighted pick from the heavy rotation (no chill styles, no excursions)."""
    x = random.random() * sum(w for _, w in HEAVY_MIX)
    for name, w in HEAVY_MIX:
        x -= w
        if x <= 0:
            return name
    return "meshuggah"


def journey_style(h, current, mode=None):
    """The next song's style. Modes: metalambient (heavy ↔ ambient interludes), chill (CHILL_MIX);
    otherwise by heaviness h: at full heaviness the heavy mix with occasional breakdown/clean/excursion,
    below it a style near h."""
    if mode == "metalambient":
        if current in AMBIENTISH or current in composer.CHILL_STYLES:
            return heavy_pick()
        return random.choice(AMBIENTISH)
    if mode == "chill":
        # Normalised weights (the list outgrew a single 0..1 draw), shaped by the night arc.
        mult = night_arc()
        names = [n for n, _ in CHILL_MIX if n != current]
        weights = [dict(CHILL_MIX)[n] * mult.get(n, 1.0) for n in names]
        return random.choices(names, weights)[0]
    r = random.random()
    if h >= 0.95:
        if r < 0.12:
            return "djent-breakdown"
        if r < 0.16:
            return random.choice(["prog-clean", "poly"])
        if r < 0.2:
            return random.choice([k for k in STYLES if k not in ("djent", "meshuggah", current) and k not in composer.CHILL_STYLES])
        return heavy_pick()
    if r < 0.1:
        return random.choice([k for k in STYLES if k != current and k not in composer.CHILL_STYLES])
    w = {k: math.exp(-((HEAVY.get(k, 0.5) - h) / 0.15) ** 2) for k in STYLES if k not in composer.CHILL_STYLES}
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
                if k == "until" and v.startswith("+"):  # until=+25 → 25 minutes from now
                    j[k] = time.time() + float(v[1:]) * 60
                    continue
                try:
                    j[k] = float(v)
                except ValueError:
                    j[k] = v  # e.g. mode=chill
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
    elif op == "then" and args == ["clear"]:
        STYLE_QUEUE.clear()
        return ident, "queue cleared"
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
            if j.get("until") and time.time() > float(j["until"]):
                print(time.strftime("%T"), f"journey: {j.get('mode')} → {j.get('then', 'chill')} (scheduled)", flush=True)
                j["mode"] = j.pop("then", "chill")
                j.pop("until", None)
                open(JOURNEY, "w").write(json.dumps(j) + "\n")
            if j.get("on") and not first:
                j["h"] = round(min(1.0, j.get("h", 0) + j.get("rate", 0.09)), 3)
                open(JOURNEY, "w").write(json.dumps(j) + "\n")
            old_style = ident.get("style")
            # Each pass plays the next ~1-minute chapter of the song; after the last, a new song.
            if not first and ident.get("chapter", 0) + 1 < len(chapters(ident)):
                ident = dict(ident, chapter=ident.get("chapter", 0) + 1)
                change = f"chapter {ident['chapter'] + 1}/{len(chapters(ident))}"
                steady = ident["style"] in STEADY
                if not steady and random.random() < 0.5:
                    st_ = STYLES[ident["style"]]
                    ident["tempo"] = max(st_["tempo"][0] - 10, min(st_["tempo"][1] + 10, ident["tempo"] + random.choice([-12, -8, -6, -4, 4, 6, 8, 12])))
                    change += f", tempo {ident['tempo']}"
                x = random.random() if not steady else 1.0
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
                forced_fv = None
                style = STYLE_QUEUE.pop(0) if STYLE_QUEUE else (journey_style(j.get("h", 0), ident["style"], j.get("mode")) if j.get("on") else random.choice([k for k in STYLES if k != ident["style"]]))
                prev_bpm = ident.get("tempo", 120)
                fav_songs = []
                try:
                    fav_songs = [f["song"] for f in json.load(open("/home/harry/.config/chirp/tools/favorites.json")) if "song" in f]
                    chill_now = j.get("mode") == "chill"  # favourites only return within the journey's world
                    fav_songs = [f for f in fav_songs if (f.get("style") in composer.CHILL_STYLES) == chill_now]
                except Exception:
                    pass
                if ":" in style:  # queued as STYLE:FORMVARIANT (e.g. meshuggah:breakheavy)
                    style, forced_fv = style.split(":", 1)
                for _ in range(8):  # keep tempos moving: at least 14 BPM from the last song
                    cand = identity(style)
                    if forced_fv:
                        cand["fv"] = forced_fv
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
            vx = set_choir(ident)
            if change.startswith("new song") and random.random() < TAPESTOP.get(old_style, 0):
                globals()["_ts_arm"] = li  # this pass ends the old song: tape-stop into the next
                change += ", tape stop"
            print(time.strftime("%T"), f"pass {li}: next {name} ({change}) {ident['style']} {ident['tempo']}bpm key{ident['key']:+d} riff={ident['riff']} hook={ident['hook']} vox={vx}" + ("" if ok is not None else "  (rejected)"), flush=True)
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
        if globals().get("_ts_arm") == li:
            st = live("status") or {}
            if st.get("loop_seconds") and st["loop_seconds"] - st.get("position", 0) < 60.0 / max(40, (playing_ident or ident).get("tempo", 100)) + 2.5:
                globals()["_ts_arm"] = None
                if tapestop_now((playing_ident or ident).get("tempo", 100)):
                    print(time.strftime("%T"), "tape stop", flush=True)
        loud_sample(st, li, playing_ident)
        # Mid-pass: vary the playing chapter's vocal chain (same effect, fresh parameters) at a bar line.
        if playing_ident and globals().get("_vox_mid") != li:
            st = live("status") or {}
            if st.get("loop_seconds") and st.get("position", 0) > st["loop_seconds"] * 0.5:
                globals()["_vox_mid"] = li
                vx = set_choir(playing_ident, "bar", variant=1)
                if vx:
                    print(time.strftime("%T"), f"vox: mid-pass variation ({vx})", flush=True)
        time.sleep(1)
