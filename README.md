# 3DPrinter & Heavy Workstation CAD

Engineering repository for parametric 3D printing equipment workstations, assemblies, and custom parts modeled in FreeCAD and OpenSCAD.

## 🛠️ Workstation Highlights (V19.2)

- **Envelope**: 1400 × 800 × 700 mm heavy-duty 4040 aluminum extrusion frame.
- **Hardware Integration**:
  - Bambu Lab P1S 3D printer
  - Bambu AMS multi-color system
  - xTool S1 enclosed diode laser cutter
  - LightMake L4 industrial equipment
  - Canon MF113w multifunction printer
- **Dual-Compartment Architecture**: Left bay 700 mm with dual acrylic drawers & pull-out tray; right bay 580 mm dedicated for P1S.

---

## 🤖 AI Harness Engineering

This repository implements the [Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/en/) standard to enable reliable autonomous pair-programming and development.

### Core Harness Artifacts

| File | Purpose |
|---|---|
| [`AGENTS.md`](file:///Users/1rten/Documents/workspace/3DPrinter/AGENTS.md) | Agent startup workflow, non-negotiable rules, and definition of done |
| [`CLAUDE.md`](file:///Users/1rten/Documents/workspace/3DPrinter/CLAUDE.md) | Claude Code / agent instructions format |
| [`init.sh`](file:///Users/1rten/Documents/workspace/3DPrinter/init.sh) | Standard environment initialization and baseline verification runner |
| [`scripts/verify.sh`](file:///Users/1rten/Documents/workspace/3DPrinter/scripts/verify.sh) | Full test and verification execution suite |
| [`feature_list.json`](file:///Users/1rten/Documents/workspace/3DPrinter/feature_list.json) | Machine-readable backlog and single source of truth for task state |
| [`progress.md`](file:///Users/1rten/Documents/workspace/3DPrinter/progress.md) | Persistent session continuity log across agent conversations |
| [`clean-state-checklist.md`](file:///Users/1rten/Documents/workspace/3DPrinter/clean-state-checklist.md) | End-of-session verification checklist |
| [`evaluator-rubric.md`](file:///Users/1rten/Documents/workspace/3DPrinter/evaluator-rubric.md) | 6-dimension evaluation rubric for quality gating |
| [`docs/HARDWARE_SPECS.md`](file:///Users/1rten/Documents/workspace/3DPrinter/docs/HARDWARE_SPECS.md) | Physical dimensions and hardware coordinates |
| [`docs/QUALITY.md`](file:///Users/1rten/Documents/workspace/3DPrinter/docs/QUALITY.md) | Codebase health snapshot across CAD domains |

### Quickstart

```bash
# Make scripts executable
chmod +x init.sh scripts/verify.sh

# Run standard environment startup and baseline check
./init.sh

# Run verification suite
./scripts/verify.sh
```
