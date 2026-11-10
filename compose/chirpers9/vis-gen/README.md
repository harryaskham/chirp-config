# How the rebuilt Accretion programmes were made

`vis/chirpers9-t2.yaml`, `-t3`, `-t4` and `-t5` keep the sets of the earlier programmes (timed
in seconds, lit by loudness) and rebind every signal to the song. Each script here takes the
earlier programme from this repository's history (the commit named in it) and applies those
edits, each asserted to match exactly once, then writes `/tmp/cv/tNn/tN.yaml`.

They are a record, not a build step: the programmes in `vis/` are the source of truth and may
be edited by hand afterwards. `t1` and `t6` were written directly (no script).

`t8.py` writes t8's programme afresh (its six elements' layers are generated, one orbit each,
read from each element's own lanes as `lane.e3.orb`). `t7` was written directly.
