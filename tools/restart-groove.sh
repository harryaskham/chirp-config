#!/usr/bin/env bash
# restart.sh SONG [ARRANGEMENT] — restart the live groove on the current binary and its evolver.
C=/tmp/lt/chirp-groove
for p in $(pgrep -f '^/home/harry/.nix-profile/bin/python3 /home/harry/.config/chirp/tools/evolve.py'); do kill "$p"; done
$C stop groove >/dev/null 2>&1
sleep 0.3
setsid nohup "$C" --loop --id groove -o music -s "$1" > /tmp/lt/groove.log 2>&1 < /dev/null &
sleep 1.2
if [ -n "$2" ]; then $C live set --id groove --when bar --xfade 150ms "tracks.arrangement.score=$2" | tail -1; fi
EVOLVE_RESUME=1 setsid nohup /home/harry/.nix-profile/bin/python3 /home/harry/.config/chirp/tools/evolve.py >> /tmp/lt/evolve.log 2>&1 < /dev/null &
sleep 0.5
$C live list
pgrep -f '^/home/harry/.nix-profile/bin/python3 /home/harry/.config/chirp/tools/evolve.py' >/dev/null && echo "evolver running"
