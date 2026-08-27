#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "JobHunterX installer"

# Detect macOS version. Playwright 1.57.0 still includes Chromium downloads
# for macOS 13 arm64; newer Playwright releases require newer macOS versions.
if [[ "$(uname -s)" == "Darwin" ]]; then
  MACOS_VERSION="$(sw_vers -productVersion)"
  MACOS_MAJOR="${MACOS_VERSION%%.*}"
  echo "Detected macOS ${MACOS_VERSION}"
else
  MACOS_MAJOR="0"
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [[ "$(uname -s)" == "Darwin" && "$MACOS_MAJOR" -eq 13 ]]; then
  echo "macOS 13 detected: forcing Playwright 1.57.0 for Apple Silicon/Intel compatibility..."
  python -m pip install --force-reinstall "playwright==1.57.0"
fi

python -m playwright install chromium
python -m jobbot.cli doctor || true

echo
 echo "Installation complete. Start JobHunterX with:"
 echo "  ./START_JOBHUNTERX_MAC_LINUX.sh"
