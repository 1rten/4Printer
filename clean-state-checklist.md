# Clean State Checklist

Before completing any agent session or declaring work finished, verify the following:

- [ ] **Startup Path Verification**: `./init.sh` executes cleanly from repository root with exit code 0.
- [ ] **Verification Path Verification**: `./scripts/verify.sh` executes all checks without errors.
- [ ] **State Synchronization**: `progress.md` reflects current verified state, files modified, and next best action.
- [ ] **Feature List Integrity**: `feature_list.json` reflects actual state:
  - Only features with executed verification and logged output evidence are marked as `passing`.
  - At most one feature is marked `in_progress`.
- [ ] **No Hidden Work**: No uncommitted scratch files, commented-out debug code, or half-finished steps left undocumented.
- [ ] **Restartability**: The next session or human engineer can immediately resume without manual repairs.
