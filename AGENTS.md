# AGENTS.md

## Project Overview

**Project Name**: 3DPrinter
**Domain**: 3D Printing & Parametric CAD Engineering (FreeCAD Python scripts, mechanical assemblies, and CAD models).
**Primary Tools**: FreeCAD 1.1+ (`freecadcmd` / `/Applications/FreeCAD.app`), Python 3.11+, OpenSCAD.

---

## Startup Workflow

Before writing code:

1. **Confirm working directory**: Run `pwd` to confirm you are in the project root.
2. **Read this file completely**: Understand the project rules and definition of done.
3. **Run `./init.sh`**: Verify the environment and baseline checks pass.
4. **Read `feature_list.json`**: Inspect feature statuses and pick the single active feature.
5. **Read `progress.md`**: Review the current verified state and notes from the previous session.
6. **Review recent git history**: Run `git log --oneline -5` to understand recent commits.

> [!IMPORTANT]
> If baseline verification fails during startup, repair the baseline before taking on any new feature scope.

---

## Working Rules

- **One feature at a time**: Pick exactly one unfinished feature (`not_started` or `in_progress`) from `feature_list.json`. Never work on multiple features concurrently.
- **Verification required**: Never mark a feature as `passing` without running the concrete verification commands and recording actual command output as evidence.
- **Update artifacts before handoff**: Keep `progress.md` and `feature_list.json` synchronized with actual repository state.
- **Stay in scope**: Modify only the files relevant to the active feature. Do not refactor unrelated modules.
- **Leave clean state**: Ensure that at the end of your session, the repository can be cleanly initialized by running `./init.sh`.

---

## Required Artifacts

- `init.sh` — Standard startup script and baseline verification entrypoint.
- `feature_list.json` — Machine-readable feature backlog and source of truth for task progress.
- `progress.md` — Human- and agent-readable session continuity log.
- `scripts/verify.sh` — Test and verification execution suite.
- `clean-state-checklist.md` — Session exit checklist.
- `session-handoff.md` — Detailed inter-session handoff documentation.
- `evaluator-rubric.md` — Quality evaluation scorecard for deliverables.

---

## Definition of Done

A feature is considered done only when ALL of the following criteria are satisfied:

- [ ] Target behavior/CAD model is completely implemented.
- [ ] Required verification commands ran successfully with 0 errors.
- [ ] Verification command output is recorded in `feature_list.json` under `evidence` and summarized in `progress.md`.
- [ ] Repository remains cleanly restartable via `./init.sh`.
- [ ] No uncommitted scratch files or temporary debug code are left behind.

---

## Verification Commands

```bash
# Standard environment initialization and baseline verification
./init.sh

# Dedicated verification runner (syntax, imports, headless CAD recompute)
./scripts/verify.sh

# Python syntax compilation check
python3 -m compileall -q drawing/

# Headless FreeCAD script verification (when FreeCAD is installed)
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd drawing/src/shoe.py
```

---

## End of Session Routine

Before concluding the session:

1. Run `./scripts/verify.sh` to confirm everything passes.
2. Update `feature_list.json` status to `passing` (or `blocked` if impeded) and record output evidence.
3. Update `progress.md` with session summary, files modified, and next best steps.
4. Review against `clean-state-checklist.md`.
5. Commit clean changes to git with a descriptive message.
