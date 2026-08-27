JOBHUNTERX DISCOVERY MESH
=========================

This build searches for evidence of a matching job across multiple public discovery lanes, then
tries to resolve the canonical employer/ATS posting. It is designed to grow its own source network
over time rather than depend on one aggregator.

DISCOVERY LANES
---------------
1. Structured discovery: JobsPipe, Adzuna, Jooble, USAJOBS.
2. Omni web index: portal-specific and ATS-specific searches through Brave Search.
3. Optional Google Jobs index through SerpAPI.
4. Direct ATS polling: Workday, Greenhouse, Lever, Ashby, SmartRecruiters.
5. Learned ATS pages: Workable, iCIMS, Oracle/Taleo, SuccessFactors, Paylocity, Jobvite,
   Dayforce and BrassRing public pages when discovered.
6. Company career mesh: robots-aware careers/jobs pages + sitemap URLs + JobPosting JSON-LD.

SELF-LEARNING
-------------
Every discovery run can teach JobHunterX new employer domains and public ATS board identifiers.
Those are saved in data/ats_registry.json and polled on future cycles.

ROTATING COVERAGE
-----------------
Adaptive roles are rotated across continuous-search cycles using data/discovery_state.json. This
prevents every daily run from spending its entire search budget on the same first few role titles.

SAFETY
------
LinkedIn/Indeed/Dice/ZipRecruiter jobs can remain visible if public hydration is blocked, but
unattended application automation waits until a direct employer/ATS URL is available by default.
The bot does not bypass CAPTCHA, MFA, login gates, robots exclusions, or legal attestations.
