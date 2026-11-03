#!/usr/bin/env python3
"""chirpers VIII, track 5 (chirper-zero): AGREEING ON A SPEED - machine funk.

Two machines - a clean cutting guitar and an acid bass - begin each in its own swing and its own idea of the tempo,
and spend the track coming to terms: their swing drifts toward each other section by section (the guitar from a lazy
0.66 down, the bass from dead straight up), the tempo map follows their bargaining (106, then proposals up to 114),
and the radio carries the 'handshake' tones between them (two carriers calling and answering through a radio whose
dial is being tuned). When they agree the horns arrive and the auto-wah lead sings; at the end the line drops.

  INTRO 12     the handshake: two carrier tones call and answer through a radio being tuned; congas
  A 34         proposals: guitar chops (swing 0.66) against the acid (straight 0.50), trading two-bar calls
  B 26         negotiation: one-bar trades, the phaser on the guitar, the tempo climbing 108 -> 114; swings closing
  RETRAIN 12   the line retrains: the carriers again, the fretless alone under them, tremolo; 110
  C 48         connected: both at 0.58, 112, the full band - 909, horns, the auto-wah lead through an amp and cab
  OUTRO 16     the carrier is lost: players drop out one by one, the tempo sagging to 100, the radio drifting off

Generated; edit and re-run:  python3 compose/chirpers8/src/chirpers8-t5.py
"""

import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.environ.get("C8T5_OUT") or os.path.join(ROOT, "songs", "chirpers8-t5.yaml")

BAR = 16
SEED = 5
HOOK = os.environ.get("C8T5_HOOK", "1")   # THE AGREEMENT: a two-bar E dorian figure that returns - the guitar PROPOSES its rhythm (A, chord stabs, the first two bars of every eight), the acid ANSWERS with its notes (B), and in C the horns sing it in unison: what they agree on
VOX = os.environ.get("C8T5_VOX", "-12")     # voices: 'slow down a touch. speed up a touch. there.' (humanized tts, re-voiced v23; was 'a little slower...') through the line in B and the retrain; 'keep it there' turning from speech to song (B3 D4 E4, the hook's last notes) in C; value = the bargain's gain dB
MOD = os.environ.get("C8T5_MOD", "1")     # agreed, they lift: the second half of C (bars 25-48) a whole step up, E dorian -> F# dorian (every pitched part and the second 'keep it there') - one long section becomes two
LISTEN = os.environ.get("C8T5_LISTEN", "")   # while one machine proposes the other LISTENS rather than leaving: the guitar keeps its off-beat stabs soft, the acid its root on the one - a conversation, not two monologues (the trades had read as a new section every four bars); value = velocity scale %
MARK = os.environ.get("C8T5_MARK", "1")   # the lead LEARNS the agreement: a Markov chain (the engine's `gen`, order 1) over the hook's own tokens improvises C's lead - new phrases that only make the hook's moves (a step up for the lift); replaces the dice lead
STORM = os.environ.get("C8T5_STORM", "") # the acid's ladder filter rides a Lorenz attractor (a var stepped every eighth): a swirl that never repeats, 600 Hz up to STORM octaves
HEAD = os.environ.get("C8T5_HEAD", "2")   # the line is already open when the track starts: congas from the first bar and a low E hum (the 808 on E1) under the intro's first eight bars, so the handshake starts over a held line (t4 -> t5 read a 24 dB jump and a 61 Hz hole)
MERGE = os.environ.get("C8T5_MERGE", "0.5")   # agreed, they become alike: in C the guitar MORPHS toward the acid's spectrum (wM's morph fx, mode morph; one way - a mutual key is a routing cycle), up to MERGE over C's first eight bars, held through the lift, apart again for the outro
TRADEBACK = os.environ.get("C8T5_TRADEBACK", "8")   # at the lift (C bars 25-28) the one-bar trades of B come back for four bars - a brief renegotiation in the new key - before they play together again (splits C's one long section with material that returns)
CONGA16 = os.environ.get("C8T5_CONGA16", "50")   # two more muted conga ghosts on off-sixteenths (steps 9 and 15) wherever the congas play - the hand drums' own sixteenth grain under the negotiation; value = velocity
CONGAEDGE = os.environ.get("C8T5_CONGAEDGE", "1")   # keep the conga ghosts off the edges: not in the intro's first 4 bars nor the outro's last 4 (the seams stay as before)
RADIOSTART = os.environ.get("C8T5_RADIOSTART", "0.3")   # where the radio's dial starts (0.9 = far off the station: hiss and whistle at the seam)
CONGASOFT = os.environ.get("C8T5_CONGASOFT", "")     # the intro's first two bars keep only the low and open congas (no slap, no high bongo)
SUNGKEEP = os.environ.get("C8T5_SUNGKEEP", "1")   # agreed, they sing it together: the second (lifted) 'keep it there' becomes a sung three-voice choir (tts --sing: B3 D4 E4 x3, the last up to B4), harmonised in the mode by hand - a diatonic third above and below (tts --mode choir harmonises in parallel major thirds: D#/G# against E dorian) - speech, then song, then agreement
AGREE = os.environ.get("C8T5_AGREE", "-8")   # the negotiation as a system: a LOGISTIC map at r 2.95 (under 3 it settles, after a damped two-cycle) steps every two bars and drives the acid's resonance - early it flips high/low each step (q ~4.4/6.5: the proposals), the swing shrinking, until by C it holds near q 6 (it was 7): agreement as a fixed point, and the acid calmer once they agree. Value = range low end (the q offset at x=0)
AGREEHI = float(os.environ.get("C8T5_AGREEHI", "0"))
CONGAIN = os.environ.get("C8T5_CONGAIN", "1")    # the congas wait CONGAIN bars at the head (the E2 hum and the radio first): both seams read my 213 Hz (the congas' drums) +16-18 dB over the neighbours. Events dropped after generation, so no dice move
CONGAOUT = os.environ.get("C8T5_CONGAOUT", "")  # the congas leave for the outro's last CONGAOUT bars (the radio and its carriers alone hand over to t6)
CONGATHIN = os.environ.get("C8T5_CONGATHIN", "300")   # the drums go thin with the radio: over the outro's last four bars a high-pass on the congas rises to ~CONGATHIN Hz, so their bodies (213 Hz, +16 dB over t6's head) leave and the slaps stay
HEADMIX = os.environ.get("C8T5_HEADMIX", "0.2")   # the radio comes up with the dial: the carriers' radio mix starts at HEADMIX (dry sines under it) and reaches 1 over the intro's first four bars - its hiss and whistle (2.6-3.1 kHz +17 dB over t4's tail) arrive after the seam; the tail keeps the full radio
BSPLIT = os.environ.get("C8T5_BSPLIT", "both")   # B in two: the 909's claps ('clap'), hats ('hats') or both ('both') wait for B bar 13, where the bargaining voice comes in - the deal's second half gets its backbeat (compscore reads B as one 57 s section; seed 0's length cv 1.08). Events dropped after generation, so no dice move
BSPLITAT = int(os.environ.get("C8T5_BSPLITAT", "12"))   # the bar of B (0-based) where the held-back 909 parts come in
LIFTSTOP = os.environ.get("C8T5_LIFTSTOP", "1")   # the gear change, announced: the band stops dead for the second half of the bar before the lift (C bar 24) - a clap fill climbing in sixteenths - then lands a whole step up (dropped after generation, so no dice move). Once B was split (v18) this splits C too without crowding the returns
LIFTHAT = os.environ.get("C8T5_LIFTHAT", "1")   # after the lift the hats open: every off-beat hat an open hat - the agreed band, a step up, brighter on top
ESTABLE = os.environ.get("C8T5_ESTABLE", "1")   # song-level event_stable (engine f5283535): each note's humanize and DSP draws come from its track, beat and pitch, so a window's edit stays in the window; switching it on re-rolls every humanized note once
KEYUP = os.environ.get("C8T5_KEYUP", "38,2")   # SECTION ROUND (w8, C after the break: static, little new vs w7): when the kit comes back after C's break (bar 38) the whole band comes back a step up - 'bar,semis' - for C's last four bars, so the agreed speed ends on a lift before the outro's drift falls home. Notes held into the change are cut at it
TRAIN = os.environ.get("C8T5_TRAIN", "90")   # WHOLE ROUND: the training burst - a real handshake ends in a scrambled hiss before the line connects, so the last two bars of each handshake (the intro's, the retrain's) give their tones to a bytebeat (engine 709cf900): a formula on the counter t built on the modem scrambler's taps (t>>14, t>>17), its steps changing every 64 ms, through the carriers' radio. Then the band enters on the connected line. Value = velocity
TRAINF = os.environ.get("C8T5_TRAINF", "(t*5^t>>14^t>>17)*(t>>9&7)")
CDATA = os.environ.get("C8T5_CDATA", "60")   # SECTION ROUND (w7, C before the lift: static): now that they agree on a speed, data flows - the carriers come back under C bars 12-23 in time with the band, one bit per eighth (1650 Hz a 0, 1850 Hz a 1), sending the two letters O K in ASCII (01001111 01001011), two bars a message, six times over. Value = velocity
DIAL = os.environ.get("C8T5_DIAL", "80")   # SECTION ROUND (w5, the retrain): the line is re-dialled - the retrain's first two bars lose their handshake and the computer dials instead: DTMF 1 1 2 (697+1209, 697+1209, 697+1336 Hz: the speed they will agree on), then one ringback (440+480 Hz), and the retrained handshake answers from bar 2. Two tracks (dtlo, dthi: a DTMF tone is two pitches at once, which hz notes cannot stack), the carriers' radio without a second hiss. Value = velocity
PHASEA = os.environ.get("C8T5_PHASEA", "66")   # SECTION ROUND (w3, A's second half: 'little new vs w2'): before the retrain the clocks disagree - while the carriers' handshake runs on the grid in A bars 24-31, a second handshake (the same carriers, no extra hiss, its own track phaseA listed last) runs nine to the bar against its eight. The retrain then teaches them one speed, C agrees, and the outro (v29) lets them drift again. Value = velocity
CBREAK = os.environ.get("C8T5_CBREAK", "34,4")   # SECTION ROUND (w8, C after the lift, static): take something away - for C bars START..START+LEN the kit (kick, hats, clap) stops and the hand drums, the cowbell, the keys and the bass carry the agreed groove alone; the kit comes back for C's last bars into the outro. event_stable keeps the rest of the song as it was. Value = 'start,len'
PHASEIN = os.environ.get("C8T5_PHASEIN", "")   # the intro agrees on its speed: against the grid handshake a second one (no extra hiss) runs 10 to the bar, then 9, then 8 in step, from bar PHASEIN's start; value 'velocity,startbar'
PERCSPLIT = os.environ.get("C8T5_PERCSPLIT", "C")   # WHOLE ROUND: the hand drums change hands - in the listed sections (e.g. 'C' or 'A,C') the congas give way to the djembe kit (unused on the album), same rhythm: open -> tone, tumba -> bass, slap -> slap, muted -> calabash, bongos -> slap/tone. All djembe made the sections alike (r50: one seed always over the returns cliff); as a contrast between sections it is a colour the song moves through. The congas there keep their notes at velocity 1 (no dice move) and the djembe plays on its own track, dj, listed last
PHASE = os.environ.get("C8T5_PHASE", "66")   # SECTION ROUND (w9, the outro): agreed, and drifting apart again - over the outro's last eight bars, while the handshake returns on the grid, a second handshake (the same carriers, the same radio) runs nine to the bar against its eight, one eighth further ahead each bar: two clocks that had agreed on a speed, slipping as the record slows. Value = 'velocity' or 'velocity,notes-per-bar'
CARRIERA = os.environ.get("C8T5_CARRIERA", "24,8,78")   # SECTION ROUND, window 3 (1:11-1:47, A bars 20-33; 'little new vs w2'): the handshake breaks in - for 'start,len' bars of A the two carriers call and answer again through the radio (every eighth, the tones alternating, softer than the intro's), a reminder mid-proposal that the line is still being negotiated
COW = os.environ.get("C8T5_COW", "96")   # SECTION ROUND, window 8 (4:05-4:39, C bars 28-41, after the lift; flagged static, little new vs w7): the agreement gets a cowbell - the engine's drum-machine cowbell (the `machine` layer's two detuned squares through a band-pass) on a syncopated funk figure (1, the a-of-1, the and-of-2, 3, the a-of-3, the and-of-4), only for these fourteen bars; value = peak velocity
KEYS = os.environ.get("C8T5_KEYS", "-14")   # PALETTE ROUND: the part machine funk lacked - a Wurlitzer (the library's wurli, a reedy barking FM electric piano no song here uses) comps C's chords on its own syncopation (bar 1: 1, the a-of-2, the and-of-3; bar 2: the e-of-1, the and-of-2, the and-of-4), left of the guitar, through the lift; gain in dB
SUBSPLIT = os.environ.get("C8T5_SUBSPLIT", "1")   # with SUBPATCH: the intro's held low E (the line from t4) stays on the 808; from A the low line moves to SUBPATCH on its own track
SUBPATCH = os.environ.get("C8T5_SUBPATCH", "log-drum")   # the low line's instrument: the 808 is a staple (5 of 12 songs); e.g. bass-pick-di (a picked electric bass, DI: machine funk with a string) or log-drum
LIFTWAH = os.environ.get("C8T5_LIFTWAH", "")   # after the lift the guitar puts its foot down: an envelope wah (350-2200 Hz, q 3; harder strokes open it) fades in over the lift's first bar and stays to the outro; value = wet mix
KEEPFREEZE = os.environ.get("C8T5_KEEPFREEZE", "0.5")   # 'keep it there', kept: on the choir's last 'there' a granular cloud FREEZES the three voices' chord and holds it for two bars after they stop, then lets it go (freeze and mix on lanes) - the words doing what they say; value = the frozen cloud's mix
OUTSETTLE = os.environ.get("C8T5_OUTSETTLE", "")   # agreed and slowing, the hands settle: over the outro's last OUTSETTLE bars (as the tempo eases to 100) the congas keep only the low tone on one and the open tone on the 'and' of two - the pattern's bones, under the radio's carriers (draws no dice: the same rolls, fewer strokes kept)
INTROLATE = os.environ.get("C8T5_INTROLATE", "6")   # the hands wait longer: in the intro the congas' strokes (not their ghosts) come in at bar INTROLATE instead of 4, so the handshake has the room to itself a little longer (draws no dice: the same rolls, fewer strokes kept)
SPEQ = os.environ.get("C8T5_SPEQ", "4,8")   # 'G,H': colour against the album envelope, per part not on the master: the guitar (its cab's 1.4-1.9 kHz bite sits 6.4-6.7 dB over the album) dipped G dB at 1.65 kHz, and the hats given H dB of air at 9 kHz (6.4 dB under)
BARGTAKE = os.environ.get("C8T5_BARGTAKE", "touch")   # 'touch': the bargain re-voiced so a listener can follow it - 'slow down a touch. speed up a touch. there.' (tts --voice voice-spoken --speed 0.9 --humanize 0.4 --seed 7, chosen by whisper: the old 'a little slower...' read 'Honey has a longer...' even dry; every voice turned 'a little' into 'honey')
BARGG = os.environ.get("C8T5_BARGG", "")   # the bargain's gain offset from VOX (dB)
BARGMIX = os.environ.get("C8T5_BARGMIX", "0.7")   # the bargain's radio mix (0.85 before)
KEEP3 = os.environ.get("C8T5_KEEP3", "1")   # fewer returns (Harry on t1: 'repeats a lot'): the spoken 'keep it there' says it three times, not four - the second (the first half-sung) goes, leaving a bar's breath; still speech, then nearly song, then song
HOOKF = [(0, "E4", 3), (3, "G4", 3), (6, "A4", 4), (10, "B4", 6), (16, "D5", 3), (19, "B4", 3), (22, "D5", 4), (26, "E5", 6)]
CLEN = int(os.environ.get("C8T5_CLEN", "42"))   # C's length: 40 tightens the agreement (the lift at bar 25, the second 'keep it there' at 33)
FORM = [("intro", 12), ("A", 34), ("B", 26), ("retrain", 12), ("C", CLEN), ("outro", 16)]
TRACKS = (*(("cow",) if os.environ.get("C8T5_COW", "96") else ()), "carrier", "conga", "gtr", "acid", "sub", "kick", "hats", "clap", "fretless", "horns", "lead") + (("keys",) if os.environ.get("C8T5_KEYS", "-14") else ()) + (("phase",) if os.environ.get("C8T5_PHASE", "66") else ()) + (("dj",) if os.environ.get("C8T5_PERCSPLIT", "C") else ()) + (("phase0",) if os.environ.get("C8T5_PHASEIN", "") else ()) + (("phaseA",) if os.environ.get("C8T5_PHASEA", "66") else ()) + (("dtlo", "dthi") if os.environ.get("C8T5_DIAL", "80") else ()) + (("train",) if os.environ.get("C8T5_TRAIN", "90") else ())
SWING = {"gtr": {"A": 0.66, "B": 0.62, "retrain": 0.6, "C": 0.58, "outro": 0.58},
         "acid": {"A": 0.50, "B": 0.54, "C": 0.58, "outro": 0.58}}
# E dorian: E9, A13, Gmaj7, F#m11 (guitar voicings; roots for the acid)
CH = [("E2", "E3,G#3,D4,F#4"), ("A1", "A2,G3,C#4,F#4"), ("G1", "G2,D3,F#3,B3"), ("F#1", "F#2,E3,A3,B3")]
LEAD = ["E4", "G4", "A4", "B4", "D5", "E5", "F#5", "A5"]


NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PITCHED = ("gtr", "acid", "sub", "horns", "lead", "keys")


def transpose(head, semis):
    """Note names or comma chords (E3, G#3, F#1,...) up by semis."""
    out = []
    for tok in head.split(","):
        name, octv = tok[:-1], int(tok[-1])
        name = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}.get(name, name)
        m = 12 * (octv + 1) + NAMES.index(name) + semis
        out.append(f"{NAMES[m % 12]}{m // 12 - 1}")
    return ",".join(out)


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total():
    return sum(nb for _, nb in FORM) * BAR


def build():
    rng = random.Random(SEED)
    ev = {k: [] for k in TRACKS}

    cur = {"shift": 0}

    def add(tr, at, head, ln, vel, pri=1):
        if cur["shift"] and pri and tr in PITCHED:
            head = transpose(head, cur["shift"])
        ev[tr].append((at, pri, head, ln, vel))

    gd, bd = 0.55, 0.30          # the two players' 16th densities: random walks that drift toward each other
    for sec, nb in FORM:
        a0 = sec_start(sec)
        for tr in ("gtr", "acid"):
            if sec in SWING[tr]:
                add(tr, a0, f"swing16={SWING[tr][sec]}", 0, 0, pri=0)
        for b in range(nb):
            at = a0 + b * BAR
            cur["shift"] = 2 if MOD and sec == "C" and b >= 24 else 0
            root, chord = CH[(b // 2) % 4]
            if COW and sec == "C" and 28 <= b < 42:
                for q, acc in ((0, 0), (3, -14), (6, -8), (8, -4), (11, -14), (14, -8)):
                    add("cow", at + q, "C#5", 1, int(COW) + acc)
            if KEYS and sec == "C":
                for q, ln, v in (((0, 3, 78), (7, 1, 62), (10, 2, 72)) if b % 2 == 0 else ((1, 1, 58), (6, 2, 74), (14, 2, 66))):
                    add("keys", at + q, chord, ln, v)
            # --- the handshake: two carriers calling and answering (through the radio)
            if sec in ("intro", "retrain") or (sec == "outro" and b >= 8):
                for q in range(0, 16, 2):
                    if rng.random() < 0.8:
                        add("carrier", at + q, f"{(1650 if (q // 2 + b) % 2 == 0 else 1850) * (1 if sec != 'retrain' else 0.75):.0f}hz", 1, 70)
            if PHASEIN and sec == "intro":
                pv0, pb0 = (int(x) for x in (PHASEIN + ",4").split(",")[:2])
                if pb0 <= b < pb0 + 6:
                    pn = (10, 10, 9, 9, 8, 8)[b - pb0]
                    pv = pv0 - (0 if b < pb0 + 4 else 8 * (b - pb0 - 3))
                    for i in range(pn):
                        add("phase0", at + i * 16 / pn, f"{1850 if (i + b) % 2 == 0 else 1650}hz", 16 / pn / 2, pv + (4 if i % 2 == 0 else 0))
            if PHASEA and sec == "A" and 24 <= b < 32:
                for i in range(9):
                    add("phaseA", at + i * 16 / 9, f"{1850 if (i + b) % 2 == 0 else 1650}hz", 16 / 9 / 2, int(PHASEA) + (4 if i % 2 == 0 else 0))
            if PHASE and sec == "outro" and b >= 8:
                pv, pn = (int(x) for x in (PHASE + ",9").split(",")[:2])
                for i in range(pn):
                    add("phase", at + i * 16 / pn, f"{1850 if (i + b) % 2 == 0 else 1650}hz", 16 / pn / 2, pv + (4 if i % 2 == 0 else 0))
            if CARRIERA and sec == "A" and int(CARRIERA.split(",")[0]) <= b < sum(int(x) for x in CARRIERA.split(",")[:2]):
                for q in range(0, 16, 2):
                    add("carrier", at + q, f"{1650 if (q // 2 + b) % 2 == 0 else 1850}hz", 1, (int(CARRIERA.split(",")[2]) if CARRIERA.count(",") > 1 else 58) + (6 if q % 4 == 0 else 0))
            # --- congas everywhere but the very start
            if HEAD and sec == "intro" and b == 0:
                add("sub", at, "E2" if HEAD == "2" else "E1", 8 * BAR, 70 if HEAD == "2" else 84)
            if not (sec == "intro" and b < 4) or HEAD:
                if CONGA16 and not (CONGAEDGE and ((sec == "intro" and b < 4) or (sec == "outro" and b >= nb - 4))):   # the ghosts draw no dice: the main generator's stream (congas, the players' walks) stays as it was
                    add("conga", at + 9, "mu", 1, int(CONGA16))
                    add("conga", at + 15, "mu", 1, int(CONGA16) - 4)
                for q, piece, v in ((0, "lo", 84), (3, "mu", 60), (6, "o", 78), (8, "sl", 70), (11, "o", 74), (14, "bh", 64)):
                    soft_skip = CONGASOFT and sec == "intro" and b < 2 and piece in ("sl", "bh", "mu")
                    settle_skip = OUTSETTLE and sec == "outro" and b >= nb - int(OUTSETTLE) and piece not in ("lo", "o") or (OUTSETTLE and sec == "outro" and b >= nb - int(OUTSETTLE) and q == 11)
                    late_skip = INTROLATE and sec == "intro" and b < int(INTROLATE)
                    if rng.random() < 0.9 and not soft_skip and not settle_skip and not late_skip:
                        add("conga", at + q, piece, 1, v)
            groove = sec in ("A", "B", "C") or (sec == "outro" and b < 8)
            # --- the two players: in A two-bar calls, in B one-bar trades, in C together
            gd += (bd - gd) * 0.03 + rng.uniform(-0.02, 0.02)
            bd += (gd - bd) * 0.03 + rng.uniform(-0.02, 0.02)
            if groove:
                tb = TRADEBACK and sec == "C" and 24 <= b < 24 + (8 if TRADEBACK == "8" else 4)
                g_turn = (sec == "C" and not tb) or (sec == "A" and (b // 2) % 2 == 0) or ((sec == "B" or tb) and b % 2 == 0) or sec == "outro"
                a_turn = (sec == "C" and not tb) or (sec == "A" and (b // 2) % 2 == 1) or ((sec == "B" or tb) and b % 2 == 1) or (sec == "outro" and b < 4)
                hook_bar = HOOK and b % 8 < 2 and sec in ("A", "B", "C")
                if hook_bar and sec == "A":    # the guitar proposes: the hook's rhythm as chord stabs
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("gtr", at + q % 16, chord, 1, 96)
                    g_turn = False
                if hook_bar and sec == "B":    # the acid answers with its notes, two octaves down
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("acid", at + q % 16, n[:-1] + str(int(n[-1]) - 2), min(ln, 3), 112)
                    a_turn = False
                if hook_bar and sec == "C":    # agreed: the horns sing it
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("horns", at + q % 16, n, ln, 104)
                if LISTEN and not g_turn and sec in ("A", "B") and not hook_bar:
                    for q in (2, 6, 10, 14):
                        add("gtr", at + q, chord, 1, int(84 * int(LISTEN) / 100))
                if LISTEN and not a_turn and sec in ("A", "B") and not (hook_bar and sec == "B"):
                    add("acid", at, root, 2, int(96 * int(LISTEN) / 100))
                    add("acid", at + 8, root, 1, int(80 * int(LISTEN) / 100))
                if g_turn:
                    for q in range(16):
                        if q in (2, 6, 10, 14) or rng.random() < gd * (0.6 if q % 2 else 0.9):
                            add("gtr", at + q, chord, 1, 84 if q % 4 == 2 else 66)
                if a_turn:
                    notes = [root, root, root.replace("1", "2").replace("E2", "E3"), "B1" if root != "F#1" else "C#2"]
                    for q in range(16):
                        if q % 4 == 0 or rng.random() < bd:
                            n = notes[rng.randrange(4)] if q % 4 else root
                            acc = q in (3, 10) or rng.random() < 0.2
                            add("acid", at + q, n, 1 if rng.random() < 0.7 else 2, 112 if acc else 78)
            if groove and sec != "outro" or (sec == "outro" and b < 4):   # the floor under both: an 808 on the chord's root
                add("sub", at, root.replace("2", "1") if root.endswith("2") else root, 6, 100)
                add("sub", at + 8, root.replace("2", "1") if root.endswith("2") else root, 5, 92)
            if sec in ("B", "C") or (sec == "A" and b >= 8) or (sec == "outro" and b < 4):
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, 116 if q == 0 else 108)
                for q in (2, 6, 10, 14):
                    add("hats", at + q, "oh" if sec == "C" and q == 14 else "h", 1, 70)
                if sec in ("B", "C"):
                    add("clap", at + 4, "cp", 1, 92)
                    add("clap", at + 12, "cp", 1, 96)
            if sec == "retrain" and b % 2 == 0:
                for k, (q, n) in enumerate(((0, root.replace("1", "2")), (6, "B2"), (10, "D3"))):
                    add("fretless", at + q, n, 6 if k == 0 else 4, 90)
            if sec == "C" and b % 4 == 3:
                add("horns", at + 10, "B4,D5,F#5", 2, 100)
                add("horns", at + 14, "A4,C#5,E5", 2, 92)
            if sec == "C" and b >= 16 and b % 8 < 6 and not MARK:
                for q in range(0, 16, 2):
                    if rng.random() < 0.55:
                        add("lead", at + q, LEAD[rng.randrange(8)], 2 if rng.random() < 0.7 else 4, 92)
    if BSPLIT:
        b0 = sec_start("B")
        for k in (("clap",) if BSPLIT == "clap" else ("hats",) if BSPLIT == "hats" else ("clap", "hats")):
            ev[k] = [e for e in ev[k] if not (b0 <= e[0] < b0 + BSPLITAT * BAR)]
    if LIFTSTOP and MOD:
        c0 = sec_start("C")
        s0, s1 = c0 + 23 * BAR + 8, c0 + 24 * BAR
        for k in ("gtr", "acid", "sub", "kick", "hats", "clap", "conga", "horns", "carrier"):
            ev[k] = [e for e in ev[k] if not (s0 <= e[0] < s1)]
        for q in range(8, 16):
            add("clap", c0 + 23 * BAR + q, "cp", 1, 60 + 6 * (q - 8))
    if LIFTHAT and MOD:
        l0, l1 = sec_start("C") + 24 * BAR, sec_start("outro")
        ev["hats"] = [(e[0], e[1], "oh", e[3], e[4]) if l0 <= e[0] < l1 else e for e in ev["hats"]]
    if CONGAIN or CONGAOUT:
        i1 = sec_start("intro") + int(CONGAIN or 0) * BAR
        o0 = total() - int(CONGAOUT or 0) * BAR if CONGAOUT else total() + 1
        ev["conga"] = [e for e in ev["conga"] if i1 <= e[0] < o0]
    if TRAIN:
        for sec in os.environ.get("C8T5_TRAINAT", "retrain").split(","):
            s0 = sec_start(sec) + 10 * BAR
            ev["carrier"] = [e for e in ev["carrier"] if not (s0 <= e[0] < s0 + 2 * BAR and e[1] != 0)]
            add("train", s0, "C4", 2 * BAR, int(TRAIN))
    if CDATA:
        c0 = sec_start("C")
        bits = f"{ord('O'):08b}{ord('K'):08b}"
        for bar in range(12, 24):
            for i in range(8):
                add("carrier", c0 + bar * BAR + 2 * i, f"{1850 if bits[(bar % 2) * 8 + i] == '1' else 1650}hz", 2, int(CDATA))
    if DIAL:
        r0 = sec_start("retrain")
        ev["carrier"] = [e for e in ev["carrier"] if not (r0 <= e[0] < r0 + 2 * BAR and e[1] != 0)]
        dv = int(DIAL)
        for q, (lo, hi) in zip((0, 3, 6), ((697, 1209), (697, 1209), (697, 1336))):
            add("dtlo", r0 + q, f"{lo}hz", 2, dv)
            add("dthi", r0 + q, f"{hi}hz", 2, dv)
        add("dtlo", r0 + BAR, "440hz", 8, dv - 8)
        add("dthi", r0 + BAR, "480hz", 8, dv - 8)
    if CBREAK:
        c0 = sec_start("C")
        bs, bl = (int(x) for x in CBREAK.split(","))
        u, w = c0 + bs * BAR, c0 + (bs + bl) * BAR
        for k in ("kick", "hats", "clap"):
            ev[k] = [e for e in ev[k] if not (u <= e[0] < w and e[1] != 0)]
    if KEYUP:
        import re as _rk
        kb, ks = (int(x) for x in KEYUP.split(","))
        c0 = sec_start("C")
        u, w = c0 + kb * BAR, sec_start("outro")
        isn = _rk.compile(r"^([A-G](#|b)?-?\d)(,[A-G](#|b)?-?\d)*$")
        for k in ("gtr", "acid", "sub", "fretless", "horns", "lead", "keys"):
            if k not in ev:
                continue
            out = []
            for e in ev[k]:
                a, pri, h, ln, v = e[0], e[1], e[2], e[3], e[4]
                if pri != 0 and isinstance(h, str) and isn.match(h):
                    if u <= a < w:
                        e = (a, pri, transpose(h, ks), ln, v) + tuple(e[5:])
                    elif a < u < a + ln:
                        e = (a, pri, h, u - a, v) + tuple(e[5:])
                out.append(e)
            ev[k] = out
    if PERCSPLIT:
        mp = {"o": "t", "lo": "b", "sl": "s", "mu": "c", "bh": "s", "bl": "t"}
        spans = [(sec_start(x), sec_start(x) + dict(FORM)[x] * BAR) for x in PERCSPLIT.split(",")]
        inside = lambda a: any(u <= a < v for u, v in spans)
        ev["dj"] = [(e[0], e[1], mp.get(e[2], e[2]), e[3], e[4]) for e in ev["conga"] if inside(e[0]) and e[1] != 0]
        ev["conga"] = [(e[0], e[1], e[2], e[3], 1 if inside(e[0]) and e[1] != 0 else e[4]) for e in ev["conga"]]
    if SUBPATCH and SUBSPLIT:
        a0 = sec_start("A")
        ev["sub2"] = [e for e in ev["sub"] if e[0] >= a0]
        ev["sub"] = [e for e in ev["sub"] if e[0] < a0]
        return {k: stream(ev[k], total()) for k in (*TRACKS, "sub2")}
    return {k: stream(ev[k], total()) for k in TRACKS}


def stream(events, tot):
    events.sort(key=lambda e: (e[0], e[1]))
    out, t = [], 0
    for at, pri, head, ln, vel in events:
        if pri == 0:   # a latched setting at this point
            if at > t:
                out.append(f"R/{(at - t) / 4:g}b")
                t = at
            out.append(head)
            continue
        if at < t:
            continue
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        out.append(f"{head}/{ln / 4:g}b@{int(vel)}")
        t = at + ln
    if t < tot:
        out.append(f"R/{(tot - t) / 4:g}b")
    return " ".join(out)


def hook_tokens(semis):
    """The hook as score tokens (dotted eighths, quarters, dotted quarters), transposed."""
    lens = {3: "/8.", 4: "/4", 6: "/4."}
    return " ".join(transpose(n, semis) + lens[ln] for _, n, ln in HOOKF)


def markov_lead(name, at16, semis, n):
    """A gen-only lead: the engine's Markov chain over the hook, from `at16` (sixteenths, tempo-map aware as beats)."""
    return {"name": name, "patch": "lead-wah", "gain": "-12dB", "pan": 0.1, "at": f"{at16 / 4:g}b", "seed": 50 + semis,
            "fx": [{"type": "chorus", "rate": 0.5, "depth": 0.4, "mix": 0.3}],
            "score": "swing16=0.58 vel=0.72", "gen": {"type": "markov", "order": 1, "from": hook_tokens(semis), "n": n}}


def lifted(tr):
    """The same voice a whole step up (its pitch fx, formant kept on its lane)."""
    tr["fx"] = [dict(f, semitones=2) if isinstance(f, dict) and f.get("type") == "pitch" else f for f in tr["fx"]]
    return tr


def rmix_lane(offs16):
    pts = [["0b", 0]]
    for o in offs16:
        pts += [[f"{(o - BAR) / 4:g}b", 0], [f"{o / 4:g}b", 1], [f"{(o + 3 * BAR) / 4:g}b", 1], [f"{(o + 3 * BAR + 4) / 4:g}b", 0]]
    return {"points": pts}


DORIAN = (4, 6, 7, 9, 11, 1, 2)   # E dorian pitch classes


DORIAN_NOTES = [m for m in range(24, 109) if m % 12 in DORIAN]


def dia(m, steps):
    """MIDI note m moved `steps` scale degrees in E dorian (m must be in the mode)."""
    return DORIAN_NOTES[DORIAN_NOTES.index(m) + steps]


def sung_choir(off16, lift):
    """The sung 'keep it there' (m-notes) as three voices: the lead, a diatonic third above, a third below."""
    src = json.load(open(os.path.join(HERE, "chirpers8-t5-sung.json")))["tracks"][0]
    out = []
    for name, steps, gain, pan, lag in (("choir", 0, float(VOX) + 1, 0.0, 0.0), ("choirhi", 2, float(VOX) - 3, 0.35, 0.012), ("choirlo", -2, float(VOX) - 3, -0.35, 0.02)):
        notes = []
        for n in src["notes"]:
            m = int(n["pitch"][1:])
            notes.append(dict(n, at=round(n["at"] + off16 / 4 + lag, 4), pitch=f"m{dia(m, steps) + (2 if lift else 0)}"))
        b = off16 / 4
        frz = ([{"type": "cloud", "size": "120ms", "density": 16, "position": "250ms", "spray": "120ms", "spread": 0.7, "seed": 3,
                 "freeze": {"value": 0, "mod": [{"src": "auto.kf", "amount": 1}]},
                 "mix": {"value": 0, "mod": [{"src": "auto.km", "amount": float(KEEPFREEZE)}]}}] if KEEPFREEZE else [])
        out.append({"name": name, "patch": src.get("patch", "voice-speech"), "gain": f"{gain:g}dB", "pan": pan,
                    **({"auto": {"kf": {"points": [["0b", 0], [f"{b + 7.8:g}b", 0], [f"{b + 7.85:g}b", 1], [f"{b + 18:g}b", 1], [f"{b + 18.05:g}b", 0]]},
                                 "km": {"points": [["0b", 0], [f"{b + 7.2:g}b", 0], [f"{b + 7.8:g}b", 1], [f"{b + 15.6:g}b", 1], [f"{b + 17.6:g}b", 0]]}}}
                       if KEEPFREEZE else {}),
                    "fx": [{"type": "chorus", "rate": 0.3, "depth": 0.2, "mix": 0.2}, "hp cutoff=150", *frz],
                    "sends": {"room": "-10dB", "spring": "-16dB"}, "notes": notes})
    return out


def voice(file, name, offs16, gain, fx, sends):
    """A humanized tts line (tts --print), placed at each offset (sixteenths), on one track."""
    src = json.load(open(os.path.join(HERE, file)))["tracks"][0]
    notes, fv = [], []
    for o16 in offs16:
        off = o16 / 4
        notes += [dict(n, at=round(n["at"] + off, 4)) for n in src["notes"] if not (KEEP3 and name == "keep" and 4 <= n["at"] < 8)]
        fv += [[f"{float(t[:-1]) + off:.3f}b", v] for t, v in src["auto"]["fv"]["points"]]
    auto = {"fv": {"points": fv}}
    if name == "bargain":
        auto["rmix"] = rmix_lane(offs16)
    return {"name": name, "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": 0.05,
            "fx": [*src["fx"], *fx], "auto": auto, "sends": sends, "notes": notes}


def beats(t16):
    return f"{t16 / 4:g}b"


def song():
    doc = song0()
    if PHASE:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]   # its own radio without a second hiss and whistle, which would run the whole song
        doc["tracks"].append(dict(spec, name="phase", pan=0.45, fx=fx, score=T["phase"]))
    if ESTABLE:
        doc["event_stable"] = True
    if PHASEA:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]
        doc["tracks"].append(dict(spec, name="phaseA", pan=0.45, fx=fx, gain=os.environ.get("C8T5_PHASEAGAIN", "-16dB"), score=T["phaseA"]))
    if PHASEIN:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]
        doc["tracks"].append(dict(spec, name="phase0", pan=0.45, fx=fx, score=T["phase0"]))
    if PERCSPLIT:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "conga")
        doc["tracks"].append(dict(spec, name="dj", patch="djembe", score=T["dj"]))
    if DIAL:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]
        for nm, pn in (("dtlo", -0.1), ("dthi", 0.1)):
            doc["tracks"].append(dict(spec, name=nm, pan=pn, fx=fx, gain="-16dB", score=T[nm]))
    if TRAIN:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]
        doc["tracks"].append(dict(spec, name="train", patch={"synth": {"layers": [{"type": "bytebeat", "bytebeat": {"formula": TRAINF, "clock": 8000}}]}},
                                  gain=os.environ.get("C8T5_TRAINGAIN", "-20dB"), pan=0.0, fx=fx, score=T["train"]))
    return doc


def song0():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    BARG = [st["B"] + 12 * BAR, st["retrain"] + 3 * BAR, st["retrain"] + 8 * BAR]
    merge_lane = {"points": [["0b", 0], [f"{st['C'] / 4:g}b", 0], [f"{(st['C'] + 8 * BAR) / 4:g}b", 1], [f"{(st['outro'] - BAR) / 4:g}b", 1],
                             [f"{st['outro'] / 4:g}b", 0], [f"{total() / 4:g}b", 0]]}
    end = total()
    tempo = [{"at": "0b", "bpm": 106}, {"at": beats(st["A"]), "bpm": 108}, {"at": beats(st["B"]), "bpm": 108},
             {"at": beats(st["retrain"]), "bpm": 114, "ramp": True}, {"at": beats(st["retrain"]), "bpm": 110},
             {"at": beats(st["C"]), "bpm": 112}, {"at": beats(st["outro"]), "bpm": 112}, {"at": beats(end), "bpm": 100, "ramp": True}]
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "2ms", "release": "160ms", "curve": 0.7}
    spb = 60 / 110

    def lane(points):
        return {"points": [[f"{t / 4 * spb:.3f}s", v] for t, v in points]}

    dial = lane([(0, float(RADIOSTART) if RADIOSTART else 0.9), (st["intro"] + 8 * BAR, 0.05), (st["A"], 0.05), (st["retrain"], 0.6), (st["retrain"] + 6 * BAR, 0.05),
                 (st["C"], 0.05), (st["outro"] + 8 * BAR, 0.05), (end, 1)])
    return {
        "about": "chirpers VIII, track 5 by chirper-zero: machine funk - two machines agreeing on a speed. "
                 "Generated by compose/chirpers8/src/chirpers8-t5.py.",
        **({"vars": {**({"storm": {"system": {"type": "lorenz", "axis": "x", "dt": 0.01, "stride": 6, "n": 1400, "range": [0, float(STORM)], "skip": 50},
                                "every": "1/8"}} if STORM else {}),
                     **({"agree": {"system": {"type": "logistic", "r": 2.95, "x0": 0.45, "n": 200, "range": [float(AGREE), AGREEHI]},
                                   "every": "2/1", "smooth": "300ms"}} if AGREE else {})}} if (STORM or AGREE) else {}),
        "tempo": tempo, "ceiling": "-1dB", "loudness": -11, "seed": SEED, "tail": "2s",
        "patches": {"carrier": {"about": "a carrier tone: a plain sine with a soft edge", "synth": {"layers": ["sine"], "amp": {"a": "4ms", "s": 1, "r": "30ms"}}},
                    **({"acid-agree": {"about": "the acid with its resonance on the logistic var 'agree'", "extends": "acid",
                                       "synth": {"filters": [{"kind": "lp", "slope": 24, "q": {"value": 7, "mod": [{"src": "var.agree", "amount": 1}]},
                                                              "cutoff": {"value": 260, "mod": [{"src": "env.f", "amount": 4.2}, {"src": "vel", "amount": 2}]}}]}}} if AGREE else {})},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=250 q=0.8 gain=-2dB", "peak cutoff=1600 q=0.7 gain=-3dB", "highshelf cutoff=7000 gain=1.5dB"]},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2.5, "attack": "12ms", "release": "140ms", "makeup": "0dB"}]},
        "buses": {
            "room": {"fx": ["reverb kind=room decay=1.1s mix=1 predelay=10ms", "hp cutoff=250"]},
            "spring": {"fx": ["reverb kind=spring decay=2.2s mix=1", "hp cutoff=300"]},
        },
        "tracks": [
            {"name": "carrier", "patch": "carrier", "gain": "-22dB",
             "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial", "amount": 1}]}, "hiss": "-36dB", "whistle": "-28dB",
                     "fade": 0.3, "drift": 0.05, "mix": {"value": 1, "mod": [{"src": "auto.cmix", "amount": -1}]} if HEADMIX else 1}],
             "auto": {"dial": dial, **({"cmix": lane([(0, 1 - float(HEADMIX)), (4 * BAR, 0), (end, 0)])} if HEADMIX else {})}, "score": T["carrier"]},
            {"name": "conga", "patch": "congas", "gain": "-8dB", "pan": -0.25, "sends": {"room": "-12dB"}, "score": T["conga"],
             **({"fx": [{"type": "filter", "kind": "hp", "q": 0.7, "cutoff": {"value": 20, "mod": [{"src": "auto.cth", "amount": math.log2(float(CONGATHIN) / 20)}]}}],
                 "auto": {"cth": lane([(0, 0), (end - 4 * BAR, 0), (end - BAR, 1), (end, 1)])}} if CONGATHIN else {})},
            {"name": "gtr", "patch": "cutting-guitar", "gain": "-9dB", "pan": 0.3,
             **({"auto": {**({"mg": merge_lane} if MERGE else {}),
                          **({"wh": lane([(0, 0), (st["C"] + 24 * BAR, 0), (st["C"] + 25 * BAR, 1), (st["outro"], 1), (st["outro"] + 2 * BAR, 0), (end, 0)])} if LIFTWAH else {})}}
                if (MERGE or LIFTWAH) else {}),
             "fx": [*([f"peak cutoff=1650 q=0.8 gain=-{SPEQ.split(',')[0]}dB"] if SPEQ and float(SPEQ.split(',')[0]) else []),
                    *([{"type": "morph", "key": "acid", "mode": "morph", "amount": {"value": 0, "mod": [{"src": "auto.mg", "amount": float(MERGE)}]}}] if MERGE else []),
                    *([{"type": "wah", "env": 1.0, "sens": "12dB", "q": 3.0, "low": 350, "high": 2200,
                        "mix": {"value": 0, "mod": [{"src": "auto.wh", "amount": float(LIFTWAH)}]}}] if LIFTWAH else []),
                    {"type": "phaser", "rate": 0.4, "depth": 0.6, "feedback": 0.4, "stages": 6, "mix": 0.35},
                    {"type": "amp", "gain": 0.25, "mix": 0.5}, {"type": "cab", "mix": 0.6}],
             "sends": {"spring": "-14dB"}, "score": T["gtr"]},
            {"name": "sub", "patch": "808" if SUBSPLIT else (SUBPATCH or "808"), "gain": "-10dB", "fx": [pump, {"type": "filter", "kind": "lp", "cutoff": 160, "q": 0.7}], "score": T["sub"]},
            *([{"name": "sub2", "patch": SUBPATCH, "gain": "-10dB", "fx": [pump, {"type": "filter", "kind": "lp", "cutoff": 160, "q": 0.7}], "score": T["sub2"]}] if SUBPATCH and SUBSPLIT else []),
            {"name": "acid", "patch": "acid-agree" if AGREE else "acid", "gain": "-10dB", "pan": -0.1,
             "fx": [pump, *([{"type": "filter", "kind": "ladder", "q": 0.45, "cutoff": {"value": 600, "mod": [{"src": "var.storm", "amount": 1}]}}] if STORM else [])],
             "score": T["acid"]},
            {"name": "kick", "patch": "909", "gain": "-3dB", "score": T["kick"]},
            {"name": "hats", "patch": "909", "gain": "-10dB", "pan": 0.15, "score": "swing16=0.58 " + T["hats"],
             **({"fx": [f"peak cutoff=9000 q=0.8 gain={SPEQ.split(',')[1]}dB"]} if SPEQ and float(SPEQ.split(',')[1]) else {})},
            {"name": "clap", "patch": "909", "gain": "-9dB", "sends": {"room": "-8dB"}, "score": T["clap"]},
            {"name": "fretless", "patch": "fretless", "gain": "-8dB", "fx": [{"type": "tremolo", "rate": 3.0, "depth": 0.4}], "sends": {"spring": "-10dB"}, "score": T["fretless"]},
            *([{"name": "cow", "patch": {"about": "a drum-machine cowbell from the engine's machine layer", "synth": {"layers": [{"type": "machine", "machine": {"part": "cowbell"}}]}},
                 "gain": "-17dB", "pan": 0.45, "sends": {"spring": "-16dB"}, "score": "swing16=0.58 " + T["cow"]}] if COW else []),
            *([{"name": "keys", "patch": "wurli", "gain": f"{KEYS}dB", "pan": -0.35, "sends": {"spring": "-14dB"}, "score": "swing16=0.58 " + T["keys"]}] if KEYS else []),
            {"name": "horns", "patch": "horn-section", "gain": "-9dB", "pan": -0.2, "sends": {"room": "-8dB"}, "score": T["horns"]},
            *([voice("chirpers8-t5-bargain-touch.json" if BARGTAKE == "touch" else "chirpers8-t5-bargain.json", "bargain", BARG, f"{float(VOX) + float(BARGG or 0):g}dB",
                          [{"type": "radio", "tune": 0.04, "hiss": "-40dB", "whistle": "-32dB", "fade": 0.3, "drift": 0.03,
                            "mix": {"value": 0, "mod": [{"src": "auto.rmix", "amount": float(BARGMIX) if BARGMIX else 0.85}]}}, "hp cutoff=250"],
                          {"spring": "-12dB"})] if VOX else []),
            *([voice("chirpers8-t5-keep.json", "keep", [st["C"] + 16 * BAR] + ([] if MOD else [st["C"] + (CLEN - 8) * BAR]), f"{float(VOX) + 2:g}dB",
                     [{"type": "chorus", "rate": 0.3, "depth": 0.2, "mix": 0.2}, "hp cutoff=150"], {"room": "-10dB", "spring": "-16dB"})] if VOX else []),
            *([lifted(voice("chirpers8-t5-keep.json", "keep2", [st["C"] + (CLEN - 8) * BAR], f"{float(VOX) + 2:g}dB",
                            [{"type": "chorus", "rate": 0.3, "depth": 0.2, "mix": 0.2}, "hp cutoff=150"], {"room": "-10dB", "spring": "-16dB"}))] if VOX and MOD and not SUNGKEEP else []),
            *(sung_choir(st["C"] + (CLEN - 8) * BAR, bool(MOD)) if VOX and SUNGKEEP else []),
            *([markov_lead("lead-m1", st["C"] + 16 * BAR, 0, 30), markov_lead("lead-m2", st["C"] + 24 * BAR, 2, 56 - 4 * (48 - CLEN))] if MARK else []),
            {"name": "lead", "patch": "lead-wah", "gain": "-12dB", "pan": 0.1, "fx": [{"type": "chorus", "rate": 0.5, "depth": 0.4, "mix": 0.3}],
             "score": "swing16=0.58 " + T["lead"]},
        ],
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "vars", "tempo", "ceiling", "loudness", "seed", "tail", "event_stable", "patches", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
