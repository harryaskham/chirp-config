#!/usr/bin/env python3
"""Take Up the Slack: a hauling song (chirper-alpha, Common Time, track fifteen).

A crew hauls in common time: a call, an answer, and on the fourth downbeat
everybody pulls. The band's riff is not in common time. In the first verse it
is fifteen sixteenths long, so its head (the one open chord) falls later than
the crew's pull by three beats, then two, then one, and on the fourth pull it
lands with them: the slack is taken up, and the song falls into four for the
chorus. In the second verse the riff is seventeen long and the rope pays out
the other way. In the third the two guitars take one each: at the first pull
the right hand is a beat early and the left a beat late, and at the second
they meet. Times here are sixteenths; the output is in quarter-note beats.
"""
import json
import os
from collections import defaultdict
from pathlib import Path

BPM, GRID, BAR = 92, 4, 16
F1 = 29                       # the eight-string's low F
PITCH = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(os.environ.get('C10T15_OUT', Path(__file__).resolve().parents[3] / 'songs/chirpers10-t15.yaml'))
# section, bars of four
FORM = [('count', 1), ('first call', 4), ('late hand', 16), ('all together', 8), ('early hand', 17),
        ('all together again', 8), ('easy', 8), ('both hands', 8), ('home', 16), ('made fast', 4)]
# The riff: position, kind (o = the open chord, the head; n = a ringing single note; m = palm stroke),
# semitones over low F, length. Fifteen long; the seventeen adds the tritone at the end.
RIFF15 = [(0, 'o', 0, 2.7), (3, 'm', 0, .65), (4, 'm', 0, .65), (6, 'n', 3, 1.7), (8, 'm', 0, .65), (9, 'm', 0, .65),
          (11, 'n', 1, 1.7), (13, 'm', 0, .65), (14, 'm', 0, .65)]
RIFF17 = RIFF15 + [(15, 'n', 6, 1.7)]
# The chorus is in four: a chord on the pull, two palm strokes, a chord under 'way', two more.
RIFF16 = [(0, 'o', 0, 5.5), (6, 'm', 0, .65), (8, 'm', 0, .65), (10, 'o', 0, 3.5), (14, 'm', 0, .65), (15, 'm', 0, .65)]
CHORDS = [0, 0, 3, 1, 0, 0, 3, 7]          # F F Ab Gb | F F Ab C
# The voices' levels (the shantyman ; the crew), set on benches: see the round note.
SHANTY_GAIN = os.environ.get('C10T15_SHANTY', '-3dB')
CREW_GAIN = os.environ.get('C10T15_CREW', '-6dB')
# THE WORDS WERE CHOSEN BY A RECOGNISER (tools/wordread.py, small.en, each voice alone): it is the one ear this
# composer has. First draft on the library's old man (voice-old): 50% of the shantyman's words read, and the
# song's key word never: 'hand' came back as 'end', 'and' or 'N' on four voices (the engine's H before a short
# A does not carry: a bead, not a mix fault), while 'man' in the same line read 9 of 9 on three of them. So the
# sung word is 'man' and the hands are the guitarists'. 'The tide is high and the hour is soon' read as 'all
# that I desire' on every voice and was rewritten from words that had read. The rasp, jitter and breath of
# voice-old cost words ('we lean on the line and we hold her low': 5 of 10 on it, 10 of 10 on voice-hook), so
# the shantyman is the plain sung voice. 'Haul' with the dictionary's vowel (AO) read as 'home' or 'hole' every
# time; with AA the crew's shout reads 'haul'. In the chorus the crew's long 'haul' still reads 'home', so the
# shantyman sings the chorus with them: one clear voice in front of five.
# v2, palette (chirper-two): THE ROPE. The song is about a rope and nothing in the band was one. Now there is: a
# bass tagelharpa, the bowed horsehair lyre (two strings of twisted hair under a bow: no other song on the record
# has one), and it sounds only when the crew pulls. Its note is how much slack is left, a semitone to a beat:
#   the first call and the first verse (the late hand): D flat, D, E flat, E, and on the fourth pull, where the
#     riff's head lands with the crew, F. Each pull finds it where the last one left it and HAULS it up a semitone
#   the second verse (the early hand): A, A flat, G, G flat, each pull letting it DOWN a semitone ("and when I
#     call then we all come down"), and F on the chorus's downbeat, where the seventeen lands after "Hold fast"
#   the third verse (both hands): two ropes, the left a semitone slack and the right a semitone tight on either
#     side of the crew's own note at the first pull (E, F, G flat: "a man too soon and a man too late"); at the
#     second both come to F ("and the rope runs straight")
#   the close: both on F under "home", and they do not move: made fast
# F is the note the crew shouts "Haul!" on (F3), so the rope closes on the shout from below, then from above,
# then from both sides, and is in tune with the men exactly when the band is in time with them.
# Track gain ; how far left and right ; the slide's time ; the loudness target (the rope adds a little to the
# song; every bar without it keeps v1's mastering gain). Empty restores v1.
ROPE = os.environ.get('C10T15_ROPE', '-9.5dB;0.5;350ms;-9.947')
# v3, whole song (chirper-one): THE CREW SINGS IN THE BAND. Read against the eleven records' voices (tools/voxref.py,
# while they sing): theirs sit 9.2 dB under their mix, ours 2.6 under in a verse and 0.9 under in a chorus, where
# shantyman and crew together stood 5.7 dB OVER the whole band; and ours were far darker than theirs: by band, against
# the voice's own level, 19 dB more under 250 Hz, 7 more at 250-500, 11 less at 2-4 kHz and 16 less above. A voice
# with no top has to be loud to be heard, and a loud dark voice is the 9 dB at 250-500 Hz that chirper-two's read
# found. So the three voice tracks get one eq (a high-pass, a dip in the body, a shelf for the consonants) and
# then come down: a trim everywhere, and a further ride in the choruses, where five men and the shantyman hold long
# notes over the band's heaviest riff. No note changes.
# AND THE BAND CARRIES THE CHORUS. In v2 the chorus was 3.5 dB louder than the verse and all of it was voices: the
# band alone is half a dB QUIETER there (long chords, fewer strokes). With the voices in their place the chorus did
# not lift at all (benched: verse -20.4, chorus -20.5), so the band's faders go up in the choruses instead.
# the eq's bands, | between them ; the trim on all three, dB ; the voices' ride in the choruses, dB ; the band's
# lift in the choruses, dB ; the loudness target. "" = v2. It is on only while the three older switches are.
INBAND = os.environ.get('C10T15_INBAND', 'hp cutoff=190|peak cutoff=330 q=0.9 gain=-5dB|peak cutoff=2600 q=0.6 gain=7dB;-3.5;-2.5;2;-10' if ROPE and SHANTY_GAIN and CREW_GAIN else '')
# v4, whole song (chirper-three): THE CHORUS HAS A FLOOR. v3 found that the band alone is no louder in the chorus
# than in the verse (long chords, fewer strokes) and carried the chorus by lifting the guitar, bass and drum buses
# 2 dB through it; its note says the size should come from the arrangement. Three parts of one, in all three chorus
# passages (0:54.8, 2:00.0, 3:02.6), under the same voices, the same riff and the same chords:
#   THE BASS WALKS. It doubled the guitars (a long note, two palm strokes, a long note, two more). Now it heaves in
#     eighths on the chord's root, eight to the bar, and on the last eighth it steps towards the next chord: F to its
#     octave, F up through G flat to A flat, A flat up through B flat to C, and under 'home' down C, A flat, G flat
#     to the F the next line starts on. The guitars' chords ring over a floor that moves.
#   A CRASH ON EVERY 'HAUL'. The chorus pulls once a bar; a crash now strikes with the china on each pull.
#   THE CREW'S FEET COME BACK. The song opens on a stomp (floor tom and foot on one and three) and loses it when
#     the band comes in. In the chorus the floor tom stamps one and three again, under the foot that is there.
# WHAT IT DID NOT DO is make the band louder (see the round note: a tenth of a decibel), so v3's lift stays.
# NOT KEPT: the octave on the chorus's chords (field two): it added half a decibel at 250-500 Hz, where the song is
# already over the records, and nothing to the level.
# the bass in eighths (1) ; the octave on the chords (1 = on) ; the crash's velocity on the pulls that had only a
# china ("" = none) ; the stomp's velocity on one (three is 0.1 less; "" = none) ; the buses' lift in the
# choruses, dB (v3's) ; the loudness target. "" = v3.
BUILT = os.environ.get('C10T15_BUILT', '1;0;0.78;0.62;2;-9.937' if INBAND else '')
WALK = {(0, 0): {14: 12}, (0, 3): {14: 1}, (3, 7): {14: 5}, (7, 0): {12: 3, 14: 1}}     # eighth: semitones over low F
# one bow, the pitch sliding inside the note (mono, legato); no chance detuning from note to note and less than half
# of the library's unsteady bowing (12 cents either way there, 5 here): taut is in tune
HAWSER = ('tagelharpa-bass play.mono=true play.legato=true play.glide={} play.glide_smooth=true '
          'synth.pitch.mod.0.amount=0 synth.pitch.mod.1.amount=0.05')
SHANTY = 'voice-hook synth.layers.0.diction=3 synth.layers.0.effort_tilt=1 play.phrase_arc=0.5'
CREW = 'voice-choir synth.layers.0.tract=1.12 synth.layers.0.diction=3 synth.layers.0.effort_tilt=1 fx.0.mix=0.14'

PH = {'oh': 'OW1', 'the': 'DH AH0', 'line': 'L AY1 N', 'is': 'IH0 Z', 'long': 'L AO1 NG', 'and': 'AH0 N D',
      'load': 'L OW1 D', 'slow': 'S L OW1', 'a': 'AH0', 'hand': 'HH AE1 N D', 'too': 'T UW1', 'late': 'L EY1 T',
      'let': 'L EH1 T', 'go': 'G OW1', 'we': 'W IY1', 'lean': 'L IY1 N', 'on': 'AA1 N', 'hold': 'HH OW1 L D',
      'her': 'HH ER0', 'low': 'L OW1', 'when': 'W EH1 N', 'i': 'AY1', 'call': 'K AO1 L', 'then': 'DH EH1 N',
      'way': 'W EY1', 'tide': 'T AY1 D', 'high': 'HH AY1', 'hour': 'AW1 R', 'soon': 'S UW1 N', 'quick': 'K W IH1 K',
      'lone': 'L OW1 N', 'wait': 'W EY1 T', 'for': 'F ER0', 'word': 'W ER1 D', 'our': 'AW1 R', 'own': 'OW1 N',
      'all': 'AO1 L', 'come': 'K AH1 M', 'down': 'D AW1 N', 'meet': 'M IY1 T', 'in': 'IH0 N', 'mid': 'M IH1',
      'dle': 'D AH0 L', 'rope': 'R OW1 P', 'runs': 'R AH1 N Z', 'straight': 'S T R EY1 T', 'take': 'T EY1 K',
      'up': 'AH1 P', 'slack': 'S L AE1 K', 'haul': 'HH AA1 L', 'to': 'T AH0', 'ge': 'G EH1', 'ther': 'DH ER0',
      'home': 'HH OW1 M', 'now': 'N AW1', 'make': 'M EY1 K', 'fast': 'F AE1 S T', 'who': 'HH UW1', 'will': 'W IH1 L',
      'with': 'W IH1 DH', 'me': 'M IY1', 'man': 'M AE1 N', 'comes': 'K AH1 M Z', 'ea': 'IY1', 'sy': 'Z IY0', 'ride': 'R AY1 D', 'oo': 'UW1'}
# A call is two bars and a pickup: syllable, start, length, pitch. Stresses fall on 0, 4, 12 and the next downbeat.
T = [(-4, 2), (-2, 2), (0, 3), (3, 1), (4, 4), (8, 2), (10, 2), (12, 3), (15, 1), (16, 8)]
T3 = [(-2, 2), (0, 2), (2, 1), (3, 1), (4, 4), (8, 2), (10, 2), (12, 3), (15, 1), (16, 8)]
T4 = [(-2, 2), (0, 3), (3, 1), (4, 4), (8, 2), (10, 2), (12, 3), (15, 1), (16, 8)]
M1 = 'C3 Eb3 F3 F3 Ab3 F3 Eb3 F3 Eb3 C3'          # falls to the fifth below: a question
M2 = 'C3 Eb3 F3 F3 Ab3 F3 Eb3 Eb3 Eb3 F3'         # comes home
M3 = 'F3 Ab3 Ab3 Ab3 C4 Ab3 F3 Ab3 F3 Eb3'        # leans up
M4 = 'F3 Ab3 Ab3 C4 Ab3 F3 Ab3 F3 F3'             # and calls the pull


def line(words, rhythm, tune):
    words, tune = words.split(), tune.split()
    assert len(words) == len(rhythm) == len(tune), (words, len(rhythm), len(tune))
    return [(w, t, d, p) for w, (t, d), p in zip(words, rhythm, tune)]


CALLS = {
    'first call': [line('oh who will come and haul with me', [(-2, 2), (0, 3), (3, 1), (4, 4), (8, 4), (12, 3), (15, 1), (16, 8)],
                        'C3 F3 F3 Ab3 F3 Eb3 Eb3 C3')],
    'late hand': [line('oh the line is long and the load is slow', T, M1),
                  line('and a man too late is a man let go', T, M2),
                  line('we lean on the line and we hold her low', T3, M3),
                  line('and when i call then a way we go', T4, M4)],
    'early hand': [line('oh the wait is long and the word comes soon', T, M1),
                   line('and a man too quick is a man a lone', T, M2),
                   line('we wait for the call and we hold our own', T3, M3),
                   line('and when i call then we all come down', T4, M4)],
    'both hands': [line('a man too soon and a man too late', T4, 'Eb3 F3 F3 Ab3 F3 Eb3 F3 Eb3 C3'),
                   line('we meet in the mid dle and the rope runs straight',
                        [(-2, 2), (0, 2), (2, 1), (3, 1), (4, 2), (6, 2), (8, 2), (10, 2), (12, 3), (15, 1), (16, 8)],
                        'F3 Ab3 Ab3 Ab3 C4 C4 Ab3 F3 Ab3 F3 F3')],
}
# The answer fills the third bar; the pull is the fourth bar's downbeat.
SLACK = line('take up the slack haul', [(32, 4), (36, 2), (38, 2), (40, 6), (48, 5)], 'Ab3 F3 Eb3 F3 F3')
ALL = line('all to ge ther haul', [(32, 4), (36, 2), (38, 2), (40, 6), (48, 5)], 'Ab3 Ab3 C4 Ab3 C4')
CHORUS = [line('haul a way', [(0, 6), (8, 2), (10, 6)], 'C4 Ab3 F3'),
          line('haul a way home', [(0, 6), (8, 2), (10, 2), (12, 4)], 'C4 Ab3 C4 F3'),
          line('haul a way', [(0, 6), (8, 2), (10, 6)], 'Eb4 C4 Ab3'),
          line('all to ge ther now', [(0, 4), (4, 2), (6, 2), (8, 4), (12, 4)], 'Gb3 Gb3 Ab3 Gb3 F3'),
          line('haul a way', [(0, 6), (8, 2), (10, 6)], 'C4 Ab3 F3'),
          line('haul a way home', [(0, 6), (8, 2), (10, 2), (12, 4)], 'C4 Ab3 C4 F3'),
          line('haul a way', [(0, 6), (8, 2), (10, 6)], 'Eb4 C4 Ab3'),
          line('haul her home', [(0, 4), (4, 4), (8, 8)], 'C4 Eb4 F4')]


def name(m):
    return PITCH[m % 12] + str(m // 12 - 1)


def make():
    ev = defaultdict(list)
    marks = {}

    def put(tr, t, dur, p, v, mute=False, **more):
        e = {'at': round(t / GRID, 5), 'len': round(dur / GRID, 5), 'pitch': name(p) if isinstance(p, int) else p, 'vel': round(v, 3)}
        if mute:
            e['expr'] = {'pm': 1}
        e.update(more)
        ev[tr].append(e)

    def kit(t, piece, v):
        tr = {'k': 'kick', 's': 'snare', 'h': 'hat', 'hp': 'hat', 'x': 'cym', 'c': 'cym', 'rde': 'cym'}.get(piece, 'toms')
        put(tr, t, 3.8 if tr == 'cym' else 1.15, piece, v)

    def sing(tr, t0, syllables, v=.8, loud=()):
        # Notes touch inside a phrase (one breath); a gap of more than a sixteenth is a new phrase.
        for j, (w, t, d, p) in enumerate(syllables):
            nxt = syllables[j + 1][1] if j + 1 < len(syllables) else None
            if nxt is not None and nxt - (t + d) <= 1:
                d = nxt - t
            put(tr, t0 + t, d - (0 if nxt is not None and nxt - t == d else .4), p, .98 if w in loud else v, ph=PH[w])

    def stroke(trs, t, kind, semi, dur, root=F1, bass=True, kick=True, whole=False):
        p = root + semi
        for tr in trs:
            put(tr, t, dur, name(p) + ',' + name(p + 7) + (',' + name(p + 12) if whole else '') if kind == 'o' else p,
                .96 if kind == 'o' else .94 if kind == 'n' else .86, kind == 'm')
        if bass:
            put('bass', t, dur, p, .92 if kind != 'm' else .86, kind == 'm')
        if kick:
            kit(t, 'k', .98 if kind != 'm' else .82)

    def cycle(trs, riff, length, a, b, head, **kw):
        # every stroke of the riff between a and b, the cycle placed so that a head falls on `head`
        k0 = -((head - a) // length) - 1
        for k in range(k0, (b - head) // length + 2):
            for pos, kind, semi, dur in riff:
                t = head + k * length + pos
                if a <= t < b:
                    stroke(trs, t, kind, semi, min(dur, b - t - .1), **kw)

    def haul(tr, t, slack, was=None, dur=9, v=.9):
        """The rope at a pull: found where the last pull left it (`was`), then hauled to `slack` semitones from the crew's F."""
        if not ROPE:
            return
        if was is not None:
            put(tr, t, 2, F1 + 24 + was, v)
            put(tr, t + 1.5, dur - 1.5, F1 + 24 + slack, v)
        else:
            put(tr, t, dur, F1 + 24 + slack, v)

    def stomp(t, v=.7):
        kit(t, 'ft', v)
        kit(t, 'k', v)

    def couplets(sec, a, n, answers, shout=True):
        for i in range(n):
            c = a + i * 4 * BAR
            sing('shanty', c, CALLS[sec][i])
            sing('crew', c, answers[i], .86, loud=('haul',))
            if shout:
                put('shanty', c + 48, 4.5, F1 + 24, .98, ph=PH['haul'])   # he pulls with them
            kit(c + 48, 'ft', .92)
            kit(c + 48, 'x', .9)

    def chorus(a, bars, wide, last_long=False, high=False, pickup=False):
        gtrs = ('gl', 'gr', 'wl', 'wr') if wide else ('gl', 'gr')
        for b in range(bars):
            t0 = a + b * BAR
            root = F1 + CHORDS[b % 8]
            final = b % 8 == 7
            built = BUILT.split(';') if BUILT else None
            ends = last_long and b == bars - 1                        # the song's last chorus bar: one long chord, as it was
            walks = bool(built and built[0] == '1') and not ends
            for pos, kind, semi, dur in RIFF16:
                if final and pos:
                    continue          # the last bar is one held chord under 'home'
                stroke(gtrs, t0 + pos, kind, semi, (15.5 if last_long and b == bars - 1 else 11.5) if final else dur, root,
                       bass=not walks, whole=bool(built and built[1] == '1'))
            if walks:                 # v4: the bass in eighths on the root, stepping to the next chord on the last
                step = WALK.get((CHORDS[b % 8], CHORDS[(b + 1) % 8]), {})
                for q in range(0, BAR, 2):
                    put('bass', t0 + q, 1.8, F1 + step[q] if q in step else root, .92 if q % 4 == 0 else .84)
            words = CHORUS[b % 8]
            sing('crew', t0, words, .9, loud=('haul',))
            mine = words
            if final and pickup:
                # he lets the last word go early: his next call starts before the bar is out
                mine = words[:-1] + [(words[-1][0], words[-1][1], 3.5, words[-1][3])]
            sing('shanty', t0, mine, .88, loud=('haul',))        # he sings the chorus with them
            if high:
                # a second gang a fourth over the pulls only (F over C, A flat over E flat: the song's own notes)
                w, t, d, p = words[0]
                if w == 'haul':
                    put('crew-high', t0 + t, d - .4, {'C4': 'F4', 'Eb4': 'Ab4'}[p], .9, ph=PH[w])
            kit(t0, 'c' if b % 4 == 0 else 'x', .9 if b % 4 == 0 else .74)
            if built and built[2] and b % 4 and words[0][0] == 'haul':
                kit(t0, 'c', float(built[2]))                         # v4: a crash on every pull, over the china that was there
            if built and built[3] and not ends:
                kit(t0, 'ft', float(built[3])), kit(t0 + 8, 'ft', float(built[3]) - .1)     # v4: the crew's feet
            for q in (4, 8, 12):
                if not (final and q == 12):
                    kit(t0 + q, 'x', .6)
            if final:
                kit(t0 + 4, 's', .94)
                for t, p in ((12, 't1'), (13, 't2'), (14, 'ft'), (15, 'ft')):
                    if not (last_long and b == bars - 1):
                        kit(t0 + t, p, .82)
            else:
                kit(t0 + 4, 's', .94)
                kit(t0 + 12, 's', .94)

    def beat(a, bars, bronze, back=(8,), skip_last_beat=True):
        for b in range(bars):
            t0 = a + b * BAR
            last = b == bars - 1
            step = 2 if bronze == 'h' else 4
            for q in range(0, BAR, step):
                if last and skip_last_beat and q >= 12:
                    continue
                kit(t0 + q, bronze, (.65 if q % 4 == 0 else .48) if bronze == 'h' else (.72 if q == 0 else .58))
            for q in back:
                if not (last and skip_last_beat and q >= 12):
                    kit(t0 + q, 's', .94)

    start = 0
    for sec, bars in FORM:
        marks[sec] = start
        a, b = start, start + bars * BAR
        if sec == 'count':
            stomp(a), stomp(a + 8)
        elif sec == 'first call':
            for k in range(bars):
                stomp(a + k * BAR, .72), stomp(a + k * BAR + 8, .62)
            couplets(sec, a, 1, [SLACK])
            haul('rope-l', a + 48, -4, -5)
        elif sec == 'late hand':
            # 15 against 16: the head is 12, 8, 4 and 0 sixteenths after the four pulls
            cycle(('gl', 'gr'), RIFF15, 15, a, b, a)
            couplets(sec, a, 4, [SLACK, SLACK, SLACK, ALL])
            for i in range(4):
                haul('rope-l', a + i * 4 * BAR + 48, i - 3, i - 4)
            beat(a, bars, 'h')
            for t, p in ((12, 't1'), (13, 't1'), (14, 't2'), (15, 'ft')):
                kit(b - BAR + t, p, .82)
        elif sec == 'early hand':
            # 17 against 16: 3, 7, 11 and 15 after; one more bar and it lands on the chorus
            cycle(('gl', 'gr'), RIFF17, 17, a, b, a)
            couplets(sec, a, 4, [SLACK, SLACK, SLACK, SLACK])
            for i in range(4):
                haul('rope-r', a + i * 4 * BAR + 48, 4 - i, 5 - i)
            haul('rope-r', b, 0, 1)                    # the seventeen lands on the chorus
            beat(a, bars - 1, 'x', skip_last_beat=False)
            hold = b - BAR
            sing('shanty', hold, line('hold fast', [(0, 6), (8, 6)], 'Ab3 C4'), .95)
            kit(hold, 'x', .8)
            for t, p in ((8, 's'), (9, 's'), (10, 't1'), (11, 't1'), (12, 't2'), (13, 't2'), (14, 'ft'), (15, 'ft')):
                kit(hold + t, p, .7 + .03 * (t - 8))
        elif sec in ('all together', 'all together again'):
            chorus(a, bars, wide=sec != 'all together', pickup=sec == 'all together')
        elif sec == 'home':
            chorus(a, bars, wide=True, last_long=True, high=True)
        elif sec == 'easy':
            land = marks_next['both hands'] + 7 * BAR
            for tr, riff, length in (('clean-l', RIFF15, 15), ('clean-r', RIFF17, 17)):
                k = -((land - a) // length) - 1
                while land + k * length < b:
                    for pos, kind, semi, dur in riff:
                        t = land + k * length + pos
                        if kind != 'm' and a <= t < b:
                            put(tr, t, 3.4, F1 + 12 + semi, .7)
                    k += 1
            for k, semi in enumerate((0, 0, 1, 1, 0, 0, 3, 1)):
                put('bass', a + k * BAR, 15, F1 + semi, .7)
                kit(a + k * BAR, 'ft', .6)
                for q in (0, 4, 8, 12):
                    kit(a + k * BAR + q, 'hp', .42)
            sing('shanty', a, line('ea sy', [(0, 4), (4, 10)], 'F3 Eb3'), .55)
            sing('shanty', a + BAR, line('ea sy', [(0, 4), (4, 10)], 'F3 C3'), .55)
            sing('shanty', a + 2 * BAR, line('let her ride', [(0, 4), (4, 4), (8, 16)], 'Eb3 F3 Ab3'), .6)
            sing('shanty', a + 4 * BAR, line('ea sy', [(0, 4), (4, 10)], 'F3 Eb3'), .55)
            sing('shanty', a + 5 * BAR, line('ea sy', [(0, 4), (4, 10)], 'F3 C3'), .55)
            sing('shanty', a + 6 * BAR, line('with the tide', [(0, 4), (4, 4), (8, 16)], 'Eb3 F3 F3'), .6)
            for k, p in enumerate(('F3', 'Gb3', 'F3', 'Eb3')):
                put('crew', a + 2 * k * BAR, 2 * BAR - 2, p, .42, ph=PH['oo'])
        elif sec == 'both hands':
            land = a + 7 * BAR
            cycle(('gl',), RIFF15, 15, a, land, land)                      # the late hand, with the bass
            cycle(('gr',), RIFF17, 17, a, land, land, bass=False, kick=False)   # the early hand
            for k in range(-8, 1):                                          # the foot marks its heads too
                if a <= land + 17 * k < land:
                    kit(land + 17 * k, 'k', .98)
            stroke(('gl', 'gr', 'wl', 'wr'), land, 'o', 0, 11.5)
            kit(land, 'c', .92)
            couplets(sec, a, 2, [SLACK, ALL])
            for i in range(2):
                haul('rope-l', a + i * 4 * BAR + 48, i - 1, i - 2, v=.75)
                haul('rope-r', a + i * 4 * BAR + 48, 1 - i, 2 - i, v=.75)
            beat(a, bars, 'x', back=(4, 12))
            for t, p in ((12, 't1'), (13, 't2'), (14, 'ft'), (15, 'ft')):
                kit(b - BAR + t, p, .84)
        elif sec == 'made fast':
            for k in range(2):
                stomp(a + k * BAR, .72), stomp(a + k * BAR + 8, .62)
            sing('crew', a, line('take up the slack', [(0, 4), (4, 2), (6, 2), (8, 8)], 'Ab3 F3 Eb3 F3'), .8)
            sing('shanty', a, line('and make her fast', [(18, 2), (20, 4), (24, 2), (26, 5.5)], 'Eb3 F3 Eb3 C3'), .8)
            stroke(('gl', 'gr', 'wl', 'wr'), a + 2 * BAR, 'o', 0, 22)
            kit(a + 2 * BAR, 'c', .92), kit(a + 2 * BAR, 'ft', .9)
            put('crew', a + 2 * BAR, 14, 'F3', .9, ph=PH['home'])
            put('shanty', a + 2 * BAR, 14, 'F3', .9, ph=PH['home'])
            haul('rope-l', a + 2 * BAR, 0, dur=14, v=.8)
            haul('rope-r', a + 2 * BAR, 0, dur=14, v=.8)
        start = b
    return ev, marks, start


# 'easy' needs to know where 'both hands' begins before the loop reaches it
marks_next = {}
_t = 0
for _s, _n in FORM:
    marks_next[_s] = _t
    _t += _n * BAR


def in_the_choruses(db):
    """A fader ride: `db` through each chorus, moving over the half beat before it and the last half beat of it."""
    points, beat = [['0b', 0]], 0
    for name_, bars in FORM:
        if name_ in ('all together', 'all together again', 'home'):
            points += [[f'{beat - 0.5:g}b', 0], [f'{beat:g}b', db], [f'{beat + 4 * bars - 0.5:g}b', db], [f'{beat + 4 * bars:g}b', 0]]
        beat += 4 * bars
    return points


def voices(tr):
    """The shantyman and the two crews: as v2, or (v3) with one eq, a trim, and a ride down in the choruses."""
    out = [tr('shanty', SHANTY, SHANTY_GAIN, -.08, sends={'hall': '-16dB'}), tr('crew', CREW, CREW_GAIN, .1),
           tr('crew-high', CREW, CREW_GAIN, -.2)]
    if not INBAND:
        return out
    bands, trim, ride = INBAND.split(';')[:3]
    eq = [{'type': 'eq', 'bands': bands.split('|')}]
    points = in_the_choruses(float(ride))
    for t in out:
        t['fx'] = eq
        t['gain'] = {'value': f"{float(t['gain'][:-2]) + float(trim):g}dB", 'mod': [{'src': 'auto.ride', 'amount': 1}]}
        t['auto'] = {'ride': {'points': points, 'curve': 0}}
    return out


def tracks_of(ev):
    def tr(name_, patch, gain, pan=0, out=None, fx=None, sends=None):
        d = {'name': name_, 'patch': patch, 'gain': gain, 'pan': pan, 'notes': sorted(ev[name_], key=lambda n: n['at'])}
        if out: d['out'] = out
        if sends: d['sends'] = sends
        if fx: d['fx'] = fx
        return d
    lift = [{'type': 'eq', 'bands': ['peak cutoff=700 q=0.9 gain=2.5dB']}]
    dip = [{'type': 'eq', 'bands': ['peak cutoff=380 q=1 gain=-3dB']}]
    air = [{'type': 'eq', 'bands': ['highshelf cutoff=9000 gain=-2dB']}]
    hair = [{'type': 'eq', 'bands': ['peak cutoff=180 q=0.8 gain=-8dB']}]
    return [
        tr('gl', 'ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone=92', '0.7dB', -1, 'gtrs', lift),
        tr('gr', 'ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone=93', '0.7dB', 1, 'gtrs', lift),
        tr('wl', 'ct-wall-stop-l', '-3.5dB', -.75, 'gtrs', dip), tr('wr', 'ct-wall-stop-r', '-3.5dB', .75, 'gtrs', dip),
        tr('clean-l', 'ct-clean', '-6dB', -.6, sends={'hall': '-12dB'}), tr('clean-r', 'ct-clean', '-6dB', .6, sends={'hall': '-12dB'}),
        tr('bass', 'ct-bass', '0.5dB', 0, 'low'),
        tr('kick', 'ct-kit', '2dB', 0, 'drums', [{'type': 'eq', 'bands': ['peak cutoff=4500 q=0.8 gain=10dB']}]),
        tr('snare', 'ct-kit', '3.5dB', 0, 'drums', [{'type': 'eq', 'bands': ['highshelf cutoff=7000 gain=-3dB']}], {'oh': '-1.5dB', 'snr': '-10dB'}),
        tr('toms', 'ct-kit', '4dB', 0, 'drums', sends={'oh': '-1.5dB'}),
        tr('cym', 'ct-kit', '-4.5dB', .3, 'drums', air, {'oh': '4.5dB'}),
        tr('hat', 'ct-kit', '14dB', -.4, 'drums', air, {'oh': '4.5dB'}),
        *voices(tr),
        # (the big lyre played this high is mostly fundamental: at a pull it stood over the whole band at 120-250 Hz
        # and 8 to 14 dB under it from 500 Hz up. Eight dB off its body, so that what is heard is the hair)
        *([tr('rope-l', HAWSER.format(ROPE.split(';')[2]), ROPE.split(';')[0], -float(ROPE.split(';')[1]), fx=hair),
           tr('rope-r', HAWSER.format(ROPE.split(';')[2]), ROPE.split(';')[0], float(ROPE.split(';')[1]), fx=hair)] if ROPE else []),
    ]


def build():
    ev, marks, end = make()
    low = [{'type': 'eq', 'bands': ['peak cutoff=44 q=1.5 gain=-7dB', 'peak cutoff=90 q=1 gain=7.5dB', 'peak cutoff=350 q=1 gain=-8dB', 'peak cutoff=1500 q=1 gain=4dB']},
           {'type': 'compressor', 'threshold': '-26dB', 'ratio': 8, 'attack': '12ms', 'release': '120ms', 'makeup': '2.5dB'},
           {'type': 'eq', 'bands': ['peak cutoff=170 q=1.2 gain=-3dB']}]
    buses = {
        'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=30ms low_cut=150']},
        'drums': {'fx': ['reverb kind=room decay=0.7s mix=0.1 predelay=8ms',
                         {'type': 'glue', 'threshold': '-24dB', 'ratio': 2.5, 'attack': '20ms', 'release': '140ms', 'knee': 6.0},
                         'clip drive=0dB ceiling=-13dB',
                         {'type': 'eq', 'bands': ['peak cutoff=400 q=0.8 gain=-6dB', 'peak cutoff=5500 q=0.9 gain=1dB', 'highshelf cutoff=9000 gain=-2dB', 'lp cutoff=14250 q=0.8']}]},
        'oh': {'fx': ['reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6', {'type': 'eq', 'bands': ['lp cutoff=14250 q=0.8']}]},
        'snr': {'fx': [{'type': 'eq', 'bands': ['peak cutoff=300 q=0.7 gain=-12dB']}]},
        'gtrs': {'fx': [{'type': 'eq', 'bands': ['peak cutoff=330 q=1.2 gain=-2dB']}, 'reverb kind=room decay=0.35s mix=0.06 predelay=6ms']},
        'low': {'fx': low},
    }
    lift = float(BUILT.split(';')[4]) if BUILT else float(INBAND.split(';')[3]) if INBAND else 0
    if lift:
        for name_ in ('gtrs', 'low', 'drums', 'oh', 'snr'):
            buses[name_]['fx'] = buses[name_]['fx'] + [{'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.lift', 'amount': 1}]}}]
            buses[name_]['auto'] = {'lift': {'points': in_the_choruses(lift), 'curve': 0}}
    doc = {'about': 'Take Up the Slack — chirpers, Common Time, track fifteen. A hauling song: the crew pulls in four, the riff is fifteen long, then seventeen, and each verse the slack between them is taken up.',
           'tempo': BPM, 'seed': 1, 'length': f'{end // GRID}b', 'tail': '3s', 'ceiling': '-1dB', 'loudness': float(BUILT.split(';')[5]) if BUILT else float(INBAND.split(';')[4]) if INBAND else float(ROPE.split(';')[3]) if ROPE else -10, 'event_stable': True,
           'buses': buses, 'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=24']}, {'type': 'gain', 'gain': '2.7dB'}]},
           'tracks': tracks_of(ev)}
    return doc, marks


def dump(d):
    return '\n'.join('tracks:\n' + '\n'.join('  - ' + json.dumps(t) for t in v) if k == 'tracks' else k + ': ' + json.dumps(v) for k, v in d.items()) + '\n'


if __name__ == '__main__':
    doc, marks = build()
    if os.environ.get('C10T15_SHOW'):
        for sec, bars in FORM:
            t = marks[sec]
            print(f'{sec:20s} bar {t // BAR + 1:3d}  {t / GRID * 60 / BPM:7.2f} s  {bars} bars')
    else:
        OUT.write_text(dump(doc))
