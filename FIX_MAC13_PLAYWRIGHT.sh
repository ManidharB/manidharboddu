#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "Repairing Playwright for macOS 13 / Apple Silicon..."
if [ ! -x ".venv/bin/python" ]; then
  echo "Virtual environment not found. Running the full installer instead."
  ./install_mac_linux.sh
  exit 0
fi
source .venv/bin/activate
python -m pip install --force-reinstall "playwright==1.57.0"
python -m playwright install chromium
echo
 echo "Repair complete. Launch with:"
 echo "  ./START_JOBHUNTERX_MAC_LINUX.sh"
