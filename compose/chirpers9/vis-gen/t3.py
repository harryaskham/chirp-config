#!/usr/bin/env python3
"""t3 rebuilt on the song: the committed programme's sets (street, plaza), every signal rebound."""
import subprocess
s = subprocess.run(['git', '-C', '/home/harry/.config/chirp', 'show', '106f4329:vis/chirpers9-t3.yaml'], capture_output=True, text=True).stdout
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

head = '''# chirpers9 t3 "Phase Margin": the first storm. Co-built with the song (tools/songmap.py chirpers9-t3).
#
# What the song does, and so what the picture does:
#   - THE STORM (from 16bar): glitching, abrasive, rhythmically hard. A city street at night.
#     The composer's `lane.glitch` is how hard it storms: how many windows are lit, how hard the
#     picture splits its colours, how much rain falls (with the `rain` track itself). Lightning
#     strikes on the thunder and on the drum fills that end each eight bars. The windows flicker
#     on the sixteenth grid and flare on the glitch shards. The walk down the street goes as fast
#     as the drums play.
#   - THE CROWD (from 40bar, the thunder crack): a wet plaza, neon pulsing magenta on the kick and
#     cyan on the hats, a crowd dancing on the beat, every dancer out of phase with the others.
#   - THE TAPE STOP (56bar): the neon goes out for the stop.
#   - THE EYE (60-64bar, `lane.still`): the drums stop, the rain stops, the dancers stand almost
#     still, birds cross overhead (the bird tracks); then the birds flee and the storm returns.
#   - PHASE (66-88bar): the song's swarm of oscillators is pulled together by `lane.sync`. The
#     dancers' phases close up exactly as far as the swarm's coupling has risen.
#   - THE LOCK (88bar, the crash): the coupling jumps and every dancer lands on the same beat.
#     The camera cuts high over them moving as one; a flock rises (`lane.flock`); the rain has
#     stopped; over the next sixteen bars dawn comes up.
# Shots cut on bar lines.
# Reads tracks: kick hats snare bass e2 hand kick7 shard chipsn rain wind thunder thunder1 thunder2
#   fills crash birdl birdr fleel fleer. Lanes: glitch still sync stop flock.
'''
i = s.index('scenes:')
s = head + s[i:]

# ---- Act I: the street ----
rep('''      env:
        flash: {on: audio.lift, decay: 0.35}
        bar8: {on: bar, every: 8, decay: 0.3}
        hit: {on: audio.onset, decay: 0.12}
      camera: {x: 0.1, y: 0.15, z: "(time.t)*0.3 - 4", look_at: [0, -0.15, "(time.t)*0.3"]}''',
'''      env:
        # Lightning: the thunder, and the fill that ends each eight bars.
        flash: {when: "3*max(max(track.thunder.hit, track.thunder1.hit), max(track.thunder2.hit, track.fills.hit))", decay: 0.35}
      vars:
        drive: {follow: "max(max(track.kick.level, track.hats.level), max(track.bass.level, 0.6*track.e2.level))", attack: 60ms, release: 900ms}
        storm: {follow: "clamp(max(track.rain.level, 4*lane.glitch) + 0.3*track.wind.level, 0, 1)", attack: 300ms, release: 2s}
        walk: {integrate: "0.08 + 0.4*var.drive"}
      camera: {x: 0.1, y: 0.15, z: "var.walk - 4", look_at: [0, -0.15, "var.walk"]}''')
rep('z: "(time.t)*0.3 - 6 + fract((floor(inst.i/2)*1.4 - (time.t)*0.3)/28)*28"', 'z: "var.walk - 6 + fract((floor(inst.i/2)*1.4 - var.walk)/28)*28"')
rep('step(0.62 - 0.12*audio.level, hash(floor((vtx.x + vtx.z)*5)*13.1 + floor(vtx.y*40)*7.7 + inst.i*31.3))*1.6*(0.6 + 0.4*step(0.5, hash(floor(time.t*8) + inst.i)))',
    'step(0.72 - 0.7*lane.glitch - 0.1*track.e2.hit, hash(floor((vtx.x + vtx.z)*5)*13.1 + floor(vtx.y*40)*7.7 + inst.i*31.3))*1.6*(0.5 + 0.5*step(0.5, hash(floor(time.beat*4) + inst.i)))*(0.7 + 0.9*track.shard.hit)')
rep('''count: 3500, from: [0, 1.8, "(time.t)*0.3 + 1"], wide: 6, deep: 10''', '''count: "150 + 3300*var.storm", from: [0, 1.8, "var.walk + 1"], wide: 6, deep: 10''')
rep('''        - {type: chroma, amount: "0.012*env.hit + 0.02*env.flash"}''',
    '''        - {type: chroma, amount: "0.05*lane.glitch*(track.shard.hit + track.chipsn.hit) + 0.02*env.flash"}''')

# ---- Act II: the plaza ----
rep('''  - at: 100
    transition: iris
    xfade: 2''', '''  - at: 40bar
    transition: iris
    xfade: 2''')
rep('''      env:
        flash: {on: audio.lift, decay: 0.35}
        bar8: {on: bar, every: 8, decay: 0.3}
        hit: {on: audio.onset, decay: 0.12}
      vars:
        lock: {value: "smooth(200, 232, time.t)"}
      camera: {x: "2.2*sin(time.t*0.02)*(1 - 0.4*var.lock)", y: "0.5 + 1.6*var.lock", z: "0 - 2.2*cos(time.t*0.02)*(1 - 0.4*var.lock)", look_at: [0, -0.25, 0]}''',
'''      env:
        flash: {when: "3*max(max(track.thunder1.hit, track.thunder2.hit), max(track.fills.hit, track.crash.hit))", decay: 0.35}
      vars:
        drive: {follow: "max(max(track.kick.level, track.hats.level), max(track.kick7.level, track.hand.level))", attack: 60ms, release: 900ms}
        storm: {follow: "clamp(max(track.rain.level, 4*lane.glitch), 0, 1)", attack: 300ms, release: 1s}
        # How far the swarm's coupling has pulled the crowd together: 0 apart, 1 as one (88bar).
        lock: {value: "clamp((lane.sync - 0.15)/3.85, 0, 1)"}
        dawn: {keys: [[88bar, 0], [104bar, 1]], ease: smooth}
        eye: {value: "clamp(0 - lane.still/60, 0, 1)"}
        birds: {follow: "max(max(track.birdl.gate, track.birdr.gate), max(track.fleel.gate, track.fleer.gate))", attack: 300ms, release: 3s}
        turn: {integrate: "0.008 + 0.022*var.drive", wrap: 1}
      camera:
        # 0 round the crowd; 1 close and low among them; 2 high over them; 3 from the front.
        - {x: "2.2*sin(var.turn)", y: 0.5, z: "0 - 2.2*cos(var.turn)", look_at: [0, -0.25, 0]}
        - {x: "1.25*sin(var.turn + 0.3)", y: -0.12, z: "0 - 1.25*cos(var.turn + 0.3)", look_at: [0, -0.2, 0]}
        - {x: "1.4*sin(var.turn)", y: 2.1, z: "0 - 1.4*cos(var.turn)", look_at: [0, -0.35, 0]}
        - {x: "0.4*sin(var.turn*2)", y: 0.15, z: -3.0, look_at: [0, -0.15, 0]}
      shot: {keys: [[40bar, 0], [48bar, 1], [56bar, 3], [60bar, 2], [66bar, 1], [72bar, 0], [80bar, 3], [86bar, 1], [88bar, 2], [96bar, 0], [104bar, 1], [108bar, 3], [112bar, 2]], ease: step}''')
rep('sun_height: "0.08*var.lock - 0.02", sun_size: 0.04, glow: "0.7*var.lock", haze: 0.4}', 'sun_height: "0.08*var.dawn - 0.02", sun_size: 0.04, glow: "0.7*var.dawn", haze: 0.4}')
rep('''- {type: sky, opacity: "var.lock", zenith: "#3a4a7a"''', '''- {type: sky, opacity: var.dawn, zenith: "#3a4a7a"''')
rep('sun_height: "0.08*var.lock - 0.02", sun_size: 0.04, glow: "0.9*var.lock"', 'sun_height: "0.08*var.dawn - 0.02", sun_size: 0.04, glow: "0.9*var.dawn"')
rep('''        # Neon round the plaza in the storm, pooling on the wet stone and rimming the dancers.''',
    '''        # Neon round the plaza: magenta on the kick, cyan on the hats, out for the tape stop.''')
rep('''color: "#ff3cb4", power: "(1.6 + 0.8*env.hit)*(1 - var.lock)*step(0.5, fract(inst.i/2))", reach: 2.5}''',
    '''color: "#ff3cb4", power: "(0.9 + 2.2*max(track.kick.hit, track.kick7.hit))*(1 - var.dawn)*(1 - lane.stop)*step(0.5, fract(inst.i/2))", reach: 2.5}''')
rep('''color: "#3cc8ff", power: "(1.6 + 0.8*env.hit)*(1 - var.lock)*(1 - step(0.5, fract(inst.i/2)))", reach: 2.5}''',
    '''color: "#3cc8ff", power: "(0.9 + 2.2*max(track.hats.hit, track.snare.hit))*(1 - var.dawn)*(1 - lane.stop)*(1 - step(0.5, fract(inst.i/2)))", reach: 2.5}''')
rep('''color: "#ffc080", power: "0.15 + 0.6*var.lock", reach: 6}''', '''color: "#ffc080", power: "0.15 + 0.35*var.lock + 0.5*var.dawn", reach: 6}''')
rep('''        # The crowd: out of step with each other (each its own phase), smearing in the
        # storm, then locking into one groove as the storm resolves.''',
    '''        # The crowd: on the beat, each out of phase with the others by as much as the swarm
        # is still apart; as one from the lock. They move as hard as the drums play.''')
rep('energy: "(0.6 + 0.5*hash(inst.i + 300)*(1 - var.lock))*(0.7 + audio.level*1.3)"', 'energy: "(0.6 + 0.5*hash(inst.i + 300)*(1 - var.lock))*(0.25 + 1.6*var.drive)*(1 - 0.8*var.eye)"')
rep('rim: "0.4 + 0.8*var.lock", rim_color: "#ffd0a0"', 'rim: "0.4 + 0.8*var.dawn", rim_color: "#ffd0a0"')
rep('''count: 2500, from: [0, 1.8, 0], wide: 5, deep: 5''', '''count: "60 + 2400*var.storm*(1 - var.eye)", from: [0, 1.8, 0], wide: 5, deep: 5''')
rep('''glow: "(0.5 + env.flash)*(1 - var.lock)", twinkle: 0, color: "#9aa8c8"''', '''glow: "0.5 + env.flash", twinkle: 0, color: "#9aa8c8"''')
# Birds: over the eye, fleeing as the storm returns; the flock that rises at the lock.
i = s.index('      filters:', s.index('  - at: 40bar'))
birds = '''        # Birds: crossing in the eye, fleeing as the storm returns; the flock rising at the lock.
        - {type: motes, mode: flock, count: 260, seed: 4, opacity: "clamp(var.birds + lane.flock/2.7, 0, 1)*(1 - var.dawn)", y: "0.9 + 0.5*lane.flock", z: 0.6, w: "2.2 + 1.2*lane.flock", h: 0.7, d: 2.2, spin: "0.8 + 2.5*max(track.fleel.gate, track.fleer.gate) + 0.5*lane.flock", wobble: 0.3, size: 0.006, stretch: 2.5, heading: true, glow: 0.35, twinkle: 0.1, color: "#cfd8e8", near: 0.3}
        - {type: motes, mode: flock, puff: true, count: 260, seed: 4, opacity: "clamp(lane.flock/2.7, 0, 1)*var.dawn", y: "0.9 + 0.5*lane.flock", z: 0.6, w: "2.2 + 1.2*lane.flock", h: 0.7, d: 2.2, spin: "0.8 + 0.5*lane.flock", wobble: 0.3, size: 0.008, stretch: 2.5, heading: true, glow: 0.9, twinkle: 0, color: "#181420", near: 0.3}
'''
s = s[:i] + birds + s[i:]
rep('''amount: "0.6 - 0.3*var.lock", reach: 2''', '''amount: "0.6 - 0.3*var.dawn", reach: 2''')
rep('''amount: "0.65*var.lock", soft: 2, size: 2048''', '''amount: "0.65*var.dawn", soft: 2, size: 2048''')
rep('''amount: "(0.012*env.hit + 0.02*env.flash)*(1 - var.lock)"''', '''amount: "0.05*lane.glitch*(track.shard.hit + track.chipsn.hit) + 0.02*env.flash + 0.05*lane.stop"''')
# Act I's lightning stands ahead of the walk, wherever it has got to.
i = s.index('  - at: 40bar')
one = s[:i]
for a_, b_ in [
    ('{type: light, x: 0, y: 6, z: 6, color: "#c8d8ff", power: "8*env.flash", reach: 20}',
     '{type: light, x: 0, y: 6, z: "var.walk + 6", color: "#c8d8ff", power: "8*env.flash", reach: 20}'),
    ('4, "8 + 3*hash(time.t - env.flash.age + 7)"], to:',
     '4, "var.walk + 8 + 3*hash(time.t - env.flash.age + 7)"], to:'),
    ('"0.2 + inst.i*1.2", "8 + 3*hash(time.t - env.flash.age + 7)"]',
     '"0.2 + inst.i*1.2", "var.walk + 8 + 3*hash(time.t - env.flash.age + 7)"]'),
]:
    assert one.count(a_) == 1, (a_, one.count(a_))
    one = one.replace(a_, b_)
s = one + s[i:]
# The plaza's cameras keep clear of the dancers (the crowd's corners are 1.2 out); the high
# one looks down at an angle, so the dance still reads; the lock is seen from the front.
rep('- {x: "1.25*sin(var.turn + 0.3)", y: -0.12, z: "0 - 1.25*cos(var.turn + 0.3)", look_at: [0, -0.2, 0]}',
    '- {x: "1.8*sin(var.turn + 0.3)", y: -0.05, z: "0 - 1.8*cos(var.turn + 0.3)", look_at: [0, -0.2, 0]}')
rep('- {x: "1.4*sin(var.turn)", y: 2.1, z: "0 - 1.4*cos(var.turn)", look_at: [0, -0.35, 0]}',
    '- {x: "2.1*sin(var.turn)", y: 1.6, z: "0 - 2.1*cos(var.turn)", look_at: [0, -0.35, 0]}')
rep('[86bar, 1], [88bar, 2], [96bar, 0], [104bar, 1], [108bar, 3], [112bar, 2]]',
    '[86bar, 1], [88bar, 3], [92bar, 2], [96bar, 0], [104bar, 1], [108bar, 3], [112bar, 2]]')
# The plaza's floor in small facets: a facet with a corner behind the camera is not drawn,
# so large ones leave a black wedge under a low camera.
rep('- {type: mesh, shape: plane, detail: 12, y: -0.62, scale: 8, color: "#3a3638"', '- {type: mesh, shape: plane, detail: 48, y: -0.62, scale: 8, color: "#3a3638"')
assert 'audio.' not in s.split('scenes:')[1], [l for l in s.split('\n') if 'audio.' in l][:3]
assert 'env.hit' not in s and 'env.bar8' not in s
open('/tmp/cv/t3n/t3.yaml', 'w').write(s)
print('ok', len(s))
