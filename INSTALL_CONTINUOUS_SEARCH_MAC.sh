#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(pwd)"
if [ ! -x "$ROOT/.venv/bin/python" ]; then
  echo "Virtual environment not installed. Running installer first..."
  ./install_mac_linux.sh
fi
PLIST="$HOME/Library/LaunchAgents/com.jobhunterx.continuous.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/logs"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.jobhunterx.continuous</string>
  <key>ProgramArguments</key><array>
    <string>$ROOT/.venv/bin/python</string>
    <string>$ROOT/continuous_runner.py</string>
    <string>--daemon</string>
  </array>
  <key>WorkingDirectory</key><string>$ROOT</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$ROOT/logs/continuous_search.out.log</string>
  <key>StandardErrorPath</key><string>$ROOT/logs/continuous_search.err.log</string>
</dict></plist>
EOF
launchctl bootout "gui/$(id -u)" "$PLIST" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/com.jobhunterx.continuous"
echo "JobHunterX continuous search installed and started."
echo "It will keep running according to Settings & Sources -> Continuous Search."
