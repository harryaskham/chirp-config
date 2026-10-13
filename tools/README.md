# chirp tools (user)

- `evolve.py` — keeps the live `groove` session evolving: every loop pass is a generated song
  (`songs/form-1|2.yaml`) with a form that suits its style (rock / edm / classical), built from
  the tempo-inheriting parts library, with a main motif and hook that return, transitions, and a
  lifted final section. A song identity persists for 2–3 passes, mutating one element per pass.
  `EVOLVE_STYLE=house python3 evolve.py` starts with a style
  (djent prog-clean poly house garage hardcore acid idm lofi classical doom-ambient).
- `restart-groove.sh SONG [ARRANGEMENT]` — restart `groove` on the current binary with the evolver.

Watch it: `chirp watch` · stop: `chirp stop`.
