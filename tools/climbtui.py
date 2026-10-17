#!/usr/bin/env python3
"""Climbs TUI: the climb queue at a glance, and what is climbable.

  python3 tools/climbtui.py        (or `climb.py tui`)

Rows are grouped by album (in track order), then the other climbs. Each shows whether it is climbable
(☑: `climb.py next` can pick it), whether it is in the groove's playlist (▶), status, rounds, best score,
the last round and who is on it now. The pane below shows the selected climb's latest notes.

Keys: ↑↓/jk move · PgUp/PgDn · space climbable · p playlist · a whole album climbable · f focus this album
(climb only it) · F focus off · n note · + / - priority · / filter · r reload · q quit. Mouse: click a row,
click ☑ or ▶ to toggle, wheel to scroll. Changes save at once (under the registry lock) and commit in the
background, like climb.py; the list reloads every few seconds as agents work."""
import curses
import importlib.util
import os
import queue
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("climb", os.path.join(HERE, "climb.py"))
climb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(climb)

QUEUED = climb.QUEUED
NO_GIT = "--no-git" in sys.argv


def album(c):
    return (c.get("meta") or {}).get("album")


def climbable(c):
    return c["status"] in QUEUED and not c.get("oob")


class Model:
    """The registry as rows, and every edit the TUI makes (testable without curses)."""

    def __init__(self):
        self.commits = queue.Queue()
        self.saving = 0
        self.message = ""
        self.filter = ""
        self.reload()

    def reload(self):
        self.reg = climb.load()
        self.starts = climb.starts()
        self.weights = climb.weights(self.reg, climb.whoami([]))

    # ── rows ────────────────────────────────────────────────────────────────────────
    def rows(self):
        """[(kind, value)]: ("album", name) headers and ("climb", climb) rows."""
        cs = [c for c in self.reg["climbs"] if c.get("status") != "dropped"]
        if self.filter:
            f = self.filter.lower()
            cs = [c for c in cs if f in " ".join(str(x) for x in (c["id"], c.get("reference"), c.get("genre"),
                                                                  album(c), c["status"])).lower()]
        albums = {}
        for c in cs:
            if album(c):
                albums.setdefault(album(c), []).append(c)
        out = []
        for name in sorted(albums, key=lambda n: (n != self.reg.get("focus"), n.lower())):
            out.append(("album", name))
            out += [("climb", c) for c in sorted(albums[name], key=lambda c: (c["meta"].get("track") or 999, c["id"]))]
        rest = [c for c in cs if not album(c)]
        if rest:
            out.append(("album", None))
            out += [("climb", c) for c in sorted(rest, key=lambda c: (not climbable(c), -(c.get("best") or {}).get("score", 0) if c.get("best") else 0, c["id"]))]
        return out

    def album_summary(self, name):
        cs = [c for c in self.reg["climbs"] if album(c) == name]
        meta = (cs[0].get("meta") or {}) if cs else {}
        up = sum(1 for c in cs if c.get("best"))
        on = sum(1 for c in cs if climbable(c))
        bits = [f"{meta.get('artist', '')} ({meta.get('year', '')})".strip(" ()"), f"{up}/{len(cs)} set up",
                f"{on} climbable", "FOCUS" if self.reg.get("focus") == name else ""]
        return " · ".join(b for b in bits if b)

    def working(self, c):
        t = time.time()
        return sorted({s["who"] for s in self.starts if s["id"] == c["id"] and t - s.get("t", 0) < climb.SPREAD})

    # ── edits ───────────────────────────────────────────────────────────────────────
    def _edit(self, ids, fn, msg, extra_paths=()):
        with climb.registry() as reg:
            for cid in ids:
                fn(climb.find(reg, cid), reg)
        self.reload()
        self.saving += 1
        self.commits.put((["climbs.json", *extra_paths], msg))

    def toggle_climbable(self, cid):
        c = climb.find(self.reg, cid)
        on = climbable(c)

        def fn(c, _):
            if on:
                c["status"] = "paused"
            else:
                c["status"] = "active" if c["rounds"] else "requested"
                c.pop("oob", None)
            c.pop("paused_by", None)
        self._edit([cid], fn, f"climbs: {cid} {'paused' if on else 'climbable'} (tui)")

    def toggle_playlist(self, cid):
        c = climb.find(self.reg, cid)
        if not c.get("enabled") and not c.get("best"):
            self.message = f"{cid} has no kept version yet: it joins the playlist with its first"
            return

        def fn(c, _):
            c["enabled"] = not c.get("enabled")
        self._edit([cid], fn, f"climbs: {cid} {'off' if c.get('enabled') else 'on'} the playlist (tui)")

    def toggle_album(self, name):
        cs = [c for c in self.reg["climbs"] if album(c) == name]
        on = any(climbable(c) for c in cs)

        def fn(c, _):
            if on and c["status"] in QUEUED:
                c["status"] = "paused"
            elif not on and c["status"] == "paused":
                c["status"] = "active" if c["rounds"] else "requested"
            c.pop("paused_by", None)
        self._edit([c["id"] for c in cs], fn, f"climbs: album {name} {'paused' if on else 'climbable'} (tui)")

    def focus(self, name):
        """Climb only this album (as `climb.py focus`): other queued climbs pause, marked."""
        def fn(c, reg):
            mine = album(c) == name
            if mine and c.get("paused_by") == "focus":
                c["status"] = "active" if c["rounds"] else "requested"
                c.pop("paused_by", None)
            elif not mine and c["status"] in QUEUED:
                c["status"], c["paused_by"] = "paused", "focus"
            reg["focus"] = name
        self._edit([c["id"] for c in self.reg["climbs"]], fn, f"climbs: focus {name} (tui)")

    def unfocus(self):
        def fn(c, reg):
            if c.get("paused_by") == "focus":
                c["status"] = "active" if c["rounds"] else "requested"
                c.pop("paused_by", None)
            reg.pop("focus", None)
        self._edit([c["id"] for c in self.reg["climbs"]], fn, "climbs: focus off (tui)")

    def priority(self, cid, delta):
        def fn(c, _):
            c["priority"] = round(max(0.1, float(c.get("priority", 1)) + delta), 2)
        self._edit([cid], fn, f"climbs: {cid} priority {'+' if delta > 0 else ''}{delta} (tui)")

    def note(self, cid, text):
        import json
        with climb.registry() as reg:
            c = climb.find(reg, cid)
            h = {"round": c["rounds"], "at": climb.now_iso(), "who": climb.whoami([]), "note": text, "steer": True}
            os.makedirs(climb.HIST, exist_ok=True)
            with open(os.path.join(climb.HIST, f"{cid}.jsonl"), "a") as f:
                f.write(json.dumps(h, ensure_ascii=False) + "\n")
        self.reload()
        self.saving += 1
        self.commits.put((["climbs.json", f"climbs/{cid}.jsonl"], f"climbs: {cid} note: {text[:60]}"))

    def committer(self):
        """Commit edits in order, off the UI thread (git can take seconds)."""
        while True:
            paths, msg = self.commits.get()
            ok = climb.commit(paths, msg, ["--no-git"] if NO_GIT else [])
            self.saving -= 1
            if not ok:
                self.message = f"NOT committed: {msg} (fix git, then edit again)"


# ── the view ──────────────────────────────────────────────────────────────────────

def fmt_row(m, c, w):
    meta = c.get("meta") or {}
    best = (c.get("best") or {}).get("score")
    hist = climb.history(c["id"])
    last = hist[-1] if hist else None
    now = m.working(c)
    track = f"{meta['track']:>2} " if meta.get("track") else "   "
    name = meta.get("title") or c["id"]
    tail = " ".join(x for x in [f"{climb.age(last['at'])} ago {last['who']}" if last else "",
                                f"now: {', '.join(now)}" if now else ""] if x)
    left = f" {'☑' if climbable(c) else '☐'} {'▶' if c.get('enabled') else '·'} {track}{name}"
    status = c["status"] + (" (focus)" if c.get("paused_by") == "focus" else "") + (" oob" if c.get("oob") else "")
    right = f"{status:16} {c['rounds']:>4}  {best if best is not None else '—':>7}  {tail}"
    pad = max(1, min(44, w - len(right) - 2) - len(left))
    return (left + " " * pad + right)[: w - 1]


def details(m, c, w, h):
    meta = c.get("meta") or {}
    best = c.get("best") or {}
    lines = [f"{c['id']} — {c.get('reference', '')}"
             + (f"  ·  {meta.get('album')} #{meta.get('track')}" if meta.get("album") else ""),
             f"best {best.get('score', '—')} ({best.get('version', '—')}) · {c['rounds']} rounds · priority "
             f"{c.get('priority', 1)} · odds {m.weights.get(c['id'], 0) / (sum(m.weights.values()) or 1):.0%} · "
             f"{c.get('genre') or 'genre unset'}"]
    hist = climb.history(c["id"])
    nxt = next((x["next"] for x in reversed(hist) if x.get("next")), None)
    for x in reversed(hist[-(h - 3):]):
        tag = "NOTE" if x.get("steer") else f"r{x['round']}"
        sc = f" {x['score']}" if x.get("score") is not None else ""
        lines.append(f"{tag} {climb.age(x['at'])} {x['who']}{sc}{' kept' if x.get('kept') else ''}: {x['note']}")
    if nxt:
        lines.insert(2, f"next: {nxt}")
    return [l[: w - 1] for l in lines[:h]]


def prompt(scr, label):
    h, w = scr.getmaxyx()
    curses.echo()
    curses.curs_set(1)
    scr.move(h - 1, 0)
    scr.clrtoeol()
    scr.addstr(h - 1, 0, label[: w - 1], curses.A_BOLD)
    try:
        s = scr.getstr(h - 1, min(len(label), w - 2), 400).decode(errors="replace")
    finally:
        curses.noecho()
        curses.curs_set(0)
    return s.strip()


def run(scr):
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.use_default_colors()
    for i, fg in enumerate((curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_YELLOW, curses.COLOR_RED), 1):
        curses.init_pair(i, fg, -1)
    scr.timeout(500)
    m = Model()
    threading.Thread(target=m.committer, daemon=True).start()
    sel, top, last_reload = 0, 0, time.time()
    selected_id = None
    while True:
        if time.time() - last_reload > 4:
            m.reload()
            last_reload = time.time()
        rows = m.rows()
        ids = [r[1]["id"] if r[0] == "climb" else None for r in rows]
        if selected_id in ids:
            sel = ids.index(selected_id)
        sel = max(0, min(sel, len(rows) - 1))
        while rows and rows[sel][0] != "climb" and sel < len(rows) - 1:
            sel += 1
        h, w = scr.getmaxyx()
        list_h = max(3, h - 10)
        top = min(max(top, sel - list_h + 1), sel) if rows else 0
        scr.erase()
        focus = m.reg.get("focus")
        head = f" Climbs — {sum(1 for c in m.reg['climbs'] if climbable(c))} climbable"
        head += f" · focus: {focus}" if focus else ""
        head += f" · filter: {m.filter}" if m.filter else ""
        head += " · saving…" if m.saving else ""
        scr.addstr(0, 0, head[: w - 1], curses.A_BOLD | curses.color_pair(1))
        cols = "   ☑ climbable  ▶ playlist" + " " * 20 + "status            rounds    best  last round"
        scr.addstr(1, 0, cols[: w - 1], curses.A_DIM)
        for y, (kind, v) in enumerate(rows[top: top + list_h]):
            i = top + y
            if kind == "album":
                text = f" {v} — {m.album_summary(v)}" if v else " Other climbs"
                scr.addstr(2 + y, 0, text[: w - 1], curses.A_BOLD | curses.color_pair(3 if v == focus else 1))
                continue
            attr = curses.A_REVERSE if i == sel else 0
            if not climbable(v):
                attr |= curses.A_DIM
            scr.addstr(2 + y, 0, fmt_row(m, v, w), attr)
        cur = rows[sel][1] if rows and rows[sel][0] == "climb" else None
        selected_id = cur["id"] if cur else None
        y0 = 2 + list_h
        scr.hline(y0, 0, curses.ACS_HLINE, w - 1)
        if cur:
            for k, line in enumerate(details(m, cur, w, h - y0 - 3)):
                scr.addstr(y0 + 1 + k, 0, line, curses.A_BOLD if k == 0 else 0)
        keys = " space climbable · p playlist · a album · f focus album · F focus off · n note · +/- priority · / filter · q quit"
        scr.addstr(h - 1, 0, (m.message or keys)[: w - 1], curses.color_pair(4) if m.message else curses.A_DIM)
        scr.refresh()
        k = scr.getch()
        if k == -1:
            continue
        m.message = ""
        if k in (ord("q"), 27):
            if m.saving:
                m.message = "saving… (q again to quit anyway)"
                if scr.getch() not in (ord("q"), 27):
                    continue
            return
        if k in (curses.KEY_DOWN, ord("j")):
            sel = next((i for i in range(sel + 1, len(rows)) if rows[i][0] == "climb"), sel)
        elif k in (curses.KEY_UP, ord("k")):
            sel = next((i for i in range(sel - 1, -1, -1) if rows[i][0] == "climb"), sel)
        elif k == curses.KEY_NPAGE:
            sel = min(len(rows) - 1, sel + list_h)
        elif k == curses.KEY_PPAGE:
            sel = max(0, sel - list_h)
        elif k in (curses.KEY_HOME, ord("g")):
            sel = 0
        elif k in (curses.KEY_END, ord("G")):
            sel = len(rows) - 1
        elif k == ord("r"):
            m.reload()
        elif k == ord("/"):
            m.filter = prompt(scr, "filter: ")
        elif k == ord("F"):
            m.unfocus()
        elif cur and k == ord(" "):
            m.toggle_climbable(cur["id"])
        elif cur and k == ord("p"):
            m.toggle_playlist(cur["id"])
        elif cur and k == ord("a"):
            if album(cur):
                m.toggle_album(album(cur))
            else:
                m.message = "not on an album"
        elif cur and k == ord("f"):
            if album(cur):
                m.focus(album(cur))
            else:
                m.message = "not on an album"
        elif cur and k in (ord("+"), ord("=")):
            m.priority(cur["id"], 0.5)
        elif cur and k == ord("-"):
            m.priority(cur["id"], -0.5)
        elif cur and k == ord("n"):
            t = prompt(scr, f"note for {cur['id']}: ")
            if t:
                m.note(cur["id"], t)
        elif k == curses.KEY_MOUSE:
            try:
                _, mx, my, _, bstate = curses.getmouse()
            except curses.error:
                continue
            if bstate & getattr(curses, "BUTTON4_PRESSED", 0):
                sel = max(0, sel - 3)
            elif bstate & getattr(curses, "BUTTON5_PRESSED", 1 << 21):
                sel = min(len(rows) - 1, sel + 3)
            elif 2 <= my < 2 + list_h and top + my - 2 < len(rows):
                i = top + my - 2
                if rows[i][0] == "climb":
                    sel = i
                    cid = rows[i][1]["id"]
                    if mx in (1, 2):
                        m.toggle_climbable(cid)
                    elif mx in (3, 4):
                        m.toggle_playlist(cid)
                elif rows[i][1]:
                    m.toggle_album(rows[i][1])
        if rows and 0 <= sel < len(rows) and rows[sel][0] == "climb":
            selected_id = rows[sel][1]["id"]


def main():
    os.environ.setdefault("ESCDELAY", "25")
    curses.wrapper(run)


if __name__ == "__main__":
    main()
