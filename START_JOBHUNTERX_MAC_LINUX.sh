#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

NEEDS_INSTALL=0
if [ ! -x ".venv/bin/python" ]; then
  NEEDS_INSTALL=1
fi

if [[ "$(uname -s)" == "Darwin" ]]; then
  MACOS_VERSION="$(sw_vers -productVersion)"
  MACOS_MAJOR="${MACOS_VERSION%%.*}"
  if [[ "$MACOS_MAJOR" -eq 13 && -x ".venv/bin/python" ]]; then
    PW_VERSION="$(.venv/bin/python -c 'import importlib.metadata as m; print(m.version("playwright"))' 2>/dev/null || true)"
    if [[ "$PW_VERSION" != "1.57.0" ]]; then
      echo "macOS 13 detected with incompatible Playwright version: ${PW_VERSION:-not installed}"
      NEEDS_INSTALL=1
    fi
  fi
fi

if [ "$NEEDS_INSTALL" -eq 1 ]; then
  echo "Running JobHunterX compatibility installation..."
  ./install_mac_linux.sh
fi

source .venv/bin/activate
python run_dashboard.py
