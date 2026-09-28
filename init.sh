#!/bin/bash
# ==============================================================================
# init.sh - Standard Initialization & Baseline Verification Script
# ==============================================================================
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

echo "=== 🚀 Initializing 3DPrinter Workspace ==="
echo "Working directory: $REPO_ROOT"

# 1. Environment Detection
PY_BIN="$(command -v python3 || command -v python || true)"
echo "Python binary: ${PY_BIN:-'Not found'}"

if [ -x "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd" ]; then
  echo "FreeCAD binary: /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
elif command -v freecadcmd >/dev/null 2>&1; then
  echo "FreeCAD binary: $(command -v freecadcmd)"
else
  echo "⚠️ FreeCAD binary not found in standard paths."
fi

# 2. Dependency / Virtualenv check
if [ -f "pyproject.toml" ] && command -v uv >/dev/null 2>&1; then
  echo "Checking uv package environment..."
  uv sync --quiet 2>/dev/null || true
fi

# 3. Baseline Verification
echo ""
echo "=== 🧪 Running Baseline Verification ==="
chmod +x ./scripts/verify.sh
./scripts/verify.sh

echo ""
echo "=== ✅ Baseline Verification Passed! ==="
echo "Next steps for Agent:"
echo "1. Read 'feature_list.json' to review active features"
echo "2. Read 'progress.md' for session context and next best action"
echo "3. Pick exactly ONE unfinished feature to work on"
echo "4. Re-run './scripts/verify.sh' and record evidence before marking done"
