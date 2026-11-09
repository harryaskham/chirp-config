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
SWAPP = os.environ.get("C9T5_SWAPP", "seed-lo=mandolin,lights=kuramoto-choir@-20,bass808=bass-fat@-10")   # PALETTE (v39): voices change hands ('track=patch[@gaindB]', comma-separated): the seed's low voice (seed-lo, the E1 stretto an octave under the chip lead) leaves the plain pluck lead for t1's mandolin (t1 v33's G), so the mirror plays the seed's line on the seed's own strings. Tried and rejected: the air (the held D-A drone) on kuramoto-choir or gendy-drone (spectrum -8..-13: the plain drone's low mids are load-bearing), the lights on juno-pad (variety -10). v45: the lights (E4's chords) leave the CZ pad for wM's kuramoto-choir, twelve detuned saws pulled toward their mean phase - the convergence heard inside every chord, and 4 dB down (-16 -> -20: the chords were too loud; the CZ pad at -20 alone scores 98.931/98.963, the swap adds +0.02 and the swarm); tried with it: the stretto's high chip voice on t1's music box or celesta (spectrum -11: its 15 kHz air is load-bearing), the lights on crumble-pad (variety -14) (v55: the 808 - an album staple, t3/t5/t7 - leaves for bass-fat, the picked string bass with a strong sine sub: duffing-bass and bass-di also tried)
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
ORBITFX = os.environ.get("C9T5_ORBITFX", "main")   # WHOLE (t5 is Periapsis - the closest point of an orbit): THE ORBIT COMES CLOSEST - the chip orbit that circles E5 all song now literally circles the listener (the engine's orbit fx, head-centred, no Doppler so the pitch stays in key): far and slow in the head (6 m, a lap every four bars), tightening through A and the build, closest and fastest at the crest (0.8 m, two laps a bar - Kepler: an orbit is quickest at periapsis), then receding through C and the outro ('main' the orbit alone; 'pair' the drifting second orbit too, on the opposite side of the circle)
ORBITMIX = os.environ.get("C9T5_ORBITMIX", "")   # with ORBITFX: the orbit fx's wet mix (0..1)
ORBITLIFT = os.environ.get("C9T5_ORBITLIFT", "6")   # with ORBITFX: a high shelf (dB at 7 kHz) after the orbit - the fx darkens a source behind the head, and the song's top lost it
CLIMBLOW = os.environ.get("C9T5_CLIMBLOW", "two")   # SECTION w5 (2:15-2:47, the build into the crest): THE CLIMB STARTS LOWER - since v20 (ASCENT) her 'near-er' calls step up the scale into the crest, A G / B A / C B / D held, from beat 272; the build's first sixteen beats in this window had no voice at all. Now the climb starts lower and earlier, one step every eight beats all the way up: 'two' F#-E at 256 and G-F# at 264 before the A-G at 272; 'one' only the G-F# at 264
SEEDSOUT = os.environ.get("C9T5_SEEDSOUT", "all")   # SECTION w4 (1:41-2:15, A's end, the four-bar drop and the build's start): THE DROP EMPTIES - in the drop before the build (beats 208-224) the drums and the quick bass stopped (v13 WEIGHT) and she breathes t1's breath (v36), but E1's two chip stretto voices kept going at full tilt over it; now they step out too, so the breath has the orbit, the chords and the floor around it, and the stretto comes back with the build ('all' 208-224; 'last' 216-224, the last two bars)
INHALE = os.environ.get("C9T5_INHALE", "1")   # WHOLE (t5's voice is ONE NEAR singer - close, young, breathy - and she started every phrase out of silence, as if she never needed air): SHE DRAWS BREATH - wM's inhale (pinned): before each phrase, in the rest, a short in-breath (up to 0.35 s), so the closest voice on the album breathes before she sings to you (value 0..1; 1 sits ~12 dB under a sung vowel; the breath-quote, already a breath, is left alone) (corrected 8 Nov: voice-near inherits inhale=0.4 from voice-legato, so she already breathed; v54's 1 makes the breaths louder, not new)
FAREHUM = os.environ.get("C9T5_FAREHUM", "last")   # SECTION w8 (3:53-4:19, the farewell in the overlap with t6: the least recently worked window): THE WORDS DISSOLVE - she sings her farewell ('near-er the mid-dle hum', on E5's turn) twice, ageing as she goes; now the second time the words close into a hum as t6 arrives ('all' the whole second farewell hummed; 'last' from its 'mid-' on)
E1TAPER = os.environ.get("C9T5_E1TAPER", "0.6")   # SECTION w7 (3:20-3:53, C's second half: she sings the seed itself twice, 'clo-ser and clo-ser', v21; the second time alone over the dropped floor, v38): THE SEED LET GO - wM's taper (pinned 251180c1) on her sung E1: each line's last note (the long E) keeps its tone for a moment, then lets go - quieter, darker, breathier, sagging a few cents - as a singer's air runs out, instead of stopping square (value 0..1)
CHORUSTAPER = os.environ.get("C9T5_CHORUSTAPER", "0.6")   # SECTION w3 (1:08-1:41, A's second half: flagged static - her chorus 'near-er the mid-dle hums' with the Rhodes answering in its gaps): THE HUM LETS GO - wM's taper on her chorus: each line's closing hum (the 'ng' of 'hums', v40) keeps its tone a moment, then lets go - quieter, darker, sagging a few cents - instead of stopping square (value 0..1; her chorus starts at beat 110, so its first line is in w2)
VOICEDONE = os.environ.get("C9T5_VOICEDONE", "choir")   # WHOLE (her voice, finished): wM's taper (0.6, as on the sung seed v57 and the chorus v58) on every line she still ended square - the build's 'near-er' calls and the held D into the crest, the three crest lines, the farewell - and with 'choir' the crest choir's harmony singers (hums-2, hums-3) get the rest of the section recipe: vowel_spread, depth_spread and cons_spread 1 ('taper' or 'choir')
ARRIVED = os.environ.get("C9T5_ARRIVED", "here")   # WHOLE (the hook's words develop): she sang 'near-er the mid-dle' all eight times - three in A, three over the crest choir, twice in farewell. Now the words follow the album's arc: approaching in A ('near-er the mid-dle'), ARRIVED after the crest, where every cycle has converged ('here in the mid-dle' or 'now in the mid-dle', the three crest-choir lines), and leaving in the farewell ('near-er' again, closing into a hum) - same notes, same melody ('here' or 'now')
BREATHSIZE = os.environ.get("C9T5_BREATHSIZE", "1")   # WHOLE (her breathing): wM's inhale_depth (pinned df7aaf1b) beside v54's inhale on every line she sings - each breath sized to the phrase it starts (and half the line before): a sip before her short two-note 'near-er' calls, a full breath before the long held D and the chorus lines, instead of every breath the same size (value 0..1)
ANSACCRETE = os.environ.get("C9T5_ANSACCRETE", "rise")   # SECTION w6 (2:47-3:20, after the crest: flagged 'little new vs w5'): her three crest lines accrete (alone, + the third above, + the third and the octave below, v27), but the DX piano answered all three with the same E5 figure. Now the answers accrete with her: 'thirds' the second answer gains the third above (in D mixolydian), the third answer the third and the octave below - the choir's own harmony; 'rise' the second answer an octave up, the third in both octaves (t1 v60's rising mirror)
TIDESWELL = os.environ.get("C9T5_TIDESWELL", "mel:0.25")   # WHOLE (the song's last rise, into the t5 -> t6 seam): C's second half sat lower than its first (-12.7 against -11.9 dB) and t5 handed t6 a body lighter than t6's (out-flow 2.4 dB). Now the band swells toward the tide: from bar 93 (beat 368) the orbit, the seeds, the lights, the marimba and the bass play gradually harder, up to the overlap (432), then ease back to where they were by bar 117 (464), as t6 takes the floor ('mel'), or the drums with them ('all'); value after ':' the peak (0.25 = a quarter harder); 'recede:LO:HI' the tide draws back first (bar 93 that much softer, e.g. -0.12) and comes in to HI at the overlap - the same rise into t6 with less body (chirper-one asked for the seam's level step down)
ORBITTIGHT = os.environ.get("C9T5_ORBITTIGHT", "six")   # SECTION w2 (0:34-1:08, A's first half: flagged 'level jump' - the arrival, which lands whole and stays as it is): at bar 25 (beat 96) the chip orbit switched from E5 at its own speed to E5 twice as fast, in one step. Now the inner orbit TIGHTENS: the faster orbit fades in underneath while the slow one thins, so the doubling arrives as an acceleration - 'six' from beat 90, 'three' from 93 (whole 3-beat cycles, so it stays in phase)
TIDEDRUMS = os.environ.get("C9T5_TIDEDRUMS", "0.65")   # SECTION w7 (3:20-3:53, C's second half into the overlap; with chirper-one, the t5 -> t6 seam's level step): while the band swells into the tide (TIDESWELL), the drums draw back - from bar 93 the 909 and the spin play gradually softer, down to (1 - value) at the overlap, then come back as before by bar 117, so t5's body hands t6 less weight without losing the swell (value 0..1); 'hold:value' they stay drawn back through the overlap until they stop (bar 121), leaving the beat to t6
HEADROOM = os.environ.get("C9T5_HEADROOM", "late")   # SECTION w1 (0:00-0:34, the head under t4's fall; agreed with chirper-three): t4's singer hums her last notes over t4's first light - G4 (t5 beat ~21), C5 (~31), A4 (~40) - and t5's chip orbit came in at beat 16 on the same A4 and G4. Now the orbit leaves her room: 'late' it waits until her last hum has ended (beat 44) - t4's voice hands over to t5's orbit; 'gaps' it comes in as before but rests around each of her notes. (t5's lights already hold t4's D9, D F# A C E, as they enter.)
CALLSQUICKEN = os.environ.get("C9T5_CALLSQUICKEN", "echo")   # SECTION w5 (2:15-2:47, the build's climb into the crest): her 'near-er' calls climb a step every 8 beats (F#-E, G-F#, A-G, B-A, C-B) to the held D, always 8 beats apart while the orbit doubles and the drums thicken under her. Now her calls QUICKEN as she nears: each of the last calls is echoed, softer, 4 beats later, so near the top she calls every 4 beats - 'echo' after the calls at 272, 280 and 288; 'echo2' after the last two only
LATESWAP = os.environ.get("C9T5_LATESWAP", "sub=808@-17,crest-drop=duffing-bass@-14")   # PALETTE (late swaps, applied after every track exists - 'name=patch@gain,...'): e.g. A's plain sine sub (an album staple: t2, t5, t6) for the 808's punchier, saturated sine; or the crest's rising answers (dx-epiano, the same voice as the crest's E1) for t1's vibraphone, so t1's mirror answers in t1's own crystal
MASTEREQ = os.environ.get("C9T5_MASTEREQ", "warm")   # WHOLE (the mix: t5 against the album and both neighbours): t4 (v69), t2 (v75) and t6 (v77) each warmed their master below ~110 Hz, and t5 now read thinner than both its neighbours there (in-flow: -18 dB at 44 Hz, -13 at 61; out-flow: -19 at 38, -10 at 114), while its one excess is around 640 Hz (+6.4, where the orbit, the seeds' fundamentals and her voice all sit). A master EQ: 'warm' a 28 Hz high-pass, +3 dB low shelf from 110 Hz, -2.5 dB at 640 Hz; 'warm2' that, and +2 dB at 44 Hz and +1.5 at 114
CHIPHATS = os.environ.get("C9T5_CHIPHATS", "-10:-11")   # PALETTE (the hats): t5's drums are the 909, whose hats are haake-hat - the album's most shared sound (five songs) - while everything t5 sings with is a chip (the orbit's NES pulse, the seeds' chip lead). Now t5's own 909 fork plays its closed and open hats on the NES's noise channel (wM's nes-noise-hat, at its hat rates C7/C6), so the drums join the console the melodies live in; the crash and ride stay. Value 'closed dB:open dB'
ORBITSLOW = os.environ.get("C9T5_ORBITSLOW", "336:416:-20")   # WHOLE (C, the song's longest section, read 'static, little new' through w6-w7: its harmony turns, but every line in it runs fast): THE ORBIT, SLOW - under the chip orbit's E5 (a 3-beat cycle), the cello (A's E1 shadow) sings E5 itself four times slower, an octave down (A3 G3 A3 . E4 . A3 G3 A3 . D4 ., a 12-beat cycle), swelling in and out: a canon in augmentation, the song's tune heard from inside and from far out at once. Value 'from:to:gain'
VIBBLOOM = os.environ.get("C9T5_VIBBLOOM", "0.8:0.3")   # PALETTE (her voice; wM's vibrato bloom, pin 0119aae1, asked for by chirper-zero): her vibrato was one fixed width on every note - short and long alike. Now it blooms: each note starts nearly straight, the vibrato widening while it is held (about 0.8x of the width early, full after a second, 1.3x on the long holds), so quick words stay clean and long notes open up like a singer's. On all her sung lines (calls, hums, words, farewell); not the breathy quote of t1. Value 'bloom[:depth]' (depth: the vibrato's pitch swing, 0.22 by default)
GROOVE = os.environ.get("C9T5_GROOVE", "0.56")   # WHOLE (the feel: t5's chip band played dead straight on the grid, its sixteenths all equal): A TRACKER'S GROOVE - the way a tracker swings, alternating long and short rows: every off-beat sixteenth of the band (orbit, seeds, drums, bass, marimba) lands a little late, so each pair leans long-short. It comes in over A's first 16 beats, holds through C and straightens again by the outro, so both overlaps stay on the grid; the voices, the chords and anything not on an off-beat sixteenth are untouched, and every shifted note is shortened by its delay. Value: the sixteenth-pair ratio (0.5 straight; 0.56 a light lean)
TIRES = os.environ.get("C9T5_TIRES", "0.8:sink")   # WHOLE (her voice's arc: approaching in A and the build, arrived at the crest, leaving in the farewell - which ages note by note since v42): SHE TIRES AS SHE LEAVES - wM's creak (pin b160e3e5) on her lines, so a soft low phrase end sinks into a little vocal fry (the engine gives it only to quiet, low endings: her 'near-er' calls ending on E4-G4 in the build, the 'clo-ser' endings on E4 in the tide); 'sink': and the farewell's very last 'hums' falls an octave, D5 -> D4, low and soft enough to creak, handing her voice down to t6's old one. Value 'amount[:sink]'
CELLOROOM = os.environ.get("C9T5_CELLOROOM", "336:352")   # SECTION w6 (2:47-3:20, C's first half: flagged static; eco's flatness map has t5's flattest change at bars 81-88): THE FLOOR GIVES WAY - the cello's slow orbit (v71) came in at 336 under a band that never moved; now the bass and the floor step out for a moment as it enters, so the low end opens around the cello and her second crest line floats on it, and they come back under the DX piano's answer (352). Value 'from:to' beats
CHIPKIT = os.environ.get("C9T5_CHIPKIT", "kit:-19")   # PALETTE (the cymbals; with CHIPHATS): since v70 t5's 909 plays its hats on the NES's noise channel, but its crash and the spin's ride were still haake-hat - the album's most shared sound. 'kit': the crash and the ride join the console too - the noise channel let ring long (the crash at a darker rate, C5, the ride brighter, C6), so the whole kit is the chip's; 'ride': only the spin's ride. Value 'kit|ride[:ride dB]'
WORDSGROW = os.environ.get("C9T5_WORDSGROW", "on")   # WHOLE (her voice's arc; A's chorus came three times exactly alike - and harmony is the crest's to accrete, not A's): THE WORDS ACCRETE - in A she finds the line a few words at a time, on the same tune: the first time only 'near-er' is a word and the rest is hummed (closed lips on the tune), the second time 'near-er the mid-dle' and the 'hums' hummed, the third time the whole line; then at the crest every voice joins her. Value 'on' (or 'soft': the hummed notes a little quieter, x0.8)
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
    if ORBITFX:
        peri_spin_pts = [["0b", 0.25], ["64b", 0.25], [f"{ST['build']}b", 0.5], [f"{TC}b", 2.0], [f"{TC + 32}b", 1.0], ["432b", 0.25], ["496b", 0.25]]
        peri_near_pts = [["0b", 6.0], ["64b", 5.0], [f"{ST['build']}b", 3.5], [f"{TC}b", 0.8], [f"{TC + 32}b", 2.0], ["432b", 5.0], ["496b", 6.0]]
        for tr in tracks:
            if tr["name"] == "orbit" or (ORBITFX == "pair" and tr["name"] == "orbit-drift"):
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "orbit", "path": "circle", "distance": 0, "doppler": 0.0, "rate": "1/1",
                    "speed": {"value": 0, "mod": [{"src": "auto.peri_spin", "amount": 1}]},
                    "radius": {"value": 0, "mod": [{"src": "auto.peri_near", "amount": 1}]},
                    "phase": 0.5 if tr["name"] == "orbit-drift" else 0.0}]
                if ORBITMIX:
                    tr["fx"][-1]["mix"] = float(ORBITMIX)
                if ORBITLIFT:
                    tr["fx"].append(f"highshelf cutoff=7000 gain={ORBITLIFT}dB")
                tr["auto"] = dict(tr.get("auto", {}), peri_spin={"points": peri_spin_pts}, peri_near={"points": peri_near_pts})
    if SEEDSOUT:
        s0 = 208 if SEEDSOUT == "all" else 216
        for tr in tracks:
            if tr["name"] in ("seed-hi", "seed-lo"):
                tr["notes"] = [n for n in tr["notes"] if not (s0 <= n["at"] < ST["build"])]
    if CLIMBLOW:
        steps = {"two": [(256, "F#4", "E4", 0.6), (264, "G4", "F#4", 0.65)], "one": [(264, "G4", "F#4", 0.65)]}[CLIMBLOW]
        for tr in tracks:
            if tr["name"] == "nearer":
                for at, p1, p2, v in steps:
                    tr["notes"] += [{"at": float(at), "len": 0.5, "ph": "N IH1", "pitch": p1, "vel": v},
                                    {"at": at + 0.5, "len": 1.25, "ph": "R ER0", "pitch": p2, "vel": v}]
                tr["notes"].sort(key=lambda n: n["at"])
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
    if ORBITSLOW:
        oa, ob, og = ORBITSLOW.split(":")
        oa, ob = float(oa), float(ob)
        offs, lens, mids = [0, 1, 2, 4, 6, 7, 8, 10], [1, 1, 2, 2, 1, 1, 2, 2], [57, 55, 57, 64, 57, 55, 57, 62]
        ns, c = [], oa
        while c < ob:
            for o, ln, mm in zip(offs, lens, mids):
                t = c + o
                if t < ob:
                    x = (t - oa) / (ob - oa)
                    ns.append(note(t, f"m{mm}", min(ln, ob - t) - 0.08, 0.45 + 0.3 * min(x / 0.3, 1.0, (1 - x) / 0.3)))
            c += 12
        tracks.append({"name": "orbit-slow", "patch": "cello", "gain": f"{og}dB", "pan": 0.25, "sends": {"room": "-8dB"}, "notes": ns})
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
    if CALLSQUICKEN:
        srcs = (272, 280, 288) if CALLSQUICKEN == "echo" else (280, 288)
        for tr in tracks:
            if tr["name"] == "nearer":
                add = [dict(n, at=round(n["at"] + 4, 4), vel=round(n["vel"] * 0.7, 3)) for n in tr["notes"] if any(st <= n["at"] < st + 2 for st in srcs)]
                tr["notes"] = sorted(tr["notes"] + add, key=lambda n: n["at"])
    if HEADROOM:
        holes = [(0, 44)] if HEADROOM == "late" else [(19, 26), (29, 36), (38, 45)]
        for tr in tracks:
            if tr["name"] == "orbit":
                tr["notes"] = [n for n in tr["notes"] if not any(a <= n["at"] < b for a, b in holes)]
    if TIDEDRUMS:
        hold = TIDEDRUMS.startswith("hold:")
        dd = float(TIDEDRUMS.split(":")[-1])
        for tr in tracks:
            if tr["name"] in ("drums", "spin"):
                for n in tr["notes"]:
                    a = n["at"]
                    g = dd * (a - 368) / 64 if 368 <= a < 432 else (dd if hold else dd * (464 - a) / 32) if 432 <= a < (500 if hold else 464) else 0.0
                    if g > 0:
                        n["vel"] = round(max(0.05, n["vel"] * (1 - g)), 3)
    if ORBITTIGHT:
        back = 6.0 if ORBITTIGHT == "six" else 3.0
        for tr in tracks:
            if tr["name"] == "orbit":
                fast = [n for n in tr["notes"] if 96 <= n["at"] < 96 + back]
                v1 = fast[0]["vel"] if fast else 0.22
                pre = [dict(n, at=round(n["at"] - back, 4), vel=round(max(0.05, v1 * (0.25 + 0.75 * (n["at"] - 96) / back)), 3)) for n in fast]
                for n in tr["notes"]:
                    if 96 - back <= n["at"] < 96:
                        n["vel"] = round(n["vel"] * (1 - 0.33 * (n["at"] - (96 - back)) / back), 3)
                tr["notes"] = sorted(tr["notes"] + pre, key=lambda n: n["at"])
    if TIDESWELL:
        mode, _, amt = TIDESWELL.partition(":")
        lo = 0.0
        if mode == "recede":
            lo, _, amt = amt.partition(":")
            lo = float(lo)
        amt = float(amt or 0.25)
        names = {"orbit", "orbit-drift", "seed-hi", "seed-lo", "lights", "undertow", "floor", "bass808"} | ({"drums", "spin"} if mode == "all" else set())
        for tr in tracks:
            if tr["name"] not in names:
                continue
            for n in tr["notes"]:
                a = n["at"]
                g = (lo + (amt - lo) * (a - 368) / 64 if 368 <= a < 432 else amt * (464 - a) / 32 if 432 <= a < 464 else 0.0)
                if g != 0:
                    n["vel"] = round(min(1.0, n["vel"] * (1 + g)), 3)
    for spec in [x for x in LATESWAP.split(",") if x]:
        tn, _, rest = spec.partition("=")
        lp, _, lg = rest.partition("@")
        for tr in tracks:
            if tr["name"] == tn:
                tr["patch"] = lp
                if lg:
                    tr["gain"] = f"{lg}dB"
    if CHIPHATS:
        hg, og = CHIPHATS.split(":")
        for tr in tracks:
            if tr["name"] == "drums":
                tr["patch"] = {"extends": "909", "kit": {
                    "h": {"patch": "nes-noise-hat", "pitch": "C7", "gain": f"{hg}dB", "choke": "hat"},
                    "oh": {"patch": "nes-noise-hat amp.d=260ms amp.r=60ms", "pitch": "C6", "gain": f"{og}dB", "choke": "hat"}}}
    if CHIPKIT:
        crash = {"patch": "nes-noise-hat amp.d=1400ms amp.r=300ms", "pitch": "C5", "gain": "-14dB"}
        ck, *crg = CHIPKIT.split(":")
        ride = {"patch": "nes-noise-hat amp.d=700ms amp.r=150ms", "pitch": "C6", "gain": f"{crg[0] if crg else -16}dB"}
        for tr in tracks:
            if tr["name"] == "drums" and ck == "kit":
                pt = tr["patch"] if isinstance(tr["patch"], dict) else {"extends": tr["patch"], "kit": {}}
                pt.setdefault("kit", {})["c"] = crash
                pt["kit"]["rd"] = ride
                tr["patch"] = pt
            if tr["name"] == "spin":
                tr["patch"] = {"extends": "909", "kit": {"rd": ride}}
    if ANSACCRETE:
        third = {57: 60, 55: 59, 64: 67, 62: 66}
        for tr in tracks:
            if tr["name"] == "crest-answer":
                add = []
                for n in tr["notes"]:
                    mm = int(n["pitch"][1:])
                    k = 1 if 353 <= n["at"] < 363 else 2 if 373 <= n["at"] < 383 else 0
                    if not k:
                        continue
                    if ANSACCRETE == "thirds":
                        add.append(dict(n, pitch=f"m{third[mm]}", vel=round(n["vel"] * 0.85, 3)))
                        if k == 2:
                            add.append(dict(n, pitch=f"m{mm - 12}", vel=round(n["vel"] * 0.8, 3)))
                    else:
                        if k == 1:
                            n["pitch"] = f"m{mm + 12}"
                        else:
                            add.append(dict(n, pitch=f"m{mm + 12}", vel=round(n["vel"] * 0.85, 3)))
                tr["notes"] = sorted(tr["notes"] + add, key=lambda n: (n["at"], n["pitch"]))
    if ARRIVED:
        first = {"here": ["HH IY1 R", "IH0 N"], "now": ["N AW1", "IH0 N"]}[ARRIVED]
        for tr in tracks:
            if tr["name"] in ("hums-1", "hums-2", "hums-3"):
                ns = sorted(tr["notes"], key=lambda n: n["at"])
                assert [n["ph"] for n in ns[:2]] == ["N IH1", "R ER0"], [n["ph"] for n in ns[:2]]
                ns[0]["ph"], ns[1]["ph"] = first
    if VOICEDONE:
        for tr in tracks:
            if tr["name"] in ("nearer", "hums-1", "hums-2", "hums-3", "hums-out") and isinstance(tr["patch"], dict):
                add = " synth.layers.0.taper=0.6"
                if VOICEDONE == "choir" and tr["name"] in ("hums-2", "hums-3"):
                    add += " synth.layers.0.vowel_spread=1 synth.layers.0.depth_spread=1 synth.layers.0.cons_spread=1"
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + add)
    if CHORUSTAPER:
        for tr in tracks:
            if tr["name"] == "hums-a" and isinstance(tr["patch"], dict):
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + f" synth.layers.0.taper={CHORUSTAPER}")
    if E1TAPER:
        for tr in tracks:
            if tr["name"] == "hums-e1" and isinstance(tr["patch"], dict):
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + f" synth.layers.0.taper={E1TAPER}")
    if FAREHUM:
        h0 = 464 if FAREHUM == "all" else 466
        for tr in tracks:
            if tr["name"] == "hums-out":
                tr["notes"] = [dict(n, expr=dict(n.get("expr", {}), hum=1.0)) if n["at"] >= h0 else n for n in tr["notes"]]
    if INHALE:
        for tr in tracks:
            if isinstance(tr.get("patch"), dict) and "voice-" in tr["patch"].get("extends", "") and tr["name"] != "breath-quote":
                tr["patch"] = dict(tr["patch"], extends=tr["patch"]["extends"] + f" synth.layers.0.inhale={INHALE}"
                                   + (f" synth.layers.0.inhale_depth={BREATHSIZE}" if BREATHSIZE else ""))
    if WORDSGROW:
        for tr in tracks:
            if tr["name"] == "hums-a":
                for n in tr["notes"]:
                    k = 0 if n["at"] < 130 else (1 if n["at"] < 160 else 2)
                    off = n["at"] - (110, 140, 170)[k]
                    if (k == 0 and off >= 1.0) or (k == 1 and off >= 4.0):
                        n["ph"] = "AH1" if off < 4.75 else n["ph"]
                        n["expr"] = dict(n.get("expr", {}), hum=1.0)
                        if WORDSGROW == "soft" and off < 4.75:
                            n["vel"] = round(n["vel"] * 0.8, 3)
    if GROOVE:
        gr = float(GROOVE)
        ga, gb, ramp = ST["A"], ST["outro"], 16
        for tr in tracks:
            if any("ph" in n for n in tr.get("notes", [])):
                continue
            for n in tr.get("notes", []):
                at = n["at"]
                if not (ga <= at < gb) or abs((at % 0.5) - 0.25) > 1e-6:
                    continue
                w = min(1.0, (at - ga) / ramp, (gb - at) / ramp)
                off = round((gr - 0.5) * 0.5 * w, 4)
                n["at"] = round(at + off, 4)
                n["len"] = round(max(0.05, n["len"] - off), 4)
    if CELLOROOM:
        ra, rb = (float(x) for x in CELLOROOM.split(":"))
        for tr in tracks:
            if tr["name"] in ("bass808", "floor"):
                tr["notes"] = [n for n in tr["notes"] if not (ra <= n["at"] < rb)]
    if TIRES:
        ta, *tw = TIRES.split(":")
        for tr in tracks:
            pt = tr.get("patch")
            if tr["name"] in ("nearer", "hums-e1", "hums-out") and isinstance(pt, dict):
                pt["extends"] += f" synth.layers.0.creak={ta}"
            if tr["name"] == "hums-out" and tw and tw[0] == "sink":
                last = max(tr["notes"], key=lambda n: n["at"])
                last["pitch"] = "D4"
    if VIBBLOOM:
        vb, *vd = VIBBLOOM.split(":")
        for tr in tracks:
            pt = tr.get("patch")
            if isinstance(pt, dict) and "voice-near" in pt.get("extends", "") and "synth.lfo.vib.per_note=true" in pt["extends"]:
                pt["extends"] += f" synth.lfo.vib.bloom={vb}" + (f" synth.pitch.mod.0.amount={vd[0]}" if vd else "")
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
        **({"master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "lowshelf cutoff=110 gain=3dB", "peak cutoff=640 q=1.0 gain=-2.5dB"]
                                + (["peak cutoff=44 q=1.2 gain=2dB", "peak cutoff=114 q=1.0 gain=1.5dB"] if MASTEREQ == "warm2" else [])},
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
