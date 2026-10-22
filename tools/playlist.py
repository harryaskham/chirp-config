#!/usr/bin/env python3
"""Hill-climb playlist driver: keeps the live `groove`'s native session playlist equal to every enabled climb
in climbs.json, each entry its song file (re-read by the session at each turn, so it plays the version
committed by then; see the registry's _protocol). Players (`chirp player`, the web) show the whole rotation.

- On start (and after a groove restart) the playlist is set, repeating, starting after the climb playing
  or queued now; afterwards only changes are applied (climbs added or removed, `passes` changed), so the
  song playing is never interrupted.
- A climb with `passes: N` plays N passes; `enabled: false` leaves the rotation.
- The session validates every file at its turn; one that fails (e.g. it needs a newer engine than the
  groove runs) is skipped and its error shows beside the entry.
- tools/playlist-solo (runtime, ignored) holding one climb id makes the playlist that climb alone.
- tools/playlist-album (runtime, ignored) holding an album name makes the playlist that album: its enabled tracks
  with a song, in track order, looping; tracks join as their first versions are kept. Until one has a song the
  whole rotation plays.
- tools/playlist-ids (runtime, ignored) listing climb ids (whitespace or commas) makes the playlist those climbs
  that have a song, in that order, looping; each joins as its first version is kept. Until one has a song,
  playlist-album (else the whole rotation) plays. It takes precedence over playlist-album.
- A player playing an album (or any playlist mostly of other songs) is left alone until it finishes
  (albums play once through) or is cleared; then the rotation comes back.
- To show Harry something, take over for one pass: `chirp live queue FILE --id groove --now --label NAME`.
  Queued songs play before the playlist's next entry; the rotation carries on afterwards.
- Underrun increases are logged with the host load (they track CPU storms on the host).

Started by tools/restart-groove.sh playlist. Log: /tmp/chirp-playlist.log."""
import getpass, json, os, socket, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
C = os.environ.get("CHIRP_BIN", os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "chirp-groove"))
ID = os.environ.get("PLAYLIST_GROOVE", "groove")


def sock_path():
    """The groove's control socket: the first of chirp's own session dirs that holds it (XDG_RUNTIME_DIR, then
    /run/user/UID, then /tmp/chirp-USER), so a driver started without XDG_RUNTIME_DIR (the watchdog's environment)
    still finds the session the binary finds."""
    if os.environ.get("PLAYLIST_SOCKET"):
        return os.environ["PLAYLIST_SOCKET"]
    dirs = [os.environ.get("XDG_RUNTIME_DIR"), f"/run/user/{os.getuid()}", f"/tmp/chirp-{getpass.getuser()}"]
    paths = [os.path.join(d, "chirp", f"{ID}.sock") for d in dirs if d]
    return next((p for p in paths if os.path.exists(p)), paths[0])


def request(req):
    """One control request on the groove's socket; returns its data (raises on an error reply)."""
    with socket.socket(socket.AF_UNIX) as s:
        s.settimeout(15)
        s.connect(sock_path())
        s.sendall((json.dumps(req) + "\n").encode())
        line = s.makefile().readline()
    r = json.loads(line)
    if not r.get("ok"):
        raise RuntimeError(r.get("error") or line.strip())
    return r.get("data")


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def enabled():
    try:
        reg = json.load(open(os.path.join(ROOT, "climbs.json")))
    except (OSError, ValueError) as e:
        log("registry unreadable:", e)
        return []
    return [c for c in reg.get("climbs", []) if c.get("enabled", True)]


def climbs():
    on = enabled()
    on = ids_only(on) or album_only(on)
    try:
        solo = open(os.path.join(HERE, "playlist-solo")).read().strip()
    except OSError:
        solo = ""
    if solo:
        on = [c for c in on if c["id"] == solo] or on
    return on


ALBUM_MODE = [None]
IDS_MODE = [None]


def ids_only(on):
    """tools/playlist-ids: only those climbs that have a song, in the listed order; None while none has (or no file)."""
    try:
        ids = [x for x in open(os.path.join(HERE, "playlist-ids")).read().replace(",", " ").split() if x]
    except OSError:
        ids = []
    mode, mine = None, None
    if ids:
        by = {c["id"]: c for c in on}
        mine = [by[i] for i in ids if i in by and by[i].get("song") and os.path.exists(path(by[i]))] or None
        mode = (f"climbs {', '.join(ids)}: {len(mine)} with a song ({', '.join(c['id'] for c in mine)})" if mine
                else f"climbs {', '.join(ids)}: none has a song yet, so the album/rotation plays")
    if mode != IDS_MODE[0]:
        IDS_MODE[0] = mode
        if mode:
            log("playlist:", mode)
    return mine


def album_only(on):
    """tools/playlist-album: only that album's enabled tracks that have a song, in track order (else everything)."""
    try:
        album = open(os.path.join(HERE, "playlist-album")).read().strip()
    except OSError:
        album = ""
    mode = None
    if album:
        mine = [c for c in on if str((c.get("meta") or {}).get("album", "")).casefold() == album.casefold()
                and c.get("song") and os.path.exists(path(c))]
        if mine:
            on = sorted(mine, key=lambda c: ((c.get("meta") or {}).get("track") or 999, c["id"]))
            mode = f"album {album}: {len(on)} track(s) ({', '.join(c['id'] for c in on)})"
        else:
            mode = f"album {album}: no track has a song yet, so the whole rotation plays"
    if mode != ALBUM_MODE[0]:
        ALBUM_MODE[0] = mode
        if mode:
            log("playlist:", mode)
    return on


def path(c):
    return os.path.join(ROOT, c["song"])


def status():
    r = subprocess.run([C, "--json", "live", "status", "--id", ID], capture_output=True, text=True)
    try:
        return json.loads(r.stdout)["data"]
    except (ValueError, KeyError, TypeError):
        return None


def label_of(c):
    return os.path.splitext(os.path.basename(c["song"]))[0]


def entry(c):
    e = {"song": path(c), "label": c["id"]}
    if c.get("meta"):
        e["meta"] = c["meta"]  # the registry's; a song's own meta wins (engines from main 8c95a3d)
    if c.get("passes", 1) != 1:
        e["passes"] = c["passes"]
    return e


def key(label, source, passes):
    return (label, source, passes or 1)


YIELDED = {"on": False}


def sync(st):
    """Make the session's playlist the enabled climbs (set it, or apply only what changed). Someone
    else's playlist (an album played from a player: mostly entries the rotation does not have) is left
    alone until it finishes or is cleared."""
    want = [entry(c) for c in climbs()]
    if not want:
        return
    pl = st.get("playlist")
    wanted = [key(e["label"], e["song"], e.get("passes")) for e in want]
    have = [key(x["label"], x["source"], x.get("passes")) for x in (pl or {}).get("entries", [])]
    # The rotation's own playlist (repeating, every entry an enabled climb) is never "another playlist", even when
    # the album/solo filter now wants far fewer entries: apply the change (a repeating rotation never finishes).
    mine = {key(e["label"], e["song"], e.get("passes")) for e in (entry(c) for c in enabled())}
    ours = bool(have) and bool(pl.get("repeat")) and all(h in mine for h in have)
    if have and not pl.get("finished") and not ours and sum(h in wanted for h in have) * 2 < len(have):
        # A once-through album on its last track: the rotation follows it (no replay, no gap);
        # the next sync then sees the rotation and drops the album's entries.
        cur = pl.get("current")
        if not pl.get("repeat") and not pl.get("stop") and cur is not None and cur == len(have) - 1:
            request({"op": "playlist-add", "entries": want})
            request({"op": "playlist-mode", "repeat": True})
            log("playlist: the album's last track is playing; the rotation follows it")
            return
        if not YIELDED["on"]:
            log(f"playlist: another playlist is playing ({len(have)} entries, e.g. {have[0][0]}): "
                "the rotation waits until it finishes or is cleared")
            YIELDED["on"] = True
        return
    if YIELDED["on"]:
        log("playlist: the other playlist is done; back to the rotation")
        YIELDED["on"] = False
    if not pl or not pl.get("entries") or pl.get("finished"):
        # Start after what is playing or queued now (the old driver queued one at a time).
        now = [q.lstrip("▶ ") for q in (st.get("queue") or [])] or [str(st.get("label", "")).lstrip("▶ ")]
        ids = [e["label"] for e in want]
        at = max((ids.index(x) for x in now if x in ids), default=-1)
        start = (at + 1) % len(want)
        request({"op": "playlist-set", "entries": want, "start": start, "repeat": True, "shuffle": False})
        log(f"playlist set: {len(want)} climbs, starting with {want[start]['label']} (after the queue)")
        return
    if have == wanted:
        return
    for i in reversed(range(len(have))):
        if have[i] not in wanted:
            request({"op": "playlist-remove", "index": i})
            log(f"playlist: removed {have[i][0]}")
    have = [h for h in have if h in wanted]
    for k, (w, e) in enumerate(zip(wanted, want)):
        if w not in have:
            at = min(k, len(have))
            request({"op": "playlist-add", "entries": [e], "at": at})
            have.insert(at, w)
            log(f"playlist: added {e['label']} at {at + 1}")


def main():
    log(f"playlist driver up (binary {C}, groove {ID}; the session's native playlist)")
    last_under = None
    while True:
        st = status()
        if st:
            u = st.get("underruns", 0)
            if last_under is not None and u > last_under:
                log(f"underruns +{u - last_under} (total {u}); host load {open('/proc/loadavg').read().split()[:3]}, groove load {st.get('load') or 0:.2f}")
            last_under = u
            try:
                sync(st)
            except (OSError, RuntimeError, ValueError) as e:
                log("playlist sync failed:", e)
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
