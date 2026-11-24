#!/usr/bin/env python3
"""chirpers10-t5 "False Summit" (chirper-zero): a riff that climbs for four minutes and ends where it began.

Harry, 15 Nov: "true djent, but that leverages audio illusions throughout mainly risers/shpehers but in djent style,
really make it a clear illlusory song, all about the illusions".

A false summit is the top you can see from below that turns out not to be the top. This piece is built on the two
illusions of endless motion, and here the BAND plays them, not a pad behind the band:

  the stair (Shepard)  A line climbs the album's six notes (F, G flat, A flat, B, C, E flat) and goes on climbing, an
                       octave every bar, and is never any higher. It is played by FOUR guitars a side, the same line
                       an octave apart. Each guitar climbs through four octaves and its fader follows where it is:
                       silent at the bottom, full in the middle, silent again at the top, where it drops back to the
                       bottom unheard. So every bar is the same bar, and every bar starts higher than the last.
                       (Three were tried first: a guitar then falls from full to nothing inside one bar and can be
                       followed out; with four, two neighbours are always within 6 dB of each other.)
  the turn (Risset)    Three of those guitars a side chug one bar of the low F at three speeds, each twice the one
                       below, and all three speed up together: each doubles its speed over four bars while the
                       fastest fades out and the slowest fades in. The riff gets faster and faster and is never any
                       faster. The speed rises in a straight line, not a curve, which makes the arithmetic close: in
                       four bars the three play three, six and twelve bars of the riff, so every fourth bar line all
                       three and the kit are together again. The kit keeps four in a bar throughout.

Common Time (track 1) turns three cells under one pulse; Odd Sympathy slides a riff against itself; Plain Hunt rings a
row through every order; Running Total adds a riff up. This piece's long cycle is one that never completes.

  the foot      bars 0-8      the stair alone on a Shepard tone (the plain form of the illusion first); then the guitars.
  the stair     bars 8-32     the band: the low string chugs under the line (F, F, A flat, E flat), the kick on the
                              line's six notes.
  the turn      bars 32-48    the chug at three speeds, speeding up for ever; the kit and the bass hold the bar.
  the descent   bars 48-72    the stair the other way, and all of it: the whole riff a step lower every bar, on the
                              three guitars and two basses. A tuning that keeps dropping and is never lower.
  the pole      bars 72-84    a breath: one chord through a filter that climbs for ever, the line slowly over it, and
                              a bass that is only its overtones (the ear supplies the note).
  both          bars 84-100   pitch and speed rise together, as a tape speeding up does: each guitar climbs an octave
                              as it doubles its speed. A riser that never arrives swells over it, and stops dead.
  the summit    bars 101-105  one bar of nothing. Then the stair's first bars, exactly: the same notes, the same
                              tempo. After all that climbing the band is where it started. One chord.

v1 is the SKELETON (track 2's terms: mine, my title, the whole shape standing, bare).
"""
import json
import math
import os

OUT = os.environ.get("C10T5_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t5.yaml"))
BPM = 100
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# ---------------------------------------------------------------------------------------------------- the material
SCALE = (0, 1, 3, 6, 7, 10)             # the album's notes over the ground: F Gb Ab B C Eb
ACC = (0, 3, 6, 9, 12, 14)              # where the line's six notes fall in the bar (sixteenths): 3 3 3 3 2 2
PEDAL = (0, 0, 3, 10)                   # the low string under the stair, a bar each: F F Ab Eb
PAT = "occoccoc"                        # the turn's bar, in eighths (3 3 2): o = open and accented, c = a muted chug
VOICES = 4                              # the guitars a side that carry the stair, an octave apart
ROLES = 3                               # the speeds of the turn, an octave of speed apart (a fourth guitar rests each cycle)
FLOOR = -70.0
CYCLE = 4                               # bars in which the turn doubles its speed

# ---------------------------------------------------------------------------------------------------- the form (bars)
FOOT = 0
RISE = FOOT + 8
TIME = RISE + 24
FALL = TIME + 4 * CYCLE
POLE = FALL + 24
BOTH = POLE + 12
STOP = BOTH + 4 * CYCLE
HOME = STOP + 1
END = HOME + 4
NB = END + 3
assert (RISE - FOOT) % 4 == 0 and (TIME - RISE) % len(PEDAL) == 0 and (FALL - TIME) % CYCLE == 0 and (STOP - BOTH) % CYCLE == 0

# the guitars' register: four octaves from the low string up, so the bell is fullest two octaves over it (F3)
LINE_BASE = int(os.environ.get("C10T5_LINEBASE", str(F1)))
RIFF_BASE = F1
# each illusion's trim on the three guitars' faders, dB: the line ; the turn ; the descent ; both
TRIM = dict(zip(("line", "time", "fall", "both"), (float(x) for x in os.environ.get("C10T5_TRIM", "1;3;1.5;3").split(";"))))
# v2: THE ILLUSIONS HOLD, AND THE JOINS ARE RISERS (whole song).
# ONE CABINET A SIDE. chirp-eco's new `tools/endless.py` read v1: inside a bar the stair holds (no saw-tooth), but the
# eight guitars did not repeat every bar, they repeated every FOUR (+0.3 -0.8 -0.2 +0.7 dB by bar; 6 dB of movement
# at 60-120 Hz), and in the turn the third and fourth cycles were 1.6 to 2 dB over the first two. Each of the eight had
# its own speaker cone and its own place in the stereo, so WHICH speaker held WHICH octave came round every four bars:
# a cycle the ear could count. Now the four on a side share one cone and one place: a bar is the same bar.
# the pan of the four a side. "" = v1 (a cone and a pan each).
ONE = os.environ.get("C10T5_ONE", "0.7")
# THE JOINS ARE RISERS, ON THE GUITARS. Harry asked for "mainly risers/shpehers but in djent style". The song's
# sections now hand over on a RUN: the eight guitars pick a semitone to the sixteenth on the same bell, so the run
# climbs four thirds of an octave a bar and is never higher (falling, at the end of the descent). Two bars each: into
# the turn (bars 30-32, rising), out of the descent (70-72, falling), and out of the pole into both (82-84, rising,
# with the riser that never arrives). Under the two rising ones the snare doubles its speed into the bar line.
# bars of run at a join ; the eight guitars' trim in it, dB ; the snare's gain in its build, dB. "" = v1 (a tom fill).
RUNS = os.environ.get("C10T5_RUNS", "2;0;-3")
# THE KIT PLAYS ONE TOO. In the pole (the breath) the hat's quarters become a tick that speeds up for ever: the
# engine's own `risset` on a kit track (three copies an octave of speed apart, each doubling in four bars; it works
# there because a drum has no amp to flatten the copies' fades). The plain form of the turn, heard alone.
# the tick's gain ; its accent's and its other strokes' velocity ; bars to double its speed. "" = v1 (hat quarters).
TICK = os.environ.get("C10T5_TICK", "22dB;0.9;0.6;4")
# v15: the pole's hat first appears going the OTHER way in the descent.
# Give the falling riff two bars to establish the beat; leave its last two to
# the toms. At the pole the same three taps accelerate. 3 dB below the pole
# hat: at its full setting the descent gained 5.2 dB at 8–16 kHz (mono).
# Empty = v14, including the china pattern.
BRAKE = os.environ.get("C10T5_BRAKE", "19dB") if TICK else ""
BRAKE_IN, BRAKE_OUT = FALL + 2, POLE - 2
# THE FIRST READ AGAINST THE RECORDS, BY PART (v1, `stembal --id`), and what it moved:
#   the stair was 3.7 dB over the eleven records at 250-500 Hz, and the Shepard tone held 57% of that band: it comes
#     down 2.5 dB under the band (and is as it was where it is alone); and 2.3 dB short at 60-120 Hz: the bass 1.5 dB up.
#   the turn was 2.9 dB short at 60-120 Hz and 2.8 over at 120-250: the bass held ONE LONG NOTE a bar there, and a long
#     note of this bass is all 120-250 Hz (alone: 60-120 Hz 7.3 dB under its total, 120-250 Hz 2.3 under; chugged it is
#     3.6 and 6.4). It now strikes every beat (in both, too): four in a bar with the kit, against the guitars' turn.
#   the descent was 2.4 dB over at 120-500 Hz, part of it the falling rumble: 2 dB off it.
# strokes of the bass to the bar in the turn and in both ("" = v1: one long note).
ANCHOR = os.environ.get("C10T5_ANCHOR", "4")
# v3: THE STAIR HAS A TUNE (whole song). The line was the scale, straight up: the plain form, and right for the first
# eight bars. But a scale is not a tune, and the band played it for twenty-two bars. From bar 16 the line is a FIGURE:
# up two steps of the scale, back one, up two, back one (F A-flat G-flat B A-flat C | B E-flat C F E-flat G-flat), six
# notes on the bar's 3 3 3 3 2 2 as before, each bar starting three steps above the last. So it is a two-bar tune that
# ends an octave above where it began and begins again there: it climbs an octave every two bars and is never higher.
# The same eight guitars on the same bell play it; the kit takes the backbeat where it comes in (it was at bar 20).
# the bar the figure starts ; its six notes, in steps of the scale over the bar's first ; steps a bar climbs. "" = v2.
FIGURE = os.environ.get("C10T5_FIGURE", "16;0,2,1,3,2,4;3")
# THE EIGHT GUITARS' OWN REGISTER. Read against the eleven records by part (v2), the stair stood 3.7 dB over them at
# 500 Hz-1 kHz and the eight guitars held 58% of that band (both: 2.8 over). One eq band on each of the eight.
# frequency : q : dB. "" = v2.
VEQ = os.environ.get("C10T5_VEQ", "700:1:-2.5")
# v13: THE EIGHT GUITARS ALONE (whole-song round: the song read again stretch by stretch against the records).
# That band was cut at 700 Hz when the stair stood 3.7 dB over the records there, with the low-string guitars and
# the plain tone both playing under the eight. Since then the tone has left the band (v11), and for more than half
# the song (the turn, the descent, the first half of "both") the eight are the ONLY guitars. There the cut left a
# hole where it had been trimming a pile: 500 Hz-1 kHz read 1.8 to 2.4 dB UNDER the records and 250-500 Hz 2.4 to
# 2.7 over: a boxy, hollow band exactly where the song's illusions are. Now the band of the eq MOVES while the eight
# are alone: the same 2.5 dB cut, an octave lower. It stands still within each illusion (it steps only at a seam
# between sections), so nothing follows the stair.
# the bars the eight are the only guitars, from:to ; the band's frequency there. "" = v12.
ALONE = os.environ.get("C10T5_ALONE", "32:92;350") if VEQ else ""
# v4: THE LEAD COMES DOWN (section round, 0:57-1:12: the stair's last six bars before the run; the map called the
# stretch static, and from the band's entry at 0:19 to the turn at 1:16 nothing JOINED). A lead guitar comes in over
# the tune and does the one thing nothing else in this song does: it really moves. It comes DOWN the scale, a note to
# the half bar, two octaves in six bars (F5 to F3), and lands on the low F exactly where the guitars' run begins. In
# those six bars the tune under it climbs three octaves and is no higher; the lead falls two and is two octaves lower.
# So the one honest line in the song shows the stair up for what it is. It is the library's `lead-tape` (the
# sustaining 8-string into a dark tape echo and a wide hall), on no other track of the album.
# the patch ; its gain ; the bar it starts ; its top note (MIDI) ; the eight guitars under it, dB. "" = v3.
# (At the patch's first gain, -16 dB, it read 23 dB under the mix: not there. 14 dB went on at the bench.)
LEAD = os.environ.get("C10T5_LEAD", "lead-tape;-2dB;24;77;-1")
# v5: THE FILL THAT NEVER LANDS (palette round). The kit had one illusion (the tick) and the descent had none of the
# kit's: for a minute the drums kept a plain beat under it. Every drummer's fill goes round the toms from the high one
# to the floor tom and stops there, because the kit has no lower drum. This song now has a set of toms that has: a new
# instrument, `fs-tom` (the kit's own tom, a struck head, made a pitched part), struck three at a time an octave apart
# under the same bell as the guitars, so a fill can go on down for as long as it likes and the drum under the sticks
# is never lower. The descent ends each of its octaves on one: eight strokes into bar 54, twelve into 60, a whole bar
# into 66, each a step of the scale to the sixteenth and each landing on the riff's F; and under the guitars' falling
# run (bars 70-72) the toms fall with it, a semitone to the sixteenth for two bars, thirty-two drums down and no
# lower. The china and the snare stop for each (the drummer's hands are on the toms); the kick keeps the riff. The
# fill into the descent (bar 47) is still the kit's four real toms, high to low to the snare: the one that lands.
# the patch ; its gain ; the fills' lengths in sixteenths, at the descent's octaves ; its pan ; its head's ring, s. "" = v4.
# (At 0 dB the new toms were the loudest thing in their bars by 4 dB, -3.3 by presence where the kit's real toms read
# -7.4 in their fill; 6.5 dB came off at the bench, in two goes: the drum bus's compressor gives back half of a cut.)
TOMS = os.environ.get("C10T5_TOMS", "fs-tom;-6.5dB;8,12,16;0.2;0.9")
TOM_BASE = F1                           # three octaves of drums from here; the bell is fullest at B2 (123 Hz)
# v6: THE RISER IS A GUITAR (palette round). The song's last climb (both: pitch and speed rising together) swelled into
# the stop on the one thing in the song that was not played: a library riser effect, a synth. Harry asked for "risers
# / shepards but in djent style". Now the riser is the LEAD GUITAR, three of them an octave apart under the bell, and
# what it plays is the song's own stair, getting steeper: for four bars the stair's TUNE (an octave every two bars),
# for two the plain SCALE (an octave a bar), for two the RUN (a semitone to the sixteenth, four thirds of an octave a
# bar), and then the stop. It climbs eight and a half octaves in eight bars and ends where it began. At 0:57 the
# lead was the one honest line in the song, the one that really came down; at the end it has caught the illusion too.
# The synth riser stays under it, lower, for its noise (swap or layer was measured: see sounds.md).
# the patch ; its gain ; the bars before the stop it starts ; its lowest note (MIDI) ; the synth riser under it, dB
# ("off": none). "" = v5.
# (First levels, lead -2 dB and the synth 3 dB down: in the last four bars the synth still read as loud as the three
# leads together, -10.0 by presence to their -12.5 to -14.4 each, and held 500 Hz-1 kHz 1.5 dB under the WHOLE mix
# as it had in v5. So the lead went up 2 dB and the synth down to -8.)
CLIMB = os.environ.get("C10T5_CLIMB", "lead-tape;0dB;8;53;-8")
# v7: THE TURN, HEARD NAKED (section round, 1:26-1:55, the turn's second half: the map called it static, and it was:
# four cycles of the same thing, the kit and the bass holding the bar under all of them). The turn is the hardest of
# the song's illusions to hear, because the thing that speeds up for ever is under a snare, a china and a bass that
# do not. Now it has a shape: two cycles with the kit holding the bar, as before (the ear gets the bar); then for the
# THIRD cycle the snare, the china and the bass stop on a crash and the chug is alone with its kick, speeding up, for
# four bars (the illusion with nothing in front of it); then the kit comes back for the last cycle harder than it
# left: the snare on the backbeat, the china in eighths, into the fill and the descent.
# the cycle (from 0) heard naked ; `lift`: the cycle after it has the backbeat and the china in eighths. "" = v6.
NAKED = os.environ.get("C10T5_NAKED", "2;lift")
# v8: THE STAIR IN HARMONY (section round, 0:28-0:57: the map called it static, nothing enters in it; the tune is
# stated four times alike before the lead comes). The stair's tune is on four guitars a side, the two sides in
# unison. From its third statement (bar 20, 0:48) the RIGHT side takes the tune two steps of the scale higher: a third
# or a fourth over the left on every note (F with A flat, G flat with B, A flat with C, B with E flat, C with F,
# E flat with G flat): the twin-guitar harmony of every metal record, except that both lines are stairs. Each side
# is still four guitars an octave apart under its own bell, so each still climbs an octave every two bars and is
# never higher, and the two stay a third apart for ever. It holds under the lead (bar 24) until the run (bar 30).
# So the stair now gathers every four bars: the tune (16), its harmony (20), the lead coming down through both (24),
# the run (30).
# the bar the right side leaves the unison ; the bar it comes back (the run) ; the steps of the scale it is above. "" = v7.
HARM = os.environ.get("C10T5_HARM", "20;30;2")
# v9: THE FALL GETS STEEPER (section round, 2:24-2:52: the descent's second half, which the map called "little new"
# against its first: twenty-two bars of the riff a step of the scale lower every bar). Now the descent falls faster
# and faster and is still never lower. Its first half is as it was, a step a bar (an octave in six bars). From bar
# 60 (2:24) it falls TWO steps a bar (an octave in three bars); from bar 66 (2:38) THREE (an octave in two); and for
# its last two bars (68-70, 2:43) SIX, a step on every one of the riff's accents: the riff has become the scale, an
# octave a bar, on the stair's own rhythm: the stair of the song's first minute, upside down. Then the run, a semitone
# on every sixteenth, as before; and the fall now reaches the run on F, the note the run starts from. The steps
# change on the riff's accents (never on a muted chug). Each of the first two changes of speed comes out of one of
# the tom fills that never land (into 2:24 and into 2:38): the fill is the gear change. So the song's two long
# illusions now answer each other: the stair gathers (tune, harmony, lead, run) and the descent steepens.
# (First cut: two steps a bar, then four, a step on every beat. The step at mid-bar fell on a muted chug, and the
# fall reached the run on A flat.)
# bar:steps a bar (1, 2, 3 or 6), from that bar on. "" = v8 (a step a bar throughout).
STEEP = os.environ.get("C10T5_STEEP", "60:2,66:3,68:6")
# v10: THE SEAM IN THE FALL (found by chirp-eco's endless.py --cycles, 16 Nov: over fourteen cycles, two seeds and
# all four speeds, the SECOND step of every octave of the descent, the E flat, was 0.28 octaves brighter and 0.7 dB
# quieter than its cycle: once an octave the fall could be read coming round). The cause was mine: the bass's eq
# follows the ground (since v1: a notch on the fundamental, a lift on its octave), and in the fall I gave it the step's
# pitch class, 0 to 11 over F. So from F to E flat the eq leapt UP ten semitones while the basses went down two:
# its notch landed on the fundamental of the bass that carries that step, and its lift on nothing. An illusion of
# endless descent wants the opposite: a tone that does not move while the notes pass through it.
# "0": the eq stands still on F through the fall; "wrap": it follows, but leaps where the two basses are equal
# (the step's pitch class less an octave when over a tritone, as `pedal()` always did); "" = v9.
FALLKEY = os.environ.get("C10T5_FALLKEY", "0")
# AND THE KIT STEEPENS WITH THE FALL. Under v9's fall, which goes six times faster by its end, the kit played one
# beat from end to end: the snare on three, the china on the quarters. Now it changes gear where the fall does:
# to bar 60 as it was (half time); from 60, where the fall takes two steps a bar, the backbeat (two and four);
# from 66 (three steps) the china in eighths as well; from 68 (six steps, an octave a bar) the snare on every beat;
# and then the run's own roll, eighths and then sixteenths, as before. One, two, four, eight, sixteen snares a bar:
# the whole second half of the descent is one acceleration into the turn. A crash marks each change of gear.
# "1" = on; "" = v9's one beat.
KITFALL = os.environ.get("C10T5_KITFALL", "1") if STEEP == "60:2,66:3,68:6" else ""
# v23 (section w3, 0:57-1:26): THE FILL THAT NEVER TOPS OUT. At 0:57 a lead guitar comes down the scale over the
# stair, two octaves in six bars: the one honest line in the song (v4), there to show the stair up. The descent has
# the kit's own illusion, the fill that never lands (v5): the toms go down the scale for as long as they like and are
# never lower, one fill at each octave the riff falls. The stair had none of the kit's: for 53 seconds the drums keep
# a plain beat under it. Now the same toms answer the lead at ITS octaves. Into 0:57.6, where the lead enters on its
# top F, and into 1:04.8, where it has really come down one octave, the drummer goes UP the toms, a step of the scale
# to the sixteenth (eight strokes, then twelve), two or three drums an octave apart under the bell, each arriving on
# the F the lead is on: a fill that climbs for as long as it likes and is never higher. So each time the honest line
# has fallen an octave the kit claims to have risen one, and at the lead's third octave (1:12) the guitars' run takes
# over, as before. The snare and the china rest under each fill (the hands are on the toms); the kick keeps the line.
# The stair's fills go up where the descent's go down; the run, its snare and everything Harry has heard are as they
# were.
# And each fill lands on a crash, as the descent's do: the crash at the lead's entry is struck as a landing, and the
# next one moves from the four-bar line (1:07.2) to the lead's octave (1:04.8). Under the lead the kit now phrases in
# threes, the honest line's time.
# (Raw, seed 0: the toms stand 6.4 and 6.5 dB under the mix in these fills, K-weighted; in the descent's they stand
# 6.1 to 6.2. The lead under the second fill is where it was against the mix, -10.4 for -10.5. A fill adds 2.4 to
# 3.2 dB at 120-500 Hz and takes 9.5 to 11 dB off 8-16 kHz while the china rests. The crash is a quiet mark: the
# new one adds 0.26 dB at 8-16 kHz over its two beats. A third fill into the run, `8,12,16`, was benched and left
# out: the run is the stair's third and largest fill already, the lead's last two notes are in the toms' register,
# and Harry heard the run as it is: "A lift: keep it".)
# the fills' lengths in sixteenths, at the lead's octaves (0: none there) ; `land`: the crashes follow the lead's
# octaves. "" = v22 (read in compose(), where it defaults on only if every later switch is on).
TOMRISE_DEFAULT = "8,12;land"
# v24 (chirper-one; section w2, 0:28.8-0:57.6, which the map calls static: "the same kit beat from 0:38 to 0:56"):
# THE KIT CLIMBS AN OCTAVE OF SPEED. The stair is the illusion in pitch, and an octave of pitch is a doubling. Under
# it the kit has always changed gear once: half time while the line is the plain scale (0:19, the snare on three),
# the backbeat when the tune comes in (0:38, the snare on two and four). Then nothing for eight bars, while the tune
# is said four times and the right side goes up into harmony. Now, where the harmony comes in (0:48), the backbeat
# doubles again: the snare on the "and" of every beat, twice as many as before, over the same riff at the same
# tempo. So the drummer says the stair's own claim in time, a doubling at each stage of the tune (half time, time,
# double time), and the band seems to have picked up speed twice without moving. Four bars; the china's eighths and
# the kick (on the line's six notes) do not change, so two of the four new strokes in a bar fall WITH the line (its
# third and sixth notes) and two between. The rising fill at 0:56.4 (v23) takes the last half bar as before, and
# at 0:57.6, where the one honest line comes in and starts to fall, the kit drops back to the plain backbeat: the
# false summit, in the drums.
# the bars in double time (from:to) ; the snare's velocity there (the backbeat's is 0.95). "" = v23 (read in
# compose(), where it defaults on only while the rising fills are as v23 left them and every older switch is on).
DOUBLE_DEFAULT = "20:24;0.92"
RLANE = {v: [] for v in range(VOICES)}                  # the right side's faders while it is in harmony
LLANE = {v: [(0.0, FLOOR)] for v in range(3)}           # the three leads' faders
LANE = {v: [(0.0, FLOOR)] for v in range(VOICES)}       # each voice's fader, (beat, dB)
BLANE = {w: [(0.0, FLOOR)] for w in range(2)}           # the descent's two basses
KEY = [(0.0, 0)]                                        # the ground under the bass's eq, (beat, semitones over F)


def bell(x):
    """A voice's level (amplitude) at x in 0..1 of its way from the bottom to the top: nothing at either end. Three
    voices a third of the way apart always add up to the same power."""
    return 0.5 - 0.5 * math.cos(2 * math.pi * (x % 1.0))


def db(a):
    return max(FLOOR, 20 * math.log10(a)) if a > 0 else FLOOR


def step(lane, beat, level):
    """The fader jumps to `level` at `beat`."""
    t, last = lane[-1]
    level = round(level, 2)
    if level == last:
        return
    if beat - 0.01 > t:
        lane.append((round(beat - 0.01, 4), last))
    lane.append((round(beat, 4), level))


def lane_at(lane, beat):
    """The fader's level at `beat`."""
    lv = lane[0][1]
    for t, x in lane:
        if t > beat:
            break
        lv = x
    return lv


def right_lane(v):
    """The right side's fader: the left's, but its own while it is in harmony."""
    if not (HARM and RLANE[v]):
        return LANE[v]
    a, z = RLANE[v][0][0], int(HARM.split(";")[1]) * 4.0
    return ([q for q in LANE[v] if q[0] < a] + RLANE[v] + [(round(z - 0.01, 4), RLANE[v][-1][1]), (z, lane_at(LANE[v], z))]
            + [q for q in LANE[v] if q[0] > z])


def ramp(lane, beat, level):
    """The fader moves in a straight line to `level` at `beat`."""
    if beat > lane[-1][0]:
        lane.append((round(beat, 4), round(level, 2)))


def addb(tr, beat, beats, pitch, vel, gain=None, **expr):
    n = {"at": round(beat, 4), "len": round(beats * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if gain is not None:
        n["gain"] = f"{gain:.1f}dB"
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def add(tr, s16, len16, pitch, vel, **expr):
    addb(tr, s16 / 4, len16 / 4, pitch, vel, **expr)


def vadd(v, beat, beats, pitch, vel, **expr):
    for side in "lr":
        addb(f"v{v}{side}", beat, beats, pitch, vel, **expr)


def drum(piece, s16, vel, gain=None):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym"}.get(piece, "toms")
    n = {"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece == "h" else 0.25, "pitch": piece, "vel": round(vel, 3)}
    if gain is not None:
        n["gain"] = f"{gain:.1f}dB"
    T.setdefault(tr, []).append(n)


def ground(beat, semis):
    if KEY[-1][1] != semis:
        KEY.append((beat, semis))


# ---------------------------------------------------------------------------------------------------- the illusions
def line(b0, b1, gtrs=True, synth=True, slow=1, rot=None):
    """THE STAIR. The six notes climbing, an octave a bar (`slow` 2: half an octave a bar), on the Shepard tone and on
    the three guitars a side. Guitar v is in octave (v + bar) mod 3 of its three, and its fader is the bell there."""
    n, rot = 0, b0 if rot is None else rot
    fig = [int(x) for x in FIGURE.split(";")[1].split(",")] if FIGURE and slow == 1 and gtrs and b0 == RISE else None
    for b in range(b0, b1):
        acc = ACC if slow == 1 else (0, 6, 12)
        for i, a in enumerate(acc):
            d = n                                  # the step of the scale: straight up
            if fig and b >= int(FIGURE.split(";")[0]):   # v3: the figure, from the octave the scale had reached
                bf = int(FIGURE.split(";")[0])
                d = 6 * (bf - b0) + int(FIGURE.split(";")[2]) * (b - bf) + fig[i]
            k, octave = d % 6, d // 6
            n16 = (acc[i + 1] if i + 1 < len(acc) else 16) - a
            t = b * 16 + a
            if synth:
                add("stair", t, n16, 65 + SCALE[k], 0.85 if k else 1.0)
            harm = bool(HARM) and gtrs and b0 == RISE and int(HARM.split(";")[0]) <= b < int(HARM.split(";")[1])
            for v in range(VOICES if gtrs else 0):
                p = 12 * ((v + octave + rot) % VOICES) + SCALE[k]
                g = db(bell(p / (12 * VOICES))) + TRIM["line"]
                dip = float(LEAD.split(";")[4]) if LEAD and b0 == RISE and b >= int(LEAD.split(";")[2]) else 0.0
                if harm:                 # v8: the right side plays the same line some steps of the scale higher, under its own bell
                    dr = d + int(HARM.split(";")[2])
                    pr = 12 * ((v + dr // 6 + rot) % VOICES) + SCALE[dr % 6]
                    gr = db(bell(pr / (12 * VOICES))) + TRIM["line"]
                    if not RLANE[v]:
                        RLANE[v].append((round(t / 4 - 0.02, 4), lane_at(LANE[v], t / 4 - 0.02)))
                    if gr > -45:
                        step(RLANE[v], t / 4, gr + dip)
                        addb(f"v{v}r", t / 4, n16 / 4, LINE_BASE + pr, 0.95)
                    if g > -45:
                        step(LANE[v], t / 4, g + dip)
                        addb(f"v{v}l", t / 4, n16 / 4, LINE_BASE + p, 0.95)
                    continue
                if g <= -45:
                    continue
                if LEAD and b0 == RISE and b >= int(LEAD.split(";")[2]):      # v4: the eight sit back a little under the lead
                    g += float(LEAD.split(";")[4])
                step(LANE[v], t / 4, g)
                vadd(v, t / 4, n16 / 4, LINE_BASE + p, 0.95)
            n += 1


def run(b0, b1, down=False, synth=True):
    """THE RISER, ON GUITARS. A semitone to the sixteenth on the eight guitars' bell (and on the Shepard tone)."""
    for n in range((b1 - b0) * 16):
        t, s = b0 * 16 + n, -n if down else n
        if synth:
            add("stair", t, 1, 65 + s % 12, 0.8)
        for v in range(VOICES):
            p = (s + 12 * v) % (12 * VOICES)
            g = db(bell(p / (12 * VOICES))) + float(RUNS.split(";")[1])
            if g <= -45:
                continue
            step(LANE[v], t / 4, g)
            vadd(v, t / 4, 0.25, LINE_BASE + p, 0.95)


def build(b0, b1):
    """The snare doubles its speed into the bar line (eighths, then sixteenths in the last bar), getting louder."""
    nb = b1 - b0
    for i, b in enumerate(range(b0, b1)):
        for p in range(0, 16, 2 if i < nb - 1 else 1):
            drum("s", b * 16 + p, 0.45 + 0.5 * (i * 16 + p) / (nb * 16), gain=float(RUNS.split(";")[2]))


def pedal(b0, b1, kick=True):
    """The low string under the stair: a chug on every sixteenth, open where the line's notes fall, the bass with it
    and the kick on the line's notes."""
    for b in range(b0, b1):
        root = PEDAL[(b - b0) % len(PEDAL)]
        ground(b * 4, root - 12 if root > 6 else root)
        for i in range(16):
            o = i in ACC
            for tr in ("gl", "gr"):
                add(tr, b * 16 + i, 1, F1 + root, 1.0 if o else 0.86, **({} if o else {"pm": 1}))
            add("bass", b * 16 + i, 1, F1 + (root - 12 if root > 6 else root), 0.95 if o else 0.82)
            if o and kick:
                drum("k", b * 16 + i, 0.95)


def descent(b0, b1, gend=None):
    """THE STAIR, DOWNWARDS, AND ALL OF IT. The whole riff (the stair's rhythm, chugged) a step of the scale lower
    every bar, on the three guitars a side over three octaves and on two basses over two."""
    rates = sorted((int(x.split(":")[0]), int(x.split(":")[1])) for x in STEEP.split(",")) if STEEP else []
    n = 0
    for b in range(b0, b1):
        per = ([1] + [r for bar, r in rates if bar <= b])[-1]      # v9: the steps of the scale this bar falls
        edges = [ACC[q * len(ACC) // per] for q in range(per)] + [16]      # the steps change on the riff's accents
        for q in range(per):
            s0, s1 = edges[q], edges[q + 1]
            lad = 12 * (n // 6) + SCALE[n % 6]
            pc = lad % 12
            ground(b * 4 + s0 / 4, 0 if FALLKEY == "0" else pc - 12 if FALLKEY == "wrap" and pc > 6 else pc)
            if FALLTONE:                       # v28: the tone says the step, held (the Shepard patch has no octave to fall out of)
                add("stair", b * 16 + s0, s1 - s0, 65 + SCALE[n % 6], 0.85 if n % 6 else 1.0)
            for v in range(VOICES):
                p = (lad + 12 * v) % (12 * VOICES)
                g = db(bell(p / (12 * VOICES))) + TRIM["fall"]
                if g <= -45 or (gend is not None and b >= gend):       # from `gend` the guitars are on the run
                    continue
                step(LANE[v], b * 4 + s0 / 4, g)
                for i in range(s0, s1):
                    o = i in ACC
                    vadd(v, b * 4 + i / 4, 0.25, RIFF_BASE + p, 1.0 if o else 0.86, **({} if o else {"pm": 1}))
            for w in range(2):
                p = (lad + 12 * w) % 24
                a = math.sin(math.pi * p / 24)
                if db(a) <= -45:
                    continue
                step(BLANE[w], b * 4 + s0 / 4, db(a))
                for i in range(s0, s1):
                    addb(f"bs{w}", b * 4 + i / 4, 0.25, RIFF_BASE + p, 0.95 if i in ACC else 0.82)
            n -= 1
        for a in ACC:
            drum("k", b * 16 + a, 0.95)


def climb(b0, b1):
    """THE RISER, ON THE LEAD: the stair's three forms, each steeper than the last (half the bars on the tune, a
    quarter on the scale, a quarter on the run), on three leads an octave apart under the bell; all three faders
    shut at b1, so nothing of it rings into the stop."""
    fig = [int(x) for x in FIGURE.split(";")[1].split(",")] if FIGURE else list(range(6))
    up = int(FIGURE.split(";")[2]) if FIGURE else 6
    nb = b1 - b0
    na, ns = nb // 2, nb // 4
    notes = []                                         # (sixteenth, sixteenths long, semitones climbed)
    for i in range(na + ns):
        for j, a in enumerate(ACC):
            d = up * i + fig[j] if i < na else up * na + 6 * (i - na) + j
            notes.append(((b0 + i) * 16 + a, (ACC[j + 1] if j + 1 < len(ACC) else 16) - a, 12 * (d // 6) + SCALE[d % 6]))
    d = up * na + 6 * ns
    h0 = 12 * (d // 6) + SCALE[d % 6]
    for n in range((nb - na - ns) * 16):
        notes.append(((b0 + na + ns) * 16 + n, 1, h0 + n))
    base = int(CLIMB.split(";")[3])
    for t, ln, h in notes:
        for v in range(3):
            p = (h + 12 * v) % 36
            g = db(bell(p / 36))
            if g <= -45:
                continue
            step(LLANE[v], t / 4, g)
            addb(f"ld{v}", t / 4, ln / 4, base + p, 0.9)
    for v in range(3):
        step(LLANE[v], b1 * 4, FLOOR)


# v12: THE POLE'S LINE IS ON GUITARS (palette round: the swap). The quiet middle of the song (2:53-3:19) is one chord
# through a filter that climbs for ever, and over it the stair's line, slowly: and that line was on the Shepard TONE,
# the one synthesiser in a song whose first sentence says the band plays the illusions. v6 took the riser from a
# synth and gave it to three lead guitars; v11 took the tone out from under the stair. This is the last place it
# carried anything: read alone it was the loudest part there with the chord and held the band from 250 Hz to 1 kHz.
# Now the slow line is on the same THREE LEAD GUITARS, an octave apart, each fading in at the bottom and out at the
# top as it climbs (the stair's own way), half an octave a bar: an endless climb sung by three guitars over the
# turning chord. The tone now does one thing only: it states the illusion, alone, for the song's first ten seconds.
# (First bench at -4 dB: the three leads together read about a dB under where the tone had been, and under the chord;
# the line is the pole's tune, so 1.5 dB up.)
# the leads' level in the pole against their level in the climb, dB. "" = v11 (the tone).
POLELEAD = os.environ.get("C10T5_POLELEAD", "-2.5") if CLIMB else ""


def slow_leads(b0, b1):
    """The stair's line at half speed (three notes a bar) on the three leads under the bell; the faders shut at b1."""
    base, trim, n = int(CLIMB.split(";")[3]), float(POLELEAD), 0
    for b in range(b0, b1):
        for i, a in enumerate((0, 6, 12)):
            h = 12 * (n // 6) + SCALE[n % 6]
            for v in range(3):
                p = (h + 12 * v) % 36
                g = db(bell(p / 36)) + trim
                if g <= -45:
                    continue
                step(LLANE[v], (b * 16 + a) / 4, g)
                addb(f"ld{v}", (b * 16 + a) / 4, ((6, 12, 16)[i] - a) / 4, base + p, 0.9)
            n += 1
    for v in range(3):
        step(LLANE[v], b1 * 4, FLOOR)


def tomfall(s0, n16, scale):
    """THE FILL THAT NEVER LANDS: `n16` sixteenths of toms from sixteenth `s0`, each stroke three drums an octave apart
    under the bell. `scale`: a step of the scale down a stroke, so that the stroke after the last would be F (the bar
    line's note); otherwise a semitone down a stroke from F, with the guitars' falling run. The snare and the china
    rest under it."""
    for i in range(n16):
        k = n16 - i
        semis = 12 * (k // 6) + SCALE[k % 6] if scale else -i
        vel = 0.72 + 0.2 * i / max(1, n16 - 1) + (0.06 if i % 4 == 0 else 0)
        for v in range(3):
            p = (semis + 12 * v) % 36
            g = db(bell(p / 36))
            if g > -45:
                addb("falls", (s0 + i) / 4, 0.25, TOM_BASE + p, min(1.0, vel), gain=g)
    for tr, pieces in (("snare", ("s",)), ("cym", ("x",))):
        T[tr] = [n for n in T.get(tr, []) if not (n["pitch"] in pieces and s0 <= round(n["at"] * 4) < s0 + n16)]


def turn(b0, b1, pitched=False):
    """THE TURN. The bar `PAT` at three speeds an octave of speed apart, all three speeding up in a straight line so
    that each doubles in CYCLE bars: guitar v plays role (v + cycle) mod 3 (x0.5 -> x1, x1 -> x2, x2 -> x4) and its
    fader is the bell over the three. In a cycle the roles play 3, 6 and 12 bars of the riff, so every cycle starts
    with all three, and the kit, on the bar line. `pitched`: each guitar also climbs an octave of the scale as it
    doubles its speed (a tape speeding up); otherwise all three stay on the low F."""
    tc, L = CYCLE * 4.0, len(PAT) * 0.5
    which = "both" if pitched else "time"
    for c in range((b1 - b0) // CYCLE):
        c0 = b0 * 4 + c * tc
        for v in range(VOICES):
            j = (v + c) % VOICES
            if j >= ROLES:                       # this guitar rests this cycle: it has left at the top and comes back in at the bottom
                step(LANE[v], c0, FLOOR)
                continue
            scale = 2 ** (j - 1) * tc
            step(LANE[v], c0, db(bell(j / ROLES)) + TRIM[which])
            for s in range(1, 17):
                ramp(LANE[v], c0 + s / 16 * tc - (0.011 if s == 16 else 0), db(bell((j + s / 16) / ROLES)) + TRIM[which])
            pats = 1.5 * scale / L
            assert abs(pats - round(pats)) < 1e-9, "the cycle must hold whole bars of the riff at every speed"
            for m in range(int(round(pats))):
                for i, tok in enumerate(PAT):
                    q = m * L + i * 0.5
                    u = -1 + math.sqrt(1 + 2 * q / scale)
                    r = 2 ** (j - 1) * (1 + u)
                    g = db(bell((j + u) / ROLES))
                    if g <= -45:
                        continue
                    p = 12 * j + SCALE[min(5, int(6 * u))] if pitched else 0
                    vadd(v, c0 + u * tc, 0.5 / r, RIFF_BASE + p, 1.0 if tok == "o" else 0.86, **({} if tok == "o" else {"pm": 1}))
                    if tok == "o":
                        drum("k", (c0 + u * tc) * 4, 0.95, gain=g)


def anchor(b):
    """The bass under the turn: it keeps the bar while the guitars leave it."""
    if not ANCHOR:
        add("bass", b * 16, 14, F1, 0.95)
        return
    n = int(ANCHOR)
    for i in range(n):
        add("bass", b * 16 + i * 16 // n, 16 // n, F1, 0.95 if i == 0 else 0.85)


def tomrise(s0, n16):
    """THE FILL THAT NEVER TOPS OUT: tomfall's mirror. `n16` sixteenths of toms from sixteenth `s0`, a step of the
    scale UP a stroke, so that the stroke after the last would be F (the bar line's note). The snare and the china
    rest under it."""
    for i in range(n16):
        k = i - n16
        semis = 12 * (k // 6) + SCALE[k % 6]
        vel = 0.72 + 0.2 * i / max(1, n16 - 1) + (0.06 if i % 4 == 0 else 0)
        for v in range(3):
            p = (semis + 12 * v) % 36
            g = db(bell(p / 36))
            if g > -45:
                addb("falls", (s0 + i) / 4, 0.25, TOM_BASE + p, min(1.0, vel), gain=g)
    for tr, pieces in (("snare", ("s",)), ("cym", ("x",))):
        T[tr] = [n for n in T.get(tr, []) if not (n["pitch"] in pieces and s0 <= round(n["at"] * 4) < s0 + n16)]


def beat(b0, b1, snare=(8,), cym="x", stepc=4, vel=0.5, crash=4):
    """The kit keeps four in a bar: the snare on the sixteenths `snare`, a cymbal every `stepc` sixteenths, a crash
    every `crash` bars."""
    for b in range(b0, b1):
        for p in snare:
            drum("s", b * 16 + p, 0.95)
        if cym:
            for p in range(0, 16, stepc):
                drum(cym, b * 16 + p, vel * (1.15 if p == 0 else 1.0 if p % 4 == 0 else 0.82))
        if crash and (b - b0) % crash == 0:
            drum("c", b * 16, 0.9 if b == b0 else 0.7)


def fill(b):
    """The last half bar before bar `b`."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, b * 16 - 8 + i, 0.6 + 0.045 * i)


def false_count(b0, b1):
    """Four bars of dotted-eighth 'quarters' fit in three bars of the stair."""
    start, settle = b0*16, (b1-1)*16
    short = ACC[1]-ACC[0]       # the stair starts with groups of three sixteenths
    assert settle-start == 4*4*short
    def stroke(at, i):
        drum('h', at, (.60,.44,.51,.44)[i])
        if i in (1,3):
            add('snare', at, .8, 'ss', .77 if i==1 else .86)
            T['snare'][-1]['gain'] = '10dB'  # the rim only; the song's snare fader stays put
    for i, t in enumerate(range(start,settle,short)):
        stroke(t, i%4)
    # Same hands, real quarter notes. The existing tom fill completes this
    # slower bar; neither the kick nor a cymbal announces the downbeat early.
    for i in range(2):
        stroke(settle+i*4, i)


def compose():
    # the foot: the stair alone on the Shepard tone; then the three guitars a side take it up
    line(FOOT, FOOT + 4, gtrs=False)
    line(FOOT + 4, RISE)
    if FALSE_COUNT:
        false_count(FOOT + 4, RISE)
    else:
        beat(FOOT + 4, RISE, snare=(), cym="h", vel=0.45, crash=0)
    fill(RISE)
    # the stair: the band
    R = int(RUNS.split(";")[0]) if RUNS else 0
    line(RISE, TIME - R)
    pedal(RISE, TIME)
    back = int(FIGURE.split(";")[0]) if FIGURE else RISE + 12        # the backbeat comes in with the figure
    beat(RISE, back, snare=(8,), cym="x", stepc=4)
    beat(back, TIME - R, snare=(4, 12), cym="x", stepc=2)
    if R:                                # v2: the stair hands over on a run, the snare doubling under it
        run(TIME - R, TIME)
        beat(TIME - R, TIME, snare=(), cym="x", stepc=2, crash=0)
        build(TIME - R, TIME)
    else:
        fill(TIME)
    if LEAD:                             # v4: a lead comes down two octaves over the tune's last six bars, onto the run's first note
        lb, top = int(LEAD.split(";")[2]), int(LEAD.split(";")[3])
        halves = 2 * (TIME - R - lb)
        assert halves == 12, "two octaves of a six-note scale, a note to the half bar"
        for i in range(halves):
            add("lead", lb * 16 + 8 * i, 8, top + 12 * (-i // 6) + SCALE[-i % 6], 0.9)
        add("lead", (TIME - R) * 16, 4, top - 24, 0.95)
    # the turn: the chug at three speeds, speeding up for ever. The kit and the bass hold the bar
    turn(TIME, FALL)
    if NAKED:                            # v7: one cycle of the turn alone with its kick; the kit comes back harder
        n0 = TIME + CYCLE * int(NAKED.split(";")[0])
        beat(TIME, n0, snare=(8,), cym="x", stepc=4, crash=CYCLE)
        drum("c", n0 * 16, 0.9)
        if NAKED.split(";")[1] == "lift":
            beat(n0 + CYCLE, FALL, snare=(4, 12), cym="x", stepc=2, crash=CYCLE)
        else:
            beat(n0 + CYCLE, FALL, snare=(8,), cym="x", stepc=4, crash=CYCLE)
    else:
        n0 = None
        beat(TIME, FALL, snare=(8,), cym="x", stepc=4, crash=CYCLE)
    for b in range(TIME, FALL):
        ground(b * 4, 0)
        if n0 is None or not n0 <= b < n0 + CYCLE:
            anchor(b)
    fill(FALL)
    # the descent
    descent(FALL, POLE, gend=POLE - R if R else None)
    if R:                                # v2: the guitars leave the descent on a falling run
        run(POLE - R, POLE, down=True, synth=False)
    if KITFALL:                          # v10: the kit changes gear where the fall does
        beat(FALL, 60, snare=(8,), cym="x", stepc=4, crash=6)
        beat(60, 66, snare=(4, 12), cym="x", stepc=4, crash=6)
        beat(66, 68, snare=(4, 12), cym="x", stepc=2, crash=2)
        beat(68, POLE - 2, snare=(0, 4, 8, 12), cym="x", stepc=2, crash=2)
        beat(POLE - 2, POLE, snare=(8,), cym="x", stepc=4, crash=0)
    else:
        beat(FALL, POLE, snare=(8,), cym="x", stepc=4, crash=6)
    T.setdefault("rumble", []).append({"at": FALL * 4, "len": (POLE - FALL) * 4 - 0.5, "pitch": "F2", "vel": 0.8})
    if TOMS:                             # v5: each octave of the descent ends on a fill that never lands; the last is the run's
        for i, n16 in enumerate(int(x) for x in TOMS.split(";")[2].split(",")):
            tomfall((FALL + 6 * (i + 1)) * 16 - n16, n16, scale=True)
        if R:
            tomfall((POLE - R) * 16, R * 16, scale=False)
    rise = os.environ.get('C10T5_TOMRISE', TOMRISE_DEFAULT if os.environ.get('C10T5_REV', '1') and all((
        TOMS, LEAD, FIGURE, HARM, NAKED, RUNS, os.environ.get('C10T5_COUNTERFALL', '1'), os.environ.get('C10T5_FALSE_COUNT', '1'),
        os.environ.get('C10T5_GONG', '1'), os.environ.get('C10T5_WHEEL', '1'), os.environ.get('C10T5_AFTERIMAGE', '1'),
        os.environ.get('C10T5_HOLD', '1'))) else '')
    double = os.environ.get('C10T5_DOUBLE', DOUBLE_DEFAULT if rise == TOMRISE_DEFAULT and all((
        POLELEAD, KITFALL, FALLKEY, STEEP, CLIMB, ALONE, VEQ, ANCHOR, BRAKE, TICK, ONE)) else '')
    if double:                           # v24: the backbeat doubles where the harmony comes in (before the fills take their rests)
        d0, d1 = (int(x) for x in double.split(";")[0].split(":"))
        assert back <= d0 < d1 <= TIME - R, "inside the stair's backbeat"
        assert sum(1 for n in T["snare"] if n["pitch"] == "s" and d0 * 4 <= n["at"] < d1 * 4) == 2 * (d1 - d0)
        T["snare"] = [n for n in T["snare"] if not (n["pitch"] == "s" and d0 * 4 <= n["at"] < d1 * 4)]
        for b in range(d0, d1):
            for p in (2, 6, 10, 14):
                drum("s", b * 16 + p, float(double.split(";")[1]))
    if rise:                             # v23: the lead's octaves each get a fill that never tops out
        lb, lengths = int(LEAD.split(";")[2]), [int(x) for x in rise.split(";")[0].split(",")]
        assert len(lengths) in (2, 3) and lb + 6 == TIME - R       # the lead falls an octave every three bars
        for i, n16 in enumerate(lengths):
            tomrise((lb + 3 * i) * 16 - n16, n16)
        if rise.split(";")[1:] == ["land"]:
            # each fill lands on a crash, as the descent's do. The one at the lead's entry is struck as a landing; the
            # next moves from the four-bar line (bar 28) to the lead's octave (bar 27). So under the lead the kit's
            # phrases are three bars and three, the honest line's time, against the tune's two and the low string's four
            crashes = {n["at"]: n for n in T["cym"] if n["pitch"] == "c"}
            crashes[lb * 4.0]["vel"] = 0.9
            moved = crashes[(lb + 4) * 4.0]
            moved["at"], moved["vel"] = (lb + 3) * 4.0, 0.9
    # the pole: one chord through a filter that climbs for ever; the line slowly; a bass that is only its overtones
    for b in range(POLE, BOTH, 2):
        root = PEDAL[((b - POLE) // 2) % len(PEDAL)]
        for tr in ("pl", "pr"):
            add(tr, b * 16, 31, ",".join(nm(F1 + root + i) for i in (0, 7, 12)), 0.9)
        add("ghost", b * 16, 31, F1 + (root - 12 if root > 6 else root), 0.85)
        drum("k", b * 16, 0.85)
    line(POLE, BOTH - R, gtrs=False, slow=2, synth=not POLELEAD)
    if POLELEAD:                         # v12: the slow line on the three leads
        slow_leads(POLE, BOTH - R)
        if HALFWAY:                             # v30: the tone says each half octave the leads climb, one held note a bar: F, B, F, B
            h0, h1 = (int(x) for x in HALFWAY.split(";")[1].split(":"))
            for b in range(h0, h1):
                add("stair", b * 16, 16, 65 + 6 * ((b - h0) % 2), 0.9)
    if TICK:                             # v2: a tick that speeds up for ever (the track's `risset`; these three strokes are its pattern)
        for at, ln, v in ((0.0, 0.5, float(TICK.split(";")[1])), (0.5, 0.5, float(TICK.split(";")[2])), (1.0, 1.0, float(TICK.split(";")[2]))):
            T.setdefault("tick", []).append({"at": at, "len": ln, "pitch": "h", "vel": v})
    else:
        beat(POLE, BOTH, snare=(), cym="h", vel=0.42, crash=0)
    T.setdefault("riser", []).append({"at": (BOTH - 4) * 4, "len": 16.0, "pitch": "F4", "vel": 0.8, **({"gain": "-3.0dB"} if R else {})})
    if R:                                # v2: a rising run into both, the snare doubling under it (the riser 3 dB down under them)
        run(BOTH - R, BOTH)
        build(BOTH - R, BOTH)
    else:
        fill(BOTH)
    # both: pitch and speed rise together. A riser that never arrives swells over the second half, and stops dead
    turn(BOTH, STOP, pitched=True)
    beat(BOTH, STOP, snare=(4, 12), cym="x", stepc=2, crash=CYCLE)
    for b in range(BOTH, STOP):
        ground(b * 4, 0)
        anchor(b)
    if not (CLIMB and CLIMB.split(";")[4] == "off"):
        T.setdefault("riser", []).append({"at": (STOP - 8) * 4, "len": 32.0, "pitch": "F4", "vel": 1.0,
                                          **({"gain": f"{float(CLIMB.split(';')[4]):.1f}dB"} if CLIMB and CLIMB.split(";")[4] else {})})
    if CLIMB:                            # v6: the riser is the lead guitar, playing the stair steeper and steeper
        climb(STOP - int(CLIMB.split(";")[2]), STOP)
    for b in range(STOP - 2, STOP):                      # the snare on every beat into the stop
        for q in (0, 8):
            drum("s", b * 16 + q, 0.85)
    # the summit: a bar of nothing; then the stair's first bars, exactly. One chord
    line(HOME, END, rot=RISE)
    pedal(HOME, END)
    beat(HOME, END, snare=(8,), cym="x", stepc=4)
    for tr in ("gl", "gr"):
        add(tr, END * 16, 40, ",".join(nm(F1 + i) for i in (0, 7, 12, 19)), 0.95)
    add("bass", END * 16, 40, F1, 0.95)
    ground(END * 4, 0)
    add("stair", END * 16, 40, 65, 0.9)
    drum("k", END * 16, 0.95)
    drum("c", END * 16, 0.95)
    # a voice that is not playing is down
    for lane in list(LANE.values()) + list(BLANE.values()):
        step(lane, END * 4, FLOOR)


def key_f(hz):
    """An eq frequency that follows the key: the lane `key` is the ground in semitones over F; the engine bends in octaves."""
    return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}


def pts(lane):
    return [[f"{t:g}b", v] for t, v in lane]


def veq_band():
    hz, q, db = VEQ.split(":")
    if not ALONE:
        return f"peak cutoff={hz} q={q} gain={db}dB"
    return {"kind": "peak", "cutoff": {"value": float(hz), "mod": [{"src": "auto.veq", "amount": 1}]}, "q": float(q), "gain": f"{db}dB"}


def veq_lane():
    """The eq band's frequency, in octaves from its own: it steps where the eight guitars are left alone and back."""
    if not ALONE:
        return {}
    import math
    a, b = (int(v) for v in ALONE.split(";")[0].split(":"))
    o = round(math.log2(float(ALONE.split(";")[1]) / float(VEQ.split(":")[0])), 4)
    return {"veq": {"points": [["0b", 0], [f"{a * 4 - 0.5:g}b", 0], [f"{a * 4:g}b", o], [f"{b * 4 - 0.5:g}b", o], [f"{b * 4:g}b", 0]], "curve": 0}}


# v16: the bass has two jobs where pitch and speed first climb together. The
# original picked string still counts four; its upper register gives way to a
# single held F whose own overtones pulse. Empty = v15 exactly.
HOLD = os.environ.get("C10T5_HOLD", "-15dB;-9")  # singing string gain; shelf on the picked string, dB


def held_string(doc):
    """Tune the sidebands in Hz so each partial beats against the four-bar turn."""
    start = BOTH * 4
    end = start + 2 * CYCLE * 4
    midi = F1 + 24
    hz = 440 * 2 ** ((midi - 69) / 12)
    period = CYCLE * 4 * 60 / BPM
    gain, cut = HOLD.split(";")
    spread = [1200 * math.log2(1 + i / (period * hz)) for i in (-2, -1, 0, 1, 2)]
    tuning = " ".join(f"synth.layers.{i}.cents={v:.8f}" for i, v in enumerate(spread))
    doc["patches"]["fs-string"] = {"extends": f"risset-arpeggio {tuning} synth.amp.a=100ms synth.amp.r=80ms",
                                   "fx": ["hp cutoff=380"]}
    doc["tracks"].append({"name": "string", "patch": "fs-string", "gain": gain, "pan": -.12,
                          "notes": [{"at": start, "len": end - start - .16, "pitch": nm(midi), "vel": .93}]})
    low = doc["buses"]["low"]
    low["auto"]["stringcut"] = {"points": [["0b", 0], [f"{start}b", 0], [f"{start + .15:g}b", float(cut)],
                                           [f"{end - .15:g}b", float(cut)], [f"{end}b", 0]], "curve": 0}
    low["fx"].append({"type": "eq", "bands": [{"kind": "highshelf", "cutoff": 340, "q": .7,
                     "gain": {"value": "0dB", "mod": [{"src": "auto.stringcut", "amount": 1}]}}]})


# v17: the summit's final F has an afterimage. All four strings attack as
# before; the two amps end on separate partials of F1. Empty restores v16.
AFTERIMAGE = os.environ.get("C10T5_AFTERIMAGE", "1" if HOLD else "")  # HOLD='' alone still gives v15


def last_chord(doc):
    """One pick, several releases. By the end there is no low string to supply the root."""
    at = END * 4
    parts = {t['name']: t for t in doc['tracks']}
    for side, sign in (('gl', -1), ('gr', 1)):
        t = parts[side]
        final = next(n for n in t['notes'] if n['at'] == at)
        strings = final['pitch'].split(',')
        assert strings == [nm(F1+i) for i in (0, 7, 12, 19)]
        # Damp the bottom strings, then leave F2 on the left amp and C3 on the
        # right. No amplifier gets both surviving pitches to make a sub tone.
        lengths = [2, 4, final['len'] if sign < 0 else 4, final['len'] if sign > 0 else 4]
        t['notes'].remove(final)
        t['notes'].extend(dict(final, pitch=p, len=length) for p,length in zip(strings,lengths))
        # Bring the two amps inward so each ear gets both pitches. Make up
        # the lost strings' level before damping: test a missing root, not
        # just a chord fading away. Ride the faders *after* the saturated amps.
        t['pan'] = {'value':t['pan'], 'mod':[{'src':'auto.inward','amount':-sign*.7}]}
        t['gain'] = {'value':t['gain'], 'mod':[{'src':'auto.release','amount':1}]}
        t.setdefault('auto', {}).update({
            'inward': {'curve':0,'points':[['0b',0],[f'{at}b',0],[f'{at+4}b',1]]},
            'release': {'curve':0,'points':[['0b',0],[f'{at+2}b',0],[f'{at+4}b',1.2],
                                           [f'{at+8:g}b',1.2],[f'{at+9:g}b',-8]]}})
    for tr, length in (('bass',3), ('stair',4)):
        next(n for n in parts[tr]['notes'] if n['at']==at)['len'] = length
    # The saturated amps still put energy around 44 Hz even with only the
    # upper strings left. Take that band out as the bass player's hand lifts;
    # this EQ is flat during the stair, turn and all earlier guitar parts.
    guitars = doc['buses']['gtrs']
    guitars.setdefault('auto', {})['root_out'] = {'curve':0,'points':[
        ['0b',0],[f'{at+2}b',0],[f'{at+4}b',-18]]}
    guitars['fx'].append({'type':'eq','bands':[{'kind':'peak','cutoff':440*2**((F1-69)/12),
                           'q':1.5,'gain':{'value':'0dB','mod':[{'src':'auto.root_out','amount':1}]}}]})


# v18: the right-hand chord in the middle of the pole goes to a wheel-bowed
# string. Empty restores v17; the older AFTERIMAGE and HOLD rollbacks still work.
WHEEL = os.environ.get('C10T5_WHEEL', '-9dB' if AFTERIMAGE else '')


def bowed_pole(doc):
    """One wheel turning under another: keep the common note when the ground changes."""
    right = next(t for t in doc['tracks'] if t['name'] == 'pr')
    start, end = 4*(POLE+2), 4*(BOTH-2)
    chords = [n for n in right['notes'] if start <= n['at'] < end]
    right['notes'] = [n for n in right['notes'] if not start <= n['at'] < end]
    home_fifth = F1 + 31  # C4 over the first and returning F chord
    previous, line = home_fifth, []
    for chord in chords:
        classes = {p[:-1] for p in chord['pitch'].split(',')}
        tones = [p for p in range(home_fifth-6, home_fifth+7) if nm(p)[:-1] in classes]
        key = home_fifth if home_fifth in tones else min(tones, key=lambda p: abs(p-previous))
        if not line or key != previous:
            line.append((chord['at'], key))
        previous = key
    notes = []
    for j,(at,key) in enumerate(line):
        # Overlap the two key changes for the slur; lift the wheel before the
        # guitars pick up the chromatic run. No restrike through the two E-flats.
        stop = line[j+1][0]+.03 if j+1<len(line) else end-.25
        notes.append({'at':at, 'len':round(stop-at,4), 'pitch':nm(key), 'vel':.86,
                      'expr':{'slur':int(j>0)}, **({'gain':'-1.5dB'} if key!=home_fifth else {})})
    doc['tracks'].append({'name':'wheel',
                          'patch':'hurdy-gurdy fx.0.mix=0 synth.amp.r=90ms play.gate=1 '
                                  'synth.layers.0.bow_pos=0.075 synth.layers.0.rosin=0.48 '
                                  'synth.layers.0.bright=0.65 synth.filters.0.cutoff=210',
                          'fx':[{'type':'eq','bands':['peak cutoff=330 q=0.9 gain=-8dB']}],
                          'gain':WHEEL, 'pan':right['pan'], 'out':right['out'], 'notes':notes})


# v19: one last swell comes from the kit. Empty restores v18.
GONG = os.environ.get("C10T5_GONG", "-8dB") if WHEEL and CLIMB and CLIMB.split(";")[4] != "off" else ""
# v20: a false count-in under the first guitar stairs only. Empty = v19;
# omitting GONG still restores the original v18 arrangement.
FALSE_COUNT = os.environ.get('C10T5_FALSE_COUNT', '1' if GONG else '')
# v21: where the fall takes two steps a bar, the right-hand guitars climb the
# same six notes against it. 'pick' keeps the riff's strokes; 'ring' holds
# each step instead. Empty = v20.
COUNTERFALL = os.environ.get('C10T5_COUNTERFALL', 'pick' if FALSE_COUNT and ONE else '')


# v22, section w4 (1:50.4-1:55.2, the turn's last two bars): THE ROLL THAT BECOMES THE NOTE. The turn speeds up for
# ever and is never faster; Harry hears it ("Faster and faster"). Under its last two bars one drum now REALLY speeds
# up: a roll on this song's own tom (`fs-tom`, the fill that never lands), from sixteenths, faster by the same factor
# every beat, until it is struck 43.65 times a second. That is the frequency of the low F. Past twenty or so
# strokes a second the ear stops counting strokes and hears a note whose pitch is the speed of the roll: so the roll
# turns into a tone that slides up and arrives, on the bar line of the descent, on the F the band is playing. At
# 0:57 the lead was the one line in the song that really came down; this is the one thing that really gets faster,
# and where it arrives is the note everyone started on. The eight guitars, the bass and the kit (with its fill, the
# one that lands) are as they were.
# (Why the tom: the first bench had two more guitars pick the roll. Their strokes never became a note: each pick of
# this string is a new burst of noise, and at 42 strokes a second the roll's waveform repeated itself by 0.15 at
# one stroke's distance. The kick read 0.08 and the bass 0.05. The tom's head is struck the same way every time:
# 0.95, with its lines on 43.6, 87.3 and 174.7 Hz.)
# (Levels, raw on seed 0: the roll enters 14.5 dB under the mix and swells to 8.4 under in its last half bar. The
# two bars gain 0.39 LU and 3.1 dB at 250-500 Hz, where this drum's head rings (lines near 200 and 325 Hz). At
# 8 dB more and with every stroke equally loud it added 1.1 LU and 6.2 dB there.)
# bars before the descent ; strokes to the beat it starts at ; track gain ; how each stroke's level follows the
# roll's speed (an exponent: positive takes level back as the roll gets denser, negative adds, so the roll swells
# into its note) ; the drum's note ; the loudness target. Empty restores v21.
REV = os.environ.get('C10T5_REV', '2;4;-22dB;-0.3;F2;-10' if COUNTERFALL and TOMS else '')


def roll_into_the_note(doc):
    bars, r0, gain, back, drum_note, lufs = REV.split(';')
    bars, r0, back = int(bars), float(r0), float(back)
    r1 = 440 * 2 ** ((F1 - 69) / 12) * 60 / BPM      # strokes to the beat at which the roll IS the low F
    tb, q, b0 = bars * 4.0, r1 / r0, (FALL - bars) * 4.0
    notes, k = [], 0
    while True:
        # the k-th stroke of a roll whose speed is r0 * q ** (t / tb): where its phase reaches k
        t = tb * math.log(1 + k * math.log(q) / (r0 * tb)) / math.log(q)
        if t >= tb - 1e-9:
            break
        r = r0 * q ** (t / tb)
        notes.append({"at": round(b0 + t, 4), "len": round(0.8 / r, 4), "pitch": drum_note, "vel": 0.9,
                      "gain": f"{-back * 20 * math.log10(r / r0):.1f}dB"})
        k += 1
    assert notes[0]["at"] == b0 and b0 + tb - 1 / r1 < notes[-1]["at"] < b0 + tb
    doc["tracks"].append({"name": "roll", "patch": TOMS.split(";")[0], "gain": gain, "pan": 0, "notes": notes})
    if float(lufs) != -10:
        doc["loudness"] = float(lufs)


def contrary_stairs(doc):
    rates = sorted((int(a), int(k)) for a, k in (v.split(':') for v in STEEP.split(',') if v))
    wheel = VOICES * len(SCALE)
    # Up two octaves and down two are four octaves apart, the whole wheel: so
    # every string, not only the sum of them, leaves from its own note and
    # arrives on the note it would have fallen to. Nothing has to jump back.
    spans = [(a, b, k) for (a, k), (b, _) in zip(rates, rates[1:]) if k == 2 and 2 * (b - a) * k % wheel == 0]
    if not spans:
        return
    a, b, per = spans[0]
    start = -sum(([1] + [k for bar, k in rates if bar <= x])[-1] for x in range(FALL, a))
    edges = [ACC[q * len(ACC) // per] for q in range(per)] + [16]
    for v in range(VOICES):
        tr = next(t for t in doc['tracks'] if t['name'] == f'v{v}r')
        was = tr['auto']['bell']['points']
        beat = lambda p: float(p[0][:-1])
        at = lambda x: [p[1] for p in was if beat(p) <= x][-1]
        lane, notes = [(a * 4.0, at(a * 4))], []
        for m in range((b - a) * per):
            bar, q = a + m // per, m % per
            d = start + m                       # the same ladder as the fall, walked the other way
            p = (12 * (d // 6) + SCALE[d % 6] + 12 * v) % (12 * VOICES)
            g = db(bell(p / (12 * VOICES))) + TRIM['fall']
            if g <= -45:
                continue
            step(lane, bar * 4 + edges[q] / 4, g)
            if COUNTERFALL == 'ring':
                notes.append({'at': bar * 4 + edges[q] / 4, 'len': round((edges[q + 1] - edges[q] - .35) / 4, 4),
                              'pitch': nm(RIFF_BASE + p), 'vel': 1.0})
                continue
            for i in range(edges[q], edges[q + 1]):
                o = i in ACC
                notes.append({'at': round(bar * 4 + i / 4, 4), 'len': round(.25 * .98, 4), 'pitch': nm(RIFF_BASE + p),
                              'vel': 1.0 if o else .86, **({} if o else {'expr': {'pm': 1.0}})})
        tr['notes'] = sorted([n for n in tr['notes'] if not a * 4 <= n['at'] < b * 4] + notes, key=lambda n: n['at'])
        tr['auto']['bell']['points'] = ([p for p in was if beat(p) <= a * 4] + pts(lane[1:]) +
                                        pts([(b * 4 - .01, lane[-1][1]), (b * 4, at(b * 4))]) + [p for p in was if beat(p) > b * 4])


def halfway(doc):
    """Strike halfway to the stop each time. Withhold the blow on the stop itself."""
    parts = {t["name"]: t for t in doc["tracks"]}
    end = STOP * 4
    rise = next(n for n in parts["riser"]["notes"] if n["at"] + n["len"] == end)
    parts["riser"]["notes"].remove(rise)
    distance = rise["len"]
    middle = end - distance / 2
    notes = []
    while distance >= .25:  # eight bars left, four, two, one, right down to a sixteenth
        i = len(notes)
        space = distance / 2
        # Same plate, never retuned. Carry the beater from near the boss to
        # the rim as the gaps close; don't let the last roll drown the lead.
        edge = min(1, .22 + .115 * i)
        notes.append({"at": end - distance, "len": min(6.5, space * .68), "pitch": nm(F1 + 12),
                      "vel": round(min(.95, .68 + .045 * i), 3), "expr": {"edge": round(edge, 3)},
                      "gain": f"{-min(3, max(0, i - 2))}dB"})
        distance = space
    cym = parts["cym"]
    # The drummer marks the long wait in eighths; past halfway the hand stays with the gong.
    cym["notes"] = [n for n in cym["notes"] if n["at"] != rise["at"] and not middle <= n["at"] < end]
    doc["tracks"].append({"name": "gong", "patch": "modal-gong play.gate=1 synth.amp.r=65ms "
                          "synth.layers.0.damp=0.1 synth.layers.0.strike=expr.edge",
                          "gain": GONG, "pan": .35, "fx": ["hp cutoff=150"], "notes": notes})


# v25: THE LEAD GETS A SPEAKER (instrument round, chirper-zero, 19 Nov; Harry: "improving our instruments, better guitars").
# THE INSTRUMENT: the lead guitar (the library's `lead-tape`): the one honest line that comes down over the stair
# (0:57.6-1:12) and the three leads that climb at the pole and in "both" (2:53-4:00). Every other guitar in this song
# goes through the engine's cabinet; the lead went through captured cabinet files, and after them through a tape
# saturator (`tape drive=0.3`) that put back, AFTER the speaker, the harmonics a speaker takes away.
# READ ALONE (the honest line, raw; third-octaves against its own 2-3.15 kHz; in brackets a guitar heard alone on the
# records, tools/guitarbench.py: three records agree to 0.7-1.6 dB): 4 kHz -3.0 (-3.6), 5 kHz -4.4 (-9.9), 6.3 kHz
# -6.9 (-16.4), 8 kHz -9.6 (-22.4), 10 kHz -12.5 (-26.7), 12.5 kHz -15.9 (-34.8). It fell 6 dB an octave where a
# guitar speaker falls 18: 10 to 19 dB of fizz from 6.3 kHz up, on the song's most exposed guitar. The eight guitars
# of the stair, through the engine's cabinet, read -6.2 -10.4 -17.6 -25.3 -31.3 -38.6.
# WHAT WAS TRIED (each benched alone): the engine's cabinet in place of the files, the saturator left on: -4.8 -7.3
# -10.5 -14.9 -19.6 -25.7 (half the fizz stays: it is the saturator's). The saturator moved ahead of the speaker, with
# the echo, as in an amp's loop: -5.6 -9.7 -19.6 -28.0 -35.6 -44.3 and the line's body thins (630 Hz 7.9 dB down).
# KEPT: the engine's cabinet with the microphone near the cone's centre, and the saturator's drive at nothing (its
# warmth, the echo and the hall as they were): -5.1 -9.3 -16.2 -21.5 -28.7 -38.6.
# ONLY THE TOP CHANGES. The cabinet alone also took 3.4 to 4 dB out of the lead at 630 Hz (its scoop, right for a
# riff) and put 3.4 to 4 in at 2.5 kHz. Two peaks in the patch's own eq hand those back, so the lead keeps the voice
# it had: against v24 at the same loudness the honest line is within 1.6 dB in every third-octave from 160 Hz to
# 4 kHz but one (500 Hz, +2.3), and then -3.2 at 5 kHz, -8.2 at 6.3, -11.6 at 8, -16.3 at 10, -23.2 at 12.5. Its top
# against its own 2-3.15 kHz: -3.8 -7.5 -15.0 -21.2 -28.7 -38.9, within 2.4 dB of the record's guitar from 4 to
# 10 kHz. Song-local patch `fs-lead`; no library patch is touched and no note changes.
# microphone (0 the cone's centre) ; cone ; distance ; the saturator's drive ; trim on the honest line's fader, dB ;
# trim on the three climbing leads' (each as loud alone as it was, -26.1 and -26.0 LUFS) ; the two peaks. "" = v24.
LEADCAB = os.environ.get("C10T5_LEADCAB", "0.1;50;0.15;0;-0.6;-0.7;670:3:3.5,2400:2:-3" if REV and os.environ.get("C10T5_DOUBLE", "1") and os.environ.get("C10T5_TOMRISE", "1") else "")


def speaker_for_the_lead(doc):
    mic, cone, dist, drive, trim, trim3, body = LEADCAB.split(";")
    doc["patches"]["fs-lead"] = {
        "about": "chirper-zero: the library's lead-tape with a speaker on top: its captured cabinet files replaced by the engine's cabinet, "
                 "the microphone near the cone's centre, and its tape saturator's drive at nothing (the saturator sat after the speaker and "
                 "put back the top a speaker takes away); two peaks in its eq keep the voice it had below 4 kHz. The same string, amp, echo and hall.",
        "extends": "lead-tape",
        "fx": [{"type": "sympathetic", "notes": "F1,Bb1,Eb2,Ab2,Db3,Gb3,Bb3,Eb4", "decay": "1.2s", "mix": 0.06},
               {"type": "amp", "model": "5150", "gain": 0.9, "ts": 0.7, "tight": 140, "boost": "6dB", "bass": 0.5, "mid": 0.68, "treble": 0.58,
                "presence": 0.6, "resonance": 0.55, "sag": 0.3, "bloom": 0.3},
               {"type": "cab", "model": "4x12-modern", "mic": float(mic), "distance": float(dist), "cone": int(cone)},
               {"type": "eq", "bands": ["peak cutoff=800 q=0.9 gain=2dB", "peak cutoff=250 q=1.2 gain=-2dB"]
                + ["peak cutoff=%s q=%s gain=%sdB" % tuple(x.split(":")) for x in body.split(",") if x]},
               {"type": "delay", "time": "1/4", "mix": 0.2, "feedback": 0.38, "tone": 2400},
               f"tape drive={float(drive):g} warmth=0.6",
               "reverb kind=hall decay=2.8s mix=0.22 predelay=30ms width=1.3"]}
    for t in doc["tracks"]:
        if t.get("patch") != "lead-tape":
            continue
        t["patch"] = "fs-lead"
        by = float(trim if t["name"] == "lead" else trim3)
        if isinstance(t["gain"], dict):
            t["gain"] = {**t["gain"], "value": f"{float(t['gain']['value'][:-2]) + by:g}dB"}
        else:
            t["gain"] = f"{float(t['gain'][:-2]) + by:g}dB"


# v26 (chirper-alpha, whole song: where the whole climb lands). Harry, 19 Nov, on the last chord (the card asked
# at v17, 'What do you hear as the bass lets go of the last chord?'): "Only the upper strings". The afterimage did
# not happen: two strings, an F on one amp and a C on the other, are a fifth, and a fifth is what he heard. A low
# note that is not there needs more than two of its overtones, and it needs them as ONE sound. The song already
# owns that sound: the pole's bass 'that is only its overtones' (the library's phantom-bass: the second to the
# sixth harmonic of its note and nothing at the note itself). So the last chord now has it too. It is struck WITH
# the chord, under the real bass, where it cannot be told from it; at three beats the bass lets go as before and
# what is left of the low F is five of its overtones in a row (87, 131, 175, 218, 262 Hz) with the two strings
# ringing inside them, to the end. Nothing sounds at 44 Hz and the F should still be there.
# its level once the bass has let go, dB against the ghost's track ; its length in beats (the patch sounds 0.85 of
# it) ; how far under that it stands while the real bass still holds (it rises over the half beat in which the bass
# lets go, so the band of the overtones keeps its level through the release). Empty restores v25.
PHANTOM = os.environ.get("C10T5_PHANTOM", "2.5;10.5;8" if LEADCAB and AFTERIMAGE else "")


# v27 (chirper-two, instrument round: the pole's tick): THE TICK IS A TICK. The kit's own illusion, the hat that
# speeds up for ever under the pole (2:52.8-3:16.8), was not a tick. v25's handoff: "the pole reads 6.3 dB over the
# records at 8-16 kHz and the leads are not what holds it: find what does". Read by part: the tick IS that band (all
# of 8-16 kHz at the pole and 77% of 4-8 kHz; the mix there 5.5 dB over the eleven records at 8-16 kHz). The kit's
# closed hat is noise through a high-pass at 8 kHz, the fader was at +22 dB to be heard at all, and it was sent to
# the kit's overhead room 4.5 dB UP (a room that passes only 5 to 12 kHz). Alone at the pole, above 2 kHz, it was
# within 12 dB of its own strokes' peaks 23% of the time: with the room off, 8%. So what was heard between the
# strokes was the room, and three copies of a pattern an octave of speed apart were being told apart through it.
# NOW, on this track only: the hat's high-pass at 5 kHz (a stick on a closed hat has its weight at 4 to 8 kHz),
# its decay 25 ms (was 45: with three copies running, a tenth of the strokes follow the one before by less than
# 45 ms), the room 10.5 dB down, 7 dB off above
# 8 kHz and 2 dB on at 5.2 kHz. Alone: 2-4 kHz +2.6 dB, 4-8 kHz -0.7, 8-16 kHz -5.6; on 6% of the time; and each
# stroke's peak is within 0.5 dB of where it was, so the tick is as loud when it ticks. In the finished mix above
# 4 kHz: on 25% -> 7% of the time, the strokes' peaks 0.5 dB lower, the level between them 1.9 dB lower. The pole
# then reads +0.1 against the records at 8-16 kHz (was +5.5) and -0.9 at 4-8 kHz (was -0.4).
# THE BRAKE (the same hat slowing down under the descent, 2:00-2:48) is NOT changed: Harry on its card, "Yes, keep
# the pull". Nor is the foot's hat.
# the hat's settings ; the track's fader ; its send to the overhead room ; its eq bands (comma between) ; the
# loudness target (empty: as it was). '' = v26.
TICKTONE = os.environ.get("C10T5_TICKTONE", "filters.0.cutoff.value=5k amp.d=25ms amp.r=10ms;24dB;-6dB;"
                          "highshelf cutoff=8000 gain=-7dB,peak cutoff=5200 q=1.2 gain=2dB;" if PHANTOM and TICK else "")


# v28 (chirper-alpha, whole song: the descent, 1:55.2-2:52.8, a quarter of the song): THE FALL HAS ITS TONE.
# Harry, 17 Nov 00:28, on the stair: "It climbed better with the tone under it". The plain Shepard tone states
# the illusion alone at the foot and has been back under the stair since v14 and at the summit (in the pole it
# plays only the run out, at 3:16.8).
# But the descent is "the stair the other way, and all of it", twenty-four bars of a tuning that keeps dropping
# and is never lower, and it has had no tone: the one stair in the song the band carries alone ('both' has none
# either: see the round's handoff). Now
# the tone says the fall as plainly as it says the climb: ONE HELD NOTE FOR EACH STEP THE RIFF FALLS, the step's
# own note (F, E flat, C, B, A flat, G flat, and round), on the same fader and the same lane as under the stair.
# So it also tells how steep the fall is, which nothing but the riff's own notes did: a step a bar for twelve
# bars (2.4 s a note), two a bar from 2:24 (where since v21 the right-hand guitars climb against it: the tone
# goes with the fall), three from 2:38.4, and from 2:43.2 six a bar: the stair's own line and rhythm, backwards,
# through the guitars' run into the pole, where it stops (its tail rings about two seconds into the pole).
# (Level, benched raw: under the stair, where he chose it, the tone stands 12.8 dB under the band, K-weighted. A
# held note sits lower than the stair's short ones: at the same fader it stood 15.1 under where the fall is a step a
# bar and 14.9 at two, and 13.7 at six, where its notes are the stair's own. So it has 1 dB more until the fall
# is six steps a bar: 14.1, 13.9, 13.1, then 13.7 and, over the guitars' run, 12.8.)
# dB on the tone under the descent, against its level under the stair ; the bar from which it is at the stair's
# own level again ; the loudness target ("" = unchanged). "" = v27.
FALLTONE = os.environ.get("C10T5_FALLTONE", "1;68;-9.975" if TICKTONE else "")


# v29 (chirper-two; section w8, 3:21.6-3:50.4, "both"; the window no round had focused): THE RIGHT HAND GOES WITH
# THE TAPE. "Both" is the song's last illusion: pitch and speed rise together, "as a tape speeding up does". But a
# tape that speeds up takes the cymbals with it, and here the drummer's right hand kept plain eighths on the china
# for the whole passage, 300 ms apart from first to last, while six guitars sped up round it: the one thing in the
# passage that says nothing is getting faster. Now the china leaves the bar and plays the riff's own strokes at all
# three of the guitars' speeds, each under the same bell as its guitar: one voice fading in at half speed, one
# doubling from the eighth to the sixteenth at full level, one from the sixteenth towards the thirty-second as it
# fades out. Each voice goes on into the next cycle twice as fast as it began, so the cymbal speeds up for twelve
# bars and is never faster. Its accents are the riff's (3 3 2), which the plain eighths never said. The LEFT hand
# and the foot stay: the snare on two and four, the bass four in a bar, the crash on each four-bar line. So the kit
# is torn in two, a hand with the tape and a hand with the clock, and the bar can still be counted.
# At 3:50.4 the hand leaves for the gong, as before (v19): the last cycle has no china.
# 95 strokes become 400 (three cycles; every one of the 400 falls on a guitar's stroke at that speed). A bar that
# had 8 strokes has 27, 29, 18 and 22 within 9 dB of full, through each cycle.
# ONE CYMBAL TO A VOICE: on one track the same strokes read 2 to 15 dB LOWER alone, bar by bar (a kit piece is one
# voice on its track: a quiet stroke of the fast voice cuts the ring of a loud one). So three tracks, `tape0-2`,
# copies of the cymbal track's own strip.
# MEASURED (raw, seed 0). The illusion holds (tools/endless.py on the three tracks, 4-bar cycle): the three cycles
# within 0.3 dB of each other, the level inside a cycle within 0.5 dB of its mean, 0.9 dB at the wrap; the notes
# the same in every cycle but two (the bar line the gong has taken). The cymbals alone, K, by bar: -29.2..-30.6
# before, -28.4..-29.0 now; against everything else -9.7..-12.2 before, -8.7..-10.6 now. The mix over the string's
# passage (3:21.6-3:40.8): +0.40 dB at 4-8 kHz, +0.54 at 8-16 kHz, and 0.04 or less in every band under 4 kHz,
# where the held string sounds ("I hear it: keep it"). In the finished file every other section is within 0.01 dB.
# the china strikes every this-many eighths of the riff ; bars from:to ; dB on its strokes there ; velocity on the
# riff's accents ; elsewhere ; strokes under this level of the bell are left out, dB ; the loudness target ("" =
# unchanged). "" = v28.
TAPE = os.environ.get("C10T5_TAPE", "1;84:96;-1;0.575;0.41;-24;" if FALLTONE else "")
# v30 (chirper-one; section w7, the pole, 2:52.8-3:16.8): HALF WAY ROUND. In the pole the three leads climb the stair's
# line at half an octave a bar, so their bars begin on F, B, F, B: the two notes of the song's scale that are half an
# octave apart. The plain tone (silent here since v12 gave its line to the leads) now says those two notes under them,
# ONE HELD NOTE A BAR, on the fader it has under the stair: ten notes, F B F B ... A stair with two steps. Half an
# octave is the one step that is as far up as it is down, and the tone has no height to settle it (alone, F's two
# loudest octaves, 349 and 698 Hz, are within 0.4 to 3 dB of each other, and B's loudest, 494 Hz, lies between them:
# up a tritone from one, down a tritone from the other). Under the leads it climbs; by itself it would only rock.
# So the tone now runs through the song: alone at the foot, under the stair, down the descent (v28), half way round at
# the pole, and up the run out of it. No other part changes.
# dB on the tone against its level under the stair ; bars from:to ; the loudness target ('' = unchanged). '' = v29.
# It is on only while no other C10T5_ switch is set, so every older switch gives exactly what it gave.
HALFWAY = os.environ.get("C10T5_HALFWAY", "-1.5;72:82;" if TAPE and not any(k.startswith("C10T5_") and k not in ("C10T5_OUT", "C10T5_SHOW", "C10T5_HALFWAY", "C10T5_SAID", "C10T5_CLIMBS", "C10T5_GROUNDED", "C10T5_EXCHANGE", "C10T5_PALM", "C10T5_SNARE", "C10T5_LEAN", "C10T5_ASCENT", "C10T5_SCRAPE", "C10T5_HAND", "C10T5_UNDER", "C10T5_SPIRAL") for k in os.environ) else "")

# v31 (chirper-two; palette: the song had no voice, and no song on the album had used the engine's speech to song):
# WE HAVE BEEN HERE BEFORE. A song "all about the illusions" (Harry, 15 Nov) had every illusion of pitch and of speed
# and none of the voice. Deutsch's is the best known: a few spoken words, repeated, begin to sound sung. The engine has
# it made real (`chirp tts --repeat --melodize`): the words are said again from a bar line, and each time their pitches
# have moved further onto a tune and their syllables further onto the grid.
#   WHERE: the pole, the song's one breath (2:52.8), one saying at each of its first five chords (F, F, A flat, E flat,
#       F: bars 72, 74, 76, 78, 80), in the chord's first bar; its second bar is left to the tone's B and the leads.
#   WHAT HE SAYS: "we have been here before". It is true of the saying itself the second time, and truer each time;
#       the chord under the fifth saying is the F the pole began on; and the song ends where it began.
#   WHAT IT TURNS INTO: the first two sayings are speech, and the same take (the illusion's own form: one recording,
#       repeated). The third and fourth are 0.35 and 0.7 of the way. The fifth is sung, and what he sings is THE STAIR'S
#       BAR: F, G flat, A flat, B, C, E flat on the bar's 3 3 3 3 2 2, the first bar of the song (the tone alone at
#       0:00) with words; six syllables for six notes, at speech's own speed (the spoken phrase lasts 3.4 beats of the
#       bar's four). He sings it ONCE: a voice has a height, and a second bar would drop back to F in the open, which
#       is what the stair hides (Harry on the stair: "It climbed better with the tone under it").
#   THE VOICE: the library's `voice-speech`, joined (one breath a saying), firmer and with more ring than it comes;
#       spoken at 125 to 171 Hz, sung F3 to E flat 4. Like every library voice it is body with no middle: alone it
#       read +17.1 dB under 250 Hz and -12.8 and -10.7 at 1-2 and 2-4 kHz against the records' voices; with the eq
#       +3.2 -0.1 +0.5 -2.7 +3.4 -9.6 -9.9 (under 250 Hz .. 8-16 kHz). Its open syllables stood 5 to 13 dB over its
#       closed ones ("have", and the sung "fore" on E flat 4); with a gain on each syllable, 2.1 to 3.3.
#   THE LEVEL IS WHERE THE WORDS COME THROUGH. At the level the records' voices stand in their mixes (-7.1 dB at
#       1-4 kHz; -6.1 to -6.7 here) the recogniser wrote 1, 2, 2, 1 and 0 of the five words from the pole's mix. At
#       this level (-4.1 to -4.6) it wrote 1, 5, 4, 4 and 2; 1.5 dB louder was no better; with half the lift at 3.2 kHz
#       it was worse (2, 5, 2, 3, 2). Alone, all five sayings are written exactly. The first is not made out in the
#       mix on any build: it comes up out of the descent's tail and both guitars' chord.
#   THE WHEEL GIVES 3 dB (-9 to -12 dB): it held 47% of the pole's 500 Hz-1 kHz, the band the voice needs.
#   COST, on the read against the eleven records' passages with a voice (the pole's ten bars): 2.96 -> 3.31, from
#       +0.9 dB at 2-4 kHz and the half dB that takes from every band below 250 Hz. At the records' level it was 3.03.
#   The first of the engine's five takes is not used: on four builds the recogniser wrote it 'We have plenty with all'.
# the voice's patch overrides ; fader ; pan ; send to the hall ; eq, band|band ; clip ceiling ('' = none) ; dB on each of the six
# syllables, one set for every time it is said ('' = none) ; the wheel's fader while he is in the song ('' = unchanged) ;
# the loudness target ('' = unchanged). '' = v30 byte for byte.
SAID = os.environ.get("C10T5_SAID", "synth.layers.0.join=true synth.layers.0.effort.value=0.75 synth.layers.0.ring=0.8 synth.layers.0.diction=2;"
                      "-18.5dB;0;-14dB;hp cutoff=200|lowshelf cutoff=400 gain=-8dB|peak cutoff=1500 q=0.7 gain=12dB|"
                      "peak cutoff=3200 q=0.8 gain=6dB|highshelf cutoff=6000 gain=12dB;;"
                      "2,-3.5,2,3,3,1.5,1,-4.5,1,2,2,0.5,2,-3.5,1.5,1,2,-1,0,-5.5,-0.5,0,0,-5.5,1,-6,-1,0,-0.5,-6.5;-12dB;" if HALFWAY else "")
SAID_TAKES = tuple(int(k) for k in os.environ.get("C10T5_SAID_TAKES", "1,1,2,3,4").split(","))   # which row below each saying is
SAID_BARS = (72, 74, 76, 78, 80)                    # the pole's first five chords: F, F, A flat, E flat, F
SAID_SUNG = (0.0, 0.0, 0.35, 0.7, 1.0)              # how far each saying has gone from speech (0) to the stair's bar (1)
# The engine's own speech to song, baked in so the generator needs no engine: `chirp tts "we have been here before" --key C3
# --bpm 100 --humanize 0.5 --seed 3 --repeat 5 --melodize 0,0,0.35,0.7,1 --melody "F3 Gb3 Ab3 B3 C4 Eb4" --join --rhythm --print`
# (engine 7138d6d5). One row a saying; a syllable is [beat in its bar, beats long, pitch, velocity, sounds, the pitch's path
# inside the syllable in cents, the length the path was made for]. Only the places and lengths are worked again below.
SAID_REPS = [
    [[0.253,0.443,"m52.473",0.763,"W IY1",[0,9,18,24,27,28,24,18,9,-3,-15],0.443],[0.696,0.752,"m52.139",0.785,"HH AE1 V",[0,5,10,15,19,22,24,27,30,32,30,23,15,10,8,7,4,-3,-14],0.752],[1.463,0.537,"m51.238",0.75,"B IH1 N",[0,7,14,20,24,25,25,25,27,24,16,4,-10,-21],0.537],[1.981,0.535,"m50.916",0.755,"HH IY1 R",[0,7,14,20,24,25,24,25,27,24,16,4,-10,-21],0.535],[2.523,0.345,"m47.961",0.858,"B IH0",[0,-3,-5,-8,-10,-13,-15,-18,-20],0.345],[2.881,0.748,"m47.701",0.774,"F AO1 R",[0,3,5,7,9,10,9,9,10,9,5,-4,-14,-22,-27,-30,-36,-45,-59],0.748]],
    [[0.248,0.443,"m52.632",0.846,"W IY1",[0,9,18,24,27,28,24,18,9,-3,-15],0.443],[0.69,0.752,"m52.166",0.774,"HH AE1 V",[0,5,10,15,19,22,24,27,30,32,30,23,15,10,8,7,4,-3,-14],0.752],[1.433,0.537,"m51.379",0.805,"B IH1 N",[0,7,14,20,24,25,25,25,27,24,16,4,-10,-21],0.537],[1.964,0.535,"m50.923",0.814,"HH IY1 R",[0,7,14,20,24,25,24,25,27,24,16,4,-10,-21],0.535],[2.505,0.345,"m47.609",0.818,"B IH0",[0,-3,-5,-8,-10,-13,-15,-18,-20],0.345],[2.855,0.748,"m47.281",0.823,"F AO1 R",[0,3,5,7,9,10,9,9,10,9,5,-4,-14,-22,-27,-30,-36,-45,-59],0.748]],
    [[0.25,0.444,"m52.616",0.764,"W IY1",[0,6,11,15,18,18,16,12,6,-2,-10],0.444],[0.709,0.744,"m52.692",0.775,"HH AE1 V",[0,3,7,10,12,14,14,16,22,27,25,15,4,-2,0,7,11,6,-6],0.744],[1.461,0.528,"m52.996",0.797,"B IH1 N",[0,5,10,14,15,12,11,17,24,21,7,-10,-22],0.528],[1.987,0.523,"m53.625",0.865,"HH IY1 R",[0,5,10,14,15,12,11,17,23,21,8,-9,-22],0.523],[2.504,0.334,"m51.838",0.769,"B IH0",[0,-2,-4,-6,-7,-9,-11,-13],0.334],[2.827,0.827,"m52.806",0.778,"F AO1 R",[0,2,3,4,6,6,5,6,9,12,10,1,-11,-18,-16,-10,-6,-11,-25,-40,-52],0.827]],
    [[0.252,0.46,"m52.805",0.854,"W IY1",[0,3,5,7,8,8,8,7,5,2,-1,-5],0.46],[0.733,0.736,"m53.316",0.801,"HH AE1 V",[0,2,3,5,6,5,3,6,13,22,22,9,-7,-14,-9,4,16,16,4],0.736],[1.485,0.508,"m54.535",0.804,"B IH1 N",[0,2,5,6,6,0,-3,5,19,23,13,-6,-22],0.508],[1.995,0.507,"m56.469",0.836,"HH IY1 R",[0,2,5,6,6,0,-4,5,19,23,13,-6,-22],0.507],[2.506,0.291,"m56.247",0.825,"B IH0",[0,-1,-2,-3,-4,-5,-6],0.291],[2.782,0.905,"m58.316",0.84,"F AO1 R",[0,1,1,2,2,3,2,2,6,11,11,2,-11,-19,-13,1,12,11,-2,-20,-32,-31,-20],0.905]],
    [[0.25,0.485,"m53",0.881,"W IY1",[0,0,0,1,-4,-14,-15,3,21,23,7,-15],0.485],[0.75,0.728,"m54",0.902,"HH AE1 V",[0,0,0,0,0,-2,-6,-4,6,17,19,5,-15,-25,-19,0,19,25,15],0.728],[1.5,0.485,"m56",0.873,"B IH1 N",[0,0,0,1,-4,-14,-15,3,21,23,7,-15],0.485],[2.0,0.485,"m59",0.896,"HH IY1 R",[0,0,0,1,-4,-14,-15,3,21,23,7,-15],0.485],[2.5,0.243,"m60",0.846,"B IH0",[],None],[2.75,0.972,"m63",0.807,"F AO1 R",[0,0,0,0,0,0,0,-1,3,9,10,3,-11,-21,-17,1,19,25,14,-6,-22,-23,-9,11,24],0.972]],
]


def we_have_been_here_before(doc):
    """A man says it at each of the pole's first five chords. The first two times he says it; by the fifth he sings it,
    and what he sings is the stair's bar: its six notes at its six places."""
    patch, fader, pan, hall, bands, ceiling, gains, wheel, lufs = SAID.split(";")
    stair = [n for n in next(t for t in doc["tracks"] if t["name"] == "stair")["notes"] if n["at"] < 4]
    places = [n["at"] for n in stair]
    assert places == [0.0, 0.75, 1.5, 2.25, 3.0, 3.5] and [n["pitch"][:-1] for n in stair] == ["F", "Gb", "Ab", "B", "C", "Eb"]
    assert [nm(int(n[2][1:]))[:-1] for n in SAID_REPS[-1]] == [n["pitch"][:-1] for n in stair]      # fully sung = the stair's notes
    said = [n[0] for n in SAID_REPS[0]]
    trim = [float(g) for g in gains.split(",")] if gains else [0.0] * 6
    trim = trim * 5 if len(trim) == 6 else trim         # six: the same for every saying; thirty: saying by saying
    assert len(trim) == 30
    notes = []
    for bar, m, rep in zip(SAID_BARS, SAID_SUNG, (SAID_REPS[k] for k in SAID_TAKES)):
        at = [n[0] if m == 0 else round((1 - m) * a + m * b, 3) for n, a, b in zip(rep, said, places)]
        for i, (_, length, pitch, vel, ph, path, made) in enumerate(rep):
            if m and i < 5:                           # joined as the engine joins a sung line (0.97), in the new places
                fill = (1 - m) * min(1.0, SAID_REPS[0][i][1] / (said[i + 1] - said[i])) + m * 0.97
                length = round((at[i + 1] - at[i]) * fill, 3)
            elif m:                                    # the last word is held as the saying turns to song
                length = round((1 - m) * SAID_REPS[0][5][1] + m * 1.5, 3)
            n = {"at": round(bar * 4 + at[i], 3), "len": length, "pitch": pitch, "vel": vel, "ph": ph}
            if path:
                n["expr_path"], n["path_len"] = {"f0": path}, made
            if trim[len(notes)]:
                n["gain"] = f"{trim[len(notes)]:g}dB"
            notes.append(n)
    assert POLE == SAID_BARS[0] and all(a["at"] < b["at"] for a, b in zip(notes, notes[1:]))
    assert all(notes[6 * k + 5]["at"] + notes[6 * k + 5]["len"] < notes[6 * k + 6]["at"] - 2 for k in range(4))   # a breath between sayings
    fx = ([{"type": "eq", "bands": bands.split("|")}] if bands else []) + ([f"clip drive=0dB ceiling={ceiling}"] if ceiling else [])
    doc["tracks"].append({"name": "said", "patch": ("voice-speech " + patch).strip(), "gain": fader, "pan": float(pan),
                          **({"sends": {"hall": hall}} if hall else {}), **({"fx": fx} if fx else {}), "notes": notes})
    if wheel:
        next(t for t in doc["tracks"] if t["name"] == "wheel")["gain"] = wheel
    if lufs:
        doc["loudness"] = float(lufs)


def the_right_hand_goes_with_the_tape(doc):
    """In "both" the china leaves the bar and plays the riff's own grid at all three speeds, under the guitars' bell:
    every stroke of it falls with a stroke of the guitar at that speed. The crashes, the snare and the bass keep the bar.
    One cymbal to a voice (a track each): on one, a quiet stroke of the fast voice cuts the ring of a loud one."""
    every, bars, trim, loud, soft, floor, lufs = TAPE.split(";")
    b0, b1 = (int(x) for x in bars.split(":"))
    assert BOTH <= b0 < b1 <= STOP and (b0 - BOTH) % CYCLE == 0 and (b1 - b0) % CYCLE == 0
    cym = next(t for t in doc["tracks"] if t["name"] == "cym")
    gone = [n for n in cym["notes"] if n["pitch"] == "x" and b0 * 4 <= n["at"] < b1 * 4]
    cym["notes"] = [n for n in cym["notes"] if not (n["pitch"] == "x" and b0 * 4 <= n["at"] < b1 * 4)]
    held = {n["at"] for n in cym["notes"]} | {n["at"] for n in gone}       # (a bar line the gong has taken stays the gong's)
    tc, L, new = CYCLE * 4.0, len(PAT) * 0.5, {v: [] for v in range(ROLES)}
    for c in range((b1 - b0) // CYCLE):
        c0 = b0 * 4 + c * tc
        for j in range(ROLES):
            scale = 2 ** (j - 1) * tc
            for m in range(int(round(1.5 * scale / L))):
                for i in range(0, len(PAT), int(every)):
                    u = -1 + math.sqrt(1 + 2 * (m * L + i * 0.5) / scale)
                    g = db(bell((j + u) / ROLES))
                    at = round(c0 + u * tc, 4)
                    if g < float(floor) or (u == 0 and at not in held):
                        continue
                    new[(j - c) % ROLES].append({"at": at, "len": 2.0, "pitch": "x", "vel": float(loud) if PAT[i] == "o" else float(soft),
                                                 "gain": f"{g + float(trim):.1f}dB"})
    for v in range(ROLES):                               # a voice goes on from one cycle to the next, twice as fast
        doc["tracks"].append({**{k: json.loads(json.dumps(x)) for k, x in cym.items() if k != "notes"}, "name": f"tape{v}",
                              "notes": sorted(new[v], key=lambda n: n["at"])})
    if lufs:
        doc["loudness"] = float(lufs)
    return len(gone), sum(len(x) for x in new.values())


def the_tick_is_a_tick(doc):
    hat, fader, room, bands, lufs = TICKTONE.split(";")
    # a kit of its own, so the brake and the foot's hat keep the hat they had
    doc["patches"]["fs-tick-kit"] = {"extends": "ct-kit-here", "kit": {"h": {"patch": f"haake-hat {hat}", "gain": "-10dB", "pan": -0.45, "choke": "hat"}}}
    tick = next(t for t in doc["tracks"] if t["name"] == "tick")
    tick["patch"], tick["gain"] = "fs-tick-kit", fader
    tick["sends"] = {"oh": room}                        # new objects: the brake was copied from this track and shares the old ones
    tick["fx"] = [{"type": "eq", "bands": bands.split(",")}]
    if lufs:
        doc["loudness"] = float(lufs)


def root_that_is_not_there(doc):
    level, length, under = (float(v) for v in PHANTOM.split(";"))
    at = END * 4
    ghost = next(t for t in doc["tracks"] if t["name"] == "ghost")
    assert all(n["at"] < at for n in ghost["notes"])
    ghost["notes"].append({"at": at, "len": length, "pitch": nm(F1), "vel": 0.85, "gain": f"{level - under:g}dB"})
    # the fader, after the patch: up as the bass's hand lifts (its note is three beats), down with the guitars' own
    # fade at the end (theirs is 9 dB over the ninth beat)
    ghost["gain"] = {"value": ghost["gain"], "mod": [{"src": "auto.takeover", "amount": 1}]}
    ghost["auto"] = {"takeover": {"curve": 0, "points": [["0b", 0], [f"{at + 2.5:g}b", 0], [f"{at + 3:g}b", under],
                                                         [f"{at + 8:g}b", under], [f"{at + 9:g}b", under - 9]]}}


def song():
    compose()
    key_lane = [["0b", 0]]
    for (b, k), (_, prev) in zip(KEY[1:], KEY):
        key_lane += [[f"{b - 0.02:g}b", prev], [f"{b:g}b", k]]
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    heavy = os.environ.get("C10T5_HEAVY", "ct-twin fx.1.model='5150' fx.2.mic=0.5 fx.2.cone={}")     # the low string
    voice = os.environ.get("C10T5_VOICE", "ct-twin fx.1.model=mark fx.2.mic=0.45 fx.2.cone={}")      # the three that carry the illusions
    GH, GV = os.environ.get("C10T5_GHEAVY", "-1.7dB"), os.environ.get("C10T5_GVOICE", "0dB")
    # the Shepard tone: its gain under the band ; its hall send ; dB over that alone at the foot ; with the guitars
    # at the foot ; in the pole
    synth = os.environ.get("C10T5_STAIR", "-19.5dB;-10dB;7.5;5.5;5.5").split(";")
    # v11: THE BAND CARRIES THE STAIR ALONE (whole-song round). The top of this file says the band plays the illusions,
    # "not a pad behind the band". But a pad WAS behind the band: the Shepard tone that states the illusion alone at
    # the foot stayed on under the whole stair (bars 8-32, a quarter of the song), 19.5 dB down on its fader. It is a
    # pure tone with all its weight around 500 Hz, and read alone it was within 3 dB of the WHOLE band from 250 to
    # 500 Hz there, the band where the stair stood 3.0 to 3.3 dB over the records. Now it does what the plan always
    # said: it states the illusion alone, the guitars take it up, and when the band comes in (0:19) it is gone. The
    # same at the summit, which is the stair's first bars again. It still sounds in the foot and in the pole.
    # the tone's level under the band, dB against its fader's own (-60 = out). "" = v10 (0: on under the band).
    # v14 (Harry, 17 Nov 00:28, asked whether the riff keeps climbing: "It climbed better with the tone under it"):
    # the tone is back under the band, at v10's level, in the stair and at the summit. His ear over my band table:
    # the stair reads 3.0 to 3.3 dB over the records at 250-500 Hz again, and that is now his to keep. The default is
    # "" again; C10T5_BANDONLY=-60 is v13 (the band alone).
    bandonly = os.environ.get("C10T5_BANDONLY", "")
    under = float(bandonly) if bandonly else 0.0
    syn_lane = [(0.0, float(synth[2]))]
    falls = [(FALL, under + float(FALLTONE.split(";")[0])), (int(FALLTONE.split(";")[1]), under)] if FALLTONE and float(FALLTONE.split(";")[0]) else []
    for bar, lvl in ((FOOT + 4, float(synth[3])), (RISE, under), *falls, (POLE, under + float(HALFWAY.split(";")[0]) if HALFWAY else float(synth[4])), (BOTH - (int(RUNS.split(";")[0]) if RUNS else 0), under)):
        step(syn_lane, bar * 4, lvl)
    tracks = [
        {"name": "gl", "patch": heavy.format(30), "gain": GH, "pan": -1, "out": "gtrs"},
        {"name": "gr", "patch": heavy.format(31), "gain": GH, "pan": 1, "out": "gtrs"},
        *[{"name": f"v{v}{side}", "patch": voice.format(32 + i if ONE else 32 + 2 * v + i), "gain": {"value": GV, "mod": [{"src": "auto.bell", "amount": 1}]},
           "pan": (-1, 1)[i] * (float(ONE) if ONE else (0.9, 0.75, 0.6, 0.45)[v]), "out": "gtrs", "auto": {"bell": {"points": pts(right_lane(v) if i else LANE[v]), "curve": 0}, **veq_lane()},
           **({"fx": [{"type": "eq", "bands": [veq_band()]}]} if VEQ else {})}
          for v in range(VOICES) for i, side in enumerate("lr")],
        {"name": "pl", "patch": heavy.format(40), "gain": os.environ.get("C10T5_POLE", "-1dB"), "pan": -0.8, "out": "pole"},
        {"name": "pr", "patch": heavy.format(41), "gain": os.environ.get("C10T5_POLE", "-1dB"), "pan": 0.8, "out": "pole"},
        {"name": "stair", "patch": "fs-stair", "gain": {"value": synth[0], "mod": [{"src": "auto.lvl", "amount": 1}]}, "pan": 0, "sends": {"hall": synth[1]},
         "auto": {"lvl": {"points": pts(syn_lane), "curve": 0}}},
        *([{"name": "lead", "patch": LEAD.split(";")[0], "gain": LEAD.split(";")[1], "pan": 0.1}] if LEAD else []),
        *([{"name": f"ld{v}", "patch": CLIMB.split(";")[0], "gain": {"value": CLIMB.split(";")[1], "mod": [{"src": "auto.bell", "amount": 1}]}, "pan": 0.1,
            "auto": {"bell": {"points": pts(LLANE[v]), "curve": 0}}} for v in range(3)] if CLIMB else []),
        {"name": "riser", "patch": "fx-riser-endless amp.a=16b", "gain": os.environ.get("C10T5_RISER", "-18dB"), "pan": 0},
        {"name": "rumble", "patch": "shepard-fall", "gain": os.environ.get("C10T5_RUMBLE", "-21dB"), "pan": 0},
        {"name": "ghost", "patch": "phantom-bass", "gain": os.environ.get("C10T5_GHOST", "-14dB"), "pan": 0},
        {"name": "bass", "patch": "ct-bass", "gain": os.environ.get("C10T5_BASS", "2dB"), "pan": 0, "out": "low"},
        *[{"name": f"bs{w}", "patch": "ct-bass", "gain": {"value": "0.5dB", "mod": [{"src": "auto.bell", "amount": 1}]}, "pan": 0, "out": "low",
           "auto": {"bell": {"points": pts(BLANE[w]), "curve": 0}}} for w in range(2)],
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        *([{"name": "falls", "patch": TOMS.split(";")[0], "gain": TOMS.split(";")[1], "pan": float(TOMS.split(";")[3]), "out": "drums", "sends": {"oh": "-1.5dB"}}] if TOMS else []),
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        *([{"name": "tick", "patch": kit, "gain": TICK.split(";")[0], "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air, "at": f"{POLE * 4}b",
            "risset": {"cycle": f"{TICK.split(';')[3]}bar", "layers": 3, "length": f"{BOTH - POLE - (int(RUNS.split(';')[0]) if RUNS else 0)}bar"}}] if TICK else []),
    ]
    if BRAKE:
        forward = next(t for t in tracks if t['name'] == 'tick')
        tracks.append({**forward, 'name': 'brake', 'gain': BRAKE, 'at': f'{BRAKE_IN * 4}b',
                       'risset': {**forward['risset'], 'down': True, 'length': f'{BRAKE_OUT - BRAKE_IN}bar'}})
        T['brake'] = [dict(n) for n in T['tick']]
        # One steady china stroke a bar to sight against the slowing hat. It
        # returns in half notes, then eighths, as the guitars' fall steepens.
        # Silence rather than delete its other taps to preserve the kit's seeds.
        mid = (FALL + POLE) // 2
        for n in T['cym']:
            if n['pitch'] != 'x':
                continue
            place = round(n['at'] * 4)
            bar, slot = divmod(place, 16)
            if BRAKE_IN <= bar < POLE - 6 and slot % (16 if bar < mid else 8):
                n['gain'] = '-60dB'
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])
    doc = {
        "about": ("chirpers X (Common Time), track 5 by chirper-zero: False Summit. True djent built on the illusions of endless motion, "
                  "played by the band: a line that climbs an octave every bar and is never higher (three guitars a side an octave "
                  "apart, each fading in at the bottom and out at the top); a chug that speeds up for ever and is never faster (the "
                  "same three at three speeds); the two together; and at the end the first bars again, exactly. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {
            "ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
            # the Shepard tone, played as notes: octave-spaced partials under a fixed bell, so a climbing scale never gets higher
            "fs-stair": {"synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "520hz", "width": 1.1}},
                                              {"type": "shepard", "cents": 6, "level": "-5dB", "shepard": {"octaves": 8, "center": "520hz", "width": 1.1}}],
                                   "filters": [{"kind": "lp", "cutoff": "5k", "q": 0.6}],
                                   "amp": {"a": "6ms", "d": "500ms", "s": 0.55, "r": "150ms"}},
                         "play": {"gate": 1.0, "vel_sens": 0.3}, "gain": "-6dB"},
            # v5: the kit's tom (ct-kit's: a struck modal head and a stick) as a pitched part, with a shorter ring so a run of them stays apart
            **({TOMS.split(";")[0]: {"synth": {"amp": {"a": "0.2ms", "d": f"{float(TOMS.split(';')[4]) * 1.4:.2f}s", "r": "150ms", "s": 0}, "drive": 0.12,
                                               "env": {"att": {"a": "0.1ms", "d": "5ms", "s": 0}},
                                               "filters": [{"cutoff": 40, "kind": "hp"}, {"cutoff": "4k", "gain": "2dB", "kind": "peak", "q": 1}],
                                               "layers": [{"type": "modal", "name": "head", "bright": {"value": 0.45, "mod": [{"src": "vel", "amount": 0.4}]},
                                                           "damp": 0.45, "decay": f"{TOMS.split(';')[4]}s", "sharp": 70.0,
                                                           "strike": {"value": 0.3, "mod": [{"src": "rand", "amount": 0.08}]}, "tilt": -2.0, "vary": 0.4},
                                                          {"type": "noise", "name": "stick",
                                                           "level": {"value": "-66dB", "mod": [{"src": "env.att", "amount": 50.0}, {"src": "vel", "amount": 8.0}]}}]},
                                     "play": {"vel_sens": 0.55}}} if TOMS else {}),
        },
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            # the pole: the endless filter sweep, one octave a bar
            "pole": {"fx": [{"type": "barberpole", "cycle": "1bar", "bands": 5, "spacing": 1, "low": "160hz", "q": 2.2, "spread": 0.4, "mix": float(os.environ.get("C10T5_POLEMIX", "0.85"))},
                            "reverb kind=hall decay=3s mix=0.25 predelay=20ms low_cut=150"]},
            "low": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                    {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]}],
                    "auto": {"key": {"points": key_lane, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T5_MASTER", "2.4dB")}]},
        "tracks": tracks,
    }
    if HOLD:
        held_string(doc)
    if AFTERIMAGE:
        last_chord(doc)
    if WHEEL:
        bowed_pole(doc)
    if GONG:
        halfway(doc)
    if COUNTERFALL:
        contrary_stairs(doc)
    if REV:
        roll_into_the_note(doc)
    if LEADCAB:
        speaker_for_the_lead(doc)
    if PHANTOM:
        root_that_is_not_there(doc)
    if TICKTONE:
        the_tick_is_a_tick(doc)
    if FALLTONE and FALLTONE.split(";")[2]:
        doc["loudness"] = float(FALLTONE.split(";")[2])
    if TAPE:
        the_right_hand_goes_with_the_tape(doc)
    if HALFWAY and HALFWAY.split(";")[2]:
        doc["loudness"] = float(HALFWAY.split(";")[2])
    if SAID:
        we_have_been_here_before(doc)
    if CLIMBS:
        the_turn_climbs_the_stair(doc)
    if GROUNDED:
        the_foot_is_on_the_ground(doc)
    if EXCHANGE:
        the_fall_neither_hand_plays(doc)
    if PALM:
        the_palm_lets_the_teeth_through(doc)
    if SNARE:
        the_snare_comes_out_of_its_box(doc)
    if LEAN:
        the_bass_leans_on_its_octave(doc)
    if ASCENT:
        the_lead_goes_back_up(doc)
    if SCRAPE:
        the_pick_is_dragged(doc)
    if HAND:
        the_descent_gets_a_hand(doc)
    if UNDER:
        the_chug_under_the_stair_holds(doc)
    if SPIRAL:
        the_stair_is_a_spiral(doc)
    return doc


# v32 (chirper-one; section round, w4, 1:26-1:55, the turn's last three cycles; the map: "static in tone"): THE
# TURN CLIMBS THE STAIR. The turn is sixteen bars of one note: the chug speeds up for ever on the low F and the bass
# counts F under it, four cycles alike in pitch. Its cycles are the one place in the song where something comes
# round and is plainly THE SAME AGAIN (every fourth bar line the three speeds and the kit are together). Now each
# time it comes round it is a step up the stair's own line: F, G flat, A flat, B: the first four of the album's six
# notes, the guitars' low string and the bass together, the bass's eq following. So the turn has two motions, one
# false and one true: it is never faster, and it IS higher, by half an octave when it ends. B is the note half way
# round from F (v30: "half way round"), the furthest the stair can be from home. And then the descent begins, on F:
# the first thing the fall does is drop that half octave in one step, and go on falling for ever. The top the turn
# reached was not the top: the song's title, said by the form. The roll under the last two bars (v22) still speeds
# up to 43.65 strokes a second and arrives on the F the band lands on.
# Nothing moves in time and no fader moves: 942 guitar strokes and 32 bass notes change pitch (the first cycle is
# as it was), and the bass bus's two keyed bands follow.
# semitones over F for each cycle of the turn in turn ; the tracks that climb ; the loudness target ("" =
# unchanged). "" = v31 byte for byte. On only while SAID is; C10T5_CLIMBS is in HALFWAY's list of names that do
# not turn it off.
CLIMBS = os.environ.get("C10T5_CLIMBS", "0,1,3,6;v0l,v0r,v1l,v1r,v2l,v2r,v3l,v3r,bass;" if SAID else "")


def the_turn_climbs_the_stair(doc):
    """v32: each cycle of the turn is a step further up the stair's line; the bass and its keyed eq go with the guitars."""
    semis, names, target = CLIMBS.split(";")
    semis = [int(x) for x in semis.split(",")]
    assert len(semis) == (FALL - TIME) // CYCLE and semis[0] == 0, semis
    b0, tc = TIME * 4, CYCLE * 4
    tr = {t["name"]: t for t in doc["tracks"]}
    for name in names.split(","):
        for n in tr[name]["notes"]:
            if b0 <= n["at"] < FALL * 4:
                c = int((n["at"] - b0 + 1e-6) // tc)
                assert n["pitch"] == nm(F1) and n["at"] + n["len"] <= b0 + (c + 1) * tc + 1e-6, (name, n)   # every one is the low F, and none is held over a cycle's line
                n["pitch"] = nm(F1 + semis[c])
    pts = doc["buses"]["low"]["auto"]["key"]["points"]
    at = lambda p: float(str(p[0]).rstrip("b"))
    i = max(k for k, p in enumerate(pts) if at(p) <= b0)
    assert pts[i][1] == 0 and (i + 1 == len(pts) or at(pts[i + 1]) >= FALL * 4), pts[i:i + 2]      # the ground is F all through the turn, and after it
    new = []
    for c in range(1, len(semis)):
        new += [[f"{b0 + c * tc - 0.02:g}b", semis[c - 1]], [f"{b0 + c * tc:g}b", semis[c]]]
    new += [[f"{FALL * 4 - 0.02:g}b", semis[-1]], [f"{FALL * 4:g}b", 0]]
    if i + 1 < len(pts) and at(pts[i + 1]) == FALL * 4:
        new.pop()
    pts[i + 1:i + 1] = new
    if target:
        doc["loudness"] = float(target)


# v33 (chirper-two; whole song: the bass drum, all 791 strokes; no stroke is added, moved or taken out): THE FOOT IS
# ON THE GROUND. The album kit's bass drum is on A (55 Hz) and wanders a sixth of a tone at random. This song is on
# F, and its whole subject is pitch that seems to move: a stair on F, A flat, E flat; a turn that v32 made climb F,
# G flat, A flat, B. Under all of it the one drum said A, a major third over the ground and a different interval
# over every other note (chirper-one's v32 handoff names it: "the kick under the turn is tuned once (55 Hz) and now
# stands under four notes"). Now every stroke is tuned to the ground under it, read from the bass bus's key lane,
# which the stair, the turn and the summit all write: F1 530 strokes, A flat 1 101, E flat 1 42, G flat 1 118 (59
# on G flat, and 59 on B, where the drum stands a fourth under the bass: on B1 itself, 61.7 Hz, the two cancel by
# turns and the mix lost 1.5 to 1.6 dB under 60 Hz, as Close Enough v21 found). The turn's third cycle, where the
# guitars and the bass drop out and the kick is alone, is the plainest place: the drum itself now says A flat.
#   THE STROKE STAYS WHERE IT WAS. The drum's stroke is a fall of 31 semitones onto its note, so a drum tuned down a
#       third lost its top with it (alone, 1.1 to 2.4 dB at 250 Hz-2 kHz and 2.0 at 4-8 kHz). The fall now starts
#       from the height it always did (35 semitones over F1), and the track's 4.5 kHz band goes +10 -> +11.2 dB:
#       alone, the drum is within 0.8 dB of v32's in every band from 120 Hz up, and level at 2-16 kHz.
#   THE CHEST: a bare sine a tenth of a second long, an octave over the drum, on every stroke, with the stroke's own
#       gain, on a track of its own past the drums' bus (the recipe of Common Measure v29). Its fader was chosen by
#       the mix's read against the records (eleven windows, every section with the drum in it): -5.5 dB 1.281 /
#       1.346 (their mixes / their passages with no voice; v32 1.269 / 1.447), -2.5 dB 1.243 / 1.291, -0.5 dB better
#       again by 0.01 / 0.04. Kept -2.5: alone the drum is then already 5 dB over the records' kicks at 80-100 Hz.
#   THE TARGET -9.975 -> -10.04: a drum whose weight is lower counts for less in the loudness measure, and the
#       master brought everything else up 0.07 to 0.10 dB. At -10.04 the stretches with no bass drum in them (the
#       foot, the pole between its six strokes, the last chord) are within 0.002 dB of v32's on seed 0 and 0.007 on
#       seed 11.
# overrides inside the kit's bass drum, after its note ; the highest note the drum may take, Hz (a ground over it:
# the drum stands a fourth lower) ; the chest: semitones over the DRUM : its length, ms : its fader ('' = no chest)
# ; how much of the way down the top of the stroke's fall does NOT come with the drum (0..1; '' = it all comes) ;
# the kick track's eq, band|band ('' = unchanged) ; the loudness target ('' = unchanged). "" = v32 byte for byte.
# On only while CLIMBS is; C10T5_GROUNDED is in HALFWAY's list of names that do not turn it off. It reads the key
# lane, so it must run after anything that moves the ground.
GROUNDED = os.environ.get("C10T5_GROUNDED", "kit.k.patch.synth.pitch.mod.1.amount=0;55;12:90:-2.5dB;1;peak cutoff=4500 q=0.8 gain=11.2dB;-10.04" if CLIMBS else "")


def the_foot_is_on_the_ground(doc):
    """v33: every bass-drum stroke is tuned to the ground under it (the bass bus's key lane, which the stair, the turn
    and the summit all write), a fourth lower where the ground is over the highest note a drum may take; and a chest
    (a bare sine, a tenth of a second) says the ground's octave on every stroke, on a track of its own past the
    drums' bus, with the stroke's own gain. No stroke is added, moved or taken out."""
    over, top, chest, stroke, eq, target = GROUNDED.split(";")
    T = {t["name"]: t for t in doc["tracks"]}
    kick = T["kick"]
    kit = kick["patch"]
    assert " " not in kit and all(n["pitch"] == "k" and "patch" not in n for n in kick["notes"])
    lane = [(float(str(b).rstrip("b")), v) for b, v in doc["buses"]["low"]["auto"]["key"]["points"]]
    ground = lambda at: F1 + [v for b, v in lane if b <= at + 1e-6][-1]
    note = lambda at: ground(at) - 5 if 440.0 * 2 ** ((ground(at) - 69) / 12) > float(top) else ground(at)
    # the kit's drum is on A1 and its stroke is a fall of 31 semitones onto the note: `stroke` (0..1) is how much of the way down the top of that fall does NOT come
    fall = lambda m: f" kit.k.patch.synth.pitch.mod.0.amount={31 + float(stroke) * (33 - m):g}" if stroke and float(stroke) else ""
    drum = lambda m: f"{kit} kit.k.pitch={nm(m)}" + (" " + over if over else "") + fall(m)
    kick["patch"] = drum(F1)
    for n in kick["notes"]:
        if note(n["at"]) != F1:
            n["patch"] = drum(note(n["at"]))
    if chest:
        semi, ms, fader = chest.split(":")
        doc["patches"]["fs-chest"] = {"extends": "808", "synth": {"layers": ["sine"], "pitch": {"value": 0, "mod": []}, "drive": 0, "filters": [],
                                                                 "amp": {"a": "2ms", "d": f"{ms}ms", "s": 0, "r": "20ms", "curve": 3}},
                                      "play": {"mono": False, "glide": "0ms", "gate": 1}}
        doc["tracks"].append({"name": "chest", "patch": "fs-chest", "gain": fader, "pan": 0,
                              "notes": [{"at": n["at"], "len": 0.25, "pitch": nm(note(n["at"]) + int(semi)), "vel": n["vel"],
                                         **({"gain": n["gain"]} if "gain" in n else {})} for n in kick["notes"]]})
    if eq:
        assert len(kick["fx"]) == 1 and kick["fx"][0]["type"] == "eq"
        kick["fx"] = [{"type": "eq", "bands": eq.split("|")}]
    if target:
        doc["loudness"] = float(target)


# v34 (chirper-alpha; section round, w6, 2:24-2:52.8, flagged static and little new; the change is its steepest two
# bars, 68 and 69, 2:43.2-2:48.0, where the fall takes six steps a bar; 107 of the eight guitars' 234 strokes there
# change pitch; nothing moves in time; the basses, the tone, the kit and every other bar are as they were).
# THE FALL THAT NEITHER HAND PLAYS.
#   The song has the illusions of pitch (the stair), of speed (the turn), of both, of the missing root, of half way
#   round, of speech turning to song. It had none of PLACE. The best known is Deutsch's scale illusion (1973): a
#   scale going down and the same scale going up, played at once, every other note of each sent to the other ear.
#   Each ear is given a line that leaps about; what is heard is two smooth lines. Tchaikovsky wrote the opening of
#   the last movement of his sixth symphony that way: neither violin section plays the tune the hall hears.
#   This song already has the two scales: at 2:24 (v21) the right side climbs the six notes while the left falls.
#   Where the fall is steepest it was all eight guitars in unison. Now both stairs are played there, six steps a
#   bar, and from step to step the two sides change places (they share the two notes where the lines meet):
#       the left plays   F  G flat  C  B  A flat  E flat     (both, climb, fall, both, fall, climb)
#       the right plays  F  E flat  A flat  B  C  G flat     (both, fall, climb, both, climb, fall)
#   twice. Nobody plays the fall, F E flat C B A flat G flat, and nobody plays the climb: each is whole only in the
#   two sides together. The two basses and the tone (v28) keep the fall under it; the kick is on every step.
#   MEASURED (raw, own seed, the eight guitars alone, the two lines' own pitch classes in each ear step by step):
#   in the left ear the climb stands 5.6 dB over the fall where the left has the climb and 5.1 under where it has
#   the fall; in the right 5.7 over and 7.8 under (medians). Both ears summed, the two lines
#   are level (climb less fall -1.3). In v33 the fall stood 5 to 9 dB over in both ears on every step. The two bars
#   are 0.06 dB up (K), each ear within 0.13 dB of v33 and the mono sum within 0.10 on the finished files; the rest
#   of the song is v33's within 0.003 dB.
# the rates of the fall (steps a bar, as STEEP gives them) whose bars are exchanged, ',' between ; which steps the
# LEFT side takes the climb on (1 = every second step from the second, 0 = from the first, '' = none: the right
# climbs and the left falls, as at 2:24) ; the loudness target ('' = unchanged). "" = v33 byte for byte. On only
# while GROUNDED and COUNTERFALL are; C10T5_EXCHANGE is in HALFWAY's list of names that do not turn it off.
EXCHANGE = os.environ.get("C10T5_EXCHANGE", "6;1;" if GROUNDED and COUNTERFALL else "")


def the_fall_neither_hand_plays(doc):
    """v34: in the fall's steepest bars both stairs are played at once, the fall and its mirror, and every second step
    the two sides change places: each side plays a line that leaps, and the fall and the climb are whole only in
    the two together. The basses, the tone and the kit keep the fall."""
    which, odd, target = EXCHANGE.split(";")
    rates = sorted((int(x.split(":")[0]), int(x.split(":")[1])) for x in STEEP.split(","))
    ends = [bar for bar, _ in rates[1:]] + [POLE - (int(RUNS.split(";")[0]) if RUNS else 0)]
    beat = lambda p: float(p[0][:-1])
    for (a, per), b in zip(rates, ends):
        if str(per) not in which.split(","):
            continue
        start = -sum(([1] + [k for bar, k in rates if bar <= x])[-1] for x in range(FALL, a))
        edges = [ACC[q * len(ACC) // per] for q in range(per)] + [16]
        for v in range(VOICES):
            for side in "lr":
                tr = next(t for t in doc["tracks"] if t["name"] == f"v{v}{side}")
                was = tr["auto"]["bell"]["points"]
                at = lambda x: [p[1] for p in was if beat(p) <= x][-1]
                lane, notes = [(a * 4.0, at(a * 4))], []
                for m in range((b - a) * per):
                    bar, q = a + m // per, m % per
                    up = (side == "r") if odd == "" else ((m % 2 == int(odd)) == (side == "l"))
                    d = start + m if up else start - m          # the fall's own ladder, walked up or down from where it stands
                    p = (12 * (d // 6) + SCALE[d % 6] + 12 * v) % (12 * VOICES)
                    g = db(bell(p / (12 * VOICES))) + TRIM["fall"]
                    if g <= -45:
                        continue
                    step(lane, bar * 4 + edges[q] / 4, g)
                    for i in range(edges[q], edges[q + 1]):
                        o = i in ACC
                        notes.append({"at": round(bar * 4 + i / 4, 4), "len": round(0.25 * 0.98, 4), "pitch": nm(RIFF_BASE + p),
                                      "vel": 1.0 if o else 0.86, **({} if o else {"expr": {"pm": 1.0}})})
                tr["notes"] = sorted([n for n in tr["notes"] if not a * 4 <= n["at"] < b * 4] + notes, key=lambda n: n["at"])
                tr["auto"]["bell"]["points"] = ([p for p in was if beat(p) <= a * 4] + pts(lane[1:]) +
                                                pts([(b * 4 - 0.01, lane[-1][1]), (b * 4, at(b * 4))]) + [p for p in was if beat(p) > b * 4])
    if target:
        doc["loudness"] = float(target)


# v35 (chirper-zero; instrument round: THE EIGHT STAIR GUITARS' PALM-MUTED CHUG, which is the whole guitar band of
# the turn 1:16.8-1:55.2, the descent 1:55.2-2:52.8 and 'both' 3:21.6-4:00: 3175 muted strokes. No note changes;
# nothing but those eight tracks' sound, and their fader in those three stretches). THE PALM LETS THE TEETH THROUGH.
# I read the whole band first (kick, snare, bass, cymbals, the two rigs, the mix by stretch). What stood furthest
# from the records was the eight's chug: through a muted stroke the records' guitars keep their teeth (400 Hz-1 kHz
# against 1-4 kHz: -11.3 dB, their range -12.7 to -6.5) and ours read -6.3 in the descent: at the edge, a box.
# And the mix said the same of the descent with nobody singing: short at 2-4 kHz (-1.3 and -1.0), over at
# 250-500 Hz (+2.3, +2.7). The palm of this rig closes a filter on the string (-3.4 as it comes) and adds a thump
# under the stroke (0.4). Here the palm closes less (-2) and the thump is out: the string's own top reaches the
# amp. Benched rung by rung on one of the eight alone, then in the mix.
# what is added to the eight's patch ; dB on the eight's faders where they chug (it holds the chug's loudness alone:
# the lighter palm is 0.45 LU louder) ; those stretches in beats ; the loudness target ('' = unchanged).
# On only while EXCHANGE is; C10T5_PALM is in HALFWAY's list of names that do not turn it off. "" = v34 byte for byte.
PALM = os.environ.get("C10T5_PALM", "synth.layers.0.thump.mod.0.amount=0 synth.filters.0.cutoff.mod.0.amount=-2;-0.45;128:288,336:400;-10.032" if EXCHANGE else "")


def the_palm_lets_the_teeth_through(doc):
    """v35: the eight stair guitars' palm closes less and loses its thump; their fader holds the chug's loudness."""
    extra, trim, spans, target = PALM.split(";")
    eight = [t for t in doc["tracks"] if len(t["name"]) == 3 and t["name"][0] == "v" and t["name"][1] in "0123" and t["name"][2] in "lr"]
    assert len(eight) == 8, [t["name"] for t in eight]
    for t in eight:
        t["patch"] = t["patch"].rstrip() + " " + extra
        if trim and float(trim):
            pts = [["0b", 0]]
            for sp in spans.split(","):
                a, b = (float(x) for x in sp.split(":"))
                assert all(a <= n["at"] < b for n in t["notes"] if (n.get("expr") or {}).get("pm")) or len(spans.split(",")) > 1
                pts += [[f"{a - 0.01:g}b", 0], [f"{a:g}b", float(trim)], [f"{b - 0.01:g}b", float(trim)], [f"{b:g}b", 0]]
            assert "palm" not in t.get("auto", {}) and isinstance(t["gain"], dict)
            t.setdefault("auto", {})["palm"] = {"curve": 0, "points": pts}
            t["gain"] = {**t["gain"], "mod": list(t["gain"].get("mod", [])) + [{"src": "auto.palm", "amount": 1}]}
        ins = [(float(x.split(":")[0]), float(x.split(":")[1])) for x in spans.split(",")]
        assert all(any(a <= n["at"] < b for a, b in ins) for n in t["notes"] if (n.get("expr") or {}).get("pm")), t["name"]   # every muted stroke is inside
    if target:
        doc["loudness"] = float(target)


# v36 (chirper-zero; instrument round: THE SNARE, the album kit's as it comes, all 180 strokes of it; chirper-two's
# v33 handoff: "the snare is the album's: the next drum to fit"): THE SNARE COMES OUT OF ITS BOX.
# In this song the snare makes the stair's claim in time: one stroke a bar, then two, then four (chirper-one's v24
# under the stair, v10 under the fall), and runs of sixteenths into the turn and out of the pole. For that each
# stroke has to be a point, as the tick had to be (v27). Alone, against six records' snares by thirds of an octave
# (tools/snarespec.py), it read 5.31 dB out: a box at 1 and 1.25 kHz (+7.5, +7.2), a hump at 2 and 2.5 kHz (+5.6,
# +6.3) where theirs dip, and 1.6 to 4.4 dB short from 4 kHz up, where theirs have their crack.
# One field of the drum's own model at a time, alone, then five whole variants in the mix (seven stretches against
# the eleven records' passages with nobody singing):
#   damp 0.3 -> 0.9, decay 0.18 s -> 0.13 s, wires 0.85 -> 0.72 (Slow Enough to Count v27's three): the head stops
#       ringing at its box without the energy going to its note. 5.31 -> 4.27 alone.
#   slap 1.2 -> 0.9 and contact 0.6 -> 0.4: the dense upper modes (the 2 kHz hump) give a little and the stick's
#       contact is shorter, so the stroke's own top reaches 4 to 5 kHz. (slap 0.6, Odd Sympathy's, read nearer the
#       records alone, 4.21, and the descent refused it: its second half fell 0.3 to 0.5 dB shorter at 2-4 kHz. The
#       mode count of ten, which cured the box at 1.25 kHz there, moved it to 1 kHz here and lengthened the ring.)
#   the piece's own filters: the box cut where it stands (1150 Hz, -6 dB), a lift at 4.5 kHz (+2 dB: the mix is
#       0.7 to 2.2 dB short at 4-8 kHz in every stretch), a shelf above 8 kHz (-2 dB: it holds the mix's top octave
#       where it was; at -4 dB five stretches came out 0.3 to 0.5 dB shorter there and the run out of the pole 1.9),
#       and the library's lift under the note (200 Hz, +5 dB) made 230 Hz, +2 dB: with it the note stands out of the
#       band as far as it did (+7.8 dB against +7.7); without it the drum read thin against its own crack (-7.3 dB,
#       the records -2.9, the old one -5.0; now -5.3).
#   the piece's gain 1 -> 2.5 dB: what the damping took.
# 4.07 alone. In the mix seven of the eight stretches it plays in read nearer the records, each by a little (the
# snare is 0.4 to 1.1 dB of any band), and the descent's second half 0.02 further. Five other variants were read.
# WHAT IT IS NOT: each stroke stands 0.6 dB LESS out of the finished file to a meter that favours the middle, because
# the box was part of what stood. Alone the drum has fallen 1.4 dB further when the next stroke of a run comes.
# The whole piece is written into the song's kit and the snare's TRACK is not touched: its eq, fader and sends are
# shared by the nine rim strokes of chirper-three's false count-in (the piece `ss`), which stay as they were.
# the drum's own fields (its `drum` layer) ; what follows the 150 Hz high-pass in the piece's own filter list, band|band
# ("" = the library's 200 Hz lift) ; the piece's gain, dB ("" = the library's 1) ; the loudness target ("" = unchanged).
# "" = v35 byte for byte. On only while PALM is; C10T5_SNARE is in HALFWAY's list of names that do not turn it off.
SNARE = os.environ.get("C10T5_SNARE", "damp=0.9 decay=0.13s wires=0.72 slap=0.9 contact=0.4;peak cutoff=230 q=1 gain=2dB|peak cutoff=1150 q=1.6 gain=-6dB|peak cutoff=4500 q=1 gain=2dB|highshelf cutoff=8000 gain=-2dB;2.5;-10.0831" if PALM else "")
# The library's piece `s` of ct-kit, written out (chirp patch show ct-kit --json, pin bffc1e5d). Written into the song's
# kit unchanged it renders the same samples as the library's (checked on the 32 strokes of the descent, alone).
SNARE_AS_IT_COMES = {"gain": "1dB", "patch": {"play": {"vel_sens": 0.65}, "synth": {"amp": {"a": "0.1ms", "curve": 1.5, "d": "140ms", "r": "30ms", "s": 0}, "drive": 0.2, "filters": ["hp cutoff=150", "peak cutoff=200 q=1 gain=5dB"], "layers": [{"beater": "stick", "cavity": 0.3, "contact": 0.6, "damp": 0.3, "decay": "0.18s", "gap": 0.1, "reso": 1.5, "reso_level": 0.7, "sharp": 30, "shell": 0.3, "shell_hz": 500, "slap": 1.2, "strike": 0.3, "type": "drum", "wire_tone": "7k", "wires": 0.85}]}}, "pitch": "A3"}


def the_snare_comes_out_of_its_box(doc):
    """v36: the snare's head is damped and shorter, its box is cut and its crack sits higher. Only the piece `s` of the
    song's kit: no note, track, fader, bus or send changes, so the nine rim strokes of the count-in (the same track,
    the piece `ss`) are as they were."""
    fields, bands, own, target = SNARE.split(";")

    def num(v):
        try:
            return float(v) if "." in v else int(v)
        except ValueError:
            return v
    kit = doc["patches"]["ct-kit-here"]
    assert "s" not in kit["kit"], kit["kit"].keys()
    players = [t["name"] for t in doc["tracks"] if any(n.get("pitch") == "s" for n in t.get("notes", []))]
    assert players == ["snare"], players                           # nobody else plays the piece
    s = json.loads(json.dumps(SNARE_AS_IT_COMES))
    layer = s["patch"]["synth"]["layers"][0]
    assert layer["type"] == "drum" and s["patch"]["synth"]["filters"][0] == "hp cutoff=150"
    for f in fields.split():
        k, v = f.split("=", 1)
        assert k in layer or k == "mode_count", k                  # a field of the drum's model
        layer[k] = num(v)
    if bands:
        s["patch"]["synth"]["filters"] = ["hp cutoff=150"] + [x for x in bands.split("|") if x]
    if own:
        s["gain"] = f"{float(own):g}dB"
    doc["patches"]["ct-kit-here"] = {**kit, "kit": {**kit["kit"], "s": s}}
    if target:
        doc["loudness"] = float(target)


# v37 (chirper-zero; instrument round: the bass. No note changes): THE BASS LEANS ON ITS OCTAVE.
# The bass was the album's bass as it comes (`ct-bass`), on all three of its tracks. Read alone beside eleven records'
# bass stems (tools/bassspec.py, a shape): under the stair 5.68 dB out: a box (+5.0, +5.0, +8.3, +10.5, +5.0 from 315
# to 800 Hz), 7.5 dB short at 80-100 Hz (the octave over its low F, where a record's bass has its weight), 5 to 9 dB
# short at 1-1.25 kHz (the string's grind); the descent's two basses 6.00 with the same box and the same missing grind.
# By muting each part in the raw mix the bass holds 2.3 to 2.5 dB of everything under 250 Hz under the stair, and the
# stair, the turn, both and the summit all read 1.2 to 1.3 dB SHORT of the records at 60-120 Hz: a line four handoffs
# carried since v25 ("the stair's 60-120 Hz 1.3 to 1.9 short"). chirper-two's v33 named the other half: with the bass
# drum on the ground's note "the sub is the kick's ... lowering the bass's sine a few dB would hand it over".
# THE FIT is the one Odd Sympathy's bass has (v40 there), in the patch's own eq and sine and nowhere else:
#   the lift at 110 Hz 6 -> 12 dB and at 220 Hz 8 -> 6 (the weight moves down to the octave over the low F);
#   the 450 Hz band becomes a 6 dB CUT at 540 Hz (the box); the 900 Hz band becomes +9 dB at 1150 Hz (the grind);
#   the sine under the string -9 -> -12 dB (the sub goes to the bass drum; it also drives the patch's compressor).
# Alone the bass is 0.3 LU louder (the grind). The fader is left: it feeds the bus's 8:1 compressor, which swallows a
# fader move (benched: 0.3 dB down on the fader read the same -26.3 LUFS alone). In the finished file no passage's
# level moves (K within 0.04 dB); the loudness target moves -10.0831 -> -10.0681 so the stretches no bass plays in
# (the foot, the pole) are where they were.
# THE DESCENT'S TWO BASSES (an octave apart under their own bell) ARE LEFT AS THEY WERE. Benched with the box, the
# grind and the sine (not the 110 Hz lift: the fall is already 1.0 to 1.1 dB over the records at 60-120 Hz): alone
# 6.00 -> 4.57, but by mute they hold nothing of the fall between 250 Hz and 1 kHz, the two windows read 0.011 nearer
# each and the finished file moved by no more than 0.05 dB in any band. A fault the mix does not show is not the
# song's. The switch's third field takes it.
# The bus `low` (the eq that follows the key, the compressor) is not touched.
# overrides on `bass` ; dB on its fader ("" = left) ; overrides on `bs0` and `bs1` ; the loudness target ("" = unchanged).
# "" = v36 byte for byte. On only while SNARE is; C10T5_LEAN is in HALFWAY's list of names that do not turn it off.
LEAN = os.environ.get("C10T5_LEAN", "fx.2.bands.0.gain=12dB fx.2.bands.1.gain=6dB fx.2.bands.2.cutoff=540 fx.2.bands.2.q=0.7 fx.2.bands.2.gain=-6dB fx.2.bands.3.cutoff=1150 fx.2.bands.3.q=1.2 fx.2.bands.3.gain=9dB synth.layers.1.level=-12dB;;;-10.0681" if SNARE else "")


def the_bass_leans_on_its_octave(doc):
    """v37: the bass's own eq and sine are refitted (its weight on the octave, its box cut, its grind up). The two
    basses of the descent only if the third field says so. A patch string: no note, fader, bus or send."""
    own, trim, fall, target = LEAN.split(";")
    by = {t["name"]: t for t in doc["tracks"]}
    assert all(by[n]["patch"] == "ct-bass" for n in ("bass", "bs0", "bs1")), [by[n]["patch"] for n in ("bass", "bs0", "bs1")]
    if own:
        by["bass"]["patch"] += " " + own
    if trim:
        assert isinstance(by["bass"]["gain"], str) and by["bass"]["gain"].endswith("dB")
        by["bass"]["gain"] = f"{float(by['bass']['gain'][:-2]) + float(trim):g}dB"
    if fall:
        for n in ("bs0", "bs1"):
            by[n]["patch"] += " " + fall
    if target:
        doc["loudness"] = float(target)


# v38 (chirper-zero; section round, w5, 1:55.2-2:24, the fall at a step a bar; no section round had worked on it):
# THE LEAD GOES BACK UP.
# The descent is "the stair, downwards, and all of it", and one by one the stair's things were given their mirror
# there: its tone (chirper-alpha, v28), its kit that changes gear (v10 for v24), its tom fill that never arrives (v5,
# which chirper-three's v23 took back up the stair), the two sides going opposite ways (v21 for v8). One thing of the
# stair's had no mirror: THE LEAD (v4), "the one honest line": over a stair that climbs for ever and is no higher,
# one guitar really comes down, two octaves, F5 to F3, a note to the half bar. The fall's first twelve bars had no
# line at all: one note a bar on eight guitars.
# Now the same guitar answers itself: over the fall that is never lower it really CLIMBS, the same thirteen notes
# backwards, F3 to F5, the same twelve half bars and the short thirteenth on the bar line. So the honest line has
# gone down two octaves and come back up two and is where it began: by walking. The band gets back to where it
# began by never having left.
# WHERE: bars 54-60 (2:09.6-2:24), and nothing was moved to fit it:
#   it comes in where the fall has gone round once and is on F again, on the low F it landed on in the stair;
#   the two tom fills that never land (v5: eight strokes into bar 54, twelve into bar 60) already stand at its two
#   ends, as chirper-three's stand at the two ends of the lead's first octave in the stair, and a crash is on each;
#   it reaches its top F on the bar line where the fall steepens and the right-hand guitars take up a climb of their
#   own (v21): the lead hands the way up to them, as in the stair it handed the way down to the guitars' run.
#   The lead goes up two steps of the scale a bar and the band comes down one, so every second bar line they are on
#   one note: F (bar 54), C (56), A flat (58), F (60).
# HOW LOUD: on the lead's own patch, pan and fader (a new last track, `ascent`). Read against the band note by note
# (raw, the mix with it less the mix without): it stands +0.45 dB (K) over the fall where the lead stands +0.44 over
# the stair; +2.6 dB at 700 Hz-1.4 kHz for +2.2. Nothing of it is above 8 kHz: the slowing hat (chirper-one, v15;
# Harry: "Yes, keep the pull") stands as it did. The notes are read from the `lead` track as it stands, so whoever
# changes the lead changes its answer.
# first bar ; the new track's fader ("" = the lead's own) ; the loudness target ("" = unchanged).
# "" = v37 byte for byte. On only while LEAN and LEAD are; C10T5_ASCENT is in HALFWAY's list of names that do not turn
# it off.
ASCENT = os.environ.get("C10T5_ASCENT", "54;;-10.0379" if LEAN and LEAD else "")


def the_lead_goes_back_up(doc):
    """v38: the stair's lead, the same thirteen notes backwards, over the fall: the same form (twelve notes a half bar
    each and a short thirteenth on the bar line), read from the `lead` track as it stands, so whoever moves the lead
    moves its answer. A new last track on the lead's own patch and pan."""
    b0, fader, target = ASCENT.split(";")
    assert LEAD, "the ascent answers the stair's lead: there is none"
    lead = next(t for t in doc["tracks"] if t["name"] == "lead")
    assert all(t["name"] != "ascent" for t in doc["tracks"]) and "ascent" not in doc.get("buses", {})
    down = sorted(lead["notes"], key=lambda n: n["at"])
    assert len(down) == 13 and all(set(n) == {"at", "len", "pitch", "vel"} for n in down), len(down)
    start = down[0]["at"]
    notes = [{"at": round(int(b0) * 4 + (n["at"] - start), 4), "len": n["len"], "pitch": back["pitch"], "vel": n["vel"]}
             for n, back in zip(down, reversed(down))]
    assert notes[-1]["at"] == int(b0) * 4 + 24 and notes[0]["pitch"] == down[-1]["pitch"]
    doc["tracks"].append({"name": "ascent", "patch": lead["patch"], "gain": f"{float(fader):g}dB" if fader else lead["gain"],
                          "pan": lead["pan"], "notes": notes})
    if target:
        doc["loudness"] = float(target)


# v39 (chirper-zero; palette round: the swap): THE PICK IS DRAGGED.
# The swap: the library's synth riser (`fx-riser-endless`, one note, 3:12.0-3:21.6) for a pick scrape on a patch of
# the song's own (`fs-scrape`), on a new last track `scrape`.
# The song's first sentence says the band plays the illusions, and one by one its synth swells have been given to
# the band: the last riser to three lead guitars (v6), the pole's line to the leads (v12), the last swell to a gong
# (chirper-one, v19, whose handoff says: "The earlier synth swell into the shared pitch/speed climb is still
# there"). This is that one. Read alone it stood 27, 16, 15 and 12 dB under everything else in its four bars (K,
# raw), a wash at 500 Hz-1 kHz under the guitars' run.
# What a guitarist does there is drag the pick's edge along the low string toward the bridge. The windings click
# under it faster and faster; when they are fast enough the clicks are a note, and the note goes on rising: in a
# pick scrape speed and pitch are one thing, which is what 'both' (the next thirty-eight seconds) is about. The
# patch is that and nothing else: one click train, from the song's sixteenth (6.67 a second) to the F three octaves
# and a bit over the low string's octave (1397 a second), an octave every 0.29 s, into the song's 5150 and cabinet.
# It plays through the run's second bar (3:19.2) and stops a sixteenth before the bar line, so the band lands alone.
# Measured, raw: the scrape stands 13 dB under everything else (K) where it starts and 0.6 under where it stops, 2.7
# OVER at 1-2 kHz in its last quarter; its peak is -14.5 dBFS. Finished: its last three sixteenths are 1.9 dB up (K),
# 3.7 at 1-2 kHz; the sixteenth after it 0.8 dB DOWN; the landing as it was, so the step onto the downbeat is 2.7 dB
# where it was 2.1 (20 dB under 120 Hz, as before). NOT HEARD IN THE MIX: the clicks you could count. The first
# sixteen stand 0.8 dB over the old file on the click (1-4 kHz): the run covers them; what is there to be heard is
# the last beat and a half, a rasp that rises. Alone, the whole of it is there.
# the bar the scrape begins in ; its length, beats ; dB on its fader ; dB its fader rises across it ; its pan ;
# "out" = the library's synth riser into 'both' is taken out (anything else: it stays) ; the loudness target ("" =
# unchanged).
# "" = v38 byte for byte. On only while ASCENT is; C10T5_SCRAPE is in HALFWAY's list of names that do not turn it off.
SCRAPE = os.environ.get("C10T5_SCRAPE", "83;3.75;6;8;0;out;" if ASCENT else "")
SCRAPE_HAND = [0.37, 0.73, 0.89, 1.33, 0.72, 1.27, -1.41, -0.1, 1.33, 0.45, 1.2, -1.16, -0.09, -0.76, 0.13, 0.22, -1.46, -0.85, -0.66, 1.25, 0.8, -1.02, 0.89, -1.08, 0.35, -1.12, -1.49, 1.11, -0.87, -0.85, 1.45]
SCRAPE_PATCH = {
    "about": "chirper-zero: a pick scrape for False Summit: the pick's edge dragged along a wound string toward the bridge. The windings click under it "
             "faster and faster: one click train whose rate follows the note's `up` (0 to 1 across the note) from the song's sixteenth to the F three "
             "octaves over the low string's octave (6.67 to 1397 clicks a second), a little unevenly (`lfo.hand`), through a peak that rises with it, "
             "into the song's 5150 and cabinet. Write the note on F1. Not a library patch.",
    "synth": {"lfo": {"hand": {"steps": SCRAPE_HAND, "rate": "83hz", "retrig": True}},
              "layers": [{"wave": "saw", "semi": {"value": -32.53, "mod": [{"src": "expr.up", "amount": 92.53}, {"src": "lfo.hand", "amount": 1}]}, "level": "0dB"}],
              "filters": [{"kind": "hp", "cutoff": 700}, {"kind": "peak", "cutoff": {"value": 700, "mod": [{"src": "expr.up", "amount": 3.0}]}, "q": 2.0, "gain": "12dB"},
                          {"cutoff": "9k", "q": 0.6}],
              "amp": {"a": "3ms", "d": "0ms", "s": 1, "r": "15ms"}},
    "fx": [{"attack": "2ms", "makeup": "3dB", "release": "60ms", "threshold": "-20dB", "type": "compressor"},
           {"bloom": 0.5, "boost": "6dB", "gain": 0.85, "mid": 0.74, "nfb": 18.0, "resonance": 0.72, "sag": 0.2, "tight": 220, "triode": True, "ts": 0.75, "type": "amp",
            "model": "5150"},
           {"mic": 0.5, "model": "4x12-modern", "type": "cab", "cone": 34},
           {"attack": "0.3ms", "hold": "5ms", "release": "12ms", "threshold": "-42dB", "type": "gate"}],
    "gain": "-23dB", "play": {"gate": 1.0, "vel_sens": 0.3}}


def the_pick_is_dragged(doc):
    """v39: one pick scrape on a new last track (the song's own patch `fs-scrape`, out to the guitars' bus), ending on
    a bar line; with "out" the library's synth riser that swelled under the same bars is taken out, and its track
    with it if nothing is left on it."""
    bar, beats, fader, swell, pan, riser, target = SCRAPE.split(";")
    at, ln = float(bar) * 4.0, float(beats)
    assert all(t["name"] != "scrape" for t in doc["tracks"]) and "scrape" not in doc.get("buses", {}) and "fs-scrape" not in doc["patches"]
    if riser == "out":
        tr = next(t for t in doc["tracks"] if t["name"] == "riser")
        tr["notes"] = [n for n in tr["notes"] if not (n["at"] < at + ln and n["at"] + n["len"] > at)]
        if not tr["notes"]:
            doc["tracks"] = [t for t in doc["tracks"] if t is not tr]
    doc["patches"] = {**doc["patches"], "fs-scrape": SCRAPE_PATCH}
    t = {"name": "scrape", "patch": "fs-scrape", "gain": f"{float(fader):g}dB", "pan": float(pan), "out": "gtrs",
         "notes": [{"at": at, "len": ln, "pitch": "F1", "vel": 0.9, "expr": {"up": 0.0}, "expr_path": {"up": [0.5, 1.0]}}]}
    if swell and float(swell):                 # the hand bears down: the fader rises across the scrape
        t["gain"] = {"value": t["gain"], "mod": [{"src": "auto.swell", "amount": 1}]}
        t["auto"] = {"swell": {"points": [["0b", -float(swell)], [f"{at:g}b", -float(swell)], [f"{at + ln:g}b", 0]], "curve": 0}}
    t["fx"] = ["hp cutoff=400"]
    doc["tracks"].append(t)
    if target:
        doc["loudness"] = float(target)


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


# v40 (chirper-zero; instrument round: THE EIGHT STAIR GUITARS' muted stroke in the descent, 1:55.2-2:52.8, 1614
# strokes. No pitch, time or length changes.) Harry, 22 Nov: "focus hard on instrument design and see if you can get
# even harder sounding guitars, bass drums etc". Read beside six records' strokes (riffpunch --strokes, the eight
# together) the descent's chug was the album's softest by one measure: ITS LOW END DIED AFTER THE STROKE (100-250 Hz in
# a stroke's first 20 ms over its 40-80 ms: +1.88 dB; the records -1.1, none over +0.3; my v35 left it at "still
# slow: said"). What cured that on other rigs did nothing on this one (the mark amp, four octaves at once): the
# string's decay under the palm +1.68, the amp's tight at 150 +2.09, both +2.25, the amp's sag out +1.73, a faster
# compressor +1.92. What does it is the engine's PHYSICAL PALM (`mute`: a hand of some width resting on the string near
# the bridge, so a muted note is a thud with a short low-mid body, not a filtered open string) with the pick half as
# soft under it: fall -1.62, punch 3.78 > 4.31, teeth -6.4 > -8.4, rise 18.5 > 10 ms. THE HAND IS ON ONLY IN THE
# DESCENT, by the note: each muted stroke there carries `expr.hand`, and the patch binds the hand to it. In the turn
# the mix refused it (the eight lose 3.9 dB at 120-250 Hz there; the mix 1.1 further at 120-500 Hz) and in 'both' it
# took 0.9 dB of the mix's 60-120 Hz from the song's climax: those two are bit for bit as they were.
# what is added to the eight's patch strings ; the beats the hand is on (FROM:TO; the descent's muted strokes run
# from beat 192.25 to 279.75: the run into the pole, 280-288, is open strings and keeps its level) ; the eight's `palm`
# lane inside them, dB ('' = left: the hand is 0.3 dB louder alone) ; the loudness target ('' = unchanged).
# "" = v39 byte for byte. On only while SCRAPE and PALM are; C10T5_HAND is in HALFWAY's list of names that do not turn it off.
HAND = os.environ.get("C10T5_HAND", "synth.layers.0.mute=expr.hand*0.8 synth.layers.0.mute_width=0.1 synth.layers.0.soft.mod.1.src=expr.hand synth.layers.0.soft.mod.1.amount=-0.5;192:280;-0.75;-10.0244" if SCRAPE and PALM else "")


def the_descent_gets_a_hand(doc):
    """v40: the eight stair guitars' muted strokes inside the span carry expr.hand = 1; the patch string binds the
    physical palm and a harder pick to it; the `palm` lane holds the eight's loudness there."""
    extra, span, trim, target = HAND.split(";")
    a, b = (float(x) for x in span.split(":"))
    eight = [i for i, t in enumerate(doc["tracks"]) if len(t["name"]) == 3 and t["name"][0] == "v" and t["name"][1] in "0123" and t["name"][2] in "lr"]
    assert len(eight) == 8
    for i in eight:
        t = doc["tracks"][i]
        assert "expr.hand" not in t["patch"] and not any("hand" in (n.get("expr") or {}) for n in t["notes"]), t["name"]
        new = {**t, "patch": t["patch"].rstrip() + " " + extra,
               "notes": [({**n, "expr": {**n["expr"], "hand": 1}} if a <= n["at"] < b and (n.get("expr") or {}).get("pm") else n) for n in t["notes"]]}
        assert sum(1 for n in new["notes"] if (n.get("expr") or {}).get("hand")) > 0, t["name"]
        if trim:
            pts, on, off, was = [], False, False, 0
            for q, v in t["auto"]["palm"]["points"]:
                x = float(q[:-1])
                if not on and x >= a:
                    if x > a:
                        pts += [[f"{a - 0.01:g}b", was], [f"{a:g}b", float(trim)]]
                    on = True
                if not off and x >= b:
                    if x > b:
                        pts += [[f"{b - 0.01:g}b", float(trim)], [f"{b:g}b", was]]
                    off = True
                pts.append([q, float(trim) if a <= x < b else v]); was = v
            assert on and off, t["name"]
            new["auto"] = {**t["auto"], "palm": {**t["auto"]["palm"], "points": pts}}
        doc["tracks"][i] = new
    if target:
        doc["loudness"] = float(target)


# v41 (chirper-zero; instrument round: THE PAIR UNDER THE STAIR, gl and gr, the 5150 rig as the library ships it:
# 560 muted strokes and 344 open ones, 0:19-1:17 and at the summit, 4:00-4:19. No note changes.) Harry, 22 Nov:
# "even harder sounding guitars". This pair was the one rig on the song no round had fitted (v35 benched a brighter
# palm on it and the mix refused the top), and stroke by stroke beside six records it was the softest on the album:
# its low end died after the stroke (100-250 Hz, the first 20 ms over 40-80 ms: +2.37 in the stair, +2.80 at the
# summit; the records -1.1, none over +0.3) and it had the fewest teeth (400 Hz-1 kHz less 1-4 kHz: -6.55; the
# records -11.3, their dullest -6.5).
#   THE STROKE HOLDS, on the rig: the engine's physical palm (a hand of some width on the string) with the pick half
#       as soft under it, the palm's thump off, the amp's tight filter 220 -> 150 Hz. One at a time, the fall:
#       hand and pick +1.62 ; thump off +1.37 ; the tighter amp +0.34. The same three without the hand: +0.98.
#       None of it adds top (teeth -6.57), which is what the mix refused at v35.
#   THE TEETH, by taking away: a cut of 4.5 dB at 650 Hz after the cabinet (teeth -9.33, punch 3.57 -> 3.80). The
#       stair is 2 dB OVER the records at 250 Hz-1 kHz and level at 2-4 kHz, so the pair gives up its box and
#       adds no top. Beside the record's lone guitar (cabspec) the pair alone goes from 2.46 dB off to 1.73.
#   The pair alone is as loud as it was (K within 0.01 dB: faders +0.22 dB).
# the tracks ; what is added to their patch strings ; an eq on each, band|band ('' = none) ; dB on their faders ;
# the loudness target ('' = unchanged). "" = v40 byte for byte. On only while HAND is; C10T5_UNDER is in HALFWAY's
# list of names that do not turn it off.
UNDER = os.environ.get("C10T5_UNDER", "gl,gr;synth.layers.0.mute=expr.pm*0.8 synth.layers.0.mute_width=0.1 synth.layers.0.soft=expr.pm*0.5 synth.layers.0.thump.mod.0.amount=0 fx.1.tight=150;peak cutoff=650 q=0.9 gain=-4.5dB;0.22;-10.0381" if HAND else "")


def the_chug_under_the_stair_holds(doc):
    """v41: the pair under the stair: overrides on its rig, one eq after it, its faders trimmed to equal loudness."""
    names, extra, eq, trim, target = UNDER.split(";")
    idx = [i for i, t in enumerate(doc["tracks"]) if t["name"] in names.split(",")]
    assert len(idx) == len(names.split(","))
    for i in idx:
        t = doc["tracks"][i]
        new = {**t, "patch": t["patch"].rstrip() + " " + extra}
        if eq:
            assert not t.get("fx"), t["name"]
            new["fx"] = [{"type": "eq", "bands": eq.split("|")}]
        if trim and float(trim):
            assert isinstance(t["gain"], dict)
            new["gain"] = {**t["gain"], "value": f"{float(t['gain']['value'][:-2]) + float(trim):g}dB"}
        doc["tracks"][i] = new
    if target:
        doc["loudness"] = float(target)


# v42: THE STAIR IS A SPIRAL (the Shepard tone under the stair, `stair`; an instrument round on Harry's 24 Nov steer for
# interesting effects and synths/environment sound; no note moves, no patch changes). The stair is the plain form of
# the illusion, and Shepard's own picture of why it works is a HELIX: pitch goes round a circle of twelve as it goes
# up, and a note an octave on stands over where it began. The tone that says the stair (Harry: "It climbed better with
# the tone under it") stood still in the middle of the stereo. Now it goes round the listener as it climbs, ONE LAP
# FOR EACH OCTAVE IT TRAVELS, so where it is IS where it is in the octave: the bar's first note straight ahead, half
# way up behind you, the top of the octave straight ahead again, where it began. A lap a bar in the foot and the
# stair (bars 0-16), a lap every two bars under the tune (16-30), a lap in three quarters of a bar in the runs (30-32,
# 82-84) ; down the descent a lap in six bars, then three, then two, then one (48-72: the fall turns faster as it
# falls faster) ; a lap a bar at the summit (101-105). In the pole (72-82) and on the last chord (105) it stands
# still, straight ahead: the published tone. (The pole was tried turning, F ahead and B behind: by level it could not
# be seen in the mix there, 90-180 Hz fell 0.65 dB on F, and the pole's stamped stretches moved away from the records.
# A metre of air is half a period of the F below middle C: I take it the tone's low partial met the pole's held chord
# the other way up.)
#   HOW: the engine's `orbit` (Chowning's moving source: the delay to each ear, the far ear's shadow, the air), a
#   circle of one metre about the listener's own place, so its distance is steady: no Doppler slide and no swell. An
#   orbit takes one rate, and its place is the song's clock times that rate, so there is ONE ORBIT FOR EACH LAP LENGTH
#   in a row on the track, each with its `mix` on a lane of its own that is 1 only in its bars ; at every hand-over
#   both are straight ahead (a `speed` lane was tried first: under one the engine adds the lap up only while the
#   track is sounding, so the tone came out of each silence part of a lap round). A lane `on` and one gain put back
#   the 1.19 dB the two ears' paths take, so the tone alone is as loud as it was (-28.871 -> -28.869 LUFS). An orbit
#   takes the track in mono: the tone's own small width (its two layers) is the orbit's now.
#   COSTS: a metre of air is 2.9 ms, so the tone is 2.9 ms late wherever it circles (four metres, tried first, was
#   11.7 ms) ; each ear hears it at most 1.2 cents sharp or flat as it passes (1.6 in the runs) ; summed to ONE
#   speaker the tone is 0.9 to 1.2 dB quieter (the foot, where it is nearly alone, 0.7 dB in the mix; elsewhere 0.1).
#   The engine's orbit turns one way, so the descent turns the same way round as the climb, slower.
# the track ; dB on a gain after the orbits wherever one is on ; the circle's radius, metres ; from:to:lap for each
# stretch, in bars (lap = a tempo-synced rate, '2/1' a lap in two bars, '@' a phase 0..1) ; the loudness target (''
# = unchanged). "" = v41 byte for byte. On only while UNDER is; C10T5_SPIRAL is in HALFWAY's list of names that do
# not turn it off.
SPIRAL = os.environ.get("C10T5_SPIRAL", "stair;1.19;1;0:16:1/1,16:30:2/1,30:32:3/4,48:60:6/1,60:66:3/1,66:68:2/1,68:72:1/1,82:84:3/4@0.6667,101:105:1/1;" if UNDER else "")


def the_stair_is_a_spiral(doc):
    """v42: the Shepard tone under the stair goes round the listener as it climbs or falls: one lap for each octave it
    travels. One `orbit` for each lap length (a circle about the listener's own place: a steady distance, no Doppler),
    in a row on the tone's track, each with its `mix` on a lane of its own that is 1 only in its bars ; a lane `on`
    is 1 wherever one of them is, and a gain makes up there what the two ears' delays take from the tone's level.
    Each orbit's place is the song's clock times its rate, so wherever one hands over to the next both are straight
    ahead (the last, the run into `both`, by its phase). Outside those bars the track is the published one."""
    name, makeup, radius, spans, target = SPIRAL.split(";")
    i, t = next((i, t) for i, t in enumerate(doc["tracks"]) if t["name"] == name)
    assert not t.get("fx") and not any(k == "on" or k[0] == "o" and k[1:].isdigit() for k in t["auto"]), t.get("fx")
    spans = [(int(a), int(b), r) for a, b, r in (sp.split(":") for sp in spans.split(","))]
    kinds = list(dict.fromkeys(r for _, _, r in spans))                # each lap length (and phase) once, in order

    def lane(bars):                                                 # 1 inside the bars, 0 outside, stepped at the bar lines
        pts, level = [["0b", 1 if any(a == 0 for a, _ in bars) else 0]], None
        edges = sorted({a for a, _ in bars} | {b for _, b in bars})
        for e in edges:
            inside = 1 if any(a <= e < b for a, b in bars) else 0
            before = 1 if any(a < e <= b for a, b in bars) else 0
            if e > 0 and inside != before:
                pts += [[f"{4 * e - 0.01:g}b", before], [f"{4 * e:g}b", inside]]
        return {"points": pts, "curve": 0}
    r = float(radius)
    fx, auto = [], dict(t["auto"])
    for k, kind in enumerate(kinds, 1):
        rate, _, phase = kind.partition("@")
        o = {"type": "orbit", "rate": rate, "radius": r if r % 1 else int(r), "distance": 0}
        if phase:
            o["phase"] = float(phase)
        o["mix"] = {"value": 0, "mod": [{"src": f"auto.o{k}", "amount": 1}]}
        fx.append(o)
        auto[f"o{k}"] = lane([(a, b) for a, b, x in spans if x == kind])
    merged = []
    for a, b, _ in spans:                                           # the bars any orbit is on, joined where they touch
        if merged and merged[-1][1] == a:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    auto["on"] = lane(merged)
    fx.append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.on", "amount": float(makeup)}]}})
    doc["tracks"] = doc["tracks"][:i] + [{**t, "fx": fx, "auto": auto}] + doc["tracks"][i + 1:]
    if target:
        doc["loudness"] = float(target)


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
