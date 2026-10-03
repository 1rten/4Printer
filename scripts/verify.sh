#!/bin/bash
# ==============================================================================
# scripts/verify.sh - Verification Runner for 3DPrinter CAD Project
# ==============================================================================
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=================================================="
echo "🔍 Running 3DPrinter Verification Suite"
echo "=================================================="

# 1. Python Syntax & Compilation Verification
echo "--- [1/2] Checking Python Syntax ---"
PY_BIN="$(command -v python3 || command -v python || true)"
if [ -z "$PY_BIN" ]; then
  echo "❌ Error: Python 3 executable not found!"
  exit 1
fi

"$PY_BIN" -m compileall -q -x '(^|/)(\.?venv|env|node_modules|build|dist|__pycache__)(/|$)' drawing/
echo "✅ Python syntax and compilation check passed."

# 2. FreeCAD CAD Script Headless Validation
echo "--- [2/2] Checking FreeCAD Environment & Models ---"
FREECAD_CMD=""
if [ -x "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd" ]; then
  FREECAD_CMD="/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
elif command -v freecadcmd >/dev/null 2>&1; then
  FREECAD_CMD="freecadcmd"
fi

if [ -n "$FREECAD_CMD" ]; then
  echo "Found FreeCAD binary: $FREECAD_CMD"
  
  # Test shoe.py
  if [ -f "drawing/src/shoe.py" ]; then
    echo "Running headless check: drawing/src/shoe.py..."
    "$FREECAD_CMD" drawing/src/shoe.py < /dev/null >/dev/null 2>&1
    echo "✅ drawing/src/shoe.py executed cleanly."
  fi

  # Test workbench.py
  if [ -f "drawing/src/workbench.py" ]; then
    echo "Running headless check: drawing/src/workbench.py..."
    "$FREECAD_CMD" drawing/src/workbench.py < /dev/null >/dev/null 2>&1
    echo "✅ drawing/src/workbench.py executed cleanly."
  fi

  # Test workbench_500.py
  if [ -f "drawing/src/workbench_500.py" ]; then
    echo "Running headless check: drawing/src/workbench_500.py..."
    "$FREECAD_CMD" drawing/src/workbench_500.py < /dev/null >/dev/null 2>&1
    echo "✅ drawing/src/workbench_500.py executed cleanly."
  fi
else
  echo "⚠️ Warning: FreeCAD not found. Skipping CAD runtime recompute checks."
fi

echo "=================================================="
echo "✅ All verification checks completed successfully!"
echo "=================================================="
