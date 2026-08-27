#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OLD="${1:-}"
if [[ -z "$OLD" ]]; then
  echo "Paste the path to your OLD JobHunterX folder, then press Enter:"
  read -r OLD
fi
"$HERE/MIGRATE_FROM_OLD_MAC.sh" "$OLD"
exec "$HERE/START_JOBHUNTERX_MAC_LINUX.sh"
