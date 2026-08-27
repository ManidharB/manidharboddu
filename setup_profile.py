from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROFILE = ROOT / "profile" / "candidate_profile.json"
ANSWERS = ROOT / "profile" / "application_answers.json"


def ask(label: str, current: str = "", required: bool = True) -> str:
    shown = "" if current == "REVIEW_REQUIRED" else current
    while True:
        prompt = f"{label}" + (f" [{shown}]" if shown else "") + ": "
        value = input(prompt).strip()
        if not value and shown:
            return shown
        if value or not required:
            return value
        print("Please enter a value.")


def ask_yes_no(label: str, current: str = "") -> str:
    shown = current.lower() if current.lower() in {"yes", "no"} else ""
    while True:
        value = ask(label + " (yes/no)", shown).lower()
        if value in {"yes", "y"}: return "yes"
        if value in {"no", "n"}: return "no"
        print("Enter yes or no.")


def main():
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    answers = json.loads(ANSWERS.read_text(encoding="utf-8"))
    print("\nJobHunterX profile wizard")
    print("Answer these exactly as you would on a real job application.\n")

    profile["city"] = ask("City", profile.get("city", ""))
    profile["state"] = ask("State", profile.get("state", ""))
    profile["postal_code"] = ask("ZIP/postal code", profile.get("postal_code", ""))
    profile["linkedin_url"] = ask("LinkedIn URL", profile.get("linkedin_url", ""))

    print("\nEmployment/application answers")
    answers["authorized_to_work_in_us"] = ask_yes_no("Are you legally authorized to work in the U.S.?", answers.get("authorized_to_work_in_us", ""))
    answers["requires_sponsorship_now_or_future"] = ask_yes_no("Will you require employer sponsorship now or in the future?", answers.get("requires_sponsorship_now_or_future", ""))
    answers["willing_to_relocate"] = ask_yes_no("Are you willing to relocate?", answers.get("willing_to_relocate", ""))
    answers["desired_salary"] = ask("Desired salary/compensation response", answers.get("desired_salary", ""))
    answers["notice_period"] = ask("Notice period", answers.get("notice_period", ""))
    answers["start_date"] = ask("Earliest start date", answers.get("start_date", ""))
    answers["previously_employed_by_company"] = ask("Default answer for previously employed by company (usually no; use REVIEW_REQUIRED if you want per-company review)", answers.get("previously_employed_by_company", ""))
    answers["non_compete_restrictions"] = ask("Default non-compete restriction answer", answers.get("non_compete_restrictions", ""))
    answers["security_clearance"] = ask("Security clearance answer", answers.get("security_clearance", ""))

    PROFILE.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    ANSWERS.write_text(json.dumps(answers, indent=2), encoding="utf-8")
    print("\nSaved. Next run: python -m jobbot.cli doctor")


if __name__ == "__main__":
    main()
