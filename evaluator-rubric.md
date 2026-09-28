# Evaluator Rubric

Use this rubric after implementation and before final acceptance.

| Category | Question | Score (0-2) | Notes |
| --- | --- | --- | --- |
| **Correctness** | Does the implemented CAD model or code match the requested requirements and physical specifications? |  |  |
| **Verification** | Did the required verification checks actually run (`./scripts/verify.sh` / FreeCAD recompute) with evidence captured? |  |  |
| **Scope discipline** | Did the session modify only files required for the selected feature in `feature_list.json`? |  |  |
| **Reliability** | Does the model recompute cleanly without GUI crashes or headless exceptions? |  |  |
| **Maintainability** | Are parametric variables well-named, clear, and documented for the next engineer? |  |  |
| **Handoff readiness** | Can a fresh session immediately continue work relying only on repository artifacts? |  |  |

## Scoring Guide
- **2 (Strong)**: Fully satisfies criteria with documented proof.
- **1 (Partial)**: Partially satisfies; minor follow-ups or manual steps needed.
- **0 (Failed)**: Did not satisfy; errors or unverified assumptions present.

## Verdict
- [ ] **Accept** (Score >= 10, no 0s)
- [ ] **Revise** (Minor issues requiring specific fixes)
- [ ] **Block** (Fundamental issues or broken baseline)

## Follow-up Action
- Missing evidence:
- Required fixes:
- Next review trigger:
