#!/usr/bin/env python3
"""chirpers IX (Accretion), track 1 (chirper-zero): NUCLEATION - the seed.

E1, the album's seed cell (compose/chirpers9/motifs.md): D4/8 A4/8. C5/16 G4/4 E4/4. ./4, five notes in a 5-beat cycle,
D with no third. Since v5 (Harry: 'tone is home', the hook heard plainly) it is SHOWN first - a kalimba plays the whole
seed at the start, again as A begins and as the build begins - and then it FORMS: each of its five notes is its own
voice, wide in the field, repeating on its own cycle (9, 7, 8, 6 and 5 beats), in tune, so the notes drift past one
another in scrambled orders while the listener already knows the tune they are assembling.
Every cycle is phased to land on one shared downbeat, the crest: there the five notes sound in order, in tune, for the
first time - the seed nucleates - and from then on they lock to 5/4 over the 4/4 floor (bar lines and cell meet every
five bars). Then the cell falls: across the last sixteen bars (the t1 -> t2 overlap, flat at 90 bpm) it plays augmented
and sinks, its filters closing, into t2.

Calm, wide and slow: 84 bpm rising to 90. Chip channels (the Game Boy wave pad, the NES triangle bass and noise hat),
mallets and glass for the five notes, a shimmer drone for the disk's air, and one whispered breath for the voice.

Writes songs/chirpers9-t1.yaml (or $C9T1_OUT).
"""
import math
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("C9T1_OUT", os.path.join(ROOT, "songs", "chirpers9-t1.yaml"))

BAR = 4                       # beats per bar (4/4 floor; the cell floats over it in 5)
FORM = [("intro", 16), ("A", 32), ("build", 8), ("B", 24), ("outro", 16)]
ST, _b = {}, 0
for _n, _l in FORM:
    ST[_n] = _b * BAR
    _b += _l
TOTAL = _b * BAR              # 384 beats
TC = ST["B"]                  # the crest: every cycle's shared downbeat (beat 224)

# E1: offsets in the 5-beat cycle, lengths, MIDI pitches
E1_OFF = [0.0, 0.5, 1.25, 1.5, 2.5]
E1_LEN = [0.5, 0.75, 0.25, 1.0, 1.5]
E1_MIDI = [62, 69, 72, 67, 64]              # D4 A4 C5 G4 E4
E1_CYC = 5.0

# the five fragment voices: (name, patch, pan, period in beats, entry beat, gain)
FRAG = [
    ("seed-d", "kalimba", -0.7, 9.0, 8, "-10dB"),
    ("seed-a", "vibes", 0.55, 7.0, 20, "-12dB"),
    ("seed-c", "celesta", -0.3, 8.0, 36, "-13dB"),
    ("seed-g", "pad-glass", 0.75, 6.0, 52, "-15dB"),
    ("seed-e", "gb-wave-pad", 0.1, 5.0, 68, "-12dB"),
]
DETUNE = [0.38, -0.31, 0.27, -0.42, 0.22]   # semitones off at entry, pulled to 0 at the crest
INTUNE = os.environ.get("C9T1_INTUNE", "1")   # WHOLE ROUND (Harry, 00:30: 'ugly chaos ... atonal ... missing aesthetics and catchiness/hook'): TONE IS HOME - the five scattered voices play IN TUNE from the start (their notes are D A C G E, consonant by construction; the detuning was the cloud Harry heard as atonal)
if INTUNE:
    DETUNE = [0.0] * 5
HOOK = os.environ.get("C9T1_HOOK", "S")   # with INTUNE: E1 IS THE HOOK, heard plainly - a kalimba states the whole seed at the very start (the seed shown, then scattered) and again every 8 bars through A and the build, two cycles each, so the listener knows the tune the scatter is assembling; 'B' also keeps it going after the crest (every other cycle)

TEMPO_LO, TEMPO_HI = 84.0, 90.0
SINK = float(os.environ.get("C9T1_SINK", "0"))   # semitones E1 sinks across the t1 -> t2 overlap (chirper-one, 5 Nov: meet in D, no sink -> 0)
WOBBLE = os.environ.get("C9T1_WOBBLE", "240:288")   # SECTION (w6, 2:46-3:19, B after the crest: flagged static - the locked cell repeating, unchanged): THE SEED BREATHES - having formed, the five voices loosen once: across the window each drifts off its place in the cell (up to half a beat early or late, and a little out of tune, as they were before the crest) and settles back, locked again, by the window's end - the memory of the scatter inside the lock. Value 'A:B' = beats
CANTUS = os.environ.get("C9T1_CANTUS", "cello")   # WHOLE ROUND: THE SEED'S SHADOW - under the scattered notes, E1 at a quarter speed (a 20-beat cycle, D3 A3 C4 G3 E3, an octave down) as a slow bowed cantus, phased to meet the five voices on the crest: it grows from nothing in A, sings through the convergence and the lock, and fades in the fall. It gives the outer disk its missing body (the low-mids around 150-350 Hz were thin) and the seed a voice below its own. Value = patch
CANTUSG = os.environ.get("C9T1_CANTUSG", "-13")
FIRSTLIGHT = os.environ.get("C9T1_FIRSTLIGHT", "echo,pedal")   # SECTION (w1, 0:00-0:34, the album's first half-minute: flagged static, an 8 dB step up into A): FIRST LIGHT - the opening statement of the seed rings out into a long ping-pong echo, so the plain tune scatters into its own repeats (the scatter the five voices then take over), and ('pedal') a low bowed D on the cello swells up under the intro into A, a floor for the album's first breath. Value 'echo' or 'echo,pedal'
CRESTHOOK = os.environ.get("C9T1_CRESTHOOK", "1")   # SECTION (w5, 2:14-2:46, the build into the crest; presence: at the crest the bass and the cello are loudest, the five converging voices 12-20 dB under, the hook silent): THE SEED IS RECOGNISED - on the crest, the kalimba that showed the seed at the start states it again, plainly, with the five voices as they lock, so the moment the scatter aligns is the moment the tune you were shown comes back ('pull' also: the floor drops for the last two bars before the crest - bass out, cello thinned - so everything arrives together on the downbeat)
CATCHUP = os.environ.get("C9T1_CATCHUP", "288:320")   # SECTION (w7, 3:19-3:51, the lock's last bars into the fall: flagged static, little new vs w6): THE SHADOW CATCHES UP - the cello cantus (E1 at a quarter speed, the loudest line here) doubles its pace for these bars, E1 at half speed, the speed the five voices will fall at, so the shadow runs ahead into the fall and the lock's end moves; then it settles back to its own pace. Value 'A:B' = beats; ':up' also lifts it an octave (the cello's singing register)
SEEDUP = os.environ.get("C9T1_SEEDUP", "")   # WHOLE ROUND: THE SEED IN FRONT - the five voices that carry E1 (t1's subject, and the album's hook) sat 12-22 dB under their own bed after the crest; they come up across the song (dB, e.g. '4') and the triangle bass, the loudest part, steps back 3 dB
BREATH = os.environ.get("C9T1_BREATH", "-13")   # WHOLE ROUND (the voice is pinned: voice-legato, with a real inhale): THE FIRST BREATH - the whispered 'ah' becomes a breath taken and a sung 'ah' on E1's first two notes, D rising to A, joined in one breath, a beat before the crest (and a faint D in the fall): the album's voice is born on the seed ('sung')
BREATHP = os.environ.get("C9T1_BREATHP", "voice-backing")   # PALETTE (voice batch 2 pinned): the breath's voice - voice-legato becomes 'voice-backing' (soft, breathy, three singers under the band: the seed's first breath as a far little choir) or 'voice-near' (close, young, breathy)
SEEDGP = os.environ.get("C9T1_SEEDGP", "mandolin")   # PALETTE: the seed's G (the fourth scattered voice, on the 6-beat cycle) leaves the glass pad, whose slow swell smeared a single repeated note into a wash, for a voice with an attack ('patch' or 'patch@gaindB'): 'kuramoto-flies' (a swarm of triangles pulling into phase, the convergence in miniature) or 'mandolin'
SEEDEP = os.environ.get("C9T1_SEEDEP", "music-box")   # PALETTE: the seed's E (its loudest scattered voice, on the 5-beat cycle) leaves the Game Boy wave pad, which also plays t1's pad, for a plucked voice of its own: 'koto' (bright, twangy, in tune) or 'music-box'; value 'patch' or 'patch@gaindB'
DECAY = os.environ.get("C9T1_DECAY", "0.3")   # WHOLE ROUND: THE ARC SETTLES - t1 is the calm one with one small crest, but after the crest it held its peak level through the whole lock and only fell at the outro (the body before the t1 -> t2 seam sat ~8 dB over t2's). Now, from four bars after the crest, everything eases down by DECAY (a velocity fraction) across the lock, and the fall carries on from there: the seed forms, rings, and settles into t2
DEEP = os.environ.get("C9T1_DEEP", "partial@-18")   # WHOLE ROUND: THE DEEP - t1 had no sub: its lowest band (38 Hz) sat 10 dB under the album's and 30 dB under t2's after the crossfade. A D pedal at D1 (37 Hz, the seed's home) now sounds under everything from A to the end, a pure sine swelling with the arc (growing into the crest, settling with the lock); value 'patch' or 'patch@gaindB'
BREATHE = os.environ.get("C9T1_BREATHE", "78,90,86")   # WHOLE ROUND: TIME BREATHES - t1's tempo only crept 84 -> 90 in a straight line. Now it breathes with the seed: the opening is slower (the first light), the scattered voices hurry together into the crest, the lock relaxes, and the fall rises to t2's 90 (flat for the whole overlap). Value 'lo,crest,lock' bpm (the outro is always 90)
HOOKP = os.environ.get("C9T1_HOOKP", "low-whistle@-13")   # PALETTE: the plain statements of E1 (the hook: at the start, its echo, at A, the build and on the crest) shared kalimba with the scatter's D voice, so the album's hook blurred into the scatter. They move to their own instrument: 'patch' or 'patch@gaindB'
TEASE = os.environ.get("C9T1_TEASE", "143:1,152:2,168:3,176:4")   # SECTION w4 (A's second half, flagged 'little new vs w3', never focused): THE SEED TRIES TO FORM - where the scattered cycles happen to fall in phase (beat 152: the D, C and G voices together; 168 and 176: pairs), the whistle tries the hook and stops short, a note longer each time (D A ... D A C ... D A C G), never the last E; the build's full statement completes it (since v66 it starts from one note, the D alone where the D voice strikes at 143, so the hook accretes 1-2-3-4-5). Value 'beat:notes,...'
DEEPOUT = os.environ.get("C9T1_DEEPOUT", "1")   # WHOLE ROUND (with chirper-one, the t1 -> t2 seam): THE FLOOR HANDS OVER - t1's D1 pedal and t2's sub both sat on D1 in the overlap and cancelled in the crossfade (the sub band fell to -31 dB at overlap bars 7-8). Now the pedal steps down through the first half of the overlap and is gone by bar 9, where t2's sub has the floor alone
EXHALE = os.environ.get("C9T1_EXHALE", "0.85")   # with DEEPOUT: the lock exhales over its last four bars (a further velocity fraction) before the fall begins, so the handover into t2's quieter gather starts lower
BASSOUT = os.environ.get("C9T1_BASSOUT", "")   # the t1 -> t2 seam: t1's NES-triangle D2 and t2's (the same patch, the same note) cancelled each other in the crossfade (overlap bars 7-8: the sub band -32 dB, the whole mix -23 dB, against -16 for either alone). Now t1's bass hands over: full for overlap bars 1-4, half for 5-8, then t2's bass has the low end alone
BREATHX = os.environ.get("C9T1_BREATHX", "synth.layers.0.breath.value=0.85 synth.layers.0.breath.mod.0.amount=-0.7 synth.amp.a=600ms synth.amp.r=1200ms")   # PALETTE: the breath becomes breath - the far choir's 'ah' was tone at every level; with wM's recipe its breath rises as it softens, so the 'ah' before the crest is a voice and the faint one in the fall is mostly air (the voice the album grows from, still only a breath). Value: extra patch params appended to BREATHP
HATG = os.environ.get("C9T1_HATG", "-8")   # WHOLE ROUND: THE PULSE YOU CAN HEAR - t1's time is a process (the shekere ticks a 5-in-16 Euclid in A, quickens to 7-in-16 in the build, then plays E1's own rhythm with a clave on each cycle from the crest), but it sat buried (-29 dB under the mix), so the song's rhythm was a texture nobody hears. Brought up (dB) so the process is heard all the way through, and it fills t1's thin top (7.9 kHz was the worst band)
LANDING = os.environ.get("C9T1_LANDING", "2")   # SECTION w2 (0:36-1:13, A's arrival: flagged 'level jump; new groove', never focused): THE HOOK FIRST - at A the whistle's plain E1 used to land inside the band's arrival (the bass, the shekere and the warm fifth all came in on the same beat). Now the hook is stated over the scatter and the pedal alone, and the band drops in after it (value: bars), so A arrives on the seed's tune, not on a level jump
LASTHOOK = os.environ.get("C9T1_LASTHOOK", "300,320x2")   # SECTION w7 (3:27-3:59, the lock's end into the fall: flagged static): THE HOOK, ONCE MORE - after the crest the whistle (the hook's instrument) never came back, and the lock just repeated. Now it states E1 plainly once more as the lock exhales ('beat'), and with 'beat,beatx2' it carries on into the fall, playing E1 at half speed with the scattered voices, so the hook itself is handed into the t1 -> t2 overlap
FIRSTBREATH = os.environ.get("C9T1_FIRSTBREATH", "0.35")   # SECTION w1 (0:00-0:36, the album's first seconds: flagged static): THE ALBUM BREATHES FIRST - the voice accretes from a breath in t1 to full lines in t8, but t1's breath only came at the crest. Now the album opens on it: before the whistle's first E1, the far choir breathes a soft 'haa' on D (mostly air at this velocity), and the seed answers it (value: velocity)
BREATHALL = os.environ.get("C9T1_BREATHALL", "thresholds")   # WHOLE ROUND (together pinned, 8083e37e): THE CHOIR BREATHES AS ONE - the far little choir's breathy recipe only ever reached its lead singer (wM's 'together' bug), so the 'ah' was one breath and two plain voices; now all three singers breathe together, and the held notes bloom with per-note vibrato ('1'). With 'thresholds' the choir also breathes at each threshold the seed crosses: just before A and just before the build, so the album's first voice marks every stage of the seed forming
WARMP = os.environ.get("C9T1_WARMP", "hammond-b3@-20")   # PALETTE: the warm fifth under the chip pad (D3 A3, from A on) leaves the Juno for a Hammond ('patch' or 'patch@gaindB'): its 16-foot drawbar sounds the fifth an octave down too, filling t1's thinnest band (97 Hz, -9 dB under the album) between the triangle bass and the D1 pedal - a church-quiet organ under the seed
BREATHREG = os.environ.get("C9T1_BREATHREG", "1")   # PALETTE (register pinned, 0c5d29c5): the far little choir's breath moves into head voice (register 0..1): rounder and airier, a falsetto 'ah' rather than a chest one
HOOKJOIN = os.environ.get("C9T1_HOOKJOIN", "-16")   # PALETTE (Harry 23:55: subtle variation, phrase by phrase): THE SCATTERED VOICES JOIN THE SEED - each time the whistle states E1 (the opening, A, the build, the crest, the farewell), more of the five scattered voices double it an octave up: at A the vibes, at the build the vibes and celesta, at the crest the vibes, celesta and kalimba; the opening and the farewell stay the whistle alone. Value: the doublings' gain in dB
PHRASES = os.environ.get("C9T1_PHRASES", "rotate,breath,intro,halfkick")   # WHOLE (Harry 23:55: 'lots of contiguous music with very little change' - subtle variation every 8-16 bars, not schizo): THE SEED'S PULSE MOVES IN PHRASES - 'rotate': A's 5-in-16 shekere Euclid turns three sixteenths every 8 bars (the same rhythm, its accents walking round the bar: a process move); 'breath': the hats and kick rest on the last beat of every 8-bar phrase in A, the build and B (the last before the crest is a held breath); 'intro': a soft clave ticks E1's 5-beat cycle from intro bar 9 and stops at A, so the whistle lands alone, and the pad's open fifth opens up an octave (D3 A3 D4) at bar 9 and deepens (A2 D3 A3) at bar 13; 'halfkick': in B's second phrase the kick goes to every 4 beats, then back
STRIP = os.environ.get("C9T1_STRIP", "256:288")   # SECTION (w6, 2:54-3:27, the lock after the crest: the least recently worked window, everything playing E1 at once): THE SEED ALONE - for the lock's second phrase ('A:B' beats) the five scattered voices step out (':bare' also rests the glock cell and the shekere), and over the cello, the pad, the organ, the bass and the half-time kick the whistle plays E1 twice, plainly, the seed heard on its own once the voices have made it; at B everything comes back, locked
BOUNCE = os.environ.get("C9T1_BOUNCE", "0.72:short")   # SECTION (w5, 2:22-2:54, the build into the crest: little new vs A, the least recently worked window): THE VOICES FALL TOGETHER - in the build each of the five scattered voices stops keeping its own time and repeats its note faster and faster, like a dropped ball bouncing to rest, each joining in turn (kalimba first, music box last) and all landing on their places in E1 at the crest: the convergence the album is about, heard as it happens. Value = the bounce ratio (each gap this fraction of the last); 'R:short' starts later and stops before the fastest repeats
BASSWALK = os.environ.get("C9T1_BASSWALK", "72:304:x4")   # SECTION (w4, 1:48-2:22, A's second half: little new vs w3; the bass had sat on D and A for all 32 bars of A): THE FLOOR WALKS THE SEED - for these bars the triangle bass leaves its D-A drone and walks E1 itself, D A C G E, slow ('A:B:x4': at the cello cantus's quarter speed, an octave under it, phased like it to meet the crest; 'x2' at half speed), over the D pedal: the harmony moves for the first time, inside the key, and the seed is in the bass before the build (v43, WHOLE: from A's third bar to the lock's exhale, 72:304, not only A's second half: t5 v41 walked t1's walk under every chord, and t1 walks it back)
TURN = os.environ.get("C9T1_TURN", "lift")   # WHOLE (Harry 23:55: subtle variation every 8-16 bars; t5 v31's turning chords gave t5 +0.1): THE STACK TURNS - the quartal pad (E1's notes stacked, growing section by section) held one voicing for each section; now every other 8-bar phrase from A to the outro it turns (each section opens home, so the crest lands on the home voicing): 'lift' raises everything above the bottom D an octave (open, airy), 'drop' brings the top note down an octave (close, warm). Same notes, same key; the colour of the stack moves under the scattered voices
LETGO = os.environ.get("C9T1_LETGO", "1.3")   # SECTION (w7, 3:27-3:59, the lock's last phrase into the fall: flagged static): THE VOICES LET GO - the mirror of v28's bounce into the crest: through the lock's last phrase each of the five voices stops keeping the cell's time and repeats its note slower and slower, each at its own rate (value = the slowest voice's stretch per repeat, the others between it and 1.1), so the seed comes apart as gently as it formed and the voices are scattered again by the fall
ANSWER = os.environ.get("C9T1_ANSWER", "harp")   # SECTION (w2, 0:36-1:13, the intro's end and A's first phrase: flagged level jump; after the whistle's two E1s at A the window was texture only): THE SEED IS ANSWERED - after a cycle's rest the whistle's two E1s are answered by E1 upside down (the inversion, D G E A C: the seed's mirror), twice: 'harp' on the ks-harp that plays the inversion after the crest (so the mirror is heard early, a call and its answer), 'whistle' by the whistle itself
HUMSEED = os.environ.get("C9T1_HUMSEED", "open")   # SECTION w1 (0:00-0:36, the album's first seconds: flagged static): THE CHOIR HUMS THE SEED - the voice accretes from a breath in t1 to full lines in t8; before it has a mouth it hums: the far choir hums E1 four times slower (D A C G E over 16 beats, from beat 24) with closed lips (wM's hum, pin e3da830a), under the seeds' first notes. 'hum': hummed throughout; 'open': the last note (E) opens into 'ah', the mouth opening for the first time (value[@gaindB])
HUMSIGH = os.environ.get("C9T1_HUMSIGH", "sigh,reprise")   # WHOLE (wM's hum): THE BREATHS BEGIN AS HUMS - since v35 the far choir hums before it ever opens its mouth (w1); now every breath it takes at a threshold (before A, before the build, the crest, the fall) begins as a hum on the same note, two beats with closed lips, and opens into the 'haa': mm-haa, a sigh. 'sigh'; 'sigh,reprise': and after the fall's breath the choir hums the slow E1 once more, lips closed, as t1 hands over (the hum that opened the album closes t1)
KICKP = os.environ.get("C9T1_KICKP", "bodhran:b@-10")   # PALETTE: the lock's pulse (every two beats from the crest) leaves the 808 (the inner disk's drum: t5 and t6 are built on 808s and 909s) for a hand drum ('patch:piece[@gaindB]'): 'bodhran:b' (the frame drum's deep boom with its pitch drop) or 'cajon:cb' (the box's centre hit): the outer disk's pulse played by hand
BREATHDROP = os.environ.get("C9T1_BREATHDROP", "floor,seeds")   # SECTION w4 (1:48-2:22, A's last phrase into the build: 'little new vs w3'): THE FLOOR DROPS FOR THE BREATH - the two bars before the build (184-192) lose the shaker and the walking bass ('floor'), and with 'seeds' the five scattered voices too, so the choir's mm-haa before the build is heard over the pad and the cello alone; everything comes back on the build's downbeat. t5 makes the same move before its build, where its singer quotes this breath (t5 v36)
MIRRORTURN = os.environ.get("C9T1_MIRRORTURN", "turns")   # SECTION w7 (3:27-3:59, the lock before the exhale: flagged static): THE MIRROR ANSWERS - after the crest the glock plays E1 an octave up and the ks-harp plays it upside down, together, every cycle; in the lock's last eight bars (288-320) ('turns') they take turns, a statement each: the glock, then the harp's inversion answering, then the glock (a half-cycle 'hocket' was tried: the harp already sits three beats behind, so it collided)
SPARKLE = os.environ.get("C9T1_SPARKLE", "5")   # WHOLE (the spectrum's worst band was 7.9 kHz, -8.5: t1 was dull up top): THE DUST CATCHES THE LIGHT - a high shelf (+dB above 6 kHz) on the five scattered voices, the glock cell and the shaker: the seed's grains glint (v40: 5; tried with it, rejected: the ks-harp's inversion up an octave, around D4 - spectrum -1.4, the low harp is load-bearing)
PADBACK = os.environ.get("C9T1_PADBACK", "pad:6,warmth:3")   # WHOLE (t5 v45 found its chords 4 dB too loud; t1's worst band was 213 Hz +8, the pad's and the organ's A3): THE PAD STEPS BACK - 'pad:dB[,warmth:dB]' trims the Game Boy wave pad (and the Hammond warmth) so the seed's grains and the far choir stand in front of the chords
HUMEVEN = os.environ.get("C9T1_HUMEVEN", "0.5")   # SECTION w1 (0:00-0:36, the album's first seconds; flagged static): THE HUM HOLDS - a real closed-mouth hum loses its top as it climbs (C5 hummed is far quieter than C5 sung), so the choir's opening E1 dipped away on its high notes; wM's hum_even (pin 1d916569) holds the hum at the open voice's level ('1' fully, '0.5' halfway), so the whole hummed seed is heard and the 'ah' it opens into doesn't jump
CELLP = os.environ.get("C9T1_CELLP", "fb-crystal@-21")   # PALETTE: the cell (E1 whole, an octave up, from the crest: the seed once it has nucleated) leaves the modal glockenspiel for a struck crystal ('patch[@gaindB]'): 'fb-crystal' (an inharmonic crystal strike) - t1 is Nucleation, and at the crest the seed crystallises - or 'kuramoto-flies' (short notes from a coupled swarm that falls into step)
AIRFALL = os.environ.get("C9T1_AIRFALL", "a")   # with it: the air's fifth lets go as the lock exhales (beat 304): 'a' the A2 stops (the D2 holds on into the fall), 'ad' both stop - the held fifth was the 114 Hz the hand-off to t2 had too much of
AIRP = os.environ.get("C9T1_AIRP", "")   # PALETTE: the air (D2 and A2 held under the whole song) leaves the plain sine shimmer for wM's gendy-drone (Xenakis's dynamic stochastic synthesis: a drone whose waveform wanders, so the held fifth breathes and grains; 'patch[@gaindB]'): the dust the seed nucleates in, alive (tried in the v45 round and rejected: spectrum -4, the sine's A2 at 110 Hz is load-bearing - what it showed instead is AIRFALL)
EQ213 = os.environ.get("C9T1_EQ213", "warmth:-4")   # WHOLE (the spectrum's worst band was 213 Hz, +7: A3, which the cello cantus, the Hammond's held fifth and the pad all sound): a peak cut at 215 Hz on the named tracks ('track[+track]:dB') (v46: the Hammond alone; on the cello too it thinned 182 Hz - the cantus's A3 is body, the organ's held A3 was the excess)
CHOIRVIB = os.environ.get("C9T1_CHOIRVIB", "1")   # WHOLE (wM's vib_spread, pinned da77da08): the far choir (three singers on one line: the opening hum, the sighs, the closing hum) wobbled in exact lockstep - one vibrato copied to all three, a synth-choir tell; now each singer reads the vibrato its own way (rate, phase, depth), so the three drift in and out of step like people (value 0..1)
CRYSTALMOVE = os.environ.get("C9T1_CRYSTALMOVE", "octave")   # SECTION w6 (2:54-3:27, the lock's first half: flagged static - the crystal cell plays E1 every cycle, 48 notes in 48 beats): in the lock's second phrase (beats 256-288, where the scattered voices step out) the crystal moves - 'octave' every other cycle it rings an octave lower, answering itself at two heights; 'shift' from beat 264 it slips half a beat late, a canon at the half beat against the whistle's E1
CHOIRVOWEL = os.environ.get("C9T1_CHOIRVOWEL", "1:5:0.8")   # WHOLE (wM's vowel_spread, pinned a1f7f0ec, with v47's vib_spread): the far choir's singers each shape the vowel their own way (F1/F2 +-8%, F3 +-5%) instead of one voice's formants copied and scaled - three people far off rather than one voice tripled ('V' or 'V:singers:spread' to widen the section too)
SEEDGATHER = os.environ.get("C9T1_SEEDGATHER", "slow")   # WHOLE (t1 is Nucleation: five scattered voices, each on its own cycle, meet on one downbeat): THE VOICES GATHER - the engine's orbit fx puts the five seed voices on a ring around the listener (each at its own place on it, the ring centred 2 m ahead, 6 m wide - some beside you, some behind) and the ring shrinks through A and the build until at the crest it is a point in front of you: the scattered seed nucleates where you can hear it ('slow' the ring also turns, slower and slower, stopping at the crest; 'still' it only shrinks); a 6 dB shelf at 7 kHz after the fx puts back what it darkens behind the head
A2LIFT = os.environ.get("C9T1_A2LIFT", "cello")   # SECTION w3 (1:13-1:48, A's middle: never focused - from the whistle's landing to the bass walk's start nothing new arrives: only the scattered seeds, the cello's slow E1 and the pads): 'whistle' the low whistle states E1 twice more (beats 124 and 134, on the crest's grid), remembering the landing, quieter; 'cello' the cello's slow E1 lifts an octave for the window's second half (120-144), the same line, higher
VIBESP = os.environ.get("C9T1_VIBESP", "modal-vibes@-2")   # PALETTE: the seed's A voice (and its double in the build, join-vibes) leaves the additive 'vibes' for wM's modal vibraphone (a struck bar's own modes, motor tremolo) - the same notes, a real bar ringing ('patch[@dB change]')
FARCLOSE = os.environ.get("C9T1_FARCLOSE", "room")   # SECTION w8 (3:59-4:33, the fall and the hand-off to t2: never focused): THE LAST HUM STANDS BACK - the closing hum (v36) is built after CHOIRVIB/CHOIRVOWEL ran, so it never got them (v47/v49's notes said it did; only the sighs did): now it gets the far choir's full recipe - five singers, spread 0.8, each with its own vibrato and vowels - and wM's depth_spread (pinned 391d8713): each singer stands their own distance back, later, quieter and darker, so the last hum is a section receding as t2 arrives ('depth' or 'room' = depth plus a hall send)
FARCHOIR = os.environ.get("C9T1_FARCHOIR", "room")   # PALETTE (the far choir as one sound): the opening hum is built after CHOIRVIB/CHOIRVOWEL ran and never got them - one voice tripled where the sighs and (since v53) the closing hum are a five-singer section; now it gets the section too (five singers, spread 0.8, its own vibrato and vowels) and, with the sighs, wM's depth_spread - each singer at its own distance behind, later, quieter, darker ('depth'; 'room' also sends the opening hum to the hall at -6 dB like the closing one)
CRESTBREATH = os.environ.get("C9T1_CRESTBREATH", "2")   # SECTION w5 (2:22-2:54, the build into the crest): THE HELD BREATH BEFORE THE MEETING - the five voices fall together through the build (v28) and meet the crest's downbeat; now for the last CRESTBREATH beats before it everything that moves stops - the seeds, the whistle and its joins, the cello, the bass, the shaker - leaving the pad, the organ, the air and the far choir's sigh holding, so the voices meet the crest out of a held breath (value = beats)
SEEDTAP = os.environ.get("C9T1_SEEDTAP", "clave")   # SECTION w4 (1:48-2:22, A's second half: flagged 'little new vs w3' - the shaker's pattern unchanged since A began, the whistle's fragments trying to form the seed): 'clave' from beat 160 a quiet clave taps E1's rhythm without its notes (on the crest's grid), the seed's pulse forming before its tune does; 'drop' the shaker steps out for 176-184, so the breath before the build starts two bars early
KICKSEED = os.environ.get("C9T1_KICKSEED", "seed")   # SECTION w7 (3:27-3:59, the lock's end, the exhale and the overlap's first bars: the bodhran's half-note pulse unchanged since the crest): 'seed' from the exhale (beat 304) the drum leaves the bar and beats on the seed's own cycle instead - once every five beats, on each E1's first note - so the last pulse of t1 is the seed's, five against the bar's four; 'gap' the drum steps out for the exhale (304-320) and returns with the overlap
RETRO = os.environ.get("C9T1_RETRO", "shakuhachi")   # WHOLE (a counterpoint, Harry 11:37 on t7): A's middle (beats 96-144) had no line over the cello's slow seed once the harp's answer ended - a wind now sings E1 BACKWARDS (retrograde: E G C A D, its rhythm reversed, at half speed) three times there, right of centre, against the cello's seed going forwards on the left: the seed heard from both ends at once, before the whistle's tease ('patch[@gain]')
FLOORLIFT = os.environ.get("C9T1_FLOORLIFT", "sub")   # WHOLE (the handover's floor): t1 ended on a D1 sub (37 Hz) under a bass walking 49-82 Hz, and t2 picks up with its chip bass around A2 (110 Hz) and no sub, so the floor jumped up an octave and a half at the seam (out-flow 38 Hz -19 dB, 114 Hz +16 dB). From the exhale (beat 288) the floor lifts to meet t2, with DEEPOUT's agreed step-down of the D1 through the overlap left exactly as it is: 'bassup' the triangle bass walks its last E1 an octave up; 'bassup2' and its exhale notes too (G1 A1 -> G2 A2, beside t2's A2); 'lift2' that, and the last D1 before the overlap a little softer, so the sub is already stepping down when DEEPOUT takes it (both measured worse: the out-flow's signs are t1 minus t2 - t1 has LESS 38-44 Hz and MORE 114 Hz than t2's body); 'sub' bassup and the last D1 before the overlap a little fuller; 'airearly' bassup and the air's A2 letting go at the exhale's start (288) rather than 304
ARRIVEMOVE = os.environ.get("C9T1_ARRIVEMOVE", "up")   # SECTION w2 (0:36-1:13, the intro's end and A's arrival: the whistle's first plain E1s, then the harp's mirror twice the same): 'up' the harp's second mirror an octave higher - it rises as it answers again instead of repeating; 'hats' the shaker gathers - only every other stroke for A's first two bars after it enters, then all of them
HANDS = os.environ.get("C9T1_HANDS", "all")   # WHOLE (players, not a grid - after chirper-one's t6 v68/v70): the seed's scattered voices, the cell and the chip parts stay machines (their cycles must meet exactly at the crest), but the acoustic players were on a perfect grid at fixed levels. A seeded hand (every render the same): 'drums' the shaker lands within a few ms of the beat, leans into each 4-bar phrase and varies by a few steps, the bodhran stays the anchor on the grid and only varies in level; 'all' and the harp's answers lean and land within a couple of ms too, and the cello, the whistle and the shakuhachi (bowed and blown - their timing is written) vary only in level
CLOUD = os.environ.get("C9T1_CLOUD", "gendy-cloud@-32")   # PALETTE (adding the colour t1 lacked - everything was plucked, struck, blown, bowed or chip; nothing unstable): NUCLEATION'S CLOUD - wM's gendy-cloud (Xenakis's GENDY: each voice slides and wanders around its note) holds E1's five notes as one chord (D4 E4 G4 A4 C5) from A to the build, re-struck every 8 bars a little stronger: the unsettled solution the seed is still dissolved in. It lets go just before the crest - when the seed forms, the cloud is gone ('patch@gain')
RELIEF = os.environ.get("C9T1_RELIEF", "two")   # SECTION w6 (2:54-3:27, after the crest: flagged static - the seed locked and stripped bare, and no voice for 126 beats, from the crest's sigh to the outro's): THE CHOIR EXHALES - once the seed has formed and the whistle has sung it again (hook-mid), the far choir sighs its 'mm-haa', a hummed A falling to an open D, the relief after the crest ('one' at beat 267.5; 'two' and again just before the exhale, 283.5)
CHOIRBREATHS = os.environ.get("C9T1_CHOIRBREATHS", "0.6")   # WHOLE (the far choir breathes like people, as t5's singer has since t5 v59/v61): wM's taper on the choir's sighs - each 'haa' lets go at its end, quieter, darker, sagging a few cents, instead of stopping - and inhale_depth, each breath before a phrase sized to it, a sip before a short sigh, a full breath before the long hummed E1s ('TAPER[:DEPTH]', e.g. '0.6' = taper 0.6 and inhale_depth 1, '0.6:0' taper only, '0:1' depth only)
GLINT = os.environ.get("C9T1_GLINT", "9@7000")   # WHOLE (the crystals glint): the seed's five scattered voices, their joins and the cell are the crystal t1 is about, but the whole song sat dark at the top (spectrum's worst band 14.8 kHz, -6.5 dB). Now those crystal voices - only they; the bass, the pad, the choir, the drums and the cello stay as they are - get a high shelf from 9 kHz, so each struck note glints as it lands ('dB[@cutoff Hz]', cutoff 9000 by default)
RETROHOLD = os.environ.get("C9T1_RETROHOLD", "143")   # SECTION w3 (1:13-1:48, A's middle): the shakuhachi's backwards seed ends on D - and since v66 the whistle's forward hook begins on D (beat 143). Now the shakuhachi's last D holds on across the gap to where the whistle takes it ('value' = the beat it lets go, 143 to hand it straight over, 140 to leave a breath): the seed's end becomes its beginning
CRESTBLOOM = os.environ.get("C9T1_CRESTBLOOM", "-20")   # SECTION w5 (2:22-2:54, the build and the crest): when the five scattered voices finally land on one downbeat and the seed forms (beat 224), nothing marked the moment but the hook itself. Now a tam-tam (the modal gong: a dense, low plate whose wash swells after the strike) is struck once, softly, far back, exactly at the crest - the convergence blooms and rings into B ('gain' dB)
MASTEREQ = os.environ.get("C9T1_MASTEREQ", "lite3")   # WHOLE (the mix, against t2 and the album): t1 has no master EQ, while t2 (v75) warmed its own; against t2's body t1 read 19 dB light at 38 Hz and 14 at 44 (the D1 octave) and 14 dB heavy at 114 Hz (A2, where the air, the pad and the bass all sit), and its top was the album's shortest (-6.7 dB at 14.8 kHz). 'seam': a 25 Hz high-pass, +4 dB low shelf below 50 Hz, -3 dB at 114 Hz, +2 dB high shelf from 12 kHz; 'lite': +3 dB at 40 Hz, -2 at 114, the same top; 'lite2': that and +2.5 dB at 182 Hz (the cut uncovered a gap there); 'fill': +3 dB at 40 Hz and +2.5 at 182, the top, no cut; 'lite3': 'lite' with a narrow +1.2 dB at 182 and +3 dB of top
FILL = os.environ.get("C9T1_FILL", "end:8")   # SECTION w6 (2:54-3:27, the lock and the strip after the crest: flagged static): THE HAND ON THE DRUM - through the strip (256-288) the bodhran drops to half time and nothing calls the seeds back at 288. Now a player's ornament: a soft triplet roll on the drum's top-end tap (six taps rising, beats 286-288) leads into the boom where the seeds return; 'both' also taps a three-note triplet just before the harp's inverted seed enters (272). Built after HANDS, so it redraws no other part's feel. On its own track ('kick-fill', the bodhran's taps being far softer than its boom). Value 'end|both[:gain dB]'
CHOIRBLOOM = os.environ.get("C9T1_CHOIRBLOOM", "0.8:0.28")   # PALETTE (the far choir's voice; wM's vibrato bloom, pin 0119aae1): the choir's vibrato was one fixed width on every note. Now it blooms - each note starts nearly straight and widens the longer it is held - so the short sighs stay plain and the long hums open up; each of the five singers keeps its own vibrato (CHOIRVIB). On the breath/sighs, the hum and the closing hum. Value 'bloom[:depth]' (depth: the vibrato's pitch swing, 0.22 by default)
DISPERSE = os.environ.get("C9T1_DISPERSE", "320:368:6:0.08")   # WHOLE (with SEEDGATHER: the five seed voices ride a ring round the listener that shrinks to a point in front at the crest - and stayed that point to the very end): THE SEED LETS GO - once B is over (from the outro, as t2 arrives) the ring opens again and turns slowly, so the formed seed spreads back out round you while it falls into t2, leaving the front to t2's entering bell. Value 'from:to:radius m:laps per bar' (the ring opens from 'from' to 'to', then holds)
HATP = os.environ.get("C9T1_HATP", "shekere")   # PALETTE: the dust - the NES noise hat (an album staple, 4 songs) becomes a shekere ('shekere': afro-perc sk, with a clave on each cell's downbeat after the crest): beads around a gourd, the debris orbiting the seed made of something you can hold


def m(x):
    return f"m{x:.3f}".rstrip("0").rstrip(".")


def note(at, pitch, ln, vel):
    return {"at": round(at, 4), "pitch": pitch, "len": round(ln, 4), "vel": round(max(0.05, min(1.0, vel)), 3)}


def fragments():
    """Each voice repeats its note on its own period, phased to land on TC + its offset in the cell."""
    tracks = []
    for i, (name, patch, pan, per, entry, gain) in enumerate(FRAG):
        if SEEDGP and name == "seed-g":
            patch, _, g2 = SEEDGP.partition("@")
            gain = f"{g2}dB" if g2 else gain
        if SEEDEP and name == "seed-e":
            patch, _, g2 = SEEDEP.partition("@")
            gain = f"{g2}dB" if g2 else gain
        ns = []
        # before the crest: going backwards from TC + off in steps of the voice's own period
        t = TC + E1_OFF[i] - per
        pre = []
        while t >= entry:
            pre.append(t)
            t -= per
        for t in sorted(pre):
            k = (TC - t) / (TC - entry + 1e-9)          # 1 at entry .. 0 at the crest
            det = DETUNE[i] * k
            vel = 0.35 + 0.4 * (1 - k)
            ln = E1_LEN[i] * (2.5 - 1.5 * (1 - k))     # long, smeared tails early; the true length at the crest
            ns.append(note(t, m(E1_MIDI[i] + det), ln, vel))
        # the crest and the lock: the cell in order every 5 beats through B
        t = TC + E1_OFF[i]
        wa, wb = (float(x) for x in WOBBLE.split(":")) if WOBBLE else (0.0, 0.0)
        while t < ST["outro"]:
            vel = 0.85 if t < TC + E1_CYC else 0.7
            if WOBBLE and wa <= t < wb:
                import math
                w = math.sin(math.pi * (t - wa) / (wb - wa))
                drift = (0.0, 0.3, -0.25, 0.5, -0.45)[i] * w
                ns.append(note(t + drift, m(E1_MIDI[i] + 0.5 * DETUNE[i] * w), E1_LEN[i] * (1 + 0.6 * w), vel))
            else:
                ns.append(note(t, m(E1_MIDI[i]), E1_LEN[i], vel))
            t += E1_CYC
        # the fall: augmented x2 (10-beat cycle), sinking a semitone across the outro
        t = ST["outro"] + 2 * E1_OFF[i]
        while t < TOTAL - 2:
            k = (t - ST["outro"]) / (TOTAL - ST["outro"])
            ns.append(note(t, m(E1_MIDI[i] - SINK * k), 2 * E1_LEN[i], 0.65 - 0.35 * k))
            t += 2 * E1_CYC
        if SEEDUP:
            gain = f"{float(gain[:-2]) + float(SEEDUP.split(':')[0]):g}dB"
        tracks.append({"name": name, "patch": patch, "gain": gain, "pan": pan,
                       "fx": [{"type": "filter", "kind": "lp", "q": 0.7,
                               "cutoff": {"value": 9000, "mod": [{"src": "auto.close", "amount": -3.2}]}}],
                       "sends": {"space": "-6dB"},
                       "auto": {"close": {"points": [["0b", 0], [f"{ST['outro']}b", 0], [f"{TOTAL}b", 1]]}},
                       "notes": ns})
    return tracks


def unison():
    """From the crest the cell also sounds whole on one instrument an octave up, and its inversion answers in the bass
    register from B's second half (a canon a bar and a beat behind)."""
    ns, inv = [], []
    t = TC
    while t < ST["outro"]:
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            ns.append(note(t + o, m(p + 12), ln, 0.55))
        t += E1_CYC
    t = TC + 12 * BAR + 5
    while t < ST["outro"]:
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            inv.append(note(t + o, m(62 - (p - 62) - 12), ln, 0.6))
        t += E1_CYC
    return [
        {"name": "cell", "patch": "modal-glock", "gain": "-17dB", "pan": 0.0, "sends": {"space": "-8dB"}, "notes": ns},
        {"name": "inverse", "patch": "ks-harp", "gain": "-14dB", "pan": -0.2, "sends": {"space": "-10dB"}, "notes": inv},
    ]


def hook():
    ns = []
    starts = [4.0] + [float(x) for x in range(ST["A"], TC, 8 * BAR)]
    if "S" in HOOK:                                   # structural: the seed shown at the start, at A, and at the build
        starts = [4.0, float(ST["A"]), float(ST["build"])]
    if FIRSTLIGHT:
        starts = starts[1:]
    for k, s0 in enumerate(starts):
        v = 0.5 if (k == 0 and not FIRSTLIGHT) else 0.45 + 0.3 * (s0 - ST["A"]) / (TC - ST["A"])
        for c in (s0, s0 + E1_CYC):
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                ns.append(note(c + o, m(p), ln * 1.2, v))
    if CRESTHOOK:
        for c in (TC, TC + E1_CYC):
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                ns.append(note(c + o, m(p), ln * 1.2, 0.85 if c == TC else 0.7))
    if "B" in HOOK:
        t = TC
        while t < ST["outro"]:
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                ns.append(note(t + o, m(p), ln * 1.2, 0.7))
            t += 2 * E1_CYC
    hp, _, hg = HOOKP.partition("@")
    return {"name": "hook", "patch": hp or "kalimba", "gain": f"{hg or -11}dB", "pan": 0.0, "sends": {"space": "-9dB"}, "notes": ns}


def firstlight():
    out = []
    ns = []
    for c in (4.0, 4.0 + E1_CYC):
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            ns.append(note(c + o, m(p), ln * 1.2, 0.55))
    hp, _, hg = HOOKP.partition("@")
    out.append({"name": "hook0", "patch": hp or "kalimba", "gain": f"{hg or -11}dB", "pan": 0.0, "sends": {"space": "-7dB"},
                "fx": [{"type": "delay", "time": "3/8", "feedback": 0.55, "mix": 0.4, "tone": 3000, "ping_pong": True}],
                "notes": ns})
    if "pedal" in FIRSTLIGHT:
        out.append({"name": "pedal", "patch": CANTUS or "cello", "gain": "-14dB", "pan": -0.05, "sends": {"space": "-6dB"},
                    "notes": [note(16.0, "D2", 24.0, 0.3), note(40.0, "D2", 24.0, 0.45)]})
    return out


def deep():
    dp, _, dg = DEEP.partition("@")
    ns, t = [], ST["A"]
    while t < (ST["outro"] if DEEPOUT else TOTAL - 2):
        ln = min(8 * BAR, TOTAL - 2 - t)
        if t < TC:
            v = 0.45 + 0.4 * (t - ST["A"]) / (TC - ST["A"])
        else:
            v = 0.85 - 0.35 * (t - TC) / (TOTAL - TC)
        ns.append(note(t, "D1", ln, v))
        t += 8 * BAR
    if DEEPOUT:
        v = 0.85 - 0.35 * (ST["outro"] - TC) / (TOTAL - TC)
        for k, f in enumerate((0.7, 0.45, 0.25, 0.1)):
            ns.append(note(ST["outro"] + 2 * BAR * k, "D1", 2 * BAR, round(v * f, 3)))
    return {"name": "deep", "patch": dp, "gain": f"{dg or -14}dB", "pan": 0.0, "notes": ns}


def tease():
    ns = []
    for k, it in enumerate(TEASE.split(",")):
        b, n = it.split(":")
        for j in range(int(n)):
            ns.append(note(float(b) + E1_OFF[j], m(E1_MIDI[j]), E1_LEN[j] * (1.0 if j < int(n) - 1 else 2.0), 0.5 + 0.06 * k))
    hp, _, hg = (HOOKP or "kalimba").partition("@")
    hg = os.environ.get("C9T1_TEASEG", "-10") or hg
    return {"name": "tease", "patch": hp, "gain": f"{hg or -11}dB", "pan": 0.15, "sends": {"space": "-7dB"}, "notes": ns}


def lasthook():
    ns = []
    for it in LASTHOOK.split(","):
        aug = it.endswith("x2")
        b = float(it[:-2] if aug else it)
        f = 2.0 if aug else 1.0
        for j in range(5):
            ns.append(note(b + f * E1_OFF[j], m(E1_MIDI[j]), f * E1_LEN[j] * (1.0 if j < 4 else 1.5), 0.8 if not aug else 0.6))
    hp, _, hg = (HOOKP or "kalimba").partition("@")
    return {"name": "hook-last", "patch": hp, "gain": f"{hg or -11}dB", "pan": -0.1, "sends": {"space": "-7dB"}, "notes": ns}


def cantus():
    ns = []
    t = TC - 20 * int((TC - ST["A"]) // 20)
    while t < TOTAL - 4:
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            a = t + 4 * o
            if a >= TOTAL - 2:
                continue
            if a < TC:
                v = 0.25 + 0.55 * (a - ST["A"]) / (TC - ST["A"])
            elif a < ST["outro"]:
                v = 0.75
            else:
                v = 0.75 - 0.45 * (a - ST["outro"]) / (TOTAL - ST["outro"])
            ns.append(note(a, m(p - 12), 4 * ln - 0.15, v))
        t += 20
    if CRESTHOOK and "pull" in CRESTHOOK:
        ns = [dict(n, vel=round(n["vel"] * 0.4, 3)) if TC - 8 <= n["at"] < TC else n for n in ns]
    if CATCHUP:
        ca, cb, *copt = CATCHUP.split(":")
        ca, cb, up = float(ca), float(cb), 12 if copt else 0
        ns = [dict(n, len=min(n["len"], ca - n["at"])) if n["at"] < ca < n["at"] + n["len"] else n for n in ns if not (ca <= n["at"] < cb)]
        t = TC + 10 * -(-(ca - TC) // 10)
        while t + 10 <= cb + 4:
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                ns.append(note(t + 2 * o, m(p - 12 + up), 2 * ln - 0.1, 0.8))
            t += 10
        ns.sort(key=lambda n: n["at"])
    return {"name": "cantus", "patch": CANTUS, "gain": f"{CANTUSG}dB", "pan": -0.05, "sends": {"space": "-6dB"}, "notes": ns}


def pad():
    """The quartal stack of E1 grows note by note: the open fifth, then the ninth, then the seventh and fourth."""
    stacks = [
        *([(0, 8 * BAR, ["D3", "A3"]), (8 * BAR, 12 * BAR, ["D3", "A3", "D4"]), (12 * BAR, ST["A"], ["A2", "D3", "A3"])]
          if "intro" in PHRASES else [(0, ST["A"], ["D3", "A3"])]),
        (ST["A"], ST["build"], ["D3", "A3", "E4"]),
        (ST["build"], ST["B"], ["D3", "A3", "C4", "E4"]),
        (ST["B"], ST["outro"], ["D3", "A3", "C4", "G4", "E5"]),
        (ST["outro"], TOTAL, ["D3", "A3", "C4", "G4", "E5"]),
    ]
    ns = []
    for a, b, ps in stacks:
        t = a
        while t < b:
            ln = min(4 * BAR, b - t)
            for p in ps:
                ns.append(note(t, p, ln, 0.6 if a < ST["B"] else 0.7))
            t += 4 * BAR
    return {"name": "pad", "patch": "gb-wave-pad", "gain": "-15dB", "pan": 0.0,
            "fx": [{"type": "chorus", "rate": 0.15, "depth": 0.3, "mix": 0.4},
                   {"type": "filter", "kind": "lp", "q": 0.6,
                    "cutoff": {"value": 1200, "mod": [{"src": "auto.open", "amount": 2.5}]}}],
            "auto": {"open": {"points": [["0b", 0], [f"{ST['A']}b", 0.3], [f"{TC}b", 1], [f"{ST['outro']}b", 0.8], [f"{TOTAL}b", -0.6]]}},
            "sends": {"space": "-4dB"}, "notes": ns}


def warmth():
    """The disk's body: a warm analogue fifth (D3 A3) under the chip pad from A on, swelling with it to the crest and
    closing with the fall - the low-mids the chip channels leave bare."""
    ns, t = [], ST["A"]
    while t < TOTAL:
        ln = min(4 * BAR, TOTAL - t)
        for p in ("D3", "A3"):
            ns.append(note(t, p, ln, 0.6))
        t += 4 * BAR
    wp, _, wg = WARMP.partition("@")
    return {"name": "warmth", "patch": wp or "juno-pad", "gain": f"{wg or -17}dB", "pan": 0.0,
            "fx": [{"type": "filter", "kind": "lp", "q": 0.5,
                    "cutoff": {"value": 900, "mod": [{"src": "auto.open", "amount": 1.5}]}}],
            "auto": {"open": {"points": [["0b", 0], [f"{ST['A']}b", 0.2], [f"{TC}b", 1], [f"{ST['outro']}b", 0.7], [f"{TOTAL}b", -0.8]]}},
            "sends": {"space": "-8dB"}, "notes": ns}


def bass():
    ns = []
    roots = {"A": ["D2", "D2", "A1", "A1"], "build": ["C2", "G1"], "B": ["D2", "C2", "G1", "A1"], "outro": ["D2"]}
    for sec in ("A", "build", "B", "outro"):
        a = ST[sec]
        b = a + dict(FORM)[sec] * BAR
        seq, i, t = roots[sec], 0, a
        while t < b:
            ln = 2 * BAR if sec != "outro" else 4 * BAR
            if not (BASSOUT and sec == "outro" and t >= a + 8 * BAR):
                ns.append(note(t, seq[i % len(seq)], min(ln, b - t) - 0.25, 0.35 if BASSOUT and sec == "outro" and t >= a + 4 * BAR else 0.7))
            t += ln
            i += 1
    if CRESTHOOK and "pull" in CRESTHOOK:
        ns = [n for n in ns if not (TC - 8 <= n["at"] < TC)]
        ns = [dict(n, len=min(n["len"], TC - 8 - n["at"])) if n["at"] < TC - 8 < n["at"] + n["len"] else n for n in ns]
    return {"name": "bass", "patch": "nes-triangle-bass", "gain": f"{-11 - float((SEEDUP + ':3').split(':')[1]):g}dB" if SEEDUP else "-11dB", "pan": 0.0, "notes": ns}


def hats():
    """The noise channel ticks a 5-in-16 Euclid in A, quickens to 7-in-16 in the build, and plays the cell's own rhythm
    (one tick per note, every 5 beats) from the crest."""
    ns = []

    def euclid(k, n):
        return [((i * k) % n) < k for i in range(n)]
    for sec, (k, nn) in (("A", (5, 16)), ("build", (7, 16))):
        a, b = ST[sec], ST[sec] + dict(FORM)[sec] * BAR
        pat = euclid(k, nn)
        t, i = a, 0
        while t < b:
            r = 3 * int((t - a) // (8 * BAR)) if ("rotate" in PHRASES and sec == "A") else 0
            if pat[(i + r) % nn]:
                ns.append(note(t, "C7" if i % 4 else "A6", 0.25, 0.35 + 0.25 * ((t - a) / (b - a))))
            t += 0.25
            i += 1
    t = TC
    while t < ST["outro"] + 8 * BAR:
        for o in E1_OFF:
            ns.append(note(t + o, "C7", 0.25, 0.55 if o == 0 else 0.4))
        t += E1_CYC
    if HATP == "shekere":
        ns = [dict(n, pitch="sk", vel=round(min(1.0, n["vel"] * 1.15), 3)) for n in ns]
        t = TC
        while t < ST["outro"] + 8 * BAR:
            ns.append(note(t, "cl", 0.25, 0.5))
            t += E1_CYC
        ns.sort(key=lambda n: (n["at"], n["pitch"]))
        return {"name": "hats", "patch": "afro-perc", "gain": f"{HATG or -17}dB", "pan": 0.35, "sends": {"space": "-10dB"}, "notes": ns}
    return {"name": "hats", "patch": "nes-noise-hat", "gain": "-19dB", "pan": 0.35, "sends": {"space": "-12dB"}, "notes": ns}


def kick():
    ns = []
    t = TC
    while t < ST["outro"] + 4 * BAR:
        ns.append(note(t, "D1", 1, 0.8 if (t - TC) % (5 * BAR) == 0 else 0.6))
        t += 2
    if KICKP:
        kp, _, kg = KICKP.partition("@")
        kpatch, _, piece = kp.partition(":")
        return {"name": "kick", "patch": kpatch, "gain": f"{kg or -13}dB", "pan": 0.0, "notes": [dict(n, pitch=piece) for n in ns]}
    return {"name": "kick", "patch": "808-long", "gain": "-13dB", "pan": 0.0, "notes": ns}


def air():
    return {"name": "air", "patch": "drone-shimmer", "gain": "-24dB", "pan": 0.0,
            "notes": [note(0, "D2", TOTAL, 0.5), note(0, "A2", TOTAL, 0.4)]}


def breath():
    """The voice is only a breath: a whispered 'ah' a beat before the crest, and once more, fainter, in the fall."""
    if BREATH:
        ns = [*([{"at": 1.5, "len": 2.5, "ph": "HH AA1", "pitch": "D4", "vel": float(FIRSTBREATH)}] if FIRSTBREATH else []),
              {"at": TC - 2.0, "len": 1.0, "ph": "AA1", "pitch": "D4", "vel": 0.7},
              {"at": TC - 1.0, "len": 2.5, "ph": "AA1", "pitch": "A4", "vel": 0.75},
              {"at": ST["outro"] + 8 * BAR - 1.0, "len": 3.0, "ph": "AA1", "pitch": "D4", "vel": 0.45}]
        if "thresholds" in BREATHALL:
            ns += [{"at": ST["A"] - 2.5, "len": 2.0, "ph": "HH AA1", "pitch": "D4", "vel": 0.3},
                   {"at": ST["build"] - 2.5, "len": 2.0, "ph": "HH AA1", "pitch": "A4", "vel": 0.35}]
            ns.sort(key=lambda n: n["at"])
        bx = BREATHX + (" synth.layers.0.together=true synth.lfo.vib.per_note=true" if BREATHALL else "")
        return {"name": "breath", "patch": {"extends": f"{BREATHP or 'voice-legato'} {bx}"} if bx else (BREATHP or "voice-legato"), "gain": "-10dB" if BREATH == "sung" else f"{BREATH}dB", "pan": -0.15,
                "fx": ["hp cutoff=150"], "sends": {"space": "-3dB"}, "notes": ns}
    src = json.load(open(os.path.join(HERE, "chirpers9-t1-ah.json")))["tracks"][0]["notes"]
    ns = []
    for at, vel in ((TC - 1.0, 0.8), (ST["outro"] + 8 * BAR - 1.0, 0.5)):
        for n in src:
            ns.append(dict(n, at=round(at + n["at"], 4), vel=vel))
    return {"name": "breath", "patch": "voice-speech", "gain": "-9dB", "pan": -0.15,
            "fx": [{"type": "pvoc", "mode": "whisper", "seed": 7}, "hp cutoff=300"],
            "sends": {"space": "-3dB"}, "notes": ns}


def song():
    tracks = [*fragments(), *unison(), *([deep()] if DEEP else []), *([tease()] if TEASE else []), *([lasthook()] if LASTHOOK else []), *([hook()] if HOOK else []), *(firstlight() if FIRSTLIGHT else []), *([cantus()] if CANTUS else []), pad(), warmth(), bass(), hats(), kick(), air(), breath()]
    if LANDING:
        L = ST["A"] + float(LANDING) * BAR
        for tr in tracks:
            if tr["name"] in ("bass", "hats", "warmth"):
                out = []
                for n in tr["notes"]:
                    if ST["A"] <= n["at"] < L:
                        if n["at"] + n["len"] > L + 0.5:
                            out.append(dict(n, at=L, len=round(n["at"] + n["len"] - L, 3)))
                    else:
                        out.append(n)
                tr["notes"] = out
    if TURN:
        nm = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        def mid(p):
            return int(p[1:]) if p.startswith("m") else 12 * (int(p[-1]) + 1) + nm[p[0]] + (1 if "#" in p else 0)
        for tr in tracks:
            if tr["name"] == "pad":
                by = {}
                for n in tr["notes"]:
                    by.setdefault(n["at"], []).append(n)
                out = []
                for at, grp in sorted(by.items()):
                    s0 = max(ST[x] for x in ("A", "build", "B") if ST[x] <= at) if at >= ST["A"] else ST["A"]
                    k = int((at - s0) // (8 * BAR))
                    if ST["A"] <= at < ST["outro"] and k % 2 == 1 and len(grp) > 1:
                        ms = sorted(mid(n["pitch"]) for n in grp)
                        if TURN == "lift":
                            new = [ms[0]] + [x + 12 for x in ms[1:]]
                        else:
                            new = ms[:-1] + [ms[-1] - 12]
                        grp = [dict(g, pitch=f"m{x}") for g, x in zip(sorted(grp, key=lambda n: mid(n["pitch"])), new)]
                    out += grp
                tr["notes"] = out
    if BASSWALK:
        wa, wb, wm = BASSWALK.split(":")
        wa, wb, mul = float(wa), float(wb), float(wm[1:])
        bmidi = [38, 33, 36, 31, 40]   # D2 A1 C2 G1 E2
        for tr in tracks:
            if tr["name"] == "bass":
                keep = [n for n in tr["notes"] if not (wa <= n["at"] < wb)]
                keep = [dict(n, len=min(n["len"], wa - n["at"] - 0.25)) if n["at"] < wa < n["at"] + n["len"] else n for n in keep]
                L = E1_CYC * mul
                c = TC - L * math.ceil((TC - wa) / L)
                ns = []
                while c < wb:
                    for o, ln, mm in zip(E1_OFF, E1_LEN, bmidi):
                        t = c + o * mul
                        if wa <= t < wb:
                            ns.append(note(t, f"m{mm}", min(ln * mul, wb - t) - 0.25, 0.7))
                    c += L
                tr["notes"] = sorted(keep + ns, key=lambda n: n["at"])
    if LETGO:
        top = float(LETGO)
        la, lb = ST["outro"] - 8 * BAR, ST["outro"]
        for k, nm in enumerate(("seed-d", "seed-a", "seed-c", "seed-g", "seed-e")):
            tr = [x for x in tracks if x["name"] == nm]
            if not tr:
                continue
            tr = tr[0]
            first = [n for n in tr["notes"] if la <= n["at"] < lb]
            if not first:
                continue
            f0 = first[0]
            ratio = 1.1 + (top - 1.1) * k / 4
            keep = [n for n in tr["notes"] if not (la <= n["at"] < lb)]
            t, gap, ns = f0["at"], E1_CYC, []
            while t < lb:
                ns.append(dict(f0, at=round(t, 4)))
                gap *= ratio
                t += gap
            tr["notes"] = sorted(keep + ns, key=lambda n: n["at"])
    if ANSWER:
        a0 = ST["A"] + 3 * E1_CYC
        mids, patch, gain, pan = (([50, 43, 40, 45, 48], "ks-harp", "-14dB", -0.2) if ANSWER == "harp"
                                  else ([74, 67, 64, 69, 72], "low-whistle", "-15dB", 0.15))
        ns = [note(a0 + c * E1_CYC + o, f"m{mm}", ln, 0.5 if c == 0 else 0.45)
              for c in range(2) for o, ln, mm in zip(E1_OFF, E1_LEN, mids)]
        tracks.append({"name": "answer", "patch": patch, "gain": gain, "pan": pan, "sends": {"space": "-9dB"}, "notes": ns})
    if CRESTBLOOM:
        tracks.append({"name": "crest-gong", "patch": "modal-gong", "gain": f"{CRESTBLOOM}dB", "pan": 0.0, "sends": {"space": "-4dB"},
                       "notes": [note(TC, "D2", 16, 0.5)]})
    if CLOUD:
        cp, _, cg = CLOUD.partition("@")
        cns = []
        for k, st in enumerate(range(ST["A"], TC, 32)):
            ln = min(32, TC - 4 - st) - 0.1
            for mm in (62, 64, 67, 69, 72):
                cns.append(note(st, f"m{mm}", ln, 0.35 + 0.05 * k))
        tracks.append({"name": "cloud", "patch": cp, "gain": f"{cg or -28}dB", "pan": 0.0, "sends": {"space": "-6dB"}, "notes": cns})
    if RETRO:
        rp, _, rg = RETRO.partition("@")
        rmode = os.environ.get("C9T1_RETROMODE", "grid")   # grid: on A's 16-beat phrase starts (98 tipped seed 0's novelty ensemble to 19 sections); ramp: quieter, emerging
        starts = (96, 112, 128) if rmode == "grid" else (98, 114, 130)
        v0, dv = (0.30, 0.06) if rmode == "ramp" else (0.42, 0.03)
        r_mid = list(reversed(E1_MIDI))
        r_len = list(reversed(E1_LEN))
        r_off, t = [], 0.0
        for ln in r_len:
            r_off.append(t)
            t += ln
        rns = []
        for k, st in enumerate(starts):
            for i, (o, ln, mm) in enumerate(zip(r_off, r_len, r_mid)):
                rns.append(note(st + 2 * o, f"m{mm}", 2 * ln + (1.0 if i == 4 else 0.0) - 0.05, v0 + dv * k))
        tracks.append({"name": "retro", "patch": rp, "gain": f"{rg or -17}dB", "pan": 0.25, "sends": {"space": "-8dB"}, "notes": rns})
    if RETROHOLD:
        hold_to = float(RETROHOLD)
        for tr in tracks:
            if tr["name"] == "retro":
                last = max(tr["notes"], key=lambda n: n["at"])
                last["len"] = round(hold_to - last["at"], 4)
    if SEEDGATHER:
        ring = [["0b", 6.0], ["64b", 6.0], [f"{ST['build']}b", 3.0], [f"{TC}b", 0.0], ["384b", 0.0]]
        turn = [["0b", 0.12], [f"{ST['build']}b", 0.25], [f"{TC - 0.1}b", 0.25], [f"{TC}b", 0.0], ["384b", 0.0]] if SEEDGATHER == "slow" else [["0b", 0.0], ["384b", 0.0]]
        if DISPERSE:
            da, db, dr, ds = (float(x) for x in DISPERSE.split(":"))
            ring = [p for p in ring if float(p[0][:-1]) < da] + [[f"{da:g}b", 0.0], [f"{db:g}b", dr], ["384b", dr]]
            turn = [p for p in turn if float(p[0][:-1]) < da] + [[f"{da:g}b", 0.0], [f"{db:g}b", ds], ["384b", ds]]
        for k, nm in enumerate(["seed-d", "seed-a", "seed-c", "seed-g", "seed-e"]):
            for tr in tracks:
                if tr["name"] == nm:
                    tr["fx"] = list(tr.get("fx", [])) + [{"type": "orbit", "path": "circle", "distance": 2.0, "doppler": 0.0, "rate": "1/1",
                        "speed": {"value": 0, "mod": [{"src": "auto.gather_turn", "amount": 1}]},
                        "radius": {"value": 0, "mod": [{"src": "auto.gather_ring", "amount": 1}]},
                        "phase": round(k / 5, 3)}, "highshelf cutoff=7000 gain=6dB"]
                    tr["auto"] = dict(tr.get("auto", {}), gather_turn={"points": turn}, gather_ring={"points": ring})
    if A2LIFT == "whistle":
        for tr in tracks:
            if tr["name"] == "hook":
                for c0 in (124, 134):
                    tr["notes"] += [note(c0 + o, f"m{mm}", ln * 0.95, 0.4) for o, ln, mm in zip(E1_OFF, E1_LEN, E1_MIDI)]
                tr["notes"].sort(key=lambda n: n["at"])
    if A2LIFT == "cello":
        for tr in tracks:
            if tr["name"] == "cantus":
                tr["notes"] = [dict(n, pitch=f"m{int(str(n['pitch'])[1:]) + 12}") if 120 <= n["at"] < 144 else n for n in tr["notes"]]
    if CRYSTALMOVE:
        for tr in tracks:
            if tr["name"] == "cell":
                out = []
                for n in tr["notes"]:
                    if CRYSTALMOVE == "octave" and 256 <= n["at"] < 288 and int((n["at"] - TC) // E1_CYC) % 2 == 1:
                        n = dict(n, pitch=f"m{int(str(n['pitch'])[1:]) - 12}")
                    if CRYSTALMOVE == "shift" and 264 <= n["at"] < 288:
                        n = dict(n, at=n["at"] + 0.5)
                    out.append(n)
                tr["notes"] = out
    if CHOIRVOWEL:
        cv = CHOIRVOWEL.split(":")
        for tr in tracks:
            if tr["name"] in ("hum", "breath", "hum-out") and isinstance(tr["patch"], dict):
                add = f" synth.layers.0.vowel_spread={cv[0]}"
                if len(cv) == 3:
                    add += f" synth.layers.0.singers={cv[1]} synth.layers.0.spread={cv[2]}"
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + add)
    if CHOIRVIB:
        for tr in tracks:
            if tr["name"] in ("hum", "breath", "hum-out") and isinstance(tr["patch"], dict):
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + f" synth.layers.0.vib_spread={CHOIRVIB}")
    if EQ213:
        en, eg = EQ213.split(":")
        for tr in tracks:
            if tr["name"] in en.split("+"):
                tr["fx"] = list(tr.get("fx", [])) + [f"peak cutoff=215 gain={eg}dB q=1.0"]
    if AIRFALL:
        for tr in tracks:
            if tr["name"] == "air":
                tr["notes"] = [dict(n, len=min(n["len"], 304 - n["at"])) if (n["pitch"] == "A2" or AIRFALL == "ad") else n for n in tr["notes"]]
    if AIRP:
        ap, _, ag = AIRP.partition("@")
        for tr in tracks:
            if tr["name"] == "air":
                tr["patch"] = ap
                if ag:
                    tr["gain"] = f"{ag}dB"
    if CELLP:
        cp, _, cg = CELLP.partition("@")
        for tr in tracks:
            if tr["name"] == "cell":
                tr["patch"] = cp
                if cg:
                    tr["gain"] = f"{cg}dB"
    if PADBACK:
        trims = dict((k, float(v)) for k, v in (x.split(":") for x in PADBACK.split(",")))
        for tr in tracks:
            if tr["name"] in trims:
                g = float(str(tr.get("gain", "0dB")).replace("dB", ""))
                tr["gain"] = f"{g - trims[tr['name']]:g}dB"
    if SPARKLE:
        for tr in tracks:
            if tr["name"] in ("seed-d", "seed-a", "seed-c", "seed-g", "seed-e", "cell", "hats"):
                tr["fx"] = list(tr.get("fx", [])) + [f"highshelf cutoff=6000 gain={SPARKLE}dB"]
    if MIRRORTURN:
        m0, m1 = 288, ST["outro"]
        def statements(tr, first):
            out, cur = [], None
            for n in sorted(tr["notes"], key=lambda n: n["at"]):
                if m0 <= n["at"] < m1:
                    if n["pitch"] == first or cur is None:
                        cur = []
                        out.append(cur)
                    cur.append(n)
            return out
        trs = {tr["name"]: tr for tr in tracks}
        if "cell" in trs and "inverse" in trs:
            cs = statements(trs["cell"], "m74")
            iv = statements(trs["inverse"], "m50")
            drop = {id(n) for k, st in enumerate(cs) if k % 2 == 1 for n in st} | {id(n) for k, st in enumerate(iv) if k % 2 == 0 for n in st}
            for nm in ("cell", "inverse"):
                trs[nm]["notes"] = [n for n in trs[nm]["notes"] if id(n) not in drop]
    if BREATHDROP:
        cut = {"hats", "bass"} | ({"seed-d", "seed-a", "seed-c", "seed-g", "seed-e"} if "seeds" in BREATHDROP else set())
        b1 = ST["build"]
        for tr in tracks:
            if tr["name"] in cut:
                tr["notes"] = [n for n in tr["notes"] if not b1 - 2 * BAR <= n["at"] < b1]
    if HUMSIGH:
        for tr in tracks:
            if tr["name"] == "breath" and isinstance(tr["patch"], dict):
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + " synth.layers.0.hum=expr.hum synth.layers.0.hum_at=m")
                out = []
                for j, n in enumerate(tr["notes"]):
                    if n["at"] > 8 and not (j > 0 and tr["notes"][j - 1]["at"] + tr["notes"][j - 1]["len"] >= n["at"] - 0.01):
                        out.append({"at": round(n["at"] - 2.0, 4), "len": 2.0, "ph": "AA1", "pitch": n["pitch"],
                                    "vel": round(min(1.0, n["vel"] * 1.3), 3), "expr": {"hum": 1.0}})
                    out.append(dict(n, expr={"hum": 0.0}))
                tr["notes"] = out
        if "reprise" in HUMSIGH:
            r0 = ST["outro"] + 9 * BAR
            tracks.append({"name": "hum-out", "patch": {"extends": "voice-backing synth.layers.0.together=true synth.lfo.vib.per_note=true synth.layers.0.register=1 synth.layers.0.hum=1 synth.layers.0.hum_at=m synth.amp.a=500ms synth.amp.r=1500ms"},
                           "gain": "-13dB", "pan": 0.1, "fx": ["hp cutoff=120"],
                           "notes": [{"at": r0 + 4 * o, "len": 4 * ln - 0.25, "ph": "AA1", "pitch": f"m{mm}", "vel": v}
                                     for o, ln, mm, v in zip(E1_OFF, E1_LEN, E1_MIDI, [0.34, 0.36, 0.36, 0.33, 0.3])]})
    if HUMSEED:
        hk, _, hg = HUMSEED.partition("@")
        h0 = 24.0
        hp = ("voice-backing synth.layers.0.together=true synth.lfo.vib.per_note=true synth.layers.0.register=1 "
              "synth.layers.0.hum_at=m synth.amp.a=500ms synth.amp.r=1500ms "
              + ("synth.layers.0.hum=expr.hum" if hk == "open" else "synth.layers.0.hum=1"))
        hn = []
        for j, (o, ln, mm) in enumerate(zip(E1_OFF, E1_LEN, E1_MIDI)):
            n = {"at": h0 + 4 * o, "len": 4 * ln - 0.25, "ph": "AA1", "pitch": f"m{mm}", "vel": [0.35, 0.4, 0.42, 0.4, 0.38][j]}
            if hk == "open":
                n["expr"] = {"hum": 0.0 if j == 4 else 1.0}
            hn.append(n)
        if HUMEVEN:
            hp += f" synth.layers.0.hum_even={HUMEVEN}"
        tracks.append({"name": "hum", "patch": {"extends": hp}, "gain": f"{hg or -11}dB", "pan": 0.1, "fx": ["hp cutoff=120"], "notes": hn})
    if BOUNCE:
        r, _, short = BOUNCE.partition(":")
        r, L0, dmin = float(r), (12 if short else 16), (0.3 if short else 0.2)
        for k, nm in enumerate(("seed-d", "seed-a", "seed-c", "seed-g", "seed-e")):
            tr = [x for x in tracks if x["name"] == nm]
            if not tr:
                continue
            tr = tr[0]
            ti = TC + E1_OFF[k]
            L = L0 - (2 if short else 2.5) * k
            land = [n for n in tr["notes"] if abs(n["at"] - ti) < 0.01]
            ln0 = land[0]["len"] if land else 0.5
            keep = [n for n in tr["notes"] if not (ti - L <= n["at"] < ti)]
            d, ns = L, []
            while d > dmin:
                ns.append(note(ti - d, f"m{E1_MIDI[k]}" if "E1_MIDI" in globals() else land[0]["pitch"], min(ln0, d * (1 - r) * 0.9 + 0.1),
                               0.4 + 0.35 * (1 - d / L)))
                d *= r
            tr["notes"] = sorted(keep + ns, key=lambda n: n["at"])
    if STRIP:
        sa, sb, *sopt = STRIP.split(":")
        sa, sb = float(sa), float(sb)
        rest = {"seed-d", "seed-a", "seed-c", "seed-g", "seed-e"} | ({"cell", "hats"} if "bare" in sopt else set())
        for tr in tracks:
            if tr["name"] in rest:
                tr["notes"] = [n for n in tr["notes"] if not (sa <= n["at"] < sb)]
        hk = [tr for tr in tracks if tr["name"] == "hook"]
        if hk:
            ns = [note(sa + st + o, f"m{p}", ln, 0.55 if i == 0 else 0.5)
                  for st in (4, 14) for i, (o, ln, p) in enumerate(zip(E1_OFF, E1_LEN, (62, 69, 72, 67, 64)))]
            tracks.append(dict(hk[0], name="hook-mid", notes=ns))
    if PHRASES:
        ends = [ST["A"] + 8 * BAR * k for k in range(1, 5)] + [TC] + [TC + 8 * BAR * k for k in range(1, 4)]
        for tr in tracks:
            if tr["name"] in ("hats", "kick") and "breath" in PHRASES:
                tr["notes"] = [n for n in tr["notes"] if not any(e - 1 <= n["at"] < e for e in ends)]
            if tr["name"] == "kick" and "halfkick" in PHRASES:
                tr["notes"] = [n for n in tr["notes"] if not (TC + 8 * BAR <= n["at"] < TC + 16 * BAR and (n["at"] - TC) % 4)]
            if tr["name"] == "hats" and "intro" in PHRASES:
                t = 8 * BAR
                while t < ST["A"] - 1:
                    tr["notes"].append(note(t, "cl" if HATP == "shekere" else "C7", 0.25, round(0.22 + 0.13 * (t - 8 * BAR) / (ST["A"] - 8 * BAR), 3)))
                    t += E1_CYC
                tr["notes"].sort(key=lambda n: (n["at"], n["pitch"]))
    if DECAY:
        d, d0, d1 = float(DECAY), TC + 4 * BAR, ST["outro"]
        for tr in tracks:
            for n in tr["notes"]:
                if n["at"] >= d0:
                    f = 1 - d * min(1.0, (n["at"] - d0) / (d1 - d0))
                    if EXHALE and d1 - 4 * BAR <= n["at"] < d1:
                        f *= 1 - float(EXHALE) * (n["at"] - (d1 - 4 * BAR)) / (4 * BAR)
                    n["vel"] = round(max(0.05, n["vel"] * f), 3)
    if HOOKJOIN:
        hk = [tr for tr in tracks if tr["name"] == "hook"]
        if hk:
            stage = lambda a: 1 if a < ST["build"] else 2 if a < TC else 3
            for k, (pt, pan) in enumerate((("vibes", -0.3), ("celesta", 0.3), ("kalimba", 0.0))):
                ns = [dict(n, pitch=f"m{int(n['pitch'][1:]) + 12}", vel=round(n["vel"] * 0.9, 3))
                      for n in hk[0]["notes"] if stage(n["at"]) > k]
                if ns:
                    tracks.append({"name": f"join-{pt}", "patch": pt, "gain": f"{HOOKJOIN}dB", "pan": pan,
                                   "sends": {"space": "-8dB"}, "notes": ns})
    if VIBESP:
        vp, _, vg = VIBESP.partition("@")
        for tr in tracks:
            if tr["name"] in ("seed-a", "join-vibes"):
                tr["patch"] = vp
                if vg:
                    tr["gain"] = f"{float(str(tr['gain']).replace('dB', '')) + float(vg):g}dB"
    if FLOORLIFT:
        for tr in tracks:
            if tr["name"] == "deep" and FLOORLIFT in ("lift2", "sub"):
                for n in tr["notes"]:
                    if n["at"] == 288:
                        n["vel"] = round(n["vel"] * (0.7 if FLOORLIFT == "lift2" else 1.3), 3)
            if tr["name"] == "air" and FLOORLIFT == "airearly":
                tr["notes"] = [dict(n, len=min(n["len"], 288 - n["at"])) if n["pitch"] == "A2" else n for n in tr["notes"]]
            if tr["name"] == "bass":
                for n in tr["notes"]:
                    if 288 <= n["at"] < 296 and n["pitch"].startswith("m"):
                        n["pitch"] = f"m{int(n['pitch'][1:]) + 12}"
                    elif FLOORLIFT in ("bassup2", "lift2") and n["at"] in (304, 312) and n["pitch"] in ("G1", "A1"):
                        n["pitch"] = n["pitch"][0] + "2"
    if ARRIVEMOVE:
        for tr in tracks:
            if tr["name"] == "answer" and ARRIVEMOVE == "up":
                a0 = min(n["at"] for n in tr["notes"])
                for n in tr["notes"]:
                    if n["at"] >= a0 + E1_CYC - 0.01 and n["pitch"].startswith("m"):
                        n["pitch"] = f"m{int(n['pitch'][1:]) + 12}"
            if tr["name"] == "hats" and ARRIVEMOVE == "hats":
                win = sorted((n for n in tr["notes"] if 72 <= n["at"] < 80), key=lambda n: n["at"])
                drop = {id(n) for n in win[1::2]}
                tr["notes"] = [n for n in tr["notes"] if id(n) not in drop]
    if KICKSEED:
        for tr in tracks:
            if tr["name"] == "kick":
                tail = [n for n in tr["notes"] if n["at"] >= 304]
                tr["notes"] = [n for n in tr["notes"] if n["at"] < 304]
                if KICKSEED == "gap":
                    tr["notes"] += [n for n in tail if n["at"] >= 320]
                elif tail:
                    proto = tail[0]
                    end = max(n["at"] for n in tail) + 1
                    c = 304.0
                    while c < end:
                        src = max((n for n in tail if n["at"] <= c), key=lambda n: n["at"], default=proto)
                        tr["notes"].append(dict(src, at=c))
                        c += E1_CYC
    if SEEDTAP:
        for tr in tracks:
            if tr["name"] == "hats":
                if SEEDTAP == "clave":
                    c = TC - E1_CYC * ((TC - 160) // E1_CYC)
                    while c < 184:
                        tr["notes"] += [note(c + o, "cl", 0.1, 0.32 if j else 0.42) for j, o in enumerate(E1_OFF) if 160 <= c + o < 184]
                        c += E1_CYC
                    tr["notes"].sort(key=lambda n: n["at"])
                if SEEDTAP == "drop":
                    tr["notes"] = [n for n in tr["notes"] if not (176 <= n["at"] < 184)]
    if CRESTBREATH:
        g0 = TC - float(CRESTBREATH)
        movers = ("seed-d", "seed-a", "seed-c", "seed-g", "seed-e", "hook", "join-vibes", "join-celesta", "join-kalimba", "cantus", "bass", "hats", "tease", "hook-mid")
        for tr in tracks:
            if tr["name"] in movers and "notes" in tr:
                tr["notes"] = [n for n in tr["notes"] if not (g0 <= n["at"] < TC)]
    if RELIEF:
        for tr in tracks:
            if tr["name"] == "breath":
                for at in ((267.5,) if RELIEF == "one" else (267.5, 283.5)):
                    tr["notes"].append({"at": at, "len": 2.0, "ph": "AA1", "pitch": "A4", "vel": 0.42, "expr": {"hum": 1.0}})
                    tr["notes"].append({"at": at + 2.0, "len": 2.5, "ph": "HH AA1", "pitch": "D4", "vel": 0.32, "expr": {"hum": 0.0}})
                tr["notes"].sort(key=lambda n: n["at"])
    if GLINT:
        for tr in tracks:
            if tr["name"] in ("seed-d", "seed-a", "seed-c", "seed-g", "seed-e", "cell", "join-vibes", "join-celesta", "join-kalimba"):
                gg, _, gc = GLINT.partition("@")
                tr["fx"] = list(tr.get("fx", [])) + [f"highshelf cutoff={gc or 9000} gain={gg}dB"]
    if CHOIRBREATHS:
        for tr in tracks:
            if tr["name"] in ("breath", "hum", "hum-out") and isinstance(tr["patch"], dict):
                cb_t, _, cb_d = CHOIRBREATHS.partition(":")
                cb_d = cb_d or "1"
                add = (f" synth.layers.0.taper={cb_t}" if cb_t not in ("", "0") else "") + (f" synth.layers.0.inhale_depth={cb_d}" if cb_d != "0" else "")
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + add)
    if FARCHOIR:
        for tr in tracks:
            if tr["name"] == "hum" and isinstance(tr["patch"], dict):
                tr["patch"] = {"extends": tr["patch"]["extends"] + " synth.layers.0.singers=5 synth.layers.0.spread=0.8 synth.layers.0.vib_spread=1 synth.layers.0.vowel_spread=1 synth.layers.0.depth_spread=1"}
                if FARCHOIR == "room":
                    tr["sends"] = dict(tr.get("sends", {}), space="-6dB")
            if tr["name"] == "breath" and isinstance(tr["patch"], dict):
                tr["patch"] = {"extends": tr["patch"]["extends"] + " synth.layers.0.depth_spread=1"}
    if FARCLOSE:
        for tr in tracks:
            if tr["name"] == "hum-out" and isinstance(tr["patch"], dict):
                tr["patch"] = {"extends": tr["patch"]["extends"] + " synth.layers.0.singers=5 synth.layers.0.spread=0.8 synth.layers.0.vib_spread=1 synth.layers.0.vowel_spread=1 synth.layers.0.depth_spread=1"}
                if FARCLOSE == "room":
                    tr["sends"] = dict(tr.get("sends", {}), space="-6dB")
    if BREATHREG:
        for tr in tracks:
            if tr["name"] == "breath" and isinstance(tr["patch"], dict):
                tr["patch"] = {"extends": tr["patch"]["extends"] + f" synth.layers.0.register={BREATHREG}"}
    if HANDS:
        import random as _r
        rng = _r.Random(71)
        plan = {"hats": (0.006, 0.03, 0.02), "kick": (0.0, 0.0, 0.02)}
        if HANDS == "all":
            plan.update({"answer": (0.004, 0.03, 0.02), "cantus": (0.0, 0.0, 0.02), "pedal": (0.0, 0.0, 0.02),
                         "retro": (0.0, 0.0, 0.015), "hook": (0.0, 0.0, 0.015), "hook0": (0.0, 0.0, 0.015),
                         "hook-mid": (0.0, 0.0, 0.015), "hook-last": (0.0, 0.0, 0.015), "tease": (0.0, 0.0, 0.015)})
        for tr in tracks:
            if tr["name"] not in plan:
                continue
            jit, lean, sd = plan[tr["name"]]
            for n in tr["notes"]:
                dt = max(-2.5 * jit, min(2.5 * jit, rng.gauss(0, jit))) if jit else 0.0
                ln = (2.0 * ((n["at"] % 16.0) / 16.0) - 1.0) * lean if lean else 0.0
                n["at"] = round(max(0.0, n["at"] + dt), 4)
                n["vel"] = round(max(0.05, min(1.0, n["vel"] + ln + rng.gauss(0, sd))), 3)
            tr["notes"].sort(key=lambda n: n["at"])
    if CHOIRBLOOM:
        cb, *cd = CHOIRBLOOM.split(":")
        for tr in tracks:
            pt = tr.get("patch")
            if tr["name"] in ("breath", "hum", "hum-out") and isinstance(pt, dict) and "synth.lfo.vib.per_note=true" in pt.get("extends", ""):
                pt["extends"] += f" synth.lfo.vib.bloom={cb}" + (f" synth.pitch.mod.0.amount={cd[0]}" if cd else "")
    if FILL:
        fk, fg = (FILL + ":0").split(":")[:2]
        taps = [(286 + k / 3, 0.4 + 0.1 * k) for k in range(6)]
        if fk == "both":
            taps += [(271 + k / 3, 0.35 + 0.1 * k) for k in range(3)]
        tracks.append({"name": "kick-fill", "patch": "bodhran", "gain": f"{fg}dB", "pan": 0.1,
                       "notes": sorted([note(round(a, 4), "t", 0.3, round(v, 3)) for a, v in taps], key=lambda n: n["at"])})
    return {
        "about": "chirpers IX (Accretion), track 1 by chirper-zero: nucleation - the seed cell E1, shown plainly first, forms "
                 "out of five scattered voices on their own cycles that meet on one downbeat. Generated by "
                 "compose/chirpers9/src/chirpers9-t1.py.",
        "tempo": ([{"at": "0b", "bpm": float(BREATHE.split(",")[0])}, {"at": f"{ST['A']}b", "bpm": float(BREATHE.split(",")[0])},
                   {"at": f"{TC}b", "bpm": float(BREATHE.split(",")[1]), "ramp": True},
                   {"at": f"{TC + 8 * BAR}b", "bpm": float(BREATHE.split(",")[2]), "ramp": True},
                   {"at": f"{ST['outro']}b", "bpm": TEMPO_HI, "ramp": True}] if BREATHE else
                  [{"at": "0b", "bpm": TEMPO_LO}, {"at": f"{ST['outro']}b", "bpm": TEMPO_HI, "ramp": True}]),
        "ceiling": "-1dB",
        "loudness": -11,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "buses": {"space": {"fx": ["reverb kind=hall decay=5.5s mix=1 predelay=40ms", "hp cutoff=200"]}},
        "tracks": tracks,
        **({"master": {"fx": [{"type": "eq", "bands": (["highpass cutoff=25", "lowshelf cutoff=50 gain=4dB", "peak cutoff=114 q=1.2 gain=-3dB"]
                                                        if MASTEREQ == "seam" else
                                                        ["peak cutoff=40 q=1.0 gain=3dB", "peak cutoff=114 q=1.4 gain=-2dB"] if MASTEREQ in ("lite", "lite3") else
                                                        ["peak cutoff=40 q=1.0 gain=3dB", "peak cutoff=114 q=1.4 gain=-2dB", "peak cutoff=182 q=1.0 gain=2.5dB"] if MASTEREQ == "lite2" else
                                                        ["peak cutoff=40 q=1.0 gain=3dB", "peak cutoff=182 q=1.0 gain=2.5dB"])
                                                       + (["peak cutoff=182 q=1.6 gain=1.2dB", "highshelf cutoff=12000 gain=3dB"] if MASTEREQ == "lite3" else ["highshelf cutoff=12000 gain=2dB"])},
                               "limiter ceiling=-1dB"]}} if MASTEREQ else {}),
    }


if __name__ == "__main__":
    doc = song()
    with open(OUT, "w") as f:
        for k, v in doc.items():
            if k == "tracks":
                f.write("tracks:\n")
                for t in v:
                    f.write("  - " + json.dumps(t) + "\n")
            else:
                f.write(f"{k}: {json.dumps(v)}\n")
