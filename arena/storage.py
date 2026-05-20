from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STATE_FILE = DATA_DIR / "arena_state.json"


def _default_state() -> dict[str, Any]:
    return {
        "useCases": [],
        "userVotes": {},
        "knownUsers": [],
    }


def load_state() -> dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        return _default_state()
    try:
        with STATE_FILE.open(encoding="utf-8") as f:
            raw = json.load(f)
        state = _default_state()
        state["useCases"] = [_migrate_use_case(uc) for uc in raw.get("useCases", [])]
        state["userVotes"] = raw.get("userVotes") or {}
        state["knownUsers"] = raw.get("knownUsers") or []
        return state
    except (json.JSONDecodeError, OSError):
        return _default_state()


def save_state(state: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def _migrate_use_case(uc: dict[str, Any]) -> dict[str, Any]:
    from arena.auth import normalize_email
    from arena.constants import is_known_department, normalize_department

    department = normalize_department(uc.get("department", ""))
    if is_known_department(department):
        uc["department"] = department
    uc.setdefault("voterEmails", [])
    uc.setdefault("voterIds", [])
    uc.setdefault("creatorMessages", [])
    uc.setdefault("comments", [])
    if not uc.get("submitterEmail") and "@" in (uc.get("submitterId") or ""):
        uc["submitterEmail"] = normalize_email(uc["submitterId"])
    else:
        uc.setdefault("submitterEmail", "")
    return uc
