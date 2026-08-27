JOBHUNTERX OMNI SEARCH
======================

What this version adds
----------------------
1. Structured job APIs: JobsPipe, Adzuna, Jooble, USAJOBS.
2. Omni Web Search: web-wide search across public listings and employer career pages using Brave Search API.
3. Source-specific public-web queries for Indeed, Dice, ZipRecruiter, LinkedIn, Workday/ATS pages, and direct company careers.
4. Public-page hydration: the bot follows results and extracts Schema.org JobPosting data where available.
5. Direct-employer resolution: if an aggregator page cannot be hydrated, a small follow-up search tries to locate the employer's direct career/ATS posting.
6. Self-learning ATS registry: Workday, Greenhouse, Lever, Ashby, SmartRecruiters, and employer career domains are learned automatically and polled directly on later runs.
7. Public company-career crawler: robots-aware, no login/CAPTCHA bypass.
8. Sponsorship intelligence remains active after discovery.

Why this is broader than a single job API
-----------------------------------------
A single job API only sees its own partners/index. Omni Search combines structured APIs, a general web index, direct ATS feeds, and employer sites. It is designed to behave more like a research agent: search broadly, resolve to the direct employer posting, normalize, de-duplicate, score, and apply.

Important boundary
------------------
JobHunterX does not bypass robots.txt, CAPTCHA, MFA, login controls, or anti-bot protections. If a portal blocks public extraction, the bot attempts to locate the direct employer/ATS posting instead.
