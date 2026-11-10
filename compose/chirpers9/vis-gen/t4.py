#!/usr/bin/env python3
"""t4 rebuilt on the song: the committed programme's sets (the beach at dusk; night and the lanterns), every signal rebound."""
import subprocess, re
s = subprocess.run(['git', '-C', '/home/harry/.config/chirp', 'show', '218a7179:vis/chirpers9-t4.yaml'], capture_output=True, text=True).stdout
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)

head = '''# chirpers9 t4 "The Warm Third": relief; warm, open, melodic; the voice at its most human.
# Co-built with the song (tools/songmap.py chirpers9-t4).
#
# What the song does, and so what the picture does:
#   - FOUR LIGHTS (E4, the element this track brings): four chords, heard alone at 8bar and
#     again at the end (121bar). Four lanterns stand in the sand round the fire; each chord
#     lights the next one in turn.
#   - THE VOICE: one of the friends is the singer. She sings when the voice sings: her mouth
#     opens on each note and her arms rise with the line. A second friend moves when the duet
#     voice answers. The shot cuts to her when she sings: from behind, against the sea.
#   - THE BAND: the friends sway, and dance as hard as the drums play (they come in at 40bar);
#     the fire burns higher with them; the sea swells with the bass; the gulls wheel once in
#     six bars.
#   - I (0bar) dusk on the beach, the sun going down through the first half (on bars).
#   - II (64bar) night. From 80bar (the singing bowl; the drums fall away and the hall opens)
#     every note she sings lets a lantern go: it rises from her and drifts out over the sea,
#     mirrored in the water. The duet's notes let go another colour. Each stroke of the bowl
#     (80, 100, 120bar) sends a ring across the water and swells every lantern. The camera
#     rises with them into the stars.
# Shots cut on bar lines.
# Reads tracks: lights voice duet kick snare-l hat-l ride-l kick2 snare2 bass sub e2 bowl.
'''
i = s.index('scenes:')
s = head + s[i:]

# ---- I: dusk ----
rep('''    look:
      background: "#000000"
      camera: {x: "(1.6 - 0.6*smooth(0, 150, time.t))*sin(time.t*0.008 + 0.15)", y: "0.35 - 0.15*smooth(0, 150, time.t)", z: "0 - (2.6 - 1.1*smooth(0, 150, time.t))*cos(time.t*0.008 + 0.15)", look_at: [0, -0.1, 0.6]}''',
'''    look:
      background: "#000000"
      env:
        chord: {when: "3*track.lights.hit", decay: 2.5}
      vars:
        drive: {follow: "max(max(track.kick.level, track.snare-l.level), max(track.hat-l.level, track.ride-l.level))", attack: 60ms, release: 900ms}
        low: {follow: "max(track.bass.level, track.sub.level)", attack: 200ms, release: 1200ms}
        sing: {follow: "track.voice.level", attack: 120ms, release: 900ms}
        mouth: {follow: "track.voice.gate", attack: 40ms, release: 140ms}
        close: {keys: [[0bar, 0], [64bar, 1]], ease: smooth}
        dusk: {keys: [[0bar, 0], [64bar, 1]], ease: linear}
        turn: {integrate: "0.004 + 0.006*var.drive", wrap: 1}
        wheel: {value: "time.bar/6"}
      camera:
        # 0 wide, closing in on the fire; 1 low and close, the fire against the sea; 2 behind
        # the singer, the sun and the sea beyond her; 3 the four lights. The sea is always
        # behind the fire (the beach is a strip: its ends and its back are never shown).
        - {x: "(1.6 - 0.6*var.close)*sin(0.1*sin(var.turn))", y: "0.35 - 0.15*var.close", z: "0 - (2.6 - 1.1*var.close)*cos(0.1*sin(var.turn))", look_at: [0, -0.1, 0.6]}
        - {x: 1.0, y: -0.4, z: -1.2, look_at: [-0.1, -0.2, 0.6]}
        - {x: -0.65, y: -0.06, z: -1.3, look_at: [0.1, 0.05, 1.5]}
        - {x: "1.9*sin(0.08*sin(var.turn + 0.4))", y: -0.3, z: "0.3 - 1.9*cos(0.08*sin(var.turn + 0.4))", look_at: [0, -0.35, 0.3]}
      shot: {keys: [[0bar, 0], [8bar, 3], [16bar, 0], [24bar, 1], [32bar, 2], [37bar, 0], [45bar, 2], [48bar, 1], [52bar, 2], [56bar, 0], [60bar, 3]], ease: step}''')
rep('sun_height: "0.035 - time.t*0.00025"', 'sun_height: "0.035 - 0.045*var.dusk"')
rep('''params: {far: 1, swell: 0.6, light: 0.25}}''', '''params: {far: 1, swell: "0.3 + 0.6*var.low", light: 0.25}}''')
rep('''- {type: group, use: kit-fire, y: -0.6, z: 0.3, params: {size: 0.7, heat: 0.65}}''',
    '''- {type: group, use: kit-fire, y: -0.6, z: 0.3, params: {size: 0.7, heat: "0.5 + 0.3*var.drive + 0.25*env.chord"}}
        # The four lights: lanterns in the sand, each chord lighting the next in turn.
        - {type: mesh, shape: sphere, detail: 12, count: 4, spawn: env.chord, x: "1.0*sin(inst.i/4 + 0.225)", z: "0.3 + 1.0*cos(inst.i/4 + 0.225)", y: -0.52, scale: 0.045, sy: 1.3, color: "#e89848", light: 0.2, ambient: 0.05, rim: 0, emit: "0.55 + 3*exp(0 - inst.age/2.5)"}
        - {type: light, count: 4, spawn: env.chord, x: "1.0*sin(inst.i/4 + 0.225)", z: "0.3 + 1.0*cos(inst.i/4 + 0.225)", y: -0.4, color: "#ffd090", power: "2.2*exp(0 - inst.age/2.5)", reach: 1.4}''')
rep('''phase: "inst.i*1.3", energy: "0.4 + 0.4*audio.level", color: "#4a3a38"''',
    '''phase: "inst.i*1.3", energy: "0.35 + 0.8*var.drive + 0.7*track.duet.level*step(inst.i, 0.5)", color: "#4a3a38"''')
rep('''face: [0, 0, 6], energy: "0.5 + 0.5*audio.level", pose: {arm_l: "0 - 0.12*smooth(0.1, 0.6, audio.level)", arm_r: "0 - 0.12*smooth(0.1, 0.6, audio.level)", head: -0.02}, color: "#4a3a38"''',
    '''face: [0, 0, 6], energy: "0.4 + 0.5*var.drive", mouth: "0.85*var.mouth", pose: {arm_l: "0 - 0.14*var.sing", arm_r: "0 - 0.14*var.sing", head: "-0.02 - 0.02*var.sing"}, color: "#4a3a38"''')
# The gulls: once round in six bars, beating with the high ostinato.
s = s.replace('time.t*0.05 + 0.02 + inst.i*0.25', 'var.wheel + 0.02 + inst.i*0.25').replace('time.t*0.05 + inst.i*0.25', 'var.wheel + inst.i*0.25')
rep('scale: 0.22, phase: "inst.i*0.37",', 'scale: 0.22, phase: "inst.i*0.37", energy: "0.7 + 0.5*track.e2.hit",')

# ---- II: night ----
rep('''  - at: 150
    transition: dissolve
    xfade: 4
    look:
      background: "#000000"
      env:
        let: {on: bar, decay: 1}
      camera: {x: "0.6*sin(time.t*0.01)", y: "0.2 + 1.2*smooth(150, 300, time.t)", z: -2.8, look_at: [0, "0.4 + 1.6*smooth(150, 300, time.t)", 4]}''',
'''  - at: 64bar
    transition: dissolve
    xfade: 4
    look:
      background: "#000000"
      env:
        chord: {when: "3*track.lights.hit", decay: 2.5}
        sung: {on: track.voice, decay: 1}
        duo: {on: track.duet, decay: 1}
        bowl: {on: track.bowl, decay: 8}
      vars:
        drive: {follow: "max(max(track.kick.level, track.snare-l.level), max(max(track.hat-l.level, track.ride-l.level), max(track.kick2.level, track.snare2.level)))", attack: 60ms, release: 900ms}
        low: {follow: "max(track.bass.level, track.sub.level)", attack: 200ms, release: 1200ms}
        sing: {follow: "track.voice.level", attack: 120ms, release: 900ms}
        mouth: {follow: "track.voice.gate", attack: 40ms, release: 140ms}
        # The camera rises with the lanterns from the bowl's first stroke.
        rise: {keys: [[80bar, 0], [128bar, 1]], ease: smooth}
        gather: {keys: [[80bar, 0], [120bar, 1]], ease: smooth}
        turn: {integrate: "0.004 + 0.006*var.drive", wrap: 1}
      camera:
        # 0 wide, rising; 1 low and close, the fire against the sea; 2 behind the singer, her
        # lanterns going up over the sea; 3 high among the lanterns.
        - {x: "0.6*sin(var.turn)", y: "0.2 + 1.2*var.rise", z: -2.8, look_at: [0, "0.4 + 1.6*var.rise", 4]}
        - {x: 1.0, y: -0.4, z: -1.2, look_at: [-0.1, "-0.2 + 0.5*var.rise", 0.6]}
        - {x: -0.65, y: -0.06, z: -1.3, look_at: [0.1, "0.1 + 0.7*var.rise", 1.5]}
        - {x: "1.2*sin(var.turn + 0.5)", y: "1.4 + 1.0*var.rise", z: 0.5, look_at: [0, "0.9 + 1.2*var.rise", 5]}
      shot: {keys: [[64bar, 0], [72bar, 1], [80bar, 0], [85bar, 2], [90bar, 0], [96bar, 1], [100bar, 3], [107bar, 2], [112bar, 0], [120bar, 3], [124bar, 2], [128bar, 0]], ease: step}''')
rep('''params: {far: 1, swell: 0.4, light: 0.04}}''', '''params: {far: 1, swell: "0.25 + 0.5*var.low", light: 0.04}}''')
rep('''- {type: group, use: kit-fire, y: -0.6, z: 0.3, params: {size: 0.6, heat: 0.6}}''',
    '''- {type: group, use: kit-fire, y: -0.6, z: 0.3, params: {size: 0.6, heat: "0.45 + 0.4*var.drive + 0.25*env.chord"}}
        # The four lights, lit again in turn by the chords at the end.
        - {type: mesh, shape: sphere, detail: 12, count: 4, spawn: env.chord, x: "1.0*sin(inst.i/4 + 0.225)", z: "0.3 + 1.0*cos(inst.i/4 + 0.225)", y: -0.52, scale: 0.045, sy: 1.3, color: "#e89848", light: 0.2, ambient: 0.05, rim: 0, emit: "0.55 + 3*exp(0 - inst.age/2.5)"}
        - {type: light, count: 4, spawn: env.chord, x: "1.0*sin(inst.i/4 + 0.225)", z: "0.3 + 1.0*cos(inst.i/4 + 0.225)", y: -0.4, color: "#ffd090", power: "2.2*exp(0 - inst.age/2.5)", reach: 1.4}
        # The singer, lit by the fire.
        - {type: figure, rig: human, motion: sway, x: -0.15, z: -0.45, y: -0.22, scale: 0.42, face: [0, 0, 6], energy: "0.4 + 0.5*var.drive", mouth: "0.85*var.mouth", pose: {arm_l: "0 - 0.14*var.sing", arm_r: "0 - 0.14*var.sing", head: "-0.02 - 0.02*var.sing"}, color: "#4a3a38", light: 1, ambient: 0.1, rim: 0.9, rim_color: "#ffc890", material: pbr, rough: 0.6, melt: 0.04}''')
rep('''face: [0, 1.5, 5], energy: 0.3, color: "#1a1418"''', '''face: [0, 1.5, 5], motion: [sway, dance], mix: "clamp(var.drive*1.6, 0, 1)", energy: "0.35 + 0.8*var.drive", color: "#1a1418"''')
rep('''- {type: figure, count: 5, rig: human, motion: sway, x: "0.9*sin(inst.i/5 + 0.1)"''', '''- {type: figure, count: 5, rig: human, x: "0.9*sin(inst.i/5 + 0.1)"''')
rep('''        - {type: light, x: 0, y: 2, z: 5, color: "#ffb060", power: "0.1 + 0.25*smooth(150, 260, time.t)", reach: 5}
        - {type: motes, mode: emit, count: "60 + 340*smooth(150, 270, time.t)",''',
    '''        - {type: light, x: 0, y: 2, z: 5, color: "#ffb060", power: "0.1 + 0.3*var.gather + 0.5*env.bowl", reach: 5}
        # Every note she sings lets one go; the duet's notes another colour.
        - {type: mesh, shape: sphere, detail: 10, count: 40, spawn: env.sung, x: "-0.15 + (hash(inst.i*1.7) - 0.5)*0.4 + 0.05*inst.age*(hash(inst.i*3.3) - 0.5)", y: "0.05 + 0.1*inst.age", z: "-0.35 + 0.2*inst.age", scale: "0.045*(1 + 0.5*env.bowl)", opacity: "clamp(inst.age*4, 0, 1)*clamp((32 - inst.age)/6, 0, 1)", color: "#ffb050", light: 0, ambient: 0, rim: 0, emit: "2.2 + 1.5*env.bowl"}
        - {type: mesh, shape: sphere, detail: 10, count: 24, spawn: env.duo, x: "0.6 + (hash(inst.i*2.3) - 0.5)*0.4 + 0.05*inst.age*(hash(inst.i*1.9) - 0.5)", y: "-0.05 + 0.09*inst.age", z: "0.9 + 0.2*inst.age", scale: "0.04*(1 + 0.5*env.bowl)", opacity: "clamp(inst.age*4, 0, 1)*clamp((32 - inst.age)/6, 0, 1)", color: "#ffe0b0", light: 0, ambient: 0, rim: 0, emit: "2.2 + 1.5*env.bowl"}
        # Each stroke of the bowl: a ring across the water.
        - {type: mesh, shape: torus, detail: 96, tube: 0.004, sy: 0.05, y: -0.9, z: 4, scale: "0.3 + 0.7*env.bowl.age", opacity: "0.5*clamp(1 - env.bowl.age/8, 0, 1)", color: "#ffd9a0", light: 0, ambient: 0, rim: 0, emit: 1.5, blend: add}
        # And the many let go along the shore, more as the theme gathers.
        - {type: motes, mode: emit, count: "8 + 380*var.gather",''')
body = s.split('scenes:')[1]
assert 'audio.' not in body, [l[:140] for l in body.split('\n') if 'audio.' in l][:4]
assert not re.search(r'smooth\(\d+, \d+, time\.t\)', body), re.findall(r'.{30}smooth\(\d+, \d+, time\.t\).{20}', body)[:3]
open('/tmp/cv/t4n/t4.yaml', 'w').write(s)
print('ok', len(s))
