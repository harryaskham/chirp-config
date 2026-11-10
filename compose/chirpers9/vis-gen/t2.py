#!/usr/bin/env python3
"""t2 rebuilt on the song: the committed programme's sets (flight, road, the hole), every signal rebound."""
import subprocess
s = subprocess.run(['git', '-C', '/home/harry/.config/chirp', 'show', '43862ad3:vis/chirpers9-t2.yaml'], capture_output=True, text=True).stdout
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)

head = '''# chirpers9 t2 "The Long Way In": infall as a journey. Co-built with the song
# (tools/songmap.py chirpers9-t2). Seven sections of 16 bars: in, gather, build, crest (48bar),
# break (64bar), drift (80bar), fall (96bar).
#
# What the song does, and so what the picture does:
#   - HOW FAST IT TRAVELS is the composer's `lane.spd` (slow through the in and the gather,
#     quickening through the build, full at the crest, stopped in the break, picking up again in
#     the drift, dying away in the fall). It is the speed of the flight over the land, the
#     walker's pace on the road, and how fast the camera circles the hole.
#   - I (0bar) THE FLIGHT, at dawn over mountains. The mist lifts as the pad's filter opens
#     (`lane.shut`). Two flocks wheel on the song's two cycles: five birds once every five bars
#     (E1's five beats), three once every seven (E2's seven), so they cross and part as the
#     polymeter does. The song's pad is a swarm of oscillators its composer couples with
#     `lane.lock`: the birds close up into formation as far as the swarm has locked. The camera
#     flies higher as the bass lifts away (`lane.grav`).
#   - II (36bar, where the composer shuts the master filter down, `lane.open`) THE ROAD at dusk:
#     a lone walker toward a light on the horizon. The lamps flare on the drums. The light
#     grows as the swarm locks and flares when the hook is sung. In the break (64bar) the walker
#     stops and stands; the fireflies rise and glitter with the guitar arpeggio; the stereo
#     field opens (`lane.WID`) and the camera draws back.
#   - III (76bar, the second kit's pickup) THE HOLE: the light was the hole. Its rings are the
#     song's parts. Clumps are thrown in on the drums and on each low note of the fall; jets
#     fire as the swarm locks under the hook (84bar), as the kit returns (88bar) and as the
#     fall begins (96bar). The camera closes in as the composer narrows the stereo field to a
#     point (`lane.WID`).
# Reads tracks: kit kitb hat3 hook infall gtrarp dust crestsung. Lanes: spd lock grav shut open
#   WID glitch.
'''
i = s.index('scenes:')
s = head + s[i:]

# ---- Act I: the flight ----
rep('''    look:
      background: "#000000"
      camera: {x: "0.3*sin(time.t*0.01)", y: "0.75 + 0.08*audio.low", z: -2.8, look_at: [0, 0.35, 2], roll: "0.02*sin(time.t*0.02)"}''',
'''    look:
      background: "#000000"
      vars:
        # The distance flown: the land goes by at the song's own speed.
        dist: {integrate: "0.3 + 1.6*lane.spd"}
        # How far the swarm has locked (0 free, 1 as one).
        lock: {value: "clamp((lane.lock - 0.3)/2.7, 0, 1)"}
        # The two flocks' laps: once in five bars, once in seven.
        five: {value: "time.bar/5"}
        seven: {value: "time.bar/7"}
        high: {follow: "0 - lane.grav", attack: 2s, release: 2s}
      camera:
        # 0 the flight; 1 beside the first flock; 2 high, looking down the valley.
        - {x: "0.3*sin(time.t*0.01)", y: "0.75 + 0.05*var.high", z: -2.8, look_at: [0, 0.35, 2], roll: "0.02*sin(time.t*0.02)"}
        - {x: "3.3*sin(var.five + 0.1)", y: 0.8, z: "2.5 + 2.4*cos(var.five + 0.1)", look_at: ["1.2*sin(var.five + 0.06)", 0.95, "2.5 + 0.8*cos(var.five + 0.06)"]}
        - {x: -0.4, y: "1.5 + 0.05*var.high", z: -3.2, look_at: [0.2, 0.1, 3]}
      shot: {keys: [[0bar, 0], [12bar, 2], [16bar, 0], [20bar, 1], [24bar, 0], [28bar, 2], [32bar, 0]], ease: step}''')
rep('params: {height: 0.9, travel: "0.45 + 0.3*audio.level", seed: 2, pbr: 1, trees: 1}}', 'params: {height: 0.9, travel: 0, shift: var.dist, seed: 2, pbr: 1, trees: 1}}')
# Flock of five: E1's cycle. Spacing closes as the swarm locks.
rep('''x: "1.2*sin(time.t*0.07 + inst.i*0.2)", y: "0.9 + 0.15*sin(time.t*0.11 + inst.i)", z: "2.5 + 0.8*cos(time.t*0.07 + inst.i*0.2)", face: ["1.2*sin(time.t*0.07 + 0.02 + inst.i*0.2)", "0.9 + 0.15*sin(time.t*0.11 + inst.i)", "2.5 + 0.8*cos(time.t*0.07 + 0.02 + inst.i*0.2)"], scale: 0.26, phase: "inst.i*0.4", energy: "0.7 + 0.5*audio.level"''',
    '''x: "1.2*sin(var.five + inst.i*(0.2 - 0.16*var.lock))", y: "0.9 + 0.15*(1 - var.lock)*sin(time.t*0.11 + inst.i) + 0.04*inst.i*var.lock", z: "2.5 + 0.8*cos(var.five + inst.i*(0.2 - 0.16*var.lock))", face: ["1.2*sin(var.five + 0.02 + inst.i*(0.2 - 0.16*var.lock))", "0.9 + 0.15*(1 - var.lock)*sin(time.t*0.11 + inst.i) + 0.04*inst.i*var.lock", "2.5 + 0.8*cos(var.five + 0.02 + inst.i*(0.2 - 0.16*var.lock))"], scale: 0.26, phase: "inst.i*0.4*(1 - var.lock)", energy: "0.6 + 0.5*track.hook.gate + 0.4*track.kit.hit"''')
# Flock of three: E2's cycle, the other way round.
rep('''x: "-1.4*sin(time.t*0.045 + inst.i*0.3)", y: "1.2 + 0.1*inst.i", z: "3.4 + 1.1*cos(time.t*0.045 + inst.i*0.3)", face: ["-1.4*sin(time.t*0.045 + 0.02 + inst.i*0.3)", "1.2 + 0.1*inst.i", "3.4 + 1.1*cos(time.t*0.045 + 0.02 + inst.i*0.3)"]''',
    '''x: "-1.4*sin(var.seven + inst.i*(0.3 - 0.24*var.lock))", y: "1.2 + 0.1*inst.i", z: "3.4 + 1.1*cos(var.seven + inst.i*(0.3 - 0.24*var.lock))", face: ["-1.4*sin(var.seven + 0.02 + inst.i*(0.3 - 0.24*var.lock))", "1.2 + 0.1*inst.i", "3.4 + 1.1*cos(var.seven + 0.02 + inst.i*(0.3 - 0.24*var.lock))"]''')
rep('''- {type: fog, color: "#d8b8a8", density: 0.08}''', '''- {type: fog, color: "#d8b8a8", density: "0.2 - 0.13*lane.shut"}''')

# ---- Act II: the road ----
rep('''  - at: 95
    transition: dissolve
    xfade: 3
    look:
      background: "#000000"
      env:
        lamp: {on: bar, decay: 0.6}
      camera: {x: "0.3 + 0.1*sin(time.t*0.05)", y: 0.3, z: -0.9, look_at: [0, 0.1, 6]}''',
'''  - at: 36bar
    transition: dissolve
    xfade: 3
    look:
      background: "#000000"
      env:
        lamp: {on: track.kit, decay: 0.3}
      vars:
        # The distance walked, and the pace (0 in the break: he stands).
        pace: {follow: "lane.spd", attack: 400ms, release: 1200ms}
        walk: {integrate: "0.8*lane.spd"}
        lock: {value: "clamp((lane.lock - 0.3)/2.7, 0, 1)"}
        sung: {follow: "max(track.hook.gate, track.crestsung.gate)", attack: 80ms, release: 900ms}
        wide: {follow: "clamp((lane.WID - 0.86)/0.29, 0, 1)", attack: 2s, release: 2s}
      camera:
        # 0 behind the walker; 1 low beside the road; 2 from above and behind: the road ahead.
        - {x: "0.3 + 0.1*sin(time.t*0.05)", y: "0.3 + 0.5*var.wide", z: "-0.9 - 1.6*var.wide", look_at: [0, 0.1, 6]}
        - {x: -0.9, y: -0.3, z: -0.2, look_at: [0.2, 0.0, 1.4]}
        - {x: 0.55, y: 0.75, z: -0.7, look_at: [0, -0.2, 2.2]}
      shot: {keys: [[36bar, 0], [44bar, 1], [48bar, 0], [56bar, 2], [60bar, 1], [64bar, 0], [72bar, 2]], ease: step}''')
rep('fract(vtx.z*14 - time.t*0.25)', 'fract(vtx.z*18 - var.walk)')
# The plain and the road reach behind the walker too (a shot from ahead looks back along them),
# in small facets: a facet with a corner behind the camera is not drawn on the current pin.
rep('- {type: mesh, shape: plane, detail: 16, y: -0.62, z: 10, scale: 14, color: "#1a1a1c"', '- {type: mesh, shape: plane, detail: 96, y: -0.62, z: 6, scale: 18, color: "#1a1a1c"')
rep('- {type: mesh, shape: plane, detail: 8, y: -0.615, z: 10, scale: 1, sx: 0.35, sz: 14, color: "#202024"', '- {type: mesh, shape: plane, detail: 48, y: -0.615, z: 6, scale: 1, sx: 0.35, sz: 18, color: "#202024"')
# The light he walks toward falls on him and on the road ahead.
rep('        # The walker, seen from behind, walking in.', '        - {type: light, x: 0, y: 1.2, z: 22, color: "#ffe8c8", power: "0.4 + 1.1*var.lock + 1.4*var.sung", reach: 30}\n        # The walker, walking in.')
rep('z: "fract((inst.i/8) - time.t*0.0083)*16 - 1"', 'z: "fract((inst.i/8) - var.walk/16)*16 - 1"', 3)
rep('''scale: "0.25 + 1.2*smooth(95, 190, time.t) + 0.4*audio.lift", color: "#fff0d0", light: 0, ambient: 0, rim: 0, emit: "3 + 4*audio.lift"}''',
    '''scale: "0.3 + 1.1*var.lock + 0.35*var.sung", color: "#fff0d0", light: 0, ambient: 0, rim: 0, emit: "3 + 4*var.sung"}''')
rep('''glow: "0.2 + 0.8*smooth(150, 190, time.t)*(0.5 + audio.level)", fade: 0.6, color: "#c8d8ff"}''',
    '''glow: "0.15 + 0.7*var.lock + 0.5*var.sung", fade: 0.6, color: "#c8d8ff"}''')
rep('''face: [0, 0, 30], energy: 0.9, color: "#1a1a20"''', '''face: [0, 0, 30], energy: "1.1*clamp(var.pace*2.5, 0, 1)", color: "#1a1a20"''')
rep('''wind_z: -0.25, fall: 0, wobble: 0.15, size: 0.004, glow: "1.2 + audio.level", twinkle: 0.8''',
    '''wind_z: "0 - 0.5*var.pace", fall: "0 - 0.12*(1 - clamp(var.pace*3, 0, 1))", wobble: 0.15, size: 0.004, glow: "1.0 + 1.6*track.gtrarp.hit + 0.8*track.dust.hit", twinkle: 0.8''')
rep('''amount: "0.6 + 0.6*audio.lift", threshold: 0.9, streak: 0.4''', '''amount: "0.4 + 0.3*var.lock + 0.6*var.sung", threshold: 0.9, streak: 0.4''')
i = s.index('        - {type: bloom', s.index('  - at: 36bar'))
s = s[:i] + '''        - {type: chroma, amount: "0.06*lane.glitch*(0.4 + track.kit.hit)"}
''' + s[i:]

# ---- Act III: the hole ----
rep('''  - at: 195
    transition: dissolve
    xfade: 4
    look: {extends: accretion3d, params: {gas: 0.5, debris: 10}}''',
'''  - at: 76bar
    transition: dissolve
    xfade: 4
    look:
      extends: accretion3d
      params: {gas: 0.5, debris: 12}
      vars:
        # The camera closes in as the stereo field narrows to a point; it circles at the
        # song's speed.
        dist: {value: "(1.5 + 1.9*clamp(lane.WID, 0.15, 1.15)/1.15)*(0.3 + 0.7*mix.in)*(1 - 0.7*mix.out)"}
        orbit: {integrate: "0.02 + 0.07*lane.spd", wrap: 1}
      env:
        hit: {when: "3*max(max(track.kitb.hit, track.kit.hit), track.infall.hit)", decay: 0.3}
        # Jets: as the swarm locks under the hook, as the kit returns, as the fall begins.
        crest: {when: {keys: [[76bar, 0], [84bar, 1], [84.5bar, 0], [88bar, 1], [88.5bar, 0], [96bar, 1], [96.5bar, 0]], ease: step}, decay: 4}
        victim: {when: "step(param.victim, time.t)*step(0.001, param.victim)", decay: 3}
      camera:
        x: "var.dist*sin(var.orbit)"
        z: "0 - var.dist*cos(var.orbit)"
        y: "0.32*var.dist*(0.35 + 0.25*sin(var.orbit*0.7))"
        look_at: [0, 0, 0]''')
body = s.split('scenes:')[1]
assert 'audio.' not in body, [l[:120] for l in body.split('\n') if 'audio.' in l][:4]
open('/tmp/cv/t2n/t2.yaml', 'w').write(s)
print('ok', len(s))
