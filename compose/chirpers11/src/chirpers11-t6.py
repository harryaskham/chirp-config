#!/usr/bin/env python3
"""Small Change (Escapement, track 6). Clicky minimal techno, 122 BPM, G minor, 192 bars (6:18).

THE RULE (the coin problem). Almost nothing is written: a bass drum, a bass, and one SEED, a single struck note every
bar or two. Everything else is change given for it. A pair of COINS is two echoes, p and q sixteenths long, that
feed themselves and each other. Every pass through the p coin lifts the sound a fifth (+7 semitones); every pass
through the q coin drops it a fourth (-5). So an echo that was passed a times through p and b times through q
  lands  p*a + q*b  sixteenths after the seed,
  sounds 7*a - 5*b  semitones from it (one step round the circle of fifths for every coin spent, whichever coin),
  and is heard on the side of the last coin it went through (p left, q right).
With coins of 3 and 5 the amounts 1, 2, 4 and 7 cannot be made, and from 8 on every sixteenth can (the largest
amount that cannot is p*q - p - q): a seed is answered by a few separate notes and then by a roll. The first five
steps round the fifths from B flat are B flat, F, C, G, D: G minor's five notes. Later steps leave the key, and the
loop gain (G) is set so that they have nearly gone by then.

The form changes the coins: 3 and 5 (7 cannot be made), 3 and 4 (5: it fills at once), 5 and 7 (23: sparse and long).
Form as arithmetic: SECTIONS is the table; each row says which pairs of coins hear the seed, how often it is
struck, on which sixteenth and note, and whether the drum and the bass play.

The pitch change is the engine's granular `pitch` effect inside each loop. It is late each pass, by about 14 ms
(up) and 18 ms (down) the first time and more on later passes, so LAG is taken off each loop's time: read on the
first seed, the change then peaks between 14 ms before and 23 ms after its sixteenths (sixteenths 3 to 16).
"""
import argparse
import json
from math import log10
from pathlib import Path

BPM = 122
S16 = 60000 / BPM / 4                       # a sixteenth, ms
BAR, SEC = 16, 16                           # sixteenths in a bar; bars in a section
UP, DOWN = 7, -5                            # a fifth up through the first coin, a fourth down through the second
LAG = {UP: 19.7, DOWN: 23.8}                # ms taken off a coin's time for the pitch effect's lateness (bench: late.py, lattice.py)
G = 0.62                                    # what a coin gives back each pass (the loop loses about 4 dB more: bench)
ALONE = 0                                   # dB the seeds' faders come up where there is no drum. 0: tried at 6, the finished sections came up 1.9 dB and the rest went to the master's limiter
PAIRS = {'a': (3, 5), 'b': (3, 4), 'c': (5, 7)}
PAN = {'a': 0.6, 'b': 0.3, 'c': 0.9, 'd': 0.6, 'e': 0.3, 'h': 0.6, 'q': 0.6, 'n': 0.6, 'r': 0.6, 's': 0.6}
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t6.yaml'

# ---- v2 (26 Nov): THE COINS DO MORE THAN ECHO. Three switches that are on, each `--without-…`, and one that is off,
# `--with-denser`, waiting for an ear (all four off is v1 byte for byte).
#   HAT    what can be paid. Counting sixteenths from where the seed falls in the bar, a hat on every amount the
#          section's two coins can make, and softer the more coins it takes: with 3 and 5 that is
#          . . . X . X x . x - x - , - , - and the bar fills up like a till. Each pair has its own pattern; where two
#          or three purses share a section they take the bars in turn. With the drum come the two coins alone (3 and
#          5, one stroke each); with the bass, everything they can pay. In the two sections
#          where the seed is off the beat (sixteenth 6) the hat and the bass are counted from there too: the whole
#          till is six sixteenths round from the drum, and comes home with the seed.
#   DEBTS  what cannot be paid. The bass leaves its written line and plays the amounts no number of the two coins can
#          make (3 and 5: 1 2 4 7; 3 and 4: 1 2 5; 5 and 7: 1 2 3 4 6 8 9 11 13), never with the drum; the largest of
#          them, the last debt, is a tone lower when it is in the bar. Hat and bass never share a sixteenth.
#   TILL   each purse opens and shuts: a low-pass inside both of its loops sweeps once in p x q sixteenths (15, 12, 35),
#          the time after which the two coins' echoes of one seed first land together.
#   DENSER (OFF) the opening and the break have a seed every four bars, and its echoes are gone in two: two bars in every
#          four are silent (under -56 dB; found by rendering the seam from Hearing Things). With it, a seed every bar there
#          (every two bars still left each second bar 17 dB under the first, and the scorer no longer heard the drum
#          come). Each is SOFT dB down, so the section is about as loud as it was and has no holes. The last
#          section keeps four: the song thins out to nothing. Off because with it the scorer no longer counts the
#          drum's entry as a section (88.3 against 97), and whether the silence is a pause or a hole is not mine to say.
ON = {'hat': True, 'debts': True, 'till': True, 'denser': False, 'long': True, 'turn': True, 'chord': True, 'wait': True,
      'leave': True, 'flip': True, 'fill': True, 'smaller': True, 'inside': False, 'roll': True, 'gap': True, 'tumble': True, 'lone': True, 'grow': True, 'owed': True, 'zeno': True, 'meet': True, 'exchange': True, 'rate': True, 'seven': True, 'abroad': True, 'herald': True, 'count': True}
# ---- v10 (26 Nov): PAID ABROAD. Three more switches, each `--without-…` (with them off it is v9 byte for byte).
#   ABROAD    the bass plays what the first purse cannot pay: 1, 2, 4 and 7 sixteenths (4 falls with the drum
#             and is left to it). But two sixteenths are three of the exchange's units, and three it can pay:
#             at home, after each chord, that debt is paid abroad and the bass does not play it. The exchange's
#             first coin sounds alone where the bass's G was (it fell ON that note in v9, and the finished song
#             read 3 dB lower there for it). 1 and 7 sixteenths are one and a half and ten and a half units:
#             no currency here pays those, and the bass keeps them.
#   HERALD    the two bars before home are the wait: no drum, no bass, no hat, only what is left of the last
#             off-beat seed. On beat three of the second a seed is given to the exchange ALONE (a track only it
#             hears; the hand opens it a little after, so nothing older gets in): 3, 5, 6, 8, 9, 10, 11 of its
#             units, and 12 is the one of home. From 8 on every sixth of a beat is paid, so the change before
#             home is a roll in the other currency, filling in, a fifth up on the left and a fourth down on the
#             right: the exchange is heard on its own before it is heard against the first purse.
#   COUNT     the second hat counts that roll: one stroke on each amount the exchange can pay, 3 5 6 8 9 10 11
#             units after the herald, softer the more coins: seven strokes that close up into sixths.
HERALD = {'beat': 2, 'pitch': 'Bb4', 'db': -16, 'feed': '4dB', 'open': 0.4, 'count': -3}   # the beat of the bar before home the herald is struck on (0 is the one); its note; dB on it (the other rolls' seeds alone are at -10); what the exchange takes of it (of home's chord it takes -6 dB: here the stroke is 6 dB under what its echoes take of it); beats after it that the exchange's hand opens (its first coin comes at half a beat); dB on the second hat's strokes that count it (alone they read -41 to -46 by unit beside the coins' -37 to -50, and where nothing else plays the finished song lifts a hat's stroke to the ceiling).
# Bench (hd.sh, hdread.py, raw, by unit from the herald): at -4 dB and a feed of -6 the stroke read -27 and its highest sample -16 dBFS where the wait's is -35 and home's first bar reads -27 whole: one loud note in two quiet bars, with its coins 9 to 21 dB under it (-36 -39 -42 -45 -45 -44 -48). 6 dB off the stroke and 4 dB more to the exchange (rendered in full): the finished song lifts the wait, so the stroke's highest sample stood at -1.8 dBFS, on the ceiling, and it read -14 in its sixth of a beat over a roll at -20 to -24. Another 6 dB off the stroke and 6 more to the exchange: the roll is the event, not the note that starts it
# ---- v9 (26 Nov): THREE FOR TWO. Three more switches, each `--without-…` (with them off it is v8 byte for byte).
#   EXCHANGE  every purse in the song counts in sixteenths or in halves and quarters of them: one currency. At home
#             (bars 161 to 176: the chord, the first purse, nothing new since v2) the same seed is now also paid
#             in another: a purse with the same coins, 3 and 5, of a unit two thirds of a sixteenth (three of its
#             units for two sixteenths: six to the beat). Its 3 is an eighth, so every amount that is a multiple
#             of three lands on the song's grid, and every other amount (5, 8, 10, 11, 13 ...) between it, on
#             the triplet: the same lattice, the same fifths up on the left and fourths down on the right, the
#             same largest debt (7), at one and a half times the speed and three against two with the first
#             purse. A hand opens it for home only (its echoes go through the fader, so shut it is empty).
#   RATE      the hat plays what the first purse can pay, in sixteenths. At home a second hat, on the other
#             side, plays what the exchange can pay, in its units, where that falls BETWEEN the first hat's
#             sixteenths: 5, 8, 10 and 11 of them after each chord (inside two beats), softer the more coins
#             an amount takes, as the first hat is. Two hats counting the same sums in two currencies. (First
#             with the sums on the grid as well, 3, 6, 9 and 12: in the finished song the bass's note an eighth
#             after the chord then read 4 dB lower, the master holding down the bass, the exchange's first coin
#             and the second hat where all three fell together.)
#   SEVEN     the bass plays what the first purse cannot pay, and its largest debt (7 sixteenths) on F. At home
#             it plays the exchange's largest debt too: 7 of its units after each chord (a beat and a sixth),
#             on F: the one bass note in the song that is not on the grid.
EXCHANGE = {'coins': (3, 5), 'per': 1.5, 'back': 0.72, 'feed': '-6dB', 'pan': 0.35, 'section': 'home'}   # the exchange purse: its coins; how many of its units make a sixteenth; what each loop gives back a pass; what it takes of the seed; how far to each side; where.
# Bench (ex.sh, exread.py: the song less v8, home's first four bars, raw, by unit): taking -4 dB its coins read -33 and -32 on 3 and 5 units where the first purse's read -33 and -35 on 3 and 5 sixteenths: two lattices level with each other. 2 dB less, so that home's own leads
RATE = {'upto': 12, 'gain': '2dB', 'pan': -0.3}   # the second hat: the largest amount it plays (twelve units is two beats); its fader (the first hat's is 4 dB); its side (the first hat is at 0.15).
# Bench: at 0 dB its highest sample was -20.8 dBFS beside the first hat's -14.6: 6 dB under, a ghost. 2 dB more
# ---- v8 (26 Nov): PAID IN FULL. Two more switches, each `--without-…` (with them off it is v7 byte for byte).
#   ZENO   v7's roll pays interest and is shut on the one by a hand: right where the drum is playing, and wrong in
#          the two bars where there is none (16 and 96: before the drum first comes, and before it comes again).
#          Alone, a roll that grows ends level with the drum it is there to bring in (1 dB under its first beat),
#          and the drum does not arrive. There the change is now paid another way: in coins that shrink. After
#          the seed each gap is three quarters of the one before and each coin that much softer, so eight coins
#          and all the coins after them fit into the two beats that are left: a debt paid in full in endless
#          instalments, the last of them on the one, which is the drum. The two coins of the song take turns:
#          the odd instalments come back a fifth up on the left, the even a fourth down on the right, so the
#          roll is the next section's first note's fifth, an octave apart, closing on it.
#   MEET   since v7 the bass plays the other purses' debts where purses share a section, and there the bass
#          and the hat fall on the same sixteenths for the first time (what one purse cannot pay another can).
#          Now the hat says so: where it meets a B flat in the bass it is let ring (an open hat, a new sound,
#          over the shut one). At the peak that is six open hats in a bar of threes and fives or threes and
#          fours and two in a bar of fives and sevens: bright for two bars and plain for one, a cycle of three
#          bars over phrases of four. (First tried as the same hat 2 dB harder: 1.1 to 1.4 dB more hat in
#          every bar, and 0.3 dB between the bars: nothing anyone would hear as a meeting.)
ZENO = {'share': 0.75, 'coins': 8, 'db': -10, 'pan': 0.6, 'up': 4, 'down': 12}   # each gap, and each coin's level, as a share of the one before; how many are heard (the next is the one); dB on its seed (v6's lone seed); how far to each side; the two buses' faders.
# Bench (zeno.sh, zenoread.py: the seed and its coins alone by 60 ms): with both faders at 0 the first coin (a fifth up) stood 7 dB under the seed where 2.5 was written and the second (a fourth down) 16 where 5 was: the pitch
# effect gives a short stroke back 4.5 dB down going up and 11 going down. So 4 and 12 dB on the buses
MEET = {'gain': '-5dB', 'pan': -0.15, 'len': 0.25}   # the open hat: its fader (the shut hat's is 4 dB), its side (the shut hat is at 0.15), beats it is held.
# Bench, bars 113 to 116 raw: at -2 dB the open hat alone stood level with the shut one (-44.5 -45.2 -47.2 -44.5 by bar beside -44.8 -44.7 -46.3 -45.0) and put 4.3 to 5.2 dB on the mix above 5 kHz (it rings five times as long): too much of a lift for one sound. So 3 dB less
OPEN = {'about': "Small Change: the hat let ring, where what one purse can pay is what another owes (v8). The machine's hat, 140 ms, above 5 kHz.",
        'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '140ms'}}], 'filters': ['hp cutoff=5000'], 'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}},
        'play': {'event_stable': True, 'vel_sens': 0.8}}
# ---- v7 (26 Nov): INTEREST. Two more switches, each `--without-…` (with them off it is v6 byte for byte).
#   GROW   v6's small change before a section could only run out (a purse gives back less than it is given): it
#          was loudest on its seed, a flurry falling away into the one. Now the roll's purse pays interest: its
#          loops give back MORE than they are given, so the change grows, pass on pass, for the two beats it
#          has; and a hand is on the purse (its fader, which its own echoes go through as well) and shuts it on
#          the one. A roll that builds and is cut off by the drum. Its seed is struck that much softer.
#   OWED   the peak was not the loudest section, because the bass plays what this bar's purse cannot pay, and
#          where three purses take the bars in turn two of them have few debts. Where purses share a section
#          (both purses, three purses) the bass now also plays what the OTHER purses there cannot pay, a third
#          higher (B flat). At the peak that is the same nine strokes in every bar (1 2 3 5 6 7 9 11 13), and
#          which of them are low says whose turn it is. There, for the first time, the bass and the hat meet:
#          what one purse can pay another cannot.
GROW = {'r': ((3, 5), 2, 2.0), 's': ((3, 5), 4, 1.6)}   # the purses that pay interest: coins, how many of its units make a sixteenth, what each loop gives back each pass
# Bench, each roll by solo, level by quarter beat from its seed to the one (grow.sh, growread.py; v6's read -26 -31 -35 -35 -36 -38 -39 -41 in thirty-seconds and -25 -30 -31 -35 -37 -40 -42 -47 in sixty-fourths):
# thirty-seconds giving back 1.5: -32 -36 -41 -35 -34 -35 -32 -32 (level); 2.0: -32 -36 -40 -32 -30 -30 -25 -23 (the stroke, a breath, and then 17 dB in a beat and a quarter). Sixty-fourths 1.15: still running out; 1.4: -31 -34 -30 -31 -31 -29 -27 -30 (level); 1.6: see the round's note.
# With its seed at -8 dB the thirty-seconds' last quarter beat stood level with the drum (-23) and its highest sample at -2.6 dBFS where the rest of the mix reaches -8: so -14
GROWN = {'h': 'r', 'q': 's'}                # the roll's purse with GROW
GROW_DB = {'db': -14, 'alone': -14}         # dB on the roll's seed with the drum and without
SHUT = 0.06                                 # beats before the one over which the hand shuts the purse
OWED = 'Bb2'                                # the other purses' debts
# ---- v6 (26 Nov): SMALL CHANGE FIRST. The ending (v5) pays its last seeds in smaller and smaller coins, and until
# then nothing in the song had heard a small coin: the ending's idea arrived from nowhere. And every new section
# but two simply began. Four more switches, each `--without-…` (with them off it is v5 byte for byte).
#   ROLL   before a section begins, small change. On beat three of the last bar a seed is struck on the next
#          section's first note and paid in coins of 3 and 5 thirty-seconds where the purse stays (the drum comes,
#          the bass comes, the drum again, up a tone) and of 3 and 5 sixty-fourths where the purse is new (threes
#          and fours, both purses, fives and sevens, three purses): the same lattice at two and four times the
#          speed: a flurry a beat long before the one. None before the turn or before home (the drum waits
#          there already) and none before the last section, which lays the small coins out in order and goes
#          one size further.
#   LONE   the roll is struck where there is no drum as well (bars 16 and 96: before the drum first comes, and
#          before it comes again), which makes eight. Alone, any sound goes to the master's ceiling: at -4 dB it
#          read -15 dBFS on its beat where the opening's seeds read -18 and the drum's first beat -16; at -10
#          it reads -18, a seed like the others, and the drum still arrives.
#   GAP    the drum gives the last beat of that bar to the change: it does not play beat four.
#   TUMBLE 'off the beat, up' (bars 145 to 160) was 'off the beat' again a tone higher. Now the purse turns over at
#          every seed: inside out, the right way, inside out. The amounts are the same, so the hat and the bass
#          do not change; the quick coin's run falls in fourths on the right, then climbs in fifths on the left.
ROLL = {'same': 'h', 'new': 'q', 'beat': 2, 'db': 0, 'alone': -10}   # the purse for a roll where the coins stay and where they change; the beat of the last bar it is struck on (0 is the one); dB on its seed with the drum and without.
# Bench, by solo, at -4 dB: its seed and then 4 to 6 dB less every half beat (thirty-seconds -30 -38 -41 -45 -49; sixty-fourths -29 -35 -42 -47 -54): a flurry a beat long, not a roll that builds (a purse can only run out).
# With the drum it stood 4.5 and 6.1 dB under the mix over its two beats, and on the beat the drum gives up it was most of what was left (-42 beside -40): so 0 dB there. Where it is alone (bars 16 and 96) see LONE
# ---- v5 (26 Nov): SMALLER CHANGE. One more switch that is on (`--without-smaller`: with it off it is v4 byte for byte) and one that is off (`--with-inside`).
#   SMALLER the song ended as it began, thinner: four seeds, each with the change the first seed had. Now each of the
#           last four seeds is paid in smaller coins than the one before: 3 and 5 sixteenths (as ever), 3 and 5
#           thirty-seconds, 3 and 5 sixty-fourths, and then 3 and 5 of a unit so small that it is a pitch: the
#           period of B flat 3 (4.29 ms). At that size the coin problem is heard all at once: the amounts that
#           cannot be made (1, 2, 4, 7) are a rattle nine milliseconds long, and from 8 on every amount can be
#           made, which is an echo every 4.29 ms, which is B flat: the last seed's change is its own note, held.
#           The smallest change there is gives you back what you paid.
#   INSIDE  (OFF) the second purse (3 and 4) had no sound of its own. In the second half of its two sections (bars 57 to
#           64 and 73 to 80) it is inside out, as the first purse is at the turn: the four lifts a fifth on the
#           left and the three drops a fourth on the right (a purse `e`: 4 and 3). The amounts are the same, so the
#           hat and the bass do not change. It does what it says (by solo the quick run falls -5, -10 where it climbed
#           +7, +14). Off because the scorer reads more of the song as returning with it (0.724 of it for 0.709;
#           the band stops at 0.70) and takes 1.45 points, and because the same turn at bar 129 (FLIP) is still
#           waiting for an ear: if that one reads as a turn, put this in.
SMALL = {'h': ((3, 5), 2, 0.8), 'q': ((3, 5), 4, 0.9)}   # the smaller purses: coins, how many of its units make a sixteenth, what it gives back each pass (its passes come sooner, so it is given back more)
NOTE = {'n': ((3, 5), 233.08, 0.70, '-19dB')}   # the purse whose unit is a pitch: coins, the pitch (B flat 3), what each loop gives back of itself and of the other, what it takes of the seed.
# Bench, the last seed raw, level every 250 ms: giving back 0.62 and taking all of the seed, -17 -36 -58 -73 -88: 13 dB over the seed itself (the purse is tuned to the seed's note) and gone in a second.
# Taking 8 dB less: 0.66 -22 -36 -54 -59 -66 -77; 0.68 -22 -32 -47 -48 -51 -58 -68 -76; 0.70 -21 -28 -40 -36 -36 -40 -48 -54 -53 -54 -58 -64, and by bar -29 -58 -85 -108, which is the slope of
# the first seed's change in sixteenths (-36 -58 -83 -108): the note takes its four bars to go, and it does go. Then less of the seed again: at -13 dB the finished song's last four bars began at -9 dBFS where the three seeds before stand at -17 or -18 (a held note alone goes to the master's ceiling as a click cannot): at -19 see the round's note
LAST = 'ahqn'                               # the last section's four seeds are paid from these in turn
INSIDE = {'e': (4, 3)}                      # the second purse inside out
INSIDE_IN = ('threes and fours', 'both purses')
# ---- v4 (26 Nov): THE PURSE INSIDE OUT. The turn (bars 129 to 160, the seed off the beat) is the song's idea and
# was its quietest moment: half the drum going was all that marked it. Three more switches, each `--without-…`
# (with them off it is v3 byte for byte).
#   LEAVE  the drum waits whenever the seed changes its place in the bar: not only for it to come home (v3) but
#          for it to leave. In the two bars before the turn (127 and 128) the drum, the bass and the hat stop and
#          the three purses pay out alone; then the seed is off the beat.
#   FLIP   while the seed is off the beat the purse is inside out: the coins change hands. The five lifts a fifth
#          on the left and the three drops a fourth on the right (a fourth purse, `d`: 5 and 3). The same amounts
#          can be made, so the hat and the bass do not change; what changes is which way the quick coin goes: the
#          three's own run (3, 6, 9 sixteenths) now falls in fourths under the seed where it climbed in fifths
#          over it, and the slow coin climbs. At home the purse is the right way out again.
#   FILL   the break's purse (5 and 7) is given back more than the opening's. Its coins are long, so its change
#          makes fewer notes a bar and every fourth bar of the break was under -52 dB (see G_FILL).
G_FILL = 1.35                               # what the break's long purse gives back each pass. Bench, the break raw, level by bar after each of its four seeds: 1.05 -40 -48 -63 -80 / -40 -48 -56 -83; 1.2 -39 -43 -57 -71; 1.35 -39 -39 -51 -63 / -39 -40 -43 -68; 1.5 -38 -36 -46 -55 (its second bar louder than its first: too near the edge)
FLIPPED = {'d': (5, 3)}                     # the purse inside out
# ---- v3 (26 Nov): WHAT IS GIVEN BACK. Four more switches, each `--without-…` (with them off it is v2 byte for byte).
#   LONG   the purse that keeps its change. In the opening and the break a seed came every four bars and its echoes
#          were gone in two (two silent bars in every four; v2 could only fill them with more seeds, and then the
#          drum's entry stopped being an event). Those seeds now go into a second pair of loops that give back
#          G_LONG of every pass where the others give back G: one seed, four bars of change.
#   TURN   where the seed is off the beat (bars 129 to 160) the drum gives up beats two and four. The till is six
#          sixteenths round from the drum, and now there is room to hear that it is: the seed falls between two
#          drums, not on top of one. The drum is whole again when the seed comes home.
#   WAIT   the drum waits for the seed to come home. In the last two bars before home (159 and 160) the drum, the
#          bass and the hat stop; the last off-beat seed's change is paid out alone; and home lands whole on the one.
#   CHORD  home is a chord. In the section where the seed comes back onto the one (bars 161 to 176) it is struck as
#          G minor (G4 B flat 4 D5). Every coin moves a note a fifth, so the purse walks the chord round the
#          fifths: G minor, D minor, A minor, each quieter. The only chords in the song, and nobody wrote the changes.
G_LONG = 1.05                               # what the long purse gives back each pass: more than it is given, and it still runs out (every pass also moves the note, until it is out of hearing). Bench, level by bar after one seed: 0.62 -35 -58 -79 -104; 0.9 -35 -46 -56 -68; 1.0 -34 -42 -49 -58; 1.1 -34 -39 -42 -48
HOME = ('G4', 'Bb4', 'D5')                  # the chord
LONG_DB = -6                                # on the seeds that go into the long purse. At 0 the master's limiter held the lone seed down 9 dB and its change came up to it: the opening read as loud as the drum (-16 -17 -22 -29 dB a bar against -15) and the drum's entry stopped being an event
HOME_DB = -6                                # on each of its three notes, so the three together stand where one seed did (at -8 the chord's section read 2 dB under the single seeds': -10.0 against -8.0 beside the mix)
WAIT = 2                                    # bars the drum waits before home
SOFT = -6                                   # dB on each seed where DENSER strikes every bar: four times the strokes, the section about as loud as it was
TILL = (3900, 1.35)                         # the sweep's middle, Hz, and its reach each way, octaves (to v1's 10 kHz at the top)
HAT = {'about': "Small Change: the hat that plays what can be paid. The machine's hat, 30 ms, above 6 kHz.",
       'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '30ms'}}], 'filters': ['hp cutoff=6000'], 'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '100ms'}},
       'play': {'event_stable': True, 'vel_sens': 0.8}}


def coins(p, q, upto=BAR - 1):
    """{amount: the fewest coins that make it} for every amount up to `upto` the two coins can make."""
    out = {}
    for a in range(upto // p + 1):
        for b in range((upto - p * a) // q + 1):
            if a + b:
                out[p * a + q * b] = min(a + b, out.get(p * a + q * b, 99))
    return dict(sorted(out.items()))


def debts(p, q, upto=BAR - 1):
    """The amounts up to `upto` that no number of the two coins can make."""
    return [s for s in range(1, upto + 1) if s not in coins(p, q, upto)]

# name, pairs that hear the seed (in turn, one per strike), bars between strikes, sixteenth of the bar, seed notes in turn, drum, bass
SECTIONS = [
    ('one seed',            'a',   4, 0, ['Bb4'],               0, 0),
    ('the drum',            'a',   2, 0, ['Bb4'],               1, 0),
    ('the bass',            'a',   2, 0, ['Bb4', 'Eb4'],        1, 1),
    ('threes and fours',    'b',   2, 0, ['Bb4'],               1, 1),
    ('both purses',         'ab',  1, 0, ['Bb4', 'F4'],         1, 1),
    ('fives and sevens',    'c',   4, 0, ['Eb4', 'F4'],         0, 0),
    ('the drum again',      'c',   2, 0, ['Eb4', 'F4'],         1, 1),
    ('three purses',        'abc', 1, 0, ['Bb4', 'F4', 'Eb4'],  1, 1),
    ('off the beat',        'a',   2, 6, ['Eb4'],               1, 1),
    ('off the beat, up',    'a',   2, 6, ['F4'],                1, 1),
    ('home',                'a',   2, 0, ['Bb4'],               1, 1),
    ('the last seed',       'a',   4, 0, ['Bb4'],               0, 0),
]
BARS = len(SECTIONS) * SEC

PATCHES = {
    'sc-seed': {'about': 'Small Change: the seed. One vibraphone bar with no motor, short, with two milliseconds of noise on its front (a click that the coins carry too): the only struck note in the song.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '180ms', 'bright': 0.6, 'strike': 0.3},
                                     {'type': 'noise', 'color': 'white', 'level': {'value': '-80dB', 'mod': [{'src': 'env.tick', 'amount': 70}]}}],
                          'env': {'tick': {'a': '0.1ms', 'd': '2ms', 's': 0, 'r': '2ms'}},
                          'amp': {'a': '0.3ms', 'd': '250ms', 's': 0, 'r': '80ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'sc-kick': {'about': "Small Change: the drum. The machine's bass drum on G, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.5, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
}


def purses():
    """The pairs of coins in use: PAIRS, and with FLIP the purse inside out."""
    return {**PAIRS, **(FLIPPED if ON['flip'] else {}), **(INSIDE if ON['inside'] else {}),
            **({k: v[0] for k, v in {**SMALL, **NOTE}.items()} if ON['smaller'] else {k: v[0] for k, v in SMALL.items()} if ON['roll'] else {}),
            **({k: v[0] for k, v in GROW.items()} if ON['grow'] and ON['roll'] else {})}


def unit(k):
    """A purse's unit, ms: a sixteenth, or for the smaller purses a part of one, or a pitch's period."""
    return S16 / SMALL[k][1] if k in SMALL else S16 / GROW[k][1] if k in GROW else 1000 / NOTE[k][1] if k in NOTE else S16


def coins_for(amount, p, q):
    """The fewest coins that make an amount, or None."""
    ways = [a + (amount - p * a) // q for a in range(amount // p + 1) if (amount - p * a) % q == 0]
    return min(ways) if ways else None


def frobenius(p, q):
    return p * q - p - q


def lattice(p, q, upto):
    """{sixteenth: [semitones, ...]} for every way of making it from the two coins."""
    out = {}
    for a in range(upto // p + 1):
        for b in range((upto - p * a) // q + 1):
            if a + b:
                out.setdefault(p * a + q * b, []).append(UP * a + DOWN * b)
    return dict(sorted(out.items()))


def rolls():
    """{bar: (purse, note)} for the rolls: the last bar of every section but the last two, where the drum does not already wait."""
    out = {}
    for i, sec in enumerate(SECTIONS[:-2]):
        nxt = SECTIONS[i + 1]
        if (ON['leave'] and sec[5] and nxt[5] and nxt[3] and not sec[3]) or (ON['wait'] and nxt[0] == 'home'):
            continue                                             # the drum waits there
        if not sec[5] and not ON['lone']:
            continue                                             # no drum in this section: the roll would be alone
        out[(i + 1) * SEC - 1] = (ROLL['new' if nxt[1] != sec[1] else 'same'], nxt[4][0])
    out = {b: (GROWN[k], n) for b, (k, n) in out.items()} if ON['grow'] else out
    return {b: ('z' if ON['zeno'] and not SECTIONS[b // SEC][5] else k, n) for b, (k, n) in out.items()}   # v8: where there is no drum, the purse of shrinking coins


def hand():
    """The hand on a purse that pays interest: shut, open from each roll's seed, and shut again on the one."""
    pts = [['0b', -60]]
    for b in sorted(rolls()):
        pts += [[f"{b * 4 + ROLL['beat'] - 0.05}b", -60], [f"{b * 4 + ROLL['beat']}b", 0], [f'{(b + 1) * 4 - SHUT}b', 0], [f'{(b + 1) * 4}b', -60]]
    return {'points': pts + [[f'{BARS * 4}b', -60]], 'curve': 0}


def build():
    T = {'kick': [], 'bass': [], 'hat': [], **{f'seed-{k}': [] for k in purses()}, **({'seed-z': []} if ON['zeno'] and ON['roll'] else {}), **({'open': []} if ON['meet'] and ON['owed'] and ON['hat'] else {}), **{f'long-{k}': [] for k in purses()}}
    if (ON['rate'] or (ON['count'] and ON['herald'])) and ON['exchange'] and ON['hat']:
        T['hat-x'] = []
    if ON['herald'] and ON['exchange']:
        T['seed-x'] = []
    for i, (name, pairs, every, at16, notes, drum, bass) in enumerate(SECTIONS):
        n = 0
        if ON['flip'] and at16:                                  # off the beat: the purse inside out
            pairs = ''.join('d' if k == 'a' else k for k in pairs)
            if ON['tumble'] and name == 'off the beat, up':      # v6: and the right way, and inside out, seed by seed
                pairs = ''.join(k + 'a' if k == 'd' else k for k in pairs)
        dense = ON['denser'] and not drum and i < len(SECTIONS) - 1
        if dense:
            every = 1
        whole = pairs
        for bar in range(i * SEC, (i + 1) * SEC):
            if ON['inside'] and name in INSIDE_IN:               # its second half: the second purse inside out
                pairs = ''.join('e' if k == 'b' else k for k in whole) if bar - i * SEC >= SEC // 2 else whole
            if ON['smaller'] and i == len(SECTIONS) - 1:         # the last seeds: each paid in smaller coins
                pairs = LAST[(bar - i * SEC) // every % len(LAST)]
            if (bar - i * SEC) % every == 0:
                kept = ON['long'] and not drum and i < len(SECTIONS) - 1          # the opening and the break: into the long purse
                home = ON['chord'] and name == 'home'
                for pitch in (HOME if home else [notes[n % len(notes)]]):
                    T[f"{'long' if kept else 'seed'}-{pairs[n % len(pairs)]}"].append({'at': bar * 4 + at16 / 4, 'len': 0.25, 'pitch': pitch, 'vel': 0.9,
                                                                                    **({'gain': f'{SOFT}dB'} if dense else {'gain': f'{HOME_DB}dB'} if home else {'gain': f'{LONG_DB}dB'} if kept and LONG_DB else {})})
                if ON['rate'] and 'hat-x' in T and name == EXCHANGE['section']:   # v9 RATE: what the exchange can pay of this seed, in its units
                    for amount in range(1, RATE['upto'] + 1):
                        if coins_for(amount, *EXCHANGE['coins']) and (amount / EXCHANGE['per']) % 1:   # only the sums that fall between the sixteenths
                            T['hat-x'].append({'at': round(bar * 4 + at16 / 4 + amount / (4 * EXCHANGE['per']), 4), 'len': 0.1, 'pitch': 'A#4', 'vel': round(.95 - .13 * (coins_for(amount, *EXCHANGE['coins']) - 1), 2)})
                if ON['seven'] and ON['exchange'] and ON['debts'] and bass and name == EXCHANGE['section']:   # v9 SEVEN: the exchange's largest debt, in the bass
                    T['bass'].append({'at': round(bar * 4 + at16 / 4 + frobenius(*EXCHANGE['coins']) / (4 * EXCHANGE['per']), 4), 'len': 0.25, 'pitch': 'F2', 'vel': .85})
                n += 1
            waits = ON['wait'] and i + 1 < len(SECTIONS) and SECTIONS[i + 1][0] == 'home' and bar >= (i + 1) * SEC - WAIT
            waits = waits or (ON['leave'] and i + 1 < len(SECTIONS) and drum and SECTIONS[i + 1][5] and SECTIONS[i + 1][3] and not at16 and bar >= (i + 1) * SEC - WAIT)
            if 'seed-x' in T and i + 1 < len(SECTIONS) and SECTIONS[i + 1][0] == EXCHANGE['section'] and bar == (i + 1) * SEC - 1:   # v10 HERALD: the change before home, in the other currency
                T['seed-x'].append({'at': bar * 4 + HERALD['beat'], 'len': 0.25, 'pitch': HERALD['pitch'], 'vel': 0.9, 'gain': f"{HERALD['db']}dB"})
                if ON['count'] and 'hat-x' in T:                 # v10 COUNT: the second hat on every amount it can pay, to the one
                    T['hat-x'] += [{'at': round(bar * 4 + HERALD['beat'] + a / (4 * EXCHANGE['per']), 4), 'len': 0.1, 'pitch': 'A#4', 'vel': round(.95 - .13 * (coins_for(a, *EXCHANGE['coins']) - 1), 2), 'gain': f"{HERALD['count']}dB"}
                                   for a in range(1, round((4 - HERALD['beat']) * 4 * EXCHANGE['per'])) if coins_for(a, *EXCHANGE['coins'])]
            if ON['roll'] and bar in rolls():                    # v6: small change before the next section
                level = ZENO['db'] if rolls()[bar][0] == 'z' else (GROW_DB if ON['grow'] else ROLL)['db' if drum else 'alone']
                T[f'seed-{rolls()[bar][0]}'].append({'at': bar * 4 + ROLL['beat'], 'len': 0.25, 'pitch': rolls()[bar][1], 'vel': 0.9, **({'gain': f"{level}dB"} if level else {})})
            if waits:                                            # the bars before home, or before the turn: only the purse
                continue
            if drum:
                for beat in range(4):
                    if ON['turn'] and at16 and beat % 2:         # off the beat: the drum gives up two and four
                        continue
                    if ON['gap'] and ON['roll'] and bar in rolls() and beat == 3:   # v6: the last beat is the change's
                        continue
                    T['kick'].append({'at': bar * 4 + beat, 'len': 0.5, 'pitch': 'G1', 'vel': .95 if beat == 0 else .88})
            pq = purses()[pairs[(bar - i * SEC) % len(pairs)]]  # the purse whose turn this bar is
            others = []
            if bass and ON['debts']:
                for s in debts(*pq):
                    if ON['abroad'] and ON['exchange'] and name == EXCHANGE['section'] and (bar - i * SEC) % every == 0 and (s * EXCHANGE['per']) % 1 == 0 and coins_for(round(s * EXCHANGE['per']), *EXCHANGE['coins']):
                        continue                                 # v10 ABROAD: the exchange pays this one
                    if (at16 + s) % 4:                           # never with the drum
                        T['bass'].append({'at': bar * 4 + (at16 + s) % BAR / 4, 'len': 0.25, 'pitch': 'F2' if s == frobenius(*pq) else 'G2', 'vel': .85})
                others = sorted({s for k in set(pairs) for s in debts(*purses()[k])} - set(debts(*pq))) if ON['owed'] else []   # v7: what the section's other purses cannot pay
                for s in others:
                    if (at16 + s) % 4:
                        T['bass'].append({'at': bar * 4 + (at16 + s) % BAR / 4, 'len': 0.25, 'pitch': OWED, 'vel': .85})
                if others:
                    T['bass'][-BAR:] = sorted(T['bass'][-BAR:], key=lambda x: x['at'])
            elif bass:
                for off, ln, p in ((2, 1.5, 'G2'), (7, 1, 'G2'), (10, 1.5, 'F2' if bar % 4 == 3 else 'G2')):
                    T['bass'].append({'at': bar * 4 + off / 4, 'len': ln / 4, 'pitch': p, 'vel': .85})
            if drum and ON['hat']:
                for s, n_coins in coins(*pq).items():
                    if bass or n_coins == 1:                     # before the bass comes, only the two coins themselves
                        T['hat'].append({'at': bar * 4 + (at16 + s) % BAR / 4, 'len': 0.1, 'pitch': 'A#4', 'vel': round(.95 - .13 * (n_coins - 1), 2)})
                        if 'open' in T and s in others and (at16 + s) % 4:   # v8 MEET: it falls with one of the other purses' debts
                            T['open'].append({**T['hat'][-1], 'len': MEET['len']})
    if ON['seven'] and ON['exchange']:
        T['bass'].sort(key=lambda n: n['at'])
    return T


def alone():
    """The seeds' fader ride: ALONE dB through the sections with no drum, 0 elsewhere, moved over the half beat before a section."""
    pts = []
    for i, sec in enumerate(SECTIONS):
        v = 0 if sec[5] else ALONE
        if pts and pts[-1][1] != v:
            pts.append([f'{i * SEC * 4 - 0.5}b', pts[-1][1]])
        if not pts or pts[-1][1] != v:
            pts.append([f'{i * SEC * 4}b', v])
    return {'points': pts + [[f'{BARS * 4}b', pts[-1][1]]], 'curve': 0}


def song():
    T = build()
    db = lambda x: f'{20 * log10(x):.2f}dB'
    under = {'type': 'pump', 'on': 'kick', 'depth': '-4dB', 'release': '170ms'}
    buses = {}
    for k, (p, q) in purses().items():
        gl = G_FILL if ON['fill'] and k == 'c' else G_LONG
        u, g = unit(k), SMALL[k][2] if k in SMALL else GROW[k][2] if k in GROW else G
        for coin, other, semi, side in ((p, q, UP, -1), (q, p, DOWN, 1)):
            me, you = f'{k}{coin}', f'{k}{other}'
            if k in NOTE:                                        # coins too small for the pitch effect, and too small to need it: the purse is the pitch
                t = f'{coin * u:.3f}ms'
                buses[me] = {'pan': side * PAN[k], 'gain': '0dB', 'fx': ['lp cutoff=6000', 'hp cutoff=40'],   # the high-pass at 150 Hz, as in the other purses, is early in phase at 466 Hz: the note read 13 cents sharp under in-tune harmonics
                             'returns': [{'from': f'seed-{k}', 'gain': NOTE[k][3], 'time': t}, {'from': me, 'gain': db(NOTE[k][2]), 'time': t}, {'from': you, 'gain': db(NOTE[k][2]), 'time': t}]}
                continue
            t = f'{coin * u - LAG[semi]:.2f}ms'
            buses[me] = {'pan': side * PAN[k], 'gain': '0dB',
                         'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, f'lp cutoff={TILL[0]}+lfo.till*{TILL[1]}' if ON['till'] else 'lp cutoff=10000', 'hp cutoff=150'],
                         **({'lfo': {'till': f'sine rate={1000 / (p * q * u):.4f}hz'}} if ON['till'] else {}),
                         'returns': [{'from': f'seed-{k}', 'gain': '0dB', 'time': t}, {'from': me, 'gain': db(g), 'time': t}, {'from': you, 'gain': db(g), 'time': t}]}
            if k in GROW:                                        # v7: the hand on the purse (its own echoes go through the fader too)
                buses[me] = {**buses[me], 'gain': {'value': '0dB', 'mod': [{'src': 'auto.hand', 'amount': 1}]}, 'auto': {'hand': hand()}}
            if ON['long'] and T[f'long-{k}']:                   # the same two loops again, giving back more
                buses[me + 'L'] = {**buses[me], 'returns': [{'from': f'long-{k}', 'gain': '0dB', 'time': t}, {'from': me + 'L', 'gain': db(gl), 'time': t}, {'from': you + 'L', 'gain': db(gl), 'time': t}]}
    doc = {
        'about': "Chirpers, Escapement, track 6: Small Change, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t6.py (its docstring is the rule). One struck note every bar or two, a bass drum and a bass are all that is written; the rest is change given for it by pairs of coins: two echoes, p and q sixteenths long, feeding themselves and each other, one lifting the sound a fifth each pass and the other dropping it a fourth. An echo lands p*a + q*b sixteenths after its seed, 7*a - 5*b semitones from it.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Small Change', 'track': 6, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{BARS * 4}b', 'tail': '5s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -12,
        'patches': PATCHES, 'buses': buses,
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [{'name': 'kick', 'patch': 'sc-kick', 'gain': '-9dB', 'notes': T['kick'],
                    'fx': [{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]},
                   {'name': 'bass', 'patch': 'sub-sine', 'gain': '-13dB', 'notes': T['bass'], 'fx': [under]}] +
                  [{'name': f'seed-{k}', 'patch': 'sc-seed', 'gain': {'value': '-3dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()},
                    'notes': T[f'seed-{k}'], 'fx': ['clip drive=0dB ceiling=-12dB']} for k in purses()],   # the seed's highest sample is its own, not the limiter's
    }
    if T.get('seed-z'):                                          # v8 ZENO: a seed of its own, and its change in shrinking coins: no loop, one echo a coin, the two pitches taking turns
        doc['tracks'].append({'name': 'seed-z', 'patch': 'sc-seed', 'gain': {'value': '-3dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()}, 'notes': T['seed-z'], 'fx': ['clip drive=0dB ceiling=-12dB']})
        r, n = ZENO['share'], ZENO['coins']
        gap = (4 - ROLL['beat']) * 60000 / BPM * (1 - r) / (1 - r ** (n + 1))        # so that coin n + 1 would fall on the one
        for name, semi, side, js in (('zu', UP, -1, range(1, n + 1, 2)), ('zd', DOWN, 1, range(2, n + 1, 2))):
            buses[name] = {'pan': side * ZENO['pan'], 'gain': f"{ZENO['up' if semi == UP else 'down']}dB", 'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, 'hp cutoff=150'],
                           'returns': [{'from': 'seed-z', 'gain': f'{20 * log10(r) * j:.2f}dB', 'time': f'{gap * (1 - r ** j) / (1 - r) - LAG[semi]:.2f}ms'} for j in js]}
    if ON['exchange']:                                           # v9: the same seed in another currency: a purse of the same coins in units two thirds of a sixteenth, open for home only
        i = [sec[0] for sec in SECTIONS].index(EXCHANGE['section'])
        (p, q), u = EXCHANGE['coins'], S16 / EXCHANGE['per']
        opens = i * SEC * 4 - (4 - HERALD['beat'] - HERALD['open'] if T.get('seed-x') else 0)   # v10: with the herald, a little after it
        hand_x = {'points': [['0b', -60], [f'{opens - 0.05}b', -60], [f'{opens}b', 0], [f'{(i + 1) * SEC * 4 - 1}b', 0], [f'{(i + 1) * SEC * 4}b', -60], [f'{BARS * 4 + 16}b', -60]], 'curve': 0}
        for coin, other, semi, side in ((p, q, UP, -1), (q, p, DOWN, 1)):
            t = f'{coin * u - LAG[semi]:.2f}ms'
            buses[f'x{coin}'] = {'pan': side * EXCHANGE['pan'], 'gain': {'value': '0dB', 'mod': [{'src': 'auto.rate', 'amount': 1}]}, 'auto': {'rate': hand_x},
                                 'fx': [{'type': 'pitch', 'semitones': semi, 'mix': 1}, f'lp cutoff={TILL[0]}+lfo.till*{TILL[1]}' if ON['till'] else 'lp cutoff=10000', 'hp cutoff=150'],
                                 **({'lfo': {'till': f'sine rate={1000 / (p * q * u):.4f}hz'}} if ON['till'] else {}),
                                 'returns': [{'from': f"seed-{SECTIONS[i][1][0]}", 'gain': EXCHANGE['feed'], 'time': t}] + ([{'from': 'seed-x', 'gain': HERALD['feed'], 'time': t}] if T.get('seed-x') else []) +
                                            [{'from': f'x{coin}', 'gain': db(EXCHANGE['back']), 'time': t}, {'from': f'x{other}', 'gain': db(EXCHANGE['back']), 'time': t}]}
    for k in purses():
        if ON['long'] and T[f'long-{k}']:
            doc['tracks'].append({'name': f'long-{k}', 'patch': 'sc-seed', 'gain': {'value': '-3dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()},
                                  'notes': T[f'long-{k}'], 'fx': ['clip drive=0dB ceiling=-12dB']})
    if T.get('seed-x') and ON['exchange']:                       # v10 HERALD: a seed only the exchange hears
        doc['tracks'].append({'name': 'seed-x', 'patch': 'sc-seed', 'gain': '-3dB', 'notes': T['seed-x'], 'fx': ['clip drive=0dB ceiling=-12dB']})
    if T.get('open'):
        doc['patches'] = {**doc['patches'], 'sc-open': OPEN}
        doc['tracks'].append({'name': 'open', 'patch': 'sc-open', 'gain': MEET['gain'], 'pan': MEET['pan'], 'notes': T['open']})
    if ON['hat']:
        doc['patches'] = {**doc['patches'], 'sc-hat': HAT}
        doc['tracks'].append({'name': 'hat', 'patch': 'sc-hat', 'gain': '4dB', 'pan': 0.15, 'notes': T['hat']})
        if T.get('hat-x'):                                       # v9 RATE: the second hat, on the other side
            doc['tracks'].append({'name': 'hat-x', 'patch': 'sc-hat', 'gain': RATE['gain'], 'pan': RATE['pan'], 'notes': T['hat-x']})
    return doc


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == 'tracks':
            lines.append('tracks:')
            lines += ['  - ' + json.dumps(t) for t in v]
        else:
            lines.append(f'{k}: {json.dumps(v)}')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--form', action='store_true', help='print the form and the coins and stop')
    for k, on in ON.items():
        ap.add_argument(f"--{'without' if on else 'with'}-{k}", action='store_true', help=f"{'leave out' if on else 'put in'} {k} (of those that are on: the last three off is v9, the last six v8, the last eight v7, the last ten v6, the last fourteen v5, the last fifteen v4, the last eighteen v3, the last twenty-two v2, all twenty-five v1)")
    a = ap.parse_args()
    for k, on in list(ON.items()):
        ON[k] = on != getattr(a, f"{'without' if on else 'with'}_{k}")
    if a.form:
        sec = 60 / BPM * 4
        for k, (p, q) in purses().items():
            lat = lattice(p, q, 24)
            print(f'coins {k}: {p} and {q}; largest amount that cannot be made {frobenius(p, q)}; made up to 24: ' + ' '.join(f'{s}:{"/".join(f"{x:+d}" for x in v)}' for s, v in lat.items()))
        for i, (name, pairs, every, at16, notes, drum, bass) in enumerate(SECTIONS):
            b = i * SEC
            every = 1 if ON['denser'] and not drum and i < len(SECTIONS) - 1 else every
            pairs = ''.join('d' if k == 'a' else k for k in pairs) if ON['flip'] and at16 else pairs
            pairs = pairs.replace('d', 'da') if ON['tumble'] and ON['flip'] and name == 'off the beat, up' else pairs
            print(f'{i + 1:2d}  bars {b + 1:3d}-{b + SEC:3d}  {int(b * sec) // 60}:{b * sec % 60:05.2f}  {name:20s} coins {pairs:3s} a seed every {every} bar(s) on sixteenth {at16} {"/".join(notes):12s} {"drum " if drum else ""}{"bass" if bass else ""}')
        if ON['inside']:
            print(f"    in the second half of {' and '.join(INSIDE_IN)} purse b is inside out (e: 4 and 3)")
        if ON['smaller']:
            print(f"    the last section's four seeds are paid from {' '.join(LAST)}: coins of 3 and 5 sixteenths, thirty-seconds, sixty-fourths, and periods of B flat 3 ({unit('n'):.2f} ms)")
        if ON['roll']:
            print('    small change before a section: ' + ', '.join(f"bar {b + 1} ({'shrinking coins' if k == 'z' else 'thirty-seconds' if k in (ROLL['same'], GROWN[ROLL['same']]) else 'sixty-fourths'}, {n})" for b, (k, n) in rolls().items()) + ('; the drum gives up beat four there' if ON['gap'] else '') + ('; the roll grows and is shut on the one' if ON['grow'] else ''))
        if ON['exchange']:
            print(f"    {EXCHANGE['section']} is also paid in another currency: coins of {EXCHANGE['coins'][0]} and {EXCHANGE['coins'][1]} of a unit two thirds of a sixteenth (three for two): amounts " + ' '.join(str(a) for a in range(1, 25) if coins_for(a, *EXCHANGE['coins'])) + '; on the grid where the amount is a multiple of three')
        if ON['rate'] and ON['exchange'] and ON['hat']:
            print(f"    a second hat plays what the exchange can pay, in its units, up to {RATE['upto']}, where it falls between the sixteenths: " + ' '.join(str(a) for a in range(1, RATE['upto'] + 1) if coins_for(a, *EXCHANGE['coins']) and (a / EXCHANGE['per']) % 1))
        if ON['abroad'] and ON['exchange'] and ON['debts']:
            print(f"    at {EXCHANGE['section']}, after each chord, the bass leaves the debts the exchange can pay: " + ', '.join(f"{s} sixteenths ({round(s * EXCHANGE['per'])} of its units)" for s in debts(*purses()['a']) if (s * EXCHANGE['per']) % 1 == 0 and coins_for(round(s * EXCHANGE['per']), *EXCHANGE['coins'])))
        if ON['herald'] and ON['exchange']:
            print(f"    the change before {EXCHANGE['section']} is in the other currency: a seed for the exchange alone on beat {HERALD['beat'] + 1} of the bar before, {HERALD['pitch']}" + ('; the second hat counts it: ' + ' '.join(str(a) for a in range(1, round((4 - HERALD['beat']) * 4 * EXCHANGE['per'])) if coins_for(a, *EXCHANGE['coins'])) + ' units' if ON['count'] and ON['hat'] else ''))
        if ON['seven'] and ON['exchange'] and ON['debts']:
            print(f"    the bass plays the exchange's largest debt: {frobenius(*EXCHANGE['coins'])} of its units after each chord, on F2")
        if ON['meet']:
            print('    the hat is let ring where it meets one of the other purses\' debts in the bass')
        if ON['owed']:
            print(f'    where purses share a section the bass also plays what the others cannot pay, on {OWED}: ' + '; '.join(f"{name}: " + ', '.join(f"{k} {' '.join(str(s) for s in sorted(set(debts(*purses()[k])) | {s for j in pairs for s in debts(*purses()[j])}) if s % 4)}" for k in pairs) for name, pairs, *_ in SECTIONS if len(pairs) > 1))
        T = build()
        print(f'{BARS} bars, {BARS * sec:.1f} s; written notes: ' + ', '.join(f'{k} {len(v)}' for k, v in T.items() if v or not k.startswith('long-')))
    else:
        a.out.write_text(dump(song()))
