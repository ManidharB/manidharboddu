from __future__ import annotations

import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

from jobbot.utils import normalize_text, resolve

DOL_PERFORMANCE_URL = "https://www.dol.gov/agencies/eta/foreign-labor/performance"


def _company_key(value: str) -> str:
    text = normalize_text(value)
    text = re.sub(r"\b(inc|incorporated|llc|ltd|limited|corp|corporation|company|co)\b", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def discover_latest_lca_url(session=requests) -> str:
    response = session.get(DOL_PERFORMANCE_URL, timeout=45)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    candidates: list[tuple[int, int, str]] = []
    for a in soup.find_all("a", href=True):
        href = str(a.get("href") or "")
        label = f"{a.get_text(' ', strip=True)} {href}"
        upper = label.upper()
        if "LCA" not in upper or not re.search(r"DIS.*CLOSURE", upper):
            continue
        if "APPENDIX" in upper or "WORKSITE" in upper:
            continue
        if not href.lower().endswith((".xlsx", ".xls")):
            continue
        fy = re.search(r"FY\s*([0-9]{4})", label, flags=re.IGNORECASE)
        q = re.search(r"Q\s*([1-4])", label, flags=re.IGNORECASE)
        if fy:
            candidates.append((int(fy.group(1)), int(q.group(1)) if q else 4, urljoin(DOL_PERFORMANCE_URL, href)))
    if not candidates:
        raise RuntimeError("Could not locate an LCA disclosure workbook on the DOL OFLC performance page.")
    candidates.sort(reverse=True)
    return candidates[0][2]


def sync_dol_history(output_path: str | Path = "data/sponsor_history.json", session=requests) -> dict:
    url = discover_latest_lca_url(session=session)
    response = session.get(url, timeout=120)
    response.raise_for_status()
    frame = pd.read_excel(io.BytesIO(response.content), engine="openpyxl")
    cols = {str(c).strip().upper(): c for c in frame.columns}
    employer_col = next((cols[k] for k in cols if k in {"EMPLOYER_NAME", "EMPLOYER NAME"}), None)
    status_col = next((cols[k] for k in cols if k in {"CASE_STATUS", "CASE STATUS"}), None)
    if employer_col is None:
        raise RuntimeError("DOL workbook did not contain an EMPLOYER_NAME column.")

    data: dict[str, dict] = {}
    for _, row in frame.iterrows():
        employer = str(row.get(employer_col) or "").strip()
        if not employer or employer.lower() == "nan":
            continue
        key = _company_key(employer)
        if not key:
            continue
        entry = data.setdefault(key, {"display_name": employer, "filings": 0, "certified": 0})
        entry["filings"] += 1
        if status_col is not None:
            status = str(row.get(status_col) or "").upper()
            if "CERTIFIED" in status:
                entry["certified"] += 1

    stamp = datetime.now(timezone.utc).isoformat()
    for entry in data.values():
        entry["source"] = "U.S. Department of Labor OFLC LCA disclosure data"
        entry["updated_at"] = stamp

    payload = {"updated_at": stamp, "source_url": url, "companies": data}
    path = resolve(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return {"companies": len(data), "source_url": url, "updated_at": stamp, "path": str(path)}
