from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jobbot.utils import normalize_text, resolve

POSITIVE_PATTERNS = [
    (r"visa sponsorship (?:is )?available", 100, "Explicit visa sponsorship available"),
    (r"(?:will|can|may) sponsor", 95, "Employer states sponsorship may be available"),
    (r"h[- ]?1b (?:visa )?(?:sponsorship|transfer)", 100, "H-1B sponsorship/transfer mentioned"),
    (r"immigration sponsorship", 95, "Immigration sponsorship mentioned"),
    (r"(?:opt|stem opt) (?:candidates|students|holders|welcome|eligible)", 90, "OPT/STEM OPT acceptance signal"),
    (r"cpt (?:candidates|students|holders|welcome|eligible)", 85, "CPT acceptance signal"),
    (r"tn visa", 85, "TN visa mentioned"),
    (r"e[- ]?3 visa", 85, "E-3 visa mentioned"),
]

NEGATIVE_PATTERNS = [
    (r"no (?:visa |immigration )?sponsorship", 0, "Posting explicitly says no sponsorship"),
    (r"(?:unable|not able) to (?:provide )?(?:visa |immigration )?sponsor", 0, "Employer says it cannot sponsor"),
    (r"(?:will|does) not (?:provide )?(?:visa |immigration )?sponsor", 0, "Employer says it will not sponsor"),
    (r"must not require (?:employment |visa )?sponsorship", 0, "Must not require sponsorship"),
    (r"without (?:current or future )?(?:visa |immigration )?sponsorship", 5, "Work authorization required without sponsorship"),
    (r"not (?:eligible|available) for (?:visa |immigration )?sponsorship", 0, "Role not eligible for sponsorship"),
    (r"sponsorship (?:is )?not available", 0, "Sponsorship not available"),
]

CITIZENSHIP_PATTERNS = [
    r"u\.?s\.? citizenship (?:is )?required",
    r"must be (?:a )?u\.?s\.? citizen",
    r"u\.?s\.? citizens? only",
    r"requires? u\.?s\.? citizenship",
]


@dataclass
class SponsorHistory:
    filings: int = 0
    certified: int = 0
    source: str = ""
    updated_at: str = ""

    @property
    def score(self) -> float:
        n = max(self.certified, self.filings)
        if n >= 500:
            return 95
        if n >= 100:
            return 88
        if n >= 25:
            return 78
        if n >= 5:
            return 68
        if n > 0:
            return 58
        return 45


class SponsorshipIntel:
    def __init__(self, config: dict[str, Any], answers: dict[str, Any]):
        self.config = config
        self.answers = answers
        self.sponsor_cfg = config.get("sponsorship", {}) or {}
        self.history_path = resolve(self.sponsor_cfg.get("history_path", "data/sponsor_history.json"))
        self._history = self._load_history()

    def _load_history(self) -> dict[str, SponsorHistory]:
        if not self.history_path.exists():
            return {}
        try:
            raw = json.loads(self.history_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
        companies = raw.get("companies", raw) if isinstance(raw, dict) else {}
        out: dict[str, SponsorHistory] = {}
        for company, entry in (companies or {}).items():
            if not isinstance(entry, dict):
                continue
            out[self._company_key(company)] = SponsorHistory(
                filings=int(entry.get("filings", 0) or 0),
                certified=int(entry.get("certified", 0) or 0),
                source=str(entry.get("source") or "DOL OFLC LCA"),
                updated_at=str(entry.get("updated_at") or ""),
            )
        return out

    @staticmethod
    def _company_key(company: str) -> str:
        text = normalize_text(company)
        text = re.sub(r"\b(inc|incorporated|llc|ltd|limited|corp|corporation|company|co)\b", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def history_for(self, company: str) -> SponsorHistory:
        key = self._company_key(company)
        if key in self._history:
            return self._history[key]
        # Conservative fuzzy fallback for common legal suffix/name variants.
        best = SponsorHistory()
        for known, hist in self._history.items():
            if key and known and (key == known or key in known or known in key):
                if hist.filings > best.filings:
                    best = hist
        return best

    def candidate_needs_sponsorship(self) -> bool | None:
        raw = self.answers.get("requires_sponsorship_now_or_future")
        if raw is None:
            return None
        text = normalize_text(str(raw))
        if text in {"yes", "y", "true", "1"}:
            return True
        if text in {"no", "n", "false", "0"}:
            return False
        return None

    def analyze(self, job) -> dict[str, Any]:
        text = normalize_text(f"{job.title} {job.description}")
        needs = self.candidate_needs_sponsorship()
        history = self.history_for(job.company)
        positive: list[str] = []
        negative: list[str] = []
        citizenship = False
        explicit_positive_score: float | None = None
        explicit_negative_score: float | None = None

        for pattern, score, reason in POSITIVE_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                positive.append(reason)
                explicit_positive_score = max(explicit_positive_score or 0, float(score))

        for pattern, score, reason in NEGATIVE_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                negative.append(reason)
                explicit_negative_score = min(explicit_negative_score if explicit_negative_score is not None else 100, float(score))

        for pattern in CITIZENSHIP_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                citizenship = True
                negative.append("U.S. citizenship requirement detected")
                explicit_negative_score = 0
                break

        if explicit_negative_score is not None:
            score = explicit_negative_score
            status = "NO_SPONSORSHIP" if not citizenship else "CITIZENSHIP_REQUIRED"
        elif explicit_positive_score is not None:
            score = explicit_positive_score
            status = "SPONSOR_FRIENDLY"
        elif history.filings > 0:
            score = history.score
            status = "HISTORICAL_SPONSOR"
        else:
            score = 50 if needs is not False else 90
            status = "UNCLEAR" if needs is not False else "NO_SPONSORSHIP_NEEDED"

        if needs is False and citizenship is False:
            score = max(score, 90)
            if status in {"UNCLEAR", "HISTORICAL_SPONSOR"}:
                status = "NO_SPONSORSHIP_NEEDED"

        label_map = {
            "SPONSOR_FRIENDLY": "🟢 Sponsor-friendly",
            "HISTORICAL_SPONSOR": "🟡 Historical sponsor",
            "UNCLEAR": "🟠 Sponsorship unclear",
            "NO_SPONSORSHIP": "🔴 No sponsorship",
            "CITIZENSHIP_REQUIRED": "🔴 U.S. citizenship required",
            "NO_SPONSORSHIP_NEEDED": "🟢 Work-auth compatible",
        }
        return {
            "score": round(float(score), 1),
            "status": status,
            "label": label_map.get(status, status),
            "candidate_needs_sponsorship": needs,
            "positive_signals": positive,
            "negative_signals": negative,
            "history": {
                "filings": history.filings,
                "certified": history.certified,
                "score": history.score,
                "source": history.source,
                "updated_at": history.updated_at,
            },
        }

    @staticmethod
    def default_history_payload() -> dict[str, Any]:
        return {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "source": "U.S. Department of Labor OFLC LCA disclosure data",
            "companies": {},
        }
