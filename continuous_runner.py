from __future__ import annotations

import argparse
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

from jobbot.service import JobHunterService
from jobbot.utils import load_yaml, resolve

STATE_PATH = Path("data/continuous_state.json")


def _read_state() -> dict:
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else {}
    except Exception:
        return {}


def _write_state(payload: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _lookback_days(cfg: dict, state: dict) -> int:
    cs = cfg.get("continuous_search", {}) or {}
    initial = max(1, int(cs.get("initial_backfill_days", 30)))
    overlap = max(1, int(cs.get("incremental_overlap_days", 2)))
    raw = state.get("last_successful_search_at")
    if not raw:
        return initial
    try:
        last = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        elapsed_days = max(0.0, (datetime.now(timezone.utc) - last).total_seconds() / 86400)
        return min(31, max(overlap, math.ceil(elapsed_days) + overlap))
    except Exception:
        return overlap


def _set_incremental_window(svc: JobHunterService, days: int) -> None:
    sources = svc.config.setdefault("sources", {})
    # Use overlapping incremental windows so downtime does not create gaps.
    sources.setdefault("jobspipe", {})["posted_at_max_age_days"] = max(1, min(days, 31))
    sources.setdefault("usajobs", {})["date_posted_days"] = max(1, min(days, 30))
    brave = sources.setdefault("brave_web", {})
    brave["freshness"] = "pd" if days <= 1 else ("pw" if days <= 7 else "pm")


def run_cycle() -> dict:
    svc = JobHunterService()
    cs = svc.config.get("continuous_search", {}) or {}
    state = _read_state()
    days = _lookback_days(svc.config, state)
    _set_incremental_window(svc, days)

    started = datetime.now(timezone.utc)
    result: dict = {"started_at": started.isoformat(), "lookback_days": days}
    try:
        result["discover"] = svc.discover()
        if bool(cs.get("auto_rank", True)):
            result["rank"] = svc.rank()
        if bool(cs.get("auto_prepare", False)):
            result["prepare"] = svc.prepare()
        if bool(cs.get("auto_apply", False)):
            result["apply"] = svc.apply()
        result["stats"] = svc.store.stats()
        result["status"] = "success"
        now = datetime.now(timezone.utc)
        state.update({
            "last_successful_search_at": now.isoformat(),
            "last_run_at": now.isoformat(),
            "last_status": "success",
            "last_lookback_days": days,
            "total_cycles": int(state.get("total_cycles", 0)) + 1,
        })
    except Exception as exc:
        result["status"] = "error"
        result["error"] = f"{type(exc).__name__}: {exc}"
        now = datetime.now(timezone.utc)
        state.update({"last_run_at": now.isoformat(), "last_status": "error", "last_error": result["error"]})
    _write_state(state)

    report_dir = resolve("output/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report = report_dir / f"continuous_search_{stamp}.json"
    report.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    return result


def daemon() -> None:
    while True:
        cfg = load_yaml("config.yaml")
        cs = cfg.get("continuous_search", {}) or {}
        if not bool(cs.get("enabled", True)):
            time.sleep(60)
            continue
        interval_hours = max(1, float(cs.get("interval_hours", 24)))
        state = _read_state()
        due = True
        raw = state.get("last_run_at")
        if raw:
            try:
                last = datetime.fromisoformat(raw.replace("Z", "+00:00"))
                if last.tzinfo is None:
                    last = last.replace(tzinfo=timezone.utc)
                due = (datetime.now(timezone.utc) - last).total_seconds() >= interval_hours * 3600
            except Exception:
                due = True
        if due:
            print(json.dumps(run_cycle(), indent=2, default=str), flush=True)
        time.sleep(60)


def main() -> None:
    ap = argparse.ArgumentParser(description="Run JobHunterX continuously with incremental daily/interval searches.")
    ap.add_argument("--daemon", action="store_true", help="Stay alive and run whenever the configured interval is due.")
    args = ap.parse_args()
    if args.daemon:
        daemon()
    else:
        print(json.dumps(run_cycle(), indent=2, default=str))


if __name__ == "__main__":
    main()
