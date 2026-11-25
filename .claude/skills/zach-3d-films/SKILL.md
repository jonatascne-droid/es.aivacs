---
name: zach-3d-films
description: "Alias of /zach-d-films (3D cartoon 'what if' explainer in three.js) under the name used in the reel. Use for /zach-3d-films."
---

# /zach-3d-films

This is `/zach-d-films` under another name: the same engine, the same worked example (the armour short, where the arrow hits the plate and his jaw drops) and the same steps.

1. Point at the real skill folder:
   ```bash
   SKILL_DIR=$(python3 -c 'import os,sys;print(os.path.realpath(os.path.join(sys.argv[1],"..","zach-d-films")))' "<base directory of this skill>")
   ```
2. Read `$SKILL_DIR/SKILL.md` and follow it exactly, with that `SKILL_DIR`.

If `$SKILL_DIR/SKILL.md` is missing, the repo was copied without `skills/zach-d-films`. Install the whole repo (see its README).
