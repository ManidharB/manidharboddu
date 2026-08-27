JOBHUNTERX CONTINUOUS SEARCH ENGINE
===================================

This edition has NO 7-day lifetime or expiry.

How it works
------------
1. The first continuous cycle performs a configurable historical backfill (default: 30 days).
2. Later cycles search incrementally with a small overlap window (default: 2 days).
3. The local SQLite database keeps the complete discovery/application history indefinitely.
4. Duplicate jobs are merged instead of re-added every day.
5. Freshness still influences ranking, but older jobs are not automatically rejected unless you explicitly enable Hard-expire older job listings.
6. The background engine keeps running until you pause/stop it.

Recommended default
-------------------
- Search interval: 24 hours
- First-run backfill: 30 days
- Incremental overlap: 2 days
- Score new jobs automatically: ON
- Tailor automatically: OFF until you trust the ranking
- Apply automatically: OFF until verified answers + browser flow are tested

macOS
-----
Open the UI -> Settings & Sources -> Continuous Search -> Install / Start continuous search.

Or run manually:
  ./INSTALL_CONTINUOUS_SEARCH_MAC.sh

Stop background search:
  ./STOP_CONTINUOUS_SEARCH_MAC.sh

Remove the LaunchAgent entirely:
  ./REMOVE_CONTINUOUS_SEARCH_MAC.sh

The background agent requires the Mac to be powered on. If the Mac sleeps, the overlapping incremental window helps catch missed jobs after it wakes.
