# JobHunterX — Discovery Mesh Edition

JobHunterX is a local, UI-first, continuous U.S. job discovery and application assistant. This
edition is built around a **source-agnostic Discovery Mesh**: discover a job anywhere public, learn
the employer source, resolve the direct ATS/career posting where possible, then run resume fit +
sponsorship intelligence before application.

## Start on macOS

```bash
chmod +x *.sh
./START_JOBHUNTERX_MAC_LINUX.sh
```

Open `http://localhost:8501`.

## Start on Windows

Double-click `START_JOBHUNTERX_WINDOWS.bat`.

## Recommended setup

1. **Profile & Answers** — complete verified application answers.
2. **Resume Manager** — confirm the active master DOCX.
3. **Settings & Sources → Targeting** — keep Adaptive role mode enabled.
4. **Settings & Sources → Free APIs** — add available discovery API credentials.
5. **Settings & Sources → Direct ATS + Web** — keep self-learning ATS and sitemap discovery enabled.
6. **Sponsorship Intelligence** — configure work-authorization matching and optional DOL history.
7. **Continuous Search** — enable the background cycle.

## Discovery Mesh

The mesh combines:

- JobsPipe, Adzuna, Jooble and USAJOBS
- Brave-powered OmniSearch across public LinkedIn/Indeed/Dice/ZipRecruiter references, ATS indexes,
  and direct employer career pages
- optional Google Jobs through SerpAPI
- direct Workday, Greenhouse, Lever, Ashby and SmartRecruiters polling
- reusable learned public ATS pages for Workable, iCIMS, Oracle/Taleo, SuccessFactors, Paylocity,
  Jobvite, Dayforce and BrassRing
- robots-aware company sitemap and Schema.org `JobPosting` discovery

Search roles rotate across continuous cycles so the system does not repeatedly spend its entire
query budget on the same titles. `data/ats_registry.json` grows as new employers are learned.

## Application safety

The system keeps unresolved portal jobs visible for coverage, but by default unattended application
automation requires a direct employer/ATS URL. It never bypasses CAPTCHA, MFA, login restrictions,
robots exclusions, or legal attestations, and it does not invent work-authorization answers or
resume experience.

## Tests

```bash
python -m pytest -q
```
