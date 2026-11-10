#!/usr/bin/env python3
"""t5 rebuilt on the song: the committed programme's sets (the star and its worlds; riding one world), every signal rebound."""
import subprocess, re
s = subprocess.run(['git', '-C', '/home/harry/.config/chirp', 'show', 'a3af8c1c:vis/chirpers9-t5.yaml'], capture_output=True, text=True).stdout
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)

head = '''# chirpers9 t5 "Periapsis": the inner disk; one pass round the star. Co-built with the song
# (tools/songmap.py chirpers9-t5).
#
# What the song does, and so what the picture does:
#   - The song's `orbit` voice circles the listener on an orbit its composer automates:
#     `lane.peri_near` is how far away it passes (6 far out, 0.8 at the closest pass, bar 76,
#     then out again) and `lane.peri_spin` how fast it goes round (four times faster at the
#     closest pass). The picture is that orbit: worlds round a hot star, drawing in and
#     speeding up exactly as the sound does, then swinging out and slowing.
#   - `lane.heat` is the star: how bright it burns and how fast its surface boils. Each of the
#     four-lights chords (the `lights` track) swells it.
#   - The three worlds are three voices: the inner one the orbit ostinato (E5), the middle one
#     the seed's high layer, the outer one its low layer. Each swells on its own notes.
#   - I (0bar) the star and its worlds, from outside.
#   - II (56bar, where the 808 comes in and the orbit starts to close) riding one world: the
#     star grows over its limb as far as the orbit has closed, and fills the sky at the closest
#     pass (76bar: the crest; a flare washes over everything). The clouds race as fast as the
#     orbit turns.
#   - III (100bar, the hats leaning to the middle) from outside again, swinging out and slowing.
# Shots cut on bar lines.
# Reads tracks: lights orbit seed-hi seed-lo drums crest hats-l hats-r. Lanes: peri_near
#   peri_spin heat.
'''
i = s.index('scenes:')
s = head + s[i:]

# ---- I and III: from outside (one look, used twice) ----
rep('''      env:
        flare: {on: audio.lift, decay: 2}
      vars:
        tight: {value: "smooth(0, 130, time.t)"}
      camera: {x: "3.4*sin(time.t*0.012)", y: "0.7 - 0.3*var.tight", z: "0 - 3.4*cos(time.t*0.012)", look_at: [0, 0.5, 0]}''',
'''      env:
        # A flare of matter: at the closest pass.
        flare: {on: track.crest, decay: 2.5}
        chord: {on: track.lights, decay: 1.6}
      vars:
        # How far the orbit has closed (0 far out, 1 at the closest pass) and how far round
        # it has gone (laps).
        tight: {value: "clamp((6 - lane.peri_near)/5.2, 0, 1)"}
        lap: {integrate: "0.05*lane.peri_spin"}
        heat: {value: "clamp((lane.heat + 0.8)/2.1, 0, 1)"}
        boil: {integrate: "0.01 + 0.06*var.heat"}
        round: {integrate: "0.004 + 0.01*lane.peri_spin", wrap: 1}
      camera:
        # 0 wide, circling; 1 low in the plane of the orbits; 2 from above: the orbits as rings.
        - {x: "3.9*sin(var.round)", y: "1.3 - 0.5*var.tight", z: "0 - 3.9*cos(var.round)", look_at: [0, 0, 0]}
        - {x: "4.0*sin(var.round + 0.3)", y: 0.3, z: "0 - 4.0*cos(var.round + 0.3)", look_at: [0, 0, 0]}
        - {x: "1.2*sin(var.round + 0.6)", y: 2.3, z: "0 - 1.2*cos(var.round + 0.6)", look_at: [0, 0, 0]}
      shot: {keys: [[0bar, 0], [8bar, 2], [16bar, 0], [24bar, 1], [32bar, 0], [40bar, 2], [44bar, 1], [48bar, 0], [100bar, 1], [108bar, 0], [116bar, 1]], ease: step}''')
rep('''        - {type: light, color: "#fff4e0", power: "1.4 + 0.6*env.flare + 0.4*audio.level", reach: 30}''',
    '''        - {type: light, color: "#fff4e0", power: "1.0 + 0.9*var.heat + 0.6*env.flare + 0.5*env.chord", reach: 30}''')
rep('''scale: "0.7 + 0.03*audio.low", color: "#ff7020", light: 0, ambient: 0, rim: "1.6 + 0.8*env.flare", rim_power: 3, emit: 0.95, paint: "1.0*pow(clamp(fbm(vtx.x*5 + time.t*0.03, vtx.y*5, vtx.z*5 - time.t*0.02)*1.5 + 0.6, 0, 1), 2)"''',
    '''scale: "0.66 + 0.06*var.heat + 0.03*env.chord", color: "#ff7020", light: 0, ambient: 0, rim: "1.0 + 1.0*var.heat + 0.8*env.flare + 0.5*env.chord", rim_power: 3, emit: "0.7 + 0.3*var.heat", paint: "(0.5 + 0.7*var.heat + 0.4*env.chord)*pow(clamp(fbm(vtx.x*5 + var.boil, vtx.y*5, vtx.z*5 - var.boil*0.7)*1.5 + 0.6, 0, 1), 2)"''')
# The three worlds: the orbit, drawn in and sped up by the composer's lanes; each a voice.
rep('''x: "(1.6 - 0.35*var.tight)*cos(time.t*(0.045 + 0.03*var.tight))", z: "(1.6 - 0.35*var.tight)*sin(time.t*(0.045 + 0.03*var.tight))", scale: 0.22,''',
    '''x: "(1.7 - 0.55*var.tight)*cos(var.lap*1.9)", z: "(1.7 - 0.55*var.tight)*sin(var.lap*1.9)", scale: "0.22*(1 + 0.25*track.orbit.hit)",''')
rep('''x: "(2.4 - 0.5*var.tight)*cos(time.t*(0.028 + 0.02*var.tight) + 0.35)", z: "(2.4 - 0.5*var.tight)*sin(time.t*(0.028 + 0.02*var.tight) + 0.35)", y: 0.1, scale: 0.3,''',
    '''x: "(2.5 - 0.9*var.tight)*cos(var.lap*1.2 + 0.35)", z: "(2.5 - 0.9*var.tight)*sin(var.lap*1.2 + 0.35)", y: 0.1, scale: "0.3*(1 + 0.2*track.seed-hi.hit)",''')
rep('''x: "(3.2 - 0.6*var.tight)*cos(time.t*(0.019 + 0.012*var.tight) + 0.7)", z: "(3.2 - 0.6*var.tight)*sin(time.t*(0.019 + 0.012*var.tight) + 0.7)", y: -0.1, scale: 0.26,''',
    '''x: "(3.3 - 1.3*var.tight)*cos(var.lap*0.8 + 0.7)", z: "(3.3 - 1.3*var.tight)*sin(var.lap*0.8 + 0.7)", y: -0.1, scale: "0.26*(1 + 0.2*track.seed-lo.hit)",''')
rep('''amount: "0.2 + 0.8*env.flare", threshold: 0.95, streak: 0.35''', '''amount: "0.15 + 0.3*var.heat + 0.8*env.flare + 0.25*env.chord", threshold: 0.95, streak: 0.35''')

# ---- II: riding one world ----
rep('''  - at: 130
    transition: dissolve
    xfade: 3
    look:
      background: "#000000"
      env:
        flare: {on: audio.lift, decay: 2.5}
      camera: {x: 0, y: 0.15, z: -3.2, look_at: [0, 0.35, 2], roll: "0.02*sin(time.t*0.07)"}''',
'''  - at: 56bar
    transition: dissolve
    xfade: 3
    look:
      background: "#000000"
      env:
        flare: {on: track.crest, decay: 3}
        chord: {on: track.lights, decay: 1.6}
      vars:
        tight: {value: "clamp((6 - lane.peri_near)/5.2, 0, 1)"}
        heat: {value: "clamp((lane.heat + 0.8)/2.1, 0, 1)"}
        boil: {integrate: "0.01 + 0.06*var.heat"}
        # The world turns under us as fast as the orbit goes round.
        turn: {integrate: "0.012*lane.peri_spin"}
        hats: {follow: "max(track.hats-l.hit, track.hats-r.hit)", attack: 10ms, release: 200ms}
      camera:
        # 0 over the limb; 1 lower and to one side; 2 looking up at the star.
        - {x: 0, y: 0.05, z: -1.6, look_at: [0, "0.45 + 0.4*var.tight", 4], roll: "0.02*sin(var.turn*3)"}
        - {x: -0.9, y: 0.0, z: -1.3, look_at: [0.3, "0.5 + 0.4*var.tight", 5], roll: -0.04}
        - {x: 0.5, y: 0.1, z: -0.6, look_at: [0, "0.8 + 0.5*var.tight", 9]}
      shot: {keys: [[56bar, 0], [64bar, 1], [72bar, 0], [76bar, 2], [80bar, 0], [88bar, 1], [96bar, 0]], ease: step}''')
# The star: its size and height from how far the orbit has closed.
rep('''- {type: light, x: 0, y: "0.4 + 0.5*smooth(130, 259, time.t)", z: 9, color: "#fff0d8", power: "1.6 + 1.2*env.flare", reach: 30}''',
    '''- {type: light, x: 0, y: "0.5 + 0.7*var.tight", z: 9, color: "#fff0d8", power: "1.0 + 0.9*var.heat + 1.2*env.flare + 0.5*env.chord", reach: 30}''')
rep('''x: 0, y: "0.4 + 0.5*smooth(130, 259, time.t)", z: 9, scale: 1.8, color: "#ff7020", light: 0, ambient: 0, rim: "1.6 + 0.8*env.flare", rim_power: 3, rim_color: "#ffe0a0", emit: 0.95, paint: "1.0*pow(clamp(fbm(vtx.x*5 + time.t*0.03, vtx.y*5, vtx.z*5 - time.t*0.02)*1.5 + 0.6, 0, 1), 2)"''',
    '''x: 0, y: "0.5 + 0.7*var.tight", z: 9, scale: "0.8 + 1.4*var.tight + 2.6*var.tight*var.tight*var.tight + 0.08*env.chord", color: "#ff7020", light: 0, ambient: 0, rim: "1.0 + 1.0*var.heat + 0.8*env.flare + 0.5*env.chord", rim_power: 3, rim_color: "#ffe0a0", emit: "0.7 + 0.3*var.heat", paint: "(0.5 + 0.7*var.heat + 0.4*env.chord)*pow(clamp(fbm(vtx.x*5 + var.boil, vtx.y*5, vtx.z*5 - var.boil*0.7)*1.5 + 0.6, 0, 1), 2)"''')
rep('''params: {sea: 0.25, seed: 7, spin: 0.012, cities: 1.5, clouds: 1.2}}''', '''ry: var.turn, params: {sea: 0.25, seed: 7, spin: 0, cities: "0.9 + 0.7*var.hats", clouds: 1.2}}''')
rep('''amount: "0.5 + 1.2*env.flare", threshold: 0.9, streak: 0.5''', '''amount: "0.3 + 0.5*var.tight + 1.2*env.flare + 0.3*env.chord", threshold: 0.9, streak: 0.5''')
rep('''y: "0.4 + 0.5*smooth(130, 259, time.t)", z: 9, amount:''', '''y: "0.5 + 0.7*var.tight", z: 9, amount:''')

# ---- III: from outside again (the first look, at 100bar) ----
i = s.index('  - at: 0\n'); j = s.index('  - at: 56bar')
first = s[i:j]
third = first.replace('  - at: 0\n', '  - at: 100bar\n    transition: dissolve\n    xfade: 3\n', 1)
s = s.rstrip('\n') + '\n' + third
body = s.split('scenes:')[1]
assert 'audio.' not in body, [l[:140] for l in body.split('\n') if 'audio.' in l][:4]
assert not re.search(r'smooth\(\d+, \d+, time\.t\)', body)
open('/tmp/cv/t5n/t5.yaml', 'w').write(s)
print('ok', len(s))
