from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

IMPACT_SCORE = {"Low": 1, "Medium": 2, "High": 3}
EFFORT_SCORE = {"Low": 1, "Medium": 2, "High": 3}


def get_impact_score(impact: str) -> int:
    return IMPACT_SCORE.get(impact, 1)


def get_effort_score(effort: str) -> int:
    return EFFORT_SCORE.get(effort, 1)


def get_days_since_created(created_at: str) -> int:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    return max(0, (now - created).days)


def calculate_innovation_score(
    votes: int,
    impact: str,
    effort: str,
    comment_count: int,
    days_since_created: int = 0,
) -> int:
    impact_score = get_impact_score(impact)
    effort_score = get_effort_score(effort)
    trendiness = 15 if days_since_created <= 7 else (8 if days_since_created <= 30 else 0)
    engagement = comment_count * 5
    return round(
        votes * 3 + impact_score * 20 - effort_score * 10 + engagement + trendiness
    )


def recalculate_use_case_score(use_case: dict[str, Any]) -> int:
    return calculate_innovation_score(
        use_case["votes"],
        use_case["impact"],
        use_case["effort"],
        len(use_case.get("comments", [])),
        get_days_since_created(use_case["createdAt"]),
    )


def derive_use_case_badges(use_case: dict[str, Any]) -> list[str]:
    badges: list[str] = []
    days = get_days_since_created(use_case["createdAt"])
    votes = use_case["votes"]
    impact = use_case["impact"]
    effort = use_case["effort"]

    if votes >= 15:
        badges.append("Crowd Favorite")
    if votes >= 8 and days <= 14:
        badges.append("Trending")
    if impact == "High":
        badges.append("High Impact")
    if impact == "High" and effort == "Low":
        badges.append("Quick Win")
    if impact == "High" and effort == "High":
        badges.append("Strategic Bet")
    return badges


def is_quick_win(use_case: dict[str, Any]) -> bool:
    return use_case["impact"] == "High" and use_case["effort"] == "Low"


def is_strategic_bet(use_case: dict[str, Any]) -> bool:
    return use_case["impact"] == "High" and use_case["effort"] == "High"
