# CLAUDE.md - Agent Instructions for 3DPrinter

## Project Information
- **Domain**: 3D Printing & Parametric CAD Engineering (FreeCAD Python scripts, OpenSCAD, and equipment layouts).
- **Core Environment**: macOS, Python 3.11+, FreeCAD 1.1+ (`/Applications/FreeCAD.app`).

## Startup Sequence
1. Confirm directory: `pwd`
2. Check baseline health: `./init.sh`
3. Inspect active features: Read `feature_list.json`
4. Inspect current status & history: Read `progress.md` and `git log --oneline -5`

## Execution Rules
- Work on exactly **ONE** feature at a time from `feature_list.json`.
- Do not claim a feature is complete without executing the verification command and recording real output into `feature_list.json` evidence.
- Maintain headless safety: FreeCAD scripts should run in both GUI and headless mode without raising `AttributeError` when `ViewObject` is `None`.
- Update `progress.md` and `feature_list.json` before ending the session.
- Keep repository clean and restartable from `./init.sh`.

## Essential Commands
- `./init.sh`: Environment initialization and baseline check.
- `./scripts/verify.sh`: Run full automated verification suite.
- `python3 -m compileall -q drawing/`: Syntax validation across all drawing scripts.
