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
# the illusion alone at the foot and has been back under the stair since v14, under the pole and at the summit.
# But the descent is "the stair the other way, and all of it", twenty-four bars of a tuning that keeps dropping
# and is never lower, and it has had no tone: the one illusion of pitch in the song the band carries alone. Now
# the tone says the fall as plainly as it says the climb: ONE HELD NOTE FOR EACH STEP THE RIFF FALLS, the step's
# own note (F, E flat, C, B, A flat, G flat, and round), on the same fader and the same lane as under the stair.
# So it also tells how steep the fall is, which nothing but the riff's own notes did: a step a bar for twelve
# bars (2.4 s a note), two a bar from 2:24 (where since v21 the right-hand guitars climb against it: the tone
# goes with the fall), three from 2:38.4, and from 2:43.2 six a bar: the stair's own line and rhythm, backwards,
# through the guitars' run into the pole, where the tone is alone again.
# (Level, benched raw: under the stair, where he chose it, the tone stands 12.8 dB under the band, K-weighted. A
# held note sits lower than the stair's short ones: at the same fader it stood 15.1 under where the fall is a step a
# bar and 14.9 at two, and 13.7 at six, where its notes are the stair's own. So it has 1 dB more until the fall
# is six steps a bar: 14.1, 13.9, 13.1, then 13.7 and, over the guitars' run, 12.8.)
# dB on the tone under the descent, against its level under the stair ; the bar from which it is at the stair's
# own level again ; the loudness target ("" = unchanged). "" = v27.
FALLTONE = os.environ.get("C10T5_FALLTONE", "1;68;-9.975" if TICKTONE else "")


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
    for bar, lvl in ((FOOT + 4, float(synth[3])), (RISE, under), *falls, (POLE, float(synth[4])), (BOTH - (int(RUNS.split(";")[0]) if RUNS else 0), under)):
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
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
