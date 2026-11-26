#!/usr/bin/env python3
"""Least Common (chirpers11, track 2). Clicky minimal techno, 126 BPM, G minor, 210 bars (6:40).

THE RULE. Three clicks keep cycles of 3, 5 and 7 sixteenths against a bass drum on every fourth. They are never
told what to do after that: everything else in the song is what happens when they MEET.
  two meet   -> a ping. 3 with 5 (every 15 sixteenths) rings D, 3 with 7 (every 21) B flat, 5 with 7 (every 35) F.
  three meet -> a chord (every 105 sixteenths: six bars and nine sixteenths).
  three meet ON THE BASS DRUM -> the song turns a page (every 420 sixteenths: 26 bars and a beat. So the pages turn
                on beat two, then beat three, then beat four).
  all meet ON THE ONE -> once in 105 bars (1680 sixteenths = 3 x 5 x 7 x 16). That is a HALF of the song.
Between two chords the pings fall on sixteenths 15 21 30 35 42 45 60 63 70 75 84 90: twelve notes, the same forwards
and backwards (gaps 15 6 9 5 7 3 15 3 7 5 9 6 15). Nobody wrote that tune. It comes round every 105 sixteenths, nine
sixteenths later in the bar each time, so it visits every sixteenth of the bar once before it is home.

THE SECOND HALF IS THE FIRST, ONE SIZE UP: cycles of 3, 5 and 7 BEATS against the bar of four. 3 x 5 x 7 x 4 beats is
105 bars again. Each long cycle is filled with the NEXT one's number, spread as evenly as it goes (Euclid): five
strokes in the three beats, seven in the five, three in the seven. Their meetings are the same tune four times
slower, so it is held, not struck: a tone that changes when two cycles begin together. From the seventh page the small
tune comes back over it (pings where cycles of 3, 5 and 7 sixteenths WOULD meet, though nobody is playing them): the
same tune at two sizes at once.

The four's own parts (bass, off-beat hat, clap) come in a page at a time and are the only things placed by page. The
chord is Give or Take's (track 1: G minor seventh) with its ninth on top, so the two songs can be laid over each other.

v2 (26 Nov): WHAT A MEETING DOES. In v1 a meeting was only a note. Six switches, each `--without-…` (all six off
is v1 byte for byte); every one is driven by the same count, how far it is to the next time all three meet:
  PLACE   the three and the five walk apart from the centre and back between two meetings of all three (the three
          to the left, the five to the right, the seven stays), so a chord is also three sounds arriving at one
          place. One size up in the second half: the walk takes a page.
  NEAR    the clicks are loudest where the three meet and NEAR dB quieter half way between.
  DOOR    a far room behind the clicks. Its door is shut when a page turns and opens a step each time the three
          meet (four steps to a page); the page turn shuts it again. In the last stretch of the first half, where the
          four stops, it is wide open: the clicks walk to the one alone in a hall. One size up in the second half:
          a step a page, wide open on the last.
  MEMORY  a click keeps the note of the last meeting it was in. The five's tock is on G after a chord, D after it
          meets the three, F after the seven; the seven's knock on G, B flat (the three), F (the five). Two tunes
          nobody wrote, in place of one note struck 400 times. Both are an octave under the pings.
  ROOTS   the bass keeps its rhythm and takes its note from the last meeting of any two (G2 after a chord, D2,
          B flat 2, F2): a bass line that the cycles write.
  BREAK   what the half does, one size down. Before each page of the first half turns, from the last time the five
          and the seven meet (35 sixteenths: two bars and three), the four stops, and the clicks walk to the page
          turn alone, the far room wide open. The page turns on the drum and the door shuts.

v3 (26 Nov): THE SPRING. The two halves were joined by a stop. Eight switches (`--without-rundown`, `-windup`,
`-through`, `-seven`, `-swing`, `-line`, `-rest`, `-wide`; all eight off is v2 byte for byte):
  RUNDOWN  the clock runs down by halves. In the last stretch of the first half (105 sixteenths, the four already
           stopped) each click loses every other stroke, and then every other one again: cycles of 3, 5 and 7
           sixteenths, then eighths, then beats. It is 3 against 5 against 7 at every size, and the size it
           reaches is the second half's, so the one arrives at the tempo the clicks have already come down to. A
           ping is as loud as the quieter of the two that meet, so the tune thins out with them.
  WINDUP   and is wound up at the end. In the last stretch of the second half the big cycles lose their fillings
           and the small cycles come back the same way backwards: every fourth stroke is already there (it is
           the head of the big cycle), then every second, then every one. The song reaches home at the size it
           began at, 3 against 5 against 7 sixteenths, so that it could begin again.
  THROUGH  the tune goes through the door as well. The pings, the chord and the held tone are sent to the far room
           (the clicks alone moved it 0.6 dB), so what a meeting makes is heard further off as the door opens.
  SEVEN    the seven was the quietest thing in the song (15 to 19 dB under the mix): 1.5 dB up.
  LINE     the bass keeps its line. In the second half it took its note from the big cycles' meetings and so held
           one note for five to nine bars: twenty slow changes that the scorer heard as twenty small sections,
           most of them alike. Now it goes on following the small cycles' meetings, as in the first half (nobody
           is playing them, but the drum's sixteenths still count them): the first half's tune stays in the bass
           under the second half's held tones, the same tune at two sizes from the one on.
  REST     the second half gets the breaks the first has, one size up: before each of its pages turns, from the
           last time the three and the five BEATS meet (60 sixteenths: three bars and three), the four stops
           and the clicks walk to the page turn alone.
  WIDE     the far room 6 dB up, so that the door is heard, and thinner (nothing under 900 Hz comes back from it).
  SWING    the door swings. It stepped open when the three met; now it opens all the way through each stretch,
           to the next step's place, so the tune moves off steadily and the page turn brings it back at once.

Form as arithmetic: everything below is computed from CYCLES, BAR and BEAT. Nothing is typed as a bar number.
"""
import argparse
import json
from math import lcm
from pathlib import Path

BPM = 126
BEAT, BAR = 4, 16                       # sixteenths
CYCLES = (3, 5, 7)                      # the three clicks, sixteenths (first half) or beats (second half)
VOICES = ('three', 'five', 'seven')
SUPER = lcm(*CYCLES)                    # 105: the three meet
PAGE = lcm(SUPER, BEAT)                 # 420: the three meet on the bass drum
HALF = lcm(SUPER, BAR)                  # 1680: all meet on the one (105 bars)
TOTAL = 2 * HALF
assert (SUPER, PAGE, HALF) == (105, 420, 1680) and HALF % BAR == 0 and PAGE // BEAT % 4 == 1
KEY = 'G'
PING = {(3, 5): 'D5', (3, 7): 'Bb4', (5, 7): 'F4'}          # the commonest meeting gets the plainest note
TONE = {(3, 5): 'D4', (3, 7): 'Bb3', (5, 7): 'F3'}           # the same three notes an octave down, held
CHORD = ('G3', 'Bb3', 'D4', 'F4', 'A4')
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers11-t2.yaml'

# ---- v2: the switches and their numbers. Nothing above is changed by them.
ON = {'place': True, 'near': True, 'door': True, 'memory': True, 'roots': True, 'break': True,
      'rundown': True, 'windup': True, 'through': True, 'seven': True, 'swing': True, 'line': True, 'rest': True, 'wide': True}
FLOOR = -24                             # dB a stroke has fallen to when it goes (RUNDOWN), or comes in at (WINDUP)
THROUGH = '-6dB'                        # the tune's send to the far room
THROUGH_DRY = -1.5                      # dB on the pings' own fader with it (547 Hz was 7.8 dB over the envelope already)
SEVEN_DB = 1.5                          # (2.5 put 641 Hz 9 dB over the envelope)
ALL = tuple(CYCLES)
WIDE = 0.8                              # how far from the centre a click stands when it is furthest from a meeting of all three
NEAR = 5                                # dB quieter there
LIFT = 2                                # dB on the clicks' faders with NEAR on (the ride takes 2.5 dB off on average)
DOOR = (-60, -12, -6, 0)                # the far room's fader, by how many times the three have met since the page turned
FAR = '-3dB'                            # each click's send to the far room
# The notes are the pings' own (D, B flat, F; G for the chord), each click an octave under the pings (the tock on the
# pings' own octave stacked with them, 13 dB over the envelope at 547 Hz; an octave over them, 12 over at 1.2 kHz).
MEMORY = {'five': {(3, 5): 'D4', (5, 7): 'F4', ALL: 'G4'}, 'seven': {(3, 7): 'Bb3', (5, 7): 'F3', ALL: 'G3'}}
ROOT = {(3, 5): 'D2', (3, 7): 'Bb2', (5, 7): 'F2', ALL: 'G2'}
ROOTS_DB = -3                           # the bass's fader with ROOTS on, beside v1's (this patch is 14 dB louder than the sine it replaces)
LC_ROOT = {'about': 'Least Common: the bass once the meetings write its line (v2). A sine and its octave, so that a line on 73 to 117 Hz is also heard on 147 to 233.',
           'synth': {'layers': [{'wave': 'sine'}, {'wave': 'sine', 'semi': 12, 'level': '-6dB'}], 'amp': {'a': '4ms', 'd': '0s', 's': 1, 'r': '60ms'}},
           'play': {'event_stable': True, 'vel_sens': 0.3}}
BREAK = lcm(*CYCLES[1:])                # 35: the last meeting of the five and the seven before a page turns
TURNS = [p * PAGE for p in range(1, HALF // PAGE)]   # the page turns of the first half (the half itself has its own, v1's)
REST = lcm(*CYCLES[:2]) * BEAT          # 60: v3, the second half's break. The last meeting of the three and the five BEATS before a page turns (3 bars and 3)
TURNS2 = [HALF + t for t in TURNS]      # the page turns of the second half
WIDE_DB = 6                             # v3: the far room's own fader (at 0 dB it added 0.6 dB to the clicks alone)
WIDE_HP = 900                           # and its high-pass with it (at 500 the wider room put 547 and 641 Hz 9 dB over the envelope and the low end 2 dB down beside them)


def broken(s):
    """Is sixteenth s in a break (the four stopped before a page turn)?"""
    return (ON['break'] and any(t - BREAK <= s < t for t in TURNS)) or (ON['rest'] and any(t - REST <= s < t for t in TURNS2))

TOCK = {'about': 'Least Common: the click that counts five, once it has a tune (v2). The same wooden bar damped twice as fast, so that a note it keeps for twenty strokes is a colour and not a drone.',
        'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '28ms', 'bright': 0.8, 'damp': 0.4, 'strike': 0.4}],
                  'amp': {'a': '0.2ms', 'd': '45ms', 's': 0, 'r': '20ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}}
TOCK_DB = 0                            # the five's fader with MEMORY on, beside v1's


def order(c, s):
    """2 where the cycle of c beats begins, 1 where the cycle of c eighths does, 0 on its other sixteenth strokes."""
    return 2 if s % (4 * c) == 0 else 1 if s % (2 * c) == 0 else 0


def rundown(c, s):
    """dB on the stroke of cycle c at sixteenth s in the last stretch of the first half (None: not played). The
    strokes of order 0 fall to FLOOR over the first half of the stretch and go; those of order 1 over the second."""
    if not ON['rundown'] or not HALF - SUPER <= s < HALF or order(c, s) == 2:
        return 0
    x = (s - (HALF - SUPER)) / SUPER * 2 - (order(c, s) == 1)
    return None if x >= 1 else round(FLOOR * max(x, 0), 1)


def windup(c, s):
    """The same backwards in the last stretch of the second half: dB on a small-cycle stroke that the big cycle
    does not already play (None: not played). Order 1 comes up over the first half of the stretch, order 0 over the second."""
    if not ON['windup'] or not TOTAL - SUPER <= s < TOTAL or s % c:
        return None
    x = (s - (TOTAL - SUPER)) / SUPER * 2 - (order(c, s) == 0)
    return None if x < 0 else round(FLOOR * (1 - min(x, 1)), 1)


def stretches():
    """(start, length, which step of four) in sixteenths, for every stretch between two meetings of all three: sixteen
    of 105 sixteenths in the first half (four to a page), four of 105 beats (a page each) in the second."""
    return ([(s, SUPER, s % PAGE // SUPER) for s in range(0, HALF, SUPER)] +
            [(s, PAGE, (s - HALF) // PAGE) for s in range(HALF, TOTAL, PAGE)])


def beats(s16):
    return ('%.4f' % (s16 / BEAT)).rstrip('0').rstrip('.') + 'b'


def walk(far):
    """A lane that is 0 where the three meet and `far` half way to the next meeting, straight lines between."""
    pts = []
    for s, n, _ in stretches():
        pts += [[beats(s), 0], [beats(s + n / 2), far]]
    return {'points': pts + [[beats(TOTAL), 0]], 'curve': 0}


def door():
    """The far room's fader: DOOR[k] through the k-th stretch since the page turned, stepping within a sixteenth."""
    pts = []
    for s, n, k in stretches():
        pts += [[beats(s), DOOR[k]], [beats(s + n - 1), DOOR[min(k + 1, len(DOOR) - 1) if ON['swing'] else k]]]
    return {'points': pts + [[beats(TOTAL), DOOR[-1]], [beats(TOTAL + BAR), DOOR[-1]]], 'curve': 0}

PATCHES = {
    'lc-kick': {'about': "Least Common: the four. The drum machine's bass drum resting on G, short enough to leave the sixteenth before the next beat empty.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'kick', 'decay': '240ms', 'click': 0.55, 'drive': 0.2, 'punch': 20}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '400ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.3}},
    'lc-three': {'about': 'Least Common: the click that counts three. Ten milliseconds of noise above 5 kHz: a tick with no note.',
                 'synth': {'layers': [{'type': 'noise', 'color': 'white'}], 'filters': ['hp cutoff=5000', 'peak cutoff=8500 q=2 gain=8dB'],
                           'amp': {'a': '0.1ms', 'd': '10ms', 's': 0, 'r': '8ms', 'curve': 3}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-five': {'about': 'Least Common: the click that counts five. A small wooden bar (1 : 4 : 10) struck hard and damped at once: a tock on G.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'bar', 'decay': '55ms', 'bright': 0.8, 'damp': 0.4, 'strike': 0.4}],
                          'amp': {'a': '0.2ms', 'd': '80ms', 's': 0, 'r': '30ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-seven': {'about': "Least Common: the click that counts seven. The drum machine's rim, tuned to G: two short pings and a click, a knock.",
                 'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'rim', 'decay': '45ms'}}],
                           'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.7}},
    'lc-ping': {'about': 'Least Common: what two clicks make when they meet. A vibraphone bar with no motor, half a second long.',
                'synth': {'layers': [{'type': 'modal', 'modes': 'vibes', 'decay': '650ms', 'bright': 0.55, 'strike': 0.3}],
                          'amp': {'a': '0.3ms', 'd': '900ms', 's': 0, 'r': '200ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
    'lc-chord': {'about': 'Least Common: what three clicks make when they meet. A short filtered chord for a delay to carry.',
                 'synth': {'layers': [{'wave': 'saw', 'detune': -7}, {'wave': 'saw', 'detune': 7}, {'wave': 'pulse', 'level': '-8dB'}],
                           'filters': [{'kind': 'lp', 'cutoff': {'value': 500, 'mod': [{'src': 'env.f', 'amount': 2.6}]}, 'q': 1.4}],
                           'env': {'f': {'a': '1ms', 'd': '140ms', 's': 0, 'r': '80ms'}},
                           'amp': {'a': '1ms', 'd': '220ms', 's': 0, 'r': '90ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.4}},
    'lc-tone': {'about': 'Least Common: the meetings one size up. A plain held tone, a sine and a little of its octave, that takes a beat to arrive.',
                'synth': {'layers': [{'wave': 'sine'}, {'wave': 'triangle', 'semi': 12, 'level': '-16dB'}],
                          'amp': {'a': '240ms', 'd': '0s', 's': 1, 'r': '900ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.2}},
    'lc-hat': {'about': "Least Common: the off beat. The drum machine's hat, closed.",
               'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'hat', 'decay': '45ms'}}],
                         'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '120ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.6}},
    'lc-clap': {'about': "Least Common: two and four. The drum machine's clap, short.",
                'synth': {'layers': [{'type': 'machine', 'machine': {'part': 'clap', 'decay': '140ms', 'bursts': 3}}],
                          'amp': {'a': '0.1ms', 'd': '0s', 's': 1, 'r': '300ms'}}, 'play': {'event_stable': True, 'vel_sens': 0.5}},
}


def euclid(k, n):
    """k strokes spread over n steps as evenly as they go, the first on the first step."""
    return [i * n // k for i in range(k)]


def touch(pos):
    """How hard a click lands: hardest where it catches the bass drum, lighter on the off beat, lightest between."""
    return .92 if pos % BEAT == 0 else .74 if pos % BEAT == 2 else .58


def build():
    T = {n: [] for n in ('kick', 'three', 'five', 'seven', 'ping', 'chord', 'tone', 'bass', 'hat', 'clap')}
    marks = []

    def add(tr, s16, len16, pitch, vel, **more):
        T[tr].append({'at': round(s16 / BEAT, 4), 'len': round(len16 / BEAT, 4), 'pitch': pitch, 'vel': round(vel, 3), **more})

    pitch = {'three': 'C6', 'five': 'G5', 'seven': 'G4'}
    mem = dict(pitch)
    roots = []                                                # the note of the last meeting of any two, at every sixteenth
    # ---- the first half: cycles of 3, 5 and 7 sixteenths. Who is in, by supercycle (the three meet at each one's head).
    supers = HALF // SUPER                                    # 16
    pages = HALF // PAGE                                      # 4
    per_page = PAGE // SUPER                                  # 4
    enters = {'three': 0, 'five': 1, 'seven': 2}              # one more click each time the three would have met
    last = supers - 1                                         # the last supercycle of the half: the four stops, to come back on the one
    for s in range(0, HALF):
        n = s // SUPER
        here = [c for c, v in zip(CYCLES, VOICES) if s % c == 0 and (n >= enters[v] or s == 0)]
        if ON['memory'] and len(here) >= 2:                   # a click keeps the note of the last meeting it was in
            for c, v in zip(CYCLES, VOICES):
                if c in here and v in MEMORY:
                    mem[v] = MEMORY[v][tuple(here)]
        loud = {c: rundown(c, s) for c in here}               # v3: 0 dB everywhere but in the last stretch
        for c, v in zip(CYCLES, VOICES):
            if c in here and loud[c] is not None:
                add(v, s, 1, mem[v], touch(s), **({'gain': f'{loud[c]}dB'} if loud[c] else {}))
        met = tuple(c for c in CYCLES if s % c == 0)
        roots.append(ROOT[met] if len(met) >= 2 else roots[-1])
        if len(here) == 2 and None not in loud.values():     # a meeting is as loud as the quieter of the two
            add('ping', s, 4, PING[tuple(here)], .8, **({'gain': f'{min(loud.values())}dB'} if min(loud.values()) else {}))
        if len(here) == 3:
            add('chord', s, 2, ','.join(CHORD), .85 if s % BEAT == 0 else .7)
        if s % BEAT == 0 and n != last and not broken(s):
            add('kick', s, 2, 'G1', .95 if s % BAR == 0 else .88)
    marks += [('first half: three, five and seven sixteenths', 0)] + [(f'page {p + 1} (the three meet on beat {p * PAGE // BEAT % 4 + 1})', p * PAGE) for p in range(1, pages)]
    marks += [('the four stops', last * SUPER)]
    # ---- the second half: one size up. Cycles of 3, 5 and 7 beats, each filled with the next one's number.
    fill = {c: euclid(CYCLES[(i + 1) % 3], c * BEAT) for i, c in enumerate(CYCLES)}
    assert [len(fill[c]) for c in CYCLES] == [5, 7, 3]
    held = []                                                  # (sixteenth, the cycles that begin together)
    for s in range(HALF, TOTAL):
        r = s - HALF
        heads = [c for c in CYCLES if r % (c * BEAT) == 0]
        small = tuple(c for c in CYCLES if r % c == 0)       # v3 LINE: the bass keeps the small cycles' meetings
        roots.append((ROOT[small] if len(small) >= 2 else roots[-1]) if ON['line'] else ROOT[tuple(heads)] if len(heads) >= 2 else roots[-1])
        if ON['memory'] and len(heads) >= 2:
            for c, v in zip(CYCLES, VOICES):
                if c in heads and v in MEMORY:
                    mem[v] = MEMORY[v][tuple(heads)]
        for c, v in zip(CYCLES, VOICES):
            filled = r % (c * BEAT) in fill[c]
            if ON['windup'] and s >= TOTAL - SUPER and r % (c * BEAT):       # v3: the fillings go, the small cycles come back
                going = (s - (TOTAL - SUPER)) / SUPER * 2
                both = [g for g in (round(FLOOR * going, 1) if filled and going < 1 else None, windup(c, s)) if g is not None]
                if both:
                    add(v, s, 1, mem[v], touch(s), **({'gain': f'{max(both)}dB'} if max(both) else {}))
            elif filled:
                add(v, s, 1, mem[v], touch(s) if r % (c * BEAT) else .95)
        if len(heads) >= 2:
            held.append((s, tuple(heads)))
        if s % BEAT == 0 and not broken(s):
            add('kick', s, 2, 'G1', .95 if s % BAR == 0 else .88)
    held.append((TOTAL, tuple(CYCLES)))
    for (s, heads), (nxt, _) in zip(held, held[1:]):
        if len(heads) == 3:
            add('chord', s, 2, ','.join(CHORD), .85)
            continue                                           # after a chord the tone rests until the next two meet
        add('tone', s, nxt - s - 2, TONE[heads], .7)
    # the same tune at both sizes: from the seventh page the pings come back over the held tones, at the small
    # cycles' own places (three, five and seven sixteenths counted from the top of the half, nobody playing them)
    for s in range(HALF + 2 * PAGE, TOTAL):
        small = tuple(c for c in CYCLES if (s - HALF) % c == 0)
        if len(small) == 2:
            add('ping', s, 4, PING[small], .62)
    # home: everything meets on the one, and that is the end
    add('chord', TOTAL, 8, ','.join(CHORD), .9)
    add('kick', TOTAL, 2, 'G1', .95)
    for v in VOICES:
        add(v, TOTAL, 1, MEMORY[v][ALL] if ON['memory'] and v in MEMORY else pitch[v], .95)
    marks += [('second half: three, five and seven beats', HALF)] + [(f'page {p + 5} (the three meet on beat {p * PAGE // BEAT % 4 + 1})', HALF + p * PAGE) for p in range(1, pages)]
    marks += [('only the drum is left of the four', HALF + last * SUPER), ('home', TOTAL)]
    if ON['break']:
        marks = sorted(marks + [('the four stops for the page turn', t - BREAK) for t in TURNS], key=lambda m: m[1])
    if ON['rest']:
        marks = sorted(marks + [('the four stops for the page turn', t - REST) for t in TURNS2], key=lambda m: m[1])
    # ---- the four's own parts: a bass that never plays with the drum, an off-beat hat, a clap on two and four.
    # Pages (from 0): the bass from page 1; the hat on pages 2, 3 and 6, 7; the clap on page 3 and pages 5, 6, 7.
    # In the last supercycle of the first half the four stops (the drum too) and comes back on the one; in the last
    # supercycle of the second half only the four is left of its parts (the drum), under the clicks, to the end.
    cell = ((2, 1.5, 'G2'), (7, 1, 'G2'), (10, 1, 'Bb2'), (14, 1.5, 'G2'))
    for s0 in range(0, TOTAL, BAR):
        page = s0 // PAGE
        if last * SUPER <= s0 < HALF or s0 >= HALF + last * SUPER:
            continue
        if page >= 1:
            for off, ln, p in cell:
                if not broken(s0 + off):
                    add('bass', s0 + off, ln, roots[s0 + off] if ON['roots'] else p, .85)
        if page in (2, 3, 6, 7):
            for off in (2, 6, 10, 14):
                if not broken(s0 + off):
                    add('hat', s0 + off, 1, 'A#4', .7)
        if page in (3, 5, 6, 7):
            for off in (4, 12):
                if not broken(s0 + off):
                    add('clap', s0 + off, 1, 'C4', .7)
    return T, marks


def song():
    T, marks = build()
    def track(name, patch, gain, pan=0, **more):
        return {'name': name, 'patch': patch, 'gain': gain, 'pan': pan, 'notes': sorted(T[name], key=lambda n: n['at']), **more}
    echo = lambda n, mix, fb: {'type': 'delay', 'time': f'{n}/16', 'mix': mix, 'feedback': fb, 'tone': 2600}
    under = {'type': 'pump', 'on': 'kick', 'depth': '-5dB', 'release': '170ms'}
    hold = lambda db: f'clip drive=0dB ceiling={db}dB'          # a click's level is its own, not the limiter's
    doc = {
        'about': "Chirpers, album eleven, track 2: Least Common, by chirper-one. Generated by compose/chirpers11/src/chirpers11-t2.py (its docstring is the rule). Three clicks on cycles of 3, 5 and 7 sixteenths against a bass drum on every fourth; a ping where two meet, a chord where three meet, a new page where three meet on the drum, and all of it on the one once in 105 bars. The second half is the first, one size up.",
        'meta': {'artist': 'chirpers', 'album': 'Escapement', 'title': 'Least Common', 'track': 2, 'year': 2026},
        'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{(TOTAL + BAR) // BEAT}b', 'tail': '3s', 'ceiling': '-1dB', 'true_peak': True, 'loudness': -13,
        'patches': PATCHES,
        'buses': {'room': {'fx': ['reverb kind=room decay=0.5s mix=1 predelay=8ms', 'hp cutoff=400']},
                  'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=25ms', 'hp cutoff=350', 'lp cutoff=6000']}},
        'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=28']}]},
        'tracks': [
            track('kick', 'lc-kick', '-6dB', fx=[{'type': 'eq', 'bands': ['peak cutoff=47 q=1.2 gain=-3dB', 'peak cutoff=130 q=0.9 gain=3dB']}]),
            track('bass', 'sub-sine', '-11dB', fx=[under]),
            track('three', 'lc-three', '-3dB', pan=-0.45, fx=[hold(-12)], sends={'room': '-14dB'}),
            track('five', 'lc-five', '0dB', pan=0.45, fx=[hold(-14)], sends={'room': '-12dB'}),
            track('seven', 'lc-seven', '-1dB', pan=0.0, fx=[hold(-14)], sends={'room': '-12dB'}),
            track('ping', 'lc-ping', '-10.5dB', pan=0.15, fx=[echo(3, 0.3, 0.45)], sends={'hall': '-10dB'}),
            track('chord', 'lc-chord', '-6dB', pan=-0.1, fx=[hold(-6), echo(3, 0.45, 0.6), under], sends={'hall': '-8dB'}),
            track('tone', 'lc-tone', '-28dB', pan=0.1, fx=[under], sends={'hall': '-6dB'}),
            track('hat', 'lc-hat', '6dB', pan=0.2, sends={'room': '-16dB'}),
            track('clap', 'lc-clap', '-6dB', pan=-0.05, sends={'room': '-10dB'}),
        ]}
    by_name = {t['name']: t for t in doc['tracks']}
    side = {'three': -1, 'five': 1, 'seven': 0}
    if ON['roots']:
        doc['patches'] = {**doc['patches'], 'lc-root': LC_ROOT}
        by_name['bass'].update(patch='lc-root', gain=f"{float(by_name['bass']['gain'][:-2]) + ROOTS_DB:g}dB")
    if ON['memory']:
        doc['patches'] = {**doc['patches'], 'lc-tock': TOCK}
        by_name['five'].update(patch='lc-tock', gain=f"{float(by_name['five']['gain'][:-2]) + TOCK_DB:g}dB")
    if ON['seven']:
        by_name['seven']['gain'] = f"{float(by_name['seven']['gain'][:-2]) + SEVEN_DB:g}dB"
    if ON['through'] and ON['door']:
        for name in ('ping', 'chord', 'tone'):
            by_name[name]['sends'] = {**by_name[name]['sends'], 'far': THROUGH}
        by_name['ping']['gain'] = f"{float(by_name['ping']['gain'][:-2]) + THROUGH_DRY:g}dB"
    for v in VOICES:
        t = by_name[v]
        if ON['place'] and side[v]:
            t['pan'] = {'value': 0, 'mod': [{'src': 'auto.place', 'amount': 1}]}
            t.setdefault('auto', {})['place'] = walk(side[v] * WIDE)
        if ON['near']:
            t['gain'] = {'value': f"{float(t['gain'][:-2]) + LIFT:g}dB", 'mod': [{'src': 'auto.near', 'amount': 1}]}
            t.setdefault('auto', {})['near'] = walk(-NEAR)
        if ON['door']:
            t['sends'] = {**t['sends'], 'far': FAR}
    if ON['door']:
        doc['buses'] = {**doc['buses'], 'far': {'fx': ['reverb kind=hall decay=2.6s mix=1 predelay=30ms', f"hp cutoff={WIDE_HP if ON['wide'] else 500}", 'lp cutoff=8000'],
                                                'gain': {'value': f"{WIDE_DB if ON['wide'] else 0}dB", 'mod': [{'src': 'auto.door', 'amount': 1}]}, 'auto': {'door': door()}}}
    return doc, marks


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
    ap.add_argument('--form', action='store_true', help='print the form and stop')
    for k in ON:
        ap.add_argument(f'--without-{k}', action='store_true', help=f'leave out {k} (the last eight off is v2, all fourteen v1)')
    a = ap.parse_args()
    for k in ON:
        ON[k] = not getattr(a, f'without_{k}')
    doc, marks = song()
    if a.form:
        sec = 60 / BPM / BEAT
        for name, s in marks:
            print(f'{s:5d}  bar {s // BAR + 1:3d} beat {s % BAR / BEAT + 1:4.2f}  {int(s * sec) // 60}:{s * sec % 60:05.2f}  {name}')
        for t in doc['tracks']:
            print(f"   {t['name']:6s} {len(t['notes']):5d} notes")
    else:
        a.out.write_text(dump(doc))
