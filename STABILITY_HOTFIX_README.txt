JobHunterX Discovery Stability Hotfix

This build restores the last known-good job discovery path while retaining:
- Adaptive role intelligence
- Continuous search
- Sponsorship intelligence
- Google Jobs / SerpAPI support
- Multi-source API configuration
- Direct ATS learning
- Windows + macOS launchers

What changed from the Discovery Mesh build:
- Normal Find Jobs no longer performs the heavy generic ATS-page sweep.
- Normal Find Jobs no longer performs the expanded sitemap crawl introduced in the last build.
- Brave query budget and employer-resolution budget are reduced for predictable response times.
- Known Workday/Greenhouse/Lever/Ashby/SmartRecruiters sources still run.
- Aggregators and Google Jobs still run when configured.

This is a rollback of the risky discovery path, not a rollback of Adaptive Roles or Sponsorship Intelligence.
