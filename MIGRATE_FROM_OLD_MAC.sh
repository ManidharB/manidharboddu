#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
OLD="${1:-}"
if [[ -z "$OLD" ]]; then
  echo "Paste the path to your OLD JobHunterX folder, then press Enter:"
  read -r OLD
fi
OLD="${OLD/#\~/$HOME}"
if [[ ! -d "$OLD" ]]; then
  echo "Old JobHunterX folder not found: $OLD"
  exit 1
fi

echo "Migrating your local state into: $HERE"
mkdir -p "$HERE/profile" "$HERE/data"
for f in master_resume.docx candidate_profile.json application_answers.json; do
  [[ -f "$OLD/profile/$f" ]] && cp -f "$OLD/profile/$f" "$HERE/profile/$f"
done
for f in source_secrets.json jobbot.sqlite3 sponsor_history.json ats_registry.json; do
  [[ -f "$OLD/data/$f" ]] && cp -f "$OLD/data/$f" "$HERE/data/$f"
done
if [[ -d "$OLD/data/browser_profile" ]]; then
  rm -rf "$HERE/data/browser_profile"
  cp -R "$OLD/data/browser_profile" "$HERE/data/browser_profile"
fi

echo "Migration complete. Your resume, profile, API keys, history, sponsor data, ATS registry, and browser profile were copied when present."
echo "Now run: ./START_JOBHUNTERX_MAC_LINUX.sh"
