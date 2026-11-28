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
from math import log10, log2
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
      'leave': True, 'flip': True, 'fill': True, 'smaller': True, 'inside': False, 'roll': True, 'gap': True, 'tumble': True, 'lone': True, 'grow': True, 'owed': True, 'zeno': True, 'meet': True, 'exchange': True, 'rate': True, 'seven': True, 'abroad': True, 'herald': True, 'count': True, 'spell': True, 'bought': True, 'back': True, 'rings': True, 'coin': True, 'through': True, 'let': True, 'bare': True, 'octave': True, 'root': True, 'follow': True, 'comes': True, 'both': True, 'three': True, 'lift': True, 'spun': True, 'lands': True, 'metal': True, 'damped': True, 'flick': True, 'tally': True, 'reckon': True, 'linger': True, 'rounded': True, 'paid': True, 'cannot': True, 'late': True, 'offkey': True, 'closing': True, 'receipt': True, 'clasp': True, 'miss': True, 'snap': True, 'product': True, 'melts': True, 'hands': True, 'term': True, 'settled': True, 'chest': False}
# ---- v27 (28 Nov): A DEBT HAS A TERM. Two switches on (`--without-term`, `-settled`; both off is v26 byte for byte)
# and one written and off (`--with-chest`).
#   TERM     the bass plays what the purse cannot pay: each debt a sixteenth long, whatever its size, and the
#            largest of them (7 for coins of 3 and 5; 5 for 3 and 4: the number this song is about) a tone under
#            the rest. Now, in the bar its seed is sown, the largest debt is OWED AS LONG AS IT IS LARGE: a debt
#            of seven is held seven sixteenths, a debt of five five, the exchange's debt of seven of its units
#            4.67: or until the next debt comes, or the section ends, if that is sooner; 6 dB under the short
#            notes. Two short notes and a long one a tone under: the bass has a line two bars long, and the song
#            has something from 58 to 117 Hz between the drum's strokes (it was 2 to 4.6 dB under the album's
#            envelope from 44 to 133 Hz). Held in EVERY bar it read 2 to 3 dB over that envelope, moved both
#            ends 0.5 to 1.2 dB and put recurrence at 0.676, on its ceiling: in the seed's bar only, none of it.
#   SETTLED  and when its term is up the debt is paid: the bass is back on the key note for a sixteenth, at the
#            instant the term ends (7 + 7 is 14, which 3 3 3 5 pays; 5 + 5 is 10, which 3 3 4 pays). Not where
#            that instant is the drum's.
#   CHEST    (off) a bell of 4 dB at 71 Hz on the drum's own track, as Wind Down's drum has. Built and measured
#            alone: the band at 71 Hz came 0.5 dB nearer the album (4.1 short for 4.6) and both ends fell 0.6 dB,
#            because the drum is 0.9 dB louder and the loudness target takes it from everything else. TERM
#            does what it was for (71 Hz is 2.1 short) at a third of that cost.
# ---- v26 (28 Nov): THE TILL MULTIPLIES. Three switches (`--without-product`, `-melts`, `-hands`; all three off is
# v25 byte for byte).
#   PRODUCT  every effect here so far ADDS coins: a purse's echoes are sums of threes and fives. A ring modulator
#            MULTIPLIES, and the product of two tones is their difference and their sum: sin 3x sin 5x is half of
#            cos 2x less cos 8x. So before the seed of bars 5, 9 and 13 of each section, from the drum to home, the
#            purse's two coins sound together as NOTES: the seed's own note three octaves down, times each coin
#            (for a seed on B flat 4 and coins 3 and 5: F3 and D4), for as many sixteenths as the two coins make
#            (3 and 5: eight, half a bar), ending as the seed is sown. Not where the seed is sown off the beat
#            (the bar before it is left empty on purpose), and 6 dB softer in the break, where it is alone.
#   MELTS    and as they sound they are multiplied (the engine's ring modulation, each coin by the other): over
#            the first coin's length the two notes melt into their difference and their sum, which ring for the
#            second coin's length: 3 x 5 gives 2 and 8: B flat 2, and B flat 4, which is the seed's own note: the
#            two coins call the seed and the seed answers. Threes and fours give 1 and 7 (the low B flat and the
#            seventh harmonic, a note no scale here has); fives and sevens give 2 and 12 (a fifth over the seed).
#   HANDS    the two coins come one from each hand (left and right); their product is the same in both, so it
#            stands in the middle.
# ---- v25 (28 Nov): THE PURSE HAS A CLASP. Three switches (`--without-clasp`, `-miss`, `-snap`; all three off is
# v24 byte for byte).
#   CLASP  the song had a drum, a bass, a hat and no backbeat. A purse has a clasp: two small metal balls that
#          pass each other, click-CLICK (`sc-clasp`: two very short glockenspiel bars, G7 then D7, the first as
#          long before the beat as the hand takes to shut a purse: SHUT, 0.06 of a beat, 30 ms; the second on
#          the beat). It is snapped on beats 2 and 4, not where the drum has given the beat to the purse (a
#          roll, a wait, the bought beats of the drum again), and only where the purse can PAY the beat: where the time since the section's last seed is an amount its coins make. With
#          3 and 5 a seed every two bars buys beat 4 of its own bar (12) and both beats of the next (20, 28)
#          and not beat 2 of its own (4 is a debt): half a backbeat, then a whole one, by turns. With 3 and 4
#          every beat is bought. Off the beat the drum plays one and three only and the clasp has two and
#          four to itself; the seed is on sixteenth 6 and every beat after it is bought (6, 14, 22, 30). From the second half of the drum (bar 25) to the end of home. Dry: it is not
#          money and goes into no purse.
#   MISS   where the purse cannot pay the beat the clasp does not catch: the first ball only, before the
#          beat, and nothing on it.
#   SNAP   the hand that shuts the purse of small change on the one after every roll was never heard: now
#          the clasp is snapped there, on the one of bars 17 33 49 65 81 97 113 145, a little harder.
#
# ---- v24 (28 Nov): THE TILL CLOSES AT HOME, AND GIVES A RECEIPT. Three switches (`--without-offkey`, `-closing`,
# `-receipt`; all three off is v23 byte for byte).
#   OFFKEY   v23's fault, measured after it was out: off the beat (bars 129 to 160) a payment's first stroke falls
#            on sixteenth 6, and in every second bar no seed is sown there: it is the first sound after half a
#            bar of nothing in its band, and this master brought it up to the seed's own level (-6.5 dBFS; the
#            payment's other strokes -12 to -20). In those bars it is OFFKEY['db'] dB down; with a seed it is
#            8 dB under the seed already and is left.
#   CLOSING  the key rested at home. Now the till closes there: a payment to each seed (bars 161, 163 ... 171),
#            and coins of 3 and 5 pay sixteen in six orders: six seeds, six orders, each once more, before the
#            coin is spun on the counter (bars 173 to 176).
#   RECEIPT  a coin moves the key's note as it moves the purse's change: a 3 up a fifth, a 5 down a fourth. Two
#            of each is a major third up whatever the order they come in: adding does not mind the order. That
#            last move was never heard: the key plays where a coin BEGINS. At home the till gives a receipt: on
#            the bar line where the payment ends, one stroke on the note the four coins come to: D6 every
#            time, home's own fifth, after six different ways there.
#
# ---- v23 (28 Nov): THE BAR IS PAID. Three switches (`--without-paid`, `-cannot`, `-late`; all three off is v22
# byte for byte). The purses have paid the seeds' change; nothing has paid the BAR. A bar is sixteen sixteenths,
# and a till that has only threes and fives pays sixteen as 3 3 5 5, in six orders. A wooden key (`sc-key`, the
# song's first new voice since the coin) is pressed once for each coin, where that coin begins: four strokes a
# bar, a different order each bar until all six have been used, then round again. And each coin moves the key's
# note as it moves the purse's change (the first coin up a fifth, the second down a fourth), so whatever the
# order the four notes are the same four: only which way each leaps, and when. The key begins an octave over
# the seed's note, so it traces one way through the purse's change, an octave over the echo that took those
# coins in that order (wood over the vibraphone bar).
#   PAID    where the purse can pay a bar: threes and fours (3 3 3 3 4 in five orders, and 4 4 4 4: on the drum),
#           both purses (the two tills bar about), three purses.
#   CANNOT  fives and sevens cannot make sixteen. They can make twenty-four (5 5 7 7, six orders): a bar and a
#           half. In the drum again the key pays ten of those across fifteen bars, three payments to two bars,
#           and bar 112 is left over: sixteen, which that till cannot pay: the key rests. In three purses the
#           third till takes its turn: 16, 16, 24: the round is three and a half bars and comes round the bar.
#   LATE    off the beat the till is inside out and its seed is on sixteenth 6: the key pays from there.
#
# ---- v22 (27 Nov): THE CHANGE IS ROUNDED TO THE COIN. One switch (`--without-rounded`; off is v21 byte for byte).
# A till that has no small coins rounds what it owes. The purse of the two sections off the beat (coins of 5 and
# 3, bars 129 to 160) is such a till: after each coin its change is rounded to a grid of 2^bits amounts (the
# engine's bit crusher, last in each of the purse's two loops, so the change is rounded again at EVERY payment):
# a debt under half the smallest amount is nothing, and the purse stops owing instead of fading. In off the
# beat (bars 129 to 144) only the AMOUNT is rounded. In off the beat, up (bars 145 to 160) the TIME is rounded
# too: the crusher holds each sample longer and longer (its rate falls from 12 kHz to 3 kHz over the sixteen
# bars), and there the other purse (coins of 3 and 5: seeds in bars 147, 151, 155, 159) is still paid in full:
# the two answer each other, one exact, one rounded worse each time. At home nothing is rounded.
PAID = {'patch': 'sc-key', 'gain': '-20dB', 'pan': -0.15, 'octave': 12, 'fold': (-7, 12), 'vel': (0.9, 0.75), 'len': 0.2, 'steps': (7, -5), 'long': 24,
        'where': ('threes and fours', 'both purses', 'three purses'), 'cannot': ('the drum again',), 'late': ('off the beat', 'off the beat, up')}   # v23: the key: its patch, fader (bench, raw, bars 49 to 56: at -12 dB its strokes stood 9 to 13 dB over the purse's echoes from 160 to 560 Hz: a lead; -18 is beside them; but an octave under the seed its strokes on the beat were 10 to 15 dB under the drum there: at the seed's own octave its first two strokes were the seed and the purse's first echo over again, 12 to 21 dB under them: it is an octave over the seed), place, semitones from the seed's note, the span its notes are folded into (semitones from its first), touch (a payment's first stroke, the rest), length (beats), what the first and the second coin do to its note (as in the purses), the amount a purse pays when it cannot pay a bar, and the sections
CLASP = {'patch': 'sc-clasp', 'gain': '-14dB', 'pan': 0.12, 'from': 24, 'on': (4, 12), 'balls': (('G7', 0.6, -14), ('D7', 0.9, 0)), 'miss': 3, 'snap': 3, 'nodrum': -3, 'bare': {4: -10, 12: -7}, 'len': 0.05, 'purses': 'abcd'}   # v25: the clasp: its patch, fader, place; the bar it begins in (from 0); the sixteenths it is snapped on; its two balls (note, touch, dB), the first SHUT beats before the beat and the second on it; dB on the one ball of a miss; dB on a snap on the one; dB more on it where no drum plays that one (bar 81, the break: it read -9.3 dBFS, 3 to 4 dB over the other snaps); dB on the second ball where the drum does not play the beat (off the beat), by the sixteenth it is on (with 7 dB off both, beat 2 still read 3.5 dB over beat 4). SET FROM A FINISHED BUILD, ball by ball: with the first ball 6 dB under the second it came out as loud as the second or louder (-10.7 to -14.4 dBFS against -11.5 to -14.4: this master lifts a click 30 ms before the drum 20 to 22 dB and one on the drum 10 to 12), so a miss was as loud as a snap; off the beat, with no drum under it, the second ball came out -5.6 to -10.0; a ball's length (beats); the purses that can buy a beat
CLASP_PATCH = {'about': "Small Change: the purse's clasp (v25). Two small metal balls that pass each other: each a very short glockenspiel bar (18 ms) with a millisecond and a half of grit on its front. Dry: it is not money and goes into no purse.",
               'synth': {'layers': [{'type': 'modal', 'modes': 'glock', 'decay': '18ms', 'bright': 0.8, 'strike': 0.6},
                                    {'type': 'noise', 'color': 'white', 'level': {'value': '-70dB', 'mod': [{'src': 'env.grit', 'amount': 52}]}}],
                         'env': {'grit': {'a': '0.1ms', 'd': '1.5ms', 's': 0, 'r': '1.5ms'}},
                         'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '30ms'}},
               'play': {'event_stable': True, 'vel_sens': 0.6}}
TERM = {'up': 2, 'vel': 0.85, 'db': -6, 'chest': 'peak cutoff=71 q=1.4 gain=4dB'}   # v27: SETTLED: the semitones from the largest debt's note to the key note it is paid on, and that note's touch; TERM: dB on a held debt (-6: between the drum's strokes it then reads 6.6 dB under the short notes, -18.0 dBFS from 50 to 130 Hz where there was -43.9; at 0 dB and in every bar the lows read 2 to 3 dB OVER the album's envelope); CHEST: the bell on the drum's track (off)
PRODUCT = {'patch': 'sc-product', 'gain': '-38dB', 'sections': (1, 11), 'bars': (4, 8, 12), 'down': -36, 'vel': 0.8, 'hands': 0.5, 'trim': {84: -6, 88: -6, 92: -6, 100: 4, 104: 4, 108: 4, 116: 4, 120: 4, 124: 4}}   # v26: the product: its patches' name (one for each pair of coins) and fader; the sections it plays in (from, to: the drum to home); the bars of a section (from 0) whose seed it leads to; the seed's note to the unit, semitones; touch; HANDS: how far to each side the two coins are; dB on a note by its seed's bar (from 0), SET FROM TWO FINISHED BUILDS, every note read (rms, 50 to 900 Hz): THIS SONG'S MASTER IS A LOUDNESS TARGET ON A SONG OF CLICKS, AND A HELD TONE IS THE LOUDEST THING IN IT: at -16 dB every note came out -6.7 to -9.5 dBFS, 3 to 10 dB OVER the drum and the bass together; at -24 dB it came out only 0.8 to 2.8 dB lower (a line of it -7.3 dBFS finished for -28.9 on the bench: 21.6 dB of lift), and BOTH ENDS OF THE SONG 0.8 dB lower: the fader was turning the rest of the song up, not the tone down. At -38 the tone is 3 to 5 dB under the drum and the bass in its band and both ends are within 0.1 dB of what they were; 6 dB more off where there is no drum (it is alone there), and 4 dB on in the two fullest sections (the drum again and three purses, where it read 8 to 14 dB under). Not where the seed is sown off the beat: there the bar before the seed is empty on purpose (the old music is -33 to -63 dBFS where the product would ring)
OFFKEY = {'db': -9}                         # v24: dB on a payment's first stroke where the payments begin off the beat (PAID['late']) and no seed is sown with it: read in the finished song (there it came out at -6.5 dBFS, the seed's own level; with a seed it is 8 dB under the seed and is left)
CLOSING = {'where': ('home',), 'bars': 12}  # v24: the sections where the till closes (a payment to each seed), and for how many of their bars (the coin is spun in home's last four)
RECEIPT = {'vel': 0.9, 'db': 3}             # v24: the receipt's touch, and dB on it (read in the finished song: at 0 dB it came out 2 to 10 dB under what else is on its bar line from 440 to 2400 Hz)
KEY = {'about': "Small Change: the till's key (v23): a short dry wooden bar, pressed once for each coin as the bar is paid.",
       'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '70ms', 'bright': 0.4, 'strike': 0.45}], 'amp': {'a': '0.2ms', 'd': '0s', 's': 1, 'r': '120ms'}},
       'play': {'event_stable': True, 'vel_sens': 0.7}}
ROUNDED = {'buses': ('d5', 'd3'), 'bits': 5, 'rate': 12000, 'octaves': -2, 'time': 'off the beat, up', 'free': 96000}   # v22: the purse's two loops; the grid (bench, the purse alone: what rounding changes stood 21.5, 13.6 and 10.1 dB under the purse at 8, 6 and 5 bits, and at 5 as much as the purse's own from 1 to 4 kHz; its loudest change is 5 amounts each way at 6 bits, so 4 bits would leave one payment); the last: a rate over the engine's own (48 kHz), at which nothing is held; the crusher's rate where the time is rounded, Hz, and how many octaves it falls over that section (a lane on a rate is in octaves, as on a cutoff); the section in which the time is rounded (before it the rate is the engine's own: nothing held)
# ---- v21 (27 Nov): THE FIRST CHANGE IS COUNTED TOO, AND THE LAST SEED'S PURSE STAYS OPEN. Two switches
# (`--without-reckon`, `-linger`; both off is v20 byte for byte).
#   RECKON  v20's coin counted the change in the break and in the last section. The first section (one seed, bars
#           1 to 16: the rule stated with nothing else in the room) was not counted. Now it is, from its third
#           seed: after bar 9 a clink on every amount threes and fives can pay up to 16 (one bar), after bar 13
#           up to 24: 3 5 6, and from 8 every one. A WORN coin: the spun coin through four low-passes at 7 kHz
#           (Hearing Things' last sixteen bars lie over these; chirper-zero allowed the count from bar 9 with
#           nothing over 10 kHz; most of the new coin is over 10 kHz), about 7 dB under the break's from 4 to
#           8 kHz. So the count is heard three times: learnt at the start, in fives and sevens in the break,
#           in smaller coins at the end.
#   LINGER  the last section's bars 179-180 and 183-184 were nearly silent (found in v20). Its first seed (bar
#           177, paid in sixteenths, as the song's first four were) now goes into the long purse, as those four
#           do: its change rings on through bars 178 to 180 and under the second seed. The seeds after it are
#           paid as they were, in smaller coins, and the silence before Out of Step (bars 183-184) stays.
#
# ---- v20 (27 Nov): THE COIN COUNTS THE CHANGE. One more switch (`--without-tally`; off is v19 byte for byte).
# v19 said "the rest of the song had nothing this round". The break (fives and sevens, bars 81-92) is twelve bars
# with three written notes: three seeds and what the purse pays back, 5 and 7 sixteenths at a time. The song's
# whole subject is which amounts can be made of two coins, and in the break nobody says it but the echoes.
#   TALLY  after each of the break's first three seeds the coin is put down once for every amount the purse can
#          pay: 5 7 10 12 14 15 17 19 20 21 22, and from 24 on EVERY sixteenth (23 is the largest amount that
#          cannot be made of fives and sevens): the line begins as scattered clinks and becomes a run of
#          sixteenths. It counts further each time: to 24, to 30, to 35 (five sevens and seven fives: the first
#          amount made two ways, and it is struck on both sides). Where it is says how it is made, as the purse's own sides do: fives alone on the
#          left, sevens alone on the right, both in the middle. Each coin more is TALLY['coin'] dB quieter, so
#          the run fades as it fills. The fourth seed's coin is not counted: it is flicked and spun (v18, v19).
#          It is the spun coin's own sound (sc-spun), let ring TALLY['ring'] s: a clink. And once more at the
#          end, for the last section's first two seeds (bars 177 and 181), in threes and fives: 3 5 6, and from
#          8 on every one, up to 15: the first in sixteenths, the second in thirty-seconds, the coins that seed
#          is paid in; nothing in the last eight bars (Out of Step lies over them).
#
# ---- v19 (27 Nov): THE COIN IS METAL. Three more switches (`--without-metal`, `-damped`, `-flick`; all off is v18
# byte for byte). v18's spun coin was the second hat's sound (a 20 ms hiss from 3 to 5.5 kHz): its own note said it
# might be a hat speeding up and not a coin. A coin on a table is a small free plate struck on its edge at every
# rattle: it rings, and the table damps the ring more the flatter it lies.
#   METAL   the spun coin has a sound of its own (new patch sc-spun): a thin plate's modes, dense and out of tune
#           with each other, from 4.2 kHz up (the patch's note is the seed's three octaves up, B flat 7), struck
#           near the edge, with a short click on its front. Each rattle's ring is on the note (expr.ring, seconds).
#           Benched against a free bar's modes on the same note (one partial at 3.7 kHz and little else: a beep)
#           and both an octave down: the plate on B flat 7 is the one with a cluster and no single note.
#   DAMPED  the ring is by the same law as the rattle: each ring's T60 is DAMPED['gaps'] of the gap to the next
#           rattle, so the coin rings long while it stands on its edge and is choked as it lies down: the rings are
#           the same share of every gap, and the last one (8 ms from the stop) is the shortest: it stops dead.
#           Without it every ring is METAL['ring'] long and the last rattles smear into one tone.
#   FLICK   a coin does not start by itself: on the spin's first instant it is flicked: one stroke of the same
#           metal in the middle, let ring FLICK['ring'] s. It says 'coin' before the rattle says 'spinning'.
# ---- v18 (27 Nov): A COIN IS SPUN ON THE COUNTER. Two more switches (`--without-spun`, `-lands`; both off is v17
# byte for byte). The song's effects so far are all sums: amounts made of coins. This one is a coin's own motion. A
# coin (or Euler's disc) spun on a table rolls on its edge, lying flatter and flatter, and its rattle quickens without
# limit and then stops dead: a finite-time singularity (Moffatt 2000, who predicted a power of -1/6). Measured (Easwar,
# Rouyer and Menon 2002: 0.3 to 0.4), the rattle's rate goes about as (t0 - t)^(-1/3), t0 the instant it stops. So the clicks are written from that law and nothing else:
# beginning at the song's own sixteenths (a rate of four a beat) and ending T beats later, click k of N falls at
# T (1 - (1 - k/N)^(3/2)), and N = (3/2) * 4 T: the rate is unbounded but the count is finite, half as many again as
# the sixteenths it runs over (96 for 64). The first gap is a sixteenth to a third of a millisecond; the last is 8 ms
# (a rattle of 119 a second: nearly a note). It is the second hat's own patch (sc-coin: the song's coin), alternately
# left and right, as an escapement's two pallets: wide and slow at first, one buzz in the middle at the end: the two
# sides close as the coin's tilt does, as (t0 - t)^(2/3) (the same measurement: the angle to the table), each track's
# pan on a lane with a point at every rattle. In mono it is the rattle alone.
#   SPUN   through the last four bars of the break ('fives and sevens', bars 93 to 96): it stops dead on the one of
#          bar 97, where the drum comes back. A riser made by a table, not by a filter.
#   LANDS  through the last four bars of 'home' (bars 173 to 176), over the whole band: it starts in step with the
#          hat's sixteenths and runs away from them (the next song is Out of Step), and stops dead on the first seed
#          of 'the last seed', as the drum and the bass leave.
SPUN = {'bars': 4, 'rate': 4, 'power': 1 / 3, 'gain': '9dB', 'pans': (-0.45, 0.45), 'vel': (0.5, 0.85), 'close': 2 / 3, 'where': {'spun': 'fives and sevens', 'lands': 'home'}}   # v18: how long the coin spins, bars; its rattles a beat as it begins (the sixteenths); the law's power; the two tracks' fader and sides; the first and last click's stroke; the section each switch's coin ends
TALLY = {'where': (('fives and sevens', (24, 30, 35), 1), ('the last seed', (15, 15), 2)), 'coin': -2.5, 'ring': 0.05, 'vel': 0.7, 'gain': '-25dB', 'pan': 0.6}   # v20: where the coin counts the change: (section; up to what amount after each of its seeds in turn: it counts further each time; how many times smaller the coins are with each seed: in the last section the second seed is paid in thirty-seconds, and counted in them); dB a coin; a clink's ring, s; its stroke; the three tracks' fader (bench: at -27 dB a one-coin clink's highest sample stood 7 to 10 dB under the spun coin's rattles); how far to each side the one-coin amounts stand
RECKON = {'where': 'one seed', 'seeds': ((2, 16), (3, 24)), 'coin': -2.5, 'ring': 0.05, 'vel': 0.7, 'gain': '-27dB', 'pan': 0.6, 'lp': 7000, 'walls': 4}   # v21: the section whose change is counted too; (which of its seeds, from 0; up to what amount); dB a coin in the amount; a clink's ring, s; its stroke; the fader; how far left and right; the worn coin: low-passes in a row and their cutoff, Hz (nothing over 10 kHz). Bench, the count alone, bar 9, raw: no filter: 4 to 8 kHz -67.2 dBFS, over 10 kHz -65.9 (most of this coin is up there); two filters -70.1 and -91.5; four -72.1 and -105.5: so four, and the fader 2 dB up from the first build's -29
LINGER = {'seeds': 1}                        # v21: how many of the last section's seeds go into the long purse
METAL = {'patch': 'sc-spun', 'modes': 'plate', 'note': 'Bb7', 'ring': 0.06, 'bright': 0.8, 'strike': 0.7, 'click': '-9dB', 'tick': '8ms', 'hp': 2500, 'gain': '-27dB'}   # v19: the spun coin's own patch: its mode set and note; a ring's T60 where it is not damped by the law, s; the modal layer's brightness and where it is struck; the click on its front (the hat machine): level and decay; the patch's high-pass, Hz; the two tracks' fader (benched against the old coin)
DAMPED = {'gaps': 2}                        # v19: a ring's T60 in gaps to the next rattle
FLICK = {'ring': 0.4, 'vel': 1.0, 'db': 3, 'len': 1}   # v19: the flick's ring, s; its stroke; dB over the rattles' fader; its length, beats
# ---- v17 (27 Nov): THE BASS FOLLOWS EVERY SEED. Four more switches (`--without-comes`, `-both`, `-three`, `-lift`;
# all four off is v16 byte for byte). v16 found the bass's note in the rule (three coins on from the seed) and used it
# where a section has one seed, and in one section where the seeds change. In the three other sections where the
# seeds change the bass was still on G under seeds whose five notes are C minor's and D minor's. No note is added or
# moved in time by the first three; the bass's whole line (its largest debt, what the other purses owe) moves.
#   COMES    'the bass' (bars 33-48; seeds B flat and E flat by turns, a seed every second bar): the bass comes in on
#            G2 for two bars and goes down to C2 for two, four times: the first thing the bass does after coming is move.
#   BOTH     'both purses' (bars 65-80; seeds B flat and F, a seed a bar): a bar on G2, a bar on D2: with the two
#            purses the bass has two notes.
#   THREE    'three purses' (bars 113-128, the peak; seeds B flat, F, E flat, a seed a bar): three purses, three
#            notes: G2, D2, C2 by the seed, a cycle of three bars against the four the form is counted in. FROM ITS
#            NINTH BAR (FROM): the peak stands on G for eight bars, as it did, and then turns: C2 G2 D2 C2 G2 D2 C2
#            G2; it ends on G and 'off the beat' begins on C. THE FIRST BUILD turned from the peak's first bar and
#            the peak stopped being an arrival: the scorer's curve at its start fell from 0.22 to 0.18, a section
#            was lost at the highest cut and the song read 99.51 for 100.0 on both seeds. A section that arrives on
#            the home note has to stand on it before its line moves again.
#   LIFT     a bass on C2 or D2 is 65 or 73 Hz and its octave (9 dB under) 131 or 147: a small speaker has neither,
#            where it had the G2 line's 196. So wherever the line is under its written note, a second track plays the
#            same notes an octave up, LIFT['db'] under the bass (the same patch, under the same pump): its own octave
#            is at 262 or 294 Hz. MEASURED, finished: from 120 to 160 Hz the low sections have 4.4 to 4.8 dB more; from
#            240 to 310 Hz 2 dB in one section and nothing in the others; above 200 Hz half a dB in one. So it is
#            heard by a speaker that reaches 130 Hz and not by one that begins at 200. And the master gives the whole
#            song 0.3 dB less for it (both ends are 0.3 dB quieter).
FOLLOWS = {'comes': 'the bass', 'both': 'both purses', 'three': 'three purses'}   # v17: the switch; the section in which the bass then follows its seeds (with v16's follow)
FROM = {'three purses': 8}                # v17: the bar of its section from which the bass follows (the peak stands on G for its first half: read the note)
LIFT = {'db': -9}                         # v17: the octave-up copy of the bass's moved notes, dB under the bass's fader
# ---- v16 (27 Nov): THE BASS STANDS ON ITS SEED'S KEY NOTE. Two more switches (`--without-root`, `-follow`; both
# off is v15 byte for byte). The rule at the top of this file says it: the seed and the first four coins spent on it
# are five notes a fifth apart, and from B flat those are G minor's five. Their key note is three coins on from the
# seed (B flat, F, C, G). The bass has stood on that G for every seed: but the form's seeds are also E flat and F,
# whose five notes are C minor's and D minor's, and under them the bass was still on G.
#   ROOT     where a section has ONE seed the bass stands three coins on from it: 'off the beat' (seed E flat) on
#            C2, 'off the beat, up' (seed F) on D2, and home (seed B flat) on G2 as ever: the song's last third is
#            the fourth, the fifth and home (iv, v, i), where it was G for six minutes. The whole line moves:
#            its largest debt (a tone under) and what the other purses owe (the seed's own note) with it.
#   FOLLOW   in 'the drum again' (seeds E flat and F by turns, a seed every second bar) the bass follows each seed:
#            two bars on C2, two on D2, eight times; it ends on D and the peak ('three purses') begins on G.
# The bass has a fundamental here (sc-debt), so C2 and D2 are 65.4 and 73.4 Hz: between the drum's two partials (49
# and 98 Hz), where this song has always been short (71 Hz: 6.7 dB under the album: nothing was ever there).
STANDS = {'home': 'Bb4', 'follow': ('the drum again',)}   # v16: the seed whose key note the bass's written line is on; the sections where the bass follows seeds that change
# ---- v15 (27 Nov): THE BASS IS HEARD COMING. Two more switches (`--without-bare`, `-octave`; both off is v14 byte
# for byte). The third section is called 'the bass', and its entrance is the song's weakest boundary (v14: it
# sits on the scorer's highest cut, and one seed lost it to a change sixty bars away). Two reasons, both read:
# the drum is already in the bass's band when it comes, and the bass is a sine at 87 to 117 Hz, which a small
# speaker does not have and which the drum's own 130 Hz stands over.
#   BARE     the bar before the bass comes, the drum waits (bar 32: no drum at all; the hat's two strokes and
#            the small change are left). chirper-zero's rule: a quiet part in an empty band takes the arrival
#            from whoever enters that band next; so leave the band bare, and let the bass and the drum
#            arrive in it together. (WAIT does this before home, for two bars; GAP gave the change one beat.)
#   OCTAVE   the bass has its octave (sc-debt: the library's sub-sine with its second harmonic 9 dB under
#            the note in place of 19, and a low-pass at 300 Hz after it): what cannot be paid is heard from
#            175 to 233 Hz as well, on any speaker, from its first note to its last (536 notes). The first
#            build had it 6 dB under and no low-pass: the patch's drive made a third to a seventh harmonic
#            of the two (260 to 750 Hz came up 1 to 1.6 dB in the finished song, where it is already over
#            the album), and the master, with more to carry, took 0.6 dB off everything under 130 Hz (the
#            71 Hz band, the song's worst, went from 6.4 to 7.0 dB short).
DEBT = {'patch': 'sc-debt', 'octave': '-30dB', 'lp': 300}   # v15: the bass's own patch; its second harmonic's level at no velocity (the library's is -40 dB; with the same 12 dB of velocity, at .85 this is 8.9 dB under the note); the low-pass after the drive, Hz
SC_DEBT = {'about': "Small Change: the bass that plays what cannot be paid, with its octave (v15). The library's sub-sine (a sine, mono, a 30 ms glide, a little drive, a low-pass at 500 Hz) with its second harmonic at -30 dB in place of -40 (9 dB under the note at this song's touch) and one more low-pass, at 300 Hz, so that the drive leaves the note and its octave and little else: a line on 87 to 117 Hz is also heard on 175 to 233.",
           'gain': '-6dB', 'params': {'grit': 0}, 'play': {'gate': 0.97, 'glide': '30ms', 'mono': True, 'vel_sens': 0.4},
           'synth': {'amp': {'a': '6ms', 'd': '0ms', 'r': '60ms', 's': 1}, 'drive': {'mod': [{'amount': 0.6, 'src': 'param.grit'}], 'value': 0.2},
                     'filters': ['hp cutoff=22', {'cutoff': {'mod': [{'amount': 2, 'src': 'param.grit'}], 'value': 500}, 'kind': 'lp'}, f"lp cutoff={DEBT['lp']}"],
                     'layers': [{'level': {'mod': [{'amount': 6, 'src': 'vel'}, {'amount': 3, 'src': 'param.grit'}], 'value': '-16dB'}, 'wave': 'sine'},
                                {'level': {'mod': [{'amount': 12, 'src': 'vel'}, {'amount': 14, 'src': 'param.grit'}], 'value': DEBT['octave']}, 'ratio': 2, 'wave': 'sine'}],
                     'pitch': {'mod': [{'amount': 0.04, 'src': 'rand'}], 'value': 0}}}
# ---- v14 (27 Nov): THE HAT RINGS ON THE LARGEST DEBT. One more switch (`--without-let`; off is v13 byte for byte).
# Since v8 the hat is 'let ring' where what one purse pays is what another owes (MEET: 84 strokes, in both
# purses and three purses). v12 found that it never rang: sc-open is a second stroke on the other side, 140 ms
# long. v12 and v13 gave the song a hat that does ring (sc-rung) and a rule for a second hat (it needs a band or
# a tail, not a side). Now:
#   LET      where the debt the hat meets is another purse's LARGEST (the largest amount it cannot make: 5 for
#            threes and fours, 7 for threes and fives: the number the bass already marks with its low note)
#            the hat really rings: sc-rung, three sixteenths and stopped. In both purses that is every one of
#            the sixteen: sixteenth 5 in the first purse's bars, 7 in the second's, bar about. In three
#            purses it is the same two places: 5 in the first purse's bars, 7 in the second's, and both in
#            the third's (eighteen of the sixty-eight); the other fifty stay strokes. So the figure learnt
#            in bars 65 to 80 is the one that comes back at the peak, and the ring is one rule in four
#            sections: a meeting off the beat (the purse's own two coins in v12; another purse's largest
#            debt here). The ring starts where the old stroke stood: 6 dB under the rung track's other
#            strokes (first built without that: the stroke itself came out 6 dB over the open hat it
#            replaced, which was not the change that was meant).
LET = {'db': -6}                            # v14: dB on a ring of LET (the rung hat's stroke alone reads 5.6 dB over the open hat's it replaces)
# ---- v13 (27 Nov): THE OTHER CURRENCY HAS ITS OWN COIN. Two more switches, each `--without-…` (with them off it is
# v12 byte for byte). Since v9 home is also paid in another currency (three of its units to two sixteenths) and
# a second hat ticks what that purse can pay where it falls between the sixteenths. It was the first hat's own
# patch on the other side, 2 dB under it, for four strokes in the first two beats of every other bar: the same
# sound in the same band, told from the first only by where it fell.
#   COIN     the second hat is a patch of its own, sc-coin: the first hat at two thirds, as its unit of time
#            is two thirds of a sixteenth: two thirds as long (20 ms for 30) and two thirds as high (the
#            centre of its sound 5.5 kHz for the first hat's 8.3: a band-pass from 3 to 5.5 kHz for a
#            high-pass at 6). First tried as a NOTE a fifth up (three for two in pitch): on the bench the
#            machine's hat does not follow its note (its partials stayed where they were, the centre of its
#            sound 8.30 to 8.35 kHz): a name and not a sound. Then as the same hat above 9 kHz: its centre
#            moved to 9.2 kHz, a ninth of the way, into the band the first hat is loudest in. Under the
#            first hat there is room: without the hats the song has -69 dBFS from 4 to 6 kHz at home.
#   THROUGH  it counts the exchange's change through the whole bar (to 24 of its units, which is the bar) and
#            not two beats of it: twelve ticks for four, each softer by the coins it took (the same rule the
#            first hat has), so that for one bar in two the bar is heard cut in twenty-four against the
#            hat's sixteen: three for two, to the bar line.
COIN = {'patch': 'sc-coin', 'decay': '20ms', 'filters': ['hp cutoff=3000', 'lp cutoff=5500', 'lp cutoff=5500'], 'gain': '12dB', 'upto': 24}   # v13: the second hat's own patch; its decay and its band (the first hat's are 30 ms and a high-pass at 6 kHz); its fader (set on the bench so that its highest sample alone is 3 dB under the first hat's); the largest amount it counts with THROUGH (a bar)
# ---- v12 (27 Nov): FIVE AND THREE MAKE EIGHT TOO. Two more switches, each `--without-…` (with them off it is v11
# byte for byte). v11 put the song's sum into its notes once, the right way round, on a beat. The song also has
# the purse inside out (since v3) and sums that fall on no beat, and neither was in the notes.
#   BACK      home's chord is struck whole twice (bars 161, 163), and counted out in its second half: G, B flat, D
#             on sixteenths 0, 3, 8: three, then five. Between the two (bars 165, 167) it is now counted out the
#             other way: D, B flat, G on sixteenths 0, 5, 8: five, then three, from the top down. So home is the
#             chord, the purse inside out, and the purse: the whole song in sixteen bars, and both spellings end
#             on the same sixteenth because 5 + 3 is 3 + 5.
#   RINGS     where the purse's two coins first meet ON a beat the drum gives it the beat (v11 BOUGHT). In two
#             sections they meet off the beat and the drum has nothing to give: threes and fours (3 + 4 = 7:
#             sixteenth 7) and off the beat (the purse inside out from sixteenth 6: 5 + 3 lands on sixteenth 14).
#             There, in the section's second half, the hat that falls on the sum is let ring in each bar that
#             has a seed (bars 57, 59, 61, 63 and 137, 139, 141, 143). On a beat the sum is a rest; off a beat
#             it is a ring. First built with the open hat the song already has (sc-open, 140 ms): on the bench
#             it lifted its own sixteenth 3 dB above 5 kHz and the sixteenth after it not at all: a louder
#             stroke, not a ring. So a new patch name, sc-rung: the same hat with a decay of 1.2 s, held three
#             sixteenths and then stopped. (The machine's `decay` is the time to fall 60 dB: at 380 ms the hat
#             alone read -38.6 -57.5 -77.0 dBFS by sixteenth, 19 dB a sixteenth, and its second sixteenth added
#             nothing over the shut hats; at 1.2 s it falls 6 dB a sixteenth.)
BACK = {'bars': (4, 8)}                     # v12: the bars of home (from its first, 0) in which the chord is counted out the other way
RINGS = ('threes and fours', 'off the beat')   # v12: the sections in whose second half the hat rings where the purse's two coins first meet off a beat
RUNG = {'patch': 'sc-rung', 'decay': '1200ms', 'release': '150ms', 'len': 0.75, 'gain': '-8dB', 'pan': -0.15}   # v12: the hat that rings on the sum: its patch, how long it rings, beats it is held, its fader, and the open hat's side.
# Its fader: at the open hat's -5 dB the finished song read 8 dB up above 5 kHz over the ring's three sixteenths (-19.8 for -27.9 dBFS), where the open hat puts 3 on its half beat: a splash. 3 dB less
# ---- v11 (27 Nov): THREE AND FIVE MAKE EIGHT. Two more switches, each `--without-…` (with them off it is v10 byte
# for byte). The song's sum has been in its echoes since v1 and nowhere in its notes.
#   SPELL     home's chord (G, B flat, D on the one, every two bars) is counted out in home's second half (bars
#             169 to 176): G on the one, B flat three sixteenths on, D five after that: on sixteenth 8, which is
#             beat three. The chord is paid in the purse's own two coins, and its top note falls where the two
#             coins first meet (3 + 5 = 5 + 3: the one amount the purse pays twice over, so its loudest echo).
#   BOUGHT    and the drum gives that beat away: in the same bars it rests on beat three of each bar that has a
#             chord (four times), so the D and the purse's eight are heard with nothing over them. Least Common
#             gives beats to its answer and Wind Down to its meetings; here the beat is bought, for 3 + 5.
#             And once before, so that it is a rule and not an event: when the drum comes back after the break
#             (bars 97 to 112) the purse is fives and sevens, and 5 + 7 = 12 is beat four: in that section's
#             second half the drum rests on beat four of each bar that has a seed (bars 105, 107, 109, 111).
SPELL = (0, 3, 8)                           # v11: sixteenths after the seed at which the chord's three notes are struck, in home's second half
BOUGHT = ('the drum again', 'home')         # v11: the sections in whose second half the drum rests where the purse's two coins first meet (5 + 7 = 12: beat four; 3 + 5 = 8: beat three)
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


NAMES = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')


def step_of(pitch):
    """v16: a note name's semitone above C (sharps read as the flat a step up)."""
    return NAMES.index(pitch[:-1]) if pitch[:-1] in NAMES else NAMES.index(pitch[0]) + 1


def moved(pitch, semis):
    """v16: a note name moved by semitones (flats for the black keys, as the seeds are written)."""
    n = step_of(pitch) + 12 * int(pitch[-1]) + semis
    return f'{NAMES[n % 12]}{n // 12}'


def follows(name, k=None):
    """v17: does the bass follow this section's seeds as they change (v16's 'the drum again'; v17's three, each by its switch), in bar k of the section (None: at all)?"""
    return ON['follow'] and (name in STANDS['follow'] or any(ON[sw] and name == sec for sw, sec in FOLLOWS.items()) and (k is None or k >= FROM.get(name, 0)))


def stands(name, notes, every, k):
    """v16 ROOT, FOLLOW: semitones the bass's line moves in bar k of a section: down to the key note of the seed that
    bar answers (three coins on from it), from the key note of the seed it was written under."""
    if not (ON['root'] and len(notes) == 1 or follows(name, k)):
        return 0
    up = (step_of(notes[k // every % len(notes)]) - step_of(STANDS['home'])) % 12
    return up - 12 if up else 0


def spun(end):
    """v18: a coin spun on the counter that stops dead at the top of bar `end` (bars from 0): the beats of its rattles. The rate begins at SPUN['rate'] a beat and rises as (t0 - t)^(-power); the phase is its integral, so click k of n is at T (1 - (1 - k/n)^(1/(1 - power))) and n = rate * T / (1 - power)."""
    beats, p = SPUN['bars'] * 4, SPUN['power']
    n = round(SPUN['rate'] * beats / (1 - p))
    return [round(end * 4 - beats + beats * (1 - (1 - k / n) ** (1 / (1 - p))), 4) for k in range(n)]


def metal_patch():
    """v19 METAL: the spun coin's own sound."""
    return {'about': f"Small Change: the spun coin (v19). A coin on a table is a small free plate struck on its edge at every rattle: a thin plate's modes (dense, out of tune with each other, from 4.2 kHz up; the patch's note is the seed's three octaves up), struck near the edge, and a short click on its front. Each stroke's ring is on the note (expr.ring: T60 in seconds over 4 ms): the song damps it by the law the rattle quickens by.",
            'synth': {'layers': [{'type': 'modal', 'modes': METAL['modes'], 'decay': {'value': 0.004, 'mod': [{'src': 'expr.ring', 'amount': 1}]}, 'bright': METAL['bright'], 'strike': METAL['strike']},
                                 {'type': 'machine', 'machine': {'part': 'hat', 'decay': METAL['tick']}, 'level': METAL['click']}],
                      'filters': [f"hp cutoff={METAL['hp']}"], 'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.8}}


def ways(p, q, total):
    """v23: every order of coins p and q that pays `total` exactly, p first (the orders a cashier could count them out in)."""
    return [[]] if total == 0 else [[c] + rest for c in (p, q) if c <= total for rest in ways(p, q, total - c)]


def paid():
    """v23 PAID: the key's payments: (section, sixteenth it begins on, purse, the coins in order, the note it begins on), in order."""
    out, turn, purse = [], {}, purses()
    for i, (name, pairs, every, at16, notes, drum, bass) in enumerate(SECTIONS):
        if name in PAID['where'] and ON['paid']:
            cycle = [(k, BAR) for k in pairs if ways(*purse[k], BAR)] + [(k, PAID['long']) for k in pairs if ON['cannot'] and not ways(*purse[k], BAR)]
        elif name in PAID['cannot'] and ON['paid'] and ON['cannot']:
            cycle = [(k, PAID['long']) for k in pairs]
        elif name in PAID['late'] and ON['paid'] and ON['late']:
            cycle = [('d' if 'd' in purse else k, BAR) for k in pairs]
        elif name in CLOSING['where'] and ON['paid'] and ON['closing']:   # v24 CLOSING: the till closes: a payment to each seed
            cycle = [(k, BAR) for k in pairs if ways(*purse[k], BAR)]
        else:
            continue
        pos, end, k = i * SEC * BAR + at16, (i + 1) * SEC * BAR, 0
        step = every * BAR if name in CLOSING['where'] else 0   # v24: from seed to seed there; elsewhere from payment to payment
        end = i * SEC * BAR + CLOSING['bars'] * BAR if name in CLOSING['where'] else end
        while pos + cycle[k % len(cycle)][1] <= end:
            key, amount = cycle[k % len(cycle)]
            orders = ways(*purse[key], amount)
            out.append((name, pos, key, orders[turn.get(key, 0) % len(orders)], moved(notes[k % len(notes)], PAID['octave'])))
            turn[key] = turn.get(key, 0) + 1
            pos, k = pos + (step or amount), k + 1
    return out


def key_notes():
    """v23 PAID: the key's strokes: one for each coin, where the coin begins; the coin moves the note as it moves the purse's change, folded into PAID['fold']."""
    out, purse = [], purses()
    sown = {x[0]: (i * SEC * BAR + x[3], x[2] * BAR) for i, x in enumerate(SECTIONS)}   # v24 OFFKEY: each section's first seed (sixteenth) and the sixteenths from seed to seed
    for name, pos, key, order, first in paid():
        semis = 0
        bare = ON['offkey'] and name in PAID['late'] and (pos - sown[name][0]) % sown[name][1] != 0   # v24 OFFKEY: a payment that begins off the beat where no seed is sown
        for j, c in enumerate(order):
            out.append({'at': pos / 4, 'len': PAID['len'], 'pitch': moved(first, semis), 'vel': PAID['vel'][0 if j == 0 else 1], **({'gain': f"{OFFKEY['db']}dB"} if bare and j == 0 else {})})
            pos, semis = pos + c, semis + PAID['steps'][0 if c == purse[key][0] else 1]
            while semis > PAID['fold'][1]:
                semis -= 12
            while semis < PAID['fold'][0]:
                semis += 12
        if ON['receipt'] and name in CLOSING['where']:          # v24 RECEIPT: where the payment ends, the note its coins come to
            out.append({'at': pos / 4, 'len': PAID['len'], 'pitch': moved(first, semis), 'vel': RECEIPT['vel'], **({'gain': f"{RECEIPT['db']}dB"} if RECEIPT['db'] else {})})
    return out


def clasp_notes(doc):
    """v25 CLASP: (the clasp's notes, {what: how many}, {section: its two-bar pattern}) read from the finished song: where the drum plays beats 2 and 4 and the purse can pay them."""
    tr = {t['name']: t for t in doc['tracks']}
    drum = {round(n['at'], 4) for n in tr['kick']['notes']} if 'kick' in tr else set()
    out, tell, told = [], {'whole': 0, 'miss': 0, 'rest': 0, 'snap': 0}, {}

    def ball(k, at, db=0):
        pitch, vel, own = CLASP['balls'][k]
        out.append({'at': round(at - (SHUT if k == 0 else 0), 4), 'len': CLASP['len'], 'pitch': pitch, 'vel': vel, **({'gain': f'{own + db:g}dB'} if own + db else {})})

    for i, (name, pairs, every, at16, notes, has_drum, bass) in enumerate(SECTIONS):
        sown = {k: sorted(n['at'] for n in tr[f'seed-{k}']['notes'] if i * SEC * 4 <= n['at'] < (i + 1) * SEC * 4 and round(n['at'] * 4) % BAR == at16 and (int(n['at'] // 4) - i * SEC) % every == 0)
                for k in CLASP['purses'] if f'seed-{k}' in tr}
        for bar in range(max(i * SEC, CLASP['from']), (i + 1) * SEC) if has_drum else ():
            for s16 in CLASP['on']:
                at = bar * 4 + s16 / 4
                gone = not any(bar * 4 <= x < bar * 4 + 4 for x in drum) or (bar in rolls() and s16 / 4 >= ROLL['beat'])   # the drum waits, or the roll has the beat
                if gone or (round(at, 4) not in drum and not at16):   # on the beat the drum plays four to the bar, and a beat it leaves out it has given to the purse; off the beat it plays one and three and the clasp has two and four to itself
                    tell['rest'] += 1
                    told.setdefault(name, []).append('-')
                    continue
                owed = [round((at - max(x for x in v if x <= at)) * 4) for k, v in sown.items() if any(x <= at for x in v)]
                can = any(a > 0 and coins_for(a, *purses()[k]) is not None for k, v in sown.items() if any(x <= at for x in v) for a in [round((at - max(x for x in v if x <= at)) * 4)])
                bare = 0 if round(at, 4) in drum else CLASP['bare'][s16]
                if can:
                    ball(0, at), ball(1, at, bare)
                    tell['whole'] += 1
                elif ON['miss']:
                    ball(0, at, CLASP['miss'])
                    tell['miss'] += 1
                told.setdefault(name, []).append(f"{min(owed) if owed else 0}{'' if can else '?'}")
    if ON['snap'] and ON['roll']:                                # v25 SNAP: the hand shuts the purse of small change on the one after every roll
        for b in sorted(rolls()):
            hard = CLASP['snap'] + (0 if round((b + 1) * 4, 4) in drum else CLASP['nodrum'])
            ball(0, (b + 1) * 4, hard), ball(1, (b + 1) * 4, hard)
            tell['snap'] += 1
    return sorted(out, key=lambda n: n['at']), tell, told


def product_patch(x, y):
    """v26 PRODUCT: the patch for a pair of coins: two sines at x and y times the note; MELTS: each ring-modulated by the other's (a silent copy before it), the blend rising from 0 to 1 over x sixteenths; HANDS: one to each side."""
    side = PRODUCT['hands'] if ON['hands'] else 0
    mix = {'value': 0, 'mod': [{'src': 'env.mul', 'amount': 1}]}
    coin = lambda r, pan, src: {'type': 'osc', 'wave': 'sine', 'ratio': r, 'phase': 0, **({'pan': pan} if pan else {}), **({'ringmod': {'from': src, 'mix': mix}} if ON['melts'] else {})}
    mute = lambda r: {'type': 'osc', 'wave': 'sine', 'ratio': r, 'phase': 0, 'level': '-140dB'}
    return {'about': f"Small Change: the till multiplies (v26): the purse's coins {x} and {y} as two plain tones at {x} and {y} times the note" + (f", each ring-modulated by the other over {x} sixteenths: they melt into {abs(x - y)} and {x + y} times the note (the product of two tones is their difference and their sum)" if ON['melts'] else '') + (', one from each side' if side else '') + '.',
            'synth': {'layers': ([mute(y), coin(x, -side, '0'), mute(x), coin(y, side, '2')] if ON['melts'] else [coin(x, -side, ''), coin(y, side, '')]),
                      **({'env': {'mul': {'a': f'{x * S16:.0f}ms', 'd': '1ms', 's': 1, 'r': '50ms'}}} if ON['melts'] else {}),
                      'amp': {'a': '4ms', 'd': '10ms', 's': 1, 'r': '40ms'}},
            'play': {'event_stable': True, 'vel_sens': 0.3, 'gate': 1}}


def product_notes(doc):
    """v26 PRODUCT: by pair of coins, the notes: before the seed of each of PRODUCT['bars'] in each of its sections, as long as the purse's two coins make, ending as the seed is sown; the note is the seed's three octaves down (home's chord: its key note)."""
    pairs_of = {**PAIRS, **FLIPPED, **INSIDE}
    seeds = sorted((n['at'], n['pitch'], t['name'].split('-')[1]) for t in doc['tracks'] if t['name'].split('-')[0] in ('seed', 'long') and t['name'].split('-')[-1] in pairs_of for n in t['notes'])
    out = {}
    for i, (name, pairs, every, at16, notes, drum, bass) in enumerate(SECTIONS):
        if not PRODUCT['sections'][0] <= i < PRODUCT['sections'][1] or at16:   # not off the beat: the gap before that seed is meant
            continue
        for b in PRODUCT['bars']:
            bar = i * SEC + b
            here = [s for s in seeds if bar * 4 <= s[0] < bar * 4 + 4]
            if not here:
                continue
            at, pitch, k = here[0]
            if name == 'home' and ON['chord']:
                at, pitch = bar * 4 + at16 / 4, STANDS['home']
            x, y = pairs_of[k]
            db = PRODUCT['trim'].get(bar, 0)
            out.setdefault((x, y), []).append({'at': round(at - (x + y) / 4, 4), 'len': (x + y) / 4, 'pitch': moved(pitch, PRODUCT['down']), 'vel': PRODUCT['vel'], **({'gain': f'{db:g}dB'} if db else {})})
    return out


def build():
    T = {'kick': [], 'bass': [], 'hat': [], **{f'seed-{k}': [] for k in purses()}, **({'seed-z': []} if ON['zeno'] and ON['roll'] else {}), **({'open': []} if ON['meet'] and ON['owed'] and ON['hat'] else {}), **{f'long-{k}': [] for k in purses()}}
    lifted = []                                                  # v17 LIFT: the bass's moved notes, an octave up
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
                kept = ON['long'] and not drum and (i < len(SECTIONS) - 1 or (ON['linger'] and (bar - i * SEC) // every < LINGER['seeds']))   # the opening and the break: into the long purse (v21 LINGER: and the last section's first seed)
                home = ON['chord'] and name == 'home'
                spelt = ON['spell'] and home and bar - i * SEC >= SEC // 2    # v11 SPELL: the chord counted out in the purse's coins
                back = ON['back'] and home and BACK['bars'][0] <= bar - i * SEC < BACK['bars'][1]   # v12 BACK: and the other way: five, then three
                for j, pitch in enumerate((HOME[::-1] if back else HOME) if home else [notes[n % len(notes)]]):
                    T[f"{'long' if kept else 'seed'}-{pairs[n % len(pairs)]}"].append({'at': bar * 4 + (at16 + (SPELL[j] if spelt else (0, SPELL[2] - SPELL[1], SPELL[2])[j] if back else 0)) / 4, 'len': 0.25, 'pitch': pitch, 'vel': 0.9,
                                                                                    **({'gain': f'{SOFT}dB'} if dense else {'gain': f'{HOME_DB}dB'} if home else {'gain': f'{LONG_DB}dB'} if kept and LONG_DB else {})})
                if ON['rate'] and 'hat-x' in T and name == EXCHANGE['section']:   # v9 RATE: what the exchange can pay of this seed, in its units
                    for amount in range(1, (COIN['upto'] if ON['through'] else RATE['upto']) + 1):
                        if coins_for(amount, *EXCHANGE['coins']) and (amount / EXCHANGE['per']) % 1:   # only the sums that fall between the sixteenths
                            T['hat-x'].append({'at': round(bar * 4 + at16 / 4 + amount / (4 * EXCHANGE['per']), 4), 'len': 0.1, 'pitch': 'A#4', 'vel': round(.95 - .13 * (coins_for(amount, *EXCHANGE['coins']) - 1), 2)})
                if ON['seven'] and ON['exchange'] and ON['debts'] and bass and name == EXCHANGE['section']:   # v9 SEVEN: the exchange's largest debt, in the bass
                    T['bass'].append({'at': round(bar * 4 + at16 / 4 + frobenius(*EXCHANGE['coins']) / (4 * EXCHANGE['per']), 4), 'len': 0.25, 'pitch': 'F2', 'vel': .85, **({'_term': frobenius(*EXCHANGE['coins']) / EXCHANGE['per']} if ON['term'] else {})})
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
                    if ON['bare'] and i + 1 < len(SECTIONS) and SECTIONS[i + 1][6] and not bass and bar == (i + 1) * SEC - 1:   # v15 BARE: the bar before the bass comes, the drum waits
                        continue
                    if ON['bought'] and name in BOUGHT and bar - i * SEC >= SEC // 2 and (bar - i * SEC) % every == 0 and beat * 4 == at16 + sum(purses()[pairs[(bar - i * SEC) % len(pairs)]]):   # v11 BOUGHT: the beat is the purse's
                        continue
                    T['kick'].append({'at': bar * 4 + beat, 'len': 0.5, 'pitch': 'G1', 'vel': .95 if beat == 0 else .88})
            pq = purses()[pairs[(bar - i * SEC) % len(pairs)]]  # the purse whose turn this bar is
            others = []
            mark = len(T['bass'])
            if bass and ON['debts']:
                for s in debts(*pq):
                    if ON['abroad'] and ON['exchange'] and name == EXCHANGE['section'] and (bar - i * SEC) % every == 0 and (s * EXCHANGE['per']) % 1 == 0 and coins_for(round(s * EXCHANGE['per']), *EXCHANGE['coins']):
                        continue                                 # v10 ABROAD: the exchange pays this one
                    if (at16 + s) % 4:                           # never with the drum
                        T['bass'].append({'at': bar * 4 + (at16 + s) % BAR / 4, 'len': 0.25, 'pitch': 'F2' if s == frobenius(*pq) else 'G2', 'vel': .85, **({'_term': s} if ON['term'] and s == frobenius(*pq) and (bar - i * SEC) % every == 0 else {})})   # v27 TERM: in the bar its seed is sown
                others = sorted({s for k in set(pairs) for s in debts(*purses()[k])} - set(debts(*pq))) if ON['owed'] else []   # v7: what the section's other purses cannot pay
                for s in others:
                    if (at16 + s) % 4:
                        T['bass'].append({'at': bar * 4 + (at16 + s) % BAR / 4, 'len': 0.25, 'pitch': OWED, 'vel': .85})
                if others:
                    T['bass'][-BAR:] = sorted(T['bass'][-BAR:], key=lambda x: x['at'])
            elif bass:
                for off, ln, p in ((2, 1.5, 'G2'), (7, 1, 'G2'), (10, 1.5, 'F2' if bar % 4 == 3 else 'G2')):
                    T['bass'].append({'at': bar * 4 + off / 4, 'len': ln / 4, 'pitch': p, 'vel': .85})
            if stands(name, notes, every, bar - i * SEC):       # v16 ROOT, FOLLOW: this bar's bass on its seed's key note
                for x in T['bass'][mark:]:
                    x['pitch'] = moved(x['pitch'], stands(name, notes, every, bar - i * SEC))
                    if ON['lift'] and stands(name, notes, every, bar - i * SEC) < 0:   # v17 LIFT: and an octave up, for a small speaker
                        lifted.append({**x, 'pitch': moved(x['pitch'], 12)})
            if drum and ON['hat']:
                for s, n_coins in coins(*pq).items():
                    if bass or n_coins == 1:                     # before the bass comes, only the two coins themselves
                        T['hat'].append({'at': bar * 4 + (at16 + s) % BAR / 4, 'len': 0.1, 'pitch': 'A#4', 'vel': round(.95 - .13 * (n_coins - 1), 2)})
                        if 'open' in T and s in others and (at16 + s) % 4:   # v8 MEET: it falls with one of the other purses' debts
                            if ON['let'] and s in {frobenius(*purses()[k]) for k in set(pairs) if purses()[k] != pq}:   # v14 LET: the debt is another purse's largest: it rings
                                T.setdefault('rung', []).append({**T['hat'][-1], 'len': RUNG['len'], 'gain': f"{LET['db']}dB"})
                            else:
                                T['open'].append({**T['hat'][-1], 'len': MEET['len']})
                        elif ON['rings'] and name in RINGS and bar - i * SEC >= SEC // 2 and (bar - i * SEC) % every == 0 and s == sum(pq) and (at16 + s) % 4:   # v12 RINGS: the sum, off the beat
                            T.setdefault('rung', []).append({**T['hat'][-1], 'len': RUNG['len']})
    if ON['seven'] and ON['exchange']:
        T['bass'].sort(key=lambda n: n['at'])
    if ON['term']:                                               # v27 TERM: the largest debt is owed as long as it is large, or until the next debt; SETTLED: then it is paid, on the key note
        order, kicks, terms, paid = sorted(T['bass'], key=lambda n: n['at']), {round(n['at'], 4) for n in T['kick']}, {}, []
        for x, nxt in zip(order, order[1:] + [None]):
            if '_term' not in x:
                continue
            term = x.pop('_term')
            held = min(term, (nxt['at'] - x['at']) * 4) if nxt else term
            held = min(held, ((x['at'] // (SEC * 4) + 1) * SEC * 4 - x['at']) * 4)   # not over a section's end
            if held <= 1:
                continue
            x['len'] = terms[round(x['at'], 4)] = round(held / 4, 4)
            if TERM['db']:
                x['gain'] = f"{TERM['db']}dB"
            end = round(x['at'] + term / 4, 4)
            if ON['settled'] and held == term and end not in kicks and end < BARS * 4 and not (nxt and round(nxt['at'], 4) == end):
                paid.append((round(x['at'], 4), {'at': end, 'len': 0.25, 'pitch': moved(x['pitch'], TERM['up']), 'vel': TERM['vel']}))
        up = {round(x['at'], 4) for x in lifted}
        for x in lifted:
            x.pop('_term', None)
            if round(x['at'], 4) in terms:
                x['len'] = terms[round(x['at'], 4)]
        for of, x in paid:
            T['bass'].append(x)
            if of in up:
                lifted.append({**x, 'pitch': moved(x['pitch'], 12)})
        T['bass'].sort(key=lambda n: n['at'])
        TERM['held'], TERM['paid'] = sorted(terms.items()), [x for _, x in paid]
    if lifted:
        T['bass-up'] = sorted(lifted, key=lambda n: n['at'])
    for sw in ('spun', 'lands'):                                 # v18: a coin spun on the counter, alternately left and right
        if ON[sw] and ON['hat']:
            clicks = spun((next(j for j, sct in enumerate(SECTIONS) if sct[0] == SPUN['where'][sw]) + 1) * SEC)
            stop = clicks[0] + SPUN['bars'] * 4
            for k, at in enumerate(clicks):
                note = {'at': at, 'len': 0.05, 'pitch': 'A#4', 'vel': round(SPUN['vel'][0] + (SPUN['vel'][1] - SPUN['vel'][0]) * k / len(clicks), 2)}
                if ON['metal']:                                  # v19 METAL: the coin's own note, and its ring on the stroke; DAMPED: by the gap to the next rattle
                    gap = ((clicks[k + 1] if k + 1 < len(clicks) else stop) - at) * 60 / BPM
                    note = {**note, 'pitch': METAL['note'], 'expr': {'ring': round(DAMPED['gaps'] * gap if ON['damped'] else METAL['ring'], 4)}}
                T.setdefault(f"spun-{'lr'[k % 2]}", []).append(note)
            if ON['flick'] and ON['metal']:                      # v19 FLICK: the coin is flicked
                T.setdefault('flick', []).append({'at': clicks[0], 'len': FLICK['len'], 'pitch': METAL['note'], 'vel': FLICK['vel'], 'expr': {'ring': FLICK['ring']}})
    if ON['tally'] and ON['metal'] and ON['hat']:                # v20 TALLY: the coin is put down for every amount the purse can pay
        for where, uptos, smaller in TALLY['where']:
            i = next(j for j, sct in enumerate(SECTIONS) if sct[0] == where)
            p, q = PAIRS[SECTIONS[i][1][0]]
            for k, upto in enumerate(uptos):
                at0 = (i * SEC + k * SECTIONS[i][2]) * 4 + SECTIONS[i][3] / 4
                for n in range(1, upto + 1):
                    for a in range(n // p + 1):
                        if (n - a * p) % q == 0:
                            b = (n - a * p) // q
                            T.setdefault('tally-' + ('m' if a and b else 'l' if a else 'r'), []).append({'at': at0 + n / 4 / smaller ** k, 'len': 0.05, 'pitch': METAL['note'], 'vel': TALLY['vel'], 'gain': f"{TALLY['coin'] * (a + b):g}dB", 'expr': {'ring': TALLY['ring']}})
    if ON['reckon'] and ON['tally'] and ON['metal'] and ON['hat']:   # v21 RECKON: the first change is counted too, from its third seed, with a worn coin
        i = next(j for j, sct in enumerate(SECTIONS) if sct[0] == RECKON['where'])
        p, q = PAIRS[SECTIONS[i][1][0]]
        for k, upto in RECKON['seeds']:
            at0 = (i * SEC + k * SECTIONS[i][2]) * 4 + SECTIONS[i][3] / 4
            for n in range(1, upto + 1):
                for a in range(n // p + 1):
                    if (n - a * p) % q == 0:
                        b = (n - a * p) // q
                        T.setdefault('reckon-' + ('m' if a and b else 'l' if a else 'r'), []).append({'at': at0 + n / 4, 'len': 0.05, 'pitch': METAL['note'], 'vel': RECKON['vel'], 'gain': f"{RECKON['coin'] * (a + b):g}dB", 'expr': {'ring': RECKON['ring']}})
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
                    'fx': [{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB'] + ([TERM['chest']] if ON['chest'] else [])}]},
                   {'name': 'bass', 'patch': DEBT['patch'] if ON['octave'] else 'sub-sine', 'gain': '-13dB', 'notes': T['bass'], 'fx': [under]}] +
                  ([{'name': 'bass-up', 'patch': DEBT['patch'] if ON['octave'] else 'sub-sine', 'gain': f"{-13 + LIFT['db']}dB", 'notes': T['bass-up'], 'fx': [under]}] if T.get('bass-up') else []) +   # v17 LIFT
                  [{'name': f'seed-{k}', 'patch': 'sc-seed', 'gain': {'value': '-3dB', 'mod': [{'src': 'auto.alone', 'amount': 1}]}, 'auto': {'alone': alone()},
                    'notes': T[f'seed-{k}'], 'fx': ['clip drive=0dB ceiling=-12dB']} for k in purses()],   # the seed's highest sample is its own, not the limiter's
    }
    if ON['octave']:                                             # v15 OCTAVE: the bass's own patch
        doc['patches'] = {**doc['patches'], DEBT['patch']: SC_DEBT}
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
    if T.get('rung'):                                            # v12 RINGS: the same hat, rung for three sixteenths
        rung = json.loads(json.dumps(OPEN))
        rung['about'] = "Small Change: the hat that rings on the purse's sum where it falls off the beat (v12). sc-open's hat with a decay of 1.2 s (6 dB a sixteenth), held three sixteenths and stopped, above 5 kHz."
        rung['synth']['layers'][0]['machine']['decay'] = RUNG['decay']
        rung['synth']['amp']['r'] = RUNG['release']
        doc['patches'] = {**doc['patches'], RUNG['patch']: rung}
        doc['tracks'].append({'name': 'rung', 'patch': RUNG['patch'], 'gain': RUNG['gain'], 'pan': RUNG['pan'], 'notes': T['rung']})
    if ON['hat']:
        doc['patches'] = {**doc['patches'], 'sc-hat': HAT}
        doc['tracks'].append({'name': 'hat', 'patch': 'sc-hat', 'gain': '4dB', 'pan': 0.15, 'notes': T['hat']})
        if T.get('hat-x'):                                       # v9 RATE: the second hat, on the other side
            if ON['coin']:                                       # v13 COIN: the other currency's own hat
                coin = json.loads(json.dumps(HAT))
                coin['about'] = "Small Change: the second hat, that ticks what the other currency can pay (v13). The first hat at two thirds: the machine's hat, 20 ms, from 3 to 5.5 kHz (its centre 5.5 kHz for the first hat's 8.3)."
                coin['synth']['layers'][0]['machine']['decay'] = COIN['decay']
                coin['synth']['filters'] = COIN['filters']
                doc['patches'] = {**doc['patches'], COIN['patch']: coin}
            doc['tracks'].append({'name': 'hat-x', 'patch': COIN['patch'] if ON['coin'] else 'sc-hat', 'gain': COIN['gain'] if ON['coin'] else RATE['gain'], 'pan': RATE['pan'], 'notes': T['hat-x']})
    metal = bool(ON['metal'] and (T.get('spun-l') or T.get('spun-r') or any(T.get('tally-' + x) for x in 'lmr')))   # v19 METAL: the spun coin's own patch (v20: and the counted coin's)
    if metal:
        doc['patches'] = {**doc['patches'], METAL['patch']: metal_patch()}
    for side, key in enumerate(('spun-l', 'spun-r')):            # v18 SPUN, LANDS: the spun coin's two pallets, closing as the coin's tilt does
        if T.get(key):
            pts = [['0b', 0]]
            for sw in ('spun', 'lands'):
                if ON[sw]:
                    c = spun((next(j for j, sct in enumerate(SECTIONS) if sct[0] == SPUN['where'][sw]) + 1) * SEC)
                    pts += [[f'{at}b', round(1 - (1 - k / len(c)) ** SPUN['close'], 4)] for k, at in enumerate(c)] + [[f'{c[0] + SPUN["bars"] * 4}b', 1], [f'{c[0] + SPUN["bars"] * 4 + 0.05}b', 0]]
            doc['tracks'].append({'name': key, 'patch': METAL['patch'] if metal else COIN['patch'] if COIN['patch'] in doc['patches'] else 'sc-hat', 'gain': METAL['gain'] if metal else SPUN['gain'], 'notes': T[key],
                                  'pan': {'value': SPUN['pans'][side], 'mod': [{'src': 'auto.close', 'amount': -SPUN['pans'][side]}]}, 'auto': {'close': {'points': pts, 'curve': 0}}})
    if metal and T.get('flick'):                                 # v19 FLICK: one stroke of the coin in the middle
        doc['tracks'].append({'name': 'flick', 'patch': METAL['patch'], 'gain': f"{float(METAL['gain'][:-2]) + FLICK['db']:g}dB", 'pan': 0, 'notes': T['flick']})
    for key, pan in (('tally-l', -TALLY['pan']), ('tally-m', 0), ('tally-r', TALLY['pan'])):   # v20 TALLY: the first coin alone on the left, the second alone on the right, both in the middle
        if T.get(key):
            doc['tracks'].append({'name': key, 'patch': METAL['patch'], 'gain': TALLY['gain'], 'pan': pan, 'notes': sorted(T[key], key=lambda n: n['at'])})
    for key, pan in (('reckon-l', -RECKON['pan']), ('reckon-m', 0), ('reckon-r', RECKON['pan'])):   # v21 RECKON: the worn coin: the same patch through low-passes on its tracks
        if T.get(key):
            doc['tracks'].append({'name': key, 'patch': METAL['patch'], 'gain': RECKON['gain'], 'pan': pan, 'notes': sorted(T[key], key=lambda n: n['at']), 'fx': [f"lp cutoff={RECKON['lp']}"] * RECKON['walls']})
    if ON['paid'] and key_notes():                               # v23 PAID: the bar itself is paid, by a wooden key
        doc['patches'] = {**doc['patches'], PAID['patch']: KEY}
        doc['tracks'].append({'name': 'key', 'patch': PAID['patch'], 'gain': PAID['gain'], 'pan': PAID['pan'], 'notes': key_notes()})
    if ON['rounded']:                                            # v22 ROUNDED: the purse's change rounded to a grid at every payment; in the second section its time too
        at = SEC * 4 * [x[0] for x in SECTIONS].index(ROUNDED['time'])   # the beat at which the time is rounded too
        free = round(log2(ROUNDED['free'] / ROUNDED['rate']) / ROUNDED['octaves'], 4)   # the lane's value at which the crusher holds nothing (the engine's own rate)
        for k in ROUNDED['buses']:
            if k in doc['buses']:
                doc['buses'][k] = {**doc['buses'][k], 'fx': list(doc['buses'][k].get('fx', [])) + [f"crush bits={ROUNDED['bits']} rate={ROUNDED['rate']}+auto.held*{ROUNDED['octaves']}"],
                                   'auto': {**doc['buses'][k].get('auto', {}), 'held': {'points': [['0b', free], [f'{at - 0.01}b', free], [f'{at}b', 0], [f'{at + SEC * 4}b', 1]], 'curve': 0}}}
    if ON['clasp']:                                              # v25 CLASP: the purse's clasp, on the beats the purse can pay
        doc['patches'] = {**doc['patches'], CLASP['patch']: CLASP_PATCH}
        doc['tracks'].append({'name': 'clasp', 'patch': CLASP['patch'], 'gain': CLASP['gain'], 'pan': CLASP['pan'], 'notes': clasp_notes(doc)[0]})
    if ON['product']:                                            # v26 PRODUCT: the purse's two coins as notes, multiplied, before a seed
        for (x, y), notes in product_notes(doc).items():
            doc['patches'] = {**doc['patches'], f"{PRODUCT['patch']}-{x}{y}": product_patch(x, y)}
            doc['tracks'].append({'name': f'product-{x}{y}', 'patch': f"{PRODUCT['patch']}-{x}{y}", 'gain': PRODUCT['gain'], 'notes': notes})
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
        ap.add_argument(f"--{'without' if on else 'with'}-{k}", action='store_true', help=f"{'leave out' if on else 'put in'} {k} (of those that are on: the last three off is v26, the last six v25, the last nine v24, the last twelve v23, the last fifteen v22, the last sixteen v21, the last eighteen v20, the last nineteen v19, the last twenty-two v18, the last twenty-four v17, the last twenty-eight v16, the last thirty v15, the last thirty-two v14, the last thirty-three v13, the last thirty-five v12, the last thirty-seven v11, the last thirty-nine v10, the last forty-two v9, the last forty-five v8, the last forty-seven v7, the last forty-nine v6, the last fifty-three v5, the last fifty-four v4, the last fifty-seven v3, the last sixty-one v2, all sixty-four v1)")
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
            upto = COIN['upto'] if ON['through'] else RATE['upto']
            print(f"    a second hat plays what the exchange can pay, in its units, up to {upto}, where it falls between the sixteenths: " + ' '.join(str(a) for a in range(1, upto + 1) if coins_for(a, *EXCHANGE['coins']) and (a / EXCHANGE['per']) % 1))
            if ON['coin']:
                print(f"    the second hat is a coin of its own ({COIN['patch']}): the first hat at two thirds, {COIN['decay'][:-2]} ms and from 3 to 5.5 kHz")
        if ON['abroad'] and ON['exchange'] and ON['debts']:
            print(f"    at {EXCHANGE['section']}, after each chord, the bass leaves the debts the exchange can pay: " + ', '.join(f"{s} sixteenths ({round(s * EXCHANGE['per'])} of its units)" for s in debts(*purses()['a']) if (s * EXCHANGE['per']) % 1 == 0 and coins_for(round(s * EXCHANGE['per']), *EXCHANGE['coins'])))
        if ON['herald'] and ON['exchange']:
            print(f"    the change before {EXCHANGE['section']} is in the other currency: a seed for the exchange alone on beat {HERALD['beat'] + 1} of the bar before, {HERALD['pitch']}" + ('; the second hat counts it: ' + ' '.join(str(a) for a in range(1, round((4 - HERALD['beat']) * 4 * EXCHANGE['per'])) if coins_for(a, *EXCHANGE['coins'])) + ' units' if ON['count'] and ON['hat'] else ''))
        if ON['seven'] and ON['exchange'] and ON['debts']:
            print(f"    the bass plays the exchange's largest debt: {frobenius(*EXCHANGE['coins'])} of its units after each chord, on F2")
        home_at = [k for k, sec in enumerate(SECTIONS) if sec[0] == 'home']
        if ON['spell'] and ON['chord'] and home_at:
            print(f"    home's chord is counted out in its second half (bars {home_at[0] * SEC + SEC // 2 + 1}-{(home_at[0] + 1) * SEC}): " + ', '.join(f'{p} on sixteenth {x}' for p, x in zip(HOME, SPELL)) + ': three, then five')
        if ON['back'] and ON['chord'] and home_at:
            print(f"    and the other way before that (bars {home_at[0] * SEC + BACK['bars'][0] + 1}-{home_at[0] * SEC + BACK['bars'][1]}): " + ', '.join(f'{p} on sixteenth {x}' for p, x in zip(HOME[::-1], (0, SPELL[2] - SPELL[1], SPELL[2]))) + ': five, then three')
        if ON['rings'] and ON['hat']:
            print('    the hat rings where the purse\'s two coins first meet off a beat: ' + '; '.join(f"{sct[0]}: sixteenth {(sct[3] + sum(sct_pq)) % BAR} (bars " + ' '.join(str(b + 1) for b in range(k * SEC + SEC // 2, (k + 1) * SEC, sct[2])) + ')' for k, sct in enumerate(SECTIONS) if sct[0] in RINGS for sct_pq in [purses()['d' if ON['flip'] and sct[3] and sct[1][0] == 'a' else sct[1][0]]]))
        for k, sct in enumerate(SECTIONS):
            if ON['bought'] and sct[0] in BOUGHT:
                print(f"    the drum gives beat {(sct[3] + sum(purses()[sct[1][0]])) // 4 + 1} to the purse in the second half of {sct[0]}, where {' and '.join(str(c) for c in purses()[sct[1][0]])} make {sum(purses()[sct[1][0]])}: bars " + ' '.join(str(b + 1) for b in range(k * SEC + SEC // 2, (k + 1) * SEC, sct[2])))
        if ON['meet']:
            print('    the hat is let ring where it meets one of the other purses\' debts in the bass')
            if ON['let'] and ON['owed'] and ON['hat']:
                met = [n for n in build().get('rung', []) if not any(i * SEC + SEC // 2 <= n['at'] // 4 < (i + 1) * SEC for i, sec in enumerate(SECTIONS) if sec[0] in RINGS and ON['rings'])]
                print("    and really rings where that debt is the other purse's largest: " + '; '.join(f"{sec[0]}: {len([n for n in met if i * SEC <= n['at'] // 4 < (i + 1) * SEC])} strokes, sixteenths {' '.join(str(x) for x in sorted({round(n['at'] % 4 * 4) for n in met if i * SEC <= n['at'] // 4 < (i + 1) * SEC}))}" for i, sec in enumerate(SECTIONS) if any(i * SEC <= n['at'] // 4 < (i + 1) * SEC for n in met)))
        if ON['owed']:
            print(f'    where purses share a section the bass also plays what the others cannot pay, on {OWED}: ' + '; '.join(f"{name}: " + ', '.join(f"{k} {' '.join(str(s) for s in sorted(set(debts(*purses()[k])) | {s for j in pairs for s in debts(*purses()[j])}) if s % 4)}" for k in pairs) for name, pairs, *_ in SECTIONS if len(pairs) > 1))
        T = build()
        if ON['bare']:
            print('    the bar before the bass comes, the drum waits: ' + ', '.join(f'bar {(i + 1) * SEC}' for i, sec in enumerate(SECTIONS[:-1]) if SECTIONS[i + 1][6] and not sec[6] and sec[5]))
        if ON['octave']:
            print("    the bass has its octave: sc-debt, the second harmonic 9 dB under the note")
        if ON['root']:
            print("    where a section has one seed the bass stands on that seed's key note, three coins on: " + ', '.join(f"{sec[0]} (seed {sec[4][0]}) on {moved('G2', stands(sec[0], sec[4], sec[2], 0))}" for sec in SECTIONS if sec[6] and len(sec[4]) == 1 and not follows(sec[0])))
        if ON['follow']:
            print('    where the seeds change the bass follows each: ' + '; '.join(f"{sec[0]}: " + ', '.join(f"bars {i * SEC + k + 1}-{i * SEC + k + sec[2]} {moved('G2', stands(sec[0], sec[4], sec[2], k))}" for k in range(0, SEC, sec[2])) for i, sec in enumerate(SECTIONS) if sec[6] and sec[0] in STANDS['follow']))
            for k, name in FOLLOWS.items():
                if ON[k]:
                    j, sct = next((j, sct) for j, sct in enumerate(SECTIONS) if sct[0] == name)
                    print(f"    and in {name} (bars {j * SEC + 1}-{(j + 1) * SEC}), {'a bar' if sct[2] == 1 else f'{sct[2]} bars'} each: " + ' '.join(moved('G2', stands(name, sct[4], sct[2], q)) for q in range(0, SEC, sct[2])))
        if ON['lift'] and (ON['root'] or ON['follow']):
            print(f"    wherever the bass is under its written note a second track plays it an octave up, {-LIFT['db']} dB under: " + f"{len(T.get('bass-up', []))} notes")
        for sw, what in (('spun', 'it stops dead on the one where the drum comes back'), ('lands', "it starts in step with the hat and runs away from it, and stops dead on the last section's first seed, as the drum and the bass leave")):
            if ON[sw] and ON['hat']:
                j = next(j for j, sct in enumerate(SECTIONS) if sct[0] == SPUN['where'][sw])
                c = spun((j + 1) * SEC) + [(j + 1) * SEC * 4]
                print(f"    a coin is spun on the counter through the last {SPUN['bars']} bars of {SPUN['where'][sw]} (bars {(j + 1) * SEC - SPUN['bars'] + 1}-{(j + 1) * SEC}): {len(c) - 1} rattles over {SPUN['bars'] * 16} sixteenths, left and right by turns and closing to the middle as its tilt does, quickening as (t0 - t)^(-1/3): the gap goes " + ' '.join(f'{(b - a) * sec * 250:.0f}' for a, b in zip(c[:4], c[1:5])) + ' ... ' + ' '.join(f'{(b - a) * sec * 250:.0f}' for a, b in zip(c[-5:], c[-4:])) + f' ms; {what}')
        if ON['metal'] and ON['hat'] and (ON['spun'] or ON['lands']):
            print(f"    the coin is metal: a thin plate's modes from 4.2 kHz up (its note is {METAL['note']}, the seed's three octaves up), with a click on its front" + (f"; each rattle rings {DAMPED['gaps']} gaps and no more (T60), so the ring goes " + ' '.join(f'{1000 * DAMPED["gaps"] * (b - a) * 60 / BPM:.0f}' for a, b in list(zip(spun(SEC), spun(SEC)[1:]))[:3]) + ' ... ' + ' '.join(f'{1000 * DAMPED["gaps"] * (b - a) * 60 / BPM:.0f}' for a, b in list(zip(spun(SEC), spun(SEC)[1:] + [SEC * 4]))[-3:]) + ' ms: the table chokes it as it lies down' if ON['damped'] else f"; every rattle rings {1000 * METAL['ring']:.0f} ms") + (f"; and it is flicked: one stroke in the middle on its first instant, let ring {FLICK['ring']} s" if ON['flick'] else ''))
        if ON['reckon'] and ON['tally'] and ON['metal'] and ON['hat']:
            j = next(x for x, sct in enumerate(SECTIONS) if sct[0] == RECKON['where'])
            pp, qq = PAIRS[SECTIONS[j][1][0]]
            print(f"    the first change is counted too, with a worn coin (nothing over 10 kHz): in {RECKON['where']}, after its seeds in bars {' '.join(str(j * SEC + k * SECTIONS[j][2] + 1) for k, _ in RECKON['seeds'])} a clink on every amount the purse can pay, in sixteenths: {' '.join(str(n) for n in range(1, frobenius(pp, qq) + 1) if any((n - a * pp) % qq == 0 for a in range(n // pp + 1)))}, and from {frobenius(pp, qq) + 1} every one, to {', then to '.join(str(u) for _, u in RECKON['seeds'])}")
        if ON['paid'] and paid():
            pays = paid(); pr = purses()
            said = {}
            for nm, pos, key, order, first in pays:
                said.setdefault((key, sum(order)), []).append(order)
            print('    the bar is paid: a wooden key (sc-key) is pressed once for each coin, where the coin begins; a different order each time until every order has been used: ' +
                  '; '.join(f"coins {' and '.join(str(c) for c in pr[key])} pay {amount} in {len(ways(*pr[key], amount))} orders ({', '.join(' '.join(str(c) for c in o) for o in ways(*pr[key], amount))}), {len(v)} payments" for (key, amount), v in said.items()))
            nm, pos, key, order, first = pays[0]
            print(f"    each coin moves the key's note as it moves the purse's change (the first coin up a fifth, the second down a fourth): whatever the order, the same notes, an octave over the seed's: bars {pos // BAR + 1} on: " +
                  ' | '.join(' '.join(n['pitch'] for n in key_notes()[sum(len(x[3]) for x in pays[:j]):sum(len(x[3]) for x in pays[:j + 1])]) for j in range(6)))
            by = {}
            for nm, pos, key, order, first in pays:
                by.setdefault(nm, []).append(pos)
            print('    the key plays in: ' + '; '.join(f"{nm} (bars {v[0] // BAR + 1}-{(v[-1] + next(sum(x[3]) for x in pays if x[1] == v[-1]) - 1) // BAR + 1}, {len(v)} payments" + (f", from sixteenth {v[0] % BAR}" if v[0] % BAR else '') + ')' for nm, v in by.items()))
            if ON['offkey'] and any(x[0] in PAID['late'] for x in pays):
                print(f"    off the beat a payment's first stroke (sixteenth {next(x[1] for x in pays if x[0] in PAID['late']) % BAR}) is {-OFFKEY['db']} dB down where no seed is sown with it: {sum(1 for n in key_notes() if n.get('gain') == str(OFFKEY['db']) + 'dB')} strokes")
            if ON['closing'] and any(x[0] in CLOSING['where'] for x in pays):
                home = [x for x in pays if x[0] in CLOSING['where']]
                ends = [n['pitch'] for n in key_notes() if any(n['at'] * 4 == x[1] + sum(x[3]) for x in home)]
                print(f"    the till closes at home: a payment to each seed, bars {' '.join(str(x[1] // BAR + 1) for x in home)}: the {len(home)} orders of {' '.join(str(c) for c in sorted(home[0][3]))}, each once more: {', '.join(' '.join(str(c) for c in x[3]) for x in home)}" +
                      (f"; and after each its receipt, on the bar line where it ends: the note its coins come to, whatever their order: {' '.join(ends)}" if ON['receipt'] else ''))
            if ON['cannot'] and any(sum(x[3]) != BAR for x in pays):
                rest = [j * SEC + SEC for j, sct in enumerate(SECTIONS) if sct[0] in PAID['cannot']]
                print(f"    fives and sevens cannot make sixteen: the key pays {PAID['long']} (a bar and a half), three payments to two bars; bar {' '.join(str(b) for b in rest)} is left over, sixteen, which that till cannot pay: the key rests")
        if ON['rounded']:
            sec_r = [x[0] for x in SECTIONS].index(ROUNDED['time'])
            print(f"    the change is rounded to the coin in the purse of 5 and 3 (bars {(sec_r - 1) * SEC + 1}-{(sec_r + 1) * SEC}): to {2 ** ROUNDED['bits']} amounts at every payment; and from bar {sec_r * SEC + 1} its time too: each sample held longer, the rate falling from {ROUNDED['rate'] / 1000:g} kHz to {ROUNDED['rate'] * 2 ** ROUNDED['octaves'] / 1000:g} kHz by bar {(sec_r + 1) * SEC}; the purse of 3 and 5 beside it is paid in full")
        if ON['linger'] and ON['long']:
            print(f"    the last section's first seed (bar {(len(SECTIONS) - 1) * SEC + 1}) goes into the long purse, as the song's first four do: its change rings on through the three bars after it")
        if ON['tally'] and ON['metal'] and ON['hat']:
            for where, uptos, smaller in TALLY['where']:
                j = next(x for x, sct in enumerate(SECTIONS) if sct[0] == where)
                pp, qq = PAIRS[SECTIONS[j][1][0]]
                can = [n for n in range(1, max(uptos) + 1) if any((n - a * pp) % qq == 0 for a in range(n // pp + 1))]
                run, seeds = frobenius(pp, qq) + 1, len(uptos)
                print(f"    the coin counts the change in {where}: after {'each of its first ' + str(seeds) + ' seeds' if seeds > 1 else 'its first seed'} (bar{'s' if seeds > 1 else ''} {' '.join(str(j * SEC + k * SECTIONS[j][2] + 1) for k in range(seeds))}) a clink on every amount the purse can pay, in {'sixteenths' if smaller == 1 else 'the coins each seed is paid in (sixteenths, then thirty-seconds)'}: {' '.join(str(n) for n in can if n < run)}, and from {run} every one, to {', then to '.join(str(u) for u in uptos)} ({frobenius(pp, qq)} is the largest that cannot be made of {pp}s and {qq}s" + (f'; {pp * qq} is the first made two ways, and is struck on both sides' if max(uptos) >= pp * qq else '') + f"); {pp}s alone on the left, {qq}s alone on the right, both in the middle; {-TALLY['coin']:g} dB quieter with each coin")
        if ON['clasp']:
            _, c_tell, c_told = clasp_notes(song())
            print(f"    the purse has a clasp ({CLASP['patch']}): two balls, {CLASP['balls'][0][0]} {1000 * SHUT * 60 / BPM:.0f} ms before the beat and {CLASP['balls'][1][0]} on it, on beats 2 and 4 from bar {CLASP['from'] + 1}, where the drum has not given the beat away and the purse can pay it (the sixteenths since the section's last seed are an amount its coins make): {c_tell['whole']} whole" +
                  (f", {c_tell['miss']} that do not catch (the first ball only: the purse cannot pay)" if ON['miss'] else '') + f"; it rests on the {c_tell['rest']} beats the drum gives away" +
                  (f"; and the hand that shuts the purse of small change is heard: a snap on the one of bars {' '.join(str(b + 2) for b in sorted(rolls()))}" if ON['snap'] and ON['roll'] else ''))
            print('    what each backbeat owes, by section (its first four bars; ? is a debt): ' + '; '.join(f"{nm}: {' '.join(v[:8])}" for nm, v in c_told.items()))
        if ON['product']:
            made = product_notes(song())
            print(f"    the till multiplies ({PRODUCT['patch']}-..): before the seed of bars {', '.join(str(b + 1) for b in PRODUCT['bars'])} of each section from {SECTIONS[PRODUCT['sections'][0]][0]} to {SECTIONS[PRODUCT['sections'][1] - 1][0]} (not off the beat), the purse's two coins sound as notes, the seed's note three octaves down times each coin, for as many sixteenths as the two make" +
                  (", and are multiplied as they sound (ring modulation): over the first coin's length they melt into their difference and their sum, which ring for the second's" if ON['melts'] else '') + (', one coin from each side' if ON['hands'] else '') + ': ' +
                  '; '.join(f"{x} x {y}" + (f" gives {abs(x - y)} and {x + y}" if ON['melts'] else '') + f": {len(v)} (bars {' '.join(str(int(q['at'] // 4) + 1) for q in v)})" for (x, y), v in made.items()) + f"; {sum(len(v) for v in made.values())} notes")
        if ON['term'] and TERM.get('held'):
            t_lens = {}
            for _, t_len in TERM['held']:
                t_lens[t_len] = t_lens.get(t_len, 0) + 1
            print("    a debt has a term: the bass owes the purse's largest debt as long as it is large, or until the next debt: " + ', '.join(f'{t_n} of {t_len * 4:g} sixteenths' for t_len, t_n in sorted(t_lens.items(), reverse=True)) +
                  f": {len(TERM['held'])} held notes: " + ', '.join(f"{SECTIONS[t_i][0]} {t_c}" for t_i, t_c in ((t_i, sum(1 for t_at, _ in TERM['held'] if t_i * SEC * 4 <= t_at < (t_i + 1) * SEC * 4)) for t_i in range(len(SECTIONS))) if t_c))
            if ON['settled'] and TERM.get('paid'):
                print(f"    and when its term is up the debt is settled: the bass is back on the key note for a sixteenth at that instant: {len(TERM['paid'])} notes (not where the instant is the drum's): " + ' '.join(sorted({t_x['pitch'] for t_x in TERM['paid']})))
        if ON['chest']:
            print(f"    the drum has a chest: a bell on its own track: {TERM['chest']}")
        print(f'{BARS} bars, {BARS * sec:.1f} s; written notes: ' + ', '.join(f'{k} {len(v)}' for k, v in T.items() if v or not k.startswith('long-')))
    else:
        a.out.write_text(dump(song()))
