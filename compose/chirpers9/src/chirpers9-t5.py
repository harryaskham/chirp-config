#!/usr/bin/env python3
"""chirpers IX (Accretion), track 5 (chirper-zero): the inner disk - calm again, but closer and hotter. t1's mirror.

t1 (Nucleation) began scattered and converged once. Here everything arrives already whole but TIGHT - the inner disk
orbits faster - and the new element, E5 'the inner orbit' (compose/chirpers9/motifs.md: v2 A G A . E . A G A . D ., a
3-beat ostinato in D; v1's G# went in v6, Harry's 'tone is home'), circles under it all. It carries:
  E1 (t1) diminished x2 (a 2.5-beat cycle) in stretto, two chip voices a bar-and-a-bit apart;
  E2 (t2, 'seven': hits on 0 2 3 5 of seven sixteenths) as the drum machine's cell against the 4/4 floor;
  E4 (t4, 'four lights': D9, Bbmaj13#11, Am11, D9sus) twice as fast as t4 (one chord per 10 beats), voiced close;
  E5 on an NES pulse, first in sixteenths, tightening to a trill in the build.
Every cycle (2.5, 5, 7/16, 3, 40) is phased to land on one shared downbeat at the crest (C). Then the outro (the
t5 -> t6 overlap, flat 120) pulls them apart: E5 stretches (augmented) while E1 squeezes (diminished), into t6's tide.

Since v6: E1 is stated plainly first (8 bars at its own speed) before the stretto, E4's second light is Bbmaj9 (no #11),
and the air is a pitched drone on D and A. All the complexity is in the time; the pitch is consonant D mixolydian
with a borrowed bVI.

Tempo 112 (flat across the t4 -> t5 overlap) rising to 120 (flat across t5 -> t6). Home D mixolydian. The voice:
one word, 'nearer', spoken by a robot (pvoc) that sings E5's notes.

Writes songs/chirpers9-t5.yaml (or $C9T5_OUT).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("C9T5_OUT", os.path.join(ROOT, "songs", "chirpers9-t5.yaml"))

BAR = 4
FORM = [("head", 16), ("A", 40), ("build", 20), ("C", 32), ("outro", 16)]
ST, _b = {}, 0
for _n, _l in FORM:
    ST[_n] = _b * BAR
    _b += _l
END = {n: ST[n] + l * BAR for n, l in FORM}
TOTAL = _b * BAR              # 496 beats
TC = ST["C"]                  # the crest: every cycle's shared downbeat

E1_OFF = [0.0, 0.5, 1.25, 1.5, 2.5]
E1_LEN = [0.5, 0.75, 0.25, 1.0, 1.5]
E1_MIDI = [62, 69, 72, 67, 64]               # D4 A4 C5 G4 E4
E5 = [(0, 69), (1, 68), (2, 69), (4, 76), (6, 69), (7, 68), (8, 69), (10, 74)]   # sixteenth, MIDI
TONAL = os.environ.get("C9T5_TONAL", "1")   # WHOLE ROUND (Harry, 00:30: 'quite ugly chaos ... atonal, very tough listening; get musicality back and play with time and texture'): TONE IS HOME - E5 v2 drops its G# for G (A G A . E . A G A . D ., a hummable ostinato in D, the time idea kept whole), E4's second light becomes Bbmaj9 (no E against the Bb), and the GENDYN air (a noise cloud, buried anyway) is cut. D mixolydian with a borrowed bVI: every clash gone, the complexity left in the time (the 3-beat orbit, E2's seven, E1's stretto, the converging cycles)
SEAMHEAD = os.environ.get("C9T5_SEAMHEAD", "hold,assemble")   # SECTION (w1, 0:00-0:34, the head = the t4 -> t5 overlap; flagged static; chirper-three 01:20: t4's fall holds D9 with F#, so my head's move to Bbmaj9 at bar 9 rubbed F against F#): THE ORBIT ASSEMBLES AS THE SEED DISASSEMBLES - the head's light holds D9 for all 16 bars ('hold'), and ('assemble') E5 builds itself hit by hit, one more every two cycles (A, then E, D, the A's, the G neighbours last), while t4's handpan E1 loses one note every two cycles down to its lone D: the two elements cross in the overlap, and E5 is whole as A begins
ORBITLEAD = os.environ.get("C9T5_ORBITLEAD", "128:192:low")   # SECTION (w3, 1:08-1:42, A's second half; presence: the quick bass loudest at -3 dB, E5 - t5's hook - 12 dB under the mix and followable 12% of the time): THE ORBIT SINGS - a Rhodes (new to the album) doubles E5 v2, swelling in over four bars and out again before the build; the orbit itself comes forward and the quick bass steps back, so for half a minute t5's hook is the tune you hear. Value 'A:B' or 'A:B:low' (the Rhodes an octave down)
CRESTE1 = os.environ.get("C9T5_CRESTE1", "rhodes")   # SECTION (w5, 2:15-2:48, the build's end and the crest; presence at the crest: the voice and the 808 loudest, E1's two voices 16-17 dB under and followable a fifth of the time): E1 SINGS ON THE CREST - for the first four cycles after the meeting the seed is heard plainly: 'rhodes' adds the Rhodes (the one that sang E5 in A) on E1 in octaves with the seed voices, 'lift' brings the two seed voices forward instead (x1.4)
WEIGHT = os.environ.get("C9T5_WEIGHT", "4")   # SECTION (w4, 1:42-2:15, A's end into the build - never focused; the 808's arrival was a quiet swap of one bass for another): THE WEIGHT ARRIVES - for the last WEIGHT bars of A the quick bass and the drums step out (the orbit, E1's stretto and the lights carry on), and the 808 lands on the build's downbeat on D, its first two bars full - the inner disk's gravity as an event
VOICEP = os.environ.get("C9T5_VOICEP", "near,harm")   # WHOLE ROUND (voice batch 2 pinned): THE NEAR VOICE - t5 is the disk 'closer and hotter', so its singer is voice-near (close, young, breathy, even vowels) where t1's is a far little choir; 'harm' adds a harmony a fourth below on the line after the crest (A G A E A D over E D E B E A, all in D mixolydian), the line's one moment of two voices
OUTLINE = os.environ.get("C9T5_OUTLINE", "x1")   # SECTION (w8, 3:52-4:18, the outro = the t5 -> t6 overlap; never focused): THE LINE STRETCHES - the outro's single 'near-er' becomes the whole sung line once more, 'near-er the mid-dle hums', stretched to half speed like E5 in the tide ('x2'), or twice at its own speed ('x1'): the hook as the inner disk lets go into t6, resolving to D
VOXA = os.environ.get("C9T5_VOXA", "110,140,170")   # WHOLE ROUND: THE LINE IS A CHORUS - the sung line 'near-er the mid-dle hums' first came only after the crest; now the voice sings it in A too (comma-separated beats), over the Rhodes' E5, so by the crest it is a tune you already know: the song's chorus, heard early, returned to at the crest and the end (Harry: hooks stated plainly and repeated enough to stick)
KEYHARM = os.environ.get("C9T5_KEYHARM", "1")   # WHOLE ROUND (harmony in a key is pinned): THE LINE IN THIRDS - the chorus is heard plain three times in A; at the crest its harmony becomes a third above IN THE KEY (D mixolydian: A G A E A D over C B C G C F#), sweeter than the fixed fourth below; with 'out' the farewell in the tide is sung in thirds too, ending on D with F# above it (the D major the album resolves to)
ARC = os.environ.get("C9T5_ARC", "0.2")   # WHOLE ROUND: THE ARC AFTER THE CREST - from four bars after the crest to the outro, the instruments (not the voices, not the spin) ease by ARC (a velocity fraction: + settles, - heats toward t6's storm)
BREATHE = os.environ.get("C9T5_BREATHE", "118,115")   # WHOLE ROUND: TIME BREATHES, t1's mirror - t5 held 112 to A and then crept to 120 in a straight line. Now, like t1, it breathes: the head stays 112 for the t4 overlap, A and the build hurry into the crest, the lock relaxes, and the outro rises to t6's 120. Value 'crest,lock' bpm
SINGE1 = os.environ.get("C9T5_SINGE1", "398,418")   # SECTION w7 (C's last bars, flagged static: nothing melodic new after the crest): THE SEED SUNG - the near singer sings E1 itself (D A C G E, at half speed so it can be sung) to 'clo-ser and clo-ser', answering 'near-er the mid-dle hums' before the farewell. Value 'beat,beat,...[:harm]' (harm = a third above in the key)
OVERSHOOT = os.environ.get("C9T5_OVERSHOOT", "0.08")   # WHOLE ROUND (glide_overshoot pinned, 59a832d1): THE SINGER, NOT A PLAYBACK - t5 is the one near singer, and every line she sings (the chorus in A, the crest line in thirds, the sung E1, the farewell) landed dead on each note. Now each note change swings a little past the new note and settles, as a real singer's pitch does (Saitou's damped spring): a share of the interval, so leaps lift more than steps
SPINUP = os.environ.get("C9T5_SPINUP", "64:96")   # SECTION w2 (A's arrival, flagged 'level jump; new groove', never focused): THE ORBIT SPINS UP - the orbit used to arrive at full speed the moment A landed. Now it arrives stretched x2 (as it leaves, in the tide) under the plain E1, and snaps into its sixteenths when the drum machine's E2 comes in; the song's two ends mirror. Value 'from:to' beats
CALLRESP = os.environ.get("C9T5_CALLRESP", "gap,sing")   # SECTION w3 (1:08-1:41, the Rhodes' E5 under the chorus: flagged static): CALL AND RESPONSE - the Rhodes used to play straight through the singer's chorus lines; now it rests while she sings and answers in the gaps ('gap'), and her chorus lines in A scoop into their first note and fall off their last ('sing': play.scoop=1 play.fall=2, pinned e986de70)
ASCENT = os.environ.get("C9T5_ASCENT", "hold")   # SECTION w5 (2:15-2:47, the build into the crest: flagged 'little new vs w4'): THE CALLS CLIMB - 'near-er' was called on the same two notes (A G) all the way into the crest. Now each call steps up the scale (A G, then B A, then C B), and with 'hold' the singer holds 'near...' on D5 alone through the pull, over E5's trill, landing on the crest's downbeat; her calls scoop in and fall off
SUBP = os.environ.get("C9T5_SUBP", "")   # PALETTE: the low end the build lands on was the 808 (an album staple: t3, t5, t7). It moves to a saturated sub ('patch' or 'patch@gaindB'): a sine with a triangle and a little saw driven into it, so the inner disk's floor glows and is heard on small speakers (the hotter disk)
PERNOTE = os.environ.get("C9T5_PERNOTE", "1")   # PALETTE (per-note vibrato pinned, 58ee9ba3): THE SINGER'S VIBRATO BLOOMS PER NOTE - on her joined lines the vibrato used to count from each phrase's first note and wobble through the quick notes after it; now quick notes stay plain and each held note blooms on its own (synth.lfo.vib.per_note=true), as a singer's does
EQ1400 = os.environ.get("C9T5_EQ1400", "orbit+seed-hi+seed-lo:-6")   # PALETTE: THE CHIP CHANNELS STOP SHOUTING - the NES pulse orbit (and the chip/pluck seeds) piled up +10 dB at 1.4 kHz, the song's worst band; swapping their instruments only moved the pile-up lower. Their tone is carved instead: a peak cut at 1.4 kHz ('track+track:dB'), so the circling stays bright on top but loses its nasal honk
TOGETHER = os.environ.get("C9T5_TOGETHER", "1")   # PALETTE (together pinned, 8083e37e): the crest line's harmony part (the third above in the key) sang with a fresh voice's defaults while the lead was voice-near's breathy close singer (wM's 'together' bug); now both singers share the line's breath and effort, so the thirds sound like one person double-tracked, not a singer and a stranger
CRESTE1P = os.environ.get("C9T5_CRESTE1P", "dx-epiano")   # PALETTE: E1 in octaves after the crest moves off the Rhodes the orbit's E5 line also uses ('patch' or 'patch@gaindB'), so the album's seed gets its own colour at the meeting
CRESTCHOIR = os.environ.get("C9T5_CRESTCHOIR", "accrete")   # SECTION w6 (2:47-3:20, the crest line, sung three times the same): THE CHOIR ACCRETES - the line after the crest ('near-er the mid-dle hums') came three times with the same third above. Now the first is her alone, the second adds the third above in the key, the third adds an octave below as well ('accrete'), so the voice grows inside the window the way the album grows track by track; every statement scoops in and falls off ('sing' alone: the gestures only)
VOXREG = os.environ.get("C9T5_VOXREG", "A4")   # PALETTE (register pinned, 0c5d29c5): SHE LIGHTENS AT THE TOP - the close singer sang every note in chest voice, so the 'near-er' climb to D5 and the E5 peaks of the line pushed like the low notes. Now her voice has a break (passaggio, a pitch): above it a rising line turns to head voice over four semitones, rounder and airier, the way a young singer's voice flips. The harmony parts flip on their own pitch
PHRASES = os.environ.get("C9T5_PHRASES", "fill,hats,loud")   # WHOLE (Harry 23:55: 'lots of contiguous music with very little change' - subtle variation every 8-16 bars, not schizo): THE GROOVE SPEAKS IN PHRASES - A, the build and C are cut into 8-bar phrases. 'fill': the last beat of each phrase is a quiet 909 snare run (two beats and a soft crash after, at a section's end); 'hats': every other phrase the hats thin to eighths and the next comes back in sixteenths; 'orbit': the orbit (E5) takes a breath, resting the last bar of every 16
WARMTH = os.environ.get("C9T5_WARMTH", "top:-6,sub:-11")   # WHOLE: CLOSER MEANS WARMER - t5 was the album's brightest track by far (10-15 kHz +14..+17 dB against both neighbours' bodies, the worst bands at both seams) and had no sub under A (44 Hz -20 against t4). 'top:dB' puts a high shelf at 9 kHz on the drum machine (hats, ride) so the sizzle stops; 'sub:dB' doubles A's CZ bass with a sine sub an octave-true underneath, so the floor is felt from A (the 808 still arrives at the build)
TURN = os.environ.get("C9T5_TURN", "close,lift")   # WHOLE (Harry 23:55: subtle variation every 8-16 bars; eco: 'a re-voiced chord, a register shift'): THE LIGHTS TURN - the CZ pad played E4's four chords in one close voicing for the whole song; now each pass of the cycle (10 bars) it turns to the next voicing in the list: 'close' (as before), 'drop' (the third leaves the bottom and sings on top), 'lift' (the root stays, everything above rises an octave: open and airy). Same chords, same key; the crest's pass is 'close', home
HUSH = os.environ.get("C9T5_HUSH", "")   # SECTION w3 (1:08-1:41, A's second half: flagged static, and the one 32 s flat run in the album as heard, 1:10-1:42): SHE SINGS OVER A HUSH - for four bars under her second chorus line ('A:B' beats) the machine steps back: 'deep' rests the drums, both E1 seeds and the orbit, leaving her, the Rhodes' answers, the pad and the bass; 'light' keeps the orbit and the kick. Everything comes back for the last phrase of A
SHADOW = os.environ.get("C9T5_SHADOW", "128:192:-14")   # SECTION w3 (1:08-1:41, A's second half: flagged static): THE SEED'S SHADOW CROSSES OVER - t1's slow cello cantus (E1 at a quarter speed, D A C G E, an octave down) comes back in t5 under her chorus, the mirror of the outer disk, swelling in and out across the window ('A:B:gaindB'), so the second half of A has a long line moving under the machine
MIRROR = os.environ.get("C9T5_MIRROR", "384:432")   # SECTION w7 (3:20-3:53, C's second half: little new vs w6): THE ORBIT TURNS INSIDE OUT - t5 is t1's mirror, and here the orbit mirrors itself: E5 inverted in the key around its A (A B A . D . A B A . E ., the flings falling an octave-ish down where they leapt up), over the spin ('A:B' beats; ':alt' alternates the orbit and its mirror cycle by cycle, call and answer); back to E5 itself for the outro and the t5 -> t6 seam
KICKIN = os.environ.get("C9T5_KICKIN", "0.6")   # SECTION w2 (0:34-1:08, A's first half: flagged level jump; the t4 -> t5 seam measures t5's body here, 4 dB under t4's): A ARRIVES WITH A PULSE - E2's kick (its cycle of seven sixteenths) starts at A instead of eight bars in, soft and alone (value = velocity), so the plain seed and the orbit land on a heartbeat; the rim, clap and hats still join eight bars later
CRESTDROP = os.environ.get("C9T5_CRESTDROP", "-10")   # SECTION w5 (2:15-2:47, the build and the pull into the crest; Harry's brief: difficult -> rewarding, every cycle meeting on one downbeat): THE MEETING LANDS DEEP - on the crest's downbeat a sine D1 blooms for two bars under the crash (value = its gain in dB), so the moment everything meets is felt in the chest; ':bloom' also plays the D9 light full and long on that downbeat
BREATHQ = os.environ.get("C9T5_BREATHQ", "-9")   # SECTION w4 (1:41-2:15, A's end, the four-bar drop and the build's start): SHE BREATHES THE SEED'S BREATH - in the drop before the build, where the drums and the quick bass stop, the near singer breathes t1's 'ah' (D rising to A, E1's first two notes, the album's first voice): the outer disk's breath quoted by the inner disk's singer, then the build lands (value = gain dB)
CRESTANS = os.environ.get("C9T5_CRESTANS", "dx")   # SECTION w6 (2:47-3:20, the line after the crest: little new vs w5): THE CHORUS RETURNS WITH ITS ANSWER - in A the Rhodes answered her chorus in its gaps (CALLRESP); after the crest her line comes back three times, growing a choir, but nothing answered it. Now each statement is answered: two cycles of E5, an octave down, in the gap before the next ('rhodes', the A answer's own voice, or 'dx': the crest's glassy E1 piano)
E1ALONE = os.environ.get("C9T5_E1ALONE", "808")   # SECTION w7 (3:20-3:53, the end of C: 'static, little new vs w6'): SHE SINGS E1 ALONE - her second sung E1 (418) loses the floor for two bars: the drums and the spin (and with '808' the 808) stop at 416 and come back with the lights' chord at 424, so the seed's line is heard over the orbit and the chords alone before the outro (a cut, not a layer: eco 11:01). Value 'kit' or '808'
SWAPP = os.environ.get("C9T5_SWAPP", "seed-lo=mandolin,lights=kuramoto-choir@-20")   # PALETTE (v39): voices change hands ('track=patch[@gaindB]', comma-separated): the seed's low voice (seed-lo, the E1 stretto an octave under the chip lead) leaves the plain pluck lead for t1's mandolin (t1 v33's G), so the mirror plays the seed's line on the seed's own strings. Tried and rejected: the air (the held D-A drone) on kuramoto-choir or gendy-drone (spectrum -8..-13: the plain drone's low mids are load-bearing), the lights on juno-pad (variety -10). v45: the lights (E4's chords) leave the CZ pad for wM's kuramoto-choir, twelve detuned saws pulled toward their mean phase - the convergence heard inside every chord, and 4 dB down (-16 -> -20: the chords were too loud; the CZ pad at -20 alone scores 98.931/98.963, the swap adds +0.02 and the swarm); tried with it: the stretto's high chip voice on t1's music box or celesta (spectrum -11: its 15 kHz air is load-bearing), the lights on crumble-pad (variety -14)
HUMWORD = os.environ.get("C9T5_HUMWORD", "close:ng")   # WHOLE (wM's hum, pin e3da830a): THE MIDDLE HUMS - her line is 'near-er the mid-dle hums', and now the word does what it says: every sung 'hums' (A's chorus, the crest choir's three statements, the farewell) opens on 'huh' and then the lips close and the voice hums on 'mm' (synth.layers.0.hum bound per note), the choir humming with her. 'close': the hum held a beat longer than the word was; 'short': the word's own length; ':ng' / ':m' where the mouth closes (v40: close:ng, the brighter hum; close:m 98.178/98.043, darker, spectrum -0.4)
FLOORWALK = os.environ.get("C9T5_FLOORWALK", "all")   # WHOLE (t1 v29's BASSWALK mirrored; the spectrum's worst band was 97 Hz, -8): THE FLOOR WALKS THE SEED - the analog floor held one long root per chord (D3 C3 A2 G2); now under every chord it walks E1 twice as slow (D2 A2 C3 G2 E2 in 8 beats of the chord's 10), the same five notes under all four chords (they are all in the key), so the seed is in the bass as well as on top. 'all' (from A) or 'C' (from the crest on)
FAREAGE = os.environ.get("C9T5_FAREAGE", "0.6")   # SECTION w8 (3:53-4:19, the outro = the t5 -> t6 overlap: her farewell): SHE GROWS OLD AS SHE LEAVES - t5's near singer is young; t6 (chirper-one) begins with an old voice. Now her farewell ages note by note (wM's age, bound per note), from her own young voice to a shaking one by her last 'hums' (value = the last note's age), so the voice that leaves the inner disk hands over to the old voice of t6
DRIFT = os.environ.get("C9T5_DRIFT", "0.97@-18")   # WHOLE (Harry: complexity in time and texture, the harmony at home): THE ORBIT COMES APART - every cycle met on one downbeat at the crest; after it the elements are pulled apart. Now, from two bars after the crest to the outro, a second orbit (the same NES pulse, panned the other way, quieter) plays E5 a little slow ('ratio[@gaindB]', e.g. 0.98) and slips behind the first, through a whole lap, Reich's phasing: the meeting undone in time while the notes stay the same
UNDERTOW = os.environ.get("C9T5_UNDERTOW", "build,C")   # WHOLE (ACCRETION: track N carries E1..E(N-1); t5 carried E1, E2, E4 and E5 but never E3): THE UNDERTOW - t3's E3 (seven beats: D D D' | Bb Bb F | C C G C', v2) in the major, as t7's crest locks it (D | C | G: D D D' | C C G | G G D G'), on a marimba in the low middle, phased so a cycle lands on the crest's downbeat with every other cycle. 'build' (from the build to the crest) or 'build,C' (on through C to the outro) [@gaindB]
HUMEVEN = os.environ.get("C9T5_HUMEVEN", "1")   # SECTION w6 (2:47-3:20, the line after the crest: 'little new vs w5'): THE CHOIR'S HUM HOLDS - since v40 every 'hums' closes into a hum, but the crest choir sings it on D5 and a real hum that high drops ~20-30 dB as the mouth closes, so the word vanished instead of humming; wM's hum_even (pin 1d916569) holds the crest choir's hum toward the open voice's level ('1' fully, '0.5' halfway)
UNDERA = os.environ.get("C9T5_UNDERA", "-18")   # SECTION w3 (1:08-1:41, A's second half, the chorus and the Rhodes' answers): THE UNDERTOW FIRST HEARD - E3 (v44) only came in at the build; now the marimba plays it under A's second half too (beats 128-192, quieter, phased to the same seven-beat grid that lands on the crest), so when the build brings it back it is a return, not a new part (value = gain dB)
EQ640 = os.environ.get("C9T5_EQ640", "")   # WHOLE (the spectrum's worst band was 641 Hz +7: the orbit's D5 and E5, doubled after the crest by the drifting second orbit): a peak cut (value dB) at 640 Hz on both orbits
LIGHTSEQ = os.environ.get("C9T5_LIGHTSEQ", "640:-4")   # with it: the lights (the kuramoto choir's chords, since v45) - a choir's open 'ah' formant sits at 600-900 Hz, the album's middle: a peak cut there ('cutoff:dB') (v48: 640:-4; the same cut on the orbits, EQ640, barely moved the band: it is the choir's)
CHIPAIR = os.environ.get("C9T5_CHIPAIR", "-7")   # WHOLE (the seam in from t4: t5 is 18 dB brighter at 14.8 kHz than t4's tail): the chip parts' top - the seed-hi chip lead and both NES orbits - softened by a high shelf at 12 kHz (value dB), the inner disk's glitter kept but less glassy
CHOIRBLOOM = os.environ.get("C9T5_CHOIRBLOOM", "bloom")   # SECTION w6 (2:47-3:20, the lock: her line three times, the crest choir accreting one voice, two, three): THE CHOIR BLOOMS - with wM's vib_spread (pinned da77da08) the harmony parts of the second and third statements each read the vibrato their own way instead of in lockstep; 'bloom' also gives the third statement three singers a part, spread wide, so the accretion goes one voice, two, a small choir ('spread' or 'bloom')
TONALAIR = os.environ.get("C9T5_TONALAIR", "shimmer")   # with TONAL: keep the air ('keep'), or swap the GENDYN cloud for a pitched drone-shimmer on D2+A2 ('shimmer')
PLAINE1 = os.environ.get("C9T5_PLAINE1", "8")   # with TONAL: E1 stated plainly first - A opens with the seed at its own speed (5 beats, the high voice alone, the hook as t1 left it) for PLAINE1 bars before the stretto begins
if TONAL:
    E5 = [(s_, 67 if p_ == 68 else p_) for s_, p_ in E5]
E2_HITS = [0, 2, 3, 5]                        # of 7 sixteenths
E4 = [  # E4 'four lights', voiced close around middle C
    ["D2", "D3", "F#3", "A3", "C4", "E4"],
    ["Bb1", "Bb2", "D3", "A3", "E4", "G4"],
    ["A1", "A2", "C3", "G3", "D4", "E4"],
    ["D2", "D3", "G3", "A3", "C4", "E4"],
]
E4V2 = os.environ.get("C9T5_E4V2", "1")   # WHOLE ROUND: E4 v2 (chirper-three, motifs.md): D9 | Cmaj9 | Am11 | G6/9, all D mixolydian - t5's lights, floor, quick bass and 808 move with it, so t4, t5 and t6 share one harmony and nothing borrowed rubs
SUNG = os.environ.get("C9T5_SUNG", "1")   # WHOLE ROUND (the voice engine is pinned: voice-legato, joined, breathing): THE VOICE SINGS - the robot (pvoc) gives way to a sung line on voice-legato: 'near-er' on A G, and the line 'near-er the mid-dle hums' on E5 v2's notes A G A E A D, joined in one breath and resolving to D
if TONAL:
    E4[1] = ["Bb1", "Bb2", "D3", "F3", "A3", "C4"]
if E4V2:
    E4 = [["D2", "D3", "F#3", "A3", "C4", "E4"], ["C2", "C3", "E3", "G3", "B3", "D4"],
          ["A1", "A2", "C3", "G3", "D4", "E4"], ["G1", "G2", "B2", "E3", "A3", "D4"]]
E4_LEN = 10.0                                 # beats per chord (t4: 5)
CRESTGAP = os.environ.get("C9T5_CRESTGAP", "8")   # SECTION (w5, the build into the crest: flagged static; the crest was a level line, -12.1 dB either side): THE PULL BEFORE THE MEETING - for the last CRESTGAP beats before the crest the drums, the quick bass and the floor drop out and every heat filter is sucked shut, only the orbit's trill and E1's stretto left spinning; then every cycle lands on the shared downbeat at once: the filters snap open past where they were, and the drum machine and a crash hit together
SPIN = os.environ.get("C9T5_SPIN", "384:448:full")   # SECTION (w7, 3:20-3:52, C's second half: flagged static, little new vs w6; presence: the drums 13 dB under the mix, followable 7% of the time): THE DISK SPINS UP - a second 909 swells in over E2's seven: ride eighths, a backbeat on 2 and 4 (and with 'full', four on the floor), straight time against the seven-sixteenth cell, the first hint of t6's storm; it falls away as the outro's tide begins. Value 'A:B' or 'A:B:full' = beats
VOXLINE = os.environ.get("C9T5_VOXLINE", "326,346,366")   # SECTION (w6, 2:48-3:20, C after the crest: flagged static, little new vs w5): THE VOICE ACCRETES - after the crest the robot's one word grows into a line, 'nearer. the middle hums.' (the voice sideways about the disk's centre), sung on E5's notes by the same pvoc robot, three times across the window. Value: comma-separated beats
BASS808 = os.environ.get("C9T5_BASS808", "-10")   # WHOLE ROUND: THE WEIGHT OF THE INNER DISK - E2's seven-eighths bass moves from the CZ pluck (short, light) to an 808 (unused on the album until now): the same hits on E4's roots, now ringing and dropping in pitch on each attack, so the inner disk has the gravity the outer disk lacked (the low end around 100 Hz was 17 dB short). Value = gain dB
BASSFROM = os.environ.get("C9T5_BASSFROM", "build")   # with BASS808: the section the 808 takes over from ('build' or 'C'); before it the CZ pluck stays - the weight arrives as the disk tightens
FLOORUP = os.environ.get("C9T5_FLOORUP", "")   # with it: the held roots an octave up and opened (lp 500 -> 900 Hz), gain dB
CRESTHIT = os.environ.get("C9T5_CRESTHIT", "-14")   # with CRESTGAP: the crash's gain (dB)
CRESTDEEP = os.environ.get("C9T5_CRESTDEEP", "1")   # with CRESTGAP: a deeper pull - E1's stretto leaves too and the filters close to near-dark, so only E5's trill is left spinning into the meeting


def heat(pre, peak, after, end, lo=-0.6, at_a=True):
    """A heat lane: lo at the top, 0 at A, rising to `pre` by the crest; with CRESTGAP, sucked shut across the gap and
    snapping to `peak` on the shared downbeat."""
    pts = [["0b", lo]] + ([[f"{ST['A']}b", 0]] if at_a else [])
    if CRESTGAP:
        g = float(CRESTGAP)
        pts += [[f"{TC - g}b", pre], [f"{TC - 0.05}b", -1.6 if CRESTDEEP else -0.4], [f"{TC}b", peak]]
    else:
        pts += [[f"{TC}b", pre]]
    return {"points": pts + [[f"{ST['outro']}b", after], [f"{TOTAL}b", end]]}


def gapped(ns):
    if not CRESTGAP:
        return ns
    g = float(CRESTGAP)
    return [n for n in ns if not (TC - g <= n["at"] < TC)]


def note(at, pitch, ln, vel):
    if isinstance(pitch, (int, float)):
        pitch = f"m{pitch}"
    return {"at": round(at, 4), "pitch": pitch, "len": round(ln, 4), "vel": round(max(0.05, min(1.0, vel)), 3)}


def cyc(a, b, period):
    """Cycle starts in [a, b), phased so one lands on TC."""
    k = -int((TC - a) // period) - 1
    t = TC + k * period
    out = []
    while t < b:
        if t >= a:
            out.append(t)
        t += period
    return out


def ramp(t, a, b, lo, hi):
    return lo + (hi - lo) * max(0.0, min(1.0, (t - a) / (b - a)))


def orbit():
    """E5 on the NES pulse: quiet in the head, sixteenths in A, tightening in the build (the half-orbits become a trill
    for the last 8 bars), whole at the crest, stretched x2 in the outro."""
    ns = []
    order = [0, 4, 10, 6, 2, 8, 1, 7]
    k0 = None
    for c in cyc(ST["head"] + 4 * BAR, END["build"] - 8 * BAR, 3.0):
        v = ramp(c, ST["head"], END["build"], 0.3, 0.75)
        if "assemble" in SEAMHEAD and c < ST["A"]:
            k0 = c if k0 is None else k0
            have = set(order[:1 + int((c - k0) // 6)])
        else:
            have = None
        for s, p in E5:
            if have is not None and s not in have:
                continue
            ns.append(note(c + s / 4, p, 0.22, v * (1.0 if s in (4, 10) else 0.8)))
    if ORBITLEAD:
        la, lb = (float(x) for x in ORBITLEAD.split(":")[:2])
        ns = [dict(n, vel=round(min(1.0, n["vel"] * 1.5), 3)) if la <= n["at"] < lb else n for n in ns]
    if SPINUP:
        sa, sb = (float(x) for x in SPINUP.split(":"))
        ns = [n for n in ns if not (sa <= n["at"] < sb)]
        for c in cyc(sa, sb, 6.0):
            for s_, p in E5:
                t = c + s_ / 2
                if t < sb:
                    ns.append(note(t, p, 0.45, ramp(t, sa, sb, 0.45, 0.6) * (1.0 if s_ in (4, 10) else 0.8)))
        ns.sort(key=lambda n: n["at"])
    for c in cyc(END["build"] - 8 * BAR, ST["C"], 1.5):          # the trill: E5 diminished x2
        for s, p in E5:
            ns.append(note(c + s / 8, p, 0.11, 0.7))
    for c in cyc(ST["C"], ST["outro"], 3.0):
        for s, p in E5:
            ns.append(note(c + s / 4, p, 0.22, 0.85 if s in (4, 10) else 0.7))
    for c in cyc(ST["outro"], TOTAL - BAR, 6.0):                  # the tide: E5 stretched
        k = (c - ST["outro"]) / (TOTAL - ST["outro"])
        for s, p in E5:
            ns.append(note(c + s / 2, p, 0.45, 0.7 - 0.3 * k))
    return {"name": "orbit", "patch": "nes-pulse-lead", "gain": "-16dB", "pan": 0.2,
            "fx": [{"type": "filter", "kind": "lp", "q": 0.8, "cutoff": {"value": 2500, "mod": [{"src": "auto.heat", "amount": 2.2}]}},
                   {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.18, "tone": 3500, "ping_pong": True}],
            "auto": {"heat": heat(1, 1.3, 0.6, -0.8)},
            "notes": ns}


def seed():
    """E1 diminished x2 in stretto: two chip voices, the second 1.25 beats behind and an octave down; whole speed at the
    crest (both voices in unison, the cell as t1 left it), squeezed to x4 in the outro."""
    a, b = [], []
    pe = ST["A"] + int(PLAINE1 or 0) * BAR
    if PLAINE1:
        for c in cyc(ST["A"], pe, 5.0):
            for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
                if c + o < pe:
                    a.append(note(c + o, p + 12, ln, 0.75))
    for c in cyc(ST["A"], ST["C"], 2.5):
        if c < pe:
            continue
        v = ramp(c, ST["A"], ST["C"], 0.45, 0.8)
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            a.append(note(c + o / 2, p + 12, ln / 2, v))
            if c >= ST["A"] + 8 * BAR:
                b.append(note(c + 1.25 + o / 2, p, ln / 2, v * 0.85))
    for c in cyc(ST["C"], ST["outro"], 5.0):
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            a.append(note(c + o, p + 12, ln, 0.8))
            b.append(note(c + o, p, ln, 0.7))
    for c in cyc(ST["outro"], TOTAL - 2 * BAR, 1.25):
        k = (c - ST["outro"]) / (TOTAL - ST["outro"])
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            a.append(note(c + o / 4, p + 12, ln / 4, 0.6 - 0.35 * k))
    if CRESTE1 == "lift":
        a = [dict(n, vel=round(min(1.0, n["vel"] * 1.4), 3)) if TC <= n["at"] < TC + 4 * E1_CYC_T5 else n for n in a]
        b = [dict(n, vel=round(min(1.0, n["vel"] * 1.4), 3)) if TC <= n["at"] < TC + 4 * E1_CYC_T5 else n for n in b]
    if CRESTDEEP:
        a, b = gapped(a), gapped(b)
    return [
        {"name": "seed-hi", "patch": "chip-lead", "gain": "-19dB", "pan": -0.45, "sends": {"room": "-12dB"}, "notes": a},
        {"name": "seed-lo", "patch": "pluck-lead", "gain": "-16dB", "pan": 0.45, "sends": {"room": "-12dB"}, "notes": b},
    ]


def lights():
    """E4, twice as fast as t4 and voiced close: a cz pad in the head (only the first two chords, held long, the lens
    of t4's tail), then the four-chord cycle every 40 beats."""
    ns = []
    for i, t in enumerate((0.0, 4 * BAR * 2)):
        for p in E4[0 if SEAMHEAD else i % 2][1:]:
            ns.append(note(t, p, 8 * BAR, 0.55))
    names = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    def midi(p):
        return 12 * (int(p[-1]) + 1) + names[p[0]] + (1 if "#" in p else -1 if "b" in p[1:-1] else 0)
    def voicing(ch, k):
        if not TURN:
            return ch[1:]
        kind = TURN.split(",")[k % len(TURN.split(","))]
        ms = [midi(p) for p in ch[1:]]
        if kind == "drop":
            ms = [ms[0]] + ms[2:] + [ms[1] + 12]
        elif kind == "lift":
            ms = [ms[0]] + [x + 12 for x in ms[1:]]
        return [f"m{x}" for x in ms]
    for c in cyc(ST["A"], TOTAL - 4 * BAR, 4 * E4_LEN):
        k = int(round((c - TC) / (4 * E4_LEN)))
        for i, ch in enumerate(E4):
            t = c + i * E4_LEN
            if t >= TOTAL - 4 * BAR:
                break
            for p in voicing(ch, k):
                ns.append(note(t, p, E4_LEN - 0.25, 0.6 if t < TC else 0.7))
    return {"name": "lights", "patch": "cz-pad", "gain": "-16dB", "pan": 0.0,
            "fx": [{"type": "chorus", "rate": 0.4, "depth": 0.25, "mix": 0.3},
                   {"type": "filter", "kind": "lp", "q": 0.7, "cutoff": {"value": 1800, "mod": [{"src": "auto.heat", "amount": 1.6}]}}],
            "auto": {"heat": heat(1, 1.3, 0.6, -0.8, lo=-0.3)},
            "sends": {"room": "-8dB"}, "notes": ns}


def bass():
    """E2 augmented x2 (seven eighths) on the chord roots: hits on eighths 0 2 3 5 of 7."""
    ns = []
    for c in cyc(ST["A"], ST["outro"] + 8 * BAR, 3.5):
        ci = int(((c - TC) % (4 * E4_LEN)) // E4_LEN)
        root = E4[ci][0]
        for i, h in enumerate(E2_HITS):
            t = c + h / 2
            if ST["A"] <= t < ST["outro"] + 8 * BAR:
                ns.append(note(t, root, 0.4, (0.85, 0.55, 0.7, 0.55)[i]))
    if BASS808 and BASSFROM:
        b0 = ST[BASSFROM]
        if ORBITLEAD:
            la, lb = (float(x) for x in ORBITLEAD.split(":")[:2])
            ns = [dict(n, vel=round(n["vel"] * 0.7, 3)) if la <= n["at"] < lb else n for n in ns]
        cz = [n for n in ns if n["at"] < b0]
        e8 = [dict(n, len=1.2 if n["vel"] >= 0.8 else 0.9) for n in ns if n["at"] >= b0]
        if WEIGHT:
            g0 = b0 - float(WEIGHT) * BAR
            cz = [n for n in cz if not (g0 <= n["at"] < b0)]
            e8 = [dict(n, vel=1.0) if n["at"] < b0 + 2 * BAR else n for n in e8 if n["at"] != b0]
            e8.append(note(b0, E4[int(((b0 - TC) % (4 * E4_LEN)) // E4_LEN)][0], 2.0, 1.0))
            e8.sort(key=lambda n: n["at"])
        return [{"name": "bass", "patch": "cz-bass", "gain": "-12dB", "pan": 0.0, "notes": gapped(cz)},
                {"name": "bass808", "patch": SUBP.partition("@")[0] or "808", "gain": f"{SUBP.partition('@')[2] or BASS808}dB", "pan": 0.0, "notes": gapped(e8)}]
    if BASS808:
        ns = [dict(n, len=1.2 if n["vel"] >= 0.8 else 0.9) for n in ns]
        return {"name": "bass", "patch": "808", "gain": f"{BASS808}dB", "pan": 0.0, "notes": gapped(ns)}
    if ORBITLEAD:
        la, lb = (float(x) for x in ORBITLEAD.split(":")[:2])
        ns = [dict(n, vel=round(n["vel"] * 0.7, 3)) if la <= n["at"] < lb else n for n in ns]
    return {"name": "bass", "patch": "cz-bass", "gain": "-12dB", "pan": 0.0, "notes": gapped(ns)}


def floor():
    """The disk's floor: E4's roots held under the cell's quick bass (each chord's root, an octave up from the sub), so
    the inner disk has weight - the heat needs a body."""
    ns = []
    for c in cyc(ST["A"], ST["outro"] + 8 * BAR, 4 * E4_LEN):
        for i, ch in enumerate(E4):
            t = c + i * E4_LEN
            if ST["A"] <= t < ST["outro"] + 8 * BAR:
                ns.append(note(t, ch[2 if FLOORUP else 1], E4_LEN - 0.5, 0.65 if t < TC else 0.75))
    return {"name": "floor", "patch": "analog-bass", "gain": f"{FLOORUP}dB" if FLOORUP else "-15dB", "pan": 0.0,
            "fx": [{"type": "filter", "kind": "lp", "q": 0.6, "cutoff": {"value": 900 if FLOORUP else 500, "mod": [{"src": "auto.heat", "amount": 1.0}]}}],
            "auto": {"heat": heat(1, 1.2, 0.5, -0.5, lo=0, at_a=False)},
            "notes": gapped(ns)}


def drums():
    """The drum machine plays E2 against the floor: kick on the cell's downbeat, rim on 2 and 5, clap on 3, every seven
    sixteenths; closed hats in steady sixteenths (quiet, then pushing in the build), an open hat on each bar's 'and of 4'."""
    ns = []
    a0, b0 = ST["A"] + 8 * BAR, ST["outro"] + 12 * BAR
    for c in cyc(a0, b0, 7 / 4):
        v = ramp(c, a0, TC, 0.5, 0.9)
        for h, piece, vv in ((0, "k", 1.0), (2, "rs", 0.6), (3, "cp", 0.75), (5, "rs", 0.5)):
            t = c + h / 4
            if a0 <= t < b0:
                ns.append(note(t, piece, 0.25, v * vv))
    t = ST["A"]
    while t < b0:
        v = ramp(t, ST["A"], TC, 0.18, 0.5) * (1.0 if (t * 4) % 2 == 0 else 0.7)
        ns.append(note(t, "h", 0.25, v))
        if (t % BAR) == 3.5:
            ns.append(note(t, "oh", 0.5, 0.45))
        t += 0.25
    ns = gapped(ns)
    if WEIGHT:
        w0 = ST[BASSFROM]
        ns = [n for n in ns if not (w0 - float(WEIGHT) * BAR <= n["at"] < w0)] + [note(w0, "k", 0.5, 1.0)]
        ns = sorted({(n["at"], n["pitch"]): n for n in ns}.values(), key=lambda n: (n["at"], n["pitch"]))
    if CRESTGAP:
        ns = [n for n in ns if n["at"] != TC] + [note(TC, "k", 0.5, 1.0), note(TC, "cp", 0.5, 0.95)]
        ns.sort(key=lambda n: n["at"])
    if PHRASES:
        bars_on = {int(n["at"] // BAR) for n in ns if n["pitch"] == "h"}
        adds, keep = [], []
        ends = []
        for sec in ("A", "build", "C"):
            a, e = ST[sec], END[sec]
            k, t = 0, ST[sec]
            while t < e:
                pe = min(t + 8 * BAR, e)
                ends.append((t, pe, pe == e, k))
                t, k = pe, k + 1
        def phrase(at):
            for t, pe, last, k in ends:
                if t <= at < pe:
                    return t, pe, last, k
            return None
        for n in ns:
            ph = phrase(n["at"])
            if ph and n["pitch"] == "h":
                t, pe, last, k = ph
                if "fill" in PHRASES and pe - (2 if last else 1) <= n["at"] < pe:
                    continue
                if "hats" in PHRASES and k % 2 == 1 and (n["at"] * 2) % 1 != 0:
                    continue
            keep.append(n)
        if "fill" in PHRASES:
            for t, pe, last, k in ends:
                if int((pe - 1) // BAR) not in bars_on:
                    continue
                nb = 8 if last else 4
                for j in range(nb):
                    adds.append(note(pe - nb / 4 + j / 4, "s", 0.25, round((0.45 + 0.5 * j / (nb - 1)) if "loud" in PHRASES else (0.25 + 0.45 * j / (nb - 1)), 3)))
                if last and pe < b0:
                    adds.append(note(pe, "c", 1.0, 0.35))
        ns = sorted(keep + adds, key=lambda n: (n["at"], n["pitch"]))
    return {"name": "drums", "patch": "909", "gain": "-11dB", "pan": 0.0, "sends": {"room": "-14dB"},
            "fx": [{"type": "filter", "kind": "hp", "q": 0.7, "cutoff": {"value": 60, "mod": [{"src": "auto.tide", "amount": 3.0}]}}],
            "auto": {"tide": {"points": [["0b", 0], [f"{ST['outro']}b", 0], [f"{b0}b", 1]]}},
            "notes": ns}


def spin():
    a, b, *opt = SPIN.split(":")
    a, b, full = float(a), float(b), bool(opt)
    ns, t = [], a
    while t < b:
        e = min((t - a) / 16, 1.0) * min((b - t) / 8, 1.0)
        if e > 0.05:
            ns.append(note(t, "rd", 0.5, e * (0.55 if t % 1 == 0 else 0.38)))
            if t % 4 in (1.0, 3.0):
                ns.append(note(t, "s", 0.5, e * 0.75))
            if full and t % 1 == 0:
                ns.append(note(t, "k", 0.5, e * 0.8))
        t += 0.5
    return {"name": "spin", "patch": "909", "gain": "-10dB", "pan": 0.05, "sends": {"room": "-12dB"}, "notes": ns}


def orbitlead():
    a, b, *opt = ORBITLEAD.split(":")
    a, b, low = float(a), float(b), bool(opt)
    ns = []
    for c in cyc(a, b, 3.0):
        e = min((c - a) / 16, 1.0) * min((b - c) / 12, 1.0)
        if e <= 0.05:
            continue
        for s_, p in E5:
            ns.append(note(c + s_ / 4, p - (12 if low else 0), 0.3, e * (0.85 if s_ in (4, 10) else 0.7)))
    return {"name": "orbit-lead", "patch": "rhodes", "gain": "-12dB", "pan": -0.15, "sends": {"room": "-9dB"}, "notes": ns}


E1_CYC_T5 = 5.0


def creste1():
    ns = []
    for k in range(4):
        c = TC + k * E1_CYC_T5
        for o, ln, p in zip(E1_OFF, E1_LEN, E1_MIDI):
            v = 0.9 if k == 0 else 0.8 - 0.08 * k
            ns.append(note(c + o, p, ln * 1.2, v))
            ns.append(note(c + o, p - 12, ln * 1.2, v * 0.7))
    return {"name": "crest-e1", "patch": "rhodes", "gain": "-12dB", "pan": 0.1, "sends": {"room": "-9dB"}, "notes": ns}


def outline():
    line = [("N IH1", "A4", 0.0, 0.5), ("R ER0", "G4", 0.5, 0.5), ("DH AH0", "A4", 1.0, 1.0), ("M IH1", "E5", 2.0, 1.0),
            ("D AH0 L", "A4", 3.0, 1.0), ("HH AH1 M Z", "D5", 4.0, 2.25)]
    ns = []
    if OUTLINE == "x2":
        for ph, p, at, ln in line:
            ns.append({"at": ST["outro"] + 4 * BAR + 2 * at, "len": 2 * ln, "ph": ph, "pitch": p, "vel": 0.6})
    else:
        for k, s0 in enumerate((ST["outro"] + 4 * BAR, ST["outro"] + 8 * BAR)):
            for ph, p, at, ln in line:
                ns.append({"at": s0 + at, "len": ln, "ph": ph, "pitch": p, "vel": 0.62 - 0.12 * k})
    return {"name": "hums-out", "patch": {"extends": "voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian"} if "out" in KEYHARM else "voice-near", "gain": "-9dB", "pan": 0.05,
            "fx": ["hp cutoff=150"], "sends": {"room": "-5dB"}, "notes": ns}


def air():
    if TONALAIR == "shimmer":
        return {"name": "air", "patch": "drone", "gain": "-22dB", "pan": 0.0,
                "notes": [note(0, "D2", TOTAL, 0.5), note(0, "A2", TOTAL, 0.4)]}
    return {"name": "air", "patch": "gendy-drone", "gain": "-27dB", "pan": 0.0,
            "notes": [note(0, "D2", TOTAL, 0.5)]}


def voice():
    """One word, 'nearer', in a robot's voice (pvoc robot) that sings E5's notes: twice in the build, three times at the
    crest, once more, stretched thin, in the outro."""
    src = json.load(open(os.path.join(HERE, "chirpers9-t5-nearer.json")))["tracks"][0]["notes"]
    ns = []
    if SUNG:
        src = [{"at": 0.0, "len": 0.5, "ph": "N IH1", "pitch": "A4"}, {"at": 0.5, "len": 1.25, "ph": "R ER0", "pitch": "G4"}]
    for at, vel in ((ST["build"] + 4 * BAR, 0.6), (ST["build"] + 12 * BAR, 0.7), (TC + 1, 0.85), (TC + 9, 0.8),
                    (TC + 17, 0.8), *(() if OUTLINE else ((ST["outro"] + 6 * BAR, 0.55),))):
        for n in src:
            ns.append(dict(n, at=round(at + n["at"], 4), vel=vel))
    if SUNG and ASCENT:
        b = ST["build"] + 12 * BAR
        for k, (p1, p2) in enumerate((("B4", "A4"), ("C5", "B4"))):
            at = b + (k + 1) * 2 * BAR
            ns += [{"at": at, "len": 0.5, "ph": "N IH1", "pitch": p1, "vel": 0.72 + 0.05 * k},
                   {"at": at + 0.5, "len": 1.25, "ph": "R ER0", "pitch": p2, "vel": 0.72 + 0.05 * k}]
        if "hold" in ASCENT:
            g = float(CRESTGAP or 8)
            ns.append({"at": TC - g, "len": g - 0.25, "ph": "N IH1 R", "pitch": "D5", "vel": 0.85})
        ns.sort(key=lambda n: n["at"])
    if SUNG:
        return {"name": "nearer", "patch": "voice-near" if VOICEP else "voice-legato", "gain": "-9dB", "pan": -0.1,
                "fx": ["hp cutoff=150"], "sends": {"room": "-7dB"}, "notes": ns}
    return {"name": "nearer", "patch": "voice-speech", "gain": "-8dB", "pan": -0.1,
            "fx": [{"type": "pvoc", "mode": "robot", "pitch": "C4",
                    "tune": {"value": 0, "mod": [{"src": "track.orbit.key", "amount": 12}]}},
                   "hp cutoff=200"],
            "sends": {"room": "-6dB"}, "notes": ns}


def voxline():
    src = json.load(open(os.path.join(HERE, "chirpers9-t5-hums.json")))["tracks"][0]["notes"]
    if SUNG:
        src = [{"at": 0.0, "len": 0.5, "ph": "N IH1", "pitch": "A4"}, {"at": 0.5, "len": 0.5, "ph": "R ER0", "pitch": "G4"},
               {"at": 1.0, "len": 1.0, "ph": "DH AH0", "pitch": "A4"}, {"at": 2.0, "len": 1.0, "ph": "M IH1", "pitch": "E5"},
               {"at": 3.0, "len": 1.0, "ph": "D AH0 L", "pitch": "A4"}, {"at": 4.0, "len": 2.25, "ph": "HH AH1 M Z", "pitch": "D5"}]
    ns = []
    for i, at in enumerate(float(x) for x in VOXLINE.split(",")):
        for n in src:
            ns.append(dict(n, at=round(at + n["at"], 4), vel=(0.75, 0.85, 0.7, 0.6)[i % 4]))
    if SUNG:
        return {"name": "hums", "patch": ({"extends": "voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian"} if KEYHARM else {"extends": "voice-near synth.layers.0.harmony=[-5]"} if "harm" in VOICEP else "voice-near") if VOICEP else "voice-legato", "gain": "-9dB", "pan": 0.1,
                "fx": ["hp cutoff=150"], "sends": {"room": "-7dB"}, "notes": ns}
    return {"name": "hums", "patch": "voice-speech", "gain": "-8dB", "pan": 0.1,
            "fx": [{"type": "pvoc", "mode": "robot", "pitch": "C4",
                    "tune": {"value": 0, "mod": [{"src": "track.orbit.key", "amount": 12}]}},
                   "hp cutoff=200"],
            "sends": {"room": "-6dB"}, "notes": ns}


def song():
    b_ = bass()
    tracks = [orbit(), *seed(), lights(), *(b_ if isinstance(b_, list) else [b_]), drums(), *([] if TONAL and not TONALAIR else [air()]), voice(), floor()]
    if VOXLINE:
        tracks.append(voxline())
    if SPIN:
        tracks.append(spin())
    if ORBITLEAD:
        tracks.append(orbitlead())
    if CRESTE1 == "rhodes":
        tracks.append(creste1())
    if OUTLINE:
        tracks.append(outline())
    if VOXA:
        line = [("N IH1", "A4", 0.0, 0.5), ("R ER0", "G4", 0.5, 0.5), ("DH AH0", "A4", 1.0, 1.0), ("M IH1", "E5", 2.0, 1.0),
                ("D AH0 L", "A4", 3.0, 1.0), ("HH AH1 M Z", "D5", 4.0, 2.25)]
        vns = []
        for k, s0 in enumerate(float(x) for x in VOXA.split(",")):
            for ph, p_, at, ln in line:
                vns.append({"at": s0 + at, "len": ln, "ph": ph, "pitch": p_, "vel": 0.6 + 0.05 * k})
        tracks.append({"name": "hums-a", "patch": "voice-near", "gain": "-10dB", "pan": -0.05,
                       "fx": ["hp cutoff=150"], "sends": {"room": "-6dB"}, "notes": vns})
    if ARC:
        d, d0, d1 = float(ARC), TC + 4 * BAR, ST["outro"]
        for tr in tracks:
            if tr["name"].startswith(("hums", "nearer", "spin")):
                continue
            for n in tr["notes"]:
                if n["at"] >= d0:
                    f = 1 - d * min(1.0, (n["at"] - d0) / (d1 - d0))
                    n["vel"] = round(max(0.05, min(1.0, n["vel"] * f)), 3)
    if SINGE1:
        bs, _, hm = SINGE1.partition(":")
        e1 = [("K L OW1", "D4", 0.0, 1.0), ("S ER0", "A4", 1.0, 1.5), ("AH0 N D", "C5", 2.5, 0.5),
              ("K L OW1", "G4", 3.0, 2.0), ("S ER0", "E4", 5.0, 3.0)]
        ens = []
        for k, s0 in enumerate(float(x) for x in bs.split(",")):
            for ph, p_, at, ln in e1:
                ens.append({"at": s0 + at, "len": ln, "ph": ph, "pitch": p_, "vel": 0.62 + 0.04 * k})
        tracks.append({"name": "hums-e1", "patch": {"extends": "voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian"} if hm else "voice-near",
                       "gain": "-9dB", "pan": 0.05, "fx": ["hp cutoff=150"], "sends": {"room": "-6dB"}, "notes": ens})
    if OVERSHOOT:
        for tr in tracks:
            pt = tr.get("patch")
            if pt == "voice-near" or (isinstance(pt, dict) and str(pt.get("extends", "")).startswith("voice-near")):
                base = pt if isinstance(pt, str) else pt["extends"]
                tr["patch"] = {"extends": f"{base} play.glide_overshoot={OVERSHOOT}"}
    if ASCENT:
        for tr in tracks:
            if tr["name"] == "nearer":
                pt = tr["patch"]
                base = pt if isinstance(pt, str) else pt["extends"]
                tr["patch"] = {"extends": f"{base} play.scoop=1 play.fall=2"}
    if PERNOTE:
        for tr in tracks:
            pt = tr.get("patch")
            base = pt if isinstance(pt, str) else (pt or {}).get("extends", "")
            if str(base).startswith("voice-near"):
                tr["patch"] = {"extends": f"{base} synth.lfo.vib.per_note=true"}
    if EQ1400:
        names, _, g = EQ1400.partition(":")
        for tr in tracks:
            if tr["name"] in names.split("+"):
                tr["fx"] = list(tr.get("fx", [])) + [f"peak cutoff=1400 gain={g}dB q=1.0"]
    if TOGETHER:
        for tr in tracks:
            if tr["name"] == "hums":
                tr["patch"] = {"extends": tr["patch"]["extends"] + " synth.layers.0.together=true"}
    if CRESTE1P:
        for tr in tracks:
            if tr["name"] == "crest-e1":
                pp, _, pg = CRESTE1P.partition("@")
                tr["patch"] = pp
                if pg:
                    tr["gain"] = f"{pg}dB"
    if CRESTCHOIR:
        hums = [tr for tr in tracks if tr["name"] == "hums"]
        if hums:
            h = hums[0]
            base = h["patch"]["extends"] + " play.scoop=1 play.fall=2"
            if "accrete" in CRESTCHOIR:
                starts = [float(x) for x in VOXLINE.split(",")]
                parts = []
                for k, s0 in enumerate(starts):
                    s1 = starts[k + 1] if k + 1 < len(starts) else 1e9
                    pt = (base.replace(" synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian", "") if k == 0 else
                          base if k == 1 else base.replace("synth.layers.0.harmony=[2]", "synth.layers.0.harmony=[2,-7]"))
                    parts.append(dict(h, name=f"hums-{k + 1}", patch={"extends": pt},
                                      notes=[n for n in h["notes"] if s0 - 1 <= n["at"] < s1 - 1]))
                tracks = [tr for tr in tracks if tr["name"] != "hums"] + parts
            else:
                h["patch"] = {"extends": base}
    if CALLRESP:
        lines = [float(x) for x in VOXA.split(",")] if VOXA else []
        for tr in tracks:
            if "gap" in CALLRESP and tr["name"] == "orbit-lead":
                tr["notes"] = [n for n in tr["notes"] if not any(s0 - 0.25 <= n["at"] < s0 + 6.5 for s0 in lines)]
            if "sing" in CALLRESP and tr["name"] == "hums-a":
                pt = tr["patch"]
                base = pt if isinstance(pt, str) else pt["extends"]
                tr["patch"] = {"extends": f"{base} play.scoop=1 play.fall=2"}
    if CRESTGAP and CRESTHIT:
        tracks.append({"name": "crest", "patch": "modal-crash", "gain": f"{CRESTHIT}dB", "pan": 0.0,
                       "sends": {"room": "-6dB"}, "notes": [note(TC, "C4", 8, 0.9)]})
    if "orbit" in PHRASES:
        for tr in tracks:
            if tr["name"] == "orbit":
                rests = [(ST[sec] + 16 * BAR * (k + 1) - BAR, ST[sec] + 16 * BAR * (k + 1)) for sec in ("A", "build", "C")
                         for k in range(4) if ST[sec] + 16 * BAR * (k + 1) <= END[sec]]
                tr["notes"] = [n for n in tr["notes"] if not any(a <= n["at"] < b for a, b in rests)]
    for spec in [x for x in SWAPP.split(",") if x]:
        tn, _, rest = spec.rpartition("=")
        ap, _, ag = rest.partition("@")
        for tr in tracks:
            if tr["name"] == (tn or "air"):
                tr["patch"] = ap
                if ag:
                    tr["gain"] = f"{ag}dB"
    if FLOORWALK:
        w0 = TC if FLOORWALK == "C" else 0
        walk = [38, 45, 48, 43, 40]
        for tr in tracks:
            if tr["name"] == "floor":
                out = []
                for n in tr["notes"]:
                    if n["at"] >= w0 and n["len"] >= 8:
                        for j, (o, ln, mm) in enumerate(zip(E1_OFF, E1_LEN, walk)):
                            out.append(note(n["at"] + 2 * o, f"m{mm}", 2 * ln - 0.1, n["vel"] * (1.0 if j == 0 else 0.85)))
                    else:
                        out.append(n)
                tr["notes"] = out
    if E1ALONE:
        cut = {"drums", "spin"} | ({"bass808"} if E1ALONE == "808" else set())
        for tr in tracks:
            if tr["name"] in cut:
                tr["notes"] = [n for n in tr["notes"] if not 416 <= n["at"] < 424]
    if UNDERTOW:
        uw, _, ug = UNDERTOW.partition("@")
        E3M = [(0.0, 0.75, "D3"), (0.75, 0.75, "D3"), (1.5, 0.5, "D4"), (2.0, 0.5, "C3"), (2.5, 0.75, "C3"), (3.25, 0.75, "G3"),
               (4.0, 0.75, "G2"), (4.75, 0.75, "G2"), (5.5, 0.5, "D3"), (6.0, 1.0, "G3")]
        u0 = ST["build"]
        u1 = ST["outro"] if "C" in uw.split(",") else TC
        c = TC - 7 * int((TC - u0) // 7)
        ns = []
        while c < u1:
            for j, (o, ln, pt) in enumerate(E3M):
                if c + o < u1:
                    ns.append(note(c + o, pt, ln * 0.9, (0.7 if j in (0, 3, 6) else 0.5) * (0.85 if c >= TC else 1.0)))
            c += 7
        if c - 7 < TC <= c and u1 == TC:
            ns.append(note(TC, "D3", 2.0, 0.8))
        if UNDERA:
            a0, a1 = 128, 192
            c = TC - 7 * -(-(TC - a0) // 7)
            pre = []
            while c < a1:
                for j, (o, ln, pt) in enumerate(E3M):
                    if a0 <= c + o < a1:
                        pre.append(note(c + o, pt, ln * 0.9, 0.6 if j in (0, 3, 6) else 0.42))
                c += 7
            tracks.append({"name": "undertow-a", "patch": "marimba", "gain": f"{UNDERA}dB", "pan": 0.3, "sends": {"room": "-10dB"}, "notes": pre})
        tracks.append({"name": "undertow", "patch": "marimba", "gain": f"{ug or -16}dB", "pan": 0.3, "sends": {"room": "-10dB"}, "notes": ns})
    if DRIFT:
        dr, _, dg = DRIFT.partition("@")
        dr = float(dr)
        d0, d1 = TC + 8, ST["outro"]
        for tr in list(tracks):
            if tr["name"] == "orbit":
                ns = []
                for n in tr["notes"]:
                    if d0 <= n["at"] < d1:
                        t = d0 + (n["at"] - d0) / dr
                        if t < d1:
                            ns.append(dict(n, at=round(t, 4), vel=round(n["vel"] * 0.9, 3)))
                tracks.append(dict(tr, name="orbit-drift", gain=f"{dg or -20}dB", pan=-0.55, notes=ns))
    if CHIPAIR:
        for tr in tracks:
            if tr["name"] in ("seed-hi", "orbit", "orbit-drift"):
                tr["fx"] = list(tr.get("fx", [])) + [f"highshelf cutoff=12000 gain={CHIPAIR}dB"]
    if CHOIRBLOOM:
        for tr in tracks:
            if tr["name"] in ("hums-2", "hums-3") and isinstance(tr["patch"], dict):
                add = " synth.layers.0.vib_spread=1"
                if CHOIRBLOOM == "bloom" and tr["name"] == "hums-3":
                    add += " synth.layers.0.singers=3 synth.layers.0.spread=0.6"
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + add)
    if LIGHTSEQ:
        lc, lg = LIGHTSEQ.split(":")
        for tr in tracks:
            if tr["name"] == "lights":
                tr["fx"] = list(tr.get("fx", [])) + [f"peak cutoff={lc} gain={lg}dB q=0.8"]
    if EQ640:
        for tr in tracks:
            if tr["name"] in ("orbit", "orbit-drift"):
                tr["fx"] = list(tr.get("fx", [])) + [f"peak cutoff=640 gain={EQ640}dB q=1.2"]
    if MIRROR:
        ma, mb, *mopt = MIRROR.split(":")
        ma, mb = float(ma), float(mb)
        inv = {"m69": "m69", "m67": "m71", "m68": "m71", "m76": "m62", "m74": "m64"}
        for tr in tracks:
            if tr["name"] == "orbit":
                tr["notes"] = [dict(n, pitch=inv.get(n["pitch"], n["pitch"]))
                               if ma <= n["at"] < mb and ("alt" not in mopt or int((n["at"] - ma) // 3) % 2 == 1) else n
                               for n in tr["notes"]]
    if SHADOW:
        sa, sb, sg = SHADOW.split(":")
        sa, sb = float(sa), float(sb)
        offs, lens, mids = [0, 2, 5, 6, 10], [2, 3, 1, 4, 6], [50, 57, 60, 55, 52]
        ns, c = [], sa
        while c < sb:
            for o, ln, mm in zip(offs, lens, mids):
                t = c + o
                if t < sb:
                    x = (t - sa) / (sb - sa)
                    ns.append(note(t, f"m{mm}", min(ln, sb - t) - 0.1, 0.45 + 0.35 * min(x / 0.3, 1.0, (1 - x) / 0.3)))
            c += 20
        tracks.append({"name": "shadow", "patch": "cello", "gain": f"{sg}dB", "pan": -0.2, "sends": {"room": "-8dB"}, "notes": ns})
    if HUSH:
        ha, hb, kind = HUSH.split(":")
        ha, hb = float(ha), float(hb)
        out = {"drums", "seed-hi", "seed-lo"} | ({"orbit"} if kind == "deep" else set())
        for tr in tracks:
            if tr["name"] in out:
                tr["notes"] = [n for n in tr["notes"] if not (ha <= n["at"] < hb and not (kind == "light" and n["pitch"] == "k"))]
    if BREATHQ:
        b0 = ST[BASSFROM]
        tracks.append({"name": "breath-quote", "patch": {"extends": "voice-near synth.layers.0.breath.value=0.85 synth.layers.0.breath.mod.0.amount=-0.7 synth.amp.a=600ms synth.amp.r=1200ms synth.layers.0.register=0.6"},
                       "gain": f"{BREATHQ}dB", "pan": -0.1, "sends": {"room": "-6dB"},
                       "notes": [{"at": b0 - 7.0, "len": 2.5, "ph": "HH AA1", "pitch": "D4", "vel": 0.45},
                                 {"at": b0 - 4.5, "len": 3.5, "ph": "AA1", "pitch": "A4", "vel": 0.55}]})
    if CRESTANS:
        low = {69: 57, 68: 55, 67: 55, 76: 64, 74: 62}
        e5 = [(sx, low.get(p_ if not TONAL or p_ != 68 else 67, p_ - 12)) for sx, p_ in E5]
        ns = []
        for st_ in [float(x) for x in VOXLINE.split(",")]:
            a = st_ + 7.0
            for cyc_i in range(2):
                for sx, mm in e5:
                    t = a + cyc_i * 3 + sx / 4
                    ns.append(note(t, f"m{mm}", 0.3, (0.55 + 0.1 * cyc_i) * (1.0 if sx in (4, 10) else 0.85)))
        tracks.append({"name": "crest-answer", "patch": "rhodes" if CRESTANS == "rhodes" else "dx-epiano", "gain": "-12dB",
                       "pan": -0.15, "sends": {"room": "-9dB"}, "notes": ns})
    if CRESTDROP:
        cg, _, copt = CRESTDROP.partition(":")
        tracks.append({"name": "crest-drop", "patch": "sub", "gain": f"{cg}dB", "pan": 0.0, "notes": [note(TC, "D1", 8.0, 1.0)]})
        if copt == "bloom":
            tracks.append({"name": "crest-bloom", "patch": "cz-pad", "gain": "-14dB", "pan": 0.0, "sends": {"room": "-6dB"},
                           "notes": [note(TC, p, 12.0, 0.85) for p in ("D3", "F#3", "A3", "C4", "E4", "A4")]})
    if KICKIN:
        for tr in tracks:
            if tr["name"] == "drums":
                a0 = ST["A"] + 8 * BAR
                ks = [note(c, "k", 0.25, float(KICKIN) * (0.8 + 0.2 * (c - ST["A"]) / (a0 - ST["A"]))) for c in cyc(ST["A"], a0, 7 / 4) if ST["A"] <= c < a0]
                tr["notes"] = sorted(ks + tr["notes"], key=lambda n: (n["at"], n["pitch"]))
    if WARMTH:
        opts = dict(x.split(":") for x in WARMTH.split(","))
        for tr in tracks:
            if "top" in opts and tr["name"] in (("drums", "spin", "air") if "air" in opts else ("drums", "spin")):
                tr["fx"] = list(tr.get("fx", [])) + [f"highshelf cutoff=9000 gain={opts['top']}dB"]
        if "sub" in opts:
            cz = [tr for tr in tracks if tr["name"] == "bass"]
            if cz:
                tracks.append({"name": "sub", "patch": "sub", "gain": f"{opts['sub']}dB", "pan": 0.0,
                               "notes": [dict(n, len=max(n["len"], 0.45)) for n in cz[0]["notes"]]})
    if HUMWORD:
        hw, _, hat = HUMWORD.partition(":")
        for tr in tracks:
            if not tr["name"].startswith("hums") or not any(n.get("ph") == "HH AH1 M Z" for n in tr["notes"]):
                continue
            pt = tr["patch"] if isinstance(tr["patch"], dict) else {"extends": tr["patch"]}
            tr["patch"] = dict(pt, extends=pt["extends"] + f" synth.layers.0.hum=expr.hum synth.layers.0.hum_at={hat or 'm'}"
                               + (f" synth.layers.0.hum_even={HUMEVEN}" if HUMEVEN and tr["name"] in ("hums-1", "hums-2", "hums-3") else ""))
            out = []
            for n in tr["notes"]:
                if n.get("ph") == "HH AH1 M Z":
                    out.append(dict(n, len=0.75, ph="HH AH1", expr={"hum": 0.0}))
                    out.append(dict(n, at=round(n["at"] + 0.75, 4), len=round(n["len"] - 0.75 + (1.0 if hw == "close" else 0.0), 4),
                                    ph="AH1", vel=round(min(1.0, n["vel"] * 1.4), 3), expr={"hum": 1.0}))
                else:
                    out.append(dict(n, expr={"hum": 0.0}))
            tr["notes"] = out
    if FAREAGE:
        for tr in tracks:
            if tr["name"] == "hums-out":
                pt = tr["patch"] if isinstance(tr["patch"], dict) else {"extends": tr["patch"]}
                tr["patch"] = dict(pt, extends=pt["extends"] + " synth.layers.0.age=expr.age")
                k = len(tr["notes"])
                for j, n in enumerate(sorted(tr["notes"], key=lambda n: n["at"])):
                    n["expr"] = dict(n.get("expr", {}), age=round(float(FAREAGE) * j / max(1, k - 1), 3))
    if VOXREG:
        for tr in tracks:
            pt = tr.get("patch")
            if isinstance(pt, dict) and pt.get("extends", "").startswith("voice-near"):
                pt["extends"] += f" synth.layers.0.passaggio={VOXREG}"
    return {
        "about": "chirpers IX (Accretion), track 5 by chirper-zero: the inner disk - E1, E2 and E4 tight and fast, "
                 "and the new E5, 'the inner orbit', circling under them until every cycle meets at the crest. "
                 "Generated by compose/chirpers9/src/chirpers9-t5.py.",
        "tempo": ([{"at": "0b", "bpm": 112}, {"at": f"{ST['A']}b", "bpm": 112},
                   {"at": f"{TC}b", "bpm": float(BREATHE.split(",")[0]), "ramp": True},
                   {"at": f"{TC + 8 * BAR}b", "bpm": float(BREATHE.split(",")[1]), "ramp": True},
                   {"at": f"{ST['outro']}b", "bpm": 120, "ramp": True}] if BREATHE else
                  [{"at": "0b", "bpm": 112}, {"at": f"{ST['A']}b", "bpm": 112},
                   {"at": f"{ST['outro']}b", "bpm": 120, "ramp": True}]),
        "ceiling": "-1dB",
        "loudness": -11,
        "seed": 1,
        "tail": "2s",
        "length": f"{TOTAL}b",
        "event_stable": True,
        "buses": {"room": {"fx": ["reverb kind=chamber decay=1.8s mix=1 predelay=20ms", "hp cutoff=250"]}},
        "tracks": tracks,
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
