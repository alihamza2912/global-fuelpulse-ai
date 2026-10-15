#!/usr/bin/env bash
# ==============================================================================
# Global FuelPulse AI — Application Startup Script
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "=========================================================="
echo "🚀 Starting Global FuelPulse AI Intelligence Platform"
echo "Project Directory: $PROJECT_DIR"
echo "=========================================================="

# Select Python binary (miniconda or virtualenv or system python)
if [ -f "/opt/miniconda3/bin/streamlit" ]; then
    STREAMLIT_BIN="/opt/miniconda3/bin/streamlit"
elif [ -f "$PROJECT_DIR/.venv/bin/streamlit" ]; then
    STREAMLIT_BIN="$PROJECT_DIR/.venv/bin/streamlit"
else
    STREAMLIT_BIN="streamlit"
fi

export PYTHONPATH="$PROJECT_DIR"

echo "Using Streamlit: $STREAMLIT_BIN"
exec "$STREAMLIT_BIN" run "$PROJECT_DIR/app.py" --server.port 8501 --server.address 0.0.0.0
